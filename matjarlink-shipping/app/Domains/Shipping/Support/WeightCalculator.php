<?php

declare(strict_types=1);

namespace App\Domains\Shipping\Support;

use App\Domains\Shipping\DTOs\PackageData;

/**
 * الوزن القابل للفوترة = الأكبر من (الوزن الفعلي، الوزن الحجمي).
 * تجاهل هذا يجعل كل سعر معروض للمستخدم خاطئاً، ويجعل فاتورة الشركة مفاجأة.
 */
final class WeightCalculator
{
    /** @param list<PackageData> $packages */
    public static function actual(array $packages): float
    {
        return round(array_sum(array_map(
            static fn (PackageData $p): float => $p->weightKg * max(1, $p->quantity),
            $packages,
        )), 3);
    }

    /** @param list<PackageData> $packages */
    public static function volumetric(array $packages, int $divisor): float
    {
        if ($divisor <= 0) {
            return 0.0;
        }

        $total = 0.0;

        foreach ($packages as $p) {
            if ($p->lengthCm && $p->widthCm && $p->heightCm) {
                $total += ($p->lengthCm * $p->widthCm * $p->heightCm) / $divisor * max(1, $p->quantity);
            }
        }

        return round($total, 3);
    }

    /** @param list<PackageData> $packages */
    public static function billable(array $packages, ?int $divisor = null): float
    {
        $divisor ??= (int) config('shipping.weight.volumetric_divisor', 5000);

        return round(max(
            self::actual($packages),
            self::volumetric($packages, $divisor),
        ), 3);
    }
}
