<?php

declare(strict_types=1);

namespace App\Domains\Shipping\Support;

use App\Domains\Shipping\Models\Shipment;
use Illuminate\Support\Facades\DB;

/** مرجع مقروء للبشر: SHP-2026-000123 — يُذكر في المكالمات ويُبحث به. */
final class ReferenceGenerator
{
    public static function next(int $storeId): string
    {
        $prefix = (string) config('shipping.reference_prefix', 'SHP');
        $year = now()->year;

        $sequence = DB::transaction(static function () use ($storeId, $year): int {
            $last = Shipment::query()
                ->withoutGlobalScopes()
                ->where('store_id', $storeId)
                ->whereYear('created_at', $year)
                ->lockForUpdate()
                ->max('store_sequence');

            return (int) $last + 1;
        });

        return sprintf('%s-%d-%06d', $prefix, $year, $sequence);
    }
}
