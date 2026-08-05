<?php

declare(strict_types=1);

namespace App\Domains\Shipping\Integration\Exceptions;

final class CarrierUnavailableException extends CarrierException
{
    public function __construct(string $message = 'Carrier unavailable')
    {
        parent::__construct($message, 'SHIPPING_CARRIER_UNAVAILABLE', retryable: true);
    }
}
