<?php

declare(strict_types=1);

namespace App\Domains\Shipping\DTOs;

final class RateQuoteData
{
    public function __construct(
        public readonly int $carrierId,
        public readonly int $accountId,
        public readonly string $carrierCode,
        public readonly string $carrierName,
        public readonly string $serviceCode,
        public readonly string $serviceName,
        public readonly float $price,
        public readonly int $etaMinDays,
        public readonly int $etaMaxDays,
        public readonly string $currency = 'OMR',
        /** @var list<string> */
        public readonly array $features = [],
        public readonly string $source = 'api',
        public readonly array $breakdown = [],
        public float $score = 0.0,
        public bool $recommended = false,
    ) {}

    public function etaLabel(): string
    {
        if ($this->etaMinDays === 0 && $this->etaMaxDays <= 1) {
            return __('shipping.rates.same_day');
        }

        return $this->etaMinDays === $this->etaMaxDays
            ? trans_choice('shipping.rates.days', $this->etaMaxDays, ['count' => $this->etaMaxDays])
            : __('shipping.rates.days_range', ['min' => $this->etaMinDays, 'max' => $this->etaMaxDays]);
    }

    public function toArray(): array
    {
        return [
            'carrier_id' => $this->carrierId, 'account_id' => $this->accountId,
            'carrier_code' => $this->carrierCode, 'carrier_name' => $this->carrierName,
            'service_code' => $this->serviceCode, 'service_name' => $this->serviceName,
            'price' => $this->price, 'currency' => $this->currency,
            'eta_min_days' => $this->etaMinDays, 'eta_max_days' => $this->etaMaxDays,
            'eta_label' => $this->etaLabel(), 'features' => $this->features,
            'source' => $this->source, 'breakdown' => $this->breakdown,
            'score' => $this->score, 'recommended' => $this->recommended,
        ];
    }
}
