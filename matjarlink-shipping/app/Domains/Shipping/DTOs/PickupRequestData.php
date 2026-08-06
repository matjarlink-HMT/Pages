<?php

declare(strict_types=1);

namespace App\Domains\Shipping\DTOs;

use Carbon\CarbonInterface;

final readonly class PickupRequestData
{
    /** @param list<string> $trackingNumbers */
    public function __construct(
        public AddressData $address,
        public CarbonInterface $date,
        public string $windowFrom,
        public string $windowTo,
        public int $piecesCount = 1,
        public array $trackingNumbers = [],
        public ?string $notes = null,
    ) {}
}
