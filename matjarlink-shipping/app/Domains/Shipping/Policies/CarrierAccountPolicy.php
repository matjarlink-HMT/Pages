<?php

declare(strict_types=1);

namespace App\Domains\Shipping\Policies;

use App\Domains\Shipping\Models\StoreCarrierAccount;
use Illuminate\Foundation\Auth\User;

final class CarrierAccountPolicy
{
    public function viewAny(User $user): bool
    {
        return $user->can('shipping.carriers.view');
    }

    public function manage(User $user): bool
    {
        return $user->can('shipping.carriers.manage');
    }

    public function update(User $user, StoreCarrierAccount $account): bool
    {
        return $user->can('shipping.carriers.manage');
    }

    public function delete(User $user, StoreCarrierAccount $account): bool
    {
        return $user->can('shipping.carriers.manage');
    }

    /** مفاتيح الـ API لمدير النظام حصراً — حتى مدير العمليات لا يملكها. */
    public function manageCredentials(User $user): bool
    {
        return $user->can('shipping.carriers.credentials');
    }
}
