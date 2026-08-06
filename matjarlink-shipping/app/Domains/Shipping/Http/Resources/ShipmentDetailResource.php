<?php

declare(strict_types=1);

namespace App\Domains\Shipping\Http\Resources;

use App\Domains\Shipping\Models\Shipment;
use App\Domains\Shipping\Models\ShipmentEvent;
use Illuminate\Http\Request;

/** @mixin Shipment */
final class ShipmentDetailResource extends ShipmentResource
{
    public function toArray(Request $request): array
    {
        return parent::toArray($request) + [
            'service' => ['code' => $this->service_code, 'name' => $this->service_name],
            'sender' => $this->whenLoaded('sender', fn (): ?array => $this->sender?->only([
                'name', 'phone', 'governorate', 'wilayat', 'street', 'landmark',
            ])),
            'receiver_full' => $this->whenLoaded('receiver', fn (): ?array => $this->receiver?->only([
                'name', 'phone', 'alt_phone', 'governorate', 'wilayat', 'area', 'street', 'building', 'landmark',
            ])),
            'packages' => $this->whenLoaded('packages', fn (): array => $this->packages->map->only([
                'piece_no', 'weight_kg', 'length_cm', 'width_cm', 'height_cm', 'barcode',
            ])->all()),
            'items' => $this->whenLoaded('items', fn (): array => $this->items->map->only([
                'sku', 'name', 'quantity', 'unit_value',
            ])->all()),
            'timeline' => $this->whenLoaded('events', fn (): array => $this->events->map(
                static fn (ShipmentEvent $e): array => [
                    'status' => $e->status->value,
                    'label' => $e->status->label(),
                    'color' => $e->status->color(),
                    'description' => $e->description(),
                    'location' => $e->location,
                    'occurred_at' => $e->occurred_at?->toIso8601String(),
                    'source' => $e->source->value,
                    'source_label' => $e->source->label(),
                ],
            )->all()),
            'notes' => $this->notes,
        ];
    }
}
