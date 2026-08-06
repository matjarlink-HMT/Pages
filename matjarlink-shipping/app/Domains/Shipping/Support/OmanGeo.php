<?php

declare(strict_types=1);

namespace App\Domains\Shipping\Support;

/**
 * الشجرة الجغرافية العُمانية: ١١ محافظة و٦١ ولاية.
 * العناوين العُمانية بلا ترميز بريدي فعّال، فالاعتماد على
 * (المحافظة ← الولاية ← المنطقة + معلم بارز + إحداثيات).
 */
final class OmanGeo
{
    public const COUNTRY_CODE = 'OM';

    /** المحافظات التي تُحتسب نائية: رسوم إضافية وأزمنة أطول. */
    public const REMOTE = ['الوسطى', 'مسندم', 'الظاهرة'];

    /** @return array<string, list<string>> */
    public static function tree(): array
    {
        return [
            'مسقط'         => ['مسقط', 'مطرح', 'بوشر', 'السيب', 'العامرات', 'قريات'],
            'ظفار'         => ['صلالة', 'طاقة', 'مرباط', 'سدح', 'رخيوت', 'ضلكوت', 'ثمريت', 'مقشن', 'شليم وجزر الحلانيات', 'المزيونة'],
            'شمال الباطنة' => ['صحار', 'شناص', 'لوى', 'صحم', 'الخابورة', 'السويق'],
            'جنوب الباطنة' => ['الرستاق', 'العوابي', 'نخل', 'وادي المعاول', 'بركاء', 'المصنعة'],
            'الداخلية'     => ['نزوى', 'بهلاء', 'منح', 'الحمراء', 'أدم', 'إزكي', 'سمائل', 'بدبد'],
            'شمال الشرقية' => ['إبراء', 'المضيبي', 'بدية', 'القابل', 'وادي بني خالد', 'دماء والطائيين'],
            'جنوب الشرقية' => ['صور', 'الكامل والوافي', 'جعلان بني بوعلي', 'جعلان بني بوحسن', 'مصيرة'],
            'البريمي'      => ['البريمي', 'محضة', 'السنينة'],
            'الظاهرة'      => ['عبري', 'ينقل', 'ضنك'],
            'الوسطى'       => ['هيماء', 'محوت', 'الدقم', 'الجازر'],
            'مسندم'        => ['خصب', 'بخا', 'دبا', 'مدحاء'],
        ];
    }

    /** @return list<string> */
    public static function governorates(): array
    {
        return array_keys(self::tree());
    }

    /** @return list<string> */
    public static function wilayats(string $governorate): array
    {
        return self::tree()[$governorate] ?? [];
    }

    public static function isRemote(?string $governorate): bool
    {
        return in_array((string) $governorate, self::REMOTE, true);
    }

    public static function exists(?string $governorate, ?string $wilayat): bool
    {
        return $governorate !== null
            && $wilayat !== null
            && in_array($wilayat, self::wilayats($governorate), true);
    }
}
