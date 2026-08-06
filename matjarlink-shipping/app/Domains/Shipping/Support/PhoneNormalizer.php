<?php

declare(strict_types=1);

namespace App\Domains\Shipping\Support;

/**
 * ‎"99123456" و"96899123456" و"+968 9912 3456" كلها رقم واحد.
 * صيغة الرقم سبب شائع جداً لرفض شركة الشحن للشحنة، فيُطبَّع قبل الإرسال.
 */
final class PhoneNormalizer
{
    public const DEFAULT_COUNTRY_CODE = '968';

    public static function normalize(?string $phone, string $countryCode = self::DEFAULT_COUNTRY_CODE): ?string
    {
        if ($phone === null || trim($phone) === '') {
            return null;
        }

        $digits = preg_replace('/\D+/', '', $phone) ?? '';

        if ($digits === '') {
            return null;
        }

        $digits = ltrim($digits, '0');

        if (! str_starts_with($digits, $countryCode)) {
            $digits = $countryCode.$digits;
        }

        return '+'.$digits;
    }

    /** التقنيع في صفحة التتبع العامة والتصديرات لغير المخوّلين. */
    public static function mask(?string $phone): string
    {
        $phone = (string) $phone;
        $len = strlen($phone);

        return $len <= 4 ? str_repeat('•', $len) : str_repeat('•', $len - 4).substr($phone, -4);
    }
}
