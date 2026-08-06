<?php

declare(strict_types=1);

namespace App\Domains\Shipping\Actions;

use App\Domains\Shipping\DTOs\ShipmentRequest;
use App\Domains\Shipping\Models\Shipment;
use App\Domains\Shipping\Services\LabelService;
use App\Domains\Shipping\Services\ShipmentCreationService;

/** حالة استخدام واحدة: أنشئ الشحنة ثم أصدر بوليصتها. */
final readonly class CreateShipmentAction
{
    public function __construct(
        private ShipmentCreationService $creator,
        private LabelService $labels,
    ) {}

    public function execute(int $storeId, ShipmentRequest $request, bool $generateLabel = true): Shipment
    {
        $shipment = $this->creator->create($storeId, $request);

        if ($generateLabel && $shipment->tracking_number !== null) {
            $this->labels->generate($shipment);
        }

        return $shipment->fresh(['carrier', 'sender', 'receiver', 'packages', 'labels']);
    }
}
