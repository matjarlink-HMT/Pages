# -*- coding: utf-8 -*-
"""Home: major & small appliances, lighting, furniture, kitchenware, textiles, cleaning."""
from lib_core import *

FAM = {}

APPLIANCE_COMMON = [
    D('power', 'Voltage', 'الجهد الكهربائي',
      '220-240 V, 110-120 V, 100-240 V (Dual Voltage), 380-415 V (3-Phase)'),
    D('power', 'Frequency', 'التردد', '50 Hz, 60 Hz, 50/60 Hz'),
    I('power', 'Power Consumption (W)', 'استهلاك الطاقة (واط)',
      'Under 500 W, 500-1000 W, 1001-1500 W, 1501-2000 W, 2001-3000 W, Above 3000 W'),
    D('power', 'Plug Type', 'نوع القابس',
      'UK 3-Pin (G-Type), EU 2-Pin (F-Type), US 2-Pin (A/B-Type), '
      'Indian (D-Type), Hardwired, Universal'),
    D('env', 'Energy Efficiency Class', 'فئة كفاءة الطاقة', ENERGY),
    I('feat', 'Noise Level (dB)', 'مستوى الضوضاء (ديسيبل)',
      'Under 40 dB, 40-50 dB, 51-60 dB, 61-70 dB, Above 70 dB'),
    D('inst', 'Installation Type', 'نوع التركيب',
      'Freestanding, Built-In, Semi Built-In, Wall Mounted, Countertop, Under Counter'),
    T('dims', 'Product Dimensions (L x W x H cm)', 'أبعاد المنتج (طول×عرض×ارتفاع سم)'),
    D('feat', 'Control Type', 'نوع التحكم',
      'Mechanical Knob, Push Button, Touch Control, Digital Display, '
      'Smart / App Control, Remote Control'),
    B('smart', 'Smart / Wi-Fi Enabled', 'ذكي / يدعم الواي فاي'),
]

# ------------------------------------------------------------------ washing machine
# Verified 2026-08-10 against eXtra's washer classifications (AUTO FL, AUTO FE,
# TWIN TUB WASHER, WASHER&DRYER), sampled from 13 live product pages under
# https://www.extra.com/en-sa/large-appliances-/washing-machines/
FAM['washer'] = blk(IDENT, [
    D('spec', 'Machine Type', 'نوع الغسالة',
      'Front Load, Top Load (Automatic), Top Load (Twin Tub / Semi-Automatic), '
      'Washer Dryer Combo, Dryer Only, Portable / Mini Washer', required='Yes'),
    # eXtra keeps loading direction, drum construction and automation level as three
    # separate attributes rather than folding them into one machine type.
    D('spec', 'Loading Type', 'نوع التحميل', 'Front Loading, Top Loading'),
    D('spec', 'Operation Type', 'نوع التشغيل',
      'Fully Automatic, Semi Automatic, Manual'),
    D('spec', 'Tub Type', 'نوع الحوض', 'Single Drum, Twin Tub'),
    D('cap', 'Washing Capacity (kg)', 'سعة الغسيل (كجم)',
      '5 kg, 6 kg, 7 kg, 8 kg, 9 kg, 10 kg, 11 kg, 12 kg, 13 kg, 15 kg, 20 kg, 25 kg',
      required='Yes', option='Yes'),
    D('cap', 'Drying Capacity (kg)', 'سعة التجفيف (كجم)',
      'Not Applicable, 4 kg, 5 kg, 6 kg, 7 kg, 8 kg, 9 kg, 10 kg'),
    D('perf', 'Maximum Spin Speed (RPM)', 'أقصى سرعة عصر (دورة/دقيقة)',
      '400 RPM, 600 RPM, 800 RPM, 1000 RPM, 1200 RPM, 1400 RPM, 1600 RPM',
      required='Yes'),
    I('feat', 'Number of Wash Programs', 'عدد برامج الغسيل',
      'Under 8, 8-12, 13-16, 17-22, Above 22'),
    D('feat', 'Wash Programs', 'برامج الغسيل',
      'Cotton, Synthetics, Delicates, Wool, Quick Wash, Eco / Energy Saving, '
      'Baby Care, Sportswear, Bedding / Duvet, Steam Wash, Drum Clean, '
      'Anti-Allergy, Heavy Duty, Rinse & Spin'),
    D('perf', 'Motor Type', 'نوع المحرك',
      'Inverter Direct Drive, Digital Inverter, Brushless DC Inverter, Belt Drive, Universal Motor'),
    B('feat', 'Steam Function', 'وظيفة البخار'),
    B('feat', 'Built-in Water Heater', 'سخّان مياه مدمج'),
    B('feat', 'Stackable', 'قابلة للتركيب فوق بعضها'),
    B('feat', 'Pedestal Available', 'قاعدة متوفرة'),
    D('perf', 'Drying Performance (Combo)', 'أداء التجفيف (غسالة نشافة)',
      'Not Applicable, Dry up to 65%, Dry 100%, All-in-One Unit'),
    D('warr', 'Motor Warranty', 'ضمان المحرك',
      'No Warranty, 1 Year, 2 Years, 5 Years, 10 Years, 20 Years'),
    B('feat', 'Child Lock', 'قفل الأطفال'),
    B('feat', 'Delay Start Timer', 'مؤقت بدء مؤجل'),
    B('feat', 'Auto Dosing / Detergent Dispenser', 'موزّع منظفات تلقائي'),
    B('feat', 'Add Item Mid-Cycle', 'إضافة ملابس أثناء الدورة'),
    B('feat', 'Anti-Vibration System', 'نظام مضاد للاهتزاز'),
    B('feat', 'Self-Diagnosis', 'التشخيص الذاتي'),
    B('feat', 'Drum Clean Cycle', 'دورة تنظيف الحلة'),
    D('mat', 'Drum Material', 'خامة الحلة',
      'Stainless Steel, Porcelain Enamel, Plastic / Polypropylene, Diamond Drum'),
    I('env', 'Water Consumption (L/cycle)', 'استهلاك الماء (لتر/دورة)',
      'Under 40 L, 40-55 L, 56-70 L, 71-90 L, Above 90 L'),
    I('env', 'Annual Energy Consumption (kWh)', 'استهلاك الطاقة السنوي (كيلوواط ساعة)',
      'Under 150 kWh, 150-200 kWh, 201-250 kWh, Above 250 kWh'),
    D('display', 'Display Type', 'نوع الشاشة', 'No Display, LED Display, LCD Display, Touch Display'),
], APPLIANCE_COMMON, COLOR, ELEC_COMMERCE)

# ------------------------------------------------------------------ refrigerator
# Verified 2026-08-10 against eXtra's refrigerator classifications (LARGE, MEDIUM,
# SMALL, COMPACT, SIDE BY SIDE REFRIGERATOR), sampled from 13 live product pages under
# https://www.extra.com/en-sa/large-appliances-/refrigerators/
FAM['fridge'] = blk(IDENT, [
    D('spec', 'Refrigerator Type', 'نوع الثلاجة',
      'Top Mount Freezer, Bottom Mount Freezer, Side by Side, French Door, '
      'Multi Door, Single Door, Mini / Compact Fridge, Chest Freezer, '
      'Upright Freezer, Wine Cooler, Beverage Cooler', required='Yes'),
    D('cap', 'Total Capacity (Litres)', 'السعة الإجمالية (لتر)',
      'Under 100 L, 100-200 L, 201-300 L, 301-400 L, 401-500 L, 501-600 L, '
      '601-700 L, 701-800 L, Above 800 L', required='Yes', option='Yes'),
    N('cap', 'Total Capacity (Cubic Feet)', 'السعة الإجمالية (قدم مكعب)',
      'Under 5 cu.ft, 5-10 cu.ft, 11-15 cu.ft, 16-20 cu.ft, 21-25 cu.ft, Above 25 cu.ft'),
    N('cap', 'Fridge Compartment (Litres)', 'سعة قسم التبريد (لتر)',
      'Under 100 L, 100-200 L, 201-300 L, 301-400 L, Above 400 L'),
    N('cap', 'Freezer Compartment (Litres)', 'سعة قسم التجميد (لتر)',
      'Under 50 L, 50-100 L, 101-150 L, 151-250 L, Above 250 L'),
    # eXtra publishes every Gulf fridge capacity in cubic feet, split three ways
    # (net total / net refrigerator / net freezer) -- that is how shoppers compare here.
    N('cap', 'Fridge Compartment (Cubic Feet)', 'سعة قسم التبريد (قدم مكعب)',
      'Under 5 cu.ft, 5-8 cu.ft, 8.1-11 cu.ft, 11.1-14 cu.ft, 14.1-18 cu.ft, '
      'Above 18 cu.ft'),
    N('cap', 'Freezer Compartment (Cubic Feet)', 'سعة قسم التجميد (قدم مكعب)',
      'Under 2 cu.ft, 2-3.5 cu.ft, 3.6-5 cu.ft, 5.1-7 cu.ft, Above 7 cu.ft'),
    D('spec', 'Defrost System', 'نظام إزالة الثلج',
      'No Frost / Frost Free, Direct Cool / Manual Defrost, Total No Frost, Auto Defrost'),
    D('spec', 'Cooling System', 'نظام التبريد',
      'Twin Cooling, Multi Air Flow, Linear Cooling, Dual Fan, Single Fan'),
    D('perf', 'Compressor Type', 'نوع الضاغط',
      'Inverter Compressor, Linear Inverter, Digital Inverter, Standard Compressor, '
      'Dual Inverter'),
    I('spec', 'Number of Doors', 'عدد الأبواب', '1, 2, 3, 4, 5'),
    B('feat', 'Water Dispenser', 'موزّع مياه'),
    B('feat', 'Through-the-Door Dispenser', 'موزّع عبر الباب'),
    B('feat', 'Ice Maker', 'صانعة ثلج'),
    B('feat', 'Water Filter', 'فلتر مياه'),
    B('feat', 'Digital Temperature Control', 'تحكم رقمي بدرجة الحرارة'),
    # Attributes eXtra records on every refrigerator listing.
    D('spec', 'Thermostat Type', 'نوع الثرموستات',
      'Digital, Electronic Control, Touch Panel, Mechanical / Manual'),
    B('feat', 'Fast Freeze', 'التجميد السريع'),
    B('feat', 'Multi Air Flow Technology', 'تقنية تدفق الهواء المتعدد'),
    B('feat', 'Adjustable Shelves', 'أرفف قابلة للتعديل'),
    B('feat', 'Adjustable Levelling Legs', 'أرجل قابلة للتسوية'),
    B('feat', 'Door-in-Door', 'باب داخل باب'),
    B('feat', 'Built-in Screen / TV', 'شاشة مدمجة'),
    B('feat', 'Interior Camera', 'كاميرا داخلية'),
    D('spec', 'Interior Lighting Type', 'نوع الإضاءة الداخلية',
      'LED, Incandescent, None'),
    D('warr', 'Compressor Warranty', 'ضمان الضاغط',
      'No Warranty, 1 Year, 2 Years, 5 Years, 7 Years, 10 Years, 12 Years'),
    B('feat', 'Door Alarm', 'إنذار الباب'),
    B('feat', 'Child Lock', 'قفل الأطفال'),
    B('feat', 'Deodoriser / Air Filter', 'مزيل روائح / فلتر هواء'),
    B('feat', 'Vacation Mode', 'وضع الإجازة'),
    B('feat', 'Convertible Freezer', 'فريزر قابل للتحويل'),
    B('feat', 'Reversible Door', 'باب قابل لعكس الاتجاه'),
    I('spec', 'Number of Shelves', 'عدد الأرفف', '2, 3, 4, 5, 6, 7, 8'),
    D('mat', 'Shelf Material', 'خامة الأرفف', 'Tempered Glass, Wire / Metal, Plastic, Spill-Proof Glass'),
    D('mat', 'Door Finish', 'تشطيب الباب',
      'Stainless Steel, Fingerprint-Resistant Steel, Painted Steel, Glass Door, '
      'Matte Finish, Black Steel, Mirror Finish'),
    D('spec', 'Climate Class', 'الفئة المناخية', 'N (Normal), ST (Subtropical), T (Tropical), SN-T'),
    D('spec', 'Refrigerant Type', 'نوع غاز التبريد', 'R600a, R134a, R290, R32'),
    I('env', 'Annual Energy Consumption (kWh)', 'استهلاك الطاقة السنوي (كيلوواط ساعة)',
      'Under 200 kWh, 200-350 kWh, 351-500 kWh, 501-700 kWh, Above 700 kWh'),
], APPLIANCE_COMMON, COLOR, ELEC_COMMERCE)

# ------------------------------------------------------------------ air conditioner
# Verified 2026-08-10 against eXtra's AC classifications (MINI SPLIT AIR CONDITIONER,
# WINDOW AIR CONDITIONER), sampled from 13 live product pages under
# https://www.extra.com/en-sa/large-appliances-/air-conditioner/
FAM['ac'] = blk(IDENT, [
    D('spec', 'Air Conditioner Type', 'نوع المكيّف',
      'Split Wall Mounted, Window AC, Portable AC, Cassette AC, Ducted / Central, '
      'Floor Standing, Tower AC, Multi-Split, VRF System, Air Cooler', required='Yes'),
    D('cap', 'Cooling Capacity (BTU/hr)', 'قدرة التبريد (وحدة حرارية/ساعة)',
      '9000 BTU, 12000 BTU, 18000 BTU, 24000 BTU, 30000 BTU, 36000 BTU, '
      '42000 BTU, 48000 BTU, 60000 BTU', required='Yes', option='Yes'),
    N('cap', 'Cooling Capacity (Tons)', 'قدرة التبريد (طن)',
      '0.75 Ton, 1 Ton, 1.5 Ton, 2 Ton, 2.5 Ton, 3 Ton, 4 Ton, 5 Ton'),
    N('spec', 'Suitable Room Size (m²)', 'مساحة الغرفة المناسبة (م²)',
      'Up to 15 m², 16-25 m², 26-35 m², 36-50 m², 51-75 m², Above 75 m²'),
    D('perf', 'Compressor Type', 'نوع الضاغط',
      'Inverter, Dual Inverter, Rotary, Scroll, Fixed Speed / Non-Inverter'),
    D('spec', 'Function', 'الوظيفة',
      'Cooling Only, Cooling & Heating (Heat Pump), Cooling / Heating / Dehumidify'),
    D('env', 'Energy Efficiency Ratio (EER / SEER)', 'معامل كفاءة الطاقة',
      'Under 9 EER, 9-11 EER, 11.1-13 EER, 13.1-16 SEER, 16.1-20 SEER, Above 20 SEER'),
    D('spec', 'Refrigerant Type', 'نوع غاز التبريد', 'R32, R410A, R22, R290, R454B'),
    B('feat', 'Wi-Fi / Smart Control', 'تحكم ذكي عبر الواي فاي'),
    B('feat', 'Remote Control Included', 'يشمل جهاز تحكم عن بعد'),
    B('feat', 'Sleep Mode', 'وضع النوم'),
    B('feat', 'Auto Restart', 'إعادة تشغيل تلقائية'),
    B('feat', 'Turbo / Fast Cooling', 'تبريد سريع'),
    B('feat', 'Self-Cleaning', 'تنظيف ذاتي'),
    B('feat', 'Anti-Bacterial Filter', 'فلتر مضاد للبكتيريا'),
    B('feat', 'Dehumidifier Function', 'وظيفة إزالة الرطوبة'),
    B('feat', 'Air Purification', 'تنقية الهواء'),
    # eXtra records swing as a direction count (2 Ways / 4 Ways), not a yes/no flag.
    D('feat', 'Air Swing Direction', 'اتجاه توزيع الهواء',
      'Not Available, 2-Way Swing, 3-Way Swing, 4-Way Swing, Auto Swing'),
    B('feat', 'Timer Function', 'وظيفة المؤقّت'),
    B('inst', 'Installation Required', 'يتطلب تركيباً'),
    B('inst', 'Installation Hardware Included', 'يشمل مستلزمات التركيب'),
    B('inst', 'Free Installation Included', 'يشمل تركيباً مجانياً'),
    D('warr', 'Compressor Warranty', 'ضمان الضاغط',
      'No Warranty, 1 Year, 2 Years, 5 Years, 7 Years, 10 Years'),
    I('feat', 'Number of Fan Speeds', 'عدد سرعات المروحة', '2, 3, 4, 5, Auto'),
    D('feat', 'Filter Type', 'نوع الفلتر',
      'Standard Mesh, HEPA, Carbon, Anti-Dust, Silver Ion, PM2.5, Multi-Layer'),
    D('spec', 'Operating Temperature Range', 'نطاق درجة حرارة التشغيل',
      'Up to 43°C, Up to 48°C, Up to 52°C, Up to 55°C (Tropical / T3)'),
    B('cert', 'T3 / Tropical Rated', 'مطابق للمناخ الحار (T3)'),
], APPLIANCE_COMMON, COLOR, ELEC_COMMERCE)

# ------------------------------------------------------------------ cooking appliance
FAM['cooking_appliance'] = blk(IDENT, [
    D('spec', 'Appliance Type', 'نوع الجهاز',
      'Gas Cooker, Electric Cooker, Built-In Oven, Built-In Hob, Microwave Oven, '
      'Microwave with Grill, Convection Microwave, Air Fryer, Deep Fryer, '
      'Electric Pressure Cooker, Rice Cooker, Slow Cooker, Toaster, Sandwich Maker, '
      'Waffle Maker, Electric Grill, Induction Cooker, Hot Plate, Steamer, Bread Maker',
      required='Yes'),
    N('cap', 'Capacity (Litres)', 'السعة (لتر)',
      '0.5 L, 1 L, 1.5 L, 2 L, 3 L, 4 L, 5 L, 6 L, 8 L, 10 L, 20 L, 25 L, 30 L, '
      '42 L, 60 L, 70 L, 90 L, 110 L', option='Yes'),
    D('power', 'Power (Watts)', 'القدرة (واط)',
      '600 W, 800 W, 1000 W, 1200 W, 1500 W, 1800 W, 2000 W, 2200 W, 2500 W, 3000 W'),
    D('spec', 'Energy Source', 'مصدر الطاقة',
      'Electric, Gas, Dual Fuel (Gas + Electric), Induction, Battery, Charcoal'),
    I('spec', 'Number of Burners / Zones', 'عدد الشعلات / المناطق', '1, 2, 3, 4, 5, 6'),
    D('spec', 'Burner Type', 'نوع الشعلات',
      'Not Applicable, Gas Burners, Ceramic / Radiant, Induction Zones, '
      'Solid Hotplate, Halogen'),
    D('feat', 'Heating Functions', 'وظائف التسخين',
      'Bake, Grill, Fan / Convection, Rotisserie, Defrost, Steam, Air Fry, '
      'Pizza Mode, Keep Warm, Slow Cook, Reheat, Toast'),
    D('spec', 'Temperature Range', 'نطاق درجة الحرارة',
      'Up to 200°C, Up to 230°C, Up to 250°C, Up to 280°C, Up to 300°C'),
    D('feat', 'Timer', 'المؤقّت',
      'No Timer, Mechanical Timer, Digital Timer, Programmable Delay Start'),
    B('feat', 'Rotisserie', 'سيخ الشواء الدوّار'),
    B('feat', 'Convection Fan', 'مروحة الحمل الحراري'),
    B('feat', 'Auto Cook Menus', 'قوائم طهي تلقائية'),
    I('feat', 'Number of Auto Programs', 'عدد البرامج التلقائية',
      'Under 5, 5-10, 11-20, 21-30, Above 30'),
    B('feat', 'Child Safety Lock', 'قفل أمان الأطفال'),
    B('feat', 'Auto Ignition', 'إشعال تلقائي'),
    B('feat', 'Flame Failure Safety Device', 'جهاز أمان انقطاع الغاز'),
    B('feat', 'Non-Stick Interior', 'طلاء داخلي غير لاصق'),
    B('feat', 'Self-Cleaning / Catalytic Liner', 'تنظيف ذاتي'),
    B('feat', 'Cool Touch Exterior', 'سطح خارجي بارد الملمس'),
    B('pack', 'Accessories Included (Trays / Racks)', 'يشمل ملحقات (صواني / شبكات)'),
    D('mat', 'Body Material', 'خامة الهيكل',
      'Stainless Steel, Painted Steel, Glass, Plastic / ABS, Enamel, Aluminium'),
    D('mat', 'Inner Pot / Cavity Material', 'خامة الوعاء الداخلي',
      'Stainless Steel, Non-Stick Coated, Ceramic Coated, Enamel, Glass, Aluminium'),
], APPLIANCE_COMMON, COLOR, ELEC_COMMERCE)

# ------------------------------------------------------------------ small kitchen appliance
FAM['small_appliance'] = blk(IDENT, [
    D('spec', 'Appliance Type', 'نوع الجهاز',
      'Blender, Hand Blender, Food Processor, Stand Mixer, Hand Mixer, Juicer, '
      'Citrus Juicer, Coffee Machine, Espresso Machine, Drip Coffee Maker, '
      'Capsule Coffee Machine, Electric Kettle, Tea Maker, Water Dispenser, '
      'Grinder, Chopper, Ice Maker, Yoghurt Maker, Milk Frother', required='Yes'),
    D('power', 'Power (Watts)', 'القدرة (واط)',
      '150 W, 300 W, 400 W, 500 W, 600 W, 800 W, 1000 W, 1200 W, 1500 W, 1800 W, 2200 W'),
    N('cap', 'Capacity (Litres)', 'السعة (لتر)',
      '0.3 L, 0.5 L, 0.75 L, 1 L, 1.5 L, 1.7 L, 2 L, 2.5 L, 3 L, 5 L', option='Yes'),
    I('feat', 'Number of Speed Settings', 'عدد سرعات التشغيل', '1, 2, 3, 5, 6, 8, 10, Variable'),
    B('feat', 'Pulse Function', 'وظيفة النبض'),
    B('feat', 'Variable Speed Control', 'تحكم متدرج بالسرعة'),
    D('mat', 'Jar / Jug Material', 'خامة الإبريق',
      'Not Applicable, Glass, Tritan Plastic, BPA-Free Plastic, Stainless Steel, Borosilicate Glass'),
    D('mat', 'Blade Material', 'خامة الشفرات',
      'Not Applicable, Stainless Steel, Japanese Stainless Steel, Titanium Coated, Ceramic'),
    B('feat', 'Dishwasher Safe Parts', 'أجزاء آمنة للغسالة'),
    B('feat', 'BPA Free', 'خالٍ من البيسفينول A'),
    B('feat', 'Overheat Protection', 'حماية من السخونة الزائدة'),
    B('feat', 'Auto Shut-Off', 'إيقاف تلقائي'),
    B('feat', 'Non-Slip Feet', 'قاعدة مانعة للانزلاق'),
    B('feat', 'Cord Storage', 'مكان لحفظ السلك'),
    D('feat', 'Water Temperature Control', 'التحكم بحرارة الماء',
      'Not Applicable, Fixed 100°C, Variable Temperature, Keep Warm Function'),
    D('spec', 'Coffee Type Supported', 'أنواع القهوة المدعومة',
      'Not Applicable, Ground Coffee, Coffee Beans, Capsules / Pods, ESE Pods, Instant'),
    I('spec', 'Pump Pressure (Bar)', 'ضغط المضخة (بار)',
      'Not Applicable, 3 Bar, 5 Bar, 15 Bar, 19 Bar, 20 Bar'),
    B('pack', 'Attachments Included', 'يشمل ملحقات'),
    T('pack', 'Included Attachments', 'الملحقات المرفقة'),
    D('mat', 'Body Material', 'خامة الهيكل',
      'ABS Plastic, Stainless Steel, Die-Cast Metal, Glass, Ceramic'),
], APPLIANCE_COMMON, COLOR, ELEC_COMMERCE)

# ------------------------------------------------------------------ vacuum / floor care
FAM['vacuum'] = blk(IDENT, [
    D('spec', 'Vacuum Type', 'نوع المكنسة',
      'Canister / Cylinder, Upright, Stick / Cordless, Handheld, Robot Vacuum, '
      'Wet & Dry, Backpack, Central Vacuum, Steam Mop, Carpet Washer', required='Yes'),
    D('power', 'Power (Watts)', 'القدرة (واط)',
      '600 W, 1000 W, 1200 W, 1600 W, 1800 W, 2000 W, 2200 W, 2400 W, Not Applicable'),
    I('perf', 'Suction Power (Pa / AW)', 'قوة الشفط',
      'Under 5000 Pa, 5000-10000 Pa, 10001-20000 Pa, 20001-30000 Pa, Above 30000 Pa'),
    D('spec', 'Dust Collection', 'طريقة تجميع الغبار',
      'Bagless Cyclonic, Dust Bag, Water Filtration, Self-Emptying Base'),
    N('cap', 'Dust Capacity (Litres)', 'سعة الغبار (لتر)',
      '0.3 L, 0.5 L, 0.8 L, 1 L, 1.5 L, 2 L, 3 L, 5 L, 10 L, 20 L, 30 L'),
    # eXtra lists the drum/bag construction, the clean-water tank on wet & dry and
    # mopping units, and whether the wand is a telescopic metal tube.
    D('spec', 'Bag / Drum Type', 'نوع الكيس / الحوض',
      'Bagless, Dust Bag, Drum, Cloth Bag'),
    N('cap', 'Water Tank Capacity (Litres)', 'سعة خزان المياه (لتر)',
      'Not Applicable, 0.2 L, 0.3 L, 0.5 L, 0.85 L, 1 L, 2 L, 3.7 L, 5 L'),
    D('design', 'Telescopic Tube', 'أنبوب تلسكوبي',
      'Not Available, Plastic Telescopic, Metal Telescopic'),
    D('mat', 'Body Material', 'خامة الهيكل',
      'ABS Plastic, Plastic, Metal, Metal & Plastic, Stainless Steel'),
    D('spec', 'Filter Type', 'نوع الفلتر',
      'HEPA 13, HEPA 14, Washable Filter, Foam Filter, Carbon Filter, '
      'Multi-Cyclone, Standard Filter'),
    D('power', 'Power Source', 'مصدر الطاقة',
      'Corded (Mains), Cordless (Battery), Corded & Cordless, Rechargeable'),
    D('batt', 'Battery Runtime (minutes)', 'مدة تشغيل البطارية (دقيقة)',
      'Not Applicable, Up to 20 min, 21-40 min, 41-60 min, 61-90 min, Above 90 min'),
    N('spec', 'Cord Length (m)', 'طول السلك (متر)',
      'Not Applicable, 3 m, 5 m, 6 m, 7 m, 8 m, 10 m'),
    B('feat', 'Wet & Dry Function', 'شفط جاف ورطب'),
    B('feat', 'Mopping Function', 'وظيفة المسح'),
    B('smart', 'App / Wi-Fi Control', 'تحكم عبر التطبيق'),
    B('smart', 'Voice Assistant Compatible', 'متوافق مع المساعد الصوتي'),
    D('smart', 'Navigation Technology', 'تقنية الملاحة',
      'Not Applicable, Random / Bump, Gyroscope, Camera (vSLAM), LiDAR, 3D Structured Light'),
    B('feat', 'Auto Empty Station', 'محطة تفريغ تلقائي'),
    B('feat', 'Self-Cleaning Brush', 'فرشاة ذاتية التنظيف'),
    D('pack', 'Included Attachments', 'الملحقات المرفقة',
      'Crevice Tool, Upholstery Brush, Dusting Brush, Motorised Brush Head, '
      'Pet Hair Tool, Extension Wand, Mop Pads, Charging Dock'),
    B('feat', 'Anti-Tangle Brush', 'فرشاة مانعة للتشابك'),
    D('usage', 'Suitable Surfaces', 'الأسطح المناسبة',
      'Hard Floors, Carpet, Rugs, Tiles, Marble, Wood / Parquet, '
      'Upholstery, Car Interior, All Surfaces'),
], APPLIANCE_COMMON, COLOR, ELEC_COMMERCE)

# ------------------------------------------------------------------ lighting
FAM['lighting'] = blk(IDENT, [
    D('spec', 'Luminaire Type', 'نوع وحدة الإنارة',
      'Downlight, Spotlight, Panel Light, Batten / Linear, Strip Light, Track Light, '
      'Pendant, Chandelier, Ceiling Surface Light, Wall Light, Floor Lamp, Table Lamp, '
      'Flood Light, High Bay, Bollard, In-Ground, Emergency Light, Street Light, '
      'Neon Flex, LED Module, Lamp Holder, Mounting Frame', required='Yes'),
    D('spec', 'Light Source', 'مصدر الضوء',
      'LED (Integrated), LED Lamp / Bulb, COB LED, SMD LED, Fluorescent, CFL, '
      'Halogen, Incandescent, Metal Halide, Sodium'),
    D('power', 'Power (Watts)', 'القدرة (واط)',
      '1 W, 3 W, 5 W, 7 W, 9 W, 12 W, 15 W, 18 W, 20 W, 24 W, 30 W, 36 W, 40 W, '
      '50 W, 60 W, 80 W, 100 W, 120 W, 150 W, 200 W, 300 W', required='Yes', option='Yes'),
    I('perf', 'Luminous Flux (Lumens)', 'التدفق الضوئي (لومن)',
      'Under 500 lm, 500-1000 lm, 1001-2000 lm, 2001-4000 lm, 4001-8000 lm, '
      '8001-15000 lm, Above 15000 lm'),
    I('perf', 'Luminous Efficacy (lm/W)', 'الكفاءة الضوئية (لومن/واط)',
      'Under 80 lm/W, 80-100 lm/W, 101-130 lm/W, 131-160 lm/W, Above 160 lm/W'),
    D('spec', 'Colour Temperature (CCT)', 'درجة حرارة اللون',
      '2200K (Extra Warm), 2700K (Warm White), 3000K (Warm White), '
      '4000K (Natural White), 5000K (Cool White), 6000K (Daylight), '
      '6500K (Cool Daylight), Tunable White (2700-6500K), RGB / RGBW',
      required='Yes', option='Yes'),
    I('spec', 'Colour Rendering Index (CRI)', 'مؤشر تجسيد اللون',
      'CRI 70, CRI 80, CRI 85, CRI 90, CRI 95, CRI 97'),
    D('spec', 'Beam Angle', 'زاوية الإضاءة',
      '10°, 15°, 24°, 36°, 38°, 45°, 60°, 90°, 120°, 180°, 360°'),
    D('elec', 'Input Voltage', 'جهد التشغيل',
      '220-240V AC, 110-240V AC, 12V DC, 24V DC, 48V DC, 3V Battery, Solar'),
    D('spec', 'Lamp Base / Cap', 'قاعدة اللمبة',
      'E27, E14, B22, GU10, GU5.3 / MR16, G9, G4, G13 (T8), G5 (T5), '
      'R7s, Integrated LED, Not Applicable'),
    D('spec', 'Dimmable', 'قابل للتعتيم',
      'Non-Dimmable, TRIAC Dimmable, 0-10V Dimmable, DALI Dimmable, '
      'PWM Dimmable, App Dimmable'),
    D('inst', 'Mounting Type', 'طريقة التركيب',
      'Recessed, Surface Mounted, Suspended / Pendant, Wall Mounted, Track Mounted, '
      'Free Standing, Clip-On, In-Ground, Pole Mounted, Magnetic'),
    N('dims', 'Cut-Out Size (mm)', 'مقاس فتحة التركيب (ملم)',
      'Not Applicable, 55 mm, 68 mm, 75 mm, 85 mm, 90 mm, 100 mm, 110 mm, 150 mm, 200 mm'),
    D('safety', 'IP Rating', 'درجة الحماية IP', IP_RATING),
    D('safety', 'IK Impact Rating', 'درجة مقاومة الصدم IK',
      'Not Rated, IK06, IK07, IK08, IK09, IK10'),
    D('usage', 'Application Area', 'مكان الاستخدام',
      'Indoor - Living Room, Indoor - Bedroom, Indoor - Kitchen, Indoor - Bathroom, '
      'Indoor - Office, Indoor - Retail, Outdoor - Garden, Outdoor - Facade, '
      'Outdoor - Street, Industrial / Warehouse, Landscape, Pool'),
    I('spec', 'Lifespan (hours)', 'العمر الافتراضي (ساعة)',
      '10000 Hours, 15000 Hours, 20000 Hours, 25000 Hours, 30000 Hours, 50000 Hours'),
    B('smart', 'Smart / App Controlled', 'ذكي / يتحكم به عبر التطبيق'),
    D('smart', 'Smart Protocol', 'بروتوكول التحكم الذكي',
      'Not Applicable, Wi-Fi, Bluetooth, Zigbee, Z-Wave, Matter, Tuya, DALI, DMX512'),
    B('feat', 'Motion Sensor', 'مستشعر حركة'),
    B('feat', 'Daylight Sensor', 'مستشعر ضوء النهار'),
    B('feat', 'Emergency Battery Backup', 'بطارية احتياطية للطوارئ'),
    B('feat', 'Solar Powered', 'يعمل بالطاقة الشمسية'),
    D('mat', 'Body Material', 'خامة الهيكل',
      'Aluminium, Die-Cast Aluminium, Steel, Stainless Steel, ABS Plastic, '
      'PC (Polycarbonate), Glass, Brass, Crystal, Wood, Rattan'),
    D('mat', 'Diffuser Material', 'خامة العاكس',
      'Opal PC, Frosted Glass, Clear Glass, Acrylic, PMMA, Prismatic, Not Applicable'),
    D('design', 'Finish', 'التشطيب',
      'White, Black, Matte Black, Chrome, Satin Nickel, Brushed Brass, Gold, '
      'Antique Bronze, Copper, Grey, Sand Black'),
    D('cert', 'Certification / Compliance', 'الشهادات والمطابقة', GCC_CERT),
    D('warr', 'Warranty Period', 'مدة الضمان', WARR_PERIOD),
], COLOR, COMMERCE)

# ------------------------------------------------------------------ furniture
FAM['furniture'] = blk(IDENT, [
    D('spec', 'Furniture Type', 'نوع الأثاث',
      'Sofa, Sofa Bed, Armchair, Recliner, Dining Table, Dining Chair, Coffee Table, '
      'Side Table, Console Table, Office Desk, Office Chair, Bed Frame, Wardrobe, '
      'Chest of Drawers, Bookshelf, TV Unit, Shoe Cabinet, Bar Stool, Bench, '
      'Dressing Table, Cabinet, Nightstand', required='Yes'),
    D('mat', 'Main Material', 'الخامة الأساسية',
      'Solid Wood, Engineered Wood, MDF, Particle Board, Plywood, Metal, '
      'Stainless Steel, Aluminium, Glass, Marble, Rattan, Bamboo, Plastic, '
      'Fabric Upholstered, Leather Upholstered', required='Yes'),
    D('mat', 'Upholstery Material', 'خامة التنجيد',
      'Not Applicable, Fabric, Linen, Velvet, Chenille, Genuine Leather, '
      'Faux Leather / PU, Bonded Leather, Microfibre, Boucle, Mesh'),
    D('mat', 'Frame Material', 'خامة الهيكل',
      'Solid Wood, Plywood, Metal, Steel, Aluminium, Engineered Wood, Plastic'),
    D('design', 'Colour / Finish', 'اللون / التشطيب',
      'White, Black, Grey, Beige, Cream, Brown, Walnut, Oak, Teak, Wenge, '
      'Natural Wood, High Gloss, Matte, Marble Effect, Gold, Chrome', option='Yes'),
    D('design', 'Style', 'الستايل',
      'Modern, Contemporary, Classic, Traditional, Scandinavian, Industrial, '
      'Minimalist, Rustic, Mid-Century, Luxury / Glam, Arabic / Majlis, Bohemian'),
    T('dims', 'Overall Dimensions (W x D x H cm)', 'الأبعاد الكلية (عرض×عمق×ارتفاع سم)'),
    N('dims', 'Width (cm)', 'العرض (سم)',
      'Under 60 cm, 60-100 cm, 101-150 cm, 151-200 cm, 201-250 cm, Above 250 cm'),
    N('dims', 'Depth (cm)', 'العمق (سم)',
      'Under 40 cm, 40-60 cm, 61-80 cm, 81-100 cm, Above 100 cm'),
    N('dims', 'Height (cm)', 'الارتفاع (سم)',
      'Under 50 cm, 50-80 cm, 81-110 cm, 111-150 cm, 151-200 cm, Above 200 cm'),
    D('spec', 'Seating Capacity', 'عدد المقاعد',
      'Not Applicable, 1 Seater, 2 Seater, 3 Seater, 4 Seater, 5 Seater, '
      '6 Seater, 7 Seater, 8 Seater, 10+ Seater', option='Yes'),
    D('spec', 'Bed Size', 'مقاس السرير',
      'Not Applicable, Single (90x190 cm), Super Single (120x190 cm), '
      'Queen (150x190 cm), King (180x200 cm), Super King (200x200 cm), '
      'Baby Cot, Bunk Bed', option='Yes'),
    I('spec', 'Number of Drawers', 'عدد الأدراج', '0, 1, 2, 3, 4, 5, 6, 8, 10'),
    I('spec', 'Number of Doors', 'عدد الأبواب', '0, 1, 2, 3, 4, 5, 6'),
    I('spec', 'Number of Shelves', 'عدد الأرفف', '0, 1, 2, 3, 4, 5, 6, 8'),
    N('spec', 'Weight Capacity (kg)', 'قدرة التحمل (كجم)',
      'Up to 80 kg, 81-120 kg, 121-150 kg, 151-200 kg, Above 200 kg'),
    B('spec', 'Assembly Required', 'يتطلب تركيباً'),
    D('inst', 'Assembly Type', 'نوع التركيب',
      'Fully Assembled, Partial Assembly, Self Assembly (Flat Pack), Professional Installation'),
    B('feat', 'Storage Included', 'يحتوي على مساحة تخزين'),
    B('feat', 'Adjustable Height', 'ارتفاع قابل للتعديل'),
    B('feat', 'Reclining Function', 'وظيفة الاستلقاء'),
    B('feat', 'Foldable', 'قابل للطي'),
    B('feat', 'Wheels / Castors', 'عجلات'),
    B('feat', 'Convertible / Sofa Bed', 'قابل للتحويل إلى سرير'),
    D('usage', 'Room Type', 'نوع الغرفة',
      'Living Room, Bedroom, Dining Room, Kitchen, Home Office, Kids Room, '
      'Majlis, Outdoor / Garden, Entryway, Bathroom, Commercial'),
    D('usage', 'Indoor / Outdoor', 'داخلي / خارجي', 'Indoor Use, Outdoor Use, Indoor & Outdoor'),
    B('feat', 'Water Resistant', 'مقاوم للماء'),
    B('feat', 'UV Resistant', 'مقاوم للأشعة فوق البنفسجية'),
    T('care', 'Care Instructions', 'تعليمات العناية'),
], COMMERCE)

# ------------------------------------------------------------------ kitchenware / tableware
FAM['kitchenware'] = blk(IDENT, [
    D('spec', 'Product Type', 'نوع المنتج',
      'Frying Pan, Saucepan, Casserole / Pot, Pressure Cooker, Wok, Cookware Set, '
      'Baking Tray, Cake Mould, Dinner Plate, Bowl, Mug, Cup & Saucer, Glass / Tumbler, '
      'Cutlery Set, Knife, Cutting Board, Serving Dish, Storage Container, '
      'Water Bottle, Flask / Thermos, Teapot, Kettle, Utensil Set, Colander, Tray',
      required='Yes'),
    D('mat', 'Material', 'الخامة',
      'Stainless Steel, Aluminium, Cast Iron, Non-Stick Coated Aluminium, '
      'Granite / Marble Coated, Ceramic, Porcelain, Bone China, Glass, '
      'Borosilicate Glass, Melamine, Plastic / BPA-Free, Silicone, Wood, '
      'Bamboo, Copper, Enamel, Tritan', required='Yes'),
    D('mat', 'Coating Type', 'نوع الطلاء',
      'Not Applicable, PTFE Non-Stick, Ceramic Non-Stick, Granite Coating, '
      'Marble Coating, Enamel, Hard Anodised, Titanium Reinforced'),
    D('pack', 'Number of Pieces', 'عدد القطع',
      '1 Piece, 2 Pieces, 3 Pieces, 4 Pieces, 5 Pieces, 6 Pieces, 8 Pieces, '
      '12 Pieces, 16 Pieces, 18 Pieces, 20 Pieces, 24 Pieces, 30 Pieces, 40+ Pieces',
      option='Yes'),
    N('cap', 'Capacity (Litres)', 'السعة (لتر)',
      '0.25 L, 0.35 L, 0.5 L, 0.75 L, 1 L, 1.5 L, 2 L, 2.5 L, 3 L, 4 L, 5 L, '
      '6 L, 8 L, 10 L', option='Yes'),
    N('dims', 'Diameter (cm)', 'القطر (سم)',
      '12 cm, 16 cm, 18 cm, 20 cm, 22 cm, 24 cm, 26 cm, 28 cm, 30 cm, 32 cm, 34 cm'),
    D('compat', 'Compatible Hob Types', 'أنواع المواقد المتوافقة',
      'Gas, Electric, Ceramic, Induction, Halogen, All Hob Types, Not Applicable'),
    B('feat', 'Induction Compatible', 'متوافق مع الحث الكهربائي'),
    B('feat', 'Oven Safe', 'آمن للفرن'),
    B('feat', 'Microwave Safe', 'آمن للميكروويف'),
    B('feat', 'Dishwasher Safe', 'آمن لغسالة الصحون'),
    B('feat', 'Freezer Safe', 'آمن للفريزر'),
    B('feat', 'Food Grade / BPA Free', 'آمن غذائياً / خالٍ من BPA'),
    B('feat', 'Non-Stick', 'غير لاصق'),
    B('feat', 'Lid Included', 'يشمل غطاء'),
    D('mat', 'Lid Material', 'خامة الغطاء',
      'Not Applicable, Tempered Glass, Stainless Steel, Plastic, Silicone, Bamboo'),
    D('mat', 'Handle Material', 'خامة المقبض',
      'Not Applicable, Bakelite, Stainless Steel, Silicone, Wood, Plastic, Cast Iron'),
    B('feat', 'Heat Resistant Handle', 'مقبض مقاوم للحرارة'),
    B('feat', 'Vacuum Insulated', 'عازل حراري مفرغ'),
    N('feat', 'Heat Retention (hours)', 'مدة حفظ الحرارة (ساعة)',
      'Not Applicable, 4 Hours, 6 Hours, 8 Hours, 12 Hours, 24 Hours'),
    B('feat', 'Leak Proof', 'مانع للتسرب'),
    B('feat', 'Stackable', 'قابل للتكديس'),
    D('design', 'Design / Pattern', 'التصميم / النقشة',
      'Plain / Solid, Printed, Floral, Geometric, Marble Effect, Gold Rim, '
      'Embossed, Hammered, Arabic / Oriental'),
    D('usage', 'Occasion', 'المناسبة',
      'Everyday Use, Formal Dining, Ramadan & Eid, Gifting, Outdoor / Picnic, Commercial'),
], COLOR, COMMERCE)

# ------------------------------------------------------------------ home textile
FAM['home_textile'] = blk(IDENT, [
    D('spec', 'Product Type', 'نوع المنتج',
      'Bedsheet Set, Duvet Cover Set, Comforter Set, Quilt, Blanket, Mattress Protector, '
      'Mattress Topper, Pillow, Pillowcase, Cushion, Cushion Cover, Curtain, '
      'Sheer Curtain, Carpet, Rug, Doormat, Bath Towel, Hand Towel, Bath Mat, '
      'Table Cloth, Table Runner, Throw', required='Yes'),
    D('spec', 'Size', 'المقاس',
      'Single, Super Single, Double, Queen, King, Super King, '
      '40x60 cm, 50x70 cm, 60x90 cm, 80x150 cm, 120x170 cm, 160x230 cm, '
      '200x290 cm, 240x340 cm, One Size', required='Yes', option='Yes'),
    D('mat', 'Material', 'الخامة',
      'Cotton, Egyptian Cotton, Organic Cotton, Cotton Blend, Microfibre, Polyester, '
      'Linen, Bamboo, Silk, Satin, Velvet, Wool, Acrylic, Jute, Chenille, '
      'Memory Foam, Down / Feather, Hollow Fibre, Viscose', required='Yes'),
    I('spec', 'Thread Count', 'عدد الخيوط',
      'Not Applicable, 144 TC, 180 TC, 200 TC, 250 TC, 300 TC, 400 TC, 500 TC, 800 TC, 1000 TC'),
    I('spec', 'GSM (Weight per m²)', 'الوزن لكل متر مربع (جرام)',
      'Under 300 GSM, 300-450 GSM, 451-600 GSM, 601-800 GSM, Above 800 GSM'),
    D('pack', 'Number of Pieces', 'عدد القطع',
      '1 Piece, 2 Pieces, 3 Pieces, 4 Pieces, 5 Pieces, 6 Pieces, 7 Pieces, 8 Pieces', option='Yes'),
    D('design', 'Pattern', 'النقشة',
      'Solid / Plain, Striped, Checked, Floral, Geometric, Abstract, Damask, '
      'Oriental / Persian, Animal Print, Printed, Embroidered, Jacquard, Textured'),
    D('design', 'Style', 'الستايل',
      'Modern, Classic, Scandinavian, Bohemian, Minimalist, Luxury, Oriental, Kids'),
    D('spec', 'Weave / Construction', 'طريقة النسج',
      'Percale, Sateen, Jersey Knit, Flannel, Terry, Waffle, Jacquard, Hand-Tufted, '
      'Machine Woven, Hand Knotted, Shaggy, Flatweave'),
    N('spec', 'Pile Height (mm)', 'ارتفاع الوبر (ملم)',
      'Not Applicable, Under 5 mm, 5-10 mm, 11-20 mm, 21-40 mm, Above 40 mm'),
    N('spec', 'Filling Weight (g/m²)', 'وزن الحشو (جم/م²)',
      'Not Applicable, 150 g, 200 g, 250 g, 300 g, 350 g, 400 g'),
    D('mat', 'Filling Material', 'خامة الحشو',
      'Not Applicable, Hollow Fibre, Microfibre, Down / Feather, Memory Foam, '
      'Latex, Polyester Fibre, Cotton, Wool'),
    D('spec', 'Curtain Header Type', 'نوع تعليق الستارة',
      'Not Applicable, Rod Pocket, Grommet / Eyelet, Pencil Pleat, Tab Top, '
      'Back Tab, Hook / Ring Top'),
    D('spec', 'Light Filtering', 'حجب الضوء',
      'Not Applicable, Sheer, Light Filtering, Room Darkening, Blackout, Thermal Blackout'),
    D('spec', 'Firmness', 'درجة الصلابة',
      'Not Applicable, Soft, Medium Soft, Medium, Medium Firm, Firm, Extra Firm'),
    B('feat', 'Hypoallergenic', 'مضاد للحساسية'),
    B('feat', 'Anti-Bacterial', 'مضاد للبكتيريا'),
    B('feat', 'Water Resistant', 'مقاوم للماء'),
    B('feat', 'Anti-Slip Backing', 'ظهر مانع للانزلاق'),
    B('feat', 'Quick Dry', 'سريع الجفاف'),
    B('feat', 'Fade Resistant', 'مقاوم لبهتان اللون'),
    D('care', 'Care Instructions', 'تعليمات العناية',
      'Machine Washable, Hand Wash, Dry Clean Only, Do Not Bleach, Tumble Dry Low, '
      'Iron Low Heat, Spot Clean Only, Vacuum Regularly'),
    D('usage', 'Room Type', 'نوع الغرفة',
      'Bedroom, Living Room, Bathroom, Kitchen, Dining Room, Kids Room, '
      'Majlis, Office, Outdoor'),
    D('usage', 'Season', 'الموسم', 'Summer, Winter, All Season'),
], COLOR, COMMERCE)

# ------------------------------------------------------------------ cleaning products
FAM['cleaning'] = blk(IDENT, [
    D('spec', 'Product Type', 'نوع المنتج',
      'Laundry Detergent (Liquid), Laundry Detergent (Powder), Laundry Capsules / Pods, '
      'Fabric Softener, Bleach, Stain Remover, Dishwashing Liquid, Dishwasher Tablets, '
      'Floor Cleaner, Multi-Surface Cleaner, Glass Cleaner, Bathroom / Toilet Cleaner, '
      'Kitchen Degreaser, Disinfectant, Hand Sanitiser, Air Freshener, '
      'Drain Cleaner, Oven Cleaner, Carpet Cleaner, Cleaning Wipes', required='Yes'),
    D('spec', 'Form', 'الشكل',
      'Liquid, Powder, Gel, Spray, Foam, Capsule / Pod, Tablet, Wipes, Cream, Aerosol, Bar'),
    N('spec', 'Volume (ml)', 'الحجم (مل)',
      '250 ml, 500 ml, 750 ml, 1 L, 1.5 L, 2 L, 3 L, 4 L, 5 L, 10 L, 20 L', option='Yes'),
    N('spec', 'Net Weight (g)', 'الوزن الصافي (جم)',
      '100 g, 250 g, 500 g, 1 kg, 1.5 kg, 2.5 kg, 3 kg, 5 kg, 9 kg, 15 kg', option='Yes'),
    D('pack', 'Pack Size', 'حجم العبوة', PACK_QTY, option='Yes'),
    D('spec', 'Scent', 'الرائحة',
      'Unscented, Fresh / Original, Lemon, Lavender, Rose, Ocean / Marine, Pine, '
      'Jasmine, Oud, Musk, Vanilla, Apple, Baby Powder, Eucalyptus'),
    D('usage', 'Suitable Surfaces', 'الأسطح المناسبة',
      'All Surfaces, Ceramic & Tiles, Marble, Wood / Parquet, Glass, Stainless Steel, '
      'Fabric & Upholstery, Carpet, Toilet & Sanitary, Kitchen Counters, Not Applicable'),
    D('usage', 'Suitable Fabrics', 'الأقمشة المناسبة',
      'Not Applicable, All Fabrics, White Fabrics, Coloured Fabrics, Delicates, '
      'Wool & Silk, Baby Clothes, Sportswear'),
    D('usage', 'Washing Machine Type', 'نوع الغسالة',
      'Not Applicable, Front Load, Top Load, Front & Top Load, Hand Wash'),
    B('feat', 'Concentrated Formula', 'تركيبة مركّزة'),
    B('feat', 'Anti-Bacterial', 'مضاد للبكتيريا'),
    B('feat', 'Bleach Free', 'خالٍ من المبيّض'),
    B('feat', 'Colour Safe', 'آمن على الألوان'),
    B('feat', 'Biodegradable / Eco-Friendly', 'قابل للتحلل / صديق للبيئة'),
    B('feat', 'Phosphate Free', 'خالٍ من الفوسفات'),
    B('feat', 'Skin Friendly / Dermatologically Tested', 'آمن على البشرة'),
    B('feat', 'Refill Pack', 'عبوة إعادة تعبئة'),
    I('perf', 'Number of Washes / Uses', 'عدد الغسلات / الاستخدامات',
      'Under 10, 10-20, 21-35, 36-60, 61-100, Above 100'),
    I('perf', 'Kills Germs (%)', 'نسبة القضاء على الجراثيم',
      'Not Specified, 99%, 99.9%, 99.99%'),
    D('pack', 'Packaging Type', 'نوع العبوة',
      'Bottle, Spray Bottle, Pouch, Box, Bucket, Sachet, Canister, Aerosol Can, Refill Pouch'),
    T('safety', 'Safety Warnings', 'تحذيرات السلامة'),
    D('cert', 'Certification / Compliance', 'الشهادات والمطابقة', GCC_CERT),
    D('origin', 'Country of Origin', 'بلد المنشأ', ORIGIN),
    N('spec', 'Shelf Life (months)', 'مدة الصلاحية (شهر)',
      '12 Months, 18 Months, 24 Months, 36 Months, 60 Months', dtype='Integer'),
], COMMERCE)
