<?php

declare(strict_types=1);

namespace App\Domains\Shipping\Events;

use App\Domains\Shipping\Models\StoreCarrierAccount;
use Illuminate\Foundation\Events\Dispatchable;
use Illuminate\Queue\SerializesModels;

final class CarrierConnectionFailed
{
    use Dispatchable;
    use SerializesModels;

    public function __construct(
        public readonly StoreCarrierAccount $account,
        public readonly string $reason,
    ) {}
}
