<?php

declare(strict_types=1);

namespace App\Domains\Shipping\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

/** يدعم الشحن الجزئي: طلب واحد ← شحنتان بأصناف مختلفة. */
final class ShipmentItem extends Model
{
    protected $fillable = [
        'shipment_id', 'order_item_id', 'sku', 'name', 'quantity',
        'unit_value', 'weight_kg', 'hs_code', 'country_of_origin',
    ];

    protected function casts(): array
    {
        return [
            'quantity' => 'integer',
            'unit_value' => 'decimal:3',
            'weight_kg' => 'decimal:3',
        ];
    }

    public function shipment(): BelongsTo
    {
        return $this->belongsTo(Shipment::class);
    }

    public function total(): float
    {
        return round((float) $this->unit_value * $this->quantity, 3);
    }
}
