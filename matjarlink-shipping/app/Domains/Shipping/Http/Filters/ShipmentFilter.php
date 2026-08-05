<?php

declare(strict_types=1);

namespace App\Domains\Shipping\Http\Filters;

use App\Domains\Shipping\Enums\ShipmentStatus;
use Illuminate\Database\Eloquent\Builder;
use Illuminate\Http\Request;

/**
 * فلترة وفرز من قائمة بيضاء معلنة لا من مدخلات حرة:
 * يمنع حقن SQL ويضمن أن كل فرز مدعوم بفهرس.
 */
final class ShipmentFilter
{
    private const SORTABLE = [
        'created_at', 'reference', 'status', 'total_cost',
        'status_updated_at', 'promised_delivery_at', 'delivered_at',
    ];

    public function apply(Builder $query, Request $request): Builder
    {
        return $query
            ->when($request->filled('q'), fn (Builder $q) => $this->search($q, (string) $request->input('q')))
            ->when($request->filled('status'), fn (Builder $q) => $q->whereIn(
                'status',
                array_intersect((array) $request->input('status'), ShipmentStatus::values()),
            ))
            ->when($request->filled('carrier_id'), fn (Builder $q) => $q->whereIn('carrier_id', (array) $request->input('carrier_id')))
            ->when($request->filled('governorate'), fn (Builder $q) => $q->whereHas(
                'receiver',
                fn (Builder $r) => $r->whereIn('governorate', (array) $request->input('governorate')),
            ))
            ->when($request->boolean('is_cod'), fn (Builder $q) => $q->where('is_cod', true))
            ->when($request->boolean('is_delayed'), fn (Builder $q) => $q->where('is_delayed', true))
            ->when($request->boolean('is_stale'), fn (Builder $q) => $q->where('is_stale', true))
            ->when($request->boolean('attention'), fn (Builder $q) => $q->needsAttention())
            ->when($request->boolean('open'), fn (Builder $q) => $q->open())
            ->when($request->filled('date_from'), fn (Builder $q) => $q->whereDate('created_at', '>=', $request->date('date_from')))
            ->when($request->filled('date_to'), fn (Builder $q) => $q->whereDate('created_at', '<=', $request->date('date_to')))
            ->orderBy(...$this->sort($request));
    }

    private function search(Builder $query, string $term): Builder
    {
        $term = trim($term);

        return $query->where(function (Builder $q) use ($term): void {
            $q->where('reference', 'like', "{$term}%")
                ->orWhere('tracking_number', 'like', "{$term}%")
                ->orWhereHas('receiver', function (Builder $r) use ($term): void {
                    $r->where('name', 'like', "%{$term}%")->orWhere('phone', 'like', "%{$term}%");
                });
        });
    }

    /** @return array{0: string, 1: string} */
    private function sort(Request $request): array
    {
        $sort = (string) $request->input('sort', '-created_at');
        $direction = str_starts_with($sort, '-') ? 'desc' : 'asc';
        $column = ltrim($sort, '-+');

        return [in_array($column, self::SORTABLE, true) ? $column : 'created_at', $direction];
    }
}
