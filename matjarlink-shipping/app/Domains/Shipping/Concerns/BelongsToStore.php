<?php

declare(strict_types=1);

namespace App\Domains\Shipping\Concerns;

use App\Domains\Shipping\Contracts\TenantResolver;
use App\Domains\Shipping\Scopes\TenantScope;
use Illuminate\Database\Eloquent\Builder;

trait BelongsToStore
{
    public static function bootBelongsToStore(): void
    {
        static::addGlobalScope(new TenantScope());

        /* store_id يُملأ من سياق الجلسة ولا يُقبل أبداً من مدخلات المستخدم. */
        static::creating(static function ($model): void {
            if ($model->store_id === null) {
                $model->store_id = app(TenantResolver::class)->currentStoreId();
            }
        });
    }

    /** للمهام الخلفية والتقارير عبر المتاجر — استخدام صريح ومقصود. */
    public function scopeAcrossStores(Builder $query): Builder
    {
        return $query->withoutGlobalScope(TenantScope::class);
    }

    public function scopeForStore(Builder $query, int $storeId): Builder
    {
        return $query->withoutGlobalScope(TenantScope::class)
            ->where($this->qualifyColumn('store_id'), $storeId);
    }
}
