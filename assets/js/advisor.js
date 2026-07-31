/* ================= المستشارون — محرك Claude ================= */
/* يعمل مباشرة من المتصفح عبر Claude API (مفتاحك يبقى في جهازك فقط) */
const Advisor = (() => {
  const MODEL = "claude-opus-5";
  const API_URL = "https://api.anthropic.com/v1/messages";
  const MAX_HISTORY = 24; // آخر 24 رسالة تُرسل للنموذج

  const getKey = () => HMT.get("api_key", "");

  const baseStyle = `
أسلوبك الإلزامي:
- عربي، مباشر ومختصر. النتيجة أولًا ثم الشرح.
- لا مجاملات ولا عبارات تحفيزية فارغة. واقعي 100% وحلول قابلة للتنفيذ فورًا.
- توصية واحدة محددة أفضل من قائمة خيارات. إذا كان لا بد من خيارات، رشّح واحدًا بوضوح.
- اربط كل إجابة ببيانات إبراهيم الفعلية أدناه — ممنوع الإجابات العامة.
- اذكر قوة الدليل بصراحة (قوي/متوسط/ضعيف) عند التوصيات.
- التحذيرات موجزة وفي النهاية فقط.
- عند المقابلات والجمع المعلومات: اسأل سؤالًا واحدًا فقط في كل رسالة.`;

  /* ---------- برومبتات المستشارين ---------- */
  const personas = {
    health: () => {
      const s = window.HMT_SEED;
      const weekly = HMT.get("weekly_logs", []);
      const monthly = HMT.get("monthly_measures", []);
      const workouts = HMT.get("workout_logs", []).slice(-6);
      return `أنت "المستشار الصحي" لإبراهيم — فريق متكامل في شخص واحد: طب وقائي، تغذية علاجية ورياضية، مكملات، تدريب قوة، نوم، هرمونات، أداء ذهني.
${baseStyle}

# الملف الصحي الكامل لإبراهيم
${JSON.stringify(s, null, 1)}

# سجلات المتابعة الأسبوعية (وزن/خصر/خطوات/تقييمات)
${JSON.stringify(weekly, null, 1) || "لا سجلات بعد"}

# القياسات الشهرية
${JSON.stringify(monthly, null, 1) || "لا قياسات بعد"}

# آخر جلسات التمرين المسجلة
${JSON.stringify(workouts, null, 1) || "لا جلسات مسجلة بعد"}

# قواعد ثابتة لا تُناقش
- القهوة خط أحمر لا يُمس — التوقيت فقط قابل للضبط (آخر كافيين 16:00).
- الخطة المعتمدة (المرحلة 1: 2 أغسطس – 24 أكتوبر 2026) هي المرجع؛ أي تعديل يجب أن يكون مبررًا بالبيانات.
- قاعدة الأمان: أي ألم صدر يزداد مع الجهد / ضيق نفس / دوخة → إيقاف وتقييم طبي فوري.
- أنت لست بديلًا عن الطبيب في التشخيص والأدوية — قلها فقط عندما يكون الموضوع طبيًا فعلًا، ليس في كل رسالة.`;
    },
    finance: () => {
      const fin = HMT.get("finance", {});
      return `أنت "المستشار المالي" لإبراهيم — خبير تخطيط مالي شخصي وإدارة ديون وميزانيات، عملي وصارم.
${baseStyle}

# السياق الشخصي
- إبراهيم، 32 سنة، عُماني، متزوج + 3 أطفال. موظف إداري + مالك مشروع "متجرلينك".
- العملة: ريال عُماني (ر.ع).
- هدفه: إنهاء ديونه وبناء ميزانية محكمة يومية/شهرية/سنوية.

# بياناته المالية المسجلة حتى الآن
${Object.keys(fin).length ? JSON.stringify(fin, null, 1) : "⚠️ لا توجد بيانات مالية بعد."}

# مهمتك
1) إذا كانت البيانات ناقصة: أدر مقابلة احترافية — سؤال واحد في كل رسالة — لجمع: صافي الدخل الشهري، دخل متجرلينك، الالتزامات الثابتة، كل دين (الجهة/المبلغ المتبقي/القسط/الفائدة/تاريخ الاستحقاق)، المصاريف المتغيرة، أي مدخرات.
2) بعد اكتمال الصورة: ابنِ خطة سداد واقعية (فضّل Avalanche للفوائد الأعلى واشرح لماذا)، وميزانية شهرية بأرقام محددة، وصندوق طوارئ تدريجي.
3) بعد كل معلومة مهمة يعطيك إياها: اطلب منه صراحة تسجيلها في قسم المالية بالمنصة حتى تبقى محفوظة.
- كن صريحًا بلا مجاملة: إذا كان الإنفاق غير منطقي قلها بالأرقام.`;
    },
    business: () => {
      const biz = HMT.get("matjarlink", {});
      return `أنت "مستشار الأعمال" لمشروع متجرلينك — خبير تجارة إلكترونية ونمو مشاريع ناشئة في الخليج، عملي وصارم.
${baseStyle}

# السياق
- المالك: إبراهيم، يدير متجرلينك مساءً بجانب وظيفته (الأحد–الخميس 07:00–13:30).
- وقته المتاح للمشروع محدود: بعد 20:00 غالبًا، حسب جدوله الصحي الجديد.
- لديه خطة تنفيذ موجودة في المنصة (HMT_Tasks).

# بيانات متجرلينك المسجلة
${Object.keys(biz).length ? JSON.stringify(biz, null, 1) : "⚠️ لا توجد بيانات مسجلة بعد — اسأل عن: طبيعة المنتج/الخدمة، المبيعات الشهرية، هامش الربح، قنوات التسويق، أكبر عائق حالي."}

# مهمتك
- قرارات نمو مبنية على أرقام. اسأل عن الأرقام قبل أي توصية تسويقية.
- احترم قيد الوقت: أي خطة يجب أن تنفذ بأقل من ساعتين يوميًا.
- اطلب منه تسجيل المؤشرات المهمة في قسم متجرلينك بالمنصة.`;
    },
  };

  /* ---------- سجل المحادثة ---------- */
  const histKey = (id) => `chat_${id}`;
  const getHistory = (id) => HMT.get(histKey(id), []);
  const saveHistory = (id, h) => HMT.set(histKey(id), h.slice(-60));

  /* ---------- استدعاء Claude (بث مباشر) ---------- */
  async function send(id, userText, onDelta) {
    const key = getKey();
    if (!key) throw new Error("NO_KEY");
    const history = getHistory(id);
    history.push({ role: "user", content: userText });

    const resp = await fetch(API_URL, {
      method: "POST",
      headers: {
        "content-type": "application/json",
        "x-api-key": key,
        "anthropic-version": "2023-06-01",
        "anthropic-dangerous-direct-browser-access": "true",
      },
      body: JSON.stringify({
        model: MODEL,
        max_tokens: 4096,
        stream: true,
        system: personas[id](),
        messages: history.slice(-MAX_HISTORY).map(m => ({ role: m.role, content: m.content })),
      }),
    });

    if (!resp.ok) {
      const err = await resp.json().catch(() => ({}));
      history.pop();
      throw new Error(err?.error?.message || `خطأ HTTP ${resp.status}`);
    }

    const reader = resp.body.getReader();
    const decoder = new TextDecoder();
    let buffer = "", fullText = "", stopReason = null;

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split("\n");
      buffer = lines.pop();
      for (const line of lines) {
        if (!line.startsWith("data: ")) continue;
        let ev;
        try { ev = JSON.parse(line.slice(6)); } catch { continue; }
        if (ev.type === "content_block_delta" && ev.delta?.type === "text_delta") {
          fullText += ev.delta.text;
          onDelta(fullText);
        } else if (ev.type === "message_delta" && ev.delta?.stop_reason) {
          stopReason = ev.delta.stop_reason;
        }
      }
    }

    if (stopReason === "refusal" && !fullText) {
      fullText = "تعذّر الرد على هذا الطلب لأسباب تتعلق بسياسات الأمان. أعد صياغة سؤالك.";
    }
    history.push({ role: "assistant", content: fullText || "…" });
    saveHistory(id, history);
    return fullText;
  }

  /* ---------- واجهة الدردشة ---------- */
  function mount(containerId, advisorId, meta) {
    const root = document.getElementById(containerId);
    if (!root) return;
    root.innerHTML = `
      <div class="advisor-head">
        <div class="av">${meta.icon}</div>
        <div>
          <b>${HMT.esc(meta.name)}</b>
          <div class="mut small">${HMT.esc(meta.desc)}</div>
        </div>
        <button class="btn o sm" style="margin-inline-start:auto" data-act="clear">🗑 محادثة جديدة</button>
      </div>
      <div class="chatbox">
        <div class="chatlog" data-log></div>
        <div class="chatin">
          <textarea placeholder="اكتب سؤالك…" data-in></textarea>
          <button class="btn" data-act="send">إرسال</button>
        </div>
      </div>`;

    const log = root.querySelector("[data-log]");
    const input = root.querySelector("[data-in]");
    const sendBtn = root.querySelector('[data-act="send"]');

    const addMsg = (role, text) => {
      const d = document.createElement("div");
      d.className = `msg ${role}`;
      d.textContent = text;
      log.appendChild(d);
      log.scrollTop = log.scrollHeight;
      return d;
    };

    // history render
    const hist = getHistory(advisorId);
    if (hist.length === 0) {
      addMsg("ai", meta.welcome);
    } else {
      hist.forEach(m => addMsg(m.role === "user" ? "user" : "ai", m.content));
    }

    const doSend = async () => {
      const text = input.value.trim();
      if (!text) return;
      if (!getKey()) {
        addMsg("ai", "⚠️ لم يتم ضبط مفتاح Claude API بعد. اذهب إلى الإعدادات ⚙️ وأدخل مفتاحك أولًا حتى يعمل المستشار.");
        return;
      }
      input.value = "";
      sendBtn.disabled = true;
      addMsg("user", text);
      const aiEl = addMsg("ai", "يفكر…");
      aiEl.classList.add("thinking");
      try {
        await send(advisorId, text, (partial) => {
          aiEl.classList.remove("thinking");
          aiEl.textContent = partial;
          log.scrollTop = log.scrollHeight;
        });
      } catch (e) {
        aiEl.classList.remove("thinking");
        aiEl.textContent = e.message === "NO_KEY"
          ? "⚠️ أدخل مفتاح API في الإعدادات أولًا."
          : `❌ خطأ: ${e.message}`;
      } finally {
        sendBtn.disabled = false;
        input.focus();
      }
    };

    sendBtn.addEventListener("click", doSend);
    input.addEventListener("keydown", e => {
      if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); doSend(); }
    });
    root.querySelector('[data-act="clear"]').addEventListener("click", () => {
      if (!confirm("مسح المحادثة الحالية والبدء من جديد؟")) return;
      HMT.del(histKey(advisorId));
      log.innerHTML = "";
      addMsg("ai", meta.welcome);
    });
  }

  return { mount, getHistory };
})();
