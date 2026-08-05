# وحدة الشحن — تنفيذ Laravel (drop-in module)

تنفيذ فعلي لوحدة إدارة الشحن بمكدس منصة متجرلينك: **PHP 8.2+ · Laravel 11 · MySQL 8 · Blade**.
المرجع التصميمي الكامل في [`docs/shipping-module/`](../docs/shipping-module/README.md).

الشجرة هنا **تطابق مسارات تطبيق Laravel حرفياً**، فالتركيب نسخٌ مباشر بلا إعادة ترتيب.

---

## ما المُنفَّذ في هذه الحزمة

المرحلتان ٠ و١ من [خارطة التنفيذ](../docs/shipping-module/10-roadmap.md) — أي **الحد الأدنى العامل** الذي يشغّل عمليات تاجر كاملة:

| الطبقة | المُنفَّذ |
|---|---|
| قاعدة البيانات | ١٠ هجرات تُنشئ ١٧ جدولاً بالفهارس المركّبة والقيود الفريدة |
| النطاق | `ShipmentStatus` (١٥ حالة) · آلة الحالات · `ShipmentEventRecorder` · `SlaEngine` |
| التكامل | عقد `CarrierDriver` · `CarrierRegistry` · `AbstractCarrierDriver` (مهلات، تسجيل، قاطع دائرة) · `ManualDriver` |
| الخدمات | إنشاء الشحنة · مقارنة الأسعار · محرك التسعير اليدوي · التغطية · تطبيع الحالات · البوالص · التحليلات |
| الحالات | `CreateShipment` · `CancelShipment` · `RecordManualEvent` · `TestCarrierConnection` |
| الواجهة | ٤ متحكّمات · ٣ Form Requests · فلتر معلن · Resources · ١٢ قالب Blade · ورقة أنماط |
| الأمان | ٢٠ صلاحية · ٥ أدوار · `TenantScope` · تشفير المفاتيح · تنقية السجلات |
| الخلفية | ٣ مهام مجدولة (مزامنة تكيّفية، كشف التأخير، تقليم السجلات) |
| الاختبارات | ٥ ملفات: الوزن الحجمي، آلة الحالات، تطبيع الهواتف، إنشاء الشحنة، **عزل المستأجرين** |

**ليس ضمن هذه الحزمة بعد** (المرحلة ٢ فما بعد): متحكّم استقبال Webhooks، Drivers لشركات محددة، الإشعارات (SMS/واتساب)، صفحة التتبع العامة، المرتجعات والمطالبات، وتسوية COD. البنية جاهزة لها جميعاً — العقود والجداول والأحداث موجودة.

---

## التركيب

### ١. نسخ الملفات

```bash
cp -r matjarlink-shipping/app/Domains/Shipping        <app>/app/Domains/
cp    matjarlink-shipping/config/shipping.php         <app>/config/
cp    matjarlink-shipping/routes/shipping.php         <app>/routes/
cp -r matjarlink-shipping/database/migrations/shipping <app>/database/migrations/
cp    matjarlink-shipping/database/seeders/*.php      <app>/database/seeders/
cp -r matjarlink-shipping/resources/views/shipping    <app>/resources/views/
cp    matjarlink-shipping/resources/css/shipping.css  <app>/public/css/
cp    matjarlink-shipping/lang/ar/shipping.php        <app>/lang/ar/
cp    matjarlink-shipping/lang/en/shipping.php        <app>/lang/en/
cp -r matjarlink-shipping/tests/*                     <app>/tests/
```

### ٢. تسجيل المزوّد

```php
// bootstrap/providers.php  (أو config/app.php في المشاريع الأقدم)
App\Domains\Shipping\ShippingServiceProvider::class,
```

هذا كل ما يلزم: المزوّد يحمّل الهجرات والقوالب والترجمات والمسارات والسياسات والأحداث والجدولة.

### ٣. ربط عقدَي التكامل

الوحدة لا تفترض شيئاً عن جداول المتاجر ولا الطلبات. حقّق العقدين في مزوّد المنصة:

```php
// app/Providers/AppServiceProvider.php
$this->app->bind(TenantResolver::class, MatjarlinkTenantResolver::class);
$this->app->bind(OrderBridge::class, MatjarlinkOrderBridge::class);
```

* **`TenantResolver`** — يُرجع `store_id` الحالي. التحقيق الافتراضي `AuthTenantResolver` يقرأ `auth()->user()->store_id`؛ استبدله إن كان تحديد المتجر لديك مختلفاً (نطاق فرعي، جلسة، رأس طلب…).
* **`OrderBridge`** — ثلاث دوال: `snapshot()` لتعبئة الشحنة من الطلب مسبقاً، `attachShipment()` لحفظ رقم التتبع داخل الطلب، `syncStatus()` لتحديث حالة الطلب من حالة الشحنة. التحقيق الافتراضي `NullOrderBridge` لا يفعل شيئاً، فتعمل الوحدة وتُختبر قبل الربط.

> ما دام `OrderBridge` غير محقَّق، تعمل الوحدة مستقلة تماماً — لكن التكامل مع الطلبات (أهم وعد في الوحدة) لا يبدأ إلا بتحقيقه.

### ٤. الهجرات والبذور

```bash
php artisan migrate
php artisan db:seed --class=ShippingCarrierSeeder      # كتالوج الشركات
php artisan db:seed --class=ShippingPermissionSeeder   # ٢٠ صلاحية + ٥ أدوار
php artisan tinker --execute="(new Database\Seeders\ShippingDemoSeeder)->run(1)"  # متجر جاهز للعمل
```

`ShippingDemoSeeder` ينشئ حساب توصيل يدوي + منطقتين + بطاقة أسعار، فيصبح التسعير والإنشاء والطباعة عاملة فوراً **قبل ربط أي شركة شحن**.

### ٥. القالب الموروث

`resources/views/shipping/layouts/shipping.blade.php` يمتد `layouts.app`. عدّل الاسم ليطابق القالب الرئيسي في متجرلينك — فترث الوحدة الهيدر والتنقل والهوية البصرية كاملة.

### ٦. الأنماط

`shipping.css` **لا يعرّف هوية بصرية جديدة**: كل قيمة مشتقة من متغيّرات نظام تصميم المنصة (`--color-primary`, `--radius-md`, `--shadow-sm` …) مع بدائل احتياطية. عدّل كتلة المتغيّرات في أعلى الملف لتطابق أسماء متغيّراتك، ولا حاجة للمسّ بما بعدها.

### ٧. الطابور والجدولة

```bash
php artisan queue:work --queue=shipping-critical,shipping-sync,shipping-labels,default
```
الجدولة تُسجَّل تلقائياً: مزامنة كل ١٥ دقيقة (للشحنات المستحقة فقط)، كشف التأخير كل ساعة، تقليم السجلات أسبوعياً.

### ٨. اختياري

* `barryvdh/laravel-dompdf` → تتحوّل البوالص إلى PDF تلقائياً. بدونه تُحفظ HTML قابلة للطباعة من المتصفح، فلا تتعطّل الطباعة بانتظار حزمة.
* `spatie/laravel-permission` → بذر الصلاحيات والأدوار (يُتخطّى بأمان إن لم يكن مثبّتاً).
* `spatie/laravel-activitylog` → سجل النشاط (البديل: سجل التطبيق).

---

## إضافة شركة شحن جديدة

هذا هو معيار نجاح المعمارية — **لا تعديل على النواة ولا قاعدة البيانات ولا الواجهات**:

```php
// ١. app/Domains/Shipping/Integration/Drivers/Asyad/AsyadDriver.php
final class AsyadDriver extends AbstractCarrierDriver
{
    public function capabilities(): CarrierCapabilities { /* … */ }
    public static function credentialSchema(): array { /* يبني نموذج الربط ديناميكياً */ }
    public function testConnection(): ConnectionResult { /* … */ }
    public function getRates(RateRequest $r): array { /* … */ }
    public function createShipment(ShipmentRequest $r): CarrierShipmentResult { /* … */ }
    public function track(string $trackingNumber): array { /* … */ }
    public function statusMap(): array { return ['DLV' => 'delivered', 'OFD' => 'out_for_delivery', /* … */]; }
}
```

```php
// ٢. config/shipping.php
'drivers' => ['manual' => ManualDriver::class, 'asyad' => AsyadDriver::class],
```

```php
// ٣. صف في shipping_carriers (Seeder) + بذر statusMap في carrier_status_maps
```

انتهى. الشركة تظهر فوراً في المقارنة والتقارير ولوحة التحكم وشاشة الربط.

---

## قرارات تظهر أثرها مباشرة في الكود

| القرار | أين | لماذا |
|---|---|---|
| الكتابة المحلية **قبل** نداء الشركة | `ShipmentCreationService::create()` | فقدان بوليصة أُنشئت لدى الشركة أسوأ من صف محلي معلّق |
| `idempotency_key` فريد + فحص مسبق | نفس الملف + هجرة `shipments` | ضغطة زر مزدوجة أو انقطاع شبكة لا ينتجان بوليصتين ورسمين |
| الحالة مشتقة من السجل الزمني | `ShipmentEventRecorder` هو الكاتب الوحيد لـ `status` | تاريخ قابل للتدقيق وإعادة البناء |
| `UNIQUE(shipment_id, hash)` | هجرة `shipment_events` | أحداث الـ Webhook تصل مكررة وخارج ترتيبها — تُحلّ في القاعدة لا في الكود |
| خريطة الحالات في القاعدة | `carrier_status_maps` | رمز حالة جديد يُحلّ بصف واحد لا بنشر جديد |
| لقطة العنوان لا مرجع | `shipment_addresses` | تعديل العميل لعنوانه لا يغيّر بوليصة مطبوعة |
| حذف الحقول المالية من الرد | `ShipmentResource::mergeWhen` | موظف الشحن لا يرى التكلفة — حذفاً لا إخفاءً بـ CSS |
| `TenantScope` عام + اختبار CI | `Concerns\BelongsToStore` + `TenantIsolationTest` | العزل افتراضي لا اختياري |
| `DECIMAL(10,3)` لكل المبالغ | كل الهجرات | الريال العُماني ثلاث خانات، والعائم يفسد المحاسبة |
| الشركة غير المتاحة تُعرض بسببها | `RateComparisonService::$unavailable` | المستخدم يحتاج أن يعرف أنها لا تغطي الوجهة لا أنها غالية |

---

## الاختبارات

```bash
php artisan test --filter=Shipping
```

اختبارات الوحدة (الوزن الحجمي، آلة الحالات، تطبيع الهواتف) تعمل بلا قاعدة بيانات.
اختبارا الميزات يحتاجان `Tests\TestCase` الخاص بالتطبيق وقاعدة اختبار.

`TenantIsolationTest` إلزامي في CI: يثبت أن متجراً لا يرى بيانات متجر آخر.
