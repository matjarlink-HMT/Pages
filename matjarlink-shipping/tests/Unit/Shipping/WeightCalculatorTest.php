<?php

declare(strict_types=1);

namespace Tests\Unit\Shipping;

use App\Domains\Shipping\DTOs\PackageData;
use App\Domains\Shipping\Support\WeightCalculator;
use PHPUnit\Framework\TestCase;

final class WeightCalculatorTest extends TestCase
{
    public function test_billable_weight_uses_volumetric_when_larger(): void
    {
        /* صندوق كبير خفيف: ٤٠×٣٠×٢٥ ÷ ٥٠٠٠ = ٦ كجم حجمي مقابل ٢ فعلي. */
        $packages = [new PackageData(weightKg: 2.0, lengthCm: 40, widthCm: 30, heightCm: 25)];

        self::assertSame(6.0, WeightCalculator::billable($packages, 5000));
    }

    public function test_billable_weight_uses_actual_when_larger(): void
    {
        $packages = [new PackageData(weightKg: 9.0, lengthCm: 20, widthCm: 20, heightCm: 10)];

        self::assertSame(9.0, WeightCalculator::billable($packages, 5000));
    }

    public function test_missing_dimensions_fall_back_to_actual_weight(): void
    {
        $packages = [new PackageData(weightKg: 3.25)];

        self::assertSame(3.25, WeightCalculator::billable($packages, 5000));
    }

    public function test_quantity_multiplies_both_weights(): void
    {
        $packages = [new PackageData(weightKg: 1.0, lengthCm: 40, widthCm: 30, heightCm: 25, quantity: 3)];

        self::assertSame(3.0, WeightCalculator::actual($packages));
        self::assertSame(18.0, WeightCalculator::volumetric($packages, 5000));
    }
}
