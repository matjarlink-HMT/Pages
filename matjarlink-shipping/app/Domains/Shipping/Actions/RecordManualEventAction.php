<?php

declare(strict_types=1);

namespace App\Domains\Shipping\Actions;

use App\Domains\Shipping\DTOs\TrackingEventData;
use App\Domains\Shipping\Enums\ShipmentEventSource;
use App\Domains\Shipping\Enums\ShipmentStatus;
use App\Domains\Shipping\Models\Shipment;
use App\Domains\Shipping\Services\ShipmentEventRecorder;
use Carbon\CarbonImmutable;

/**
 * تحديث يدوي: للشركات بلا API، ولخدمة العملاء بعد الاتصال بالشركة.
 * وجود هذا المسار يعني أن أي عطل خارجي لا يوقف عمل التاجر.
 */
final readonly class RecordManualEventAction
{
    public function __construct(private ShipmentEventRecorder $recorder) {}

    public function execute(
        Shipment $shipment,
        ShipmentStatus $status,
        string $description,
        ?string $location = null,
        ?CarbonImmutable $occurredAt = null,
    ): Shipment {
        $this->recorder->record($shipment, new TrackingEventData(
            status: $status,
            occurredAt: $occurredAt ?? CarbonImmutable::now(),
            descriptionAr: $description,
            location: $location,
            source: ShipmentEventSource::Manual,
        ));

        return $shipment->fresh(['events']);
    }
}
