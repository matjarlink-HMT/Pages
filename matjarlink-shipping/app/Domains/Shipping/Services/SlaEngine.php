<?php

declare(strict_types=1);

namespace App\Domains\Shipping\Services;

use App\Domains\Shipping\Models\Shipment;
use Carbon\CarbonImmutable;
use Carbon\CarbonInterface;

/**
 * الوعد بالتسليم وكشف التأخير والصمت.
 *
 * «متأخرة» و«صامتة» علامتان مستقلتان لا حالتان: شحنة قد تكون أثناء النقل
 * ومتأخرة وصامتة في آن واحد، وخلطها في حقل واحد يُفقد المعلومة.
 */
final class SlaEngine
{
    /** عطلة نهاية الأسبوع في عُمان: الجمعة والسبت. */
    private const WEEKEND = [CarbonInterface::FRIDAY, CarbonInterface::SATURDAY];

    public function promisedAt(int $etaMaxDays, ?CarbonInterface $from = null): CarbonImmutable
    {
        $date = CarbonImmutable::instance($from ?? now());

        /* بعد وقت القطع اليومي تُحتسب الشحنة على يوم العمل التالي. */
        if ($date->hour >= 15) {
            $date = $this->nextWorkingDay($date);
        }

        for ($i = 0; $i < max(1, $etaMaxDays); $i++) {
            $date = $this->nextWorkingDay($date);
        }

        return $date->setTime(18, 0);
    }

    public function isDelayed(Shipment $shipment): bool
    {
        return $shipment->promised_delivery_at !== null
            && ! $shipment->status->isTerminal()
            && $shipment->promised_delivery_at->isPast();
    }

    /** صمت التتبع مؤشر خطر أبكر من التأخير الفعلي. */
    public function isStale(Shipment $shipment, ?int $thresholdHours = null): bool
    {
        if ($shipment->status->isTerminal()) {
            return false;
        }

        $threshold = $thresholdHours ?? (int) config('shipping.stale_after_hours', 72);
        $last = $shipment->last_synced_at ?? $shipment->status_updated_at ?? $shipment->created_at;

        return $last !== null && $last->diffInHours(now()) >= $threshold;
    }

    /** جدولة المزامنة التالية حسب الحالة — لا نستنزف حدود الـ API بالتساوي. */
    public function nextSyncAt(Shipment $shipment): ?CarbonImmutable
    {
        if ($shipment->status->isTerminal()) {
            return null;
        }

        $minutes = (int) config(
            "shipping.sync_intervals.{$shipment->status->value}",
            config('shipping.sync_intervals.in_transit', 180),
        );

        /* الشركات التي تدفع Webhooks تحتاج استعلاماً يومياً كتسوية فقط. */
        if ($shipment->account?->carrier?->capabilities()->webhook) {
            $minutes = max($minutes, (int) config('shipping.sync_intervals.webhook_backstop', 1440));
        }

        return CarbonImmutable::now()->addMinutes($minutes);
    }

    private function nextWorkingDay(CarbonImmutable $date): CarbonImmutable
    {
        do {
            $date = $date->addDay();
        } while (in_array($date->dayOfWeek, self::WEEKEND, true));

        return $date;
    }
}
