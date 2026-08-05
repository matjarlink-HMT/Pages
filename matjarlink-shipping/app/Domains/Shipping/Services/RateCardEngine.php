<?php

declare(strict_types=1);

namespace App\Domains\Shipping\Services;

use App\Domains\Shipping\DTOs\RateQuoteData;
use App\Domains\Shipping\DTOs\RateRequest;
use App\Domains\Shipping\Models\ShippingRateCard;
use App\Domains\Shipping\Models\ShippingRateRule;
use App\Domains\Shipping\Models\StoreCarrierAccount;
use App\Domains\Shipping\Support\OmanGeo;

/**
 * تسعير محلي للشركات بلا API.
 * يُرجع RateQuoteData بنفس شكل عرض الـ API تماماً، فتعامله بقية الوحدة
 * والواجهة معاملة واحدة ولا يظهر أي فرق للمستخدم.
 */
final class RateCardEngine
{
    public function __construct(private readonly CoverageResolver $coverage) {}

    public function hasActiveCard(StoreCarrierAccount $account): bool
    {
        return ShippingRateCard::query()
            ->where('store_carrier_account_id', $account->id)
            ->effective()
            ->exists();
    }

    /** @return list<RateQuoteData> */
    public function quote(StoreCarrierAccount $account, RateRequest $request): array
    {
        $zone = $this->coverage->resolveZone(
            $account,
            $request->destination->governorate,
            $request->destination->wilayat,
        );

        if ($zone === null) {
            return [];
        }

        $weight = $request->billableWeight($account->carrier->capabilities()->volumetricDivisor);
        $isRemote = $request->isRemoteDestination() || OmanGeo::isRemote($request->destination->governorate);

        $rules = ShippingRateRule::query()
            ->where('zone_id', $zone->id)
            ->whereHas('card', static fn ($q) => $q->where('store_carrier_account_id', $account->id)->effective())
            ->when($request->serviceCode !== null, fn ($q) => $q->where('service_code', $request->serviceCode))
            ->orderByDesc('priority')
            ->get()
            ->filter(static fn (ShippingRateRule $rule): bool => $rule->coversWeight($weight))
            /* قاعدة واحدة لكل خدمة: الأعلى أولوية تفوز. */
            ->unique('service_code');

        $quotes = [];

        foreach ($rules as $rule) {
            $quotes[] = $this->buildQuote($account, $rule, $request, $weight, $isRemote);
        }

        usort($quotes, static fn (RateQuoteData $a, RateQuoteData $b): int => $a->price <=> $b->price);

        return $quotes;
    }

    private function buildQuote(
        StoreCarrierAccount $account,
        ShippingRateRule $rule,
        RateRequest $request,
        float $weight,
        bool $isRemote,
    ): RateQuoteData {
        $base = (float) $rule->base_price;

        $extraKg = max(0.0, $weight - (float) $rule->min_weight_kg);
        $extra = round($extraKg * (float) $rule->price_per_extra_kg, 3);

        $remote = $isRemote ? (float) $rule->remote_area_surcharge : 0.0;

        $cod = 0.0;
        if ($request->isCod) {
            $cod = round(
                (float) $rule->cod_fee_fixed + ($request->codAmount * (float) $rule->cod_fee_percent / 100),
                3,
            );
        }

        $insurance = round($request->declaredValue * (float) $rule->insurance_percent / 100, 3);

        $subtotal = $base + $extra + $remote + $cod + $insurance;
        $fuel = round($subtotal * (float) $rule->fuel_surcharge_percent / 100, 3);
        $subtotal += $fuel;

        /* هامش التاجر يُطبَّق قبل الضريبة. */
        $markup = $this->markup($account, $subtotal);
        $subtotal += $markup;

        $vat = round($subtotal * (float) $rule->vat_percent / 100, 3);
        $total = round($subtotal + $vat, 3);

        return new RateQuoteData(
            carrierId: $account->carrier_id,
            accountId: $account->id,
            carrierCode: $account->carrier->code,
            carrierName: $account->carrier->name(),
            serviceCode: (string) $rule->service_code,
            serviceName: (string) ($rule->service_name ?: $rule->service_code),
            price: $total,
            etaMinDays: (int) $rule->eta_min_days + ($isRemote ? 1 : 0),
            etaMaxDays: (int) $rule->eta_max_days + ($isRemote ? 2 : 0),
            currency: (string) config('shipping.currency', 'OMR'),
            features: $this->features($account, $request),
            source: 'rate_card',
            breakdown: array_filter([
                'base' => $base, 'extra_weight' => $extra, 'remote_area' => $remote,
                'cod_fee' => $cod, 'insurance' => $insurance, 'fuel' => $fuel,
                'markup' => $markup, 'vat' => $vat,
            ], static fn (float $v): bool => $v > 0),
        );
    }

    private function markup(StoreCarrierAccount $account, float $amount): float
    {
        return match ($account->markup_type) {
            'percent' => round($amount * (float) $account->markup_value / 100, 3),
            'fixed' => (float) $account->markup_value,
            default => 0.0,
        };
    }

    /** @return list<string> */
    private function features(StoreCarrierAccount $account, RateRequest $request): array
    {
        $caps = $account->carrier->capabilities();

        return array_values(array_filter([
            $caps->tracking ? __('shipping.features.tracking') : null,
            $request->isCod && $caps->cod ? __('shipping.features.cod') : null,
            $caps->insurance ? __('shipping.features.insurance') : null,
            $caps->pickup ? __('shipping.features.pickup') : null,
        ]));
    }
}
