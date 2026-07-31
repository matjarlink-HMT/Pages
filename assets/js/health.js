/* ================= قسم الصحة ================= */
(() => {
  const S = window.HMT_SEED;
  HMT.renderHeader("health.html");
  HMT.initTabs("#healthRoot");

  /* ========== 1) التقرير الصحي ========== */
  const latestWeekly = () => (HMT.get("weekly_logs", []).slice(-1)[0] || null);

  const ovStats = document.getElementById("ovStats");
  const lw = latestWeekly();
  const curW = lw?.weight ?? S.measurements.weight;
  const curWaist = lw?.waist ?? S.measurements.waist;
  const bmi = (curW / ((S.measurements.height / 100) ** 2)).toFixed(1);
  ovStats.innerHTML = `
    <div class="stat"><div class="lbl">الوزن الحالي</div><div class="val">${curW} كجم</div><div class="sub">البداية: ${S.measurements.weight} كجم</div></div>
    <div class="stat"><div class="lbl">الخصر</div><div class="val">${curWaist} سم</div><div class="sub">الهدف: ≤88 سم</div></div>
    <div class="stat warn"><div class="lbl">BMI</div><div class="val">${bmi}</div><div class="sub">الطبيعي: 18.5–24.9</div></div>
    <div class="stat warn"><div class="lbl">نسبة الدهون (تقديري)</div><div class="val">~${S.measurements.bodyFat}%</div><div class="sub">Navy method</div></div>`;

  // الأهداف
  const goalsEl = document.getElementById("ovGoals");
  document.getElementById("goalDeadline").textContent = `— حتى ${HMT.fmtDate(S.goals12w.deadline)}`;
  const currentFor = (key) => {
    if (key === "waist") return curWaist;
    if (key === "weight") return curW;
    if (key === "steps") return lw?.steps ?? S.goals12w.items.find(g => g.key === "steps").from;
    if (key === "sleep") return lw?.sleepScore ? null : null;
    return null;
  };
  goalsEl.innerHTML = S.goals12w.items.map(g => {
    const cur = currentFor(g.key);
    let pct = 0;
    if (cur != null) {
      pct = g.dir === "down"
        ? Math.max(0, Math.min(100, (g.from - cur) / (g.from - g.to) * 100))
        : Math.max(0, Math.min(100, (cur - g.from) / (g.to - g.from) * 100));
    }
    return `<div class="card">
      <div style="display:flex;justify-content:space-between;align-items:center">
        <b>${g.label}</b>
        <span class="badge ${pct >= 100 ? "b-green" : pct > 0 ? "b-amber" : "b-gray"}">${cur != null ? cur : "—"} / ${g.to} ${g.unit}</span>
      </div>
      <div class="pbar" style="margin-top:8px"><i style="width:${pct}%"></i></div>
      <div class="mut small" style="margin-top:4px">${Math.round(pct)}% من الهدف · البداية: ${g.from} ${g.unit}</div>
    </div>`;
  }).join("");

  // التحاليل
  const st = { high: '<span class="badge b-red">مرتفع</span>', low: '<span class="badge b-red">منخفض</span>', warn: '<span class="badge b-amber">حدّي</span>', ok: '<span class="badge b-green">طبيعي</span>' };
  document.getElementById("lipidsTable").innerHTML =
    `<tr><th>التحليل</th><th>النتيجة</th><th>المرجع</th><th>الحالة</th></tr>` +
    S.labs.lipids.map(l => `<tr><td>${l.name}</td><td><b>${l.val}</b> ${l.unit}</td><td>${l.ref}</td><td>${st[l.status]}</td></tr>`).join("");
  document.getElementById("metabolicNote").textContent = S.labs.metabolicNote;
  document.getElementById("otherLabs").innerHTML = S.labs.other.map(l =>
    `<div style="display:flex;justify-content:space-between;gap:8px;padding:5px 0;border-bottom:1px solid var(--line)">
      <span class="small">${l.name}</span><span class="small"><b>${l.val}</b> ${st[l.status]}</span></div>`).join("");
  document.getElementById("echoNote").textContent = S.labs.echo;
  document.getElementById("missingLabs").textContent = "ناقص ويُفحص لاحقًا: " + S.labs.missing;

  document.getElementById("ratingsCard").innerHTML = `<div class="grid g4">` +
    S.ratings.map(r => {
      const c = r.v >= 7 ? "var(--green)" : r.v >= 5 ? "var(--amber)" : "var(--red)";
      return `<div><div class="small" style="font-weight:700">${r.k}</div>
        <div style="display:flex;align-items:center;gap:8px">
          <div class="pbar" style="flex:1"><i style="width:${r.v * 10}%;background:${c}"></i></div>
          <b style="color:${c}">${r.v}</b></div></div>`;
    }).join("") + `</div>`;
  document.getElementById("safetyRule").textContent = S.safetyRule;

  /* ========== 2) المخطط اليومي ========== */
  const today = HMT.todayKey();
  const isTraining = HMT.isTrainingDay();
  document.getElementById("dayTitle").textContent = HMT.fmtDate(new Date());
  document.getElementById("dayHint").textContent = isTraining
    ? "🏋️ اليوم يوم تمرين مقاومة (17:00–18:00) — الخطة بالتبويب المجاور."
    : "اليوم بدون مقاومة — المشي والتصحيحي أساسيان.";

  const dayItems = S.daySchedule.filter(i => isTraining || i.key !== "gym");
  const dayStateKey = `day_${today}`;
  const renderDay = () => {
    const state = HMT.get(dayStateKey, {});
    document.getElementById("dayChecklist").innerHTML = dayItems.map(i => `
      <label class="chk ${state[i.key] ? "done" : ""}">
        <input type="checkbox" data-day="${i.key}" ${state[i.key] ? "checked" : ""}>
        <span class="time">${i.time}</span>
        <span class="txt">${i.txt}</span>
      </label>`).join("");
    const done = dayItems.filter(i => state[i.key]).length;
    const pct = Math.round(done / dayItems.length * 100);
    document.getElementById("dayPct").textContent = pct + "%";
    document.getElementById("dayPbar").style.width = pct + "%";
    document.querySelectorAll("[data-day]").forEach(cb => cb.addEventListener("change", () => {
      const s = HMT.get(dayStateKey, {});
      s[cb.dataset.day] = cb.checked;
      HMT.set(dayStateKey, s);
      renderDay();
    }));
  };
  renderDay();

  document.getElementById("mealsTable").innerHTML =
    S.nutrition.meals.map(m => `<tr><td style="white-space:nowrap"><b style="color:var(--orange)">${m.time}</b></td><td><b>${m.name}</b></td><td class="small">${m.desc}</td></tr>`).join("");
  document.getElementById("macros").innerHTML =
    `<b>الماكروز اليومية:</b> بروتين ${S.nutrition.protein}غ · دهون ~${S.nutrition.fat}غ · كارب ~${S.nutrition.carbs}غ · ألياف ${S.nutrition.fiber}غ · ماء ${S.nutrition.water}`;
  document.getElementById("nutriRules").innerHTML = S.nutrition.rules.map(r => `<li>${r}</li>`).join("");

  /* ========== 3) التمارين ========== */
  document.getElementById("workoutToday").innerHTML = isTraining
    ? `🏋️ <b>اليوم يوم تمرين!</b> الموعد 17:00–18:00. بدّل بين A وB (آخر خطة سجلتها: ${lastPlanUsed() || "لم تبدأ بعد — ابدأ بـ A"}).`
    : `اليوم راحة من المقاومة. أيام التمرين: <b>الاثنين والخميس</b> 17:00. لا تنسَ المشي والتصحيحي.`;

  function lastPlanUsed() {
    const logs = HMT.get("workout_logs", []);
    return logs.length ? logs[logs.length - 1].plan : null;
  }

  const planView = document.getElementById("planView");
  const renderPlan = (id) => {
    if (id === "home") {
      planView.innerHTML = `<div class="card"><h3><span class="ic">🏠</span> ${S.workouts.homeAlt.name}</h3>
        <div>${S.workouts.homeAlt.desc}</div>
        <div class="alert warn small" style="margin-top:8px">توصية: الاشتراك بجيم قريب من بيت صحار خلال شهر.</div></div>`;
      return;
    }
    if (id === "corrective") {
      planView.innerHTML = `<div class="card"><h3><span class="ic">🩹</span> ${S.workouts.corrective.name}</h3>
        <ol>${S.workouts.corrective.items.map(i => `<li>${i}</li>`).join("")}</ol>
        <div class="alert info small">الهدف: زوال ألم الأبهر الأيسر الناتج عن الجلوس الطويل. يوميًا الساعة 22:15.</div></div>`;
      return;
    }
    const p = S.workouts[id];
    planView.innerHTML = `
      <div class="card">
        <h3><span class="ic">🏋️</span> ${p.name}</h3>
        <div class="small mut">🔸 ${p.warmup} &nbsp;·&nbsp; 🔹 الختام: ${p.cooldown}</div>
        <div style="margin-top:12px">
        ${p.exercises.map(e => `
          <details class="excard">
            <summary>▸ ${e.name} <span class="meta">${e.sets} · ${e.muscle}</span></summary>
            <div class="body">
              <b>طريقة الأداء:</b>
              <ol>${e.how.map(h => `<li>${h}</li>`).join("")}</ol>
              <div class="cue">💡 ${e.cue}</div>
              <a href="${e.video}" target="_blank" rel="noopener" class="small">🎬 شاهد فيديو توضيحي للتمرين</a>
            </div>
          </details>`).join("")}
        </div>
      </div>`;
  };
  renderPlan("A");
  document.querySelectorAll("[data-wplan]").forEach(b => b.addEventListener("click", () => {
    document.querySelectorAll("[data-wplan]").forEach(x => x.classList.remove("active"));
    b.classList.add("active");
    renderPlan(b.dataset.wplan);
  }));

  /* --- تسجيل الجلسات --- */
  const sessionForm = document.getElementById("sessionForm");
  document.getElementById("startSession").addEventListener("click", () => {
    const plan = document.getElementById("logPlan").value;
    const exs = plan === "home"
      ? ["سكوات كأس", "اندفاع", "ضغط أرضي", "تجديف دمبل", "ضغط كتف", "بلانك"].map(n => ({ name: n }))
      : S.workouts[plan].exercises;
    sessionForm.innerHTML = `
      <div class="alert info small">سجّل الوزن (كجم) والتكرارات المنجزة لكل تمرين. اترك ما لم تنفذه فارغًا.</div>
      <div class="tblwrap"><table class="t">
        <tr><th>التمرين</th><th>الوزن</th><th>التكرارات (مثال: 10/10/9)</th></tr>
        ${exs.map((e, i) => `<tr><td>${e.name}</td>
          <td><input class="f" style="width:90px" type="number" step="0.5" data-sw="${i}"></td>
          <td><input class="f" style="width:140px" type="text" data-sr="${i}" placeholder="10/10/10"></td></tr>`).join("")}
      </table></div>
      <label class="f">ملاحظات الجلسة</label><input class="f" id="sNotes" placeholder="مثال: الأبهر أخف، زد الوزن القادم…">
      <button class="btn" id="saveSession" style="margin-top:10px">💾 حفظ الجلسة</button>`;
    document.getElementById("saveSession").addEventListener("click", () => {
      const entries = exs.map((e, i) => ({
        name: e.name,
        weight: sessionForm.querySelector(`[data-sw="${i}"]`).value || null,
        reps: sessionForm.querySelector(`[data-sr="${i}"]`).value || null,
      })).filter(e => e.weight || e.reps);
      if (!entries.length) return HMT.toast("لم تسجل أي تمرين");
      const logs = HMT.get("workout_logs", []);
      logs.push({ date: HMT.todayKey(), plan, entries, notes: document.getElementById("sNotes").value });
      HMT.set("workout_logs", logs);
      sessionForm.innerHTML = "";
      renderSessions();
      HMT.toast("✅ تم حفظ الجلسة");
    });
  });

  const renderSessions = () => {
    const logs = HMT.get("workout_logs", []).slice().reverse();
    document.getElementById("sessionsTable").innerHTML =
      `<tr><th>التاريخ</th><th>الخطة</th><th>التمارين</th><th>ملاحظات</th></tr>` +
      (logs.length ? logs.map(l =>
        `<tr><td style="white-space:nowrap">${HMT.fmtDate(l.date)}</td><td><span class="badge b-purple">${l.plan}</span></td>
        <td class="small">${l.entries.map(e => `${e.name}: ${e.weight ?? "-"}كجم ×${e.reps ?? "-"}`).join(" · ")}</td>
        <td class="small">${HMT.esc(l.notes || "")}</td></tr>`).join("")
      : `<tr><td colspan="4" class="mut">لا جلسات مسجلة بعد — سجل أول جلسة يوم الاثنين أو الخميس.</td></tr>`);
  };
  renderSessions();
  document.getElementById("progressionRule").textContent = S.workouts.progression;

  /* ========== 4) المكملات ========== */
  document.getElementById("suppDate").textContent = HMT.fmtDate(new Date());
  const zincDue = () => {
    // زنك يوم بعد يوم — نعتمد على آخر يوم أُخذ فيه
    const hist = HMT.get("supp_history", {});
    const days = Object.keys(hist).sort();
    for (let i = days.length - 1; i >= 0; i--) {
      if (hist[days[i]]?.zinc) return HMT.daysBetween(days[i], today) >= 2;
    }
    return true;
  };
  const suppKey = `supp_${today}`;
  const renderSupp = () => {
    const state = HMT.get(suppKey, {});
    const zinc = zincDue();
    document.getElementById("suppChecklist").innerHTML = S.supplements.map(s => {
      if (s.id === "zinc" && !zinc && !state.zinc)
        return `<div class="chk" style="opacity:.5;cursor:default"><span style="width:18px">⏸</span><span class="time"></span><span class="txt">${s.name} — ليس اليوم (يوم بعد يوم)</span></div>`;
      return `<label class="chk ${state[s.id] ? "done" : ""}">
        <input type="checkbox" data-supp="${s.id}" ${state[s.id] ? "checked" : ""}>
        <span class="txt"><b>${s.name}</b> ${s.dose} <span class="mut small">— ${s.when}</span></span>
      </label>`;
    }).join("");
    document.querySelectorAll("[data-supp]").forEach(cb => cb.addEventListener("change", () => {
      const st2 = HMT.get(suppKey, {});
      st2[cb.dataset.supp] = cb.checked;
      HMT.set(suppKey, st2);
      const hist = HMT.get("supp_history", {});
      hist[today] = st2;
      HMT.set("supp_history", hist);
      renderSupp(); renderStreak();
    }));
  };
  renderSupp();

  document.getElementById("suppTable").innerHTML =
    `<tr><th>المكمل</th><th>الجرعة</th><th>التوقيت</th></tr>` +
    S.supplements.map(s => `<tr><td><b>${s.name}</b></td><td>${s.dose}</td><td class="small">${s.when}</td></tr>`).join("");
  document.getElementById("stoppedSupp").textContent = S.stoppedSupplements;

  const renderStreak = () => {
    const hist = HMT.get("supp_history", {});
    let html = `<div style="display:flex;gap:5px;flex-wrap:wrap">`;
    for (let i = 13; i >= 0; i--) {
      const d = new Date(); d.setDate(d.getDate() - i);
      const k = d.toISOString().slice(0, 10);
      const state = hist[k] || {};
      const taken = S.supplements.filter(s => s.daily).filter(s => state[s.id]).length;
      const total = S.supplements.filter(s => s.daily).length;
      const pct = taken / total;
      const bg = pct >= 0.8 ? "var(--green)" : pct >= 0.4 ? "var(--amber)" : pct > 0 ? "#e0a0a8" : "#efe8f1";
      html += `<div title="${HMT.fmtDate(k)}: ${taken}/${total}" style="width:34px;height:34px;border-radius:8px;background:${bg};display:flex;align-items:center;justify-content:center;color:${pct > 0 ? "#fff" : "var(--muted)"};font-size:11px;font-weight:800">${d.getDate()}</div>`;
    }
    document.getElementById("suppStreak").innerHTML = html + `</div><div class="mut small" style="margin-top:8px">أخضر = التزام كامل · أصفر = جزئي · فارغ = لا تسجيل</div>`;
  };
  renderStreak();

  /* ========== 5) المتابعة ========== */
  const wDateEl = document.getElementById("wDate");
  wDateEl.value = today;
  document.getElementById("mDate").value = today;

  // موعد التقرير القادم (الجمعة)
  const nextFriday = () => {
    const d = new Date();
    const diff = (5 - d.getDay() + 7) % 7;
    d.setDate(d.getDate() + (diff === 0 ? 0 : diff));
    return d;
  };
  document.getElementById("nextReportHint").textContent =
    `التقرير القادم: ${HMT.fmtDate(nextFriday())} — أول تقرير معتمد: الجمعة 7/8/2026`;

  document.getElementById("saveWeekly").addEventListener("click", () => {
    const entry = {
      date: wDateEl.value,
      weight: +document.getElementById("wWeight").value || null,
      waist: +document.getElementById("wWaist").value || null,
      steps: +document.getElementById("wSteps").value || null,
      sessions: +document.getElementById("wSessions").value || 0,
      energy: +document.getElementById("wEnergy").value || null,
      sleepScore: +document.getElementById("wSleep").value || null,
      diet: +document.getElementById("wDiet").value || null,
      notes: document.getElementById("wNotes").value,
    };
    if (!entry.date || (!entry.weight && !entry.waist)) return HMT.toast("أدخل التاريخ + الوزن أو الخصر على الأقل");
    const logs = HMT.get("weekly_logs", []).filter(l => l.date !== entry.date);
    logs.push(entry);
    logs.sort((a, b) => a.date.localeCompare(b.date));
    HMT.set("weekly_logs", logs);
    renderWeekly();
    HMT.toast("✅ تم حفظ التقرير الأسبوعي");
  });

  document.getElementById("saveMonthly").addEventListener("click", () => {
    const entry = {
      date: document.getElementById("mDate").value,
      neck: +document.getElementById("mNeck").value || null,
      chest: +document.getElementById("mChest").value || null,
      arm: +document.getElementById("mArm").value || null,
      hip: +document.getElementById("mHip").value || null,
      thigh: +document.getElementById("mThigh").value || null,
    };
    if (!entry.date) return HMT.toast("أدخل التاريخ");
    const logs = HMT.get("monthly_measures", []).filter(l => l.date !== entry.date);
    logs.push(entry);
    logs.sort((a, b) => a.date.localeCompare(b.date));
    HMT.set("monthly_measures", logs);
    HMT.toast("✅ تم حفظ القياسات الشهرية");
  });

  const renderWeekly = () => {
    const logs = HMT.get("weekly_logs", []);
    // الرسم — نضيف نقطة البداية
    const base = { date: S.measurements.date, weight: S.measurements.weight, waist: S.measurements.waist };
    const pts = [base, ...logs];
    HMT.lineChart(document.getElementById("weightChart"), [
      { label: "الوزن (كجم)", color: "#8E1B5B", points: pts.map(l => ({ x: l.date.slice(5), y: l.weight })) },
      { label: "الخصر (سم)", color: "#F2A03D", points: pts.map(l => ({ x: l.date.slice(5), y: l.waist })) },
    ]);
    document.getElementById("weeklyTable").innerHTML =
      `<tr><th>التاريخ</th><th>الوزن</th><th>الخصر</th><th>الخطوات</th><th>جلسات</th><th>طاقة</th><th>نوم</th><th>أكل</th><th>ملاحظات</th></tr>` +
      (logs.length ? logs.slice().reverse().map(l =>
        `<tr><td style="white-space:nowrap">${l.date}</td><td><b>${l.weight ?? "—"}</b></td><td><b>${l.waist ?? "—"}</b></td>
        <td>${l.steps ?? "—"}</td><td>${l.sessions}</td><td>${l.energy ?? "—"}</td><td>${l.sleepScore ?? "—"}</td><td>${l.diet ?? "—"}</td>
        <td class="small">${HMT.esc(l.notes || "")}</td></tr>`).join("")
      : `<tr><td colspan="9" class="mut">لا تقارير بعد — أول تقرير الجمعة 7/8/2026.</td></tr>`);
  };
  renderWeekly();

  /* ========== 6) المستشار ========== */
  Advisor.mount("healthAdvisor", "health", {
    icon: "🧠",
    name: "المستشار الصحي",
    desc: "فريق متكامل: طب وقائي · تغذية · تدريب · مكملات · نوم — يقرأ ملفك وسجلاتك الحية",
    welcome: "أهلًا إبراهيم. أنا مستشارك الصحي — قرأت ملفك الكامل وتحاليلك وخطتك. اسألني أي شيء: تعديل وجبة، مشكلة في تمرين، تفسير رقم، أو قرار صحي تتردد فيه. بدون مجاملات.",
  });
})();
