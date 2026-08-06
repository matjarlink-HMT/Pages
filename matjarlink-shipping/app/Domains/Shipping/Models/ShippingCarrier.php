<?php

declare(strict_types=1);

namespace App\Domains\Shipping\Models;

use App\Domains\Shipping\DTOs\CarrierCapabilities;
use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

/**
 * كتالوج شركات الشحن — عام لكل المتاجر.
 * إضافة شركة = صف هنا + صنف Driver. لا هجرة ولا نشر جديد للنواة.
 *
 * @property string $code
 */
final class ShippingCarrier extends Model
{
    use HasFactory;

    protected $fillable = [
        'code', 'name_ar', 'name_en', 'logo_path', 'capabilities',
        'coverage_scope', 'website_url', 'support_phone', 'is_active', 'sort_order',
    ];

    protected function casts(): array
    {
        return [
            'capabilities' => 'array',
            'is_active' => 'boolean',
            'sort_order' => 'integer',
        ];
    }

    public function accounts(): HasMany
    {
        return $this->hasMany(StoreCarrierAccount::class, 'carrier_id');
    }

    public function statusMaps(): HasMany
    {
        return $this->hasMany(CarrierStatusMap::class, 'carrier_id');
    }

    public function capabilities(): CarrierCapabilities
    {
        return CarrierCapabilities::fromArray($this->capabilities ?? []);
    }

    public function name(): string
    {
        return app()->getLocale() === 'ar' ? $this->name_ar : ($this->name_en ?: $this->name_ar);
    }

    public function scopeActive($query)
    {
        return $query->where('is_active', true);
    }
}
