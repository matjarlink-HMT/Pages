<?php

declare(strict_types=1);

namespace Tests\Feature\Shipping;

use App\Domains\Shipping\DTOs\AddressData;
use App\Domains\Shipping\DTOs\PackageData;
use App\Domains\Shipping\DTOs\ShipmentRequest;
use App\Domains\Shipping\Enums\ShipmentStatus;
use App\Domains\Shipping\Models\Shipment;
use App\Domains\Shipping\Services\ShipmentCreationService;
use Database\Seeders\ShippingCarrierSeeder;
use Database\Seeders\ShippingDemoSeeder;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

final class CreateShipmentTest extends TestCase
{
    use RefreshDatabase;

    private const STORE_ID = 1;

    protected function setUp(): void
    {
        parent::setUp();

        $this->seed(ShippingCarrierSeeder::class);
        (new ShippingDemoSeeder())->run(self::STORE_ID);
    }

    public function test_creates_shipment_with_tracking_and_timeline(): void
    {
        $shipment = app(ShipmentCreationService::class)->create(self::STORE_ID, $this->request());

        self::assertSame(ShipmentStatus::Created, $shipment->status);
        self::assertNotNull($shipment->tracking_number);
        self::assertNotNull($shipment->promised_delivery_at);
        self::assertGreaterThan(0, (float) $shipment->total_cost);

        /* الحالة انعكاس للسجل الزمني: لا شحنة بلا حدث. */
        self::assertDatabaseHas('shipment_events', [
            'shipment_id' => $shipment->id,
            'status' => ShipmentStatus::Created->value,
        ]);
    }

    /** ضغطة زر مزدوجة أو انقطاع شبكة يجب ألا ينتجا بوليصتين ورسمين. */
    public function test_duplicate_request_returns_the_same_shipment(): void
    {
        $service = app(ShipmentCreationService::class);

        $first = $service->create(self::STORE_ID, $this->request());
        $second = $service->create(self::STORE_ID, $this->request());

        self::assertSame($first->id, $second->id);
        self::assertSame(1, Shipment::query()->withoutGlobalScopes()->count());
    }

    public function test_billable_weight_uses_volumetric_when_box_is_large(): void
    {
        $shipment = app(ShipmentCreationService::class)->create(self::STORE_ID, $this->request(
            packages: [new PackageData(weightKg: 2.0, lengthCm: 40, widthCm: 30, heightCm: 25)],
        ));

        self::assertSame('6.000', (string) $shipment->billable_weight_kg);
    }

    /** @param list<PackageData>|null $packages */
    private function request(?array $packages = null): ShipmentRequest
    {
        return new ShipmentRequest(
            accountId: (int) \App\Domains\Shipping\Models\StoreCarrierAccount::query()
                ->withoutGlobalScopes()->value('id'),
            sender: new AddressData('متجرلينك', '+96824000000', 'مسقط', 'بوشر'),
            receiver: new AddressData('سالم بن ناصر', '+96899123456', 'مسقط', 'السيب'),
            packages: $packages ?? [new PackageData(weightKg: 2.5)],
            orderId: 1001,
            serviceCode: 'STD',
            declaredValue: 25.0,
            isCod: true,
            codAmount: 25.0,
        );
    }
}
