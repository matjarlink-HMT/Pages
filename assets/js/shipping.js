/* ============ وحدة الشحن — النموذج التفاعلي ============
   يعرض شاشات الوحدة كما ستكون داخل متجرلينك، ببيانات تجريبية في المتصفح.
   المرجع الهندسي الكامل: docs/shipping-module/ */

const SHIP = (() => {
  const S = SHIPDATA, ST = S.STATUS;

  /* ================= أدوات ================= */
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const esc = HMT.esc;
  const OMR = (n) => (Math.round((n || 0) * 1000) / 1000).toFixed(3) + " ر.ع";
  const num = (n) => (n || 0).toLocaleString("en");
  const pct = (n) => (Math.round(n * 10) / 10).toFixed(1) + "٪";
  const dOnly = (s) => String(s).slice(0, 10);
  const dTime = (s) => { const d = new Date(s); return `${dOnly(s)} · ${String(d.getHours()).padStart(2, "0")}:${String(d.getMinutes()).padStart(2, "0")}`; };
  const rel = (s) => {
    const m = Math.round((Date.now() - new Date(s)) / 60000);
    if (m < 1) return "الآن";
    if (m < 60) return `قبل ${m} دقيقة`;
    const h = Math.round(m / 60);
    if (h < 24) return `قبل ${h} ساعة`;
    const d = Math.round(h / 24);
    return d < 30 ? `قبل ${d} يوم` : `قبل ${Math.round(d / 30)} شهر`;
  };
  const badge = (st) => `<span class="badge ${ST[st].badge}">${ST[st].ar}</span>`;
  const clogo = (code) => { const c = S.carrier(code); return `<span class="clogo" style="background:${c.color}">${c.short}</span>`; };
  const cname = (code) => `<span class="carriercell">${clogo(code)}<span>${esc(S.carrier(code).name)}</span></span>`;
  const days = (a, b) => (new Date(b) - new Date(a)) / 86400000;

  /* ================= الحالة ================= */
  const KEY = "shipping";
  let db = null, view = null;

  const load = () => {
    db = HMT.get(KEY, null);
    if (!db || !db.shipments?.length) reset(true);
  };
  const save = () => HMT.set(KEY, db);
  const reset = (silent) => {
    db = { shipments: S.generate(), accounts: S.defaultAccounts(), seededAt: new Date().toISOString() };
    save();
    if (!silent) { HMT.toast("↺ أُعيدت البيانات التجريبية"); renderAll(); }
  };
  const acc = (code) => db.accounts.find(a => a.code === code);

  /* ================= رسوم ================= */
  const barChart = (el, rows, color) => {
    if (!rows.length) { el.innerHTML = `<div class="mut small" style="padding:14px">لا بيانات في هذه الفترة.</div>`; return; }
    const max = Math.max(...rows.map(r => r.value)) || 1;
    el.innerHTML = `<div class="bars">` + rows.map(r => `
      <div class="row">
        <span title="${esc(r.label)}">${esc(r.label)}</span>
        <span class="track"><i style="width:${Math.max(3, (r.value / max) * 100)}%${color ? `;background:${color}` : ""}"></i></span>
        <span class="v">${esc(r.display ?? num(r.value))}</span>
      </div>`).join("") + `</div>`;
  };

  const donut = (el, rows) => {
    const total = rows.reduce((s, r) => s + r.value, 0) || 1;
    const R = 60, C = 2 * Math.PI * R;
    let off = 0;
    const arcs = rows.map(r => {
      const len = (r.value / total) * C;
      const seg = `<circle cx="75" cy="75" r="${R}" fill="none" stroke="${r.color}" stroke-width="22"
        stroke-dasharray="${len} ${C - len}" stroke-dashoffset="${-off}" transform="rotate(-90 75 75)"><title>${esc(r.label)}: ${r.value}</title></circle>`;
      off += len; return seg;
    }).join("");
    el.innerHTML = `<div class="donutwrap">
      <svg class="donut" viewBox="0 0 150 150">${arcs}
        <text x="75" y="72" text-anchor="middle" font-size="21" font-weight="800" fill="#8E1B5B">${total}</text>
        <text x="75" y="90" text-anchor="middle" font-size="10" fill="#7a6c80">شحنة</text></svg>
      <div class="dlegend">${rows.map(r => `<div><span class="dot" style="background:${r.color}"></span>${esc(r.label)}
        <b style="color:#8E1B5B">${r.value}</b> <span class="mut">(${pct(r.value / total * 100)})</span></div>`).join("")}</div></div>`;
  };

  /* ================= لوحة التحكم ================= */
  let range = 30;
  const inRange = (list, d) => {
    const from = Date.now() - d * 86400000;
    return list.filter(s => new Date(s.createdAt) >= from);
  };
  const trend = (now, prev) => {
    if (!prev) return `<span class="trend flat">—</span>`;
    const p = ((now - prev) / prev) * 100;
    const cls = Math.abs(p) < 1 ? "flat" : p > 0 ? "up" : "down";
    return `<span class="trend ${cls}">${p > 0 ? "▲" : p < 0 ? "▼" : "—"} ${Math.abs(Math.round(p))}٪</span>`;
  };

  const renderDashboard = () => {
    const all = db.shipments;
    const cur = inRange(all, range);
    const prevFrom = Date.now() - range * 2 * 86400000, prevTo = Date.now() - range * 86400000;
    const prev = all.filter(s => { const t = new Date(s.createdAt); return t >= prevFrom && t < prevTo; });

    const by = (l, st) => l.filter(s => s.status === st).length;
    const cost = (l) => l.reduce((a, s) => a + s.cost, 0);
    const delivered = cur.filter(s => s.status === "delivered");
    const avgDays = delivered.length ? delivered.reduce((a, s) => a + days(s.createdAt, s.deliveredAt), 0) / delivered.length : 0;
    const onTime = delivered.filter(s => new Date(s.deliveredAt) <= new Date(s.promisedAt)).length;

    /* تحتاج انتباهك */
    const attn = [
      { k: "delayed", n: all.filter(s => s.isDelayed).length, t: "شحنات متأخرة", h: "تجاوزت الموعد الموعود" },
      { k: "failed_attempt", n: all.filter(s => s.status === "failed_attempt").length, t: "فشل تسليم", h: "تحتاج إعادة جدولة", warn: true },
      { k: "stale", n: all.filter(s => s.isStale).length, t: "بلا تحديث ٧٢ ساعة", h: "صمت في التتبع", warn: true },
      { k: "carrier_error", n: all.filter(s => s.status === "carrier_error").length, t: "فشل إرسال للشركة", h: "لم تصل لنظام الشركة" },
    ].filter(a => a.n > 0);
    $("#dashAttn").innerHTML = attn.length
      ? attn.map(a => `<button data-attn="${a.k}" class="${a.warn ? "warn" : ""}">
          <div class="n">${a.n}</div><div class="t">${a.t}</div><div class="h">${a.h}</div></button>`).join("")
      : `<div class="alert ok" style="grid-column:1/-1">✅ لا شيء يحتاج تدخلك الآن — كل الشحنات ضمن المسار الطبيعي.</div>`;

    /* مؤشرات التشغيل */
    const tile = (lbl, val, sub, cls) =>
      `<div class="stat ${cls || ""}"><div class="lbl">${lbl}</div><div class="val">${val}</div><div class="sub">${sub || ""}</div></div>`;
    $("#dashOps").innerHTML =
      tile("إجمالي الشحنات", num(cur.length), trend(cur.length, prev.length) + ` مقابل ${num(prev.length)}`) +
      tile("جديدة / قيد الإنشاء", num(by(cur, "created") + by(cur, "pending_carrier")), "بانتظار الاستلام") +
      tile("قيد الاستلام", num(by(cur, "picked_up")), "استلمتها الشركة") +
      tile("أثناء النقل", num(by(cur, "in_transit")), "في الطريق") +
      tile("خرجت للتسليم", num(by(cur, "out_for_delivery")), "مع المندوب") +
      tile("تم التسليم", num(by(cur, "delivered")), pct(cur.length ? by(cur, "delivered") / cur.length * 100 : 0) + " من الفترة", "good") +
      tile("تم الإرجاع", num(by(cur, "returned")), pct(cur.length ? by(cur, "returned") / cur.length * 100 : 0), "bad") +
      tile("فشل التسليم", num(by(cur, "failed_attempt")), "محاولات فاشلة", "bad");

    /* مؤشرات مالية وأداء */
    const bestC = carrierScores(cur)[0];
    $("#dashFin").innerHTML =
      tile("إجمالي تكلفة الشحن", OMR(cost(cur)), trend(cost(cur), cost(prev))) +
      tile("متوسط تكلفة الشحنة", OMR(cur.length ? cost(cur) / cur.length : 0), "لكل شحنة") +
      tile("متوسط مدة التوصيل", (Math.round(avgDays * 10) / 10) + " يوم", `${delivered.length} شحنة مسلّمة`) +
      tile("التسليم في الموعد", pct(delivered.length ? onTime / delivered.length * 100 : 0), "من المسلَّم", "good") +
      tile("تحصيل COD معلّق", OMR(cur.filter(s => s.isCod && s.status !== "delivered" && !ST[s.status].terminal).reduce((a, s) => a + s.codAmount, 0)), "لم يُحصَّل بعد", "warn") +
      tile("أفضل شركة شحن", bestC ? esc(S.carrier(bestC.code).name) : "—", bestC ? `تقييم مركّب ${bestC.score}` : "لا بيانات");

    /* رسوم */
    const buckets = {};
    cur.forEach(s => { const k = dOnly(s.createdAt); (buckets[k] = buckets[k] || { n: 0, c: 0 }).n++; buckets[k].c += s.cost; });
    const keys = Object.keys(buckets).sort();
    const step = range <= 7 ? 1 : range <= 30 ? 2 : 6;   // ~١٥ نقطة مهما كانت الفترة
    const pts = keys.filter((_, i) => i % step === 0);
    HMT.lineChart($("#chartVolume"), [
      { label: "عدد الشحنات", color: "#8E1B5B", points: pts.map(k => ({ x: k.slice(5), y: buckets[k].n })) },
    ]);
    HMT.lineChart($("#chartCost"), [
      { label: "تكلفة الشحن (ر.ع)", color: "#F2A03D", points: pts.map(k => ({ x: k.slice(5), y: Math.round(buckets[k].c * 100) / 100 })) },
    ]);

    const cities = {};
    cur.forEach(s => cities[s.wilayat] = (cities[s.wilayat] || 0) + 1);
    barChart($("#chartCities"), Object.entries(cities).sort((a, b) => b[1] - a[1]).slice(0, 10)
      .map(([label, value]) => ({ label, value })));

    const dist = S.CARRIERS.map(c => ({ label: c.name, color: c.color, value: cur.filter(s => s.carrier === c.code).length }))
      .filter(r => r.value > 0);
    donut($("#chartCarriers"), dist);
  };

  /* تقييم مركّب لشركات الشحن */
  const carrierScores = (list) => S.CARRIERS.map(c => {
    const mine = list.filter(s => s.carrier === c.code);
    const done = mine.filter(s => s.status === "delivered");
    const ret = mine.filter(s => s.status === "returned").length;
    const late = done.filter(s => new Date(s.deliveredAt) > new Date(s.promisedAt)).length;
    const avg = done.length ? done.reduce((a, s) => a + days(s.createdAt, s.deliveredAt), 0) / done.length : 0;
    const costAvg = mine.length ? mine.reduce((a, s) => a + s.cost, 0) / mine.length : 0;
    /* النجاح يُقاس على الشحنات المنتهية فقط (سُلّمت أو أُرجعت) — الشحنات في الطريق ليست فشلاً */
    const concluded = done.length + ret;
    const success = concluded ? done.length / concluded * 100 : 0;
    const ontime = done.length ? (done.length - late) / done.length * 100 : 0;
    const score = mine.length ? Math.round((success * 0.4 + ontime * 0.4 + Math.max(0, 100 - avg * 12) * 0.2) * 10) / 10 : 0;
    return { code: c.code, count: mine.length, delivered: done.length, returned: ret, late, avg, costAvg, success, ontime, score,
      spend: mine.reduce((a, s) => a + s.cost, 0), variance: mine.reduce((a, s) => a + (s.cost - s.quotedCost), 0) };
  }).filter(r => r.count > 0).sort((a, b) => b.score - a.score);

  /* ================= جدول الشحنات ================= */
  const F = { q: "", quick: "all", status: "", carrier: "", gov: "", sort: "createdAt", dir: -1, limit: 25 };
  const sel = new Set();

  const filtered = () => {
    let l = db.shipments.slice();
    if (F.quick === "attention") l = l.filter(s => s.isDelayed || s.isStale || ST[s.status].attention);
    if (F.quick === "today") l = l.filter(s => dOnly(s.createdAt) === HMT.todayKey());
    if (F.quick === "delayed") l = l.filter(s => s.isDelayed);
    if (F.quick === "stale") l = l.filter(s => s.isStale);
    if (F.quick === "cod") l = l.filter(s => s.isCod);
    if (F.quick === "open") l = l.filter(s => !ST[s.status].terminal);
    if (F.quick === "failed_attempt") l = l.filter(s => s.status === "failed_attempt");
    if (F.quick === "carrier_error") l = l.filter(s => s.status === "carrier_error");
    if (F.status) l = l.filter(s => s.status === F.status);
    if (F.carrier) l = l.filter(s => s.carrier === F.carrier);
    if (F.gov) l = l.filter(s => s.gov === F.gov);
    if (F.q) {
      const q = F.q.trim().toLowerCase();
      l = l.filter(s => [s.ref, s.orderNo, s.tracking, s.customer, s.phone, s.wilayat].join(" ").toLowerCase().includes(q));
    }
    const k = F.sort;
    l.sort((a, b) => {
      let x = a[k], y = b[k];
      if (k === "status") { x = ST[a.status].ar; y = ST[b.status].ar; }
      if (k === "carrier") { x = S.carrier(a.carrier).name; y = S.carrier(b.carrier).name; }
      if (typeof x === "number") return (x - y) * F.dir;
      return String(x).localeCompare(String(y), "ar") * F.dir;
    });
    return l;
  };

  const renderShipments = () => {
    const l = filtered(), shown = l.slice(0, F.limit);
    const counts = {
      all: db.shipments.length,
      attention: db.shipments.filter(s => s.isDelayed || s.isStale || ST[s.status].attention).length,
      today: db.shipments.filter(s => dOnly(s.createdAt) === HMT.todayKey()).length,
      open: db.shipments.filter(s => !ST[s.status].terminal).length,
      delayed: db.shipments.filter(s => s.isDelayed).length,
      cod: db.shipments.filter(s => s.isCod).length,
    };
    $("#shipChips").innerHTML = [
      ["all", "الكل"], ["attention", "تحتاج انتباهك"], ["open", "قيد التنفيذ"],
      ["today", "اليوم"], ["delayed", "متأخرة"], ["cod", "الدفع عند الاستلام"],
    ].map(([k, t]) => `<button class="chip ${F.quick === k ? "on" : ""}" data-quick="${k}">${t}<span class="n">${counts[k] ?? 0}</span></button>`).join("");

    const th = (k, t) => `<th class="sortable" data-sort="${k}">${t} <span class="ar">${F.sort === k ? (F.dir === 1 ? "▲" : "▼") : ""}</span></th>`;
    $("#shipTable").innerHTML = shown.length ? `
      <tr>
        <th style="width:26px"><input type="checkbox" class="rowsel" id="selAll"></th>
        ${th("ref", "المرجع")}${th("orderNo", "الطلب")}<th>رقم التتبع</th>${th("carrier", "الشركة")}
        ${th("customer", "العميل")}${th("wilayat", "الولاية")}${th("createdAt", "الإنشاء")}
        ${th("status", "الحالة")}${th("updatedAt", "آخر تحديث")}${th("cost", "التكلفة")}
      </tr>` + shown.map(s => `
      <tr class="clickable" data-open="${s.id}">
        <td><input type="checkbox" class="rowsel" data-sel="${s.id}" ${sel.has(s.id) ? "checked" : ""}></td>
        <td data-l="المرجع" class="num small">${s.ref}</td>
        <td data-l="الطلب" class="num small">${s.orderNo}</td>
        <td data-l="رقم التتبع" class="num"><span class="copyable" data-copy="${s.tracking}">${s.tracking}</span></td>
        <td data-l="الشركة">${cname(s.carrier)}</td>
        <td data-l="العميل">${esc(s.customer)}</td>
        <td data-l="الولاية">${esc(s.wilayat)}<div class="mut small">${esc(s.gov)}</div></td>
        <td data-l="الإنشاء" class="num small">${dOnly(s.createdAt)}</td>
        <td data-l="الحالة">${badge(s.status)}${s.isDelayed ? ` <span class="badge b-red">متأخرة</span>` : ""}${s.isStale ? ` <span class="badge b-amber">صامتة</span>` : ""}</td>
        <td data-l="آخر تحديث" class="small mut">${rel(s.updatedAt)}</td>
        <td data-l="التكلفة" class="num"><b>${OMR(s.cost)}</b>${s.isCod ? `<div class="mut small">تحصيل ${OMR(s.codAmount)}</div>` : ""}</td>
      </tr>`).join("")
      : `<tr><td class="mut" style="padding:26px;text-align:center">لا نتائج${F.q ? ` لـ «${esc(F.q)}»` : ""}. <button class="btn sm o" id="clearF">مسح الفلاتر</button></td></tr>`;

    $("#shipCount").innerHTML = `عرض <b>${Math.min(F.limit, l.length)}</b> من <b>${l.length}</b> شحنة`;
    $("#moreWrap").innerHTML = l.length > F.limit ? `<button class="btn o" id="moreBtn">تحميل المزيد (${l.length - F.limit})</button>` : "";
    renderBulk();
  };

  const renderBulk = () => {
    const el = $("#bulkBar");
    if (!sel.size) { el.style.display = "none"; return; }
    el.style.display = "flex";
    el.innerHTML = `<span class="cnt">${sel.size} شحنة محدّدة</span>
      <button class="btn sm" data-bulk="labels">🖨 طباعة البوالص</button>
      <button class="btn sm" data-bulk="pickup">📮 جدولة استلام</button>
      <button class="btn sm" data-bulk="export">⬇️ تصدير</button>
      <button class="btn sm o" data-bulk="clear" style="background:transparent;color:#fff;border-color:rgba(255,255,255,.5)">إلغاء التحديد</button>`;
  };

  /* ================= تفاصيل الشحنة ================= */
  const openShipment = (id) => {
    const s = db.shipments.find(x => x.id === id);
    if (!s) return;
    const c = S.carrier(s.carrier), cur = ST[s.status].stage;
    const bad = ["failed_attempt", "exception", "returning", "returned", "carrier_error"].includes(s.status);

    const stages = S.STAGES.map((t, i) => {
      const n = i + 1;
      let cls = n < cur ? "done" : n === cur ? (bad ? "bad" : "now") : "";
      if (s.status === "delivered" && n <= 5) cls = "done";
      return `<div class="s ${cls}"><span class="dot">${n < cur || s.status === "delivered" ? "✓" : n}</span><span class="cap">${t}</span></div>`;
    }).join("");

    const tl = s.events.slice().reverse().map(e => {
      const k = e.status === "delivered" ? "ok" : ["failed_attempt", "exception", "returning", "returned", "carrier_error"].includes(e.status) ? "bad" : "";
      const srcAr = { webhook: "تحديث تلقائي", polling: "مزامنة", manual: "يدوي", system: "النظام" }[e.source] || e.source;
      return `<div class="ev ${k}"><div class="h">${esc(e.text)}</div>
        <div class="m">${dTime(e.at)} · ${esc(e.location)} <span class="src">${srcAr}</span></div></div>`;
    }).join("");

    const variance = s.cost - s.quotedCost;
    $("#drawerBody").innerHTML = `
      <div class="card">
        <div style="display:flex;align-items:center;gap:9px;flex-wrap:wrap">
          ${badge(s.status)}${s.isDelayed ? `<span class="badge b-red">متأخرة</span>` : ""}${s.isStale ? `<span class="badge b-amber">صامتة</span>` : ""}
          <span class="mut small" style="margin-inline-start:auto">${rel(s.updatedAt)}</span>
        </div>
        <div style="margin-top:10px;font-size:13.5px">
          رقم التتبع: <b class="copyable" data-copy="${s.tracking}" style="direction:ltr;display:inline-block">${s.tracking}</b>
        </div>
        <div class="stages" style="margin-top:12px">${stages}</div>
        <div class="row" style="display:flex;gap:7px;flex-wrap:wrap">
          <button class="btn sm" data-act="sync">🔄 تحديث الآن</button>
          <button class="btn sm o" data-act="label">🖨 بوليصة الشحن</button>
          <button class="btn sm o" data-act="notify">📤 إرسال التتبع للعميل</button>
          ${ST[s.status].terminal ? "" : `<button class="btn sm danger" data-act="cancel" data-id="${s.id}">✕ إلغاء الشحنة</button>`}
        </div>
      </div>

      <div class="card"><h3><span class="ic">🕒</span> السجل الزمني</h3><div class="tline">${tl}</div>
        <button class="btn sm o" data-act="manual" data-id="${s.id}">➕ تسجيل حدث يدوي</button></div>

      <div class="card"><h3><span class="ic">👤</span> بيانات المستلم</h3>
        <dl class="dl">
          <dt>الاسم</dt><dd>${esc(s.customer)}</dd>
          <dt>الهاتف</dt><dd style="direction:ltr">${esc(s.phone)}</dd>
          <dt>المحافظة</dt><dd>${esc(s.gov)}</dd>
          <dt>الولاية</dt><dd>${esc(s.wilayat)}</dd>
          <dt>العنوان</dt><dd>${esc(s.street)}</dd>
        </dl></div>

      <div class="card"><h3><span class="ic">🚚</span> الشحن</h3>
        <dl class="dl">
          <dt>الشركة</dt><dd>${cname(s.carrier)}</dd>
          <dt>الخدمة</dt><dd>${esc(s.serviceName)}</dd>
          <dt>الطلب</dt><dd>${s.orderNo}</dd>
          <dt>الوزن</dt><dd>${s.weight} كجم · ${s.pieces} قطعة</dd>
          <dt>الوعد بالتسليم</dt><dd>${dOnly(s.promisedAt)}</dd>
          ${s.deliveredAt ? `<dt>تاريخ التسليم</dt><dd>${dTime(s.deliveredAt)}</dd>` : ""}
        </dl></div>

      <div class="card"><h3><span class="ic">💰</span> التكلفة</h3>
        <dl class="dl">
          <dt>السعر المُسعّر</dt><dd>${OMR(s.quotedCost)}</dd>
          <dt>التكلفة الفعلية</dt><dd>${OMR(s.cost)}</dd>
          <dt>الفرق</dt><dd style="color:${variance > 0.001 ? "var(--red)" : "var(--green)"}">${variance > 0.001 ? "+" : ""}${OMR(variance)}</dd>
          <dt>الدفع</dt><dd>${s.isCod ? `عند الاستلام — ${OMR(s.codAmount)}` : "مدفوع مسبقاً"}</dd>
        </dl>
        ${variance > 0.001 ? `<div class="alert warn small" style="margin-bottom:0">⚠️ التكلفة الفعلية تجاوزت المُسعّر — يظهر هذا الفرق في تقرير مطابقة الفواتير.</div>` : ""}
      </div>`;
    $("#drawerTitle").textContent = s.ref;
    $("#drawer").classList.add("on"); $("#scrim").classList.add("on");
  };
  const closeDrawer = () => { $("#drawer").classList.remove("on"); $("#scrim").classList.remove("on"); };

  /* ================= معالج إنشاء شحنة ================= */
  const W = { step: 1, data: {}, quotes: [], picked: null };

  const renderWizard = () => {
    $("#wSteps").innerHTML = [["١", "البيانات"], ["٢", "اختيار الشركة"], ["٣", "التأكيد"]]
      .map((s, i) => `<div class="w ${W.step === i + 1 ? "on" : W.step > i + 1 ? "ok" : ""}"><div class="n">الخطوة ${s[0]}</div><div class="t">${s[1]}</div></div>`).join("");
    $$("#tabCreate .wpane").forEach((p, i) => p.style.display = (i + 1 === W.step) ? "block" : "none");
  };

  const fillWilayats = () => {
    const g = $("#fGov").value;
    $("#fWilayat").innerHTML = (S.GEO[g] || []).map(w => `<option>${w}</option>`).join("");
  };

  const volumetric = () => {
    const l = +$("#fLen").value || 0, w = +$("#fWid").value || 0, h = +$("#fHei").value || 0;
    const vol = (l * w * h) / 5000;
    const actual = +$("#fWeight").value || 0;
    const bill = Math.max(vol, actual);
    $("#volHint").innerHTML = vol > 0
      ? `الوزن الحجمي <b>${(Math.round(vol * 100) / 100)} كجم</b> · الوزن المحتسب للفوترة <b style="color:var(--maroon)">${Math.round(bill * 100) / 100} كجم</b>`
      : `أدخل الأبعاد ليُحسب الوزن الحجمي — الشركات تسعّر بالأكبر من الوزنين.`;
    return bill;
  };

  const buildQuotes = (d) => {
    const remote = S.REMOTE.includes(d.gov);
    const out = [];
    S.CARRIERS.forEach(c => {
      const a = acc(c.code);
      if (!a || !a.active || !a.connected) return out.push({ code: c.code, off: "الحساب غير مفعّل" });
      if (a.status === "failed") return out.push({ code: c.code, off: "تعذّر الاتصال — بيانات الاعتماد مرفوضة" });
      if (!a.zones.includes(d.gov)) return out.push({ code: c.code, off: `لا تغطي ${d.gov}` });
      c.services.forEach(svc => {
        const base = svc.base + Math.max(0, d.bill - 1) * 0.25 + (remote ? 0.9 : 0) + (d.pieces - 1) * 0.4;
        const codFee = d.isCod ? Math.max(0.3, d.value * 0.01) : 0;
        const price = S.round3(base + codFee);
        const dmin = svc.days[0] + (remote ? 1 : 0), dmax = svc.days[1] + (remote ? 2 : 0);
        const pr = c.perf;
        const score = Math.round((pr.success * 0.35 + pr.ontime * 0.35 + Math.max(0, 100 - dmax * 14) * 0.15 + Math.max(0, 100 - price * 11) * 0.15) * 10) / 10;
        out.push({ code: c.code, svc: svc.code, svcName: svc.name, price, dmin, dmax, score, perf: pr, feat: c.feat });
      });
    });
    const ok = out.filter(q => !q.off).sort((a, b) => b.score - a.score);
    if (ok[0]) ok[0].best = true;
    return { ok, off: out.filter(q => q.off) };
  };

  const renderQuotes = () => {
    const box = $("#quotes");
    box.innerHTML = `<div class="skel"></div><div class="skel"></div><div class="skel"></div>`;
    setTimeout(() => {
      const { ok, off } = buildQuotes(W.data);
      W.quotes = ok;
      const cheapest = ok.length ? Math.min(...ok.map(q => q.price)) : 0;
      box.innerHTML = ok.map((q, i) => {
        const c = S.carrier(q.code);
        return `<div class="rate ${W.picked === i ? "on" : ""}" data-q="${i}">
          <div class="top">${clogo(q.code)}<span class="nm">${esc(c.name)} — ${esc(q.svcName)}</span>
            ${q.best ? `<span class="best">⭐ الأنسب</span>` : q.price === cheapest ? `<span class="best" style="background:var(--green-bg);color:var(--green)">الأرخص</span>` : ""}</div>
          <div style="display:flex;align-items:baseline;gap:12px;flex-wrap:wrap">
            <span class="price">${OMR(q.price)}</span>
            <span class="eta">${q.dmin === 0 ? "نفس اليوم" : `${q.dmin}–${q.dmax} يوم عمل`}</span>
            ${q.price > cheapest ? `<span class="mut small">+${OMR(q.price - cheapest)} عن الأرخص</span>` : ""}
          </div>
          <div class="perf">نجاح ${pct(q.perf.success)} · في الموعد ${pct(q.perf.ontime)} · تقييم ${q.perf.rating} · تقييم مركّب ${q.score}</div>
          <div class="feat">${q.feat.map(f => `<span>✓ ${esc(f)}</span>`).join("")}</div>
        </div>`;
      }).join("") + (off.length ? `<div class="card" style="background:#faf8fb">
        <div class="mut small" style="font-weight:800;margin-bottom:6px">غير متاحة لهذه الشحنة</div>
        ${off.map(q => `<div class="small mut">• ${esc(S.carrier(q.code).name)} — ${esc(q.off)}</div>`).join("")}
        <div class="small mut" style="margin-top:6px">تُعرض الأسباب صراحة بدل إخفاء الشركة — المستخدم يحتاج أن يعرف السبب.</div></div>` : "");
      if (!ok.length) box.innerHTML = `<div class="alert danger">تعذّر جلب أي سعر لهذه الوجهة. <button class="btn sm" id="retryQ">إعادة المحاولة</button></div>`;
    }, 550);
  };

  const createShipment = () => {
    const q = W.quotes[W.picked], d = W.data, c = S.carrier(q.code);
    const now = new Date().toISOString();
    const s = {
      id: "n" + Date.now(),
      ref: "SHP-2026-" + String(db.shipments.length + 1001).padStart(6, "0"),
      orderNo: d.orderNo || "ORD-" + (49000 + db.shipments.length),
      carrier: q.code, service: q.svc, serviceName: q.svcName,
      tracking: c.pre + String(90000000 + Math.floor(Math.random() * 9999999)),
      customer: d.name, phone: d.phone, gov: d.gov, wilayat: d.wilayat, street: d.street, area: "", landmark: d.landmark,
      createdAt: now, updatedAt: now,
      promisedAt: new Date(Date.now() + q.dmax * 86400000).toISOString(),
      status: "created", weight: d.weight, pieces: d.pieces, declaredValue: d.value,
      isCod: d.isCod, codAmount: d.isCod ? d.value : 0,
      quotedCost: q.price, cost: q.price, notes: d.notes, deliveredAt: null, isDelayed: false, isStale: false,
      events: [{ status: "created", text: "تم إنشاء الشحنة وإصدار بوليصة الشحن", location: "متجرلينك", at: now, source: "system" }],
    };
    db.shipments.unshift(s); save();
    $("#wDone").innerHTML = `
      <div class="alert ok"><b>✅ تم إنشاء الشحنة بنجاح</b> — حُفظ رقم التتبع داخل الطلب ${esc(s.orderNo)} تلقائياً.</div>
      <div class="grid g2">
        <div class="card"><h3><span class="ic">📦</span> ${s.ref}</h3>
          <dl class="dl">
            <dt>رقم التتبع</dt><dd class="copyable" data-copy="${s.tracking}" style="direction:ltr">${s.tracking}</dd>
            <dt>الشركة</dt><dd>${cname(s.carrier)}</dd>
            <dt>الخدمة</dt><dd>${esc(s.serviceName)}</dd>
            <dt>التكلفة</dt><dd><b>${OMR(s.cost)}</b></dd>
            <dt>الوعد بالتسليم</dt><dd>${dOnly(s.promisedAt)}</dd>
          </dl>
          <div class="row" style="display:flex;gap:7px;flex-wrap:wrap;margin-top:10px">
            <button class="btn sm" data-act="label">🖨 طباعة البوليصة</button>
            <button class="btn sm o" data-act="notify">📤 إرسال التتبع للعميل</button>
            <button class="btn sm o" data-open="${s.id}">فتح الشحنة</button>
          </div></div>
        <div class="card"><h3><span class="ic">🔁</span> الخطوة التالية</h3>
          <p class="small mut">في النظام الحقيقي تُرسل الآن رسالة واتساب للعميل برابط تتبع بعلامة المتجر، وتتحدّث حالة الطلب تلقائياً مع كل حدث من شركة الشحن.</p>
          <button class="btn" id="wAgain">➕ إنشاء شحنة أخرى</button></div>
      </div>`;
    W.step = 4; renderWizard();
    $("#wDone").style.display = "block";
    renderDashboard(); renderShipments();
    HMT.toast("✅ تم إنشاء الشحنة");
  };

  /* ================= شركات الشحن ================= */
  const renderCarriers = () => {
    $("#carrierGrid").innerHTML = S.CARRIERS.map(c => {
      const a = acc(c.code);
      const mine = db.shipments.filter(s => s.carrier === c.code);
      const done = mine.filter(s => s.status === "delivered").length;
      const st = a.status === "connected" ? `<span class="st ok">● متصل</span>`
              : a.status === "failed" ? `<span class="st no">● فشل الاتصال</span>`
              : `<span class="st na">○ غير مربوط</span>`;
      return `<div class="ccard ${a.active ? "" : "dim"}">
        <div class="ch">${clogo(c.code)}<span class="nm">${esc(c.name)}</span>${a.isDefault ? `<span class="deftag">افتراضية</span>` : ""}${st}</div>
        <div class="meta">${c.api ? "تكامل API" : "إدارة يدوية (بلا API)"} · ${esc(c.scope)} · ${a.zones.length} محافظة مغطاة</div>
        <div class="meta">${num(mine.length)} شحنة · تسليم ${done ? pct(done / mine.length * 100) : "—"} · آخر فحص ${rel(a.checkedAt)}</div>
        ${a.error ? `<div class="alert danger small" style="margin:2px 0">${esc(a.error)}</div>` : ""}
        ${c.api ? `<div class="meta">مفتاح API: <b style="direction:ltr;display:inline-block">${a.key || "—"}</b></div>` : ""}
        <div class="row">
          <button class="btn sm o" data-test="${c.code}">🔌 اختبار الاتصال</button>
          ${a.isDefault ? "" : `<button class="btn sm o" data-def="${c.code}">⭐ اجعلها الافتراضية</button>`}
          <label class="sw" style="margin-inline-start:auto">
            <input type="checkbox" data-toggle="${c.code}" ${a.active ? "checked" : ""}><span class="tr"></span>
            <span class="small mut">${a.active ? "مفعّلة" : "معطّلة"}</span></label>
        </div>
      </div>`;
    }).join("");
  };

  /* ================= التقارير ================= */
  const renderReports = () => {
    const cur = inRange(db.shipments, range);
    const rows = carrierScores(cur);

    $("#repCarriers").innerHTML = `
      <tr><th>الشركة</th><th>الشحنات</th><th>نسبة النجاح</th><th>في الموعد</th><th>متوسط المدة</th><th>الإرجاع</th><th>متوسط التكلفة</th><th>الإنفاق</th><th>التقييم المركّب</th></tr>` +
      (rows.length ? rows.map(r => `<tr>
        <td>${cname(r.code)}</td>
        <td class="num">${num(r.count)}</td>
        <td class="num">${pct(r.success)}</td>
        <td class="num">${pct(r.ontime)}</td>
        <td class="num">${(Math.round(r.avg * 10) / 10) || "—"} يوم</td>
        <td class="num">${pct(r.count ? r.returned / r.count * 100 : 0)}</td>
        <td class="num">${OMR(r.costAvg)}</td>
        <td class="num"><b>${OMR(r.spend)}</b></td>
        <td><b style="color:var(--maroon)">${r.score}</b></td></tr>`).join("")
      : `<tr><td colspan="9" class="mut">لا بيانات في هذه الفترة.</td></tr>`);

    const cities = {}, custs = {}, months = {};
    cur.forEach(s => {
      cities[s.wilayat] = (cities[s.wilayat] || 0) + 1;
      (custs[s.customer] = custs[s.customer] || { n: 0, c: 0 }).n++; custs[s.customer].c += s.cost;
      const m = s.createdAt.slice(0, 7);
      (months[m] = months[m] || { n: 0, c: 0 }).n++; months[m].c += s.cost;
    });
    barChart($("#repCities"), Object.entries(cities).sort((a, b) => b[1] - a[1]).slice(0, 10).map(([label, value]) => ({ label, value })));
    barChart($("#repCost"), Object.entries(months).sort().map(([label, v]) => ({ label, value: Math.round(v.c * 1000) / 1000, display: OMR(v.c) })), "linear-gradient(90deg,#1f9d6b,#F2A03D)");

    $("#repCustomers").innerHTML = `<tr><th>العميل</th><th>الشحنات</th><th>إجمالي الشحن</th></tr>` +
      Object.entries(custs).sort((a, b) => b[1].n - a[1].n).slice(0, 10)
        .map(([k, v]) => `<tr><td>${esc(k)}</td><td class="num">${v.n}</td><td class="num">${OMR(v.c)}</td></tr>`).join("");

    const done = cur.filter(s => s.status === "delivered");
    const late = done.filter(s => new Date(s.deliveredAt) > new Date(s.promisedAt)).length;
    const ret = cur.filter(s => s.status === "returned").length;
    const variance = cur.reduce((a, s) => a + (s.cost - s.quotedCost), 0);
    const varCount = cur.filter(s => s.cost - s.quotedCost > 0.001).length;
    $("#repSummary").innerHTML = `
      <div class="stat"><div class="lbl">عدد الشحنات</div><div class="val">${num(cur.length)}</div></div>
      <div class="stat"><div class="lbl">إجمالي مصروفات الشحن</div><div class="val">${OMR(cur.reduce((a, s) => a + s.cost, 0))}</div></div>
      <div class="stat ${late / (done.length || 1) > 0.15 ? "bad" : "good"}"><div class="lbl">نسبة التأخير</div><div class="val">${pct(done.length ? late / done.length * 100 : 0)}</div><div class="sub">${late} من ${done.length} مسلّمة</div></div>
      <div class="stat ${ret / (cur.length || 1) > 0.07 ? "bad" : ""}"><div class="lbl">نسبة الإرجاع</div><div class="val">${pct(cur.length ? ret / cur.length * 100 : 0)}</div><div class="sub">${ret} شحنة</div></div>
      <div class="stat warn"><div class="lbl">فروقات الفواتير</div><div class="val">${OMR(variance)}</div><div class="sub">${varCount} شحنة فُوترت أعلى من المُسعّر</div></div>
      <div class="stat"><div class="lbl">تحصيل COD</div><div class="val">${OMR(cur.filter(s => s.isCod && s.status === "delivered").reduce((a, s) => a + s.codAmount, 0))}</div><div class="sub">محصّل ومكتمل</div></div>`;
  };

  /* ================= تصدير ================= */
  const exportCsv = (list) => {
    const head = ["المرجع", "الطلب", "رقم التتبع", "الشركة", "الخدمة", "العميل", "الهاتف", "المحافظة", "الولاية",
      "تاريخ الإنشاء", "الحالة", "آخر تحديث", "الوزن", "القطع", "التكلفة", "الدفع عند الاستلام"];
    const rows = list.map(s => [s.ref, s.orderNo, s.tracking, S.carrier(s.carrier).name, s.serviceName, s.customer, s.phone,
      s.gov, s.wilayat, dOnly(s.createdAt), ST[s.status].ar, dOnly(s.updatedAt), s.weight, s.pieces, s.cost, s.isCod ? s.codAmount : 0]);
    const csv = "﻿" + [head, ...rows].map(r => r.map(v => `"${String(v).replace(/"/g, '""')}"`).join(",")).join("\n");
    const url = URL.createObjectURL(new Blob([csv], { type: "text/csv;charset=utf-8" }));
    const a = document.createElement("a");
    a.href = url; a.download = `shipments-${HMT.todayKey()}.csv`; a.click();
    URL.revokeObjectURL(url);
    HMT.toast(`⬇️ صُدّرت ${list.length} شحنة`);
  };

  /* ================= الربط ================= */
  const renderAll = () => { renderDashboard(); renderShipments(); renderCarriers(); renderReports(); };

  const bind = () => {
    /* الفترة */
    $$("[data-range]").forEach(b => b.addEventListener("click", () => {
      range = +b.dataset.range;
      $$("[data-range]").forEach(x => x.classList.toggle("on", x === b));
      renderDashboard(); renderReports();
    }));

    /* تفويض الأحداث على مستوى الصفحة */
    document.addEventListener("click", (e) => {
      const t = e.target;

      const copy = t.closest("[data-copy]");
      if (copy) { navigator.clipboard?.writeText(copy.dataset.copy); HMT.toast("📋 نُسخ: " + copy.dataset.copy); return; }

      const attn = t.closest("[data-attn]");
      if (attn) { goShipments(attn.dataset.attn); return; }

      const quick = t.closest("[data-quick]");
      if (quick) { F.quick = quick.dataset.quick; F.limit = 25; renderShipments(); return; }

      const sort = t.closest("[data-sort]");
      if (sort) { const k = sort.dataset.sort; F.dir = F.sort === k ? -F.dir : -1; F.sort = k; renderShipments(); return; }

      if (t.id === "selAll") return;
      const cb = t.closest("[data-sel]");
      if (cb) { e.stopPropagation(); cb.checked ? sel.add(cb.dataset.sel) : sel.delete(cb.dataset.sel); renderBulk(); return; }

      const open = t.closest("[data-open]");
      if (open) { openShipment(open.dataset.open); return; }

      const bulk = t.closest("[data-bulk]");
      if (bulk) {
        const list = db.shipments.filter(s => sel.has(s.id));
        const k = bulk.dataset.bulk;
        if (k === "export") exportCsv(list);
        else if (k === "labels") HMT.toast(`🖨 دُمجت ${list.length} بوليصة في ملف PDF واحد (محاكاة)`);
        else if (k === "pickup") HMT.toast(`📮 جُدول استلام لـ ${list.length} شحنة (محاكاة)`);
        else { sel.clear(); renderShipments(); }
        return;
      }

      const test = t.closest("[data-test]");
      if (test) {
        const a = acc(test.dataset.test);
        test.textContent = "⏳ جارٍ الفحص…"; test.disabled = true;
        setTimeout(() => {
          const ok = a.code !== "smsa";
          a.status = ok ? "connected" : "failed";
          a.connected = ok;
          a.error = ok ? "" : "بيانات الاعتماد مرفوضة (401) — يلزم تحديث المفتاح";
          a.checkedAt = new Date().toISOString();
          save(); renderCarriers();
          HMT.toast(ok ? "✅ الاتصال ناجح" : "❌ فشل الاتصال — راجع المفتاح");
        }, 900);
        return;
      }

      const def = t.closest("[data-def]");
      if (def) { db.accounts.forEach(a => a.isDefault = a.code === def.dataset.def); save(); renderCarriers(); HMT.toast("⭐ حُدّدت الشركة الافتراضية"); return; }

      const act = t.closest("[data-act]");
      if (act) {
        const k = act.dataset.act;
        if (k === "sync") HMT.toast("🔄 طُلب تحديث فوري من شركة الشحن (محاكاة)");
        if (k === "label") window.print();
        if (k === "notify") HMT.toast("📤 أُرسل رابط التتبع للعميل عبر واتساب (محاكاة)");
        if (k === "cancel") {
          const s = db.shipments.find(x => x.id === act.dataset.id);
          if (s && confirm(`إلغاء الشحنة ${s.ref}؟ سيُطلب الإلغاء من شركة الشحن أيضاً.`)) {
            s.status = "cancelled"; s.isDelayed = false; s.isStale = false; s.updatedAt = new Date().toISOString();
            s.events.push({ status: "cancelled", text: "أُلغيت الشحنة بواسطة المستخدم", location: "متجرلينك", at: s.updatedAt, source: "manual" });
            save(); openShipment(s.id); renderAll(); HMT.toast("✕ أُلغيت الشحنة");
          }
        }
        if (k === "manual") {
          const s = db.shipments.find(x => x.id === act.dataset.id);
          const txt = prompt("وصف الحدث (مثال: اتصلت بالشركة وأكدت الاستلام):");
          if (s && txt) {
            const at = new Date().toISOString();
            s.events.push({ status: s.status, text: txt, location: "—", at, source: "manual" });
            s.updatedAt = at; s.isStale = false;
            save(); openShipment(s.id); renderShipments(); HMT.toast("✅ سُجّل الحدث");
          }
        }
        return;
      }

      if (t.id === "clearF") { F.q = ""; F.quick = "all"; F.status = ""; F.carrier = ""; F.gov = ""; $("#shipSearch").value = ""; $("#fStatus").value = ""; $("#fCarrier").value = ""; $("#fGovF").value = ""; renderShipments(); }
      if (t.id === "moreBtn") { F.limit += 25; renderShipments(); }
      if (t.id === "wAgain") { W.step = 1; W.picked = null; $("#wDone").style.display = "none"; renderWizard(); }
      if (t.id === "retryQ") renderQuotes();
    });

    /* تحديد الكل */
    document.addEventListener("change", (e) => {
      if (e.target.id === "selAll") {
        const on = e.target.checked;
        filtered().slice(0, F.limit).forEach(s => on ? sel.add(s.id) : sel.delete(s.id));
        renderShipments();
      }
      const tg = e.target.closest("[data-toggle]");
      if (tg) { const a = acc(tg.dataset.toggle); a.active = tg.checked; save(); renderCarriers(); }
    });

    /* الإغلاق */
    $("#scrim").addEventListener("click", closeDrawer);
    $("#drawerClose").addEventListener("click", closeDrawer);
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape") closeDrawer();
      if (e.key === "/" && document.activeElement.tagName !== "INPUT" && document.activeElement.tagName !== "TEXTAREA") {
        e.preventDefault(); goShipments(); $("#shipSearch").focus();
      }
    });

    /* الفلاتر */
    let deb;
    $("#shipSearch").addEventListener("input", (e) => { clearTimeout(deb); deb = setTimeout(() => { F.q = e.target.value; F.limit = 25; renderShipments(); }, 180); });
    ["fStatus", "fCarrier", "fGovF"].forEach(id => $("#" + id).addEventListener("change", () => {
      F.status = $("#fStatus").value; F.carrier = $("#fCarrier").value; F.gov = $("#fGovF").value;
      F.limit = 25; renderShipments();
    }));
    $("#exportBtn").addEventListener("click", () => exportCsv(filtered()));
    $("#printBtn").addEventListener("click", () => window.print());
    $("#resetBtn").addEventListener("click", () => { if (confirm("إعادة توليد البيانات التجريبية من جديد؟")) { sel.clear(); reset(); } });

    /* المعالج */
    $("#fGov").addEventListener("change", fillWilayats);
    ["fWeight", "fLen", "fWid", "fHei"].forEach(id => $("#" + id).addEventListener("input", volumetric));
    $("#toStep2").addEventListener("click", () => {
      const d = {
        name: $("#fName").value.trim(), phone: $("#fPhone").value.trim(), gov: $("#fGov").value,
        wilayat: $("#fWilayat").value, street: $("#fStreet").value.trim(), landmark: $("#fLandmark").value.trim(),
        weight: +$("#fWeight").value || 0, pieces: +$("#fPieces").value || 1, value: +$("#fValue").value || 0,
        isCod: $("#fCod").checked, notes: $("#fNotes").value.trim(), orderNo: $("#fOrder").value.trim(),
        bill: volumetric(),
      };
      if (!d.name || !d.phone) return HMT.toast("أدخل اسم المستلم ورقم هاتفه");
      if (!d.weight) return HMT.toast("أدخل وزن الطرد");
      W.data = d; W.picked = null; W.step = 2; renderWizard(); renderQuotes();
    });
    $("#backTo1").addEventListener("click", () => { W.step = 1; renderWizard(); });
    $("#backTo2").addEventListener("click", () => { W.step = 2; renderWizard(); renderQuotes(); });
    $("#quotes").addEventListener("click", (e) => {
      const q = e.target.closest("[data-q]");
      if (!q) return;
      W.picked = +q.dataset.q;
      $$("#quotes .rate").forEach(r => r.classList.toggle("on", r === q));
      $("#toStep3").disabled = false;
    });
    $("#toStep3").addEventListener("click", () => {
      if (W.picked == null) return HMT.toast("اختر شركة الشحن أولاً");
      const q = W.quotes[W.picked], d = W.data;
      $("#confirmBox").innerHTML = `
        <div class="grid g2">
          <div class="card"><h3><span class="ic">👤</span> المستلم</h3><dl class="dl">
            <dt>الاسم</dt><dd>${esc(d.name)}</dd><dt>الهاتف</dt><dd style="direction:ltr">${esc(d.phone)}</dd>
            <dt>الوجهة</dt><dd>${esc(d.wilayat)} — ${esc(d.gov)}</dd>
            <dt>العنوان</dt><dd>${esc(d.street) || "—"}</dd></dl></div>
          <div class="card"><h3><span class="ic">📦</span> الطرد والشحن</h3><dl class="dl">
            <dt>الوزن المحتسب</dt><dd>${Math.round(d.bill * 100) / 100} كجم (${d.pieces} قطعة)</dd>
            <dt>الشركة</dt><dd>${cname(q.code)}</dd>
            <dt>الخدمة</dt><dd>${esc(q.svcName)} · ${q.dmin === 0 ? "نفس اليوم" : `${q.dmin}–${q.dmax} يوم`}</dd>
            <dt>الدفع</dt><dd>${d.isCod ? `عند الاستلام — ${OMR(d.value)}` : "مدفوع مسبقاً"}</dd>
            <dt>التكلفة</dt><dd><b style="font-size:16px;color:var(--maroon)">${OMR(q.price)}</b></dd></dl></div>
        </div>`;
      W.step = 3; renderWizard();
    });
    $("#confirmBtn").addEventListener("click", (e) => { e.target.disabled = true; createShipment(); setTimeout(() => e.target.disabled = false, 800); });
  };

  const goShipments = (quick) => {
    const btn = $('[data-tab="tabShipments"]');
    btn.click();
    if (quick) { F.quick = ["delayed", "stale", "failed_attempt", "carrier_error"].includes(quick) ? quick : "attention"; F.limit = 25; renderShipments(); }
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  /* ================= التشغيل ================= */
  const init = () => {
    load();
    /* تعبئة القوائم */
    $("#fCarrier").innerHTML = `<option value="">كل الشركات</option>` + S.CARRIERS.map(c => `<option value="${c.code}">${c.name}</option>`).join("");
    $("#fStatus").innerHTML = `<option value="">كل الحالات</option>` + Object.entries(ST).map(([k, v]) => `<option value="${k}">${v.ar}</option>`).join("");
    $("#fGovF").innerHTML = `<option value="">كل المحافظات</option>` + S.GOVS.map(g => `<option>${g}</option>`).join("");
    $("#fGov").innerHTML = S.GOVS.map(g => `<option>${g}</option>`).join("");
    fillWilayats(); volumetric(); renderWizard();
    bind(); renderAll();
  };

  return { init, reset };
})();
