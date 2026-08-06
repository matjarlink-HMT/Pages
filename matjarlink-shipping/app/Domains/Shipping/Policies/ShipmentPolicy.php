<?php

declare(strict_types=1);

namespace App\Domains\Shipping\Policies;

use App\Domains\Shipping\Models\Shipment;
use Illuminate\Foundation\Auth\User;

/**
 * الفرض الحقيقي هنا وفي طبقة Resource — الإخفاء في الواجهة تجميلي.
 * أهم قاعدة: موظف الشحن يُنشئ ويطبع دون أن يرى ما يدفعه المتجر.
 */
final class ShipmentPolicy
{
    public function viewAny(User $user): bool
    {
        return $user->can('shipping.shipments.view_all') || $user->can('shipping.shipments.view_own');
    }

    public function view(User $user, Shipment $shipment): bool
    {
        if ($user->can('shipping.shipments.view_all')) {
            return true;
        }

        return $user->can('shipping.shipments.view_own') && $shipment->created_by === $user->getAuthIdentifier();
    }

    public function create(User $user): bool
    {
        return $user->can('shipping.shipments.create');
    }

    public function update(User $user, Shipment $shipment): bool
    {
        return $user->can('shipping.shipments.update') && ! $shipment->status->isTerminal();
    }

    public function cancel(User $user, Shipment $shipment): bool
    {
        return $user->can('shipping.shipments.cancel') && ! $shipment->status->isTerminal();
    }

    public function recordEvent(User $user, Shipment $shipment): bool
    {
        return $user->can('shipping.shipments.manual_event') && ! $shipment->status->isTerminal();
    }

    public function printLabel(User $user, Shipment $shipment): bool
    {
        return $user->can('shipping.labels.print');
    }

    /** التكاليف تُحذف من الرد لمن لا يملك الصلاحية، لا تُخفى بـ CSS. */
    public function viewCosts(User $user): bool
    {
        return $user->can('shipping.costs.view');
    }
}
