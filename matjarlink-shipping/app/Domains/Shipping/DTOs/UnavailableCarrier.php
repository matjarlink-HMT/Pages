<?php

declare(strict_types=1);

namespace App\Domains\Shipping\DTOs;

/**
 * الشركة غير المتاحة تُعرض مع سببها بدل إخفائها.
 * المستخدم يحتاج أن يعرف أنها استُبعدت لعدم التغطية لا لأنها غالية.
 */
final readonly class UnavailableCarrier
{
    public function __construct(
        public string $carrierCode,
        public string $carrierName,
        public string $reason,
    ) {}

    public function toArray(): array
    {
        return ['carrier_code' => $this->carrierCode, 'carrier_name' => $this->carrierName, 'reason' => $this->reason];
    }
}
