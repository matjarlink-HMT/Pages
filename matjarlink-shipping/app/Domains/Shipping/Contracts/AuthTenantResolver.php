<?php

declare(strict_types=1);

namespace App\Domains\Shipping\Contracts;

use Illuminate\Contracts\Auth\Factory as AuthFactory;

/** التحليل الافتراضي: المتجر المرتبط بالمستخدم المسجّل دخوله. */
final readonly class AuthTenantResolver implements TenantResolver
{
    public function __construct(private AuthFactory $auth) {}

    public function currentStoreId(): ?int
    {
        $user = $this->auth->guard()->user();

        return isset($user->store_id) ? (int) $user->store_id : null;
    }
}
