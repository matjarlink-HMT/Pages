<?php

declare(strict_types=1);

namespace Tests\Feature\Shipping;

use App\Domains\Shipping\Contracts\TenantResolver;
use App\Domains\Shipping\Models\Shipment;
use Database\Seeders\ShippingCarrierSeeder;
use Database\Seeders\ShippingDemoSeeder;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

/**
 * اختبار إلزامي في CI: متجر «أ» لا يرى بيانات متجر «ب» بأي حال.
 * عزل المستأجرين افتراضي لا اختياري.
 */
final class TenantIsolationTest extends TestCase
{
    use RefreshDatabase;

    public function test_store_cannot_see_another_stores_shipments(): void
    {
        $this->seed(ShippingCarrierSeeder::class);
        (new ShippingDemoSeeder())->run(1);
        (new ShippingDemoSeeder())->run(2);

        $this->actingAsStore(1);
        Shipment::query()->create($this->shipmentAttributes(1, 'SHP-2026-000001', 'key-one'));

        $this->actingAsStore(2);
        Shipment::query()->create($this->shipmentAttributes(2, 'SHP-2026-000002', 'key-two'));

        self::assertSame(1, Shipment::query()->count());
        self::assertSame('SHP-2026-000002', Shipment::query()->first()->reference);

        $this->actingAsStore(1);
        self::assertSame('SHP-2026-000001', Shipment::query()->first()->reference);

        /* تجاوز النطاق صريح ومقصود — للمهام الخلفية فقط. */
        self::assertSame(2, Shipment::query()->withoutGlobalScopes()->count());
    }

    private function actingAsStore(int $storeId): void
    {
        $this->app->bind(TenantResolver::class, fn (): TenantResolver => new class($storeId) implements TenantResolver
        {
            public function __construct(private readonly int $storeId) {}

            public function currentStoreId(): ?int
            {
                return $this->storeId;
            }
        });
    }

    private function shipmentAttributes(int $storeId, string $reference, string $key): array
    {
        $account = \App\Domains\Shipping\Models\StoreCarrierAccount::query()
            ->withoutGlobalScopes()->where('store_id', $storeId)->firstOrFail();

        return [
            'uuid' => (string) \Illuminate\Support\Str::uuid(),
            'reference' => $reference,
            'carrier_id' => $account->carrier_id,
            'store_carrier_account_id' => $account->id,
            'status' => 'created',
            'idempotency_key' => hash('sha256', $key),
        ];
    }
}
