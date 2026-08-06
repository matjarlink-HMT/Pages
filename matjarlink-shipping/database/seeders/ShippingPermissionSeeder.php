<?php

declare(strict_types=1);

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\Log;

/**
 * صلاحيات الوحدة وأدوارها الخمسة.
 * تستخدم نظام الصلاحيات القائم في متجرلينك (spatie/laravel-permission)
 * ولا تنشئ نظاماً موازياً.
 */
final class ShippingPermissionSeeder extends Seeder
{
    private const PERMISSIONS = [
        'shipping.dashboard.view',
        'shipping.shipments.view_all',
        'shipping.shipments.view_own',
        'shipping.shipments.create',
        'shipping.shipments.update',
        'shipping.shipments.cancel',
        'shipping.shipments.manual_event',
        'shipping.labels.print',
        'shipping.costs.view',
        'shipping.carriers.view',
        'shipping.carriers.manage',
        'shipping.carriers.credentials',
        'shipping.rates.manage',
        'shipping.pickups.manage',
        'shipping.returns.manage',
        'shipping.claims.manage',
        'shipping.reports.view',
        'shipping.reports.financial',
        'shipping.settings.manage',
        'shipping.logs.view',
    ];

    /** @var array<string, list<string>> */
    private const ROLES = [
        'مدير النظام' => ['*'],

        'مدير العمليات' => [
            'shipping.dashboard.view', 'shipping.shipments.view_all', 'shipping.shipments.create',
            'shipping.shipments.update', 'shipping.shipments.cancel', 'shipping.shipments.manual_event',
            'shipping.labels.print', 'shipping.costs.view', 'shipping.carriers.view',
            'shipping.carriers.manage', 'shipping.rates.manage', 'shipping.pickups.manage',
            'shipping.returns.manage', 'shipping.claims.manage', 'shipping.reports.view',
            'shipping.reports.financial', 'shipping.settings.manage', 'shipping.logs.view',
        ],

        /* موظف الشحن يُنشئ ويطبع دون أن يرى ما يدفعه المتجر. */
        'موظف الشحن' => [
            'shipping.dashboard.view', 'shipping.shipments.view_all', 'shipping.shipments.create',
            'shipping.shipments.update', 'shipping.shipments.cancel', 'shipping.shipments.manual_event',
            'shipping.labels.print', 'shipping.carriers.view', 'shipping.pickups.manage',
            'shipping.returns.manage',
        ],

        /* خدمة العملاء ترى كل شيء وتسجّل أحداثاً، ولا تنشئ شحنات. */
        'خدمة العملاء' => [
            'shipping.dashboard.view', 'shipping.shipments.view_all', 'shipping.shipments.manual_event',
            'shipping.carriers.view', 'shipping.returns.manage', 'shipping.claims.manage',
            'shipping.reports.view',
        ],

        'المحاسبة' => [
            'shipping.dashboard.view', 'shipping.shipments.view_all', 'shipping.costs.view',
            'shipping.carriers.view', 'shipping.claims.manage', 'shipping.reports.view',
            'shipping.reports.financial',
        ],
    ];

    public function run(): void
    {
        if (! class_exists(\Spatie\Permission\Models\Permission::class)) {
            Log::warning('shipping: spatie/laravel-permission غير مثبّت — تخطّي بذر الصلاحيات.');

            return;
        }

        $permissionModel = \Spatie\Permission\Models\Permission::class;
        $roleModel = \Spatie\Permission\Models\Role::class;

        foreach (self::PERMISSIONS as $permission) {
            $permissionModel::findOrCreate($permission, 'web');
        }

        foreach (self::ROLES as $roleName => $permissions) {
            $role = $roleModel::findOrCreate($roleName, 'web');

            $role->givePermissionTo($permissions === ['*'] ? self::PERMISSIONS : $permissions);
        }
    }
}
