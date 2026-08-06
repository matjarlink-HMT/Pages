<?php

declare(strict_types=1);

namespace App\Domains\Shipping\Contracts;

use App\Domains\Shipping\DTOs\OrderSnapshot;
use App\Domains\Shipping\Enums\ShipmentStatus;
use App\Domains\Shipping\Models\Shipment;

/**
 * نقطة التكامل الوحيدة مع وحدة الطلبات.
 * وحدة الشحن لا تستورد موديل الطلب ولا تعرف جداوله — تنفّذ المنصة هذا العقد
 * وتُسجّله في الحاوية، فيبقى فصل الوحدتين قابلاً للفحص الآلي.
 */
interface OrderBridge
{
    /** بيانات الطلب لتعبئة الشحنة مسبقاً — تحقيق وعد «لا إدخال مرتين». */
    public function snapshot(int $orderId): ?OrderSnapshot;

    /** حفظ رقم التتبع ورابطه داخل الطلب فور إنشاء الشحنة. */
    public function attachShipment(int $orderId, Shipment $shipment): void;

    /** مزامنة حالة الطلب مع حالة الشحنة (تم التسليم / أُرجعت / أُلغيت). */
    public function syncStatus(int $orderId, ShipmentStatus $status): void;
}
