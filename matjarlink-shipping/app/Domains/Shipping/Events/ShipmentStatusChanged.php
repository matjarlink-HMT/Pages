<?php

declare(strict_types=1);

namespace App\Domains\Shipping\Events;

use App\Domains\Shipping\Enums\ShipmentStatus;
use App\Domains\Shipping\Models\Shipment;
use Illuminate\Foundation\Events\Dispatchable;
use Illuminate\Queue\SerializesModels;

/** الحدث الذي تتفرّع منه كل الآثار: الطلب، الإشعارات، التحليلات، سجل النشاط. */
final class ShipmentStatusChanged
{
    use Dispatchable;
    use SerializesModels;

    public function __construct(
        public readonly Shipment $shipment,
        public readonly ShipmentStatus $from,
        public readonly ShipmentStatus $to,
    ) {}
}
