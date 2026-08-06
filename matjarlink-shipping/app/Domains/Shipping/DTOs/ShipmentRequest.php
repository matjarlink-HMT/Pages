<?php

declare(strict_types=1);

namespace App\Domains\Shipping\DTOs;

use App\Domains\Shipping\Support\WeightCalculator;

final readonly class ShipmentRequest
{
    /**
     * @param list<PackageData> $packages
     * @param list<ItemData>    $items
     */
    public function __construct(
        public int $accountId,
        public AddressData $sender,
        public AddressData $receiver,
        public array $packages,
        public array $items = [],
        public ?int $orderId = null,
        public ?string $serviceCode = null,
        public float $declaredValue = 0.0,
        public bool $isCod = false,
        public float $codAmount = 0.0,
        public string $currency = 'OMR',
        public ?string $notes = null,
        public ?string $internalNotes = null,
        public ?string $idempotencyKey = null,
    ) {}

    public function billableWeight(?int $divisor = null): float
    {
        return WeightCalculator::billable($this->packages, $divisor);
    }

    public function piecesCount(): int
    {
        return array_sum(array_map(static fn (PackageData $p): int => max(1, $p->quantity), $this->packages));
    }

    public function toRateRequest(): RateRequest
    {
        return new RateRequest(
            origin: $this->sender,
            destination: $this->receiver,
            packages: $this->packages,
            declaredValue: $this->declaredValue,
            isCod: $this->isCod,
            codAmount: $this->codAmount,
            serviceCode: $this->serviceCode,
            currency: $this->currency,
        );
    }

    /**
     * مفتاح الحماية من الازدواج: ضغطة زر مزدوجة أو انقطاع شبكة يجب
     * ألا ينتجا بوليصتين ورسمين على نفس الطلب.
     */
    public function idempotencyKey(): string
    {
        return $this->idempotencyKey ?? hash('sha256', json_encode([
            $this->orderId, $this->accountId, $this->serviceCode,
            $this->receiver->phone, $this->receiver->wilayat,
            $this->billableWeight(), $this->piecesCount(), $this->codAmount,
        ], JSON_THROW_ON_ERROR));
    }
}
