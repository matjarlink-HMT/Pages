<?php

declare(strict_types=1);

namespace App\Domains\Shipping\Http\Requests;

use App\Domains\Shipping\DTOs\AddressData;
use App\Domains\Shipping\DTOs\PackageData;
use App\Domains\Shipping\DTOs\RateRequest;
use Illuminate\Foundation\Http\FormRequest;

final class RateQuoteRequest extends FormRequest
{
    public function authorize(): bool
    {
        return $this->user()?->can('viewAny', \App\Domains\Shipping\Models\Shipment::class) ?? false;
    }

    public function rules(): array
    {
        return [
            'origin' => ['nullable', 'array'],
            'destination' => ['required', 'array'],
            'destination.governorate' => ['required', 'string', 'max:100'],
            'destination.wilayat' => ['required', 'string', 'max:100'],
            'packages' => ['required', 'array', 'min:1'],
            'packages.*.weight_kg' => ['required', 'numeric', 'gt:0'],
            'packages.*.length_cm' => ['nullable', 'numeric', 'gt:0'],
            'packages.*.width_cm' => ['nullable', 'numeric', 'gt:0'],
            'packages.*.height_cm' => ['nullable', 'numeric', 'gt:0'],
            'declared_value' => ['nullable', 'numeric', 'min:0'],
            'is_cod' => ['boolean'],
            'cod_amount' => ['nullable', 'numeric', 'min:0'],
            'service_code' => ['nullable', 'string', 'max:50'],
        ];
    }

    public function toDto(array $originDefaults = []): RateRequest
    {
        return new RateRequest(
            origin: AddressData::fromArray((array) ($this->input('origin') ?: $originDefaults)),
            destination: AddressData::fromArray((array) $this->input('destination')),
            packages: array_map(
                static fn (array $p): PackageData => PackageData::fromArray($p),
                (array) $this->input('packages', []),
            ),
            declaredValue: (float) $this->input('declared_value', 0),
            isCod: $this->boolean('is_cod'),
            codAmount: (float) $this->input('cod_amount', 0),
            serviceCode: $this->input('service_code'),
            currency: (string) config('shipping.currency', 'OMR'),
        );
    }
}
