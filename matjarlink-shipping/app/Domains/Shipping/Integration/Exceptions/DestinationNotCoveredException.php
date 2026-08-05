<?php

declare(strict_types=1);

namespace App\Domains\Shipping\Integration\Exceptions;

final class DestinationNotCoveredException extends CarrierException
{
    public function __construct(string $destination = '')
    {
        parent::__construct("Destination not covered: {$destination}", 'SHIPPING_DESTINATION_NOT_COVERED');
    }
}
