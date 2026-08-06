<?php

declare(strict_types=1);

namespace App\Domains\Shipping\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

/**
 * لقطة العنوان وقت الإنشاء — لا مرجع لجدول عناوين.
 * تعديل العميل لعنوانه بعد شهر يجب ألا يغيّر ما طُبع على بوليصة سابقة:
 * سلامة السجل التاريخي فوق التطبيع.
 */
final class ShipmentAddress extends Model
{
    protected $fillable = [
        'shipment_id', 'type', 'name', 'phone', 'alt_phone', 'email', 'country_code',
        'governorate', 'wilayat', 'area', 'street', 'building', 'landmark',
        'postal_code', 'latitude', 'longitude', 'notes',
    ];

    protected function casts(): array
    {
        return ['latitude' => 'float', 'longitude' => 'float'];
    }

    public function shipment(): BelongsTo
    {
        return $this->belongsTo(Shipment::class);
    }

    public function oneLine(): string
    {
        return implode('، ', array_filter([
            $this->building, $this->street, $this->area, $this->wilayat, $this->governorate,
        ]));
    }
}
