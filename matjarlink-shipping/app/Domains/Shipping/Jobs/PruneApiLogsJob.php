<?php

declare(strict_types=1);

namespace App\Domains\Shipping\Jobs;

use App\Domains\Shipping\Models\CarrierApiLog;
use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Bus\Dispatchable;
use Illuminate\Queue\SerializesModels;

/** سجلات النداءات تكبر بسرعة — والسجلات الفاشلة تُحفظ أطول للتشخيص. */
final class PruneApiLogsJob implements ShouldQueue
{
    use Dispatchable;
    use Queueable;
    use SerializesModels;

    public function handle(): void
    {
        CarrierApiLog::query()
            ->withoutGlobalScopes()
            ->where('success', true)
            ->where('created_at', '<', now()->subDays((int) config('shipping.logs.retention_days', 90)))
            ->delete();

        CarrierApiLog::query()
            ->withoutGlobalScopes()
            ->where('success', false)
            ->where('created_at', '<', now()->subDays((int) config('shipping.logs.failed_retention_days', 180)))
            ->delete();
    }
}
