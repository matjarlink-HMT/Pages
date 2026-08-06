<?php

declare(strict_types=1);

namespace App\Domains\Shipping\Models;

use App\Domains\Shipping\Enums\LabelFormat;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Support\Facades\Storage;

/** الاحتفاظ بالنسخ يمنع سؤال «أي بوليصة الصحيحة؟» بعد إعادة الإصدار. */
final class ShipmentLabel extends Model
{
    protected $fillable = [
        'shipment_id', 'format', 'disk', 'path', 'version',
        'printed_at', 'printed_by', 'print_count',
    ];

    protected function casts(): array
    {
        return [
            'format' => LabelFormat::class,
            'printed_at' => 'datetime',
            'version' => 'integer',
            'print_count' => 'integer',
        ];
    }

    public function shipment(): BelongsTo
    {
        return $this->belongsTo(Shipment::class);
    }

    /** رابط موقّع قصير الأجل — البوالص تحمل بيانات عملاء ولا تُنشر. */
    public function temporaryUrl(): string
    {
        return Storage::disk($this->disk)->temporaryUrl(
            $this->path,
            now()->addMinutes((int) config('shipping.storage.signed_url_minutes', 15)),
        );
    }
}
