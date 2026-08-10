# -*- coding: utf-8 -*-
"""Technology families, part 2: imaging, audio, wearables, gaming, office, network, accessories."""
from lib_core import *

FAM = {}

# ------------------------------------------------------------------ camera
FAM['camera'] = blk(IDENT, [
    D('spec', 'Camera Type', 'نوع الكاميرا',
      'DSLR, Mirrorless, Compact / Point-and-Shoot, Bridge Camera, Action Camera, '
      'Instant Camera, Cinema Camera, 360 Camera, Film Camera', required='Yes'),
    D('spec', 'Sensor Type', 'نوع المستشعر',
      'Full Frame, APS-C, Micro Four Thirds, 1 inch, 1/1.7 inch, 1/2.3 inch, '
      'Medium Format, CMOS, BSI-CMOS, Stacked CMOS'),
    D('spec', 'Effective Resolution (MP)', 'الدقة الفعلية (ميجابكسل)',
      'Under 16 MP, 16-20 MP, 21-26 MP, 27-33 MP, 34-45 MP, 46-61 MP, Above 61 MP',
      required='Yes'),
    D('spec', 'Lens Mount', 'قاعدة العدسة',
      'Canon RF, Canon EF, Canon EF-S, Nikon Z, Nikon F, Sony E / FE, Sony A, '
      'Fujifilm X, Fujifilm G, Micro Four Thirds, Leica L, Pentax K, Fixed Lens'),
    B('pack', 'Lens Included (Kit)', 'يشمل عدسة (طقم)'),
    T('spec', 'Included Lens Focal Length', 'البعد البؤري للعدسة المرفقة'),
    D('spec', 'Maximum Video Resolution', 'أقصى دقة فيديو',
      'Full HD 1080p, 4K 24fps, 4K 30fps, 4K 60fps, 4K 120fps, 6K, 8K 30fps'),
    D('spec', 'ISO Range', 'نطاق الأيزو',
      '100-6400, 100-12800, 100-25600, 100-51200, 100-102400, 50-204800, Expandable'),
    D('spec', 'Maximum Shutter Speed', 'أقصى سرعة غالق',
      '1/2000 s, 1/4000 s, 1/8000 s, 1/16000 s, 1/32000 s (Electronic)'),
    D('spec', 'Continuous Shooting (fps)', 'التصوير المتتابع (إطار/ث)',
      '3 fps, 5 fps, 7 fps, 10 fps, 15 fps, 20 fps, 30 fps, 40 fps, 120 fps'),
    D('spec', 'Autofocus System', 'نظام التركيز التلقائي',
      'Contrast Detection, Phase Detection, Hybrid AF, Dual Pixel AF, '
      'Eye / Face Detection AF, Animal Detection AF, Subject Tracking AF'),
    I('spec', 'Autofocus Points', 'عدد نقاط التركيز',
      '9, 45, 61, 121, 273, 425, 693, 759, 1053, 5000+'),
    D('spec', 'Image Stabilisation', 'مثبّت الصورة',
      'None, Lens-Based (OIS), In-Body (IBIS), Sensor-Shift 5-Axis, Digital / Electronic, Hybrid'),
    D('display', 'Screen Type', 'نوع الشاشة',
      'Fixed LCD, Tilting LCD, Vari-Angle / Flip-Out LCD, Touchscreen, No Screen'),
    N('display', 'Screen Size (inch)', 'حجم الشاشة (بوصة)',
      '2 inch, 2.7 inch, 3 inch, 3.2 inch, 3.5 inch'),
    D('spec', 'Viewfinder', 'عدسة الرؤية',
      'Optical (OVF), Electronic (EVF), Hybrid, None'),
    D('storage', 'Memory Card Type', 'نوع بطاقة الذاكرة',
      'SD / SDHC / SDXC, microSD, CFexpress Type A, CFexpress Type B, CFast, XQD, Internal Only'),
    I('storage', 'Number of Card Slots', 'عدد فتحات البطاقات', '1, 2'),
    D('conn', 'Connectivity', 'الاتصال',
      'Wi-Fi, Bluetooth, NFC, USB-C, Micro USB, HDMI, Microphone Input, '
      'Headphone Jack, GPS, Ethernet'),
    D('batt', 'Battery Type', 'نوع البطارية',
      'Rechargeable Li-Ion Pack, Built-In Rechargeable, AA Batteries'),
    I('batt', 'Battery Life (shots)', 'عمر البطارية (عدد اللقطات)',
      'Under 250 Shots, 250-400 Shots, 401-600 Shots, 601-900 Shots, Above 900 Shots'),
    D('safety', 'Weather Sealing', 'مقاومة العوامل الجوية',
      'None, Splash & Dust Resistant, Weather Sealed, Waterproof, Shockproof, Freezeproof'),
    N('design', 'Weight (g)', 'الوزن (جم)',
      'Under 300 g, 300-500 g, 501-700 g, 701-1000 g, Above 1000 g'),
    D('usage', 'Recommended Use', 'الاستخدام الموصى به',
      'Beginner / Entry Level, Enthusiast, Professional, Vlogging & Content Creation, '
      'Sports & Wildlife, Studio & Portrait, Travel, Underwater'),
], COLOR, ELEC_COMMERCE)

# ------------------------------------------------------------------ headphones / audio wearable
FAM['headphones'] = blk(IDENT, [
    D('spec', 'Headphone Type', 'نوع السماعة',
      'In-Ear (Wired), True Wireless (TWS), Neckband, On-Ear, Over-Ear, '
      'Open-Ear / Air Conduction, Bone Conduction, Gaming Headset, Single Ear Headset',
      required='Yes'),
    D('conn', 'Connection Type', 'نوع الاتصال',
      'Wireless (Bluetooth), Wired (3.5mm), Wired (USB-C), Wired (Lightning), '
      '2.4 GHz Dongle, Multi-Mode (Wired + Wireless)', required='Yes'),
    D('conn', 'Bluetooth Version', 'إصدار البلوتوث',
      'Not Applicable, Bluetooth 4.2, Bluetooth 5.0, Bluetooth 5.1, Bluetooth 5.2, '
      'Bluetooth 5.3, Bluetooth 5.4, Bluetooth 6.0'),
    D('feat', 'Noise Cancellation', 'إلغاء الضوضاء',
      'None, Passive Noise Isolation, Active Noise Cancellation (ANC), '
      'Adaptive ANC, Hybrid ANC, ANC + Transparency Mode'),
    B('feat', 'Transparency / Ambient Mode', 'وضع الشفافية / المحيط'),
    N('audio', 'Driver Size (mm)', 'حجم المشغّل (ملم)',
      '6 mm, 8 mm, 10 mm, 11 mm, 12 mm, 13 mm, 40 mm, 45 mm, 50 mm, 53 mm'),
    D('audio', 'Driver Type', 'نوع المشغّل',
      'Dynamic, Balanced Armature, Planar Magnetic, Electrostatic, Hybrid Dual Driver'),
    D('audio', 'Frequency Response', 'استجابة التردد',
      '20 Hz - 20 kHz, 20 Hz - 40 kHz, 10 Hz - 40 kHz, 5 Hz - 40 kHz'),
    D('audio', 'Audio Codecs', 'ترميزات الصوت',
      'SBC, AAC, aptX, aptX HD, aptX Adaptive, aptX Lossless, LDAC, LHDC, LC3'),
    B('audio', 'Hi-Res Audio Certified', 'معتمد للصوت عالي الدقة'),
    B('audio', 'Spatial / 3D Audio', 'الصوت المكاني ثلاثي الأبعاد'),
    D('batt', 'Playback Time (hours)', 'مدة التشغيل (ساعة)',
      'Up to 4 Hours, 5-8 Hours, 9-12 Hours, 13-20 Hours, 21-30 Hours, '
      '31-50 Hours, Above 50 Hours'),
    D('batt', 'Total Time with Case (hours)', 'المدة الإجمالية مع العلبة (ساعة)',
      'Not Applicable, Up to 20 Hours, 21-30 Hours, 31-40 Hours, 41-60 Hours, Above 60 Hours'),
    D('batt', 'Charging Port', 'منفذ الشحن',
      'USB Type-C, Micro USB, Lightning, Wireless Charging, Not Applicable'),
    B('batt', 'Fast Charging', 'شحن سريع'),
    B('batt', 'Wireless Charging Case', 'علبة شحن لاسلكي'),
    D('feat', 'Microphone', 'الميكروفون',
      'Built-In Mic, Dual Mic, Triple Mic, Beamforming Mic, Detachable Boom Mic, '
      'Retractable Mic, No Microphone'),
    B('feat', 'ENC / Call Noise Reduction', 'خفض ضوضاء المكالمات'),
    D('feat', 'Controls', 'التحكم',
      'Touch Controls, Physical Buttons, Voice Control, App Control, Inline Remote'),
    B('feat', 'Multipoint Pairing', 'الاقتران بجهازين'),
    B('feat', 'Voice Assistant Support', 'دعم المساعد الصوتي'),
    B('feat', 'Foldable Design', 'تصميم قابل للطي'),
    D('safety', 'Water & Sweat Resistance', 'مقاومة الماء والعرق', IP_RATING),
    D('usage', 'Recommended Use', 'الاستخدام الموصى به',
      'Everyday Listening, Sports & Fitness, Gaming, Studio & Monitoring, '
      'Travel & Commute, Calls & Meetings, Swimming'),
    N('design', 'Weight (g)', 'الوزن (جم)',
      'Under 10 g, 10-50 g, 51-150 g, 151-250 g, 251-400 g, Above 400 g'),
    D('mat', 'Ear Cushion Material', 'خامة وسادة الأذن',
      'Protein Leather, Memory Foam, Velour, Silicone, Fabric, Genuine Leather, Not Applicable'),
    B('pack', 'Carrying Case Included', 'يشمل حقيبة حمل'),
], COLOR, ELEC_COMMERCE)

# ------------------------------------------------------------------ speaker
FAM['speaker'] = blk(IDENT, [
    D('spec', 'Speaker Type', 'نوع السماعة',
      'Portable Bluetooth Speaker, Smart Speaker, Soundbar, Home Theatre System, '
      'Bookshelf Speaker, Tower / Floor Standing, Party Speaker, PC Speaker, '
      'Ceiling Speaker, Subwoofer, Karaoke Speaker', required='Yes'),
    D('power', 'Output Power (W)', 'قدرة الإخراج (واط)',
      '5 W, 10 W, 20 W, 30 W, 50 W, 80 W, 100 W, 150 W, 200 W, 300 W, 500 W, 1000 W'),
    D('audio', 'Channel Configuration', 'تكوين القنوات',
      'Mono, 2.0, 2.1, 3.1, 5.1, 5.1.2, 7.1, 7.1.4, 9.1.4'),
    D('conn', 'Connection Type', 'نوع الاتصال',
      'Bluetooth, Wi-Fi, AUX 3.5mm, USB, HDMI ARC / eARC, Optical, RCA, '
      'NFC, Ethernet, AirPlay 2, Chromecast Built-In'),
    D('conn', 'Bluetooth Version', 'إصدار البلوتوث',
      'Not Applicable, Bluetooth 4.2, Bluetooth 5.0, Bluetooth 5.1, Bluetooth 5.2, Bluetooth 5.3'),
    D('audio', 'Audio Technology', 'تقنية الصوت',
      'Dolby Atmos, Dolby Digital, DTS:X, DTS Virtual:X, Hi-Res Audio, '
      '360 Reality Audio, Standard Stereo'),
    B('smart', 'Voice Assistant Built-In', 'مساعد صوتي مدمج'),
    D('smart', 'Voice Assistant', 'المساعد الصوتي',
      'Not Available, Amazon Alexa, Google Assistant, Apple Siri, Bixby, Multiple'),
    D('batt', 'Battery Life (hours)', 'عمر البطارية (ساعة)',
      'Not Applicable (Mains Powered), Up to 6 Hours, 7-12 Hours, 13-20 Hours, '
      '21-30 Hours, Above 30 Hours'),
    D('power', 'Power Source', 'مصدر الطاقة',
      'Rechargeable Battery, Mains / AC Power, Battery + Mains, USB Powered, Solar'),
    D('safety', 'Water & Dust Resistance', 'مقاومة الماء والغبار', IP_RATING),
    B('feat', 'Stereo Pairing', 'الاقتران الاستريو'),
    B('feat', 'Built-In Microphone', 'ميكروفون مدمج'),
    B('feat', 'Multi-Room Audio', 'الصوت متعدد الغرف'),
    B('feat', 'Karaoke / Mic Input', 'مدخل ميكروفون / كاريوكي'),
    B('feat', 'RGB Lighting', 'إضاءة RGB'),
    B('feat', 'App Control / EQ', 'تحكم عبر التطبيق / معادل صوتي'),
    B('feat', 'Wireless Subwoofer Included', 'يشمل مضخم صوت لاسلكي'),
    D('design', 'Mounting Type', 'طريقة التركيب',
      'Free Standing, Wall Mountable, Ceiling Mounted, Desktop, Portable / Handle, Trolley'),
    D('mat', 'Housing Material', 'خامة الهيكل',
      'ABS Plastic, Fabric Mesh, Aluminium, Wood / MDF, Silicone, Metal Grille'),
], COLOR, ELEC_COMMERCE)

# ------------------------------------------------------------------ smartwatch / wearable
# Verified 2026-08-10 against eXtra's "SMART WATCH" classification, sampled from
# 11 live product pages under
# https://www.extra.com/en-sa/mobiles-tablets/wearable/smart-watches/
FAM['smartwatch'] = blk(IDENT, [
    D('spec', 'Device Type', 'نوع الجهاز',
      'Smartwatch, Fitness Tracker / Band, Hybrid Smartwatch, Kids Smartwatch, '
      'Sports GPS Watch, Smart Ring', required='Yes'),
    D('general', 'Operating System', 'نظام التشغيل',
      'watchOS, Wear OS, Tizen, HarmonyOS, Proprietary RTOS, Garmin OS, Zepp OS'),
    D('compat', 'Compatible With', 'التوافق', 'iOS Only, Android Only, iOS & Android'),
    D('display', 'Display Type', 'نوع الشاشة',
      'AMOLED, Super AMOLED, OLED, LCD / TFT, LTPO AMOLED, MIP (Memory in Pixel), E-Ink'),
    N('display', 'Display Size (inch)', 'حجم الشاشة (بوصة)',
      '1.1 inch, 1.3 inch, 1.4 inch, 1.5 inch, 1.6 inch, 1.8 inch, 1.9 inch, 2.0 inch'),
    D('display', 'Display Resolution', 'دقة الشاشة',
      '240x240, 320x320, 360x360, 396x484, 416x496, 466x466, 480x480, 502x410'),
    B('display', 'Always-On Display', 'شاشة دائمة العمل'),
    D('design', 'Case Size (mm)', 'مقاس الهيكل (ملم)',
      '38 mm, 40 mm, 41 mm, 42 mm, 44 mm, 45 mm, 46 mm, 47 mm, 49 mm', option='Yes'),
    D('design', 'Case Shape', 'شكل الهيكل', 'Round, Square, Rectangular, Oval'),
    D('mat', 'Case Material', 'خامة الهيكل',
      'Aluminium, Stainless Steel, Titanium, Plastic / Polycarbonate, '
      'Fibre-Reinforced Polymer, Ceramic'),
    D('mat', 'Strap Material', 'خامة السوار',
      'Silicone, Fluoroelastomer, Leather, Nylon / Fabric, Stainless Steel Link, '
      'Milanese Loop, Ocean Band, Woven Braided', option='Yes'),
    D('design', 'Strap Size', 'مقاس السوار', 'Small / Medium, Medium / Large, One Size, Adjustable'),
    B('design', 'Interchangeable Strap', 'سوار قابل للتبديل'),
    D('conn', 'Connectivity', 'الاتصال',
      'Bluetooth Only, Bluetooth + Wi-Fi, Bluetooth + Wi-Fi + GPS, '
      'LTE / Cellular (eSIM), NFC, ANT+'),
    B('conn', 'Built-In GPS', 'نظام تحديد المواقع مدمج'),
    # eXtra sells the GPS-only and GPS+Cellular variants as distinct SKUs, and lists
    # the watch SiP and RAM on the product page.
    D('conn', 'Cellular Support', 'دعم الشبكة الخلوية',
      'Not Supported, GPS Only, GPS + Cellular (eSIM)'),
    T('perf', 'Chipset / Processor', 'المعالج / الشريحة'),
    D('mem', 'RAM', 'الذاكرة العشوائية',
      '32 MB, 128 MB, 256 MB, 512 MB, 1 GB, 2 GB, Not Specified'),
    B('conn', 'NFC Payments', 'الدفع عبر NFC'),
    D('sensors', 'Health Sensors', 'مستشعرات الصحة',
      'Heart Rate, Blood Oxygen (SpO2), ECG / EKG, Body Temperature, '
      'Bioimpedance (Body Composition), Blood Pressure, Sleep Tracking, '
      'Stress Monitoring, Skin Temperature'),
    D('sensors', 'Motion Sensors', 'مستشعرات الحركة',
      'Accelerometer, Gyroscope, Compass / Magnetometer, Barometric Altimeter, '
      'Ambient Light Sensor, Depth Gauge'),
    I('feat', 'Sport Modes', 'أوضاع الرياضة',
      'Under 20 Modes, 20-50 Modes, 51-100 Modes, 101-150 Modes, Above 150 Modes'),
    D('batt', 'Battery Life (typical use)', 'عمر البطارية (استخدام معتاد)',
      'Up to 1 Day, 2-3 Days, 4-7 Days, 8-14 Days, 15-30 Days, Above 30 Days'),
    D('batt', 'Charging Method', 'طريقة الشحن',
      'Magnetic Charger, Wireless Qi, USB-C Cable, Pogo Pin, Solar Assisted'),
    D('safety', 'Water Resistance', 'مقاومة الماء',
      '3 ATM, 5 ATM, 10 ATM, 20 ATM, IP67, IP68, IP69K, MIL-STD-810H, Not Water Resistant'),
    B('feat', 'Calling Support (Speaker & Mic)', 'دعم المكالمات'),
    B('feat', 'Music Storage', 'تخزين الموسيقى'),
    D('storage', 'Internal Storage', 'التخزين الداخلي',
      'Not Available, 4 GB, 8 GB, 16 GB, 32 GB, 64 GB'),
    D('feat', 'Safety Features', 'ميزات السلامة',
      'Fall Detection, Crash Detection, Emergency SOS, Irregular Rhythm Alerts, '
      'Loud Sound Alerts, None'),
    D('usage', 'Gender / Target User', 'الفئة المستهدفة', 'Men, Women, Unisex, Kids'),
], COLOR, ELEC_COMMERCE)

# ------------------------------------------------------------------ game console
FAM['console'] = blk(IDENT, [
    D('spec', 'Console Type', 'نوع الجهاز',
      'Home Console, Handheld / Portable Console, Hybrid Console, '
      'Retro / Mini Console, Cloud Gaming Device', required='Yes'),
    D('spec', 'Console Edition', 'إصدار الجهاز',
      'Standard Edition, Digital Edition, Slim, Pro, Limited / Special Edition, Bundle'),
    D('storage', 'Storage Capacity', 'سعة التخزين',
      '32 GB, 64 GB, 256 GB, 500 GB, 512 GB, 825 GB, 1 TB, 2 TB',
      required='Yes', option='Yes'),
    D('storage', 'Storage Type', 'نوع التخزين', 'SSD, HDD, eMMC, Cartridge / Flash'),
    B('storage', 'Expandable Storage', 'تخزين قابل للتوسعة'),
    D('spec', 'Optical Drive', 'مشغّل الأقراص',
      'Blu-ray 4K UHD, Blu-ray, DVD, No Disc Drive, Detachable Disc Drive'),
    D('display', 'Maximum Resolution', 'أقصى دقة',
      '720p HD, 1080p Full HD, 1440p, 4K UHD, 8K UHD'),
    D('display', 'Maximum Frame Rate', 'أقصى معدل إطارات', '30 fps, 60 fps, 120 fps, 144 fps'),
    B('display', 'Ray Tracing Support', 'دعم تتبع الأشعة'),
    D('display', 'Built-In Screen', 'الشاشة المدمجة',
      'Not Applicable, 6.2 inch LCD, 7 inch LCD, 7 inch OLED, 7.9 inch LCD, 8 inch LCD'),
    D('conn', 'Connectivity', 'الاتصال',
      'Wi-Fi, Ethernet (LAN), Bluetooth, HDMI, USB-A, USB-C, 3.5mm Audio'),
    I('pack', 'Controllers Included', 'عدد أذرع التحكم المرفقة', '0, 1, 2, 3, 4'),
    B('pack', 'Games Included', 'يشمل ألعاباً'),
    T('pack', 'Included Game Titles', 'أسماء الألعاب المرفقة'),
    D('spec', 'Region', 'المنطقة', 'Region Free, UAE / Middle East, Europe (PAL), USA (NTSC), Japan, Asia'),
    D('spec', 'Backwards Compatibility', 'التوافق مع الأجيال السابقة',
      'Full Backwards Compatible, Partial, Not Supported'),
    B('feat', 'VR Ready', 'جاهز للواقع الافتراضي'),
    B('feat', 'Online Multiplayer Support', 'دعم اللعب الجماعي عبر الإنترنت'),
    I('power', 'Power Consumption (W)', 'استهلاك الطاقة (واط)',
      'Under 50 W, 50-100 W, 101-200 W, 201-350 W, Above 350 W'),
    D('batt', 'Battery Life (hours)', 'عمر البطارية (ساعة)',
      'Not Applicable, Up to 3 Hours, 3-5 Hours, 5-9 Hours, Above 9 Hours'),
], COLOR, ELEC_COMMERCE)

# ------------------------------------------------------------------ printer / office machine
FAM['printer'] = blk(IDENT, [
    D('spec', 'Printer Type', 'نوع الطابعة',
      'Inkjet, Ink Tank, Laser (Mono), Laser (Colour), LED, Thermal, Dot Matrix, '
      '3D Printer, Photo Printer, Label Printer, Plotter / Wide Format', required='Yes'),
    D('spec', 'Functions', 'الوظائف',
      'Print Only, Print & Scan, All-in-One (Print / Scan / Copy), '
      'All-in-One with Fax, Scan Only, Copy Only', required='Yes'),
    D('spec', 'Print Colour', 'لون الطباعة', 'Colour, Monochrome / Black & White'),
    D('spec', 'Maximum Paper Size', 'أقصى حجم ورق',
      'A4, A3, A3+, A2, A1, A0, Letter, Legal, 4x6 inch Photo'),
    D('perf', 'Print Speed (Mono ppm)', 'سرعة الطباعة (أبيض وأسود صفحة/دقيقة)',
      'Under 10 ppm, 10-20 ppm, 21-30 ppm, 31-40 ppm, 41-60 ppm, Above 60 ppm'),
    D('perf', 'Print Speed (Colour ppm)', 'سرعة الطباعة (ملون صفحة/دقيقة)',
      'Not Applicable, Under 10 ppm, 10-20 ppm, 21-30 ppm, 31-40 ppm, Above 40 ppm'),
    D('perf', 'Print Resolution (dpi)', 'دقة الطباعة',
      '600 x 600 dpi, 1200 x 1200 dpi, 2400 x 600 dpi, 4800 x 1200 dpi, 5760 x 1440 dpi'),
    D('perf', 'Scan Resolution (dpi)', 'دقة المسح الضوئي',
      'Not Applicable, 600 x 600 dpi, 1200 x 1200 dpi, 2400 x 2400 dpi, 4800 x 4800 dpi'),
    B('feat', 'Automatic Duplex (2-Sided) Printing', 'طباعة تلقائية على الوجهين'),
    B('feat', 'Automatic Document Feeder (ADF)', 'وحدة تغذية تلقائية للمستندات'),
    I('spec', 'Input Tray Capacity (sheets)', 'سعة درج الورق (ورقة)',
      '50 Sheets, 100 Sheets, 150 Sheets, 250 Sheets, 500 Sheets, Above 500 Sheets'),
    D('conn', 'Connectivity', 'الاتصال',
      'USB, Wi-Fi, Wi-Fi Direct, Ethernet (LAN), Bluetooth, NFC, Cloud Printing, '
      'Mobile Printing (AirPrint / Mopria)'),
    D('spec', 'Cartridge / Toner Type', 'نوع الحبر / التونر',
      'Individual Ink Cartridges, Combined Cartridge, Refillable Ink Tank, '
      'Toner Cartridge, Ribbon, Not Applicable'),
    I('spec', 'Number of Cartridges', 'عدد الخراطيش', '1, 2, 3, 4, 5, 6, 8'),
    I('perf', 'Monthly Duty Cycle (pages)', 'دورة العمل الشهرية (صفحة)',
      'Up to 1000, 1001-5000, 5001-20000, 20001-50000, Above 50000'),
    I('perf', 'Page Yield (black)', 'إنتاجية الصفحات (أسود)',
      'Under 1000, 1000-3000, 3001-6000, 6001-12000, Above 12000'),
    D('display', 'Control Panel', 'لوحة التحكم',
      'LED Indicators, Mono LCD, Colour LCD, Touchscreen, No Display'),
    B('feat', 'Borderless Printing', 'طباعة بدون حواف'),
    B('feat', 'Mobile App Support', 'دعم تطبيق الجوال'),
    D('power', 'Power Consumption (W)', 'استهلاك الطاقة (واط)',
      'Under 20 W, 20-50 W, 51-100 W, 101-400 W, Above 400 W'),
    D('usage', 'Recommended Use', 'الاستخدام الموصى به',
      'Home Use, Home Office, Small Office, Medium Business, Enterprise, '
      'Photo Printing, Commercial Printing'),
], COLOR, ELEC_COMMERCE)

# ------------------------------------------------------------------ networking
FAM['network'] = blk(IDENT, [
    D('spec', 'Device Type', 'نوع الجهاز',
      'Wi-Fi Router, Mesh Wi-Fi System, Range Extender / Repeater, Access Point, '
      'Network Switch, Modem, Modem-Router Combo, Powerline Adapter, '
      'Network Card / Adapter, Firewall, 4G/5G Portable Router', required='Yes'),
    D('conn', 'Wi-Fi Standard', 'معيار الواي فاي',
      'Wi-Fi 4 (802.11n), Wi-Fi 5 (802.11ac), Wi-Fi 6 (802.11ax), Wi-Fi 6E, '
      'Wi-Fi 7 (802.11be), Not Applicable'),
    D('perf', 'Wi-Fi Speed', 'سرعة الواي فاي',
      'AC750, AC1200, AC1750, AC2100, AX1500, AX1800, AX3000, AX5400, AX6000, '
      'AX11000, BE3600, BE9300, BE19000'),
    D('conn', 'Frequency Bands', 'نطاقات التردد',
      'Single Band (2.4 GHz), Dual Band (2.4 + 5 GHz), Tri-Band, Quad-Band'),
    I('conn', 'Number of LAN Ports', 'عدد منافذ LAN', '0, 1, 2, 3, 4, 5, 8, 16, 24, 48'),
    D('conn', 'Ethernet Port Speed', 'سرعة منافذ الإيثرنت',
      '10/100 Mbps, 1 Gbps, 2.5 Gbps, 5 Gbps, 10 Gbps'),
    I('conn', 'Number of Antennas', 'عدد الهوائيات', '0 (Internal), 2, 3, 4, 6, 8, 12'),
    D('conn', 'Antenna Type', 'نوع الهوائي', 'Internal, External Fixed, External Detachable'),
    N('spec', 'Coverage Area (m²)', 'مساحة التغطية (م²)',
      'Up to 100 m², 101-200 m², 201-350 m², 351-500 m², Above 500 m²'),
    I('spec', 'Supported Devices', 'عدد الأجهزة المدعومة',
      'Up to 20, 21-40, 41-80, 81-150, Above 150'),
    D('feat', 'Security Protocols', 'بروتوكولات الأمان',
      'WEP, WPA, WPA2, WPA3, WPA2/WPA3 Mixed, Enterprise Security'),
    B('feat', 'Guest Network', 'شبكة الضيوف'),
    B('feat', 'Parental Controls', 'الرقابة الأبوية'),
    B('feat', 'VPN Support', 'دعم VPN'),
    B('feat', 'Mesh Support', 'دعم شبكة Mesh'),
    B('feat', 'MU-MIMO', 'تقنية MU-MIMO'),
    B('feat', 'Beamforming', 'تقنية Beamforming'),
    B('feat', 'App Management', 'إدارة عبر التطبيق'),
    D('conn', 'SIM Support', 'دعم شريحة الاتصال',
      'Not Applicable, Nano SIM, Micro SIM, Standard SIM, eSIM'),
    D('conn', 'Cellular Network', 'شبكة الاتصال',
      'Not Applicable, 3G, 4G LTE, 5G, 5G Advanced'),
    D('power', 'Power Source', 'مصدر الطاقة',
      'AC Adapter, PoE (Power over Ethernet), USB Powered, Built-In Battery'),
    D('inst', 'Mounting', 'التركيب', 'Desktop, Wall Mount, Rack Mount, Ceiling Mount, Portable'),
], COLOR, ELEC_COMMERCE)

# ------------------------------------------------------------------ storage device
FAM['storage_device'] = blk(IDENT, [
    D('spec', 'Storage Type', 'نوع وحدة التخزين',
      'USB Flash Drive, microSD Card, SD Card, CompactFlash, CFexpress, '
      'External HDD, External SSD, Internal SSD (SATA), Internal SSD (NVMe M.2), '
      'Internal HDD, NAS Drive, Optical Disc', required='Yes'),
    D('spec', 'Capacity', 'السعة',
      '8 GB, 16 GB, 32 GB, 64 GB, 128 GB, 256 GB, 512 GB, 1 TB, 2 TB, 4 TB, '
      '8 TB, 12 TB, 16 TB, 20 TB', required='Yes', option='Yes'),
    D('conn', 'Interface', 'الواجهة',
      'USB 2.0, USB 3.0 / 3.2 Gen 1, USB 3.2 Gen 2, USB 3.2 Gen 2x2, USB4, '
      'Thunderbolt 3, Thunderbolt 4, SATA III, PCIe 3.0 x4, PCIe 4.0 x4, PCIe 5.0 x4, '
      'UHS-I, UHS-II, UHS-III'),
    D('perf', 'Read Speed', 'سرعة القراءة',
      'Up to 100 MB/s, Up to 200 MB/s, Up to 550 MB/s, Up to 1050 MB/s, '
      'Up to 2000 MB/s, Up to 3500 MB/s, Up to 5000 MB/s, Up to 7000 MB/s, Up to 14000 MB/s'),
    D('perf', 'Write Speed', 'سرعة الكتابة',
      'Up to 50 MB/s, Up to 100 MB/s, Up to 500 MB/s, Up to 1000 MB/s, '
      'Up to 2000 MB/s, Up to 3300 MB/s, Up to 6900 MB/s, Up to 12000 MB/s'),
    D('perf', 'Speed Class (Cards)', 'فئة السرعة (البطاقات)',
      'Not Applicable, Class 10, U1, U3, V10, V30, V60, V90, A1, A2'),
    D('spec', 'Form Factor', 'الشكل',
      '2.5 inch, 3.5 inch, M.2 2280, M.2 2242, mSATA, Stick / Portable, '
      'Card, Pocket Size, Not Applicable'),
    N('perf', 'RPM (HDD)', 'سرعة الدوران (قرص صلب)',
      'Not Applicable, 5400 RPM, 5900 RPM, 7200 RPM, 10000 RPM', dtype='Integer'),
    D('spec', 'NAND Type', 'نوع الذاكرة',
      'Not Applicable, SLC, MLC, TLC, QLC, 3D NAND, 3D V-NAND'),
    B('feat', 'Hardware Encryption', 'تشفير عتادي'),
    B('feat', 'Password Protection', 'حماية بكلمة مرور'),
    B('safety', 'Shock Resistant', 'مقاوم للصدمات'),
    D('safety', 'Water & Dust Resistance', 'مقاومة الماء والغبار', IP_RATING),
    D('compat', 'Compatible With', 'التوافق',
      'Windows, macOS, Linux, Android, iOS / iPadOS, PlayStation, Xbox, '
      'Smart TV, Cameras, Drones, Universal'),
    D('perf', 'Endurance (TBW)', 'التحمل (تيرابايت مكتوبة)',
      'Not Specified, Under 150 TBW, 150-300 TBW, 301-600 TBW, 601-1200 TBW, Above 1200 TBW'),
    B('pack', 'Cable Included', 'يشمل كابل'),
    B('pack', 'Adapter Included', 'يشمل محوّل'),
], COLOR, ELEC_COMMERCE)

# ------------------------------------------------------------------ power bank
FAM['powerbank'] = blk(IDENT, [
    D('cap', 'Battery Capacity (mAh)', 'سعة البطارية (مللي أمبير/ساعة)',
      '5000 mAh, 10000 mAh, 15000 mAh, 20000 mAh, 25000 mAh, 26800 mAh, '
      '30000 mAh, 40000 mAh, 50000 mAh', required='Yes', option='Yes'),
    N('cap', 'Energy Capacity (Wh)', 'الطاقة (واط/ساعة)',
      'Under 20 Wh, 20-40 Wh, 41-75 Wh, 76-100 Wh, 101-160 Wh, Above 160 Wh'),
    D('power', 'Maximum Output Power (W)', 'أقصى قدرة إخراج (واط)',
      '10 W, 15 W, 18 W, 20 W, 22.5 W, 30 W, 45 W, 65 W, 100 W, 140 W, 200 W, 300 W',
      required='Yes'),
    D('power', 'Fast Charging Standard', 'معيار الشحن السريع',
      'USB Power Delivery (PD), PD 3.0, PD 3.1, Quick Charge 3.0, Quick Charge 4+, '
      'Super Fast Charging, SuperVOOC, SuperCharge, None'),
    I('conn', 'Number of Output Ports', 'عدد منافذ الإخراج', '1, 2, 3, 4, 5, 6'),
    D('conn', 'Output Ports', 'منافذ الإخراج',
      'USB-A, USB-C, Micro USB, Lightning, AC Socket, DC Output, Built-In Cable'),
    D('conn', 'Input Port', 'منفذ الإدخال', 'USB-C, Micro USB, Lightning, DC Barrel, Solar'),
    B('feat', 'Wireless Charging', 'شحن لاسلكي'),
    B('feat', 'MagSafe / Magnetic', 'مغناطيسي / MagSafe'),
    B('feat', 'Built-In Cable', 'كابل مدمج'),
    B('feat', 'Pass-Through Charging', 'الشحن أثناء الشحن'),
    D('display', 'Display Type', 'نوع المؤشر',
      'LED Indicators, Digital LCD Display, OLED Display, No Display'),
    D('batt', 'Cell Type', 'نوع الخلايا', 'Li-Ion, Li-Polymer, LiFePO4, Silicon-Carbon'),
    B('safety', 'Airline Approved', 'مسموح على متن الطائرة'),
    D('safety', 'Safety Protections', 'وسائل الحماية',
      'Over-Charge Protection, Over-Discharge Protection, Short Circuit Protection, '
      'Over-Current Protection, Temperature Control, Multi-Protect System'),
    B('feat', 'Solar Charging', 'شحن بالطاقة الشمسية'),
    B('feat', 'Built-In Flashlight', 'كشاف مدمج'),
    D('mat', 'Housing Material', 'خامة الهيكل',
      'ABS Plastic, Aluminium Alloy, Metal, Silicone, Fabric, Rubberised'),
    D('usage', 'Recommended Use', 'الاستخدام الموصى به',
      'Phones, Tablets, Laptops, Cameras, Travel, Camping & Outdoor, Emergency Backup'),
], COLOR, ELEC_COMMERCE)
