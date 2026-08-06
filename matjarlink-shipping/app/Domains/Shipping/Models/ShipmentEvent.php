<?php

declare(strict_types=1);

namespace App\Domains\Shipping\Models;

use App\Domains\Shipping\Enums\ShipmentEventSource;
use App\Domains\Shipping\Enums\ShipmentStatus;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

/**
 * السجل الزمني — مصدر الحقيقة للحالة.
 * occurred_at هو زمن الحدث لدى الشركة لا زمن استقبالنا له، لأن أحداث
 * الـ Webhook تصل خارج ترتيبها الزمني.
 */
final class ShipmentEvent extends Model
{
    public const UPDATED_AT = null;

    protected $fillable = [
        'shipment_id', 'status', 'carrier_status_code', 'carrier_status_text',
        'description_ar', 'description_en', 'location', 'occurred_at',
        'source', 'actor_id', 'hash', 'raw_payload',
    ];

    protected function casts(): array
    {
        return [
            'status' => ShipmentStatus::class,
            'source' => ShipmentEventSource::class,
            'occurred_at' => 'datetime',
            'raw_payload' => 'array',
        ];
    }

    public function shipment(): BelongsTo
    {
        return $this->belongsTo(Shipment::class);
    }

    public function description(): string
    {
        return app()->getLocale() === 'ar'
            ? ($this->description_ar ?: $this->status->label())
            : ($this->description_en ?: $this->status->label());
    }
}
