<?php

declare(strict_types=1);

namespace App\Domains\Shipping\Scopes;

use App\Domains\Shipping\Contracts\TenantResolver;
use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Scope;

/**
 * عزل المستأجرين افتراضي لا اختياري: لا استعلام على بيانات الشحن
 * يخرج بلا قيد store_id حتى لو نسي المطوّر إضافته.
 */
final class TenantScope implements Scope
{
    public function apply(Builder $builder, Model $model): void
    {
        $storeId = app(TenantResolver::class)->currentStoreId();

        if ($storeId !== null) {
            $builder->where($model->qualifyColumn('store_id'), $storeId);
        }
    }
}
