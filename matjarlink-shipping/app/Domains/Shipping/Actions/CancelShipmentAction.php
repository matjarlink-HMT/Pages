<?php

declare(strict_types=1);

namespace App\Domains\Shipping\Actions;

use App\Domains\Shipping\DTOs\TrackingEventData;
use App\Domains\Shipping\Enums\ShipmentEventSource;
use App\Domains\Shipping\Enums\ShipmentStatus;
use App\Domains\Shipping\Events\ShipmentCancelled;
use App\Domains\Shipping\Integration\CarrierRegistry;
use App\Domains\Shipping\Models\Shipment;
use App\Domains\Shipping\Services\ShipmentEventRecorder;
use RuntimeException;
use Throwable;

final readonly class CancelShipmentAction
{
    public function __construct(
        private CarrierRegistry $registry,
        private ShipmentEventRecorder $recorder,
    ) {}

    public function execute(Shipment $shipment, ?string $reason = null): Shipment
    {
        if ($shipment->status->isTerminal()) {
            throw new RuntimeException(__('shipping.errors.already_terminal'));
        }

        $feeRefunded = false;

        /* نُخطر الشركة إن دعمت الإلغاء، وفشل الإخطار لا يمنع الإلغاء محلياً. */
        if ($shipment->carrier_shipment_id !== null && $shipment->carrier->capabilities()->cancellation) {
            try {
                $result = $this->registry->for($shipment->account)->cancelShipment($shipment->carrier_shipment_id);
                $feeRefunded = $result->feeRefunded;
            } catch (Throwable) {
                $feeRefunded = false;
            }
        }

        $shipment->forceFill([
            'cancelled_at' => now(),
            'cancelled_by' => auth()->id(),
            'is_delayed' => false,
            'is_stale' => false,
            'next_sync_at' => null,
        ])->save();

        $this->recorder->record($shipment, new TrackingEventData(
            status: ShipmentStatus::Cancelled,
            occurredAt: now(),
            descriptionAr: $reason ?? __('shipping.events.cancelled'),
            source: ShipmentEventSource::Manual,
        ));

        $shipment = $shipment->fresh();

        event(new ShipmentCancelled($shipment, $reason, $feeRefunded));

        return $shipment;
    }
}
