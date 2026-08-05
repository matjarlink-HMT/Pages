<?php

declare(strict_types=1);

namespace App\Domains\Shipping\Models;

use App\Domains\Shipping\Enums\ShipmentStatus;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

/**
 * خريطة حالات الشركة → الحالة الداخلية، في القاعدة لا في الكود:
 * حين تضيف شركة رمز حالة جديداً يوم الجمعة يحلّها فريق العمليات بصف واحد
 * بدل انتظار نشر جديد.
 */
final class CarrierStatusMap extends Model
{
    protected $fillable = [
        'carrier_id', 'carrier_status_code', 'carrier_status_text',
        'internal_status', 'is_terminal', 'notes',
    ];

    protected function casts(): array
    {
        return ['internal_status' => ShipmentStatus::class, 'is_terminal' => 'boolean'];
    }

    public function carrier(): BelongsTo
    {
        return $this->belongsTo(ShippingCarrier::class, 'carrier_id');
    }
}
