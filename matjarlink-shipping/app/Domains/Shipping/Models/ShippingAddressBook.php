<?php

declare(strict_types=1);

namespace App\Domains\Shipping\Models;

use App\Domains\Shipping\Concerns\BelongsToStore;
use App\Domains\Shipping\DTOs\AddressData;
use Illuminate\Database\Eloquent\Model;

final class ShippingAddressBook extends Model
{
    use BelongsToStore;

    protected $table = 'shipping_address_book';

    protected $fillable = [
        'store_id', 'type', 'label', 'customer_id', 'name', 'phone', 'email',
        'country_code', 'governorate', 'wilayat', 'area', 'street', 'building',
        'landmark', 'latitude', 'longitude', 'is_default', 'usage_count', 'last_used_at',
    ];

    protected function casts(): array
    {
        return [
            'is_default' => 'boolean',
            'usage_count' => 'integer',
            'last_used_at' => 'datetime',
            'latitude' => 'float',
            'longitude' => 'float',
        ];
    }

    public function toAddressData(): AddressData
    {
        return AddressData::fromArray($this->only([
            'name', 'phone', 'email', 'country_code', 'governorate', 'wilayat',
            'area', 'street', 'building', 'landmark', 'latitude', 'longitude',
        ]));
    }

    public function markUsed(): void
    {
        $this->forceFill([
            'usage_count' => $this->usage_count + 1,
            'last_used_at' => now(),
        ])->save();
    }
}
