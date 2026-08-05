<?php

declare(strict_types=1);

namespace Tests\Unit\Shipping;

use App\Domains\Shipping\Support\PhoneNormalizer;
use PHPUnit\Framework\TestCase;

final class PhoneNormalizerTest extends TestCase
{
    /**
     * صيغة الرقم سبب شائع لرفض شركة الشحن للشحنة — كل هذه الصيغ رقم واحد.
     *
     * @dataProvider omaniNumbers
     */
    public function test_normalizes_omani_numbers(string $input): void
    {
        self::assertSame('+96899123456', PhoneNormalizer::normalize($input));
    }

    public static function omaniNumbers(): array
    {
        return [
            ['99123456'],
            ['+96899123456'],
            ['96899123456'],
            ['+968 9912 3456'],
            ['00968-9912-3456'],
        ];
    }

    public function test_masks_all_but_last_four_digits(): void
    {
        self::assertSame('••••••••3456', PhoneNormalizer::mask('+96899123456'));
    }

    public function test_empty_input_returns_null(): void
    {
        self::assertNull(PhoneNormalizer::normalize(''));
        self::assertNull(PhoneNormalizer::normalize(null));
    }
}
