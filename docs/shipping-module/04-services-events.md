# ٠٤ — الخدمات والأحداث والمهام

## ١. الخدمات (Application Services)

كل خدمة مسؤولية واحدة، تُحقن اعتمادياً، وقابلة للاختبار بمعزل عن HTTP.

### ١.١ `CarrierRegistry`
سجل الـ Drivers. يحوّل `store_carrier_accounts` إلى نسخة Driver جاهزة مع بيانات الاعتماد المفكوكة التشفير.
```php
$driver = $registry->for($account);         // CarrierDriver
$registry->register('asyad', AsyadDriver::class);   // من ServiceProvider
$registry->availableFor($store, $destination);      // الشركات المغطّية للوجهة
```

### ١.٢ `RateComparisonService`
- يبني `RateRequest` من الشحنة/الطلب (يحسب الوزن القابل للفوترة والوزن الحجمي).
- يستدعي كل الحسابات النشطة **بالتوازي** (`Http::pool`) بمهلة ٥ ثوانٍ.
- يدمج نتائج الـ API مع نتائج `RateCardEngine` للشركات بلا تسعير حي.
- يحسب `score` لكل عرض:
  ```
  score = (w_price × سعر_معياري) + (w_speed × سرعة_معيارية)
        + (w_reliability × نسبة_النجاح) + (w_delay × (1 − نسبة_التأخير))
  ```
  الأوزان قابلة للضبط في إعدادات المتجر (تاجر يريد الأرخص وآخر يريد الأسرع).
- يحفظ العروض في `rate_quotes` ويُرجعها مرتّبة، مع وسم **"الأنسب"** لا "الأرخص" فقط.
- كاش ١٠ دقائق على بصمة `(destination, weight, service, cod)`.

### ١.٣ `RateCardEngine`
تسعير محلي للشركات بلا API: يحل المنطقة من العنوان ← يطابق القاعدة (الوزن/الخدمة/الأولوية) ← يطبّق الرسوم الإضافية (COD، منطقة نائية، وقود، تأمين، ضريبة) ← يُرجع `RateQuote` بنفس الشكل تماماً كعرض API.

### ١.٤ `CoverageResolver`
يجيب: هل يستطيع هذا الحساب التوصيل إلى (محافظة، ولاية)؟ يقرأ `shipping_zones` ويُستخدم للترشيح قبل التسعير — لا نستدعي API شركة لا تغطي الوجهة أصلاً.

### ١.٥ `ShipmentCreationService` (الخدمة الأهم)
```
1. التحقق (Validation) + حل الوجهة والتغطية
2. حساب idempotency_key ← إن وُجد سجل مطابق: أعد الشحنة القائمة (لا تكرار)
3. معاملة قاعدة بيانات:
     - إنشاء الشحنة بحالة pending_carrier
     - لقطات العناوين + القطع + الأصناف
     - قفل الطلب (lockForUpdate) وربط الشحنة به
4. خارج المعاملة: نداء الشركة (createShipment)
5. نجاح  → tracking_number + label + حالة created + حدث ShipmentCreated
   فشل   → carrier_error + إدراج في طابور إعادة المحاولة + تنبيه المستخدم
6. تسجيل carrier_api_logs في الحالتين
```
> الترتيب مقصود: **الكتابة المحلية قبل النداء الخارجي.** فقدان بوليصة أُنشئت لدى الشركة أسوأ بكثير من صف محلي معلّق.

### ١.٦ `BulkShipmentService`
`Bus::batch` لإنشاء دفعي، مع تقرير نتائج لكل عنصر (نجح/فشل ولماذا)، وبثّ التقدّم للواجهة.

### ١.٧ `LabelService`
جلب/توليد البوليصة، حفظها على قرص خاص، دمج بوالص متعددة في PDF واحد (`setasign/fpdi`)، توليد بوليصة داخلية بباركود Code128 للشركات اليدوية، وروابط تنزيل موقّعة بصلاحية ١٥ دقيقة.

### ١.٨ `TrackingSyncService`
ينتقي الشحنات المستحقة (`next_sync_at <= now`)، يستدعي `track()`، يمرّر الأحداث إلى `ShipmentEventRecorder`، ويحسب `next_sync_at` التالي حسب الجدول التكيّفي.

### ١.٩ `WebhookIngestionService`
`استقبال → حفظ خام فوراً → تحقق توقيع → مطابقة الشحنة → إخراج المعالجة لطابور → إرجاع 200 سريعاً`.
الإرجاع السريع مهم: شركات الشحن تعطّل الـ Webhook إن تأخر ردّك.

### ١.١٠ `StatusNormalizer`
يقرأ `carrier_status_maps` (مع كاش)، ويحوّل رمز الشركة إلى حالة داخلية. الرمز غير المعروف → `exception` + تسجيله في قائمة "رموز غير معيّنة" للعمليات.

### ١.١١ `ShipmentEventRecorder`
البوابة الوحيدة لتغيير حالة الشحنة:
```
احسب hash → موجود؟ تجاهل (idempotent)
           → جديد؟ أدرج الحدث
                   → هل occurred_at أحدث من الحالة الحالية وغير منقوض لحالة نهائية؟
                       نعم → غيّر الحالة + أطلق ShipmentStatusChanged
```

### ١.١٢ `ShipmentNotificationService`
يقرر القنوات من إعدادات المتجر والحالة المُطلِقة، يمنع التكرار عبر القيد الفريد، يبني الرسالة من القالب بمتغيرات (`{{customer_name}}`, `{{tracking_url}}`…)، ويرسل عبر Laravel Notifications بقنوات: `mail`, `sms`, `whatsapp`, `database`.

### ١.١٣ `OrderShippingBridge` (نقطة التكامل الوحيدة مع وحدة الطلبات)
- يستمع لأحداث الطلبات: `OrderPaid`, `OrderConfirmed`, `OrderCancelled`.
- يبني `ShipmentDraft` مسبق التعبئة من الطلب (العميل، العنوان، الأصناف، الأوزان، مبلغ COD).
- يستمع لأحداث الشحن ويحدّث الطلب: `delivered → completed`، `returned → returned`، وحفظ رقم التتبع ورابطه داخل الطلب.
- يطلق `InventoryReleaseRequested` عند التسليم (وحدة المخزون تقرر ما تفعله).

### ١.١٤ `ShippingAnalyticsService`
يخدم لوحة التحكم والتقارير من `carrier_performance_daily`، ويقرأ الجدول الحي فقط لبيانات اليوم الجاري.

### ١.١٥ `CodReconciliationService`
يبني التسوية للفترة، يطابق كشف الشركة (استيراد CSV/Excel) مع شحنات COD، ويُخرج الفروقات صنفاً صنفاً.

### ١.١٦ `CarrierInvoiceAuditService`
يقارن `quoted_cost` بـ `actual_cost` ورسوم الفاتورة، ويُبرز: وزن مُعاد تقديره، رسوم منطقة نائية غير متوقعة، شحنات مفوترة مرتين، شحنات ملغاة مفوترة.

### ١.١٧ `SlaEngine`
يحسب `promised_delivery_at` عند الإنشاء (من `eta_max_days` + تقويم أيام العمل + وقت القطع اليومي)، ويعلّم المتأخر والصامت.

### ١.١٨ `AutomationRuleEngine`
يطبّق `shipping_automation_rules` لاختيار الشركة تلقائياً حسب الشروط، مع بديل التوصية الذكية إن لم تُطابق قاعدة.

### ١.١٩ `CarrierHealthCheckService`
اختبار الاتصال اليدوي + فحص دوري كل ٦ ساعات لكل حساب نشط، وتحديث `connection_status`، وتنبيه عند التحول إلى `failed`.

### ١.٢٠ `PublicTrackingService`
يخدم صفحة التتبع العامة: يُرجع السجل الزمني منقّحاً (بلا تكلفة أو بيانات داخلية) عبر `uuid` أو رقم تتبع + آخر ٤ أرقام من الهاتف.

---

## ٢. الأحداث والمستمعون

| الحدث | المستمعون |
|---|---|
| `ShipmentCreated` | حفظ التتبع في الطلب · إشعار العميل · سجل النشاط · جدولة أول مزامنة |
| `ShipmentStatusChanged` | جسر تحديث الطلب · الإشعارات · التحليلات التزايدية · سجل النشاط |
| `ShipmentDelivered` | إكمال الطلب · طلب تحرير المخزون · تسجيل التكلفة محاسبياً · إغلاق SLA · طلب تقييم من العميل |
| `ShipmentDelayed` | تنبيه داخلي · مهمة متابعة لخدمة العملاء · إشعار اعتذار اختياري للعميل |
| `ShipmentFailedAttempt` | سير عمل إعادة الجدولة · تنبيه خدمة العملاء |
| `ShipmentReturned` | تحديث الطلب · فتح مرتجع · تنبيه المخزون |
| `ShipmentCancelled` | تحرير الطلب · إلغاء لدى الشركة · سجل النشاط |
| `CarrierConnectionFailed` | تنبيه المدير · فتح قاطع الدائرة · استبعاد الشركة من المقارنة مؤقتاً |
| `LabelGenerated` | سجل النشاط · تحديث عدّاد الطباعة |

**قاعدة:** كل مستمع في طابور (`ShouldQueue`) عدا المستمعين الذين يجب أن يكونوا داخل المعاملة. لا مستمع يوقف مستمعاً آخر عند فشله.

---

## ٣. المهام (Jobs)

| المهمة | الطابور | إعادة المحاولة |
|---|---|---|
| `CreateCarrierShipmentJob` | `shipping-critical` | ٥ محاولات، تراجع أُسّي ٣٠ث→١٦د |
| `ProcessCarrierWebhookJob` | `shipping-webhooks` | ٣ محاولات |
| `SyncShipmentTrackingJob` | `shipping-sync` | ٣ محاولات |
| `GenerateLabelJob` | `shipping-labels` | ٣ |
| `MergeLabelsPdfJob` | `shipping-labels` | ٢ |
| `SendShipmentNotificationJob` | `notifications` | ٣ |
| `BulkCreateShipmentsBatch` | `shipping-bulk` | لكل عنصر ٢ |
| `RollupCarrierPerformanceJob` | `analytics` | ٢ |
| `DetectDelayedShipmentsJob` | `shipping-sync` | ١ |
| `PruneApiLogsJob` | `maintenance` | ١ |
| `CarrierHealthCheckJob` | `shipping-sync` | ١ |

**خنق لكل شركة:** `RateLimited::for('carrier:'.$account->id)` بحدود من إعدادات الـ Driver.

---

## ٤. الجدولة (Scheduler)

```php
$schedule->job(SyncShipmentTrackingJob::class)->everyFifteenMinutes()->withoutOverlapping();
$schedule->job(DetectDelayedShipmentsJob::class)->hourly();
$schedule->job(CarrierHealthCheckJob::class)->everySixHours();
$schedule->job(RollupCarrierPerformanceJob::class)->dailyAt('00:30');
$schedule->job(RetryFailedCarrierShipmentsJob::class)->everyTenMinutes();
$schedule->job(ReconcileWebhookGapsJob::class)->dailyAt('03:00');  // تسوية: هل فاتنا حدث؟
$schedule->job(PruneApiLogsJob::class)->weekly();
$schedule->job(ExpireStaleRateQuotesJob::class)->hourly();
```

---

## ٥. سياسة الأخطاء

| النوع | السلوك |
|---|---|
| خطأ تحقق (عنوان ناقص، وزن صفر) | يُعرض فوراً في النموذج، لا يصل لطابور |
| خطأ شركة قابل للإعادة (5xx، مهلة) | إعادة محاولة أُسّية، الحالة `pending_carrier` |
| خطأ شركة غير قابل للإعادة (بيانات اعتماد خاطئة، وجهة غير مدعومة) | `carrier_error` فوراً + رسالة عربية مفهومة + اقتراح شركة بديلة |
| خطأ توقيع Webhook | يُحفظ الخام بعلم `signature_valid=false`، لا يُعالَج، وينبّه الأمن |
| فشل إشعار | لا يؤثر على الشحنة إطلاقاً؛ يُسجَّل في `shipment_notifications` بحالة `failed` قابلة لإعادة الإرسال |

**مبدأ:** فشل نظام خارجي لا يمنع التاجر من العمل. كل عملية فاشلة لها مسار يدوي بديل معروض في الواجهة.
