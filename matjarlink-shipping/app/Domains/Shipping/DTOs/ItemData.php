<?php

declare(strict_types=1);

namespace App\Domains\Shipping\DTOs;

final readonly class ItemData
{
    public function __construct(
        public string $name,
        public int $quantity = 1,
        public ?string $sku = null,
        public ?int $orderItemId = null,
        public float $unitValue = 0.0,
        public ?float $weightKg = null,
        public ?string $hsCode = null,
        public ?string $countryOfOrigin = null,
    ) {}

    public static function fromArray(array $data): self
    {
        return new self(
            name: (string) ($data['name'] ?? ''),
            quantity: (int) ($data['quantity'] ?? 1),
            sku: $data['sku'] ?? null,
            orderItemId: isset($data['order_item_id']) ? (int) $data['order_item_id'] : null,
            unitValue: (float) ($data['unit_value'] ?? 0),
            weightKg: isset($data['weight_kg']) ? (float) $data['weight_kg'] : null,
            hsCode: $data['hs_code'] ?? null,
            countryOfOrigin: $data['country_of_origin'] ?? null,
        );
    }

    public function total(): float
    {
        return round($this->unitValue * $this->quantity, 3);
    }

    public function toArray(): array
    {
        return [
            'name' => $this->name, 'quantity' => $this->quantity, 'sku' => $this->sku,
            'order_item_id' => $this->orderItemId, 'unit_value' => $this->unitValue,
            'weight_kg' => $this->weightKg, 'hs_code' => $this->hsCode,
            'country_of_origin' => $this->countryOfOrigin,
        ];
    }
}
