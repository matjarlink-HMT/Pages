# ٠٥ — واجهات الـ API

أربع مجموعات منفصلة تماماً في المسار والمصادقة:

| المجموعة | البادئة | المصادقة | الغرض |
|---|---|---|---|
| لوحة التاجر | `/api/v1/shipping/*` | جلسة/Sanctum + صلاحيات | واجهة متجرلينك نفسها |
| Webhooks الواردة | `/webhooks/shipping/{carrier}` | توقيع الشركة + IP | استقبال أحداث الشركات |
| التتبع العام | `/track/*` | بلا مصادقة (رابط موقّع) | العميل النهائي |
| تكامل خارجي | `/api/partner/v1/shipping/*` | API Key + HMAC | ERP / POS / CRM |

كل الردود بمظروف موحّد ومعرّف ارتباط:
```json
{ "data": {...}, "meta": {...}, "correlation_id": "01JB..." }
```

---

## ١. لوحة التاجر

### لوحة التحكم والتحليلات
```
GET  /api/v1/shipping/dashboard?range=30d&carrier_id=&governorate=
GET  /api/v1/shipping/dashboard/timeseries?metric=shipments|cost|delivery_time&group=day
GET  /api/v1/shipping/dashboard/attention        # الشحنات المتأخرة/الصامتة/الفاشلة
```

### الشحنات
```
GET    /api/v1/shipping/shipments
       ?q=&status[]=&carrier_id[]=&governorate[]=&is_cod=&is_delayed=
       &date_from=&date_to=&sort=-created_at&cursor=&per_page=25
POST   /api/v1/shipping/shipments                 # إنشاء (Idempotency-Key مطلوب)
GET    /api/v1/shipping/shipments/{uuid}
PATCH  /api/v1/shipping/shipments/{uuid}          # ملاحظات/بيانات قابلة للتعديل قبل التسليم
DELETE /api/v1/shipping/shipments/{uuid}          # إلغاء (يستدعي الشركة إن دعمت)
POST   /api/v1/shipping/shipments/{uuid}/sync     # تحديث فوري يدوي
POST   /api/v1/shipping/shipments/{uuid}/events   # حدث يدوي (للشركات بلا API)
GET    /api/v1/shipping/shipments/{uuid}/events
POST   /api/v1/shipping/shipments/{uuid}/label    # إصدار/إعادة إصدار
GET    /api/v1/shipping/shipments/{uuid}/label?format=pdf_a4   # رابط موقّع
POST   /api/v1/shipping/shipments/{uuid}/duplicate
GET    /api/v1/shipping/shipments/export?format=csv|xlsx       # تصدير خلفي
```

**عمليات دفعية:**
```
POST /api/v1/shipping/shipments/bulk                # إنشاء من عدة طلبات
POST /api/v1/shipping/shipments/bulk/labels         # دمج بوالص في PDF واحد
POST /api/v1/shipping/shipments/bulk/status         # تحديث حالة يدوي جماعي
POST /api/v1/shipping/shipments/bulk/import         # استيراد CSV (شركات يدوية)
```

**نموذج إنشاء شحنة:**
```http
POST /api/v1/shipping/shipments
Idempotency-Key: 8f14e45fceea167a5a36dedd4bea2543
```
```json
{
  "order_id": 10432,
  "store_carrier_account_id": 7,
  "service_code": "EXPRESS",
  "sender":   { "address_book_id": 3 },
  "receiver": {
    "name": "سالم بن ناصر", "phone": "+96899123456",
    "governorate": "مسقط", "wilayat": "بوشر", "area": "الغبرة الشمالية",
    "street": "شارع 3011", "building": "منزل 24",
    "landmark": "خلف مسجد النور", "latitude": 23.588, "longitude": 58.383
  },
  "packages": [ { "weight_kg": 2.4, "length_cm": 30, "width_cm": 20, "height_cm": 15 } ],
  "items": [ { "order_item_id": 88213, "sku": "TSH-BLK-M", "quantity": 2, "unit_value": 7.5 } ],
  "declared_value": 15.0,
  "is_cod": true,
  "cod_amount": 15.0,
  "notes": "الاتصال قبل التوصيل بساعة"
}
```

**الرد (201):**
```json
{
  "data": {
    "uuid": "9d1f...", "reference": "SHP-2026-000123",
    "status": "created", "status_label": "تم الإنشاء",
    "tracking_number": "ASY9938271", "tracking_url": "https://…/track/9d1f…",
    "carrier": { "id": 1, "code": "asyad", "name": "أسياد إكسبريس" },
    "label": { "format": "pdf_a4", "url": "https://…signed…", "expires_at": "…" },
    "costs": { "quoted": 2.150, "cod_fee": 0.500, "total": 2.650, "currency": "OMR" },
    "promised_delivery_at": "2026-08-08T15:00:00+04:00"
  }
}
```

### التسعير والمقارنة
```
POST /api/v1/shipping/rates          # يُرجع كل العروض من كل الشركات المتاحة
POST /api/v1/shipping/rates/best     # عرض واحد حسب قواعد الأتمتة/التوصية
```
رد التسعير:
```json
{ "data": [{
    "carrier": { "code": "asyad", "name": "أسياد إكسبريس", "logo": "…" },
    "account_id": 7, "service_code": "EXPRESS", "service_name": "توصيل سريع",
    "price": 2.150, "currency": "OMR",
    "eta": { "min_days": 1, "max_days": 2, "label": "١–٢ يوم عمل" },
    "features": ["تتبع مباشر", "الدفع عند الاستلام", "تأمين حتى 50 ر.ع"],
    "performance": { "success_rate": 96.4, "on_time_rate": 91.2, "rating": 4.6 },
    "score": 88.5, "recommended": true, "source": "api"
}], "meta": { "quote_group_uuid": "…", "expires_at": "…", "unavailable": [
    { "carrier": "dhl", "reason": "لا تغطي الوجهة" },
    { "carrier": "smsa", "reason": "تعذّر الاتصال — انتهت المهلة" } ] } }
```
> **قرار تجربة:** الشركات غير المتاحة تُعرض مع سببها بدل إخفائها. المستخدم يحتاج أن يعرف أن دي إتش إل لم تُستبعد لأنها غالية بل لأنها لا تغطي.

### شركات الشحن والحسابات
```
GET    /api/v1/shipping/carriers                     # الكتالوج + حالة الربط
GET    /api/v1/shipping/carriers/{code}/schema       # مخطط بناء نموذج الربط
GET    /api/v1/shipping/carrier-accounts
POST   /api/v1/shipping/carrier-accounts
PATCH  /api/v1/shipping/carrier-accounts/{id}
DELETE /api/v1/shipping/carrier-accounts/{id}
POST   /api/v1/shipping/carrier-accounts/{id}/test       # اختبار الاتصال
POST   /api/v1/shipping/carrier-accounts/{id}/toggle
POST   /api/v1/shipping/carrier-accounts/{id}/set-default
GET    /api/v1/shipping/carrier-accounts/{id}/services   # الخدمات من الشركة
```
> بيانات الاعتماد **تُكتب ولا تُقرأ أبداً**: الرد يُرجع `"api_key": "••••••••3f21"` فقط.

### المناطق والتسعيرات اليدوية
```
GET|POST|PATCH|DELETE /api/v1/shipping/zones
GET|POST|PATCH|DELETE /api/v1/shipping/rate-cards
GET|POST|PATCH|DELETE /api/v1/shipping/rate-cards/{id}/rules
POST /api/v1/shipping/rate-cards/{id}/simulate     # جرّب: وجهة + وزن ← السعر
```

### طلبات الاستلام والمرتجعات والمطالبات
```
GET|POST /api/v1/shipping/pickups
POST     /api/v1/shipping/pickups/{id}/cancel
GET|POST /api/v1/shipping/returns
POST     /api/v1/shipping/returns/{id}/approve|reject
GET|POST /api/v1/shipping/claims
POST     /api/v1/shipping/claims/{id}/submit
```

### التقارير
```
GET /api/v1/shipping/reports/overview?from=&to=
GET /api/v1/shipping/reports/carriers          # مقارنة أداء الشركات
GET /api/v1/shipping/reports/cities            # أكثر المدن/الولايات
GET /api/v1/shipping/reports/customers         # أكثر العملاء
GET /api/v1/shipping/reports/costs?group=day|week|month|carrier
GET /api/v1/shipping/reports/delivery-times
GET /api/v1/shipping/reports/delays
GET /api/v1/shipping/reports/returns
GET /api/v1/shipping/reports/cod-settlements
GET /api/v1/shipping/reports/invoice-audit     # فروقات الفواتير
GET /api/v1/shipping/reports/{report}/export?format=csv|xlsx|pdf
```

### الإعدادات وقواعد الأتمتة والقوالب
```
GET|PATCH /api/v1/shipping/settings
GET|POST|PATCH|DELETE /api/v1/shipping/automation-rules
POST /api/v1/shipping/automation-rules/{id}/test     # جرّب القاعدة على شحنة نموذجية
GET|POST|PATCH /api/v1/shipping/notification-templates
GET|POST|PATCH /api/v1/shipping/address-book
```

---

## ٢. Webhooks الواردة

```
POST /webhooks/shipping/{carrier_code}
POST /webhooks/shipping/{carrier_code}/{account_uuid}   # للشركات التي تدعم مسارات لكل حساب
```
السلوك: `حفظ خام → 200 فوراً → معالجة في طابور`.
الحماية: توقيع HMAC/رمز الشركة · قائمة IP بيضاء لكل Driver · نافذة زمنية ٥ دقائق ضد إعادة الإرسال · `event_uid` فريد.

**واجهة تشخيص للعمليات:**
```
GET  /api/v1/shipping/webhook-events?carrier=&processed=&signature_valid=
POST /api/v1/shipping/webhook-events/{id}/replay
```

---

## ٣. التتبع العام (للعميل النهائي)

```
GET /track/{shipment_uuid}                  # صفحة بعلامة المتجر
GET /api/public/track/{shipment_uuid}
POST /api/public/track/lookup               # { tracking_number, phone_last4 }
```
يُرجع فقط: الحالة، السجل الزمني، الوعد بالتسليم، اسم الشركة، آخر ٤ أرقام من الهاتف مقنّعة.
**لا يُرجع أبداً:** التكلفة، الهامش، البيانات الداخلية، اسم الموظف.
خانق: ٣٠ طلباً/دقيقة لكل IP.

---

## ٤. التكامل الخارجي (ERP / POS / CRM)

```
POST /api/partner/v1/shipping/shipments
GET  /api/partner/v1/shipping/shipments/{reference}
GET  /api/partner/v1/shipping/rates
GET  /api/partner/v1/shipping/carriers
```
مصادقة: `X-Api-Key` + `X-Signature` (HMAC للجسم) + `X-Timestamp`.
حدود: ٦٠ طلباً/دقيقة لكل مفتاح.

### Webhooks صادرة (نُخطر أنظمة التاجر)
```
POST <عنوان التاجر>    الأحداث: shipment.created | shipment.status_changed
                                | shipment.delivered | shipment.returned | shipment.delayed
```
حمولة موقّعة بـ HMAC، إعادة محاولة ٥ مرات بتراجع أُسّي، وصندوق صادر (Outbox) قابل لإعادة الإرسال يدوياً.

---

## ٥. اصطلاحات عامة

| الموضوع | القرار |
|---|---|
| الترقيم | Cursor Pagination على القوائم الكبيرة (أداء ثابت مهما عمق الصفحة) |
| الفلترة | معاملات صريحة لا لغة استعلام حرة (أمان + إمكانية الفهرسة) |
| التصدير | دائماً غير متزامن: `202 Accepted` + معرّف مهمة + إشعار عند الجاهزية |
| رموز الأخطاء | `SHIPPING_CARRIER_UNAVAILABLE`, `SHIPPING_DESTINATION_NOT_COVERED`, `SHIPPING_DUPLICATE_REQUEST`, `SHIPPING_INVALID_CREDENTIALS`, `SHIPPING_WEIGHT_EXCEEDS_LIMIT` … مع رسالة عربية جاهزة للعرض |
| الإصدارات | `/v1` في المسار؛ إضافة حقول غير كاسرة، والحذف يمر بفترة إهمال معلنة |
| المناطق الزمنية | التخزين UTC، والعرض بتوقيت المتجر (`Asia/Muscat`) |
| اللغة | `Accept-Language: ar|en` يحدد لغة الرسائل والحالات |
