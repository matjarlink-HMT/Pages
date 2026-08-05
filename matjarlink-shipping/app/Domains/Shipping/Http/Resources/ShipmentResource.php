<?php

declare(strict_types=1);

namespace App\Domains\Shipping\Http\Resources;

use App\Domains\Shipping\Models\Shipment;
use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;

/** @mixin Shipment */
final class ShipmentResource extends JsonResource
{
    public function toArray(Request $request): array
    {
        $canSeeCosts = $request->user()?->can('viewCosts', Shipment::class) ?? false;

        return [
            'uuid' => $this->uuid,
            'reference' => $this->reference,
            'order_id' => $this->order_id,
            'tracking_number' => $this->tracking_number,
            'status' => [
                'value' => $this->status->value,
                'label' => $this->status->label(),
                'color' => $this->status->color(),
                'stage' => $this->status->stage(),
                'is_terminal' => $this->status->isTerminal(),
            ],
            'flags' => [
                'is_delayed' => (bool) $this->is_delayed,
                'is_stale' => (bool) $this->is_stale,
                'is_cod' => (bool) $this->is_cod,
            ],
            'carrier' => $this->whenLoaded('carrier', fn (): array => [
                'id' => $this->carrier->id,
                'code' => $this->carrier->code,
                'name' => $this->carrier->name(),
            ]),
            'receiver' => $this->whenLoaded('receiver', fn (): ?array => $this->receiver === null ? null : [
                'name' => $this->receiver->name,
                'governorate' => $this->receiver->governorate,
                'wilayat' => $this->receiver->wilayat,
            ]),
            'weight' => [
                'total_kg' => (float) $this->total_weight_kg,
                'billable_kg' => (float) $this->billable_weight_kg,
                'pieces' => (int) $this->pieces_count,
            ],
            /* حذف كامل للحقول المالية لغير المخوّلين — لا إرسال ثم إخفاء. */
            $this->mergeWhen($canSeeCosts, fn (): array => [
                'costs' => [
                    'quoted' => (float) $this->quoted_cost,
                    'actual' => (float) $this->actual_cost,
                    'total' => (float) $this->total_cost,
                    'variance' => $this->costVariance(),
                    'cod_amount' => (float) $this->cod_amount,
                    'currency' => $this->currency,
                ],
            ]),
            'promised_delivery_at' => $this->promised_delivery_at?->toIso8601String(),
            'delivered_at' => $this->delivered_at?->toIso8601String(),
            'created_at' => $this->created_at?->toIso8601String(),
            'status_updated_at' => $this->status_updated_at?->toIso8601String(),
        ];
    }
}
