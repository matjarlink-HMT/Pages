<?php

declare(strict_types=1);

namespace App\Domains\Shipping\DTOs;

final readonly class CancellationResult
{
    public function __construct(
        public bool $success,
        public ?string $message = null,
        /** هل استُردت رسوم الشحنة؟ يفيد المحاسبة ومطابقة الفواتير. */
        public bool $feeRefunded = false,
    ) {}

    public static function ok(bool $feeRefunded = false): self
    {
        return new self(true, null, $feeRefunded);
    }

    public static function failed(string $message): self
    {
        return new self(false, $message);
    }
}
