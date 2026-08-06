<?php

declare(strict_types=1);

namespace App\Domains\Shipping\DTOs;

/** نتيجة إنشاء الشحنة لدى شركة الشحن. */
final readonly class CarrierShipmentResult
{
    public function __construct(
        public bool $success,
        public ?string $trackingNumber = null,
        public ?string $carrierShipmentId = null,
        public ?LabelFile $label = null,
        public ?float $cost = null,
        public array $costBreakdown = [],
        public ?int $etaMaxDays = null,
        public ?string $errorMessage = null,
        /** غير القابل لإعادة المحاولة يفشل فوراً بدل استهلاك الطابور. */
        public bool $retryable = false,
        public array $raw = [],
    ) {}

    public static function failure(string $message, bool $retryable = false, array $raw = []): self
    {
        return new self(success: false, errorMessage: $message, retryable: $retryable, raw: $raw);
    }
}
