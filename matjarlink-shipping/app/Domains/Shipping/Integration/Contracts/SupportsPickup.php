<?php

declare(strict_types=1);

namespace App\Domains\Shipping\Integration\Contracts;

use App\Domains\Shipping\DTOs\PickupRequestData;
use App\Domains\Shipping\DTOs\PickupResult;

interface SupportsPickup
{
    public function schedulePickup(PickupRequestData $request): PickupResult;

    public function cancelPickup(string $carrierReference): bool;
}
