# ٠٢ — البنية المعمارية

## ١. المبدأ الحاكم

> **النواة لا تعرف شيئاً عن أي شركة شحن.**

كل ما تعرفه النواة هو عقد واحد (`CarrierDriver`) وآلة حالات داخلية واحدة. إضافة "أسياد إكسبريس" أو "أرامكس" أو مندوب محلي بلا API = تنفيذ نفس العقد. لا شرط `if ($carrier == 'aramex')` في أي مكان خارج مجلد الـ Drivers.

---

## ٢. نمط الوحدة: Modular Monolith

```
متجرلينك (Laravel Application)
├── app/Domains/Orders
├── app/Domains/Catalog
├── app/Domains/Customers
└── app/Domains/Shipping   ◄── وحدة الشحن (معزولة، لا تُستدعى إلا عبر واجهاتها العامة)
```

**لماذا لا Microservice؟** إنشاء الشحنة يجب أن يحدّث الطلب ويحجز رقم التتبع في **معاملة واحدة**. فصل الخدمة يحوّل هذا إلى معاملة موزّعة (Saga) بلا مبرر في هذه المرحلة. الوحدة مصمّمة بحدود نظيفة تسمح بفصلها لاحقاً دون إعادة كتابة:

- لا وصول مباشر لجداول الوحدات الأخرى — التواصل عبر أحداث ونقاط تكامل معلنة (`OrderShippingBridge`).
- لا استدعاء مباشر لموديلات الشحن من خارج الوحدة — عبر `ShippingFacade` فقط.
- كل الأحداث الصادرة موثّقة كعقد عام.

---

## ٣. الطبقات

```
┌─────────────────────────────────────────────────────────────┐
│  Presentation                                               │
│  Blade + Livewire 3 + Alpine · Controllers · API Resources  │
│  (نفس Design System للمنصة — لا مكتبة UI منفصلة)             │
├─────────────────────────────────────────────────────────────┤
│  Application                                                │
│  Services · Actions · DTOs · Form Requests · Policies       │
│  (كل حالة استخدام = Action واحد قابل للاختبار وحده)          │
├─────────────────────────────────────────────────────────────┤
│  Domain                                                     │
│  Models · Enums · State Machine · Events · Value Objects    │
│  Rate Card Engine · Coverage Resolver · SLA Engine          │
│  (لا يعرف HTTP ولا شركات الشحن)                              │
├─────────────────────────────────────────────────────────────┤
│  Integration                                                │
│  CarrierRegistry · CarrierDriver Contract · Drivers/*       │
│  StatusNormalizer · WebhookVerifiers · CircuitBreaker       │
├─────────────────────────────────────────────────────────────┤
│  Infrastructure                                             │
│  Repositories · Queues/Jobs · Scheduler · Storage · Cache   │
│  Notification Channels (Mail/SMS/WhatsApp/Database)         │
└─────────────────────────────────────────────────────────────┘
```

قاعدة الاعتماد: الطبقات العليا تعتمد على السفلى فقط. طبقة Domain لا تستورد شيئاً من Integration — التواصل عبر واجهات (Interfaces) تُحقن.

---

## ٤. عقد شركة الشحن (Carrier Driver Contract)

```php
namespace App\Domains\Shipping\Integration\Contracts;

interface CarrierDriver
{
    /** قدرات الشركة — تُشتق منها الواجهة: زر يظهر أو يختفي حسبها */
    public function capabilities(): CarrierCapabilities;

    /** مخطط بيانات الاعتماد لبناء نموذج الربط ديناميكياً */
    public static function credentialSchema(): array;

    /** اختبار الاتصال — يُستدعى من زر "اختبار الاتصال" */
    public function testConnection(): ConnectionResult;

    /** تسعير: يُرجع عروضاً متعددة (خدمة عادية/سريعة/مبرّدة…) */
    public function getRates(RateRequest $request): RateQuoteCollection;

    /** إنشاء شحنة — يجب أن يكون Idempotent عبر $request->idempotencyKey */
    public function createShipment(ShipmentRequest $request): CarrierShipmentResult;

    /** جلب البوليصة (PDF/ZPL) — قد تكون مضمّنة في نتيجة الإنشاء */
    public function fetchLabel(string $carrierShipmentId, LabelFormat $format): LabelFile;

    /** تتبّع — للـ Polling */
    public function track(string $trackingNumber): TrackingEventCollection;

    public function cancelShipment(string $carrierShipmentId): CancellationResult;

    public function schedulePickup(PickupRequest $request): PickupResult;

    /** التحقق من توقيع الـ Webhook قبل أي معالجة */
    public function verifyWebhook(WebhookPayload $payload): bool;

    /** تحويل حمولة الـ Webhook إلى أحداث تتبع موحّدة */
    public function parseWebhook(WebhookPayload $payload): TrackingEventCollection;

    /** خريطة حالات الشركة → الحالات الداخلية */
    public function statusMap(): array;
}
```

### قدرات الشركة (Capabilities)

```php
final class CarrierCapabilities
{
    public bool $supportsRating;        // تسعير حي عبر API
    public bool $supportsLabel;         // إصدار بوليصة
    public bool $supportsTracking;      // تتبع عبر API
    public bool $supportsWebhook;       // دفع الأحداث
    public bool $supportsCancellation;
    public bool $supportsPickup;
    public bool $supportsCod;
    public bool $supportsReturns;
    public bool $supportsMultiPiece;
    public bool $supportsInsurance;
    public float $volumetricDivisor;    // معامل الوزن الحجمي (5000 غالباً)
    public array $labelFormats;         // ['pdf_a4','pdf_10x15','zpl']
    public string $coverageScope;       // domestic | gcc | international
}
```

**الواجهة تُبنى من القدرات**: إن كانت `supportsPickup = false` لا يظهر زر جدولة الاستلام أصلاً — لا رسالة خطأ بعد الضغط. هذا فارق تجربة كبير.

### الأنواع الثلاثة من الـ Drivers

| النوع | مثال | التسعير | البوليصة | التتبع |
|---|---|---|---|---|
| **API كامل** | أرامكس، DHL، SMSA، iMile | حيّ من الـ API | من الشركة | Webhook + Polling |
| **API جزئي** | شركات محلية بتتبع فقط | من `RateCardEngine` محلياً | قالب داخلي | Polling |
| **يدوي (بلا API)** | مندوب/شركة صغيرة | `RateCardEngine` بالكامل | قالب داخلي بباركود | تحديث يدوي أو استيراد CSV |

`ManualDriver` ليس حالة استثنائية بل Driver كامل يحقق نفس العقد — لذلك يظهر في المقارنة والتقارير ولوحة التحكم مثل غيره تماماً.

---

## ٥. آلة حالات الشحنة (State Machine)

### الحالات الداخلية الموحّدة

```
draft ──► pending_carrier ──► created ──► picked_up ──► in_transit ──► out_for_delivery ──► delivered ✔
                  │              │            │              │                  │
                  │              │            │              │                  ├──► failed_attempt ──┐
                  │              │            │              │                  │                     │
                  ▼              ▼            ▼              ▼                  ▼                     │
              carrier_error  cancelled ✖  cancelled ✖    exception  ◄───────────────────────────────┘
                                                             │
                                                             ├──► returning ──► returned ✖
                                                             └──► lost / damaged ✖
```

| الحالة | العربية | نهائية؟ | ملاحظة |
|---|---|---|---|
| `draft` | مسودة | لا | أُنشئت محلياً ولم تُرسل للشركة |
| `pending_carrier` | بانتظار شركة الشحن | لا | نداء الـ API قيد التنفيذ/إعادة المحاولة |
| `carrier_error` | فشل الإرسال للشركة | لا | يحتاج تدخلاً — يظهر في قائمة "تحتاج انتباهك" |
| `created` | تم الإنشاء | لا | بوليصة ورقم تتبع جاهزان |
| `picked_up` | تم الاستلام | لا | الشركة استلمت الطرد |
| `in_transit` | أثناء النقل | لا | يشمل مراكز الفرز |
| `out_for_delivery` | خرجت للتسليم | لا | |
| `delivered` | تم التسليم | **نعم** | يطلق تحديث الطلب والمخزون |
| `failed_attempt` | فشل التسليم | لا | العدّاد `delivery_attempts` يزيد |
| `exception` | استثناء | لا | عنوان خاطئ، عميل غير متجاوب… |
| `returning` | في طريق الإرجاع | لا | |
| `returned` | تم الإرجاع | **نعم** | |
| `cancelled` | ملغاة | **نعم** | |
| `lost` / `damaged` | مفقودة / تالفة | **نعم** | تفتح مطالبة تلقائياً |

### علامات مشتقة (لا حالات)
- `is_delayed` — الآن > `promised_delivery_at` والحالة غير نهائية.
- `is_stale` — لا حدث تتبع منذ ٧٢ ساعة والحالة غير نهائية.

فصلها عن الحالة مقصود: شحنة قد تكون `in_transit` **و** متأخرة **و** صامتة في آن واحد.

### قواعد الانتقال
1. **الانتقالات النهائية لا تُنقض** — حدث متأخر من الشركة يصل بعد `delivered` يُسجَّل في السجل الزمني ولا يغيّر الحالة.
2. **الترتيب الزمني لا رقم الوصول** — الحالة تُحسب من الحدث الأحدث حسب `occurred_at`، فأحداث الـ Webhook قد تصل خارج ترتيبها.
3. **كل انتقال يُسجَّل** في `shipment_events` مع مصدره (`webhook`/`polling`/`manual`/`system`) ومن قام به.
4. **لا انتقال بلا حدث** — الحالة انعكاس للسجل الزمني، وليست حقلاً يُكتب مباشرة.

---

## ٦. تدفق تحديث الحالة

```
        شركة الشحن
       ╱          ╲
  Webhook       Polling (احتياطي/للشركات بلا Webhook)
     │              │
     ▼              ▼
[التحقق من التوقيع]  [SyncShipmentTrackingJob]
     │              │
     ▼              │
carrier_webhook_events (حفظ خام + event_uid فريد للحماية من التكرار)
     │              │
     ▼              ▼
        StatusNormalizer  (حالة الشركة → حالة داخلية)
                  │
                  ▼
        ShipmentEventRecorder  (منع التكرار عبر hash)
                  │
        ┌─────────┴──────────┐
        ▼                    ▼
   تحديث الحالة        ShipmentStatusChanged (Event)
                             │
        ┌────────────┬───────┴────────┬──────────────┐
        ▼            ▼                ▼              ▼
  تحديث الطلب   إشعار العميل   سجل النشاط    تحديث التحليلات
```

### استراتيجية الـ Polling التكيّفية
استدعاء كل الشحنات كل ٥ دقائق يستنزف حدود الـ API. الجدولة حسب حالة الشحنة:

| الحالة | التكرار |
|---|---|
| `out_for_delivery` | كل ٣٠ دقيقة |
| `in_transit` / `picked_up` | كل ٣ ساعات |
| `created` (لم تُستلم بعد) | كل ٦ ساعات |
| `exception` / `failed_attempt` | كل ساعة |
| نهائية | لا استدعاء |

وإذا كانت الشركة تدعم Webhook مؤكداً، يهبط الـ Polling إلى **مرة يومية كتسوية** فقط للتحقق من عدم فقدان حدث.

---

## ٧. الموثوقية أمام أنظمة خارجية

| الخطر | المعالجة |
|---|---|
| بطء الـ API يجمّد الواجهة | كل نداء بمهلة صارمة؛ التسعير متوازٍ (`Http::pool`)؛ الشركة التي تتأخر تظهر "غير متاحة الآن" ولا توقف عرض البقية |
| تعطّل مستمر لشركة | **Circuit Breaker** لكل حساب: ٥ إخفاقات متتالية ← فتح الدائرة ٥ دقائق ← نصف مفتوحة للاختبار |
| إنشاء شحنة مكرر | `idempotency_key = hash(order_id + account_id + payload)` + قفل صف الطلب + فحص السجل قبل النداء |
| حدث Webhook مكرر | `event_uid` فريد + `hash` فريد على `shipment_events` |
| Webhook مزوّر | تحقق توقيع HMAC/توقيع الشركة + قائمة IP بيضاء + نافذة زمنية ضد إعادة الإرسال |
| فشل بعد إنشاء الشحنة لدى الشركة (نجحت لديهم وفشل الحفظ لدينا) | تُكتب الشحنة محلياً **قبل** النداء بحالة `pending_carrier`، ونتيجة النداء تُحدّثها — لا تُفقد بوليصة أبداً |
| تجاوز حدود المعدل | طابور مخصّص لكل شركة مع خانق (Throttle) قابل للضبط لكل Driver |

---

## ٨. الأداء

| المسار | الهدف | الوسيلة |
|---|---|---|
| لوحة التحكم | < ٤٠٠ مللي ثانية | قراءة من `carrier_performance_daily` المجمّعة مسبقاً + كاش ٥ دقائق، لا `COUNT(*)` على جدول الشحنات |
| جدول الشحنات (١٠٠ ألف صف) | < ٣٠٠ مللي | فهارس مركّبة + ترقيم بالمؤشر (Cursor) + `select` للأعمدة المطلوبة فقط |
| مقارنة الأسعار | < ٢ ثانية لـ ٦ شركات | استدعاء متوازٍ + كاش عروض ١٠ دقائق لنفس بصمة الشحنة |
| إنشاء دفعي لـ ١٠٠ شحنة | خلفي مع شريط تقدّم | Job Batch + بث التقدّم |
| دمج ١٠٠ بوليصة PDF | خلفي | Job + رابط تنزيل موقّع عند الاكتمال |

الحقول المشتقة (`is_delayed`, `total_cost`) **مُخزّنة ومحدّثة بالأحداث**، لا محسوبة في كل استعلام.
