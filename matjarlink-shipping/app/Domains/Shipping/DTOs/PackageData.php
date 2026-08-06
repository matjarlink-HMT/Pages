<?php

declare(strict_types=1);

namespace App\Domains\Shipping\DTOs;

final readonly class PackageData
{
    public function __construct(
        public float $weightKg,
        public ?float $lengthCm = null,
        public ?float $widthCm = null,
        public ?float $heightCm = null,
        public int $quantity = 1,
        public ?string $description = null,
    ) {}

    public static function fromArray(array $data): self
    {
        return new self(
            weightKg: (float) ($data['weight_kg'] ?? 0),
            lengthCm: isset($data['length_cm']) ? (float) $data['length_cm'] : null,
            widthCm: isset($data['width_cm']) ? (float) $data['width_cm'] : null,
            heightCm: isset($data['height_cm']) ? (float) $data['height_cm'] : null,
            quantity: (int) ($data['quantity'] ?? 1),
            description: $data['description'] ?? null,
        );
    }

    public function volumetricWeight(int $divisor): float
    {
        if (! $this->lengthCm || ! $this->widthCm || ! $this->heightCm || $divisor <= 0) {
            return 0.0;
        }

        return round($this->lengthCm * $this->widthCm * $this->heightCm / $divisor, 3);
    }

    public function toArray(): array
    {
        return [
            'weight_kg' => $this->weightKg, 'length_cm' => $this->lengthCm,
            'width_cm' => $this->widthCm, 'height_cm' => $this->heightCm,
            'quantity' => $this->quantity, 'description' => $this->description,
        ];
    }
}
