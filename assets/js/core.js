/* ================= HMT OS — النواة المشتركة ================= */
const HMT = (() => {
  const PREFIX = "hmtos_";

  /* ---------- التخزين ---------- */
  const get = (key, fallback = null) => {
    try {
      const raw = localStorage.getItem(PREFIX + key);
      return raw === null ? fallback : JSON.parse(raw);
    } catch { return fallback; }
  };
  const set = (key, val) => localStorage.setItem(PREFIX + key, JSON.stringify(val));
  const del = (key) => localStorage.removeItem(PREFIX + key);
  const allKeys = () => Object.keys(localStorage).filter(k => k.startsWith(PREFIX)).map(k => k.slice(PREFIX.length));

  const exportAll = () => {
    const out = {};
    allKeys().forEach(k => out[k] = get(k));
    return JSON.stringify({ app: "HMT-OS", version: 1, exportedAt: new Date().toISOString(), data: out }, null, 2);
  };
  const importAll = (json) => {
    const parsed = JSON.parse(json);
    if (!parsed || !parsed.data) throw new Error("ملف غير صالح");
    Object.entries(parsed.data).forEach(([k, v]) => set(k, v));
  };

  /* ---------- التاريخ ---------- */
  const DAYS = ["الأحد","الاثنين","الثلاثاء","الأربعاء","الخميس","الجمعة","السبت"];
  const todayKey = () => new Date().toISOString().slice(0, 10);
  const fmtDate = (d) => {
    const dt = typeof d === "string" ? new Date(d + "T12:00:00") : d;
    return `${DAYS[dt.getDay()]} ${dt.getDate()}/${dt.getMonth() + 1}/${dt.getFullYear()}`;
  };
  const isTrainingDay = (d = new Date()) => (window.HMT_SEED?.workouts.trainingDays || [1,4]).includes(d.getDay());
  const isWorkDay = (d = new Date()) => d.getDay() >= 0 && d.getDay() <= 4;
  const daysBetween = (a, b) => Math.round((new Date(b) - new Date(a)) / 86400000);

  /* ---------- Toast ---------- */
  const toast = (msg) => {
    let t = document.getElementById("toast");
    if (!t) { t = document.createElement("div"); t.id = "toast"; document.body.appendChild(t); }
    t.textContent = msg;
    t.classList.add("show");
    clearTimeout(t._h);
    t._h = setTimeout(() => t.classList.remove("show"), 2600);
  };

  /* ---------- Escape ---------- */
  const esc = (s) => String(s ?? "").replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));

  /* ---------- الهيدر والتنقل ---------- */
  const NAV = [
    { href: "index.html", label: "🏠 الرئيسية" },
    { href: "health.html", label: "❤️ الصحة" },
    { href: "finance.html", label: "💰 المالية" },
    { href: "matjarlink.html", label: "🛒 متجرلينك" },
    { href: "life.html", label: "🎯 الأهداف والعادات" },
    { href: "settings.html", label: "⚙️ الإعدادات" },
  ];
  const renderHeader = (active) => {
    const el = document.getElementById("siteHeader");
    if (!el) return;
    const today = fmtDate(new Date());
    el.innerHTML = `
      <div class="head-in">
        <div class="logo">🧭</div>
        <div>
          <h1>منصة إبراهيم — HMT OS</h1>
          <div class="sub">محرك القرارات: صحة · مال · متجرلينك</div>
        </div>
        <div class="head-side">${today}</div>
      </div>
      <nav class="main">
        ${NAV.map(n => `<a href="${n.href}" class="${n.href === active ? "active" : ""}">${n.label}</a>`).join("")}
      </nav>`;
  };

  /* ---------- Tabs ---------- */
  const initTabs = (containerSel) => {
    document.querySelectorAll(`${containerSel} .tabs button`).forEach(btn => {
      btn.addEventListener("click", () => {
        const c = btn.closest(containerSel);
        c.querySelectorAll(".tabs button").forEach(b => b.classList.remove("active"));
        c.querySelectorAll(":scope > .tabpane").forEach(p => p.classList.remove("show"));
        btn.classList.add("active");
        c.querySelector(`#${btn.dataset.tab}`)?.classList.add("show");
      });
    });
  };

  /* ---------- رسم بياني خطي SVG بسيط ---------- */
  const lineChart = (el, series, opts = {}) => {
    // series: [{label, color, points:[{x:label,y:num}]}]
    const W = opts.width || Math.max(el.clientWidth || 600, 320), H = opts.height || 220;
    const P = { t: 16, r: 14, b: 34, l: 40 };
    const all = series.flatMap(s => s.points.map(p => p.y)).filter(v => v != null);
    if (!all.length) { el.innerHTML = `<div class="mut" style="padding:20px;text-align:center">لا توجد بيانات بعد — سجّل أول قراءة.</div>`; return; }
    let min = Math.min(...all), max = Math.max(...all);
    if (min === max) { min -= 1; max += 1; }
    const pad = (max - min) * 0.12; min -= pad; max += pad;
    const n = Math.max(...series.map(s => s.points.length));
    const xs = i => P.l + (n === 1 ? (W - P.l - P.r) / 2 : i * (W - P.l - P.r) / (n - 1));
    const ys = v => P.t + (H - P.t - P.b) * (1 - (v - min) / (max - min));
    let g = "";
    // grid
    for (let i = 0; i <= 4; i++) {
      const v = min + (max - min) * i / 4, y = ys(v);
      g += `<line x1="${P.l}" y1="${y}" x2="${W - P.r}" y2="${y}" stroke="#ece2ee"/>` +
           `<text x="${P.l - 6}" y="${y + 4}" font-size="10" fill="#7a6c80" text-anchor="end">${v.toFixed(1)}</text>`;
    }
    series.forEach(s => {
      const pts = s.points.map((p, i) => p.y == null ? null : `${xs(i)},${ys(p.y)}`).filter(Boolean);
      if (pts.length > 1) g += `<polyline points="${pts.join(" ")}" fill="none" stroke="${s.color}" stroke-width="2.5" stroke-linejoin="round"/>`;
      s.points.forEach((p, i) => {
        if (p.y == null) return;
        g += `<circle cx="${xs(i)}" cy="${ys(p.y)}" r="4" fill="${s.color}"><title>${esc(p.x)}: ${p.y}</title></circle>`;
      });
    });
    // x labels (sparse)
    const step = Math.ceil(n / 8);
    (series[0]?.points || []).forEach((p, i) => {
      if (i % step === 0 || i === n - 1)
        g += `<text x="${xs(i)}" y="${H - 10}" font-size="10" fill="#7a6c80" text-anchor="middle">${esc(p.x)}</text>`;
    });
    // legend
    let lg = series.map((s, i) =>
      `<circle cx="${P.l + i * 110 + 5}" cy="${H - P.b + 26}" r="4" fill="${s.color}"/>` ).join("");
    el.innerHTML = `<svg viewBox="0 0 ${W} ${H}" width="100%" height="${H}" role="img">${g}</svg>` +
      `<div class="small" style="display:flex;gap:16px;justify-content:center">` +
      series.map(s => `<span><span style="color:${s.color}">●</span> ${esc(s.label)}</span>`).join("") + `</div>`;
  };

  return { get, set, del, allKeys, exportAll, importAll, todayKey, fmtDate, isTrainingDay, isWorkDay, daysBetween, toast, esc, renderHeader, initTabs, lineChart, DAYS };
})();
