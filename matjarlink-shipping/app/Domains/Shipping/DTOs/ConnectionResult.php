<?php

declare(strict_types=1);

namespace App\Domains\Shipping\DTOs;

final readonly class ConnectionResult
{
    public function __construct(
        public bool $success,
        public string $message,
        public ?int $durationMs = null,
        public array $details = [],
    ) {}

    public static function ok(string $message, ?int $durationMs = null, array $details = []): self
    {
        return new self(true, $message, $durationMs, $details);
    }

    public static function failed(string $message, ?int $durationMs = null): self
    {
        return new self(false, $message, $durationMs);
    }
}
