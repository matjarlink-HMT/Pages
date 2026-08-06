<?php

declare(strict_types=1);

namespace App\Domains\Shipping\Http\Requests;

use App\Domains\Shipping\DTOs\AddressData;
use App\Domains\Shipping\DTOs\ItemData;
use App\Domains\Shipping\DTOs\PackageData;
use App\Domains\Shipping\DTOs\ShipmentRequest;
use App\Domains\Shipping\Models\Shipment;
use App\Domains\Shipping\Support\OmanGeo;
use Illuminate\Foundation\Http\FormRequest;
use Illuminate\Validation\Validator;

final class CreateShipmentRequest extends FormRequest
{
    public function authorize(): bool
    {
        return $this->user()?->can('create', Shipment::class) ?? false;
    }

    public function rules(): array
    {
        $maxKg = (float) config('shipping.weight.max_kg', 30);

        return [
            'store_carrier_account_id' => ['required', 'integer'],
            'service_code' => ['nullable', 'string', 'max:50'],
            'order_id' => ['nullable', 'integer'],

            'sender' => ['required', 'array'],
            'sender.name' => ['required', 'string', 'max:150'],
            'sender.phone' => ['required', 'string', 'max:30'],
            'sender.governorate' => ['required', 'string', 'max:100'],
            'sender.wilayat' => ['required', 'string', 'max:100'],

            'receiver' => ['required', 'array'],
            'receiver.name' => ['required', 'string', 'max:150'],
            'receiver.phone' => ['required', 'string', 'max:30'],
            'receiver.governorate' => ['required', 'string', 'max:100'],
            'receiver.wilayat' => ['required', 'string', 'max:100'],
            'receiver.street' => ['nullable', 'string', 'max:255'],
            'receiver.landmark' => ['nullable', 'string', 'max:255'],
            'receiver.latitude' => ['nullable', 'numeric', 'between:-90,90'],
            'receiver.longitude' => ['nullable', 'numeric', 'between:-180,180'],

            'packages' => ['required', 'array', 'min:1', 'max:50'],
            'packages.*.weight_kg' => ['required', 'numeric', 'gt:0', "max:{$maxKg}"],
            'packages.*.length_cm' => ['nullable', 'numeric', 'gt:0', 'max:300'],
            'packages.*.width_cm' => ['nullable', 'numeric', 'gt:0', 'max:300'],
            'packages.*.height_cm' => ['nullable', 'numeric', 'gt:0', 'max:300'],
            'packages.*.quantity' => ['nullable', 'integer', 'min:1', 'max:99'],

            'items' => ['nullable', 'array'],
            'items.*.name' => ['required_with:items', 'string', 'max:255'],
            'items.*.quantity' => ['nullable', 'integer', 'min:1'],
            'items.*.unit_value' => ['nullable', 'numeric', 'min:0'],

            'declared_value' => ['nullable', 'numeric', 'min:0'],
            'is_cod' => ['boolean'],
            'cod_amount' => ['nullable', 'numeric', 'min:0', 'required_if:is_cod,true'],
            'notes' => ['nullable', 'string', 'max:500'],
        ];
    }

    public function withValidator(Validator $validator): void
    {
        $validator->after(function (Validator $validator): void {
            foreach (['sender', 'receiver'] as $side) {
                $gov = $this->input("{$side}.governorate");
                $wilayat = $this->input("{$side}.wilayat");

                if ($gov && $wilayat && ! OmanGeo::exists($gov, $wilayat)) {
                    $validator->errors()->add("{$side}.wilayat", __('shipping.validation.unknown_wilayat'));
                }
            }
        });
    }

    public function toDto(): ShipmentRequest
    {
        return new ShipmentRequest(
            accountId: (int) $this->integer('store_carrier_account_id'),
            sender: AddressData::fromArray((array) $this->input('sender')),
            receiver: AddressData::fromArray((array) $this->input('receiver')),
            packages: array_map(
                static fn (array $p): PackageData => PackageData::fromArray($p),
                (array) $this->input('packages', []),
            ),
            items: array_map(
                static fn (array $i): ItemData => ItemData::fromArray($i),
                (array) $this->input('items', []),
            ),
            orderId: $this->filled('order_id') ? (int) $this->integer('order_id') : null,
            serviceCode: $this->input('service_code'),
            declaredValue: (float) $this->input('declared_value', 0),
            isCod: $this->boolean('is_cod'),
            codAmount: (float) $this->input('cod_amount', 0),
            currency: (string) config('shipping.currency', 'OMR'),
            notes: $this->input('notes'),
            /* ترويسة Idempotency-Key من العميل تمنع الازدواج عند إعادة الإرسال. */
            idempotencyKey: $this->header('Idempotency-Key'),
        );
    }
}
