<?php

declare(strict_types=1);

namespace App\Domains\Shipping\Contracts;

use App\Domains\Shipping\DTOs\OrderSnapshot;
use App\Domains\Shipping\Enums\ShipmentStatus;
use App\Domains\Shipping\Models\Shipment;

/**
 * تحقيق فارغ يسمح بتشغيل الوحدة واختبارها قبل ربطها بوحدة الطلبات.
 * التنفيذ الحقيقي يُسجَّل في ServiceProvider الخاص بالمنصة.
 */
final class NullOrderBridge implements OrderBridge
{
    public function snapshot(int $orderId): ?OrderSnapshot
    {
        return null;
    }

    public function attachShipment(int $orderId, Shipment $shipment): void {}

    public function syncStatus(int $orderId, ShipmentStatus $status): void {}
}
