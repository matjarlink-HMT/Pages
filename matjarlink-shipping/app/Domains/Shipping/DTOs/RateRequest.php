<?php

declare(strict_types=1);

namespace App\Domains\Shipping\DTOs;

use App\Domains\Shipping\Support\OmanGeo;
use App\Domains\Shipping\Support\WeightCalculator;

final readonly class RateRequest
{
    /** @param list<PackageData> $packages */
    public function __construct(
        public AddressData $origin,
        public AddressData $destination,
        public array $packages,
        public float $declaredValue = 0.0,
        public bool $isCod = false,
        public float $codAmount = 0.0,
        public ?string $serviceCode = null,
        public string $currency = 'OMR',
    ) {}

    public function billableWeight(?int $divisor = null): float
    {
        return WeightCalculator::billable($this->packages, $divisor);
    }

    public function piecesCount(): int
    {
        return array_sum(array_map(static fn (PackageData $p): int => max(1, $p->quantity), $this->packages));
    }

    public function isRemoteDestination(): bool
    {
        return OmanGeo::isRemote($this->destination->governorate);
    }

    /** بصمة تُستخدم لكاش العروض: نفس الشحنة لا تُسعَّر مرتين خلال دقائق. */
    public function fingerprint(): string
    {
        return md5(json_encode([
            $this->origin->governorate, $this->origin->wilayat,
            $this->destination->governorate, $this->destination->wilayat,
            $this->billableWeight(), $this->piecesCount(),
            $this->isCod, $this->codAmount, $this->serviceCode,
        ], JSON_THROW_ON_ERROR));
    }
}
