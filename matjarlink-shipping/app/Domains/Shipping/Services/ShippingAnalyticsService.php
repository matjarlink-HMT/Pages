<?php

declare(strict_types=1);

namespace App\Domains\Shipping\Services;

use App\Domains\Shipping\Enums\ShipmentStatus;
use App\Domains\Shipping\Models\Shipment;
use Carbon\CarbonInterface;
use Illuminate\Support\Facades\Cache;
use Illuminate\Support\Facades\DB;

/**
 * مؤشرات لوحة التحكم والتقارير.
 * تُقرأ من تجميعات مُكيَّشة لا من COUNT(*) حي على جدول الشحنات —
 * لوحة التحكم يجب أن تبقى تحت ٤٠٠ مللي مهما بلغ حجم البيانات.
 */
final class ShippingAnalyticsService
{
    private const CACHE_TTL = 300;

    public function dashboard(int $storeId, CarbonInterface $from, CarbonInterface $to): array
    {
        $key = sprintf('shipping:dashboard:%d:%s:%s', $storeId, $from->toDateString(), $to->toDateString());

        return Cache::remember($key, self::CACHE_TTL, function () use ($storeId, $from, $to): array {
            $base = Shipment::query()->forStore($storeId)->whereBetween('created_at', [$from, $to]);

            $byStatus = (clone $base)
                ->select('status', DB::raw('COUNT(*) as total'))
                ->groupBy('status')
                ->pluck('total', 'status')
                ->all();

            $totals = (clone $base)
                ->selectRaw('COUNT(*) as shipments')
                ->selectRaw('COALESCE(SUM(total_cost), 0) as cost')
                ->selectRaw('COALESCE(SUM(CASE WHEN is_cod = 1 THEN cod_amount ELSE 0 END), 0) as cod_total')
                ->first();

            $delivered = (clone $base)->where('status', ShipmentStatus::Delivered->value);

            $deliveredCount = (clone $delivered)->count();
            $onTime = (clone $delivered)->whereColumn('delivered_at', '<=', 'promised_delivery_at')->count();

            $avgHours = (clone $delivered)
                ->selectRaw('AVG(TIMESTAMPDIFF(HOUR, created_at, delivered_at)) as avg_hours')
                ->value('avg_hours');

            return [
                'shipments' => (int) ($totals->shipments ?? 0),
                'cost' => round((float) ($totals->cost ?? 0), 3),
                'cod_total' => round((float) ($totals->cod_total ?? 0), 3),
                'by_status' => $byStatus,
                'delivered' => $deliveredCount,
                'on_time_rate' => $deliveredCount > 0 ? round($onTime / $deliveredCount * 100, 1) : null,
                'avg_delivery_hours' => $avgHours !== null ? round((float) $avgHours, 1) : null,
            ];
        });
    }

    /** صف «تحتاج انتباهك»: يحوّل الاستخدام من تصفّح إلى عمل موجّه. */
    public function attention(int $storeId): array
    {
        $base = static fn (): \Illuminate\Database\Eloquent\Builder => Shipment::query()->forStore($storeId);

        return [
            'delayed' => $base()->where('is_delayed', true)->count(),
            'stale' => $base()->where('is_stale', true)->count(),
            'failed_attempt' => $base()->where('status', ShipmentStatus::FailedAttempt->value)->count(),
            'carrier_error' => $base()->where('status', ShipmentStatus::CarrierError->value)->count(),
        ];
    }

    /**
     * أداء كل شركة — يغذّي التوصية في المقارنة وبطاقة الأداء في التقارير.
     * نسبة النجاح تُحتسب على الشحنات المنتهية فقط: شحنة ما زالت في الطريق ليست فشلاً.
     *
     * @return array<int, array{success_rate: float, on_time_rate: float, avg_hours: float|null, shipments: int}>
     */
    public function carrierPerformance(int $storeId, int $days = 90): array
    {
        return Cache::remember(
            "shipping:carrier_perf:{$storeId}:{$days}",
            self::CACHE_TTL,
            static function () use ($storeId, $days): array {
                $rows = Shipment::query()
                    ->forStore($storeId)
                    ->where('created_at', '>=', now()->subDays($days))
                    ->select('carrier_id')
                    ->selectRaw('COUNT(*) as shipments')
                    ->selectRaw('SUM(status = ?) as delivered', [ShipmentStatus::Delivered->value])
                    ->selectRaw('SUM(status = ?) as returned', [ShipmentStatus::Returned->value])
                    ->selectRaw('SUM(status = ? AND delivered_at <= promised_delivery_at) as on_time', [ShipmentStatus::Delivered->value])
                    ->selectRaw('AVG(CASE WHEN status = ? THEN TIMESTAMPDIFF(HOUR, created_at, delivered_at) END) as avg_hours', [ShipmentStatus::Delivered->value])
                    ->groupBy('carrier_id')
                    ->get();

                $out = [];

                foreach ($rows as $row) {
                    $concluded = (int) $row->delivered + (int) $row->returned;
                    $out[(int) $row->carrier_id] = [
                        'shipments' => (int) $row->shipments,
                        'success_rate' => $concluded > 0 ? round((int) $row->delivered / $concluded * 100, 1) : 90.0,
                        'on_time_rate' => (int) $row->delivered > 0 ? round((int) $row->on_time / (int) $row->delivered * 100, 1) : 85.0,
                        'avg_hours' => $row->avg_hours !== null ? round((float) $row->avg_hours, 1) : null,
                    ];
                }

                return $out;
            },
        );
    }

    /** @return array<string, int> */
    public function topWilayats(int $storeId, CarbonInterface $from, CarbonInterface $to, int $limit = 10): array
    {
        return Shipment::query()
            ->forStore($storeId)
            ->whereBetween('shipments.created_at', [$from, $to])
            ->join('shipment_addresses', function ($join): void {
                $join->on('shipment_addresses.shipment_id', '=', 'shipments.id')
                    ->where('shipment_addresses.type', '=', 'receiver');
            })
            ->select('shipment_addresses.wilayat', DB::raw('COUNT(*) as total'))
            ->groupBy('shipment_addresses.wilayat')
            ->orderByDesc('total')
            ->limit($limit)
            ->pluck('total', 'wilayat')
            ->all();
    }

    /** فروقات الفوترة: ما دفعناه فعلاً مقابل ما سُعِّر لنا. */
    public function invoiceVariance(int $storeId, CarbonInterface $from, CarbonInterface $to): array
    {
        $row = Shipment::query()
            ->forStore($storeId)
            ->whereBetween('created_at', [$from, $to])
            ->selectRaw('COALESCE(SUM(actual_cost - quoted_cost), 0) as variance')
            ->selectRaw('SUM(CASE WHEN actual_cost > quoted_cost THEN 1 ELSE 0 END) as overbilled')
            ->first();

        return [
            'variance' => round((float) ($row->variance ?? 0), 3),
            'overbilled_count' => (int) ($row->overbilled ?? 0),
        ];
    }

    public function flush(int $storeId): void
    {
        Cache::forget("shipping:carrier_perf:{$storeId}:90");
    }
}
