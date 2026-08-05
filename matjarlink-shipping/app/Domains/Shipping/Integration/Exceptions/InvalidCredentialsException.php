<?php

declare(strict_types=1);

namespace App\Domains\Shipping\Integration\Exceptions;

final class InvalidCredentialsException extends CarrierException
{
    public function __construct(string $message = 'Invalid carrier credentials')
    {
        parent::__construct($message, 'SHIPPING_INVALID_CREDENTIALS');
    }
}
