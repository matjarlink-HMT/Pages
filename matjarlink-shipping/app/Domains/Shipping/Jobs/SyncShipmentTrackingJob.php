<?php

declare(strict_types=1);

namespace App\Domains\Shipping\Jobs;

use App\Domains\Shipping\Integration\CarrierRegistry;
use App\Domains\Shipping\Models\Shipment;
use App\Domains\Shipping\Services\ShipmentEventRecorder;
use App\Domains\Shipping\Services\SlaEngine;
use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Bus\Dispatchable;
use Illuminate\Queue\InteractsWithQueue;
use Illuminate\Queue\SerializesModels;
use Illuminate\Support\Facades\Log;
use Throwable;

/**
 * المزامنة الاحتياطية للشركات التي لا تدفع Webhooks — أو كتسوية يومية
 * للتي تدفعها، للتأكد من عدم فقدان أي حدث.
 */
final class SyncShipmentTrackingJob implements ShouldQueue
{
    use Dispatchable;
    use InteractsWithQueue;
    use Queueable;
    use SerializesModels;

    public int $tries = 3;

    public array $backoff = [30, 120, 600];

    public function __construct(public readonly int $shipmentId)
    {
        $this->onQueue((string) config('shipping.queues.sync', 'shipping-sync'));
    }

    public function handle(
        CarrierRegistry $registry,
        ShipmentEventRecorder $recorder,
        SlaEngine $sla,
    ): void {
        $shipment = Shipment::query()->withoutGlobalScopes()->with('account.carrier')->find($this->shipmentId);

        if ($shipment === null || $shipment->status->isTerminal() || $shipment->tracking_number === null) {
            return;
        }

        if (! $shipment->carrier->capabilities()->tracking) {
            $shipment->forceFill(['next_sync_at' => null])->save();

            return;
        }

        try {
            $events = $registry->for($shipment->account)->track($shipment->tracking_number);
            $recorder->recordMany($shipment, $events);

            $shipment->forceFill([
                'last_synced_at' => now(),
                'sync_failures' => 0,
                'next_sync_at' => $sla->nextSyncAt($shipment->refresh()),
                'is_stale' => $sla->isStale($shipment),
                'is_delayed' => $sla->isDelayed($shipment),
            ])->save();
        } catch (Throwable $e) {
            $shipment->forceFill([
                'sync_failures' => $shipment->sync_failures + 1,
                'next_sync_at' => now()->addMinutes(30 * max(1, $shipment->sync_failures)),
            ])->save();

            Log::warning('shipping.sync_failed', [
                'shipment_id' => $shipment->id,
                'error' => $e->getMessage(),
            ]);

            throw $e;
        }
    }
}
