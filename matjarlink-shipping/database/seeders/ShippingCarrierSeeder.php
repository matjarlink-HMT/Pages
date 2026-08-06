<?php

declare(strict_types=1);

namespace Database\Seeders;

use App\Domains\Shipping\Models\ShippingCarrier;
use Illuminate\Database\Seeder;

/**
 * كتالوج الشركات. الشركة الوحيدة العاملة من اليوم الأول هي «التوصيل اليدوي»
 * لأنها لا تحتاج API ولا بيانات اعتماد — وبها يستطيع التاجر تشغيل عملياته
 * كاملة قبل إتمام أي اتفاقية ربط.
 *
 * إضافة شركة ذات API لاحقاً: صف هنا + صنف Driver + تسجيله في config/shipping.php.
 */
final class ShippingCarrierSeeder extends Seeder
{
    public function run(): void
    {
        $carriers = [
            [
                'code' => 'manual',
                'name_ar' => 'توصيل يدوي / مندوب',
                'name_en' => 'Manual delivery',
                'coverage_scope' => 'domestic',
                'sort_order' => 100,
                'capabilities' => [
                    'rating' => true, 'label' => true, 'tracking' => false, 'webhook' => false,
                    'cancellation' => true, 'pickup' => false, 'cod' => true, 'returns' => true,
                    'multi_piece' => true, 'insurance' => false, 'volumetric_divisor' => 5000,
                    'label_formats' => ['pdf_a4', 'pdf_10x15'], 'coverage_scope' => 'domestic',
                ],
            ],
        ];

        foreach ($carriers as $carrier) {
            ShippingCarrier::query()->updateOrCreate(['code' => $carrier['code']], $carrier);
        }
    }
}
