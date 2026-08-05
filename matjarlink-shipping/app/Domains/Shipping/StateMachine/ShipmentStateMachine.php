<?php

declare(strict_types=1);

namespace App\Domains\Shipping\StateMachine;

use App\Domains\Shipping\Enums\ShipmentStatus as S;

/**
 * قواعد انتقال الحالة.
 *
 * ثلاثة مبادئ:
 *   ١. الحالة النهائية لا تُنقض — حدث متأخر من الشركة يُسجَّل ولا يغيّر النتيجة.
 *   ٢. لا رجوع للخلف في المسار الطبيعي إلا عبر مسار استثنائي معلن.
 *   ٣. المصدر الوحيد للحقيقة هو السجل الزمني، والحالة انعكاس له.
 */
final class ShipmentStateMachine
{
    /** @var array<string, list<S>> */
    private const TRANSITIONS = [
        'draft'            => [S::PendingCarrier, S::Created, S::Cancelled],
        'pending_carrier'  => [S::Created, S::CarrierError, S::Cancelled],
        'carrier_error'    => [S::PendingCarrier, S::Created, S::Cancelled],
        'created'          => [S::PickedUp, S::InTransit, S::Exception, S::Cancelled, S::Lost],
        'picked_up'        => [S::InTransit, S::OutForDelivery, S::Exception, S::Returning, S::Lost, S::Damaged],
        'in_transit'       => [S::InTransit, S::OutForDelivery, S::Exception, S::Returning, S::Lost, S::Damaged],
        'out_for_delivery' => [S::Delivered, S::FailedAttempt, S::Exception, S::Returning, S::Lost, S::Damaged],
        'failed_attempt'   => [S::OutForDelivery, S::Delivered, S::Returning, S::Exception, S::FailedAttempt],
        'exception'        => [S::InTransit, S::OutForDelivery, S::Returning, S::Delivered, S::Cancelled, S::Lost],
        'returning'        => [S::Returned, S::Exception, S::Lost, S::Damaged],
    ];

    public function canTransition(S $from, S $to): bool
    {
        if ($from === $to) {
            return false;
        }

        if ($from->isTerminal()) {
            return false;
        }

        return in_array($to, self::TRANSITIONS[$from->value] ?? [], true);
    }

    /** @return list<S> */
    public function allowedFrom(S $from): array
    {
        return $from->isTerminal() ? [] : (self::TRANSITIONS[$from->value] ?? []);
    }

    /**
     * أحداث الـ Webhook تصل خارج ترتيبها الزمني، فالحالة تُحسب من الحدث
     * الأحدث زمنياً لا من آخر حدث وصل.
     */
    public function resolve(S $current, S $incoming, bool $incomingIsNewer): S
    {
        if (! $incomingIsNewer || ! $this->canTransition($current, $incoming)) {
            return $current;
        }

        return $incoming;
    }
}
