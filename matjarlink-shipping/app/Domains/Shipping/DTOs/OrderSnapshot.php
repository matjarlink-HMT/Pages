<?php

declare(strict_types=1);

namespace App\Domains\Shipping\DTOs;

/** لقطة الطلب لتعبئة الشحنة مسبقاً — تُنتجها المنصة عبر OrderBridge. */
final readonly class OrderSnapshot
{
    /**
     * @param list<ItemData>    $items
     * @param list<PackageData> $suggestedPackages
     */
    public function __construct(
        public int $orderId,
        public string $orderNumber,
        public AddressData $receiver,
        public array $items = [],
        public array $suggestedPackages = [],
        public float $total = 0.0,
        public bool $isCod = false,
        public float $codAmount = 0.0,
        public string $currency = 'OMR',
        public ?string $notes = null,
    ) {}
}
