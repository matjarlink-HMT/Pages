<?php

declare(strict_types=1);

namespace App\Domains\Shipping\Events;

use App\Domains\Shipping\Models\Shipment;
use Illuminate\Foundation\Events\Dispatchable;
use Illuminate\Queue\SerializesModels;

final class ShipmentCreated
{
    use Dispatchable;
    use SerializesModels;

    public function __construct(public readonly Shipment $shipment) {}
}
