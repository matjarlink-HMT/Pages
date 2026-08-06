<?php

declare(strict_types=1);

namespace App\Domains\Shipping\Models;

use App\Domains\Shipping\Concerns\BelongsToStore;
use App\Domains\Shipping\Enums\ConnectionStatus;
use App\Domains\Shipping\Support\CredentialMasker;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Relations\HasMany;
use Illuminate\Database\Eloquent\SoftDeletes;

/**
 * ربط التاجر بشركة شحن. يسمح بأكثر من حساب لنفس الشركة
 * (عقد مسقط / عقد صلالة) عبر الحقل label.
 */
final class StoreCarrierAccount extends Model
{
    use BelongsToStore;
    use SoftDeletes;

    protected $fillable = [
        'store_id', 'carrier_id', 'label', 'credentials', 'environment',
        'is_active', 'is_default', 'priority', 'connection_status',
        'last_checked_at', 'last_error', 'service_codes', 'default_service_code',
        'cod_enabled', 'cod_fee_percent', 'cod_fee_fixed', 'markup_type', 'markup_value',
        'pickup_address_id', 'circuit_opened_until', 'created_by',
    ];

    /** لا تخرج المفاتيح إلى JSON ولا إلى أي عرض. */
    protected $hidden = ['credentials'];

    protected function casts(): array
    {
        return [
            'credentials' => 'encrypted:array',
            'service_codes' => 'array',
            'is_active' => 'boolean',
            'is_default' => 'boolean',
            'cod_enabled' => 'boolean',
            'cod_fee_percent' => 'decimal:2',
            'cod_fee_fixed' => 'decimal:3',
            'markup_value' => 'decimal:3',
            'connection_status' => ConnectionStatus::class,
            'last_checked_at' => 'datetime',
            'circuit_opened_until' => 'datetime',
        ];
    }

    public function carrier(): BelongsTo
    {
        return $this->belongsTo(ShippingCarrier::class, 'carrier_id');
    }

    public function shipments(): HasMany
    {
        return $this->hasMany(Shipment::class, 'store_carrier_account_id');
    }

    public function rateCards(): HasMany
    {
        return $this->hasMany(ShippingRateCard::class, 'store_carrier_account_id');
    }

    public function displayName(): string
    {
        return $this->label
            ? "{$this->carrier->name()} — {$this->label}"
            : $this->carrier->name();
    }

    /** @return array<string, string> المفاتيح مقنّعة للعرض — لا تُرجع القيم أبداً. */
    public function maskedCredentials(): array
    {
        return array_map(
            static fn ($v): string => CredentialMasker::mask(is_string($v) ? $v : null),
            (array) $this->credentials,
        );
    }

    public function isUsable(): bool
    {
        return $this->is_active
            && $this->connection_status !== ConnectionStatus::Failed
            && ($this->circuit_opened_until === null || $this->circuit_opened_until->isPast());
    }

    public function scopeUsable($query)
    {
        return $query->where('is_active', true)
            ->where('connection_status', '!=', ConnectionStatus::Failed->value)
            ->where(function ($q): void {
                $q->whereNull('circuit_opened_until')->orWhere('circuit_opened_until', '<=', now());
            });
    }
}
