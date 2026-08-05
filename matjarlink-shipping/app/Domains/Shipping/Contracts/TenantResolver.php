<?php

declare(strict_types=1);

namespace App\Domains\Shipping\Contracts;

/**
 * تحلّه المنصة بما يناسب نظام المستأجرين لديها.
 * الوحدة لا تفترض شكل جدول المتاجر ولا كيف يُعرف المتجر الحالي.
 */
interface TenantResolver
{
    public function currentStoreId(): ?int;
}
