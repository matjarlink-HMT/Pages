<?php

declare(strict_types=1);

namespace App\Domains\Shipping\Services;

use App\Domains\Shipping\DTOs\RateQuoteData;
use App\Domains\Shipping\DTOs\RateRequest;
use App\Domains\Shipping\DTOs\UnavailableCarrier;
use App\Domains\Shipping\Integration\CarrierRegistry;
use App\Domains\Shipping\Models\RateQuote;
use App\Domains\Shipping\Models\ShippingSettings;
use App\Domains\Shipping\Models\StoreCarrierAccount;
use Illuminate\Support\Facades\Cache;
use Illuminate\Support\Facades\Log;
use Illuminate\Support\Str;
use Throwable;

/**
 * مقارنة الأسعار عبر كل الحسابات المتاحة.
 *
 * قراران يظهران للمستخدم مباشرة:
 *  • الشركة التي تفشل أو تتأخر لا توقف عرض بقية الأسعار.
 *  • الشركة غير المتاحة تُعرض **مع سببها** بدل إخفائها.
 */
final class RateComparisonService
{
    /** @var list<UnavailableCarrier> */
    private array $unavailable = [];

    public function __construct(
        private readonly CarrierRegistry $registry,
        private readonly CoverageResolver $coverage,
        private readonly ShippingAnalyticsService $analytics,
    ) {}

    /** @return list<RateQuoteData> */
    public function compare(int $storeId, RateRequest $request, bool $persist = true): array
    {
        $this->unavailable = [];

        $accounts = StoreCarrierAccount::query()
            ->forStore($storeId)
            ->usable()
            ->with('carrier')
            ->orderByDesc('is_default')
            ->orderBy('priority')
            ->get();

        $quotes = [];

        foreach ($accounts as $account) {
            $carrierQuotes = $this->quotesFor($account, $request);

            foreach ($carrierQuotes as $quote) {
                $quotes[] = $quote;
            }
        }

        $quotes = $this->score($storeId, $quotes);

        if ($persist && $quotes !== []) {
            $this->persist($storeId, $request, $quotes);
        }

        return $quotes;
    }

    /** @return list<UnavailableCarrier> */
    public function unavailable(): array
    {
        return $this->unavailable;
    }

    /** @return list<RateQuoteData> */
    private function quotesFor(StoreCarrierAccount $account, RateRequest $request): array
    {
        $carrier = $account->carrier;

        if (! $this->coverage->covers($account, $request->destination->governorate, $request->destination->wilayat)) {
            $this->unavailable[] = new UnavailableCarrier(
                $carrier->code,
                $carrier->name(),
                __('shipping.unavailable.not_covered', ['area' => $request->destination->governorate]),
            );

            return [];
        }

        $cacheKey = "shipping:rates:{$account->id}:{$request->fingerprint()}";

        try {
            /** @var list<RateQuoteData> $quotes */
            $quotes = Cache::remember(
                $cacheKey,
                now()->addMinutes(10),
                fn (): array => $this->registry->for($account)->getRates($request),
            );
        } catch (Throwable $e) {
            Log::warning('shipping.rate_failed', [
                'account_id' => $account->id,
                'carrier' => $carrier->code,
                'error' => $e->getMessage(),
            ]);

            $this->unavailable[] = new UnavailableCarrier(
                $carrier->code,
                $carrier->name(),
                __('shipping.unavailable.connection_failed'),
            );

            return [];
        }

        if ($quotes === []) {
            $this->unavailable[] = new UnavailableCarrier(
                $carrier->code,
                $carrier->name(),
                __('shipping.unavailable.no_rate'),
            );
        }

        return $quotes;
    }

    /**
     * التقييم المركّب: السعر والسرعة والموثوقية والالتزام بالموعد.
     * الأوزان في إعدادات المتجر — تاجر يريد الأرخص وآخر يريد الأسرع.
     *
     * @param  list<RateQuoteData>  $quotes
     * @return list<RateQuoteData>
     */
    private function score(int $storeId, array $quotes): array
    {
        if ($quotes === []) {
            return [];
        }

        $weights = ShippingSettings::query()->find($storeId)?->scoringWeights()
            ?? (array) config('shipping.scoring');

        $prices = array_map(static fn (RateQuoteData $q): float => $q->price, $quotes);
        $etas = array_map(static fn (RateQuoteData $q): int => $q->etaMaxDays, $quotes);

        $minPrice = min($prices);
        $maxPrice = max($prices);
        $minEta = min($etas);
        $maxEta = max($etas);

        $performance = $this->analytics->carrierPerformance($storeId);

        foreach ($quotes as $quote) {
            $priceScore = $maxPrice > $minPrice ? 1 - (($quote->price - $minPrice) / ($maxPrice - $minPrice)) : 1.0;
            $speedScore = $maxEta > $minEta ? 1 - (($quote->etaMaxDays - $minEta) / ($maxEta - $minEta)) : 1.0;

            $stats = $performance[$quote->carrierId] ?? null;
            $reliability = $stats['success_rate'] ?? 90.0;
            $punctuality = $stats['on_time_rate'] ?? 85.0;

            $quote->score = round(
                ($priceScore * ($weights['price'] ?? 0.3)
                    + $speedScore * ($weights['speed'] ?? 0.2)
                    + ($reliability / 100) * ($weights['reliability'] ?? 0.3)
                    + ($punctuality / 100) * ($weights['punctuality'] ?? 0.2)) * 100,
                2,
            );
        }

        usort($quotes, static fn (RateQuoteData $a, RateQuoteData $b): int => $b->score <=> $a->score);
        $quotes[0]->recommended = true;

        return $quotes;
    }

    /** @param list<RateQuoteData> $quotes */
    private function persist(int $storeId, RateRequest $request, array $quotes): void
    {
        $group = (string) Str::uuid();
        $expiresAt = now()->addMinutes(30);

        foreach ($quotes as $quote) {
            RateQuote::query()->create([
                'store_id' => $storeId,
                'quote_group_uuid' => $group,
                'carrier_id' => $quote->carrierId,
                'store_carrier_account_id' => $quote->accountId,
                'service_code' => $quote->serviceCode,
                'service_name' => $quote->serviceName,
                'price' => $quote->price,
                'currency' => $quote->currency,
                'eta_min_days' => $quote->etaMinDays,
                'eta_max_days' => $quote->etaMaxDays,
                'features' => $quote->features,
                'score' => $quote->score,
                'source' => $quote->source,
                'expires_at' => $expiresAt,
                'raw' => $quote->breakdown,
            ]);
        }
    }
}
