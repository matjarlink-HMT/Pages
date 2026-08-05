<?php

declare(strict_types=1);

namespace App\Domains\Shipping\Models;

use App\Domains\Shipping\Concerns\BelongsToStore;
use App\Domains\Shipping\Enums\PaymentType;
use App\Domains\Shipping\Enums\ShipmentStatus;
use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Concerns\HasUuids;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Relations\HasMany;
use Illuminate\Database\Eloquent\Relations\HasOne;
use Illuminate\Database\Eloquent\SoftDeletes;

/**
 * الشحنة — الجدول المحوري.
 *
 * ملاحظتان تصميميتان:
 *  • الحالة هنا انعكاس للسجل الزمني (shipment_events) لا حقل يُكتب مباشرة،
 *    ولا يغيّرها إلا ShipmentEventRecorder.
 *  • الشحنة مستند مالي: لا تُحذف فعلياً بل تُلغى أو تُؤرشف.
 */
final class Shipment extends Model
{
    use BelongsToStore;
    use SoftDeletes;

    protected $fillable = [
        'store_id', 'uuid', 'reference', 'store_sequence', 'order_id',
        'carrier_id', 'store_carrier_account_id', 'service_code', 'service_name',
        'status', 'status_updated_at', 'tracking_number', 'carrier_shipment_id',
        'idempotency_key', 'pieces_count', 'total_weight_kg', 'billable_weight_kg',
        'declared_value', 'currency', 'is_cod', 'cod_amount', 'cod_collected_at',
        'quoted_cost', 'actual_cost', 'extra_fees', 'total_cost', 'cost_breakdown',
        'payment_type', 'promised_delivery_at', 'picked_up_at', 'delivered_at',
        'returned_at', 'cancelled_at', 'delivery_attempts', 'is_delayed', 'is_stale',
        'last_synced_at', 'next_sync_at', 'sync_failures', 'notes', 'internal_notes',
        'carrier_error', 'created_by', 'cancelled_by',
    ];

    protected function casts(): array
    {
        return [
            'status' => ShipmentStatus::class,
            'payment_type' => PaymentType::class,
            'cost_breakdown' => 'array',
            'is_cod' => 'boolean',
            'is_delayed' => 'boolean',
            'is_stale' => 'boolean',
            'total_weight_kg' => 'decimal:3',
            'billable_weight_kg' => 'decimal:3',
            'declared_value' => 'decimal:3',
            'cod_amount' => 'decimal:3',
            'quoted_cost' => 'decimal:3',
            'actual_cost' => 'decimal:3',
            'extra_fees' => 'decimal:3',
            'total_cost' => 'decimal:3',
            'status_updated_at' => 'datetime',
            'promised_delivery_at' => 'datetime',
            'picked_up_at' => 'datetime',
            'delivered_at' => 'datetime',
            'returned_at' => 'datetime',
            'cancelled_at' => 'datetime',
            'cod_collected_at' => 'datetime',
            'last_synced_at' => 'datetime',
            'next_sync_at' => 'datetime',
        ];
    }

    public function getRouteKeyName(): string
    {
        return 'uuid';
    }

    /* ---------------- العلاقات ---------------- */

    public function carrier(): BelongsTo
    {
        return $this->belongsTo(ShippingCarrier::class, 'carrier_id');
    }

    public function account(): BelongsTo
    {
        return $this->belongsTo(StoreCarrierAccount::class, 'store_carrier_account_id');
    }

    public function addresses(): HasMany
    {
        return $this->hasMany(ShipmentAddress::class);
    }

    public function sender(): HasOne
    {
        return $this->hasOne(ShipmentAddress::class)->where('type', 'sender');
    }

    public function receiver(): HasOne
    {
        return $this->hasOne(ShipmentAddress::class)->where('type', 'receiver');
    }

    public function packages(): HasMany
    {
        return $this->hasMany(ShipmentPackage::class);
    }

    public function items(): HasMany
    {
        return $this->hasMany(ShipmentItem::class);
    }

    public function events(): HasMany
    {
        return $this->hasMany(ShipmentEvent::class)->orderByDesc('occurred_at');
    }

    public function labels(): HasMany
    {
        return $this->hasMany(ShipmentLabel::class);
    }

    /* ---------------- استعلامات ---------------- */

    public function scopeOpen(Builder $query): Builder
    {
        return $query->whereNotIn('status', array_map(
            static fn (ShipmentStatus $s): string => $s->value,
            array_filter(ShipmentStatus::cases(), static fn (ShipmentStatus $s): bool => $s->isTerminal()),
        ));
    }

    public function scopeNeedsAttention(Builder $query): Builder
    {
        return $query->where(function (Builder $q): void {
            $q->where('is_delayed', true)
                ->orWhere('is_stale', true)
                ->orWhereIn('status', array_map(
                    static fn (ShipmentStatus $s): string => $s->value,
                    array_filter(ShipmentStatus::cases(), static fn (ShipmentStatus $s): bool => $s->needsAttention()),
                ));
        });
    }

    public function scopeDueForSync(Builder $query): Builder
    {
        return $query->whereNotNull('next_sync_at')
            ->where('next_sync_at', '<=', now())
            ->whereIn('status', array_map(
                static fn (ShipmentStatus $s): string => $s->value,
                ShipmentStatus::syncable(),
            ));
    }

    /* ---------------- مشتقات ---------------- */

    public function costVariance(): float
    {
        return round((float) $this->actual_cost - (float) $this->quoted_cost, 3);
    }

    public function isOverbilled(): bool
    {
        return $this->costVariance() > 0.001;
    }

    public function deliveryDurationHours(): ?float
    {
        return $this->delivered_at?->floatDiffInHours($this->created_at);
    }

    public function wasOnTime(): ?bool
    {
        if ($this->delivered_at === null || $this->promised_delivery_at === null) {
            return null;
        }

        return $this->delivered_at->lessThanOrEqualTo($this->promised_delivery_at);
    }
}
