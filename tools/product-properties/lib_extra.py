# -*- coding: utf-8 -*-
"""Extra families: phone/PC accessories, dishwasher, video games."""
from lib_core import *

FAM = {}

# ------------------------------------------------------------------ phone & tablet accessory
FAM['phone_accessory'] = blk(IDENT, [
    D('spec', 'Accessory Type', 'نوع الإكسسوار',
      'Phone Case / Cover, Tablet Case / Folio, Screen Protector, Wall Charger, '
      'Car Charger, Wireless Charger, Charging Cable, Adapter / Converter, '
      'Power Bank, Phone Holder / Mount, Stand, Stylus Pen, PopSocket / Grip, '
      'Ring Holder, Lanyard / Strap, Camera Lens Protector, SIM Ejector, '
      'Cleaning Kit, Repair Tool Kit, Selfie Stick, Memory Card, Battery',
      required='Yes'),
    D('compat', 'Compatible Brand', 'العلامة المتوافقة',
      'Apple, Samsung, Huawei, Xiaomi, Oppo, Vivo, Realme, Honor, Nothing, '
      'Google, OnePlus, Nokia, Infinix, Tecno, Universal', required='Yes'),
    T('compat', 'Compatible Model', 'الموديل المتوافق', required='Yes'),
    D('compat', 'Compatible Device Type', 'نوع الجهاز المتوافق',
      'Smartphone, Tablet, Smartwatch, Laptop, Earbuds, Universal'),
    D('compat', 'Compatible Screen Size', 'مقاس الشاشة المتوافق',
      'Not Applicable, Up to 6.1 inch, 6.2-6.9 inch, 7-8 inch, 9-11 inch, '
      '11-13 inch, Universal'),
    D('mat', 'Material', 'الخامة',
      'Silicone, TPU, Hard Plastic / PC, PU Leather, Genuine Leather, '
      'Tempered Glass, Aramid Fibre, Metal / Aluminium, Fabric, Rubber, '
      'Hydrogel Film, PET Film, Nylon, Braided Nylon'),
    D('spec', 'Protection Level', 'مستوى الحماية',
      'Not Applicable, Basic, Shockproof, Military Grade (MIL-STD-810G), '
      'Rugged / Heavy Duty, Waterproof, Drop Tested 2m'),
    D('spec', 'Hardness (Screen Protector)', 'الصلابة',
      'Not Applicable, 9H, 10H, 11H'),
    D('power', 'Power Output (W)', 'قدرة الشحن (واط)',
      'Not Applicable, 5 W, 10 W, 15 W, 18 W, 20 W, 25 W, 30 W, 33 W, 45 W, '
      '65 W, 100 W, 120 W, 140 W, 240 W', option='Yes'),
    D('power', 'Fast Charging Standard', 'معيار الشحن السريع',
      'Not Applicable, USB Power Delivery (PD), PD 3.0, Quick Charge 3.0, '
      'Quick Charge 4+, Super Fast Charging, SuperVOOC, SuperCharge, MagSafe, Qi2'),
    I('conn', 'Number of Ports', 'عدد المنافذ', 'Not Applicable, 1, 2, 3, 4, 5, 6'),
    D('conn', 'Connector Type', 'نوع الموصل',
      'Not Applicable, USB-C to USB-C, USB-A to USB-C, USB-A to Lightning, '
      'USB-C to Lightning, Micro USB, HDMI, 3.5mm Audio, Multi-Head'),
    N('spec', 'Cable Length (m)', 'طول الكابل (متر)',
      'Not Applicable, 0.25 m, 0.5 m, 1 m, 1.5 m, 2 m, 3 m, 5 m', option='Yes'),
    I('perf', 'Data Transfer Speed', 'سرعة نقل البيانات',
      'Not Applicable, USB 2.0 (480 Mbps), USB 3.0 (5 Gbps), USB 3.2 (10 Gbps), '
      'USB4 (40 Gbps), Charging Only'),
    D('elec', 'Plug Type', 'نوع القابس',
      'Not Applicable, UK 3-Pin (G-Type), EU 2-Pin, US 2-Pin, Universal'),
    D('spec', 'Mounting Method', 'طريقة التثبيت',
      'Not Applicable, Suction Cup, Air Vent Clip, Adhesive, Magnetic, '
      'Clamp, Dashboard, Free Standing, Wall Mount'),
    B('feat', 'MagSafe / Magnetic Compatible', 'متوافق مع MagSafe'),
    B('feat', 'Wireless Charging Compatible', 'يدعم الشحن اللاسلكي'),
    B('feat', 'Camera Protection Raised Edge', 'حافة حماية للكاميرا'),
    B('feat', 'Kickstand / Stand Function', 'حامل مدمج'),
    B('feat', 'Card Holder', 'جيب للبطاقات'),
    B('feat', 'Anti-Fingerprint Coating', 'طلاء مضاد للبصمات'),
    B('feat', 'Privacy Filter', 'مرشّح الخصوصية'),
    B('feat', 'Anti-Glare / Matte', 'مضاد للانعكاس'),
    B('feat', 'Case Friendly', 'متوافق مع الأغطية'),
    D('pack', 'Pack Quantity', 'الكمية في العبوة', PACK_QTY, option='Yes'),
    D('design', 'Pattern / Design', 'التصميم',
      'Plain / Solid, Transparent / Clear, Printed, Marble, Glitter, '
      'Carbon Fibre, Camouflage, Character / Cartoon, Textured'),
], COLOR, ELEC_COMMERCE)

# ------------------------------------------------------------------ PC peripheral
FAM['pc_peripheral'] = blk(IDENT, [
    D('spec', 'Peripheral Type', 'نوع الملحق',
      'Keyboard, Mouse, Keyboard & Mouse Combo, Mouse Pad, Webcam, '
      'USB Hub, Docking Station, Graphics Tablet, Numeric Keypad, '
      'Cooling Pad, Laptop Stand, Cable Organiser, Adapter', required='Yes'),
    D('conn', 'Connection Type', 'نوع الاتصال',
      'Wired (USB-A), Wired (USB-C), Wireless (2.4 GHz Dongle), Bluetooth, '
      'Dual Mode (Bluetooth + 2.4 GHz), Tri-Mode', required='Yes'),
    D('spec', 'Keyboard Type', 'نوع لوحة المفاتيح',
      'Not Applicable, Membrane, Mechanical, Optical-Mechanical, Scissor Switch, '
      'Magnetic / Hall Effect, Ergonomic, Virtual'),
    D('spec', 'Switch Type', 'نوع المفاتيح',
      'Not Applicable, Red (Linear), Brown (Tactile), Blue (Clicky), '
      'Silver / Speed, Optical, Low Profile'),
    D('spec', 'Keyboard Layout', 'تخطيط لوحة المفاتيح',
      'Not Applicable, Full Size (104 Keys), TKL (87 Keys), 75%, 65%, 60%, '
      'Compact, Ergonomic Split'),
    D('spec', 'Language Layout', 'لغة الأحرف',
      'Not Applicable, English (US), English (UK), Arabic / English, '
      'French (AZERTY), German (QWERTZ)'),
    I('perf', 'Mouse DPI / Sensitivity', 'دقة الفأرة (DPI)',
      'Not Applicable, 800 DPI, 1200 DPI, 1600 DPI, 3200 DPI, 8000 DPI, '
      '16000 DPI, 26000 DPI, Adjustable'),
    I('spec', 'Number of Buttons', 'عدد الأزرار', 'Not Applicable, 2, 3, 5, 6, 7, 8, 12, 16'),
    I('perf', 'Polling Rate (Hz)', 'معدل الاستجابة',
      'Not Applicable, 125 Hz, 500 Hz, 1000 Hz, 4000 Hz, 8000 Hz'),
    D('spec', 'Sensor Type', 'نوع المستشعر',
      'Not Applicable, Optical, Laser, Infrared, Trackball'),
    D('feat', 'Backlight / RGB', 'الإضاءة',
      'No Backlight, White Backlight, Single Colour, RGB, Per-Key RGB'),
    D('batt', 'Battery Type', 'نوع البطارية',
      'Not Applicable, AA Batteries, AAA Batteries, Built-In Rechargeable, Wired / No Battery'),
    D('batt', 'Battery Life', 'عمر البطارية',
      'Not Applicable, Up to 1 Month, 2-3 Months, 4-6 Months, 7-12 Months, Above 12 Months'),
    D('compat', 'Compatible With', 'التوافق',
      'Windows, macOS, Linux, Android, iOS / iPadOS, Chrome OS, '
      'PlayStation, Xbox, Universal'),
    D('spec', 'Webcam Resolution', 'دقة الكاميرا',
      'Not Applicable, HD 720p, Full HD 1080p, 2K QHD, 4K UHD'),
    B('feat', 'Built-In Microphone', 'ميكروفون مدمج'),
    B('feat', 'Palm Rest Included', 'مسند معصم'),
    B('feat', 'Programmable Keys / Macros', 'مفاتيح قابلة للبرمجة'),
    B('feat', 'Anti-Ghosting / N-Key Rollover', 'مضاد للتداخل'),
    B('feat', 'Silent / Quiet Operation', 'تشغيل صامت'),
    B('feat', 'Ergonomic Design', 'تصميم مريح'),
    B('feat', 'Adjustable Height / Tilt', 'ارتفاع قابل للتعديل'),
    B('feat', 'Software Customisation', 'تخصيص عبر برنامج'),
    D('mat', 'Material', 'الخامة',
      'ABS Plastic, PBT Plastic, Aluminium, Stainless Steel, Rubber, '
      'Fabric, Silicone, Wood'),
    D('usage', 'Recommended Use', 'الاستخدام الموصى به',
      'Office & Productivity, Gaming, Programming, Graphic Design, '
      'Travel & Portable, Home Use'),
], COLOR, ELEC_COMMERCE)

# ------------------------------------------------------------------ dishwasher
FAM['dishwasher'] = blk(IDENT, [
    D('spec', 'Dishwasher Type', 'نوع غسالة الصحون',
      'Freestanding, Built-In / Integrated, Semi-Integrated, Slimline, '
      'Countertop / Compact, Drawer Dishwasher', required='Yes'),
    I('cap', 'Place Settings', 'عدد أطقم الأواني',
      '6, 8, 9, 10, 12, 13, 14, 15, 16', required='Yes', option='Yes'),
    N('dims', 'Width (cm)', 'العرض (سم)', '45 cm, 55 cm, 60 cm, 90 cm'),
    I('feat', 'Number of Programs', 'عدد البرامج', '4, 5, 6, 7, 8, 9, 10, 12'),
    D('feat', 'Wash Programs', 'برامج الغسيل',
      'Intensive, Auto / Normal, Eco, Quick / Rapid, Glass / Delicate, '
      'Half Load, Pre-Rinse, Hygiene / Steam, Self Clean, Baby Care'),
    I('spec', 'Number of Spray Arms', 'عدد أذرع الرش', '1, 2, 3, 4'),
    I('spec', 'Number of Racks / Baskets', 'عدد الأرفف', '2, 3'),
    B('feat', 'Third / Cutlery Rack', 'رف ثالث للملاعق'),
    B('feat', 'Adjustable Racks', 'أرفف قابلة للتعديل'),
    B('feat', 'Half Load Function', 'وظيفة نصف الحمولة'),
    B('feat', 'Delay Start Timer', 'مؤقت بدء مؤجل'),
    B('feat', 'Child Lock', 'قفل الأطفال'),
    B('feat', 'Auto Door Opening (Drying)', 'فتح الباب التلقائي للتجفيف'),
    B('feat', 'Leak Protection (AquaStop)', 'حماية من التسرب'),
    B('feat', 'Water Softener', 'ملطّف الماء'),
    D('perf', 'Drying System', 'نظام التجفيف',
      'Condensation Drying, Heat Drying, Turbo Fan Drying, Zeolith Drying, Air Dry'),
    D('perf', 'Drying Class', 'فئة التجفيف', 'A, B, C, D, E, F, G'),
    I('env', 'Water Consumption (L/cycle)', 'استهلاك الماء (لتر/دورة)',
      'Under 9 L, 9-11 L, 12-14 L, 15-18 L, Above 18 L'),
    I('env', 'Annual Energy Consumption (kWh)', 'استهلاك الطاقة السنوي',
      'Under 75 kWh, 75-100 kWh, 101-150 kWh, 151-250 kWh, Above 250 kWh'),
    I('perf', 'Cycle Duration (minutes)', 'مدة الدورة (دقيقة)',
      'Under 30 min, 30-60 min, 61-120 min, 121-180 min, Above 180 min'),
    D('mat', 'Interior Material', 'خامة الداخل',
      'Stainless Steel, Polypropylene / Plastic, Mixed'),
    D('display', 'Display Type', 'نوع الشاشة',
      'No Display, LED Indicators, LED Display, LCD Display, Touch Display'),
    B('feat', 'Beam on Floor Indicator', 'مؤشر ضوئي على الأرض'),
], [
    D('power', 'Voltage', 'الجهد الكهربائي', '220-240 V, 110-120 V'),
    I('power', 'Power Consumption (W)', 'استهلاك الطاقة (واط)',
      'Under 1200 W, 1200-1800 W, 1801-2200 W, Above 2200 W'),
    D('power', 'Plug Type', 'نوع القابس',
      'UK 3-Pin (G-Type), EU 2-Pin (F-Type), US 2-Pin (A/B-Type), Hardwired'),
    D('env', 'Energy Efficiency Class', 'فئة كفاءة الطاقة', ENERGY),
    I('feat', 'Noise Level (dB)', 'مستوى الضوضاء (ديسيبل)',
      'Under 40 dB, 40-44 dB, 45-49 dB, 50-55 dB, Above 55 dB'),
    D('inst', 'Installation Type', 'نوع التركيب',
      'Freestanding, Built-In, Semi Built-In, Under Counter, Countertop'),
    B('smart', 'Smart / Wi-Fi Enabled', 'ذكي / يدعم الواي فاي'),
    T('dims', 'Product Dimensions (L x W x H cm)', 'أبعاد المنتج (سم)'),
], COLOR, ELEC_COMMERCE)

# ------------------------------------------------------------------ video game
FAM['video_game'] = blk([
    T('main', 'Game Title', 'اسم اللعبة', required='Yes'),
    T('main', 'Publisher', 'الناشر'),
    T('main', 'Developer', 'المطوّر'),
    D('compat', 'Platform', 'المنصة',
      'PlayStation 5, PlayStation 4, Xbox Series X|S, Xbox One, Nintendo Switch, '
      'Nintendo Switch 2, PC, Steam Deck, Mobile, Multi-Platform',
      required='Yes', option='Yes'),
    D('spec', 'Genre', 'النوع',
      'Action, Adventure, Action-Adventure, Role Playing (RPG), Shooter (FPS), '
      'Shooter (TPS), Sports, Racing, Fighting, Strategy, Simulation, '
      'Puzzle, Platformer, Horror / Survival, Open World, Family & Kids, '
      'Music & Party, MMO', required='Yes'),
    D('spec', 'Edition', 'الإصدار',
      'Standard Edition, Deluxe Edition, Ultimate Edition, Gold Edition, '
      'Collector\'s Edition, Game of the Year Edition, Legacy Edition'),
    D('spec', 'Format', 'الصيغة', 'Physical Disc, Physical Cartridge, Digital Download Code'),
    D('spec', 'Age Rating (PEGI / ESRB)', 'التصنيف العمري',
      'PEGI 3, PEGI 7, PEGI 12, PEGI 16, PEGI 18, ESRB E, ESRB E10+, '
      'ESRB T, ESRB M, ESRB AO'),
    D('spec', 'Region', 'المنطقة',
      'Region Free, UAE / Middle East, Europe (PAL), USA (NTSC), Japan, Asia'),
    D('spec', 'Language Support', 'اللغات المدعومة',
      'Arabic Subtitles, Arabic Audio, English, Arabic & English, '
      'French, Spanish, Multilingual'),
    D('spec', 'Number of Players', 'عدد اللاعبين',
      'Single Player, 2 Players, 2-4 Players, Up to 8 Players, Online Multiplayer, '
      'Co-Op, Massively Multiplayer'),
    B('feat', 'Online Play Required', 'يتطلب اتصالاً بالإنترنت'),
    B('feat', 'Subscription Required', 'يتطلب اشتراكاً'),
    D('spec', 'Release Year', 'سنة الإصدار',
      'Before 2018, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026'),
    D('display', 'Maximum Resolution', 'أقصى دقة', '1080p, 1440p, 4K UHD, 8K'),
    D('display', 'Frame Rate Support', 'معدل الإطارات', '30 fps, 60 fps, 120 fps'),
    B('feat', 'VR Support', 'دعم الواقع الافتراضي'),
    B('feat', 'Backwards Compatible', 'متوافق مع الأجهزة السابقة'),
    N('storage', 'Installation Size (GB)', 'حجم التثبيت (جيجابايت)',
      'Under 10 GB, 10-30 GB, 31-60 GB, 61-100 GB, Above 100 GB'),
    D('general', 'Condition', 'الحالة', 'New / Sealed, Opened - Like New, Pre-Owned'),
    D('origin', 'Country of Origin', 'بلد المنشأ', ORIGIN),
])
