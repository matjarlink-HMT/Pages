<?php

declare(strict_types=1);

namespace App\Domains\Shipping\Enums;

/**
 * الحالات الداخلية الموحّدة لكل شركات الشحن.
 * حالات الشركات تُترجَم إلى هذه القيم عبر StatusNormalizer، فلا تعرف
 * بقية الوحدة شيئاً عن مسميات أي شركة.
 */
enum ShipmentStatus: string
{
    case Draft           = 'draft';
    case PendingCarrier  = 'pending_carrier';
    case CarrierError    = 'carrier_error';
    case Created         = 'created';
    case PickedUp        = 'picked_up';
    case InTransit       = 'in_transit';
    case OutForDelivery  = 'out_for_delivery';
    case Delivered       = 'delivered';
    case FailedAttempt   = 'failed_attempt';
    case Exception       = 'exception';
    case Returning       = 'returning';
    case Returned        = 'returned';
    case Cancelled       = 'cancelled';
    case Lost            = 'lost';
    case Damaged         = 'damaged';

    public function label(): string
    {
        return __('shipping.status.'.$this->value);
    }

    /** حالة نهائية: لا حدث لاحق يغيّرها. */
    public function isTerminal(): bool
    {
        return in_array($this, [
            self::Delivered, self::Returned, self::Cancelled, self::Lost, self::Damaged,
        ], true);
    }

    /** تحتاج تدخّلاً بشرياً — تُبرز في صف «تحتاج انتباهك». */
    public function needsAttention(): bool
    {
        return in_array($this, [
            self::CarrierError, self::FailedAttempt, self::Exception, self::Lost, self::Damaged,
        ], true);
    }

    /** ترتيب المرحلة على شريط التقدّم (٠ = خارج المسار الطبيعي). */
    public function stage(): int
    {
        return match ($this) {
            self::Created                                   => 1,
            self::PickedUp                                  => 2,
            self::InTransit, self::Exception, self::Returning => 3,
            self::OutForDelivery, self::FailedAttempt       => 4,
            self::Delivered, self::Returned                 => 5,
            default                                         => 0,
        };
    }

    /** مفتاح لون دلالي — الواجهة تترجمه إلى نظام تصميم المنصة. */
    public function color(): string
    {
        return match ($this) {
            self::Delivered                              => 'green',
            self::OutForDelivery, self::Returning        => 'amber',
            self::PickedUp, self::InTransit              => 'purple',
            self::Created                                => 'blue',
            self::CarrierError, self::FailedAttempt,
            self::Exception, self::Lost, self::Damaged   => 'red',
            default                                      => 'gray',
        };
    }

    /** الحالات التي ما زالت تستحق مزامنة مع شركة الشحن. */
    public static function syncable(): array
    {
        return array_values(array_filter(
            self::cases(),
            static fn (self $s): bool => ! $s->isTerminal() && $s !== self::Draft,
        ));
    }

    public static function values(): array
    {
        return array_column(self::cases(), 'value');
    }
}
