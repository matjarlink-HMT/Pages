<?php

declare(strict_types=1);

namespace App\Domains\Shipping\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

final class ShippingZoneRegion extends Model
{
    protected $fillable = ['zone_id', 'country_code', 'governorate', 'wilayat', 'area', 'is_remote'];

    protected function casts(): array
    {
        return ['is_remote' => 'boolean'];
    }

    public function zone(): BelongsTo
    {
        return $this->belongsTo(ShippingZone::class, 'zone_id');
    }

    /** wilayat فارغة تعني «كل ولايات المحافظة». */
    public function matches(string $governorate, ?string $wilayat = null): bool
    {
        if ($this->governorate !== $governorate) {
            return false;
        }

        return $this->wilayat === null || $this->wilayat === $wilayat;
    }
}
