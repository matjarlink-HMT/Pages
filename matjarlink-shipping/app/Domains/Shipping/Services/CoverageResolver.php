<?php

declare(strict_types=1);

namespace App\Domains\Shipping\Services;

use App\Domains\Shipping\Models\ShippingZone;
use App\Domains\Shipping\Models\StoreCarrierAccount;
use Illuminate\Support\Collection;

/**
 * يجيب سؤالاً واحداً: هل يستطيع هذا الحساب التوصيل إلى هذه الوجهة؟
 * الترشيح قبل التسعير — لا نستهلك API شركة لا تغطي الوجهة أصلاً.
 */
final class CoverageResolver
{
    public function covers(StoreCarrierAccount $account, string $governorate, ?string $wilayat = null): bool
    {
        $zones = $this->zonesFor($account);

        /* بلا مناطق معرّفة = تغطية كاملة (السلوك الافتراضي عند الربط). */
        if ($zones->isEmpty()) {
            return true;
        }

        return $zones->contains(
            static fn (ShippingZone $zone): bool => $zone->covers($governorate, $wilayat),
        );
    }

    /** @return Collection<int, ShippingZone> */
    public function zonesFor(StoreCarrierAccount $account): Collection
    {
        return ShippingZone::query()
            ->where('is_active', true)
            ->whereHas('rules.card', static fn ($q) => $q->where('store_carrier_account_id', $account->id))
            ->with('regions')
            ->get();
    }

    public function resolveZone(StoreCarrierAccount $account, string $governorate, ?string $wilayat = null): ?ShippingZone
    {
        return $this->zonesFor($account)
            ->first(static fn (ShippingZone $zone): bool => $zone->covers($governorate, $wilayat));
    }
}
