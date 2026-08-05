<?php

declare(strict_types=1);

namespace Database\Seeders;

use App\Domains\Shipping\Models\ShippingCarrier;
use App\Domains\Shipping\Models\ShippingRateCard;
use App\Domains\Shipping\Models\ShippingZone;
use App\Domains\Shipping\Models\StoreCarrierAccount;
use App\Domains\Shipping\Support\OmanGeo;
use Illuminate\Database\Seeder;

/**
 * إعداد متجر جاهز للعمل خلال ثوانٍ: حساب توصيل يدوي + منطقتان
 * (مسقط والمحافظات) + بطاقة أسعار — فيصبح التسعير والإنشاء والطباعة
 * كلها عاملة قبل ربط أي شركة.
 */
final class ShippingDemoSeeder extends Seeder
{
    public function run(int $storeId = 1): void
    {
        $carrier = ShippingCarrier::query()->where('code', 'manual')->firstOrFail();

        $account = StoreCarrierAccount::query()->updateOrCreate(
            ['store_id' => $storeId, 'carrier_id' => $carrier->id, 'label' => 'مندوب المتجر'],
            [
                'environment' => 'live',
                'is_active' => true,
                'is_default' => true,
                'connection_status' => 'connected',
                'default_service_code' => 'STD',
                'cod_enabled' => true,
                'cod_fee_fixed' => 0.300,
            ],
        );

        $muscat = $this->zone($storeId, 'مسقط الكبرى', ['مسقط']);
        $others = $this->zone($storeId, 'بقية المحافظات', array_values(array_diff(OmanGeo::governorates(), ['مسقط'])));

        $card = ShippingRateCard::query()->updateOrCreate(
            ['store_id' => $storeId, 'store_carrier_account_id' => $account->id, 'name' => 'تسعيرة المندوب'],
            ['currency' => 'OMR', 'is_active' => true],
        );

        $rules = [
            [$muscat->id, 'STD', 'توصيل داخل مسقط', 0, 5, 1.000, 0.250, 0, 1],
            [$muscat->id, 'EXP', 'توصيل سريع (نفس اليوم)', 0, 5, 1.800, 0.250, 0, 1],
            [$others->id, 'STD', 'توصيل للمحافظات', 0, 10, 2.500, 0.350, 0.900, 3],
        ];

        foreach ($rules as [$zoneId, $code, $name, $min, $max, $base, $extra, $remote, $eta]) {
            $card->rules()->updateOrCreate(
                ['zone_id' => $zoneId, 'service_code' => $code],
                [
                    'service_name' => $name,
                    'min_weight_kg' => $min,
                    'max_weight_kg' => $max,
                    'base_price' => $base,
                    'price_per_extra_kg' => $extra,
                    'remote_area_surcharge' => $remote,
                    'cod_fee_fixed' => 0.300,
                    'vat_percent' => 5,
                    'eta_min_days' => max(0, $eta - 1),
                    'eta_max_days' => $eta,
                    'priority' => 10,
                ],
            );
        }
    }

    /** @param list<string> $governorates */
    private function zone(int $storeId, string $name, array $governorates): ShippingZone
    {
        $zone = ShippingZone::query()->updateOrCreate(
            ['store_id' => $storeId, 'name' => $name],
            ['is_active' => true],
        );

        foreach ($governorates as $governorate) {
            $zone->regions()->updateOrCreate(
                ['governorate' => $governorate, 'wilayat' => null],
                ['country_code' => 'OM', 'is_remote' => OmanGeo::isRemote($governorate)],
            );
        }

        return $zone;
    }
}
