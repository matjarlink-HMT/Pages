<?php

declare(strict_types=1);

namespace App\Domains\Shipping\DTOs;

final readonly class PickupResult
{
    public function __construct(
        public bool $success,
        public ?string $carrierReference = null,
        public ?string $message = null,
    ) {}
}
