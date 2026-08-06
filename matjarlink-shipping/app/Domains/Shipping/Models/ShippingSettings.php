<?php

declare(strict_types=1);

namespace App\Domains\Shipping\Models;

use Illuminate\Database\Eloquent\Model;

/** صف واحد لكل متجر — إعدادات الوحدة. */
final class ShippingSettings extends Model
{
    protected $table = 'shipping_settings';

    protected $primaryKey = 'store_id';

    public $incrementing = false;

    protected $fillable = [
        'store_id', 'default_carrier_account_id', 'auto_create_shipment_on',
        'auto_select_carrier', 'default_service_code', 'label_format',
        'sla_default_days', 'stale_threshold_hours', 'sender_defaults',
        'notification_settings', 'cod_settings', 'public_tracking_enabled',
        'scoring_weights', 'timezone',
    ];

    protected function casts(): array
    {
        return [
            'sender_defaults' => 'array',
            'notification_settings' => 'array',
            'cod_settings' => 'array',
            'scoring_weights' => 'array',
            'auto_select_carrier' => 'boolean',
            'public_tracking_enabled' => 'boolean',
            'sla_default_days' => 'integer',
            'stale_threshold_hours' => 'integer',
        ];
    }

    public static function forStore(int $storeId): self
    {
        return self::query()->firstOrCreate(['store_id' => $storeId]);
    }

    /** أوزان التوصية: تاجر يريد الأرخص وآخر يريد الأسرع. */
    public function scoringWeights(): array
    {
        return array_merge((array) config('shipping.scoring'), (array) $this->scoring_weights);
    }
}
