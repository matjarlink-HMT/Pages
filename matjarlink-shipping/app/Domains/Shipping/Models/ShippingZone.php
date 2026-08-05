<?php

declare(strict_types=1);

namespace App\Domains\Shipping\Models;

use App\Domains\Shipping\Concerns\BelongsToStore;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

final class ShippingZone extends Model
{
    use BelongsToStore;

    protected $fillable = ['store_id', 'name', 'description', 'is_active'];

    protected function casts(): array
    {
        return ['is_active' => 'boolean'];
    }

    public function regions(): HasMany
    {
        return $this->hasMany(ShippingZoneRegion::class, 'zone_id');
    }

    public function rules(): HasMany
    {
        return $this->hasMany(ShippingRateRule::class, 'zone_id');
    }

    public function covers(string $governorate, ?string $wilayat = null): bool
    {
        return $this->regions->contains(
            static fn (ShippingZoneRegion $r): bool => $r->matches($governorate, $wilayat),
        );
    }
}
