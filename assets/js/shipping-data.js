/* ============ وحدة الشحن — البيانات المرجعية ومولّد البيانات التجريبية ============
   النموذج التفاعلي فقط: يولّد بيانات ثابتة (بذرة واحدة) لتجربة الشاشات قبل تنفيذ الخلفية.
   لا يمثّل منطق العمل الحقيقي — المرجع هو docs/shipping-module/ */

const SHIPDATA = (() => {

  /* ---------- الحالات الداخلية الموحّدة ---------- */
  const STATUS = {
    draft:            { ar: "مسودة",              badge: "b-gray",   stage: 0, terminal: false },
    pending_carrier:  { ar: "بانتظار الشركة",     badge: "b-gray",   stage: 0, terminal: false },
    carrier_error:    { ar: "فشل الإرسال للشركة", badge: "b-red",    stage: 0, terminal: false, attention: true },
    created:          { ar: "تم الإنشاء",         badge: "b-blue",   stage: 1, terminal: false },
    picked_up:        { ar: "تم الاستلام",        badge: "b-purple", stage: 2, terminal: false },
    in_transit:       { ar: "أثناء النقل",        badge: "b-purple", stage: 3, terminal: false },
    out_for_delivery: { ar: "خرجت للتسليم",       badge: "b-amber",  stage: 4, terminal: false },
    delivered:        { ar: "تم التسليم",         badge: "b-green",  stage: 5, terminal: true },
    failed_attempt:   { ar: "فشل التسليم",        badge: "b-red",    stage: 4, terminal: false, attention: true },
    exception:        { ar: "استثناء",            badge: "b-red",    stage: 3, terminal: false, attention: true },
    returning:        { ar: "في طريق الإرجاع",    badge: "b-amber",  stage: 3, terminal: false },
    returned:         { ar: "تم الإرجاع",         badge: "b-gray",   stage: 5, terminal: true },
    cancelled:        { ar: "ملغاة",              badge: "b-gray",   stage: 0, terminal: true },
  };
  const STAGES = ["الإنشاء", "الاستلام", "النقل", "خرجت للتسليم", "التسليم"];

  /* ---------- شركات الشحن ---------- */
  const CARRIERS = [
    { code: "asyad", pre: "ASY",     name: "أسياد إكسبريس", short: "أس", color: "#1f6f5c", api: true,  scope: "محلي",
      services: [{ code: "STD", name: "توصيل عادي", days: [2, 3], base: 1.700 },
                 { code: "EXP", name: "توصيل سريع", days: [1, 2], base: 2.150 }],
      feat: ["تتبع مباشر", "الدفع عند الاستلام", "استلام من الموقع"], perf: { success: 96.4, ontime: 91.2, rating: 4.6 } },
    { code: "oman_post", pre: "OPX", name: "بريد عُمان",     short: "بع", color: "#8E1B5B", api: true,  scope: "محلي",
      services: [{ code: "STD", name: "توصيل عادي", days: [3, 5], base: 1.200 }],
      feat: ["تغطية كل الولايات", "الدفع عند الاستلام"], perf: { success: 93.1, ontime: 82.5, rating: 4.0 } },
    { code: "aramex", pre: "ARX",    name: "أرامكس",        short: "أر", color: "#d23b4e", api: true,  scope: "إقليمي/دولي",
      services: [{ code: "DOM", name: "محلي", days: [1, 2], base: 2.400 },
                 { code: "GCC", name: "خليجي", days: [3, 5], base: 5.800 }],
      feat: ["تتبع مباشر", "تأمين", "شحن دولي"], perf: { success: 94.8, ontime: 88.9, rating: 4.4 } },
    { code: "smsa", pre: "SMS",      name: "سمسا",          short: "سم", color: "#2f6bd6", api: true,  scope: "إقليمي",
      services: [{ code: "DOM", name: "محلي", days: [2, 3], base: 2.050 }],
      feat: ["تتبع مباشر", "الدفع عند الاستلام"], perf: { success: 91.6, ontime: 79.3, rating: 3.9 } },
    { code: "imile", pre: "IML",     name: "آي مايل",       short: "آم", color: "#7a3fc9", api: true,  scope: "محلي",
      services: [{ code: "STD", name: "توصيل عادي", days: [1, 3], base: 1.550 }],
      feat: ["الدفع عند الاستلام", "توصيل مسائي"], perf: { success: 95.2, ontime: 86.7, rating: 4.3 } },
    { code: "manual", pre: "MJL",    name: "مندوب المتجر",  short: "مم", color: "#c9821a", api: false, scope: "مسقط فقط",
      services: [{ code: "OWN", name: "توصيل ذاتي", days: [0, 1], base: 1.000 }],
      feat: ["نفس اليوم", "الدفع عند الاستلام"], perf: { success: 98.1, ontime: 94.4, rating: 4.8 } },
  ];
  const carrier = (code) => CARRIERS.find(c => c.code === code) || CARRIERS[0];

  /* ---------- الجغرافيا العُمانية ---------- */
  const GEO = {
    "مسقط":            ["مسقط", "مطرح", "بوشر", "السيب", "العامرات", "قريات"],
    "ظفار":            ["صلالة", "طاقة", "مرباط", "ثمريت", "رخيوت"],
    "شمال الباطنة":    ["صحار", "شناص", "لوى", "صحم", "الخابورة", "السويق"],
    "جنوب الباطنة":    ["الرستاق", "العوابي", "نخل", "وادي المعاول", "بركاء", "المصنعة"],
    "الداخلية":        ["نزوى", "بهلاء", "منح", "الحمراء", "أدم", "إزكي", "سمائل", "بدبد"],
    "شمال الشرقية":    ["إبراء", "المضيبي", "بدية", "وادي بني خالد", "دماء والطائيين"],
    "جنوب الشرقية":    ["صور", "الكامل والوافي", "جعلان بني بوعلي", "جعلان بني بوحسن", "مصيرة"],
    "البريمي":         ["البريمي", "محضة", "السنينة"],
    "الظاهرة":         ["عبري", "ينقل", "ضنك"],
    "الوسطى":          ["هيماء", "محوت", "الدقم", "الجازر"],
    "مسندم":           ["خصب", "بخا", "دبا", "مدحاء"],
  };
  const GOVS = Object.keys(GEO);
  /* المناطق النائية: رسوم إضافية وأزمنة أطول */
  const REMOTE = ["الوسطى", "مسندم", "الظاهرة"];

  /* ---------- أسماء تجريبية ---------- */
  const FIRST = ["سالم", "ناصر", "خالد", "أحمد", "يوسف", "بدر", "حمد", "طارق", "سيف", "ماجد",
                 "مريم", "عائشة", "فاطمة", "نورة", "هدى", "سمية", "لطيفة", "أسماء", "زينب", "ريم"];
  const LAST  = ["الحارثي", "البلوشي", "الرواحي", "الكندي", "المعمري", "الهنائي", "السيابي",
                 "الشامسي", "الغافري", "البوسعيدي", "الفارسي", "الزدجالي", "العبري", "الريامي"];

  /* ---------- مولّد عشوائي ببذرة ثابتة ---------- */
  const rng = (seed) => () => (seed = (seed * 1103515245 + 12345) & 0x7fffffff) / 0x7fffffff;

  const pick = (r, arr) => arr[Math.floor(r() * arr.length)];
  const between = (r, a, b) => a + Math.round(r() * (b - a));
  const round3 = (n) => Math.round(n * 1000) / 1000;
  const iso = (d) => new Date(d).toISOString();
  const addH = (d, h) => new Date(new Date(d).getTime() + h * 3600000);

  /* أوزان توزيع الحالات — يعكس واقعاً تشغيلياً معقولاً */
  const MIX = [
    ["delivered", 58], ["in_transit", 9], ["out_for_delivery", 6], ["picked_up", 5],
    ["created", 6], ["returned", 5], ["failed_attempt", 4], ["exception", 3],
    ["cancelled", 2], ["carrier_error", 1], ["returning", 1],
  ];
  /* الشحنات الأقدم من ٥ أيام وصلت غالباً لحالة نهائية */
  const MIX_OLD = [
    ["delivered", 79], ["returned", 8], ["cancelled", 4], ["failed_attempt", 3],
    ["exception", 2], ["returning", 2], ["in_transit", 2],
  ];
  const pickStatus = (r, mix = MIX) => {
    const total = mix.reduce((s, m) => s + m[1], 0);
    let x = r() * total;
    for (const [k, w] of mix) { if ((x -= w) <= 0) return k; }
    return "delivered";
  };

  /* ---------- بناء السجل الزمني من الحالة ----------
     كل الأحداث كنسب من مدة D حتى لا يسبق حدث حدثاً قبله ولا يقع أي حدث في المستقبل. */
  const buildEvents = (r, sh) => {
    const elapsed = (Date.now() - new Date(sh.createdAt)) / 3600000;
    const D = sh.status === "delivered"
      ? Math.min(sh.deliveryHours, elapsed * 0.95)
      : Math.max(1.5, Math.min(elapsed * 0.9, sh.deliveryHours * 1.4));
    sh.deliveryHours = Math.round(D * 10) / 10;

    const evs = [];
    const push = (st, txt, loc, f, src) => evs.push({
      status: st, text: txt, location: loc, at: iso(addH(sh.createdAt, Math.min(f * D, elapsed * 0.99))),
      source: src || (carrier(sh.carrier).api ? "webhook" : "manual"),
    });
    push("created", "تم إنشاء الشحنة وإصدار بوليصة الشحن", "متجرلينك", 0, "system");

    const st = sh.status, sg = STATUS[st].stage;
    if (st === "cancelled") { push("cancelled", "أُلغيت الشحنة قبل الاستلام", "متجرلينك", 0.5, "manual"); return evs; }
    if (st === "carrier_error") { push("carrier_error", "تعذّر إرسال الشحنة إلى نظام الشركة — بيانات المستلم مرفوضة", "—", 0.02, "system"); return evs; }

    const returning = st === "returning" || st === "returned";
    if (sg >= 2 || returning) push("picked_up", "استلمت شركة الشحن الطرد من المتجر", "مسقط", 0.15);
    if (sg >= 3 || returning) {
      push("in_transit", "وصل الطرد إلى مركز الفرز الرئيسي", "مركز فرز مسقط", 0.32);
      if (sh.gov !== "مسقط") push("in_transit", `غادر الطرد متجهاً إلى ${sh.gov}`, "مركز فرز مسقط", 0.5);
    }
    if ((sg >= 4 && st !== "exception") || st === "returned")
      push("out_for_delivery", "خرج الطرد مع المندوب للتسليم", sh.wilayat, 0.78);

    if (st === "delivered") push("delivered", "تم تسليم الطرد للمستلم", sh.wilayat, 1);
    if (st === "failed_attempt") push("failed_attempt", "تعذّر التسليم — المستلم غير متجاوب", sh.wilayat, 0.92);
    if (st === "exception") push("exception", "العنوان غير واضح — بانتظار تأكيد من المتجر", sh.wilayat, 0.6);
    if (st === "returning") push("returning", "بدأ إرجاع الطرد إلى المتجر", sh.wilayat, 0.95);
    if (st === "returned") {
      push("failed_attempt", "تعذّر التسليم — رفض المستلم الاستلام", sh.wilayat, 0.84);
      push("returning", "بدأ إرجاع الطرد إلى المتجر", sh.wilayat, 0.9);
      push("returned", "تم إرجاع الطرد إلى المتجر", "مسقط", 1);
    }
    return evs.sort((a, b) => a.at.localeCompare(b.at));
  };

  /* ---------- توليد الشحنات ---------- */
  const generate = (count = 240, seed = 20260805) => {
    const r = rng(seed);
    const today = new Date(); today.setHours(12, 0, 0, 0);
    const out = [];
    for (let i = 0; i < count; i++) {
      const daysAgo = Math.floor(Math.pow(r(), 1.5) * 89);        // كثافة أعلى للأيام القريبة
      const createdAt = iso(new Date(today.getTime() - daysAgo * 86400000 - between(r, 0, 10) * 3600000));
      const gov = r() < 0.44 ? "مسقط" : pick(r, GOVS);
      const wilayat = pick(r, GEO[gov]);
      const c = pick(r, gov === "مسقط" ? CARRIERS : CARRIERS.filter(x => x.code !== "manual"));
      const svc = pick(r, c.services);
      const remote = REMOTE.includes(gov);
      const weight = round3(0.5 + r() * 8);
      const pieces = r() < 0.82 ? 1 : between(r, 2, 4);
      const isCod = r() < 0.62;
      const orderTotal = round3(5 + r() * 85);

      const status = daysAgo < 2 ? pick(r, ["created", "picked_up", "in_transit", "out_for_delivery", "created"])
                   : daysAgo < 5 ? pickStatus(r)
                   : pickStatus(r, MIX_OLD);

      const etaDays = svc.days[1] + (remote ? 2 : 0);
      const promisedAt = iso(new Date(new Date(createdAt).getTime() + etaDays * 86400000));
      /* زمن التسليم كنسبة من الوعد: ~٨٠٪ ضمن الموعد و~٢٠٪ متأخرة — توزيع تشغيلي معقول */
      const deliveryHours = Math.max(4, Math.round(etaDays * 24 * (0.45 + r() * 0.68)));
      const sh = {
        id: "s" + (i + 1),
        ref: "SHP-2026-" + String(1000 + i).padStart(6, "0"),
        orderNo: "ORD-" + (48200 + i * 3 + between(r, 0, 2)),
        carrier: c.code, service: svc.code, serviceName: svc.name,
        tracking: c.pre + String(90000000 + Math.floor(r() * 9999999)),
        customer: pick(r, FIRST) + " " + pick(r, LAST),
        phone: "+9689" + between(r, 1000000, 9999999),
        gov, wilayat,
        area: "", street: "شارع " + between(r, 10, 90), landmark: "",
        createdAt, promisedAt, deliveryHours, status,
        weight, pieces, declaredValue: orderTotal,
        isCod, codAmount: isCod ? orderTotal : 0,
        cost: 0, quotedCost: 0, notes: "",
      };
      // التكلفة: أساس الخدمة + وزن + منطقة نائية + رسوم تحصيل
      const base = svc.base + Math.max(0, weight - 1) * 0.25 + (remote ? 0.9 : 0) + (pieces - 1) * 0.4;
      sh.quotedCost = round3(base + (isCod ? Math.max(0.3, orderTotal * 0.01) : 0));
      // الفعلي يختلف أحياناً عن المُسعّر — أساس تقرير مطابقة الفواتير
      sh.cost = round3(sh.quotedCost * (r() < 0.12 ? 1 + r() * 0.22 : 1));
      sh.events = buildEvents(r, sh);
      const last = sh.events[sh.events.length - 1];
      sh.updatedAt = last.at;
      sh.deliveredAt = status === "delivered" ? last.at : null;
      sh.isDelayed = !STATUS[status].terminal && new Date(promisedAt) < new Date();
      sh.isStale = !STATUS[status].terminal && (Date.now() - new Date(sh.updatedAt)) > 72 * 3600000;
      out.push(sh);
    }
    return out.sort((a, b) => b.createdAt.localeCompare(a.createdAt));
  };

  /* ---------- حسابات شركات الشحن الافتراضية ---------- */
  const defaultAccounts = () => CARRIERS.map((c, i) => ({
    code: c.code,
    connected: i < 4 || c.code === "manual",
    active: i < 4 || c.code === "manual",
    isDefault: c.code === "asyad",
    env: "live",
    key: c.api ? "••••••" + (3000 + i * 137) : "",
    status: c.code === "smsa" ? "failed" : (i < 4 || c.code === "manual" ? "connected" : "unknown"),
    error: c.code === "smsa" ? "بيانات الاعتماد مرفوضة (401) — يلزم تحديث المفتاح" : "",
    checkedAt: iso(new Date(Date.now() - (i + 1) * 37 * 60000)),
    zones: c.code === "manual" ? ["مسقط"] : (c.code === "oman_post" ? GOVS.slice() : GOVS.filter(g => !REMOTE.includes(g) || c.code === "asyad")),
  }));

  return { STATUS, STAGES, CARRIERS, carrier, GEO, GOVS, REMOTE, generate, defaultAccounts, round3 };
})();
