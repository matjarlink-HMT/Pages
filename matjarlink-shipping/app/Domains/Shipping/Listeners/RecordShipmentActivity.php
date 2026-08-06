<?php

declare(strict_types=1);

namespace App\Domains\Shipping\Listeners;

use App\Domains\Shipping\Events\ShipmentCancelled;
use App\Domains\Shipping\Events\ShipmentCreated;
use App\Domains\Shipping\Events\ShipmentStatusChanged;
use Illuminate\Support\Facades\Log;

/**
 * سجل النشاط. يستخدم نظام المنصة (spatie/activitylog) إن كان مثبّتاً،
 * وإلا يكتب في سجل التطبيق — فلا يضيع أثر أي عملية في أي حال.
 */
final class RecordShipmentActivity
{
    public function created(ShipmentCreated $event): void
    {
        $this->write('shipment.created', $event->shipment->id, [
            'reference' => $event->shipment->reference,
            'carrier_id' => $event->shipment->carrier_id,
            'cost' => $event->shipment->total_cost,
        ]);
    }

    public function statusChanged(ShipmentStatusChanged $event): void
    {
        $this->write('shipment.status_changed', $event->shipment->id, [
            'from' => $event->from->value,
            'to' => $event->to->value,
        ]);
    }

    public function cancelled(ShipmentCancelled $event): void
    {
        $this->write('shipment.cancelled', $event->shipment->id, [
            'reason' => $event->reason,
            'fee_refunded' => $event->feeRefunded,
        ]);
    }

    private function write(string $action, int $subjectId, array $properties): void
    {
        if (function_exists('activity')) {
            activity('shipping')
                ->withProperties($properties + ['ip' => request()->ip()])
                ->event($action)
                ->log($action);

            return;
        }

        Log::channel(config('logging.default'))->info($action, [
            'shipment_id' => $subjectId,
            'user_id' => auth()->id(),
        ] + $properties);
    }
}
