<?php

declare(strict_types=1);

namespace App\Domains\Shipping\Listeners;

use App\Domains\Shipping\Enums\ShipmentStatus;
use App\Domains\Shipping\Events\ShipmentStatusChanged;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Support\Facades\Log;

/**
 * الوحدة لا تدير المخزون: تُعلن الحدث فقط وتترك القرار لوحدة المخزون.
 * حدّ الوحدة معلن في docs/shipping-module/01-analysis.md §5.
 */
final class ReleaseInventoryOnDelivery implements ShouldQueue
{
    public string $queue = 'shipping-sync';

    public function handle(ShipmentStatusChanged $event): void
    {
        if ($event->to !== ShipmentStatus::Delivered) {
            return;
        }

        Log::info('shipping.inventory_release_requested', [
            'shipment_id' => $event->shipment->id,
            'order_id' => $event->shipment->order_id,
        ]);

        /* تستمع وحدة المخزون لهذا الحدث وتقرّر ما يناسب سير عملها. */
    }
}
