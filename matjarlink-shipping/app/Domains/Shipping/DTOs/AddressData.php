<?php

declare(strict_types=1);

namespace App\Domains\Shipping\DTOs;

use App\Domains\Shipping\Support\PhoneNormalizer;

final readonly class AddressData
{
    public function __construct(
        public string $name,
        public string $phone,
        public string $governorate,
        public string $wilayat,
        public ?string $altPhone = null,
        public ?string $email = null,
        public string $countryCode = 'OM',
        public ?string $area = null,
        public ?string $street = null,
        public ?string $building = null,
        public ?string $landmark = null,
        public ?string $postalCode = null,
        public ?float $latitude = null,
        public ?float $longitude = null,
        public ?string $notes = null,
    ) {}

    public static function fromArray(array $data): self
    {
        return new self(
            name: (string) ($data['name'] ?? ''),
            phone: (string) (PhoneNormalizer::normalize($data['phone'] ?? null) ?? ''),
            governorate: (string) ($data['governorate'] ?? ''),
            wilayat: (string) ($data['wilayat'] ?? ''),
            altPhone: PhoneNormalizer::normalize($data['alt_phone'] ?? null),
            email: $data['email'] ?? null,
            countryCode: (string) ($data['country_code'] ?? 'OM'),
            area: $data['area'] ?? null,
            street: $data['street'] ?? null,
            building: $data['building'] ?? null,
            landmark: $data['landmark'] ?? null,
            postalCode: $data['postal_code'] ?? null,
            latitude: isset($data['latitude']) ? (float) $data['latitude'] : null,
            longitude: isset($data['longitude']) ? (float) $data['longitude'] : null,
            notes: $data['notes'] ?? null,
        );
    }

    public function toArray(): array
    {
        return [
            'name' => $this->name, 'phone' => $this->phone, 'alt_phone' => $this->altPhone,
            'email' => $this->email, 'country_code' => $this->countryCode,
            'governorate' => $this->governorate, 'wilayat' => $this->wilayat, 'area' => $this->area,
            'street' => $this->street, 'building' => $this->building, 'landmark' => $this->landmark,
            'postal_code' => $this->postalCode, 'latitude' => $this->latitude,
            'longitude' => $this->longitude, 'notes' => $this->notes,
        ];
    }

    public function oneLine(): string
    {
        return implode('، ', array_filter([
            $this->building, $this->street, $this->area, $this->wilayat, $this->governorate,
        ]));
    }
}
