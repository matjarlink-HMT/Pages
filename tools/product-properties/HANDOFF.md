# HANDOFF — توسعة خصائص المنتجات (MatjarLink)

> ملف تسليم لنقل العمل إلى جلسة Claude Code جديدة.
> الجلسة السابقة كانت تعمل في بيئة سحابية بدون وصول للمتصفح. الجلسة الجديدة يُفترض
> أن تعمل على جهاز الويندوز المرتبط، أي **مع إمكانية تصفّح المواقع** — وهذه هي النقطة
> الأهم في المهمة المتبقية.

---

## 1. الطلب الأصلي

> «بناءً على ملف MatjarLink_Master_Data_File (LAST_UPDATE)، اشتغل فقط على
> `Product Properties sheet` و `Properties + Options sheet`.
> أضف خيارات أكثر للبروبيرتي بناءً على المنتج — بعض المنتجات تتجاوز 15 بروبيرتي وبعضها
> يتجاوز 30، والهواتف النقالة أكثر من 40. استعن بمواقع عالمية مثل نون، إكسترا،
> شرف دي جي، نمشي وغيرها من المواقع الموثوقة. البيانات دقيقة وصحيحة بدون تخمين.
> النتيجة النهائية: ملف إكسل منفصل.»

قيود مهمة التزمت بها الجلسة السابقة:
- **لا يتم تعديل الملف الرئيسي** — المخرجات في ملف منفصل.
- **لا تُحذف ولا تُعاد صياغة أي خاصية موجودة** — تُقرأ كما هي وتوضع أولاً.
- العمل محصور في الشيتين المذكورين فقط.

---

## 2. الحالة الحالية — ما تم إنجازه

### المخرجات

| المؤشر | قبل | بعد |
|---|---|---|
| عدد الفئات | 1,172 | 1,172 |
| إجمالي الخصائص | 7,007 | **43,660** |
| الحد الأدنى للفئة | 4 | **21** |
| المتوسط للفئة | 6.0 | **37.3** |
| الأعلى للفئة | 13 | **66** (هاتف جوال) |

التوزيع: 35 فئة تحت 25 خاصية · 304 بين 25-34 · 736 بين 35-44 · 97 بـ 45 فأكثر.

أمثلة: هاتف جوال 66 · ثلاجات 50 · حواسيب محمولة 49 · غسالة 46 · تلفزيون 45 ·
فساتين 43 · سيارات 43 · كاميرا 41 · تابلت 41.

### أماكن الملفات

**Google Drive (المصدر — للقراءة فقط):**
- الملف الرئيسي: `MatjarLink_Master_Data_File (LAST_UPDATE)`
  - `fileId = 1mpeAFGxsI9V2S3o5vIUuTLO87NfOb-wq`
  - المجلد الأب: `1FPZjplJ69l1gSpYmaUc_r-4wI6lpy3V0`
  - الشيتات: `Overview`, `Categories`, `Brands`, `Category Brands`,
    **`Product Properties`**, **`Properties + Options`**,
    `All Activities (ISIC Oman)`, `Activity ↔ Categories (L2)`, `Activity Field`

**مستودع GitHub:**
- `matjarlink-HMT/Pages` — الفرع `claude/expanded-product-properties-vak7pa`
- كوميت: `e5060f0` · PR مسودة رقم **#9**
- `data/MatjarLink_Product_Properties_Expanded.xlsx` ← الملف النهائي
- `tools/product-properties/` ← سكربتات التوليد + `README.md` + هذا الملف

---

## 3. بنية الحل (مهم لفهم الكود قبل تعديله)

```
tools/product-properties/
├── build.py         # المشغّل الرئيسي: يقرأ master.xlsx ويكتب ملف الإخراج
├── classify.py      # تصنيف كل فئة إلى "عائلة خصائص" بقواعد Regex مرتّبة
├── lib_core.py      # الدوال المساعدة + الكتل المشتركة + قوائم القيم العامة
├── lib_tech.py      # mobile_phone, tablet, laptop, desktop, monitor, television
├── lib_tech2.py     # camera, headphones, speaker, smartwatch, console, printer,
│                    # network, storage_device, powerbank
├── lib_home.py      # washer, fridge, ac, cooking_appliance, small_appliance,
│                    # vacuum, lighting, furniture, kitchenware, home_textile, cleaning
├── lib_auto.py      # auto_part, auto_light, auto_brake, auto_filter,
│                    # auto_accessory, tyre, vehicle, auto_consumable
├── lib_misc.py      # apparel, footwear, bag, jewellery, watch, eyewear, makeup,
│                    # perfume, personal_care, baby, toy, pet, livestock
├── lib_misc2.py     # medicine, supplement, medical_device, sports_equipment,
│                    # stationery, book, craft, gift
├── lib_ind.py       # power_tool, hand_tool, construction, tiles, paint, sanitary,
│                    # electrical, industrial, safety_ppe
├── lib_last.py      # camping, food, beverage, decor, garden, course, service, generic
└── lib_extra.py     # phone_accessory, pc_peripheral, dishwasher, video_game
```

### كيف يعمل `build.py`

1. يقرأ `master.xlsx` (يجب وضعه بجانب السكربتات بهذا الاسم).
2. يقرأ شيت `Categories` ويبني خريطة `Leaf → (L1, L2)` بمطابقة نصية + fuzzy.
3. لكل فئة: `classify()` يعيد اسم عائلة، ثم تُدمج كتلة العائلة مع الخصائص الموجودة.
4. المطابقة للتكرار تتم بـ `norm_name()` — تُسقط ما بين الأقواس وتوحّد `&`/الرموز،
   فلا تتكرر «Screen Size (inch)» مع «Screen Size».
5. الترتيب النهائي حسب `GROUP_ORDER` الثابت (Main، General، Specifications، … Origin).

### تعريف الخاصية

كل خاصية = تابل من 9 حقول:
```
(group, en, ar, pp_type, pp_list, po_data, po_list, required, option)
```
تُبنى عبر دوال مختصرة في `lib_core.py`:

| الدالة | الاستخدام | Data_Type | Data (Options sheet) |
|---|---|---|---|
| `D(...)` | قائمة منسدلة | `Dropdown` | `List` + نفس القائمة |
| `B(...)` | نعم/لا | `Boolean` | `List` + `Yes, No` |
| `N(...)` | رقم عشري + قائمة شرائح | `Decimal` | `List` + الشرائح |
| `I(...)` | رقم صحيح + قائمة شرائح | `Integer` | `List` + الشرائح |
| `T(...)` | نص حر | `Text` | `Free` (بدون قيم) |

`blk(*parts)` تدمج كتلاً متعددة وتزيل التكرار بالاسم مع الإبقاء على أول ظهور.

كتل مشتركة جاهزة في `lib_core.py`: `IDENT`, `COMMERCE`, `COLOR`, `CERT`,
`ELEC_COMMERCE`, `BEAUTY_BASE`, `APPAREL_BASE`, `FOOTWEAR_BASE`, `FOOD_BASE`.
وقوائم قيم عامة: `COLORS`, `COND`, `WARR_TYPE`, `WARR_PERIOD`, `ORIGIN`,
`WEIGHT_KG`, `IP_RATING`, `ENERGY`, `GCC_CERT`, `PACK_QTY`.

### تشغيل التوليد

```bash
pip install openpyxl
cd tools/product-properties
# ضع الملف الرئيسي بجانب السكربتات باسم master.xlsx
python3 build.py
```
المخرج: `MatjarLink_Product_Properties_Expanded.xlsx` + `report.json` (تقرير لكل فئة).

⚠️ لا تُشغّله عبر `| head` — إغلاق الأنبوب مبكراً يقتل العملية قبل كتابة `report.json`.

---

## 4. المهمة المتبقية — وهي سبب نقل الجلسة

### المشكلة

الجلسة السابقة **لم تتمكن من فتح المواقع المطلوبة**. سياسة الشبكة في البيئة السحابية
حجبت النطاقات بالكامل — كل هذه رجعت `000` (فشل اتصال):

```
noon.com · extra.com · sharafdg.com · namshi.com · gsmarena.com
```

`WebFetch` أعاد `EGRESS_BLOCKED` لكل نطاق خارجي. المتاح كان `WebSearch` فقط —
أي نتائج بحث مختصرة، لا فتح صفحات.

### ما بُني عليه المحتوى فعلياً (وهو صحيح لكنه غير مُطابَق حرفياً)

مصادر تم التحقق منها من نتائج البحث:
- **نون**: فلاتر الجوالات — الماركة، التقييم، تاريخ الإطلاق، الرام، السعر،
  سعة البطارية، الكاميرا، سنة الموديل، نوع الشبكة، عدد الشرائح، اللون.
- **نمشي**: بارامترات الفلاتر في الرابط — `size_clothing`، `namshi_dress_style`،
  `namshi_neck_type` بقيم `high_neck, halter_neck, sweetheart_neck, square_neck, plunge_neck`.
- **شرف دي جي**: بنية السمات في الرابط — `taxonomies.attr.Processor`.
- **الغسالات**: السعة بالكيلو، سرعة العصر RPM (400–1800)، ملصق الطاقة الأوروبي A–G
  (النسخة المعتمدة منذ مارس 2021).

معايير صناعية موثّقة استُخدمت مباشرة:
IP / IK ratings · EU Energy Label · PEI (البلاط) · مؤشرات الإطارات (الحمل والسرعة) ·
ECE R44/04 و UN R129 i-Size (كراسي الأطفال) · EN 397 / EN 166 / EN 149 (معدات السلامة) ·
GCC Conformity / SASO / G-Mark / ESMA · بنية أوراق مواصفات الهواتف بنمط GSMArena.

### 🎯 المطلوب من الجلسة الجديدة

افتح المواقع بالمتصفح **وطابِق** قوائم الخيارات الحالية مع الفلاتر الحقيقية، ثم عدّل
ملفات `lib_*.py` وأعد التوليد.

**أولوية عالية — الفئات الأكثر أهمية تجارياً:**

| الفئة | العائلة / الملف | ما يجب التقاطه من الموقع |
|---|---|---|
| هاتف جوال | `mobile_phone` / `lib_tech.py` | كل فلاتر صفحة الجوالات + ورقة مواصفات منتج واحد كاملة |
| حواسيب محمولة | `laptop` / `lib_tech.py` | فلاتر المعالج، الجيل، الرام، التخزين، كرت الشاشة، الشاشة |
| تلفزيون | `television` / `lib_tech.py` | المقاسات، تقنية الشاشة، نظام التشغيل، معدل التحديث |
| ثلاجات / غسالات / مكيفات | `fridge`, `washer`, `ac` / `lib_home.py` | السعات، فئات الطاقة، أنظمة التبريد، البرامج |
| ملابس نسائية/رجالية | `apparel` / `lib_misc.py` | المقاسات، القصّة، فتحة الرقبة، الخامة، المناسبة |
| أحذية | `footwear` / `lib_misc.py` | جداول المقاسات EU/UK/US، الخامات، نوع الكعب |
| عطور | `perfume` / `lib_misc.py` | العائلات العطرية، الأحجام، التركيز |
| مكياج | `makeup` / `lib_misc.py` | الدرجات، التغطية، اللمسة النهائية |
| إطارات | `tyre` / `lib_auto.py` | المقاسات، مؤشرات الحمل والسرعة، المواسم |
| قطع غيار السيارات | `auto_part` وأخواتها / `lib_auto.py` | منظومة التوافق (Make/Model/Year) |

**المواقع المقترحة حسب الفئة:**
- إلكترونيات وأجهزة: `extra.com` · `sharafdg.com` · `noon.com` · `amazon.ae`
- أزياء: `namshi.com` · `ounass.com` · `noon.com`
- تجميل وعطور: `namshi.com` · `sephora.ae` · `noon.com`
- بقالة وأغذية: `carrefouruae.com` · `luluhypermarket.com`
- أثاث ومنزل: `ikea.com/ae` · `homecentre.com` · `danubehome.com`
- سيارات وقطع: `carrefouruae.com` · مواقع الوكلاء المحليين
- مواصفات هواتف تفصيلية: `gsmarena.com`

**طريقة العمل المقترحة لكل فئة:**
1. افتح صفحة الفئة على الموقع.
2. وسّع كل الفلاتر الجانبية والتقط **أسماء الفلاتر وقيمها كاملة**.
3. افتح منتجاً واحداً على الأقل والتقط **جدول المواصفات الكامل**.
4. قارن مع الكتلة الحالية في ملف `lib_*.py` المقابل.
5. عدّل: أضف الخصائص الناقصة، صحّح القيم غير المطابقة، احذف غير الموجودة فعلاً.
6. سجّل المصدر (الرابط + التاريخ) في تعليق فوق الكتلة المعدّلة.

---

## 5. مشاكل معروفة تحتاج قراراً

1. **`Mirrors | مرايا`** — في الملف الأصلي تخلط خصائص مرايا المنزل مع مرايا السيارات
   (`Adjustment Type`, `Position`, `Integrated Indicator`, `Compatible Vehicle Make`).
   لم تُفصل تلقائياً. يحتاج قراراً: فصل إلى فئتين، أو إبقاؤها.

2. **فئات مكررة الاسم في المصدر** — الشيت الأصلي يحتوي فئات ببلوكين متداخلين
   (مثل `Soap`, `Cutlery`, `Pillows`). `build.py` يدمجها بالاسم ويحتفظ بأغنى قائمة
   خيارات، لكن الأصل يبقى فيه تكرار.

3. **356 فئة موجودة في `Product Properties` وغير موجودة في `Properties + Options`**
   في الملف الأصلي. ملف الإخراج يوحّد الشيتين (1,172 فئة في كليهما) — تأكد أن هذا
   هو السلوك المطلوب.

4. **أدنى الفئات (21–24 خاصية)** — معظمها `livestock` (جِمال، أبقار، دواجن…) و
   `gift` و `video_game`. طبيعتها لا تحتمل خصائص كثيرة، لكن يمكن توسيعها لو أردت.

---

## 6. فحوصات الجودة (أعد تشغيلها بعد أي تعديل)

سكربت التحقق يفحص الملف الناتج على:
- تطابق قائمة الفئات وترتيبها بين الشيتين.
- تطابق ترتيب الصفوف صفاً بصف بين الشيتين.
- عدم وجود خاصية مكررة داخل نفس الفئة.
- عدم وجود اسم عربي ناقص.
- كل `Dropdown` له `Item_List`.
- كل `Text`/`Integer`/`Decimal` **بدون** `Item_List` في شيت الخصائص.
- كل `List` في شيت الخيارات له قيم.
- كل `Required` و `Option` ضمن `Yes`/`No` فقط.

**النتيجة الحالية: صفر أخطاء.**

```python
import openpyxl, collections
wb = openpyxl.load_workbook('MatjarLink_Product_Properties_Expanded.xlsx', read_only=True)

def parse(name, n):
    ws = wb[name]; cats = collections.OrderedDict(); cur = grp = None
    for r in list(ws.iter_rows(values_only=True))[1:]:
        if r[0]: cur = r[0]; cats[cur] = []
        elif r[1]: grp = r[1]
        elif r[2]: cats[cur].append((grp,) + tuple(r[2:n]))
    return cats

pp, po = parse('Product Properties', 7), parse('Properties + Options', 8)
errs = collections.Counter()
assert list(pp) == list(po)
for c in pp:
    a, b = pp[c], po[c]
    if len(a) != len(b): errs['len_mismatch'] += 1
    if len({x[1].strip().lower() for x in a}) != len(a): errs['dup_prop'] += 1
    for i, (grp, en, ar, dt, il, req) in enumerate(a):
        if not ar: errs['missing_ar'] += 1
        if dt == 'Dropdown' and not il: errs['dropdown_no_list'] += 1
        if dt in ('Text', 'Integer', 'Decimal') and il: errs['nonlist_has_list'] += 1
        if req not in ('Yes', 'No'): errs['bad_req'] += 1
        if b[i][1] != en: errs['misalign'] += 1
    for (grp, en, ar, data, vals, req, opt) in b:
        if data not in ('List', 'Free'): errs['bad_data'] += 1
        if data == 'List' and not vals: errs['list_no_vals'] += 1
        if opt not in ('Yes', 'No'): errs['bad_opt'] += 1
print(dict(errs) or 'NO ERRORS')
```

---

## 7. برومبت جاهز للجلسة الجديدة

```
اقرأ tools/product-properties/HANDOFF.md في مستودع matjarlink-HMT/Pages
على الفرع claude/expanded-product-properties-vak7pa.

المهمة: التحقق من قوائم خيارات الخصائص ومطابقتها مع الفلاتر الحقيقية على
نون وإكسترا وشرف دي جي ونمشي وأمازون الإمارات، باستخدام المتصفح.

ابدأ بفئة الهواتف النقالة (mobile_phone في lib_tech.py):
افتح صفحة الجوالات على نون وإكسترا، وسّع كل الفلاتر، والتقط أسماءها وقيمها،
ثم افتح ورقة مواصفات منتج واحد كاملة. قارنها مع الكتلة الحالية وعدّلها،
وسجّل الرابط والتاريخ في تعليق فوق الكتلة.

بعدها انتقل للحواسيب المحمولة والتلفزيونات حسب جدول الأولويات في ملف التسليم.
أعد تشغيل python3 build.py وفحص الجودة بعد كل تعديل، ثم اعمل كوميت على نفس الفرع.
```

---

## 8. ملاحظات بيئية

- الجلسة السابقة عملت في حاوية سحابية معزولة؛ `WebFetch` محجوب لكل النطاقات الخارجية،
  و`gh` CLI غير متاح (استُخدم GitHub MCP بدلاً منه).
- الجلسة الجديدة على ويندوز يُفترض أن `WebFetch` والمتصفح يعملان — **تحقق أولاً**
  بجلب صفحة واحدة قبل بناء خطة تعتمد على التصفّح.
- `openpyxl` هي التبعية الوحيدة.
- ملف الإخراج ~4.6 MB و 58,965 صفاً في كل شيت.
