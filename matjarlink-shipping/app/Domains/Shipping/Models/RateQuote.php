<?php

declare(strict_types=1);

namespace App\Domains\Shipping\Models;

use App\Domains\Shipping\Concerns\BelongsToStore;
use Illuminate\Database\Eloquent\Model;

/**
 * العروض المحفوظة: تثبت لماذا اختير هذا السعر وقتها (تدقيق)،
 * وتغذّي تقرير «كم وفّرنا باختيار الأنسب».
 */
final class RateQuote extends Model
{
    use BelongsToStore;

    public const UPDATED_AT = null;

    protected $fillable = [
        'store_id', 'quote_group_uuid', 'order_id', 'shipment_id', 'carrier_id',
        'store_carrier_account_id', 'service_code', 'service_name', 'price', 'currency',
        'eta_min_days', 'eta_max_days', 'features', 'score', 'is_selected',
        'source', 'expires_at', 'raw',
    ];

    protected function casts(): array
    {
        return [
            'features' => 'array',
            'raw' => 'array',
            'price' => 'decimal:3',
            'score' => 'decimal:2',
            'is_selected' => 'boolean',
            'expires_at' => 'datetime',
        ];
    }
}
