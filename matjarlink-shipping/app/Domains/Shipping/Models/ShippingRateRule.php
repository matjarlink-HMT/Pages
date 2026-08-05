<?php

declare(strict_types=1);

namespace App\Domains\Shipping\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

final class ShippingRateRule extends Model
{
    protected $fillable = [
        'rate_card_id', 'zone_id', 'service_code', 'service_name',
        'min_weight_kg', 'max_weight_kg', 'base_price', 'price_per_extra_kg',
        'cod_fee_fixed', 'cod_fee_percent', 'remote_area_surcharge',
        'insurance_percent', 'fuel_surcharge_percent', 'vat_percent',
        'eta_min_days', 'eta_max_days', 'priority',
    ];

    protected function casts(): array
    {
        return [
            'min_weight_kg' => 'decimal:3',
            'max_weight_kg' => 'decimal:3',
            'base_price' => 'decimal:3',
            'price_per_extra_kg' => 'decimal:3',
            'cod_fee_fixed' => 'decimal:3',
            'cod_fee_percent' => 'decimal:2',
            'remote_area_surcharge' => 'decimal:3',
            'insurance_percent' => 'decimal:2',
            'fuel_surcharge_percent' => 'decimal:2',
            'vat_percent' => 'decimal:2',
            'eta_min_days' => 'integer',
            'eta_max_days' => 'integer',
            'priority' => 'integer',
        ];
    }

    public function card(): BelongsTo
    {
        return $this->belongsTo(ShippingRateCard::class, 'rate_card_id');
    }

    public function zone(): BelongsTo
    {
        return $this->belongsTo(ShippingZone::class, 'zone_id');
    }

    public function coversWeight(float $weightKg): bool
    {
        return $weightKg >= (float) $this->min_weight_kg
            && ($this->max_weight_kg === null || $weightKg <= (float) $this->max_weight_kg);
    }
}
