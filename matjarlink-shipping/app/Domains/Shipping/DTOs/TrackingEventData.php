<?php

declare(strict_types=1);

namespace App\Domains\Shipping\DTOs;

use App\Domains\Shipping\Enums\ShipmentEventSource;
use App\Domains\Shipping\Enums\ShipmentStatus;
use Carbon\CarbonInterface;

final readonly class TrackingEventData
{
    public function __construct(
        public ShipmentStatus $status,
        public CarbonInterface $occurredAt,
        public ?string $carrierStatusCode = null,
        public ?string $carrierStatusText = null,
        public ?string $descriptionAr = null,
        public ?string $descriptionEn = null,
        public ?string $location = null,
        public ShipmentEventSource $source = ShipmentEventSource::Polling,
        public array $raw = [],
    ) {}

    /**
     * بصمة الحدث: أحداث الـ Webhook تصل مكررة وخارج ترتيبها،
     * والقيد الفريد على هذه البصمة يمنع التكرار في القاعدة لا في الكود.
     */
    public function hash(int $shipmentId): string
    {
        return sha1(implode('|', [
            $shipmentId,
            $this->status->value,
            $this->occurredAt->utc()->format('Y-m-d H:i'),
            (string) $this->carrierStatusCode,
        ]));
    }

    public function description(): string
    {
        return $this->descriptionAr
            ?? $this->carrierStatusText
            ?? __('shipping.status.'.$this->status->value);
    }
}
