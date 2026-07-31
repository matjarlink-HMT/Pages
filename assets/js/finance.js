/* ================= القسم المالي ================= */
(() => {
  HMT.renderHeader("finance.html");
  HMT.initTabs("#finRoot");

  const OMR = (n) => (Math.round(n * 1000) / 1000).toLocaleString("en", { maximumFractionDigits: 3 }) + " ر.ع";
  const getFin = () => HMT.get("finance", { base: {}, fixed: [], debts: [], expenses: [], payments: [] });
  const setFin = (f) => HMT.set("finance", f);

  /* ========== البيانات الأساسية ========== */
  const loadBase = () => {
    const f = getFin();
    ["fSalary","fBizIncome","fOtherIncome","fSavings"].forEach(id => {
      const key = id.slice(1).charAt(0).toLowerCase() + id.slice(2);
      document.getElementById(id).value = f.base?.[key] ?? "";
    });
    renderFixed();
  };
  const renderFixed = () => {
    const f = getFin();
    document.getElementById("fixedList").innerHTML = (f.fixed || []).map((x, i) =>
      `<div style="display:flex;justify-content:space-between;align-items:center;padding:6px 10px;border-bottom:1px solid var(--line)">
        <span>${HMT.esc(x.name)}</span>
        <span><b>${OMR(x.amount)}</b> <button class="btn sm danger" data-delfix="${i}" style="margin-inline-start:8px">✕</button></span>
      </div>`).join("") || `<div class="mut small" style="padding:8px">لا التزامات مسجلة بعد.</div>`;
    document.querySelectorAll("[data-delfix]").forEach(b => b.addEventListener("click", () => {
      const f2 = getFin(); f2.fixed.splice(+b.dataset.delfix, 1); setFin(f2); renderFixed(); renderOverview();
    }));
  };
  document.getElementById("addFixed").addEventListener("click", () => {
    const name = document.getElementById("fixName").value.trim();
    const amt = +document.getElementById("fixAmt").value;
    if (!name || !amt) return HMT.toast("أدخل البند والمبلغ");
    const f = getFin(); f.fixed = f.fixed || []; f.fixed.push({ name, amount: amt }); setFin(f);
    document.getElementById("fixName").value = ""; document.getElementById("fixAmt").value = "";
    renderFixed(); renderOverview();
  });
  document.getElementById("saveFinBase").addEventListener("click", () => {
    const f = getFin();
    f.base = {
      salary: +document.getElementById("fSalary").value || 0,
      bizIncome: +document.getElementById("fBizIncome").value || 0,
      otherIncome: +document.getElementById("fOtherIncome").value || 0,
      savings: +document.getElementById("fSavings").value || 0,
    };
    setFin(f); renderOverview(); HMT.toast("✅ تم حفظ البيانات الأساسية");
  });

  /* ========== الديون ========== */
  document.getElementById("addDebt").addEventListener("click", () => {
    const d = {
      name: document.getElementById("dName").value.trim(),
      balance: +document.getElementById("dBalance").value || 0,
      payment: +document.getElementById("dPayment").value || 0,
      rate: +document.getElementById("dRate").value || 0,
      due: +document.getElementById("dDue").value || null,
    };
    if (!d.name || !d.balance) return HMT.toast("أدخل الجهة والمبلغ على الأقل");
    const f = getFin(); f.debts = f.debts || [];
    const idx = f.debts.findIndex(x => x.name === d.name);
    if (idx >= 0) f.debts[idx] = { ...f.debts[idx], ...d }; else f.debts.push(d);
    setFin(f);
    ["dName","dBalance","dPayment","dRate","dDue"].forEach(id => document.getElementById(id).value = "");
    renderDebts(); renderOverview(); HMT.toast("✅ تم حفظ الدين");
  });

  const renderDebts = () => {
    const f = getFin();
    const debts = f.debts || [];
    document.getElementById("debtsTable").innerHTML =
      `<tr><th>الجهة</th><th>المتبقي</th><th>القسط</th><th>الفائدة</th><th>الاستحقاق</th><th></th></tr>` +
      (debts.length ? debts.map((d, i) =>
        `<tr><td><b>${HMT.esc(d.name)}</b></td><td>${OMR(d.balance)}</td><td>${OMR(d.payment)}</td>
        <td>${d.rate}%</td><td>${d.due ? "يوم " + d.due : "—"}</td>
        <td><button class="btn sm danger" data-deldebt="${i}">✕</button></td></tr>`).join("")
      : `<tr><td colspan="6" class="mut">لا ديون مسجلة. أضف كل دين حتى يبني المستشار خطة السداد.</td></tr>`);
    document.querySelectorAll("[data-deldebt]").forEach(b => b.addEventListener("click", () => {
      if (!confirm("حذف هذا الدين نهائيًا؟")) return;
      const f2 = getFin(); f2.debts.splice(+b.dataset.deldebt, 1); setFin(f2);
      renderDebts(); renderOverview();
    }));
    // قائمة الدفع
    document.getElementById("payDebtSel").innerHTML =
      debts.map((d, i) => `<option value="${i}">${HMT.esc(d.name)} (${OMR(d.balance)})</option>`).join("") || `<option value="">—</option>`;
    renderPayoff();
  };

  document.getElementById("payDebt").addEventListener("click", () => {
    const f = getFin();
    const i = +document.getElementById("payDebtSel").value;
    const amt = +document.getElementById("payAmt").value;
    if (isNaN(i) || !f.debts?.[i] || !amt) return HMT.toast("اختر الدين وأدخل المبلغ");
    f.debts[i].balance = Math.max(0, f.debts[i].balance - amt);
    f.payments = f.payments || [];
    f.payments.push({ date: HMT.todayKey(), debt: f.debts[i].name, amount: amt });
    if (f.debts[i].balance === 0) HMT.toast(`🎉 مبروك! أنهيت دين ${f.debts[i].name} بالكامل!`);
    else HMT.toast("✅ تم تسجيل الدفعة");
    setFin(f);
    document.getElementById("payAmt").value = "";
    renderDebts(); renderOverview();
  });

  /* --- محاكاة خطة السداد --- */
  let strategy = "avalanche";
  document.querySelectorAll("[data-strategy]").forEach(b => b.addEventListener("click", () => {
    document.querySelectorAll("[data-strategy]").forEach(x => x.classList.remove("active"));
    b.classList.add("active");
    strategy = b.dataset.strategy;
    renderPayoff();
  }));
  document.getElementById("extraPay").addEventListener("input", () => renderPayoff());

  const renderPayoff = () => {
    const f = getFin();
    const el = document.getElementById("payoffPlan");
    let debts = (f.debts || []).filter(d => d.balance > 0).map(d => ({ ...d }));
    if (!debts.length) { el.innerHTML = `<div class="mut small">أضف ديونك أولًا لعرض الخطة.</div>`; return; }
    const extra = +document.getElementById("extraPay").value || 0;
    debts.sort(strategy === "avalanche" ? (a, b) => b.rate - a.rate : (a, b) => a.balance - b.balance);

    // محاكاة شهرية (حد 240 شهر)
    let months = 0, totalInterest = 0;
    const order = [];
    const sim = debts.map(d => ({ ...d }));
    while (sim.some(d => d.balance > 0) && months < 240) {
      months++;
      let freed = extra + sim.filter(d => d.balance <= 0).reduce((s, d) => s + d.payment, 0);
      for (const d of sim) {
        if (d.balance <= 0) continue;
        const interest = d.balance * (d.rate / 100 / 12);
        totalInterest += interest;
        d.balance += interest;
        let pay = d.payment;
        // المبلغ الإضافي كله لأول دين نشط بالترتيب
        const firstActive = sim.find(x => x.balance > 0);
        if (d === firstActive) { pay += freed; freed = 0; }
        d.balance = Math.max(0, d.balance - pay);
        if (d.balance === 0 && !order.find(o => o.name === d.name)) order.push({ name: d.name, month: months });
      }
    }
    const yrs = Math.floor(months / 12), rem = months % 12;
    el.innerHTML = `
      <div class="stat" style="margin-bottom:8px"><div class="lbl">مدة التحرر من الديون (بهذه الخطة)</div>
        <div class="val">${yrs ? yrs + " سنة " : ""}${rem ? rem + " شهر" : ""}</div>
        <div class="sub">إجمالي الفوائد المتوقعة: ${OMR(totalInterest)}</div></div>
      <div class="small"><b>ترتيب الإغلاق:</b></div>
      <ol class="small" style="margin:4px 0;padding-inline-start:20px">
        ${order.map(o => `<li>${HMT.esc(o.name)} — الشهر ${o.month}</li>`).join("")}
      </ol>
      <div class="mut small">القاعدة: سدد الحد الأدنى للجميع + كل مبلغ إضافي يذهب ${strategy === "avalanche" ? "للدين ذي الفائدة الأعلى" : "لأصغر دين"} حتى يُغلق، ثم ينتقل قسطه للتالي.</div>`;
  };

  /* ========== المصاريف ========== */
  document.getElementById("expDate").value = HMT.todayKey();
  document.getElementById("addExp").addEventListener("click", () => {
    const e = {
      date: document.getElementById("expDate").value,
      cat: document.getElementById("expCat").value,
      amount: +document.getElementById("expAmt").value,
      note: document.getElementById("expNote").value,
    };
    if (!e.date || !e.amount) return HMT.toast("أدخل التاريخ والمبلغ");
    const f = getFin(); f.expenses = f.expenses || []; f.expenses.push(e); setFin(f);
    document.getElementById("expAmt").value = ""; document.getElementById("expNote").value = "";
    renderExpenses(); renderOverview(); HMT.toast("✅ تم التسجيل");
  });

  const renderExpenses = () => {
    const f = getFin();
    const ym = HMT.todayKey().slice(0, 7);
    const monthExp = (f.expenses || []).filter(e => e.date.startsWith(ym));
    const byCat = {};
    monthExp.forEach(e => byCat[e.cat] = (byCat[e.cat] || 0) + e.amount);
    const total = monthExp.reduce((s, e) => s + e.amount, 0);
    document.getElementById("monthSummary").innerHTML =
      `<div class="stat" style="margin-bottom:10px"><div class="lbl">إجمالي مصاريف الشهر المتغيرة</div><div class="val">${OMR(total)}</div></div>` +
      Object.entries(byCat).sort((a, b) => b[1] - a[1]).map(([c, v]) => {
        const pct = total ? Math.round(v / total * 100) : 0;
        return `<div style="margin-bottom:6px"><div style="display:flex;justify-content:space-between" class="small"><span>${c}</span><b>${OMR(v)} (${pct}%)</b></div>
          <div class="pbar"><i style="width:${pct}%"></i></div></div>`;
      }).join("") || `<div class="mut small">لا مصاريف هذا الشهر بعد.</div>`;

    document.getElementById("expTable").innerHTML =
      `<tr><th>التاريخ</th><th>الفئة</th><th>المبلغ</th><th>ملاحظة</th><th></th></tr>` +
      (monthExp.length ? monthExp.slice().reverse().map((e) => {
        const gi = f.expenses.indexOf(e);
        return `<tr><td>${e.date}</td><td>${e.cat}</td><td><b>${OMR(e.amount)}</b></td><td class="small">${HMT.esc(e.note || "")}</td>
          <td><button class="btn sm danger" data-delexp="${gi}">✕</button></td></tr>`;
      }).join("") : `<tr><td colspan="5" class="mut">لا مصاريف مسجلة هذا الشهر.</td></tr>`);
    document.querySelectorAll("[data-delexp]").forEach(b => b.addEventListener("click", () => {
      const f2 = getFin(); f2.expenses.splice(+b.dataset.delexp, 1); setFin(f2);
      renderExpenses(); renderOverview();
    }));
  };

  /* ========== النظرة العامة ========== */
  const renderOverview = () => {
    const f = getFin();
    const hasData = f.base?.salary || (f.debts || []).length;
    document.getElementById("finEmpty").innerHTML = hasData ? "" :
      `<div class="alert warn">⚠️ القسم المالي فارغ. ابدأ بتبويب <b>"البيانات الأساسية"</b> لتسجيل دخلك والتزاماتك، ثم أضف ديونك — أو افتح <b>المستشار المالي</b> واكتب له "ابدأ المقابلة المالية" وسيجمع كل شيء منك خطوة بخطوة.</div>`;

    const income = (f.base?.salary || 0) + (f.base?.bizIncome || 0) + (f.base?.otherIncome || 0);
    const fixedTotal = (f.fixed || []).reduce((s, x) => s + x.amount, 0);
    const debtsTotal = (f.debts || []).reduce((s, d) => s + d.balance, 0);
    const paymentsTotal = (f.debts || []).filter(d => d.balance > 0).reduce((s, d) => s + d.payment, 0);
    const ym = HMT.todayKey().slice(0, 7);
    const monthVar = (f.expenses || []).filter(e => e.date.startsWith(ym)).reduce((s, e) => s + e.amount, 0);
    const free = income - fixedTotal - paymentsTotal - monthVar;

    document.getElementById("finStats").innerHTML = `
      <div class="stat"><div class="lbl">الدخل الشهري</div><div class="val">${OMR(income)}</div></div>
      <div class="stat ${debtsTotal > 0 ? "bad" : "good"}"><div class="lbl">إجمالي الديون</div><div class="val">${OMR(debtsTotal)}</div><div class="sub">أقساط شهرية: ${OMR(paymentsTotal)}</div></div>
      <div class="stat"><div class="lbl">التزامات ثابتة</div><div class="val">${OMR(fixedTotal)}</div></div>
      <div class="stat ${free >= 0 ? "good" : "bad"}"><div class="lbl">المتبقي هذا الشهر</div><div class="val">${OMR(free)}</div><div class="sub">بعد الثابت والأقساط والمصاريف</div></div>`;

    document.getElementById("ovDebtsTable").innerHTML =
      `<tr><th>الجهة</th><th>المتبقي</th><th>القسط</th><th>الفائدة</th></tr>` +
      ((f.debts || []).length ? f.debts.map(d =>
        `<tr><td><b>${HMT.esc(d.name)}</b></td><td>${OMR(d.balance)}</td><td>${OMR(d.payment)}</td><td>${d.rate}%</td></tr>`).join("")
      : `<tr><td colspan="4" class="mut">لا ديون مسجلة بعد.</td></tr>`);

    document.getElementById("ovFixed").innerHTML = (f.fixed || []).length
      ? f.fixed.map(x => `<div style="display:flex;justify-content:space-between;padding:5px 0;border-bottom:1px solid var(--line)"><span class="small">${HMT.esc(x.name)}</span><b class="small">${OMR(x.amount)}</b></div>`).join("")
      : `<div class="mut small">لا التزامات مسجلة.</div>`;

    document.getElementById("ovCalc").innerHTML = `
      <div class="small" style="line-height:2.2">
        الدخل: <b style="color:var(--green)">+${OMR(income)}</b><br>
        الالتزامات الثابتة: <b style="color:var(--red)">−${OMR(fixedTotal)}</b><br>
        أقساط الديون: <b style="color:var(--red)">−${OMR(paymentsTotal)}</b><br>
        مصاريف الشهر المتغيرة: <b style="color:var(--red)">−${OMR(monthVar)}</b>
        <hr class="soft">
        المتاح: <b style="color:${free >= 0 ? "var(--green)" : "var(--red)"}">${OMR(free)}</b>
      </div>`;
  };

  loadBase();
  renderDebts();
  renderExpenses();
  renderOverview();

  /* ========== المستشار ========== */
  Advisor.mount("financeAdvisor", "finance", {
    icon: "💰",
    name: "المستشار المالي",
    desc: "تخطيط مالي · إدارة ديون · ميزانيات — يقرأ بياناتك المالية المسجلة",
    welcome: "أهلًا إبراهيم. أنا مستشارك المالي. هدفنا واضح: إنهاء ديونك وبناء ميزانية محكمة. إذا عندك وقت الآن اكتب \"ابدأ المقابلة المالية\" وسأجمع منك كل التفاصيل سؤالًا سؤالًا. أو اسأل مباشرة عن أي قرار مالي.",
  });
})();
