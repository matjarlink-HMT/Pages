# -*- coding: utf-8 -*-
"""Automotive: vehicles, spare parts, accessories, tyres, batteries, fluids."""
from lib_core import *

FAM = {}

FITMENT = [
    D('fitment', 'Compatible Make', 'الماركة المتوافقة',
      'Toyota, Nissan, Honda, Mitsubishi, Mazda, Suzuki, Lexus, Infiniti, Hyundai, '
      'Kia, Chevrolet, Ford, GMC, Dodge, Jeep, Cadillac, Mercedes-Benz, BMW, Audi, '
      'Volkswagen, Porsche, Land Rover, Jaguar, Volvo, Peugeot, Renault, Citroen, '
      'MG, Chery, Geely, Haval, Changan, BYD, Isuzu, Mitsubishi Fuso, Universal',
      required='Yes'),
    T('fitment', 'Compatible Model', 'الموديل المتوافق', required='Yes'),
    D('fitment', 'Compatible Year From', 'من سنة',
      '1990, 1995, 2000, 2005, 2008, 2010, 2012, 2014, 2015, 2016, 2017, 2018, '
      '2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026'),
    D('fitment', 'Compatible Year To', 'إلى سنة',
      '1995, 2000, 2005, 2008, 2010, 2012, 2014, 2015, 2016, 2017, 2018, 2019, '
      '2020, 2021, 2022, 2023, 2024, 2025, 2026, Present'),
    D('fitment', 'Engine Type', 'نوع المحرك',
      'Petrol, Diesel, Hybrid, Plug-In Hybrid, Electric, LPG / CNG, Universal'),
    D('fitment', 'Engine Displacement', 'سعة المحرك',
      'Under 1.0 L, 1.0-1.5 L, 1.6-2.0 L, 2.1-2.5 L, 2.6-3.0 L, 3.1-4.0 L, '
      '4.1-5.0 L, Above 5.0 L, Not Applicable'),
    D('fitment', 'Vehicle Type', 'نوع المركبة',
      'Passenger Car, SUV, Pickup Truck, Van, Bus, Light Truck, Heavy Truck, '
      'Motorcycle, Trailer, Heavy Equipment, Universal'),
    D('fitment', 'Drive Side', 'جهة القيادة', 'Left Hand Drive (LHD), Right Hand Drive (RHD), Both'),
    D('fitment', 'Fitting Position', 'موضع التركيب',
      'Front, Rear, Front Left, Front Right, Rear Left, Rear Right, Left, Right, '
      'Upper, Lower, Inner, Outer, Centre, Not Applicable'),
]

AUTOPART_BASE = [
    T('main', 'OEM Part Number', 'رقم القطعة الأصلي (OEM)'),
    D('spec', 'Part Quality / Grade', 'جودة القطعة',
      'Genuine OEM, OES (Original Equipment Supplier), Aftermarket - Premium, '
      'Aftermarket - Standard, Refurbished / Remanufactured, Used - Good, High Copy',
      required='Yes'),
    D('mat', 'Material', 'الخامة',
      'Steel, Stainless Steel, Cast Iron, Aluminium, Aluminium Alloy, Plastic / ABS, '
      'Rubber, Composite, Ceramic, Carbon Fibre, Copper, Brass, Nylon, Mixed'),
    D('spec', 'Sold As', 'طريقة البيع',
      'Single Piece, Pair (Left & Right), Set, Kit, Axle Set, Complete Assembly'),
    I('pack', 'Quantity per Pack', 'الكمية في العبوة', '1, 2, 4, 5, 6, 8, 10, 12, 16, 20'),
    D('cert', 'Certification / Compliance', 'الشهادات والمطابقة',
      'ISO 9001, IATF 16949, TÜV, ECE Approved, DOT Approved, SAE, E-Mark, '
      'GCC Conformity, None'),
    B('spec', 'Direct Replacement (Plug & Play)', 'بديل مباشر (دون تعديل)'),
    B('inst', 'Professional Installation Recommended', 'يُنصح بالتركيب لدى فني'),
    T('spec', 'Technical Specifications', 'المواصفات الفنية'),
]

# ------------------------------------------------------------------ generic auto part
FAM['auto_part'] = blk(IDENT, FITMENT, AUTOPART_BASE, [
    T('dims', 'Part Dimensions (mm)', 'أبعاد القطعة (ملم)'),
    N('pack', 'Item Weight (kg)', 'وزن المنتج (كجم)', WEIGHT_KG),
    D('spec', 'Surface Finish / Coating', 'التشطيب / الطلاء',
      'Painted, Powder Coated, Zinc Plated, Chrome Plated, Anodised, '
      'Galvanised, Raw / Unfinished, Black Oxide'),
], COLOR, [
    D('general', 'Condition', 'الحالة', COND, required='Yes'),
    D('origin', 'Country of Origin', 'بلد المنشأ', ORIGIN),
    D('warr', 'Warranty Type', 'نوع الضمان', WARR_TYPE),
    D('warr', 'Warranty Period', 'مدة الضمان', WARR_PERIOD),
    T('pack', 'Package Contents', 'محتويات العبوة'),
])

# ------------------------------------------------------------------ car lighting
FAM['auto_light'] = blk(IDENT, FITMENT, AUTOPART_BASE, [
    D('spec', 'Bulb / Lamp Type', 'نوع اللمبة',
      'Halogen, LED, Xenon / HID, Laser, Incandescent, Neon, Not Applicable'),
    D('spec', 'Bulb Base / Socket', 'قاعدة اللمبة',
      'H1, H3, H4, H7, H8, H9, H11, H13, HB3 (9005), HB4 (9006), 9012, D1S, D2S, '
      'D3S, D4S, T10 (W5W), T15, T20, 1156, 1157, BA9S, Festoon, Not Applicable'),
    D('spec', 'Colour Temperature', 'درجة حرارة اللون',
      '3000K (Yellow), 4300K (Warm White), 5000K (White), 6000K (Cool White), '
      '6500K (Daylight), 8000K (Blue), Amber, Red'),
    D('power', 'Power (Watts)', 'القدرة (واط)',
      '5 W, 10 W, 12 W, 21 W, 25 W, 35 W, 45 W, 55 W, 65 W, 70 W, 100 W'),
    D('elec', 'Voltage', 'الجهد', '12V, 24V, 12V/24V'),
    I('perf', 'Luminous Flux (Lumens)', 'التدفق الضوئي (لومن)',
      'Under 1000 lm, 1000-2000 lm, 2001-4000 lm, 4001-8000 lm, Above 8000 lm'),
    D('safety', 'IP Rating', 'درجة الحماية IP', IP_RATING),
    B('feat', 'CANBUS Error Free', 'خالٍ من أخطاء CANBUS'),
    B('feat', 'Plug and Play', 'تركيب مباشر'),
    I('spec', 'Lifespan (hours)', 'العمر الافتراضي (ساعة)',
      '500 Hours, 1000 Hours, 2000 Hours, 5000 Hours, 10000 Hours, 30000 Hours, 50000 Hours'),
    D('spec', 'Lens Material', 'خامة العدسة',
      'Polycarbonate, Glass, Acrylic, PMMA, Not Applicable'),
], COLOR, [
    D('general', 'Condition', 'الحالة', COND, required='Yes'),
    D('origin', 'Country of Origin', 'بلد المنشأ', ORIGIN),
    D('warr', 'Warranty Period', 'مدة الضمان', WARR_PERIOD),
    T('pack', 'Package Contents', 'محتويات العبوة'),
])

# ------------------------------------------------------------------ brake part
FAM['auto_brake'] = blk(IDENT, FITMENT, AUTOPART_BASE, [
    D('spec', 'Brake Component', 'مكوّن الفرامل',
      'Brake Pads, Brake Discs / Rotors, Brake Shoes, Brake Drum, Brake Caliper, '
      'Master Cylinder, Wheel Cylinder, Brake Hose, Brake Line, Brake Booster, '
      'ABS Sensor, ABS Pump, Handbrake Cable, Wear Sensor, Brake Fluid'),
    N('dims', 'Disc Diameter (mm)', 'قطر القرص (ملم)',
      'Not Applicable, 256 mm, 276 mm, 280 mm, 288 mm, 296 mm, 300 mm, 312 mm, '
      '320 mm, 330 mm, 345 mm, 350 mm, 380 mm'),
    N('dims', 'Disc Thickness (mm)', 'سماكة القرص (ملم)',
      'Not Applicable, 10 mm, 12 mm, 18 mm, 22 mm, 24 mm, 26 mm, 28 mm, 30 mm, 32 mm'),
    D('spec', 'Disc Type', 'نوع القرص',
      'Not Applicable, Solid, Ventilated, Drilled, Slotted, Drilled & Slotted, Carbon Ceramic'),
    D('mat', 'Friction Material', 'خامة الاحتكاك',
      'Not Applicable, Ceramic, Semi-Metallic, Low-Metallic, Organic / NAO, Sintered'),
    B('spec', 'Wear Sensor Included', 'يشمل حساس التآكل'),
    B('spec', 'Fitting Kit Included', 'يشمل طقم التركيب'),
    D('spec', 'Brake System Type', 'نوع نظام الفرامل',
      'Disc Brake, Drum Brake, Disc & Drum, Not Applicable'),
], COLOR, [
    D('general', 'Condition', 'الحالة', COND, required='Yes'),
    D('origin', 'Country of Origin', 'بلد المنشأ', ORIGIN),
    D('warr', 'Warranty Period', 'مدة الضمان', WARR_PERIOD),
    T('pack', 'Package Contents', 'محتويات العبوة'),
])

# ------------------------------------------------------------------ auto filter
FAM['auto_filter'] = blk(IDENT, FITMENT, AUTOPART_BASE, [
    D('spec', 'Filter Type', 'نوع الفلتر',
      'Oil Filter, Air Filter, Cabin / Pollen Filter, Fuel Filter, Hydraulic Filter, '
      'Coolant Filter, Transmission Filter, Diesel Particulate Filter, Filter Set',
      required='Yes'),
    D('spec', 'Filter Design', 'شكل الفلتر',
      'Spin-On, Cartridge / Insert, Panel, Round / Cylindrical, In-Line, Conical'),
    D('mat', 'Filter Media', 'خامة الوسط الترشيحي',
      'Cellulose Paper, Synthetic Fibre, Activated Carbon, Foam, Cotton Gauze, '
      'Metal Mesh, HEPA, Multi-Layer'),
    T('dims', 'Filter Dimensions (mm)', 'أبعاد الفلتر (ملم)'),
    N('spec', 'Filtration Rating (micron)', 'درجة الترشيح (ميكرون)',
      'Not Specified, 5 micron, 10 micron, 20 micron, 25 micron, 30 micron, 40 micron'),
    B('feat', 'Washable / Reusable', 'قابل للغسل وإعادة الاستخدام'),
    B('feat', 'Activated Carbon Layer', 'طبقة كربون منشط'),
    B('feat', 'Anti-Bacterial Treatment', 'معالجة مضادة للبكتيريا'),
    I('spec', 'Service Interval (km)', 'فترة الاستبدال (كم)',
      '5000 km, 10000 km, 15000 km, 20000 km, 30000 km, 40000 km'),
], [
    D('general', 'Condition', 'الحالة', COND, required='Yes'),
    D('origin', 'Country of Origin', 'بلد المنشأ', ORIGIN),
    D('warr', 'Warranty Period', 'مدة الضمان', WARR_PERIOD),
    T('pack', 'Package Contents', 'محتويات العبوة'),
])

# ------------------------------------------------------------------ car accessory
FAM['auto_accessory'] = blk(IDENT, [
    D('spec', 'Accessory Type', 'نوع الإكسسوار',
      'Floor Mats, Trunk Liner, Car Cover, Seat Cover, Steering Wheel Cover, '
      'Sunshade, Phone Holder, Dash Cam, Reverse Camera, Parking Sensor, '
      'Jump Starter, Battery Charger, Tow Rope, Roof Rack, Roof Box, Bike Carrier, '
      'Snow Chains, Warning Triangle, Fire Extinguisher, Car Vacuum, Air Purifier, '
      'Air Freshener, Tyre Inflator, Power Inverter, Car Organiser', required='Yes'),
    D('mat', 'Material', 'الخامة',
      'Rubber, TPE, PVC, Carpet / Textile, Leather, Faux Leather, Polyester, '
      'Nylon, Aluminium, Steel, ABS Plastic, Silicone, Neoprene, EVA'),
    D('spec', 'Fit Type', 'نوع التركيب',
      'Universal Fit, Custom Fit (Model Specific), Semi-Custom, Adjustable'),
    D('fitment', 'Compatible Make', 'الماركة المتوافقة',
      'Toyota, Nissan, Honda, Mitsubishi, Mazda, Suzuki, Lexus, Hyundai, Kia, '
      'Chevrolet, Ford, GMC, Jeep, Mercedes-Benz, BMW, Audi, Volkswagen, '
      'Land Rover, MG, Chery, Universal'),
    T('fitment', 'Compatible Model', 'الموديل المتوافق'),
    D('fitment', 'Vehicle Type', 'نوع المركبة',
      'Sedan, Hatchback, SUV, Coupe, Pickup Truck, Van, MPV, Truck, Universal'),
    I('pack', 'Number of Pieces', 'عدد القطع', '1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12'),
    D('elec', 'Power Source', 'مصدر الطاقة',
      'Not Applicable, 12V Car Socket, USB, Built-In Battery, Hardwired, Solar'),
    D('elec', 'Voltage', 'الجهد', 'Not Applicable, 12V, 24V, 12V/24V, 110V, 220V'),
    B('feat', 'Waterproof', 'مقاوم للماء'),
    B('feat', 'Anti-Slip', 'مانع للانزلاق'),
    B('feat', 'UV Resistant', 'مقاوم للأشعة فوق البنفسجية'),
    B('feat', 'Foldable / Portable', 'قابل للطي / محمول'),
    B('feat', 'Easy Installation', 'سهل التركيب'),
    N('spec', 'Load Capacity (kg)', 'قدرة التحميل (كجم)',
      'Not Applicable, Up to 20 kg, 21-50 kg, 51-75 kg, 76-100 kg, Above 100 kg'),
    D('usage', 'Usage Position', 'موضع الاستخدام',
      'Front, Rear, Front & Rear, Interior, Exterior, Roof, Trunk, Windscreen, Universal'),
    D('usage', 'Season', 'الموسم', 'All Season, Summer, Winter, Rainy'),
], COLOR, COMMERCE)

# ------------------------------------------------------------------ tyre
FAM['tyre'] = blk(IDENT, [
    D('spec', 'Tyre Width (mm)', 'عرض الإطار (ملم)',
      '155, 165, 175, 185, 195, 205, 215, 225, 235, 245, 255, 265, 275, 285, '
      '295, 305, 315, 325', required='Yes', option='Yes'),
    D('spec', 'Aspect Ratio (%)', 'نسبة الارتفاع (%)',
      '30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85', required='Yes', option='Yes'),
    D('spec', 'Rim Diameter (inch)', 'قطر الجنط (بوصة)',
      '12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24', required='Yes', option='Yes'),
    D('spec', 'Tyre Type', 'نوع الإطار',
      'Passenger Car, SUV / 4x4, All-Terrain (A/T), Mud-Terrain (M/T), '
      'Highway Terrain (H/T), Performance / Sport, Light Truck (LT), '
      'Commercial Van, Truck / Bus, Winter, Run-Flat, Spare / Temporary', required='Yes'),
    D('spec', 'Load Index', 'مؤشر التحميل',
      '75, 79, 82, 85, 88, 91, 94, 97, 100, 103, 106, 109, 112, 115, 118, 121'),
    D('spec', 'Speed Rating', 'مؤشر السرعة',
      'N (140 km/h), P (150 km/h), Q (160 km/h), R (170 km/h), S (180 km/h), '
      'T (190 km/h), H (210 km/h), V (240 km/h), W (270 km/h), Y (300 km/h), '
      'ZR (Above 240 km/h)'),
    D('spec', 'Season', 'الموسم', 'Summer, All Season, Winter, All Weather'),
    D('spec', 'Construction', 'التركيب', 'Radial, Bias / Diagonal, Run-Flat'),
    I('spec', 'Ply Rating', 'عدد الطبقات', '4 PR, 6 PR, 8 PR, 10 PR, 12 PR, 14 PR, 16 PR'),
    D('spec', 'Tread Pattern', 'نمط المداس',
      'Symmetric, Asymmetric, Directional, Directional & Asymmetric, Block, Rib'),
    D('env', 'Fuel Efficiency Grade', 'درجة كفاءة الوقود', 'A, B, C, D, E, F, G'),
    D('perf', 'Wet Grip Grade', 'درجة التماسك على المبلل', 'A, B, C, D, E, F, G'),
    I('perf', 'External Rolling Noise (dB)', 'ضجيج الدوران (ديسيبل)',
      'Under 68 dB, 68-70 dB, 71-72 dB, Above 72 dB'),
    D('spec', 'Manufacturing Year (DOT)', 'سنة الصنع',
      '2022, 2023, 2024, 2025, 2026'),
    B('feat', 'Run-Flat Technology', 'تقنية الاستمرار بعد الثقب'),
    B('feat', 'Reinforced / XL', 'مقوّى (XL)'),
    B('feat', 'Self-Sealing', 'ذاتي الإغلاق'),
    D('pack', 'Sold As', 'طريقة البيع', 'Single Tyre, Set of 2, Set of 4'),
    D('origin', 'Country of Origin', 'بلد المنشأ', ORIGIN),
    D('warr', 'Warranty Period', 'مدة الضمان', WARR_PERIOD),
    D('general', 'Condition', 'الحالة', COND, required='Yes'),
])

# ------------------------------------------------------------------ vehicle (whole)
FAM['vehicle'] = blk(IDENT, [
    D('main', 'Year of Manufacture', 'سنة الصنع',
      '2010, 2012, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, '
      '2024, 2025, 2026', required='Yes'),
    T('main', 'Trim / Variant', 'الفئة'),
    D('spec', 'Body Type', 'نوع الهيكل',
      'Sedan, Hatchback, SUV, Crossover, Coupe, Convertible, Pickup Truck, Van, '
      'MPV / Minivan, Wagon, Bus, Truck, Trailer, Tanker, Refrigerated Truck, '
      'Excavator, Loader, Bulldozer, Crane, Dump Truck, Motorcycle, Boat, Jet Ski',
      required='Yes'),
    D('engine', 'Fuel Type', 'نوع الوقود',
      'Petrol, Diesel, Hybrid, Plug-In Hybrid, Electric, LPG, CNG, Hydrogen',
      required='Yes'),
    D('engine', 'Engine Size (Litres)', 'سعة المحرك (لتر)',
      'Under 1.0 L, 1.0-1.4 L, 1.5-1.8 L, 1.9-2.4 L, 2.5-3.0 L, 3.1-4.0 L, '
      '4.1-5.0 L, 5.1-6.0 L, Above 6.0 L, Electric'),
    D('engine', 'Cylinders', 'عدد الأسطوانات',
      '3 Cylinders, 4 Cylinders, 5 Cylinders, 6 Cylinders, 8 Cylinders, '
      '10 Cylinders, 12 Cylinders, Electric Motor'),
    I('engine', 'Horsepower (hp)', 'القدرة الحصانية',
      'Under 100 hp, 100-150 hp, 151-200 hp, 201-300 hp, 301-400 hp, '
      '401-600 hp, Above 600 hp'),
    I('engine', 'Torque (Nm)', 'عزم الدوران (نيوتن متر)',
      'Under 150 Nm, 150-250 Nm, 251-400 Nm, 401-600 Nm, Above 600 Nm'),
    D('spec', 'Transmission', 'ناقل الحركة',
      'Automatic, Manual, CVT, Dual Clutch (DCT), Tiptronic, Semi-Automatic, Single Speed (EV)',
      required='Yes'),
    D('spec', 'Drivetrain', 'نظام الدفع',
      'Front Wheel Drive (FWD), Rear Wheel Drive (RWD), All Wheel Drive (AWD), '
      'Four Wheel Drive (4WD / 4x4), 6x4, 6x6, 8x4'),
    D('spec', 'Mileage (km)', 'المسافة المقطوعة (كم)',
      '0 km (Brand New), Under 10000 km, 10000-30000 km, 30001-60000 km, '
      '60001-100000 km, 100001-150000 km, 150001-200000 km, Above 200000 km',
      required='Yes'),
    D('spec', 'Number of Seats', 'عدد المقاعد', '2, 4, 5, 7, 8, 9, 12, 15, 20+'),
    I('spec', 'Number of Doors', 'عدد الأبواب', '2, 3, 4, 5'),
    D('design', 'Exterior Colour', 'اللون الخارجي',
      'White, Black, Silver, Grey, Blue, Red, Green, Brown, Beige, Gold, '
      'Orange, Yellow, Maroon, Purple, Other', option='Yes'),
    D('design', 'Interior Colour', 'اللون الداخلي',
      'Black, Beige, Grey, Brown, Tan, Red, White, Two-Tone'),
    D('mat', 'Upholstery Material', 'خامة المقاعد',
      'Fabric, Leather, Leatherette, Alcantara, Combination'),
    D('general', 'Condition', 'الحالة',
      'Brand New, Used - Excellent, Used - Very Good, Used - Good, Used - Fair, '
      'Salvage / Damaged, Certified Pre-Owned', required='Yes'),
    D('spec', 'Regional Specification', 'مواصفات المنطقة',
      'GCC Specifications, American Specifications, European Specifications, '
      'Japanese Specifications, Canadian Specifications, Other'),
    D('spec', 'Steering Side', 'جهة المقود', 'Left Hand Drive, Right Hand Drive'),
    B('spec', 'Accident Free', 'خالٍ من الحوادث'),
    B('spec', 'Service History Available', 'يتوفر سجل صيانة'),
    B('spec', 'Under Manufacturer Warranty', 'تحت ضمان الوكيل'),
    I('spec', 'Number of Previous Owners', 'عدد المالكين السابقين', '0, 1, 2, 3, 4, 5+'),
    D('feat', 'Comfort Features', 'ميزات الراحة',
      'Air Conditioning, Climate Control, Heated Seats, Ventilated Seats, '
      'Power Seats, Sunroof, Panoramic Roof, Keyless Entry, Push Start, '
      'Cruise Control, Adaptive Cruise Control, Power Windows, Electric Mirrors'),
    D('feat', 'Safety Features', 'ميزات السلامة',
      'ABS, EBD, Airbags, Traction Control, Electronic Stability Control, '
      'Lane Departure Warning, Blind Spot Monitoring, Rear Camera, 360 Camera, '
      'Parking Sensors, Autonomous Emergency Braking, Tyre Pressure Monitoring'),
    I('feat', 'Number of Airbags', 'عدد الوسائد الهوائية', '2, 4, 6, 7, 8, 10, 12'),
    D('feat', 'Infotainment', 'نظام الترفيه',
      'Touchscreen Display, Apple CarPlay, Android Auto, Bluetooth, Navigation / GPS, '
      'Premium Sound System, Rear Entertainment, Wireless Charging, Head-Up Display'),
    N('env', 'Fuel Consumption (L/100km)', 'استهلاك الوقود (لتر/100كم)',
      'Under 5 L, 5-7 L, 7.1-9 L, 9.1-12 L, 12.1-16 L, Above 16 L'),
    N('batt', 'Electric Range (km)', 'المدى الكهربائي (كم)',
      'Not Applicable, Under 100 km, 100-250 km, 251-400 km, 401-550 km, Above 550 km'),
    N('batt', 'Battery Capacity (kWh)', 'سعة البطارية (كيلوواط ساعة)',
      'Not Applicable, Under 40 kWh, 40-60 kWh, 61-80 kWh, 81-100 kWh, Above 100 kWh'),
    N('spec', 'Payload Capacity (kg)', 'الحمولة (كجم)',
      'Not Applicable, Under 1000 kg, 1000-3000 kg, 3001-8000 kg, 8001-15000 kg, Above 15000 kg'),
    N('spec', 'Towing Capacity (kg)', 'قدرة السحب (كجم)',
      'Not Applicable, Under 1000 kg, 1000-2500 kg, 2501-3500 kg, Above 3500 kg'),
    D('spec', 'Registration / Papers', 'الترخيص والأوراق',
      'Registered in Oman, GCC Registered, Imported - Not Registered, '
      'Customs Cleared, Export Only'),
    D('origin', 'Country of Origin', 'بلد المنشأ', ORIGIN),
    D('warr', 'Warranty Period', 'مدة الضمان', WARR_PERIOD),
])

# ------------------------------------------------------------------ car battery / fluids
FAM['auto_consumable'] = blk(IDENT, [
    D('spec', 'Product Type', 'نوع المنتج',
      'Engine Oil, Gear Oil, Transmission Fluid, Brake Fluid, Power Steering Fluid, '
      'Coolant / Antifreeze, Windscreen Washer Fluid, Car Battery, Grease, '
      'Fuel Additive, AdBlue / Urea, Radiator Flush, Degreaser', required='Yes'),
    D('spec', 'Viscosity Grade (SAE)', 'درجة اللزوجة',
      'Not Applicable, 0W-16, 0W-20, 0W-30, 0W-40, 5W-20, 5W-30, 5W-40, 5W-50, '
      '10W-30, 10W-40, 10W-60, 15W-40, 20W-50, 75W-90, 80W-90, 85W-140'),
    D('spec', 'Oil Type', 'نوع الزيت',
      'Not Applicable, Fully Synthetic, Semi-Synthetic, Synthetic Blend, Mineral'),
    D('spec', 'API / Specification', 'المواصفة القياسية',
      'Not Applicable, API SN, API SP, API CK-4, API CJ-4, ACEA A3/B4, ACEA C3, '
      'DOT 3, DOT 4, DOT 5.1, ILSAC GF-6, JASO MA2'),
    N('cap', 'Volume (Litres)', 'الحجم (لتر)',
      '0.25 L, 0.5 L, 1 L, 3 L, 4 L, 4.5 L, 5 L, 6 L, 20 L, 200 L', option='Yes'),
    D('compat', 'Suitable For Engine', 'مناسب لمحرك',
      'Petrol Engines, Diesel Engines, Petrol & Diesel, Hybrid, Motorcycle, '
      'Heavy Duty / Truck, Not Applicable'),
    D('spec', 'Battery Capacity (Ah)', 'سعة البطارية (أمبير/ساعة)',
      'Not Applicable, 35 Ah, 45 Ah, 50 Ah, 60 Ah, 70 Ah, 74 Ah, 80 Ah, 90 Ah, '
      '100 Ah, 120 Ah, 150 Ah, 200 Ah', option='Yes'),
    I('spec', 'Cold Cranking Amps (CCA)', 'تيار البدء البارد',
      'Not Applicable, 300 CCA, 450 CCA, 550 CCA, 650 CCA, 750 CCA, 850 CCA, 1000 CCA'),
    D('spec', 'Battery Technology', 'تقنية البطارية',
      'Not Applicable, Lead Acid (Flooded), Maintenance Free (MF), EFB, AGM, Gel, Lithium'),
    D('elec', 'Voltage', 'الجهد', 'Not Applicable, 12V, 24V, 6V'),
    D('spec', 'Terminal Layout', 'ترتيب الأقطاب',
      'Not Applicable, Right Positive (+), Left Positive (+), Top Terminal, Side Terminal'),
    N('spec', 'Shelf Life (months)', 'مدة الصلاحية (شهر)',
      '12 Months, 24 Months, 36 Months, 48 Months, 60 Months', dtype='Integer'),
    D('cert', 'Certification / Compliance', 'الشهادات والمطابقة', GCC_CERT),
], COMMERCE)
