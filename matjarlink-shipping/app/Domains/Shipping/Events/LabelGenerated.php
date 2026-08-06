<?php

declare(strict_types=1);

namespace App\Domains\Shipping\Events;

use App\Domains\Shipping\Models\Shipment;
use App\Domains\Shipping\Models\ShipmentLabel;
use Illuminate\Foundation\Events\Dispatchable;
use Illuminate\Queue\SerializesModels;

final class LabelGenerated
{
    use Dispatchable;
    use SerializesModels;

    public function __construct(
        public readonly Shipment $shipment,
        public readonly ShipmentLabel $label,
    ) {}
}
