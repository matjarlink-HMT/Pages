<?php

declare(strict_types=1);

namespace App\Domains\Shipping\Services;

use App\Domains\Shipping\DTOs\TrackingEventData;
use App\Domains\Shipping\Enums\ShipmentStatus;
use App\Domains\Shipping\Events\ShipmentStatusChanged;
use App\Domains\Shipping\Models\Shipment;
use App\Domains\Shipping\Models\ShipmentEvent;
use App\Domains\Shipping\StateMachine\ShipmentStateMachine;
use Illuminate\Database\QueryException;
use Illuminate\Support\Facades\DB;

/**
 * البوابة الوحيدة لتغيير حالة الشحنة.
 *
 * لا مكان آخر في الوحدة يكتب shipments.status مباشرة — الحالة نتيجة
 * لتسجيل حدث، لا حقل يُعدَّل. هذا ما يجعل التاريخ قابلاً للتدقيق وإعادة البناء.
 */
final class ShipmentEventRecorder
{
    public function __construct(
        private readonly ShipmentStateMachine $stateMachine,
        private readonly SlaEngine $sla,
    ) {}

    /** @param list<TrackingEventData> $events */
    public function recordMany(Shipment $shipment, array $events): int
    {
        $recorded = 0;

        /* الترتيب الزمني لا ترتيب الوصول: أحداث الـ Webhook تصل مختلطة. */
        usort($events, static fn (TrackingEventData $a, TrackingEventData $b): int
            => $a->occurredAt <=> $b->occurredAt);

        foreach ($events as $event) {
            if ($this->record($shipment, $event)) {
                $recorded++;
            }
        }

        return $recorded;
    }

    public function record(Shipment $shipment, TrackingEventData $event): bool
    {
        $hash = $event->hash($shipment->id);

        try {
            $created = DB::transaction(function () use ($shipment, $event, $hash): bool {
                $exists = ShipmentEvent::query()
                    ->where('shipment_id', $shipment->id)
                    ->where('hash', $hash)
                    ->exists();

                if ($exists) {
                    return false;
                }

                ShipmentEvent::query()->create([
                    'shipment_id' => $shipment->id,
                    'status' => $event->status,
                    'carrier_status_code' => $event->carrierStatusCode,
                    'carrier_status_text' => $event->carrierStatusText,
                    'description_ar' => $event->descriptionAr ?? $event->description(),
                    'description_en' => $event->descriptionEn,
                    'location' => $event->location,
                    'occurred_at' => $event->occurredAt,
                    'source' => $event->source,
                    'actor_id' => auth()->id(),
                    'hash' => $hash,
                    'raw_payload' => $event->raw ?: null,
                ]);

                return true;
            });
        } catch (QueryException $e) {
            /* سباق على القيد الفريد: حدثان متطابقان وصلا في اللحظة نفسها. */
            if ($this->isDuplicate($e)) {
                return false;
            }

            throw $e;
        }

        if ($created) {
            $this->applyStatus($shipment, $event);
        }

        return $created;
    }

    private function applyStatus(Shipment $shipment, TrackingEventData $event): void
    {
        $current = $shipment->status;

        $isNewer = $shipment->status_updated_at === null
            || $event->occurredAt->greaterThanOrEqualTo($shipment->status_updated_at);

        $next = $this->stateMachine->resolve($current, $event->status, $isNewer);

        /* آخر تحديث يتغيّر حتى لو لم تتغيّر الحالة — يمنع وسم الشحنة «صامتة». */
        $shipment->forceFill([
            'last_synced_at' => now(),
            'is_stale' => false,
        ]);

        if ($next === $current) {
            $shipment->save();

            return;
        }

        $shipment->forceFill(array_filter([
            'status' => $next,
            'status_updated_at' => $event->occurredAt,
            'picked_up_at' => $next === ShipmentStatus::PickedUp ? $event->occurredAt : $shipment->picked_up_at,
            'delivered_at' => $next === ShipmentStatus::Delivered ? $event->occurredAt : $shipment->delivered_at,
            'returned_at' => $next === ShipmentStatus::Returned ? $event->occurredAt : $shipment->returned_at,
            'delivery_attempts' => $next === ShipmentStatus::FailedAttempt
                ? $shipment->delivery_attempts + 1
                : $shipment->delivery_attempts,
        ], static fn ($v): bool => $v !== null));

        $shipment->forceFill([
            'is_delayed' => $this->sla->isDelayed($shipment),
            'next_sync_at' => $this->sla->nextSyncAt($shipment),
        ])->save();

        event(new ShipmentStatusChanged($shipment->fresh(), $current, $next));
    }

    private function isDuplicate(QueryException $e): bool
    {
        return in_array($e->getCode(), ['23000', '23505'], true);
    }
}
