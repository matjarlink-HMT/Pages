<?php

declare(strict_types=1);

return [

    'module' => 'إدارة الشحن',
    'dashboard' => 'لوحة التحكم',
    'shipments' => 'الشحنات',
    'create_shipment' => 'إنشاء شحنة',
    'carriers' => 'شركات الشحن',
    'reports' => 'التقارير',

    'status' => [
        'draft' => 'مسودة',
        'pending_carrier' => 'بانتظار شركة الشحن',
        'carrier_error' => 'فشل الإرسال للشركة',
        'created' => 'تم الإنشاء',
        'picked_up' => 'تم الاستلام',
        'in_transit' => 'أثناء النقل',
        'out_for_delivery' => 'خرجت للتسليم',
        'delivered' => 'تم التسليم',
        'failed_attempt' => 'فشل التسليم',
        'exception' => 'استثناء',
        'returning' => 'في طريق الإرجاع',
        'returned' => 'تم الإرجاع',
        'cancelled' => 'ملغاة',
        'lost' => 'مفقودة',
        'damaged' => 'تالفة',
    ],

    'source' => [
        'webhook' => 'تحديث تلقائي',
        'polling' => 'مزامنة',
        'manual' => 'تسجيل يدوي',
        'system' => 'النظام',
        'import' => 'استيراد',
    ],

    'payment' => [
        'prepaid' => 'مدفوع مسبقاً',
        'cod' => 'الدفع عند الاستلام',
        'carrier_account' => 'على حساب الشركة',
    ],

    'connection' => [
        'unknown' => 'غير مربوط',
        'connected' => 'متصل',
        'failed' => 'فشل الاتصال',
    ],

    'features' => [
        'tracking' => 'تتبع مباشر',
        'cod' => 'الدفع عند الاستلام',
        'insurance' => 'تأمين',
        'pickup' => 'استلام من الموقع',
    ],

    'rates' => [
        'same_day' => 'نفس اليوم',
        'days' => '{1} يوم عمل|{2} يومان|[3,10] :count أيام عمل|[11,*] :count يوم عمل',
        'days_range' => ':min–:max يوم عمل',
        'recommended' => 'الأنسب',
        'cheapest' => 'الأرخص',
        'unavailable_title' => 'غير متاحة لهذه الشحنة',
    ],

    /* الشركة غير المتاحة تُعرض مع سببها — المستخدم يحتاج أن يعرف السبب. */
    'unavailable' => [
        'not_covered' => 'لا تغطي :area',
        'connection_failed' => 'تعذّر الاتصال بالشركة الآن',
        'no_rate' => 'لا يوجد سعر لهذه الشحنة',
        'account_inactive' => 'الحساب غير مفعّل',
    ],

    'events' => [
        'created' => 'تم إنشاء الشحنة وإصدار بوليصة الشحن',
        'cancelled' => 'أُلغيت الشحنة',
        'carrier_error' => 'تعذّر إرسال الشحنة إلى نظام الشركة — :reason',
    ],

    'errors' => [
        'shipping_carrier_error' => 'حدث خطأ لدى شركة الشحن. حاول مرة أخرى أو اختر شركة بديلة.',
        'shipping_carrier_unavailable' => 'شركة الشحن غير متاحة حالياً. يمكنك المتابعة بشركة أخرى.',
        'shipping_destination_not_covered' => 'شركة الشحن المختارة لا تغطي هذه الوجهة.',
        'shipping_invalid_credentials' => 'بيانات الاعتماد مرفوضة — راجع إعدادات الحساب.',
        'shipping_duplicate_request' => 'هذه الشحنة أُنشئت مسبقاً.',
        'no_rate_for_destination' => 'لا توجد تسعيرة تغطي هذه الوجهة. أضف منطقة وسعراً في إعدادات التسعير.',
        'cancellation_unsupported' => 'شركة الشحن لا تدعم الإلغاء عبر النظام — تواصل معها مباشرة.',
        'already_terminal' => 'الشحنة وصلت حالة نهائية ولا يمكن إلغاؤها.',
    ],

    'validation' => [
        'unknown_wilayat' => 'الولاية المختارة لا تتبع هذه المحافظة.',
    ],

    'manual' => [
        'ready' => 'التوصيل اليدوي جاهز — التسعيرة مفعّلة.',
        'no_rate_card' => 'لا توجد بطاقة أسعار مفعّلة لهذا الحساب.',
    ],

    'flash' => [
        'created' => 'تم إنشاء الشحنة :reference وإصدار بوليصتها.',
        'cancelled' => 'أُلغيت الشحنة.',
        'sync_queued' => 'طُلب تحديث الحالة من شركة الشحن.',
        'event_recorded' => 'سُجّل الحدث في السجل الزمني.',
        'export_queued' => 'يجري تجهيز ملف التصدير وسيصلك إشعار عند اكتماله.',
        'carrier_connected' => 'تم ربط شركة الشحن وتفعيلها بعد نجاح الاختبار.',
        'carrier_failed' => 'حُفظ الحساب لكن الاتصال فشل: :reason',
        'carrier_updated' => 'حُدّثت بيانات الحساب.',
        'carrier_removed' => 'حُذف الحساب.',
        'connection_ok' => 'الاتصال ناجح.',
        'connection_failed' => 'فشل الاتصال: :reason',
        'default_set' => 'حُدّدت الشركة الافتراضية.',
    ],

    'attention' => [
        'delayed' => 'شحنات متأخرة',
        'stale' => 'بلا تحديث منذ ٧٢ ساعة',
        'failed_attempt' => 'فشل تسليم',
        'carrier_error' => 'فشل إرسال للشركة',
    ],

    'ui' => [
        'attention' => 'تحتاج انتباهك',
        'delayed' => 'متأخرة',
        'stale' => 'بلا تحديث',
        'total_shipments' => 'إجمالي الشحنات',
        'total_cost' => 'إجمالي تكلفة الشحن',
        'avg_cost' => 'متوسط تكلفة الشحنة',
        'avg_delivery' => 'متوسط مدة التوصيل',
        'on_time_rate' => 'التسليم في الموعد',
        'cod_pending' => 'تحصيل معلّق',
        'invoice_variance' => 'فروقات الفواتير',
        'top_wilayats' => 'أكثر الولايات شحناً',
        'billable_weight' => 'الوزن المحتسب للفوترة',
        'volumetric_hint' => 'الشركات تسعّر بالأكبر من الوزن الفعلي والحجمي.',
        'timeline' => 'السجل الزمني',
        'no_shipments' => 'لا توجد شحنات بعد.',
        'no_results' => 'لا نتائج مطابقة.',
        'clear_filters' => 'مسح الفلاتر',
        'load_more' => 'تحميل المزيد',
    ],
];
