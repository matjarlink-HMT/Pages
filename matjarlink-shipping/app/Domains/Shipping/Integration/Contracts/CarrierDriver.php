<?php

declare(strict_types=1);

namespace App\Domains\Shipping\Integration\Contracts;

use App\Domains\Shipping\DTOs\CancellationResult;
use App\Domains\Shipping\DTOs\CarrierCapabilities;
use App\Domains\Shipping\DTOs\CarrierShipmentResult;
use App\Domains\Shipping\DTOs\ConnectionResult;
use App\Domains\Shipping\DTOs\LabelFile;
use App\Domains\Shipping\DTOs\RateRequest;
use App\Domains\Shipping\DTOs\ShipmentRequest;
use App\Domains\Shipping\Enums\LabelFormat;
use App\Domains\Shipping\Models\StoreCarrierAccount;

/**
 * العقد الوحيد الذي تعرفه النواة عن شركات الشحن.
 *
 * إضافة «أسياد» أو «أرامكس» أو مندوب محلي بلا API = تنفيذ هذا العقد.
 * لا يوجد شرط باسم شركة في أي مكان خارج مجلد Drivers — وهذا هو معيار
 * نجاح المعمارية.
 */
interface CarrierDriver
{
    public function forAccount(StoreCarrierAccount $account): static;

    /** قدرات الشركة — تُشتق منها الواجهة والإجراءات المتاحة. */
    public function capabilities(): CarrierCapabilities;

    /** مخطط بيانات الاعتماد لبناء نموذج الربط ديناميكياً بلا نموذج مكتوب لكل شركة. */
    public static function credentialSchema(): array;

    public function testConnection(): ConnectionResult;

    /** @return list<\App\Domains\Shipping\DTOs\RateQuoteData> */
    public function getRates(RateRequest $request): array;

    /** يجب أن يكون Idempotent عبر $request->idempotencyKey(). */
    public function createShipment(ShipmentRequest $request): CarrierShipmentResult;

    public function fetchLabel(string $carrierShipmentId, LabelFormat $format): ?LabelFile;

    /** @return list<\App\Domains\Shipping\DTOs\TrackingEventData> */
    public function track(string $trackingNumber): array;

    public function cancelShipment(string $carrierShipmentId): CancellationResult;

    /** خريطة حالات الشركة إلى الحالات الداخلية: ['DLV' => 'delivered', ...] */
    public function statusMap(): array;
}
