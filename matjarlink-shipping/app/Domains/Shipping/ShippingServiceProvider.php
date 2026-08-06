<?php

declare(strict_types=1);

namespace App\Domains\Shipping;

use App\Domains\Shipping\Contracts\AuthTenantResolver;
use App\Domains\Shipping\Contracts\NullOrderBridge;
use App\Domains\Shipping\Contracts\OrderBridge;
use App\Domains\Shipping\Contracts\TenantResolver;
use App\Domains\Shipping\Events\ShipmentCancelled;
use App\Domains\Shipping\Events\ShipmentCreated;
use App\Domains\Shipping\Events\ShipmentStatusChanged;
use App\Domains\Shipping\Integration\CarrierRegistry;
use App\Domains\Shipping\Jobs\DetectDelayedShipmentsJob;
use App\Domains\Shipping\Jobs\PruneApiLogsJob;
use App\Domains\Shipping\Jobs\SyncShipmentTrackingJob;
use App\Domains\Shipping\Listeners\RecordShipmentActivity;
use App\Domains\Shipping\Listeners\ReleaseInventoryOnDelivery;
use App\Domains\Shipping\Listeners\UpdateOrderFromShipment;
use App\Domains\Shipping\Models\Shipment;
use App\Domains\Shipping\Models\StoreCarrierAccount;
use App\Domains\Shipping\Policies\CarrierAccountPolicy;
use App\Domains\Shipping\Policies\ShipmentPolicy;
use App\Domains\Shipping\Services\ShipmentEventRecorder;
use Illuminate\Console\Scheduling\Schedule;
use Illuminate\Support\Facades\Blade;
use Illuminate\Support\Facades\Event;
use Illuminate\Support\Facades\Gate;
use Illuminate\Support\Facades\Route;
use Illuminate\Support\ServiceProvider;

/**
 * نقطة تركيب الوحدة. إضافتها إلى المنصة = تسجيل هذا المزوّد فقط:
 *   config/app.php  →  App\Domains\Shipping\ShippingServiceProvider::class
 */
final class ShippingServiceProvider extends ServiceProvider
{
    public function register(): void
    {
        $this->mergeConfigFrom(__DIR__.'/../../../config/shipping.php', 'shipping');

        /* تُبدّلهما المنصة بتحقيقاتها الحقيقية دون لمس كود الوحدة. */
        $this->app->bindIf(TenantResolver::class, AuthTenantResolver::class);
        $this->app->bindIf(OrderBridge::class, NullOrderBridge::class);

        $this->app->singleton(CarrierRegistry::class);
        $this->app->singleton(ShipmentEventRecorder::class);
    }

    public function boot(): void
    {
        $this->loadMigrationsFrom(__DIR__.'/../../../database/migrations/shipping');
        $this->loadViewsFrom(__DIR__.'/../../../resources/views/shipping', 'shipping');
        $this->loadTranslationsFrom(__DIR__.'/../../../lang', 'shipping');

        /* يجعل <x-shipping.status-badge> يحلّ إلى shipping/components/status-badge.blade.php */
        Blade::anonymousComponentNamespace('shipping.components', 'shipping');

        $this->registerRoutes();
        $this->registerPolicies();
        $this->registerEvents();
        $this->registerSchedule();

        $this->publishes([
            __DIR__.'/../../../config/shipping.php' => config_path('shipping.php'),
        ], 'shipping-config');
    }

    private function registerRoutes(): void
    {
        Route::group([
            'prefix' => config('shipping.routes.prefix', 'shipping'),
            'middleware' => config('shipping.routes.middleware', ['web', 'auth']),
        ], function (): void {
            $this->loadRoutesFrom(__DIR__.'/../../../routes/shipping.php');
        });
    }

    private function registerPolicies(): void
    {
        Gate::policy(Shipment::class, ShipmentPolicy::class);
        Gate::policy(StoreCarrierAccount::class, CarrierAccountPolicy::class);
    }

    private function registerEvents(): void
    {
        Event::listen(ShipmentStatusChanged::class, UpdateOrderFromShipment::class);
        Event::listen(ShipmentStatusChanged::class, ReleaseInventoryOnDelivery::class);
        Event::listen(ShipmentStatusChanged::class, [RecordShipmentActivity::class, 'statusChanged']);
        Event::listen(ShipmentCreated::class, [RecordShipmentActivity::class, 'created']);
        Event::listen(ShipmentCancelled::class, [RecordShipmentActivity::class, 'cancelled']);
    }

    private function registerSchedule(): void
    {
        $this->app->booted(function (): void {
            /** @var Schedule $schedule */
            $schedule = $this->app->make(Schedule::class);

            /* المزامنة التكيّفية: الشحنات المستحقة فقط، لا الجدول كله. */
            $schedule->call(static function (): void {
                Shipment::query()->withoutGlobalScopes()->dueForSync()
                    ->select('id')->chunkById(200, static function ($shipments): void {
                        foreach ($shipments as $shipment) {
                            SyncShipmentTrackingJob::dispatch($shipment->id);
                        }
                    });
            })->everyFifteenMinutes()->name('shipping:sync-tracking')->withoutOverlapping();

            $schedule->job(new DetectDelayedShipmentsJob())->hourly()->name('shipping:detect-delays');
            $schedule->job(new PruneApiLogsJob())->weekly()->name('shipping:prune-logs');
        });
    }
}
