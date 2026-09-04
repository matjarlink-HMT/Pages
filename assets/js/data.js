/* HMT OS — الهيكل والمكتبات العامة فقط.
   ⚠️ لا تضع أي بيانات شخصية هنا — هذا المستودع عام على الإنترنت.
   بياناتك الحقيقية تُستورد من الإعدادات وتُحفظ في متصفحك (localStorage). */
const DEFAULT_SEED = {
  profile: {
    name: "", age: null, gender: "", nationality: "",
    home: "", work: "", family: "", job: "", schedule: "",
  },
  measurements: {
    date: null, height: null, weight: null, bmi: null,
    waist: null, neck: null, chest: null, arm: null, hip: null, thigh: null,
    bodyFat: null, whr: null,
  },
  labs: { date: null, place: "", echo: "", lipids: [], other: [], missing: "", metabolicNote: "" },
  ratings: [],
  workCycle: {
    anchor: "2026-08-02",
    pattern: ["إجازة", "دوام", "دوام", "دوام"],
    note: "",
  },
  goals12w: { start: "2026-08-02", deadline: "2026-10-24", items: [] },
  nutrition: { calories: null, protein: null, fat: null, carbs: null, fiber: "", water: "", rules: [], meals: [] },
  daySchedule: [
    { time: "06:30", txt: "استيقاظ + ماء + تعرض للضوء", key: "wake" },
    { time: "06:45", txt: "فطور بروتيني + قهوة", key: "breakfast" },
    { time: "07:00", txt: "دوام — قيام دقيقتين كل ساعة", key: "work" },
    { time: "14:00", txt: "غداء + D3 + أوميغا-3", key: "lunch" },
    { time: "14:45", txt: "قيلولة بمنبه ≤ 60 دقيقة", key: "nap" },
    { time: "16:00", txt: "سناك + آخر قهوة", key: "snack" },
    { time: "17:00", txt: "جيم (أيام التمرين: اثنين + خميس)", key: "gym" },
    { time: "18:00", txt: "مشي 30–45 دقيقة (هدف 7–8 آلاف خطوة)", key: "walk" },
    { time: "19:30", txt: "عشاء", key: "dinner" },
    { time: "22:15", txt: "تصحيحي الأبهر 5د + مغنيسيوم + لبن", key: "corrective" },
    { time: "22:40", txt: "هاتف خارج السرير", key: "phone" },
    { time: "23:00", txt: "نوم", key: "sleep" },
  ],
  workouts: {
    trainingDays: [1, 4], // اثنين=1، خميس=4 (JS: الأحد=0)
    A: {
      name: "تمرين A — جسم كامل",
      warmup: "إحماء 8 دقائق: مشي سريع/دراجة + تحريك مفاصل",
      cooldown: "كارديو خفيف 10 دقائق + إطالات",
      exercises: [
        { name: "Goblet Squat — سكوات الكأس", sets: "3×10", muscle: "أرجل + جذع",
          how: ["امسك دمبل عموديًا أمام صدرك بكلتا يديك", "قدماك بعرض الكتفين، أصابع القدم للخارج قليلًا", "انزل ببطء حتى يوازي الفخذ الأرض مع إبقاء الصدر مرفوعًا", "ادفع بكعبيك للصعود"],
          cue: "الركبتان باتجاه أصابع القدم — لا تنحني للداخل. الظهر مستقيم دائمًا.",
          video: "https://www.youtube.com/results?search_query=goblet+squat+form" },
        { name: "Chest Press آلة — ضغط صدر", sets: "3×10", muscle: "صدر + ترايسبس",
          how: ["اضبط المقعد بحيث المقابض بمستوى منتصف الصدر", "ظهرك ملتصق بالمسند", "ادفع للأمام حتى شبه فرد الذراعين (لا تقفل المرفق)", "ارجع ببطء 2-3 ثوان"],
          cue: "لا ترفع كتفيك نحو أذنيك — الكتف ثابت ومسحوب للخلف.",
          video: "https://www.youtube.com/results?search_query=machine+chest+press+form" },
        { name: "Seated Cable Row — تجديف كابل جالس", sets: "3×12", muscle: "ظهر (مهم للأبهر)",
          how: ["اجلس وظهرك مستقيم وركبتاك منحنيتان قليلًا", "اسحب المقبض نحو أسفل بطنك", "اعصر لوحي الكتف معًا في النهاية ثانية", "ارجع ببطء بتحكم كامل"],
          cue: "هذا أهم تمرين لألم الأبهر — ركز على عصر لوحي الكتف، لا تسحب بذراعيك فقط.",
          video: "https://www.youtube.com/results?search_query=seated+cable+row+form" },
        { name: "DB RDL — رفعة رومانية بالدمبل", sets: "3×10", muscle: "خلفية الفخذ + أسفل الظهر",
          how: ["امسك دمبلين أمام فخذيك", "انحنِ من الورك (ليس الخصر) مع ظهر مستقيم تمامًا", "انزل بالدمبل ملاصقًا لساقيك حتى تحس شد خلفية الفخذ", "ارجع بعصر المؤخرة"],
          cue: "الحركة من الورك — الظهر لا ينحني أبدًا. ركبة منحنية قليلًا وثابتة.",
          video: "https://www.youtube.com/results?search_query=dumbbell+romanian+deadlift+form" },
        { name: "Face Pull — سحب للوجه", sets: "3×15", muscle: "كتف خلفي (علاج وضعية الجلوس)",
          how: ["اضبط الكابل بمستوى الوجه مع حبل مزدوج", "اسحب الحبل نحو وجهك مع فتح اليدين لجانبي الرأس", "اعصر لوحي الكتف ثانية كاملة", "ارجع ببطء"],
          cue: "وزن خفيف وتكرارات نظيفة — هذا تمرين علاجي لوضعيتك، ليس تمرين قوة.",
          video: "https://www.youtube.com/results?search_query=face+pull+form" },
        { name: "Plank — بلانك", sets: "3×30 ثانية", muscle: "جذع",
          how: ["ارتكز على ساعديك وأطراف قدميك", "جسمك خط مستقيم من الرأس للكعب", "شد بطنك ومؤخرتك طوال الوقت", "تنفس طبيعيًا"],
          cue: "لا تدع وسطك يهبط ولا ترفع مؤخرتك — خط واحد مستقيم.",
          video: "https://www.youtube.com/results?search_query=plank+form" },
      ],
    },
    B: {
      name: "تمرين B — جسم كامل",
      warmup: "إحماء 8 دقائق: مشي سريع/دراجة + تحريك مفاصل",
      cooldown: "كارديو خفيف 10 دقائق + إطالات",
      exercises: [
        { name: "Leg Press — دفع أرجل", sets: "3×12", muscle: "أرجل",
          how: ["قدماك بعرض الكتفين على المنصة", "انزل بالمنصة حتى زاوية 90 درجة بالركبة", "ادفع بكامل القدم بدون قفل الركبة", "تحكم بالنزول"],
          cue: "لا ترفع أسفل ظهرك عن المقعد أبدًا أثناء النزول.",
          video: "https://www.youtube.com/results?search_query=leg+press+form" },
        { name: "Lat Pulldown — سحب أمامي", sets: "3×10", muscle: "ظهر عريض",
          how: ["امسك البار أوسع من كتفيك قليلًا", "اسحب البار لأعلى صدرك مع ميل خفيف للخلف", "اعصر لوحي الكتف بالأسفل", "ارجع ببطء لفرد شبه كامل"],
          cue: "اسحب بمرفقيك نحو جيوبك — لا تتأرجح بجسمك.",
          video: "https://www.youtube.com/results?search_query=lat+pulldown+form" },
        { name: "DB Shoulder Press — ضغط كتف بالدمبل", sets: "3×10", muscle: "كتف",
          how: ["اجلس بمسند ظهر، دمبل بكل يد بمستوى الأذن", "ادفع للأعلى حتى شبه التقاء الدمبلين", "لا تقفل المرفقين", "انزل ببطء لمستوى الأذن"],
          cue: "لا تقوّس أسفل ظهرك — شد بطنك طوال التمرين.",
          video: "https://www.youtube.com/results?search_query=seated+dumbbell+shoulder+press" },
        { name: "Reverse Fly — رفرفة خلفية", sets: "3×15", muscle: "كتف خلفي (علاجي)",
          how: ["انحنِ للأمام بظهر مستقيم، دمبلان خفيفان", "ارفع ذراعيك للجانبين كجناحين", "اعصر لوحي الكتف بالأعلى", "انزل بتحكم"],
          cue: "وزن خفيف جدًا — الهدف عضلات الكتف الخلفية لا الزخم.",
          video: "https://www.youtube.com/results?search_query=reverse+fly+dumbbell+form" },
        { name: "Farmer Carry — حمل المزارع", sets: "3×30 متر", muscle: "قبضة + جذع + كامل الجسم",
          how: ["امسك دمبلين ثقيلين على جانبيك", "امشِ بخطوات ثابتة وصدر مرفوع", "كتفاك للخلف وبطنك مشدود", "30 متر ثم راحة"],
          cue: "قامة ملكية — كأن أحدًا يشدك من أعلى رأسك بخيط.",
          video: "https://www.youtube.com/results?search_query=farmer+carry+form" },
        { name: "Dead Bug — الحشرة الميتة", sets: "3×10 لكل جانب", muscle: "جذع عميق",
          how: ["استلقِ على ظهرك، ذراعاك للسقف وركبتاك 90 درجة", "مدّ ذراعك اليمنى خلف رأسك ورجلك اليسرى للأمام معًا", "أسفل ظهرك ملتصق بالأرض دائمًا", "ارجع وبدّل الجانب"],
          cue: "إذا ارتفع أسفل ظهرك عن الأرض — صغّر مدى الحركة.",
          video: "https://www.youtube.com/results?search_query=dead+bug+exercise+form" },
      ],
    },
    homeAlt: {
      name: "بديل المنزل (دمبل 5 كجم + جهاز كارديو)",
      desc: "دائرة 3 جولات: سكوات كأس ×15 · اندفاع ×10 لكل رجل · ضغط أرضي ×أقصى · تجديف بالدمبل ×12 · ضغط كتف ×12 · بلانك 30ث — ثم 15 دقيقة كارديو. راحة 60-90ث بين الجولات.",
    },
    corrective: {
      name: "التصحيحي اليومي للأبهر (5 دقائق)",
      items: ["إطالة صدر بإطار الباب 3×30 ثانية", "Chin Tucks (سحب ذقن) ×10", "إطالة رقبة جانبية لكل جهة 30 ثانية", "أثناء الدوام: قيام وحركة دقيقتين كل ساعة"],
    },
    progression: "أسبوعان تعويد سهلان → ثم Double Progression: زد التكرارات حتى سقف المدى ثم زد الوزن. دائمًا 1-2 تكرار بالخزان. لا فشل عضلي أول 12 أسبوعًا.",
  },
  supplements: [],
  stoppedSupplements: "",
  safetyRule: "⚠️ أي ألم صدر يزداد مع الجهد / ضيق نفس / دوخة → أوقف فورًا وقيّم طبيًا.",
};

/* ---------- دمج بياناتك الخاصة من المتصفح ----------
   يعمل قبل core.js، لذا يقرأ localStorage مباشرة بنفس البادئة "hmtos_". */
(function () {
  const deepMerge = (base, over) => {
    if (Array.isArray(over)) return over.slice();
    if (over && typeof over === "object" && !Array.isArray(base) && base && typeof base === "object") {
      const out = { ...base };
      for (const k of Object.keys(over)) out[k] = deepMerge(base[k], over[k]);
      return out;
    }
    return over === undefined ? base : over;
  };
  let priv = null;
  try { priv = JSON.parse(localStorage.getItem("hmtos_seed") || "null"); } catch (e) { priv = null; }
  window.HMT_SEED = priv ? deepMerge(DEFAULT_SEED, priv) : DEFAULT_SEED;
  window.HMT_HOME = window.HMT_SEED.profile.home || "المنزل";
  window.HMT_WORK = String(window.HMT_SEED.profile.work || "").split(" (")[0] || "مقر العمل";
  window.HMT_SEED_LOADED = !!(priv && priv.measurements && priv.measurements.weight);
})();
