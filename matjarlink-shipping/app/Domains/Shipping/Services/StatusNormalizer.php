<?php

declare(strict_types=1);

namespace App\Domains\Shipping\Services;

use App\Domains\Shipping\Enums\ShipmentStatus;
use App\Domains\Shipping\Models\CarrierStatusMap;
use Illuminate\Support\Facades\Cache;
use Illuminate\Support\Facades\Log;

/**
 * يترجم رمز حالة الشركة إلى الحالة الداخلية.
 * الرمز غير المعروف لا يُسقَط ولا يُخمَّن: يُسجَّل كـ exception ويظهر في
 * قائمة «رموز تحتاج تعيين» لفريق العمليات.
 */
final class StatusNormalizer
{
    private const CACHE_TTL = 3600;

    public function normalize(int $carrierId, ?string $carrierCode, ?string $carrierText = null): ShipmentStatus
    {
        if ($carrierCode === null || $carrierCode === '') {
            return ShipmentStatus::Exception;
        }

        $map = $this->mapFor($carrierId);
        $key = strtoupper(trim($carrierCode));

        if (isset($map[$key])) {
            return ShipmentStatus::from($map[$key]);
        }

        Log::warning('shipping.unmapped_carrier_status', [
            'carrier_id' => $carrierId,
            'code' => $carrierCode,
            'text' => $carrierText,
        ]);

        return ShipmentStatus::Exception;
    }

    /** @return array<string, string> */
    public function mapFor(int $carrierId): array
    {
        return Cache::remember(
            "shipping:status_map:{$carrierId}",
            self::CACHE_TTL,
            static fn (): array => CarrierStatusMap::query()
                ->where('carrier_id', $carrierId)
                ->pluck('internal_status', 'carrier_status_code')
                ->mapWithKeys(static fn ($status, $code): array => [
                    strtoupper((string) $code) => $status instanceof ShipmentStatus ? $status->value : (string) $status,
                ])
                ->all(),
        );
    }

    public function forget(int $carrierId): void
    {
        Cache::forget("shipping:status_map:{$carrierId}");
    }
}
