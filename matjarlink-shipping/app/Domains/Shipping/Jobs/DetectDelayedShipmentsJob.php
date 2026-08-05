<?php

declare(strict_types=1);

namespace App\Domains\Shipping\Jobs;

use App\Domains\Shipping\Models\Shipment;
use App\Domains\Shipping\Services\SlaEngine;
use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Bus\Dispatchable;
use Illuminate\Queue\SerializesModels;

/**
 * يضبط علامتي «متأخرة» و«صامتة» دورياً.
 * العلامتان مخزّنتان لا محسوبتين في كل استعلام — لوحة التحكم تقرأ فهرساً
 * لا تمسح الجدول.
 */
final class DetectDelayedShipmentsJob implements ShouldQueue
{
    use Dispatchable;
    use Queueable;
    use SerializesModels;

    public function __construct()
    {
        $this->onQueue((string) config('shipping.queues.sync', 'shipping-sync'));
    }

    public function handle(SlaEngine $sla): void
    {
        Shipment::query()
            ->withoutGlobalScopes()
            ->open()
            ->chunkById(500, static function ($shipments) use ($sla): void {
                foreach ($shipments as $shipment) {
                    $delayed = $sla->isDelayed($shipment);
                    $stale = $sla->isStale($shipment);

                    if ($delayed !== (bool) $shipment->is_delayed || $stale !== (bool) $shipment->is_stale) {
                        $shipment->forceFill(['is_delayed' => $delayed, 'is_stale' => $stale])->save();
                    }
                }
            });
    }
}
