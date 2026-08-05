<?php

declare(strict_types=1);

namespace App\Domains\Shipping\Integration\Exceptions;

use RuntimeException;

class CarrierException extends RuntimeException
{
    public function __construct(
        string $message,
        public readonly string $errorCode = 'SHIPPING_CARRIER_ERROR',
        public readonly bool $retryable = false,
    ) {
        parent::__construct($message);
    }

    /** رسالة عربية جاهزة للعرض — لا تُسرَّب نصوص مزوّد الخدمة للمستخدم. */
    public function userMessage(): string
    {
        return __('shipping.errors.'.strtolower($this->errorCode));
    }
}
