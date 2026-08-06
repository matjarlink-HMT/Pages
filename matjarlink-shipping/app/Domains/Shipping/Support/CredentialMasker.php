<?php

declare(strict_types=1);

namespace App\Domains\Shipping\Support;

/**
 * لا تخرج قيمة سرّية إلى واجهة ولا سجل ولا تقرير خطأ.
 * تُستدعى في: عرض الحسابات، تسجيل نداءات الشركات، وتقارير الاستثناءات.
 */
final class CredentialMasker
{
    public static function mask(?string $value, int $visible = 4): string
    {
        $value = (string) $value;

        if ($value === '') {
            return '—';
        }

        return strlen($value) <= $visible
            ? str_repeat('•', strlen($value))
            : str_repeat('•', 6).substr($value, -$visible);
    }

    /** تنقية عميقة لأي حمولة قبل تسجيلها. */
    public static function redact(array $payload): array
    {
        $keys = array_map('strtolower', (array) config('shipping.logs.redact', []));

        foreach ($payload as $key => $value) {
            if (is_array($value)) {
                $payload[$key] = self::redact($value);
                continue;
            }

            if (in_array(strtolower((string) $key), $keys, true)) {
                $payload[$key] = '[REDACTED]';
            }
        }

        return $payload;
    }
}
