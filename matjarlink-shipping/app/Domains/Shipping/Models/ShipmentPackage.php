<?php

declare(strict_types=1);

namespace App\Domains\Shipping\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

final class ShipmentPackage extends Model
{
    protected $fillable = [
        'shipment_id', 'piece_no', 'weight_kg', 'length_cm', 'width_cm', 'height_cm',
        'volumetric_weight_kg', 'barcode', 'carrier_piece_id', 'description',
    ];

    protected function casts(): array
    {
        return [
            'weight_kg' => 'decimal:3',
            'length_cm' => 'decimal:2',
            'width_cm' => 'decimal:2',
            'height_cm' => 'decimal:2',
            'volumetric_weight_kg' => 'decimal:3',
        ];
    }

    public function shipment(): BelongsTo
    {
        return $this->belongsTo(Shipment::class);
    }
}
