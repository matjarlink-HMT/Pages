<?php

declare(strict_types=1);

namespace App\Domains\Shipping\Models;

use App\Domains\Shipping\Concerns\BelongsToStore;
use Illuminate\Database\Eloquent\Model;

/** سجل نداءات الشركات — منقّح من الأسرار، وتُقلَّم سجلاته دورياً. */
final class CarrierApiLog extends Model
{
    use BelongsToStore;

    public const UPDATED_AT = null;

    protected $fillable = [
        'store_id', 'store_carrier_account_id', 'operation', 'correlation_id',
        'request_payload', 'response_payload', 'http_status', 'duration_ms',
        'success', 'error_message', 'shipment_id',
    ];

    protected function casts(): array
    {
        return [
            'request_payload' => 'array',
            'response_payload' => 'array',
            'success' => 'boolean',
            'http_status' => 'integer',
            'duration_ms' => 'integer',
        ];
    }
}
