/* ============================================================================
   UI — نواة صغيرة قائمة بذاتها للنموذج
   تخزين، إشعارات، تبويبات، رسم خطي، ومبدّل العرض.
   لا اعتماد على أي منصة أو مكتبة خارجية.
   ============================================================================ */

const UI = (() => {
  const PREFIX = "mjl_ship_";

  /* ---------- التخزين ----------
     بيئات المعاينة المعزولة قد تمنع localStorage، فيُستبدل بذاكرة الجلسة
     تلقائياً بدل أن ينهار النموذج. */
  const memory = new Map();
  const canPersist = (() => {
    try {
      const probe = PREFIX + "probe";
      localStorage.setItem(probe, "1");
      localStorage.removeItem(probe);
      return true;
    } catch { return false; }
  })();

  const get = (key, fallback = null) => {
    try {
      const raw = canPersist ? localStorage.getItem(PREFIX + key) : memory.get(key) ?? null;
      return raw === null || raw === undefined ? fallback : JSON.parse(raw);
    } catch { return fallback; }
  };

  const set = (key, val) => {
    const raw = JSON.stringify(val);
    try {
      if (canPersist) localStorage.setItem(PREFIX + key, raw);
      else memory.set(key, raw);
    } catch { memory.set(key, raw); }
  };

  /* ---------- التاريخ ---------- */
  const todayKey = () => {
    const d = new Date();
    return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
  };

  /* ---------- الهروب من HTML ---------- */
  const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) =>
    ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));

  /* ---------- إشعار ---------- */
  const toast = (msg) => {
    let t = document.getElementById("toast");
    if (!t) {
      t = document.createElement("div");
      t.id = "toast";
      t.setAttribute("role", "status");
      t.setAttribute("aria-live", "polite");
      document.body.appendChild(t);
    }
    t.textContent = msg;
    t.classList.add("show");
    clearTimeout(t._h);
    t._h = setTimeout(() => t.classList.remove("show"), 2600);
  };

  /* ---------- تبويبات ---------- */
  const initTabs = (containerSel) => {
    const root = document.querySelector(containerSel);
    if (!root) return;

    root.querySelectorAll(".tabs button").forEach((btn) => {
      btn.setAttribute("role", "tab");
      btn.addEventListener("click", () => {
        root.querySelectorAll(".tabs button").forEach((b) => {
          b.classList.toggle("active", b === btn);
          b.setAttribute("aria-selected", b === btn ? "true" : "false");
        });
        root.querySelectorAll(":scope > .tabpane").forEach((p) => p.classList.remove("show"));
        root.querySelector(`#${btn.dataset.tab}`)?.classList.add("show");
      });
    });
  };

  /* ---------- ألوان مشتقة من رموز التصميم ----------
     تُقرأ وقت الرسم لا وقت التحميل، فتتبع الرسوم وضع العرض الحالي. */
  const token = (name, fallback) => {
    const v = getComputedStyle(document.documentElement).getPropertyValue(name).trim();
    return v || fallback;
  };

  /* ---------- رسم خطي SVG ---------- */
  const lineChart = (el, series, opts = {}) => {
    if (!el) return;
    const W = opts.width || Math.max(el.clientWidth || 600, 320);
    const H = opts.height || 210;
    const P = { t: 14, r: 14, b: 34, l: 44 };

    const values = series.flatMap((s) => s.points.map((p) => p.y)).filter((v) => v != null);
    if (!values.length) {
      el.innerHTML = `<p class="mut" style="padding:20px;text-align:center">لا توجد بيانات في هذه الفترة.</p>`;
      return;
    }

    let min = Math.min(...values), max = Math.max(...values);
    if (min === max) { min -= 1; max += 1; }
    const pad = (max - min) * 0.12;
    min -= pad; max += pad;

    const n = Math.max(...series.map((s) => s.points.length));
    const xs = (i) => P.l + (n === 1 ? (W - P.l - P.r) / 2 : (i * (W - P.l - P.r)) / (n - 1));
    const ys = (v) => P.t + (H - P.t - P.b) * (1 - (v - min) / (max - min));

    const gridColor = token("--line", "#dce4ea");
    const textColor = token("--ink-soft", "#5a6b7b");

    let g = "";
    for (let i = 0; i <= 4; i++) {
      const v = min + ((max - min) * i) / 4;
      const y = ys(v);
      g += `<line x1="${P.l}" y1="${y}" x2="${W - P.r}" y2="${y}" stroke="${gridColor}"/>`;
      g += `<text x="${P.l - 7}" y="${y + 4}" font-size="10" fill="${textColor}" text-anchor="end">${
        Math.abs(v) >= 100 ? Math.round(v) : v.toFixed(1)}</text>`;
    }

    series.forEach((s) => {
      const pts = s.points.map((p, i) => (p.y == null ? null : `${xs(i)},${ys(p.y)}`)).filter(Boolean);
      if (pts.length > 1) {
        /* تعبئة خفيفة تحت الخط تجعل الاتجاه مقروءاً بلا قراءة الأرقام */
        g += `<polygon points="${pts.join(" ")} ${xs(s.points.length - 1)},${H - P.b} ${xs(0)},${H - P.b}"
              fill="${s.color}" opacity=".10"/>`;
        g += `<polyline points="${pts.join(" ")}" fill="none" stroke="${s.color}" stroke-width="2.4"
              stroke-linejoin="round" stroke-linecap="round"/>`;
      }
      s.points.forEach((p, i) => {
        if (p.y == null) return;
        const last = i === s.points.length - 1;
        g += `<circle cx="${xs(i)}" cy="${ys(p.y)}" r="${last ? 4.5 : 3}" fill="${s.color}"
              ${last ? `stroke="${token("--surface", "#fff")}" stroke-width="2"` : ""}>
              <title>${esc(p.x)}: ${p.y}</title></circle>`;
      });
    });

    const step = Math.max(1, Math.ceil(n / 8));
    (series[0]?.points || []).forEach((p, i) => {
      if (i % step === 0 || i === n - 1) {
        g += `<text x="${xs(i)}" y="${H - 12}" font-size="10" fill="${textColor}" text-anchor="middle">${esc(p.x)}</text>`;
      }
    });

    el.innerHTML =
      `<svg viewBox="0 0 ${W} ${H}" width="100%" height="${H}" role="img" aria-label="${esc(series[0]?.label || "")}">${g}</svg>` +
      `<p class="small mut" style="display:flex;gap:16px;justify-content:center;margin:2px 0 0">` +
      series.map((s) => `<span><span style="color:${s.color}">●</span> ${esc(s.label)}</span>`).join("") +
      `</p>`;
  };

  /* ---------- وضع العرض ---------- */
  const THEME_KEY = "theme";

  const applyTheme = (mode) => {
    if (mode === "auto") document.documentElement.removeAttribute("data-theme");
    else document.documentElement.setAttribute("data-theme", mode);
  };

  const currentTheme = () => get(THEME_KEY, "auto");

  const initTheme = (btnSel, onChange) => {
    applyTheme(currentTheme());

    const btn = document.querySelector(btnSel);
    if (!btn) return;

    const systemDark = () => matchMedia("(prefers-color-scheme: dark)").matches;
    const label = () => {
      const mode = currentTheme();
      const dark = mode === "dark" || (mode === "auto" && systemDark());
      btn.textContent = dark ? "☀" : "☾";
      btn.setAttribute("aria-label", dark ? "التبديل إلى الوضع الفاتح" : "التبديل إلى الوضع الداكن");
      btn.title = btn.getAttribute("aria-label");
    };

    btn.addEventListener("click", () => {
      const dark = currentTheme() === "dark" || (currentTheme() === "auto" && systemDark());
      const next = dark ? "light" : "dark";
      set(THEME_KEY, next);
      applyTheme(next);
      label();
      onChange?.();
    });

    matchMedia("(prefers-color-scheme: dark)").addEventListener("change", () => { label(); onChange?.(); });
    label();
  };

  return { get, set, todayKey, esc, toast, initTabs, lineChart, initTheme, canPersist };
})();
