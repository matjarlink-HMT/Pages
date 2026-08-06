<?php

declare(strict_types=1);

namespace App\Domains\Shipping\Listeners;

use App\Domains\Shipping\Contracts\OrderBridge;
use App\Domains\Shipping\Events\ShipmentStatusChanged;
use Illuminate\Contracts\Queue\ShouldQueue;

/**
 * الأثر الوحيد على وحدة الطلبات يمر من هنا عبر العقد OrderBridge.
 * لا تعرف وحدة الشحن جداول الطلبات ولا تستورد موديلاتها.
 */
final class UpdateOrderFromShipment implements ShouldQueue
{
    public string $queue = 'shipping-sync';

    public function __construct(private readonly OrderBridge $orders) {}

    public function handle(ShipmentStatusChanged $event): void
    {
        if ($event->shipment->order_id === null) {
            return;
        }

        $this->orders->syncStatus($event->shipment->order_id, $event->to);
    }
}
