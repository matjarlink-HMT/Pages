<?php

declare(strict_types=1);

namespace App\Domains\Shipping\Services;

use App\Domains\Shipping\Contracts\OrderBridge;
use App\Domains\Shipping\DTOs\AddressData;
use App\Domains\Shipping\DTOs\CarrierShipmentResult;
use App\Domains\Shipping\DTOs\ItemData;
use App\Domains\Shipping\DTOs\PackageData;
use App\Domains\Shipping\DTOs\ShipmentRequest;
use App\Domains\Shipping\DTOs\TrackingEventData;
use App\Domains\Shipping\Enums\PaymentType;
use App\Domains\Shipping\Enums\ShipmentEventSource;
use App\Domains\Shipping\Enums\ShipmentStatus;
use App\Domains\Shipping\Events\ShipmentCreated;
use App\Domains\Shipping\Integration\CarrierRegistry;
use App\Domains\Shipping\Models\Shipment;
use App\Domains\Shipping\Models\StoreCarrierAccount;
use App\Domains\Shipping\Support\ReferenceGenerator;
use App\Domains\Shipping\Support\WeightCalculator;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Log;
use Illuminate\Support\Str;
use Throwable;

/**
 * إنشاء الشحنة — الخدمة الأهم في الوحدة.
 *
 * ترتيب الخطوات مقصود: **الكتابة المحلية قبل النداء الخارجي**.
 * فقدان بوليصة أُنشئت فعلاً لدى الشركة أسوأ بكثير من صف محلي معلّق،
 * لذا تُكتب الشحنة أولاً بحالة pending_carrier ثم تُحدَّث بنتيجة النداء.
 */
final class ShipmentCreationService
{
    public function __construct(
        private readonly CarrierRegistry $registry,
        private readonly CoverageResolver $coverage,
        private readonly ShipmentEventRecorder $recorder,
        private readonly SlaEngine $sla,
        private readonly OrderBridge $orders,
    ) {}

    public function create(int $storeId, ShipmentRequest $request): Shipment
    {
        $account = StoreCarrierAccount::query()
            ->forStore($storeId)
            ->with('carrier')
            ->findOrFail($request->accountId);

        $this->guardCoverage($account, $request);

        $idempotencyKey = $request->idempotencyKey();

        /* الحماية من الازدواج قبل أي عمل: نفس الطلب لا يُنشئ بوليصتين. */
        $existing = Shipment::query()
            ->forStore($storeId)
            ->where('idempotency_key', $idempotencyKey)
            ->first();

        if ($existing !== null) {
            Log::info('shipping.duplicate_create_prevented', [
                'shipment_id' => $existing->id,
                'order_id' => $request->orderId,
            ]);

            return $existing;
        }

        $shipment = $this->persistLocally($storeId, $account, $request, $idempotencyKey);

        /* النداء الخارجي خارج المعاملة: لا نُبقي قفلاً مفتوحاً على شبكة بطيئة. */
        $result = $this->callCarrier($account, $request);

        return $this->applyResult($shipment, $result, $request);
    }

    private function guardCoverage(StoreCarrierAccount $account, ShipmentRequest $request): void
    {
        $covered = $this->coverage->covers(
            $account,
            $request->receiver->governorate,
            $request->receiver->wilayat,
        );

        if (! $covered) {
            throw new \App\Domains\Shipping\Integration\Exceptions\DestinationNotCoveredException(
                $request->receiver->governorate,
            );
        }
    }

    private function persistLocally(
        int $storeId,
        StoreCarrierAccount $account,
        ShipmentRequest $request,
        string $idempotencyKey,
    ): Shipment {
        return DB::transaction(function () use ($storeId, $account, $request, $idempotencyKey): Shipment {
            $divisor = $account->carrier->capabilities()->volumetricDivisor;
            $reference = ReferenceGenerator::next($storeId);

            $shipment = Shipment::query()->create([
                'store_id' => $storeId,
                'uuid' => (string) Str::uuid(),
                'reference' => $reference,
                'store_sequence' => (int) substr($reference, -6),
                'order_id' => $request->orderId,
                'carrier_id' => $account->carrier_id,
                'store_carrier_account_id' => $account->id,
                'service_code' => $request->serviceCode ?? $account->default_service_code,
                'status' => ShipmentStatus::PendingCarrier,
                'status_updated_at' => now(),
                'idempotency_key' => $idempotencyKey,
                'pieces_count' => $request->piecesCount(),
                'total_weight_kg' => WeightCalculator::actual($request->packages),
                'billable_weight_kg' => $request->billableWeight($divisor),
                'declared_value' => $request->declaredValue,
                'currency' => $request->currency,
                'is_cod' => $request->isCod,
                'cod_amount' => $request->isCod ? $request->codAmount : 0,
                'payment_type' => $request->isCod ? PaymentType::Cod : PaymentType::Prepaid,
                'delivery_attempts' => 0,
                'notes' => $request->notes,
                'internal_notes' => $request->internalNotes,
                'created_by' => auth()->id(),
            ]);

            $this->storeAddress($shipment, 'sender', $request->sender);
            $this->storeAddress($shipment, 'receiver', $request->receiver);
            $this->storePackages($shipment, $request->packages, $divisor);
            $this->storeItems($shipment, $request->items);

            return $shipment;
        });
    }

    private function callCarrier(StoreCarrierAccount $account, ShipmentRequest $request): CarrierShipmentResult
    {
        try {
            return $this->registry->for($account)->createShipment($request);
        } catch (Throwable $e) {
            Log::error('shipping.create_failed', [
                'account_id' => $account->id,
                'order_id' => $request->orderId,
                'error' => $e->getMessage(),
            ]);

            return CarrierShipmentResult::failure($e->getMessage(), retryable: true);
        }
    }

    private function applyResult(Shipment $shipment, CarrierShipmentResult $result, ShipmentRequest $request): Shipment
    {
        if (! $result->success) {
            $shipment->forceFill([
                'status' => ShipmentStatus::CarrierError,
                'status_updated_at' => now(),
                'carrier_error' => $result->errorMessage,
                'sync_failures' => $shipment->sync_failures + 1,
            ])->save();

            $this->recorder->record($shipment, new TrackingEventData(
                status: ShipmentStatus::CarrierError,
                occurredAt: now(),
                descriptionAr: __('shipping.events.carrier_error', ['reason' => (string) $result->errorMessage]),
                source: ShipmentEventSource::System,
            ));

            return $shipment->fresh();
        }

        $etaDays = $result->etaMaxDays ?? (int) config('shipping.default_eta_days', 3);

        $shipment->forceFill([
            'status' => ShipmentStatus::Created,
            'status_updated_at' => now(),
            'tracking_number' => $result->trackingNumber,
            'carrier_shipment_id' => $result->carrierShipmentId,
            'quoted_cost' => $result->cost,
            'actual_cost' => $result->cost,
            'total_cost' => $result->cost,
            'cost_breakdown' => $result->costBreakdown ?: null,
            'promised_delivery_at' => $this->sla->promisedAt($etaDays),
            'carrier_error' => null,
        ]);

        $shipment->forceFill(['next_sync_at' => $this->sla->nextSyncAt($shipment)])->save();

        $this->recorder->record($shipment, new TrackingEventData(
            status: ShipmentStatus::Created,
            occurredAt: now(),
            descriptionAr: __('shipping.events.created'),
            source: ShipmentEventSource::System,
        ));

        $shipment = $shipment->fresh();

        /* حفظ رقم التتبع داخل الطلب فوراً — لا يرى العميل طلباً بلا تتبع. */
        if ($request->orderId !== null) {
            $this->orders->attachShipment($request->orderId, $shipment);
        }

        event(new ShipmentCreated($shipment));

        return $shipment;
    }

    private function storeAddress(Shipment $shipment, string $type, AddressData $address): void
    {
        $shipment->addresses()->create(['type' => $type] + $address->toArray());
    }

    /** @param list<PackageData> $packages */
    private function storePackages(Shipment $shipment, array $packages, int $divisor): void
    {
        $pieceNo = 1;

        foreach ($packages as $package) {
            for ($i = 0; $i < max(1, $package->quantity); $i++) {
                $shipment->packages()->create([
                    'piece_no' => $pieceNo,
                    'weight_kg' => $package->weightKg,
                    'length_cm' => $package->lengthCm,
                    'width_cm' => $package->widthCm,
                    'height_cm' => $package->heightCm,
                    'volumetric_weight_kg' => $package->volumetricWeight($divisor),
                    'barcode' => $shipment->reference.'-'.$pieceNo,
                    'description' => $package->description,
                ]);

                $pieceNo++;
            }
        }
    }

    /** @param list<ItemData> $items */
    private function storeItems(Shipment $shipment, array $items): void
    {
        foreach ($items as $item) {
            $shipment->items()->create($item->toArray());
        }
    }
}
