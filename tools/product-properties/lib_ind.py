# -*- coding: utf-8 -*-
"""Tools, construction, plumbing, paint, electrical, industrial, camping, services, food, generic."""
from lib_core import *

FAM = {}

# ------------------------------------------------------------------ power tool
FAM['power_tool'] = blk(IDENT, [
    D('spec', 'Tool Type', 'نوع الأداة',
      'Drill, Impact Drill, Hammer Drill, Rotary Hammer, Screwdriver / Driver, '
      'Impact Driver, Angle Grinder, Circular Saw, Jigsaw, Reciprocating Saw, '
      'Mitre Saw, Table Saw, Chain Saw, Planer, Router, Sander, Polisher, '
      'Heat Gun, Soldering Iron, Nail Gun, Air Compressor, Pressure Washer, '
      'Multi-Tool, Rotary Tool, Demolition Hammer', required='Yes'),
    D('power', 'Power Source', 'مصدر الطاقة',
      'Corded Electric, Cordless (Battery), Pneumatic / Air, Petrol / Gas, Hydraulic',
      required='Yes'),
    D('power', 'Power Input (Watts)', 'قدرة الدخل (واط)',
      'Not Applicable, 400 W, 550 W, 650 W, 750 W, 850 W, 1000 W, 1200 W, '
      '1500 W, 1800 W, 2000 W, 2400 W'),
    D('batt', 'Battery Voltage', 'جهد البطارية',
      'Not Applicable, 3.6V, 12V, 14.4V, 18V, 20V, 24V, 36V, 40V, 56V, 60V',
      option='Yes'),
    D('batt', 'Battery Capacity (Ah)', 'سعة البطارية (أمبير/ساعة)',
      'Not Applicable, 1.5 Ah, 2.0 Ah, 2.5 Ah, 3.0 Ah, 4.0 Ah, 5.0 Ah, '
      '6.0 Ah, 8.0 Ah, 9.0 Ah, 12.0 Ah', option='Yes'),
    I('batt', 'Number of Batteries Included', 'عدد البطاريات المرفقة', '0, 1, 2, 3, 4'),
    B('batt', 'Charger Included', 'يشمل شاحن'),
    D('perf', 'No-Load Speed (RPM)', 'السرعة بدون حمل (دورة/دقيقة)',
      'Under 1000 RPM, 1000-3000 RPM, 3001-6000 RPM, 6001-11000 RPM, '
      '11001-20000 RPM, Above 20000 RPM'),
    D('perf', 'Maximum Torque (Nm)', 'أقصى عزم (نيوتن متر)',
      'Not Applicable, Under 20 Nm, 20-40 Nm, 41-60 Nm, 61-100 Nm, '
      '101-200 Nm, Above 200 Nm'),
    N('spec', 'Chuck Size (mm)', 'مقاس ظرف المثقاب (ملم)',
      'Not Applicable, 6.5 mm, 10 mm, 13 mm, 16 mm, SDS-Plus, SDS-Max'),
    N('spec', 'Disc / Blade Diameter (mm)', 'قطر القرص / النصل (ملم)',
      'Not Applicable, 76 mm, 100 mm, 115 mm, 125 mm, 150 mm, 180 mm, '
      '185 mm, 190 mm, 230 mm, 254 mm, 305 mm'),
    N('perf', 'Maximum Cutting Depth (mm)', 'أقصى عمق قطع (ملم)',
      'Not Applicable, 20 mm, 40 mm, 55 mm, 65 mm, 85 mm, 100 mm, 150 mm'),
    I('perf', 'Impact Rate (BPM)', 'معدل الطرق (طرقة/دقيقة)',
      'Not Applicable, Under 3000 BPM, 3000-15000 BPM, 15001-30000 BPM, Above 30000 BPM'),
    B('feat', 'Variable Speed Control', 'تحكم متغير بالسرعة'),
    B('feat', 'Brushless Motor', 'محرك بدون فحمات'),
    B('feat', 'Soft Start', 'بدء تدريجي'),
    B('feat', 'LED Work Light', 'إضاءة LED للعمل'),
    B('feat', 'Reverse Function', 'وظيفة العكس'),
    B('feat', 'Dust Extraction', 'شفط الغبار'),
    B('feat', 'Anti-Vibration System', 'نظام مضاد للاهتزاز'),
    B('feat', 'Overload Protection', 'حماية من الحمل الزائد'),
    D('elec', 'Voltage', 'الجهد', 'Not Applicable, 110V, 220-240V, 380V'),
    N('pack', 'Item Weight (kg)', 'وزن المنتج (كجم)', WEIGHT_KG),
    B('pack', 'Carry Case Included', 'يشمل حقيبة حمل'),
    B('pack', 'Accessories Included', 'يشمل ملحقات'),
    T('pack', 'Included Accessories', 'الملحقات المرفقة'),
    D('usage', 'Recommended Use', 'الاستخدام الموصى به',
      'DIY / Home Use, Semi-Professional, Professional / Trade, Industrial'),
    D('usage', 'Suitable Materials', 'المواد المناسبة',
      'Wood, Metal, Concrete, Masonry, Tile, Plastic, Drywall, Multi-Material'),
    D('cert', 'Certification / Compliance', 'الشهادات والمطابقة', GCC_CERT),
], COLOR, COMMERCE)

# ------------------------------------------------------------------ hand tool
FAM['hand_tool'] = blk(IDENT, [
    D('spec', 'Tool Type', 'نوع الأداة',
      'Hammer, Screwdriver, Screwdriver Set, Wrench / Spanner, Adjustable Wrench, '
      'Socket Set, Pliers, Cutting Pliers, Wire Stripper, Utility Knife, Saw, '
      'Hacksaw, Chisel, File, Clamp, Vice, Measuring Tape, Spirit Level, '
      'Square, Caliper, Trowel, Float, Putty Knife, Allen Key Set, Tool Box, '
      'Tool Set, Ladder, Scaffolding', required='Yes'),
    D('mat', 'Material', 'الخامة',
      'Chrome Vanadium Steel, Carbon Steel, Stainless Steel, Alloy Steel, '
      'Forged Steel, Aluminium, Fibreglass, Plastic / ABS, Rubber, Wood, '
      'Titanium Coated'),
    D('spec', 'Size / Dimension', 'المقاس',
      'Not Applicable, 6 mm, 8 mm, 10 mm, 12 mm, 13 mm, 14 mm, 17 mm, 19 mm, '
      '21 mm, 22 mm, 24 mm, 1/4 inch, 3/8 inch, 1/2 inch, Assorted Set',
      option='Yes'),
    I('pack', 'Number of Pieces', 'عدد القطع',
      '1, 2, 3, 5, 6, 8, 10, 12, 18, 20, 24, 40, 46, 57, 82, 108, 150+', option='Yes'),
    D('spec', 'Drive Size', 'مقاس السن',
      'Not Applicable, 1/4 inch, 3/8 inch, 1/2 inch, 3/4 inch, 1 inch'),
    D('mat', 'Handle Material', 'خامة المقبض',
      'Rubber Grip, TPR Bi-Material, Plastic, Wood, Fibreglass, Steel, Cushion Grip'),
    D('spec', 'Finish / Coating', 'التشطيب',
      'Chrome Plated, Nickel Plated, Black Oxide, Powder Coated, Polished, '
      'Zinc Plated, Anti-Rust Coating'),
    N('spec', 'Length (cm)', 'الطول (سم)',
      'Under 10 cm, 10-20 cm, 21-30 cm, 31-50 cm, 51-100 cm, Above 100 cm'),
    N('spec', 'Measuring Range', 'نطاق القياس',
      'Not Applicable, 3 m, 5 m, 7.5 m, 8 m, 10 m, 30 m, 50 m, 0-150 mm, 0-200 mm'),
    N('spec', 'Load Capacity (kg)', 'قدرة التحمل (كجم)',
      'Not Applicable, Up to 50 kg, 51-100 kg, 101-150 kg, 151-200 kg, Above 200 kg'),
    B('feat', 'Insulated (VDE 1000V)', 'معزول كهربائياً (1000 فولت)'),
    B('feat', 'Magnetic Tip', 'رأس مغناطيسي'),
    B('feat', 'Anti-Slip Grip', 'مقبض مانع للانزلاق'),
    B('feat', 'Rust Resistant', 'مقاوم للصدأ'),
    B('feat', 'Ratcheting Mechanism', 'آلية سقاطة'),
    B('feat', 'Foldable / Telescopic', 'قابل للطي / تلسكوبي'),
    B('pack', 'Storage Case Included', 'يشمل علبة حفظ'),
    D('usage', 'Recommended Use', 'الاستخدام الموصى به',
      'DIY / Home Use, Automotive, Electrical, Plumbing, Carpentry, '
      'Construction, Professional / Trade, Industrial'),
    D('cert', 'Certification / Compliance', 'الشهادات والمطابقة',
      'ISO 9001, DIN, ANSI, VDE, GS Mark, CE, GCC Conformity, None'),
], COLOR, COMMERCE)

# ------------------------------------------------------------------ construction material
FAM['construction'] = blk(IDENT, [
    D('spec', 'Material Type', 'نوع المادة',
      'Cement (OPC), White Cement, Ready Mix Concrete, Sand, Aggregate / Gravel, '
      'Concrete Block, Brick, Interlock, Steel Rebar, Steel Section, '
      'Timber / Wood, Plywood, Gypsum Board, Insulation, Waterproofing Membrane, '
      'Tile Adhesive, Grout, Mortar, Plaster, Water Tank, Scaffolding',
      required='Yes'),
    D('spec', 'Grade / Class', 'الدرجة / الفئة',
      'Not Applicable, Grade 42.5N, Grade 52.5N, C20, C25, C30, C35, C40, C50, '
      'Grade 40, Grade 60, Class A, Class B, Class C'),
    D('spec', 'Standard / Specification', 'المواصفة القياسية',
      'ASTM, BS EN, DIN, ISO, GSO (GCC Standard), OS (Omani Standard), '
      'SASO, JIS, Not Specified'),
    N('spec', 'Unit Weight (kg)', 'الوزن للوحدة (كجم)',
      '1 kg, 5 kg, 10 kg, 20 kg, 25 kg, 40 kg, 50 kg, 1000 kg (1 Ton), Bulk',
      option='Yes'),
    D('spec', 'Packaging / Unit of Sale', 'وحدة البيع',
      'Bag, Piece, Square Metre (m²), Cubic Metre (m³), Linear Metre, Ton, '
      'Pallet, Roll, Bundle, Truck Load, Litre', required='Yes'),
    T('dims', 'Dimensions (L x W x H mm)', 'الأبعاد (طول×عرض×ارتفاع ملم)'),
    N('dims', 'Thickness (mm)', 'السماكة (ملم)',
      'Not Applicable, 3 mm, 6 mm, 8 mm, 10 mm, 12 mm, 15 mm, 18 mm, 20 mm, '
      '25 mm, 50 mm, 75 mm, 100 mm, 150 mm, 200 mm'),
    N('spec', 'Diameter (mm)', 'القطر (ملم)',
      'Not Applicable, 8 mm, 10 mm, 12 mm, 16 mm, 20 mm, 25 mm, 32 mm, 40 mm'),
    I('perf', 'Compressive Strength (MPa)', 'مقاومة الانضغاط (ميجاباسكال)',
      'Not Applicable, Under 10 MPa, 10-20 MPa, 21-30 MPa, 31-40 MPa, Above 40 MPa'),
    I('perf', 'Tensile / Yield Strength (MPa)', 'مقاومة الشد (ميجاباسكال)',
      'Not Applicable, 250 MPa, 350 MPa, 420 MPa, 460 MPa, 500 MPa, 550 MPa'),
    N('perf', 'Thermal Conductivity (W/mK)', 'التوصيل الحراري',
      'Not Applicable, Under 0.03, 0.03-0.05, 0.051-0.10, 0.11-0.50, Above 0.50'),
    I('perf', 'Fire Resistance (minutes)', 'مقاومة الحريق (دقيقة)',
      'Not Applicable, 30 min, 60 min, 90 min, 120 min, 180 min, 240 min'),
    I('perf', 'Sound Reduction (dB)', 'عزل الصوت (ديسيبل)',
      'Not Applicable, Under 30 dB, 30-40 dB, 41-50 dB, Above 50 dB'),
    N('spec', 'Coverage (m² per unit)', 'التغطية (م² لكل وحدة)',
      'Not Applicable, Under 1 m², 1-3 m², 3.1-6 m², 6.1-12 m², Above 12 m²'),
    N('spec', 'Water Absorption (%)', 'امتصاص الماء (%)',
      'Not Applicable, Under 0.5%, 0.5-3%, 3.1-6%, 6.1-10%, Above 10%'),
    D('mat', 'Base Material', 'المادة الأساسية',
      'Portland Cement, Concrete, Clay, Steel, Galvanised Steel, Stainless Steel, '
      'Aluminium, Wood / Timber, Gypsum, Polystyrene (EPS/XPS), Polyurethane, '
      'Rock Wool, Fibreglass, Bitumen, Polyethylene, PVC, GRP'),
    D('design', 'Finish / Surface', 'التشطيب / السطح',
      'Not Applicable, Smooth, Textured, Matte, Polished, Glossy, Anti-Slip, '
      'Rustic, Honed, Brushed, Galvanised, Painted'),
    D('usage', 'Application', 'مجال الاستخدام',
      'Structural / Load Bearing, Non-Structural, Flooring, Wall, Ceiling, '
      'Roofing, Foundation, Waterproofing, Thermal Insulation, Acoustic Insulation, '
      'Interior, Exterior, Wet Areas, Landscaping'),
    B('feat', 'Water Resistant', 'مقاوم للماء'),
    B('feat', 'Fire Retardant', 'مقاوم للحريق'),
    B('feat', 'UV Resistant', 'مقاوم للأشعة فوق البنفسجية'),
    B('feat', 'Corrosion Resistant', 'مقاوم للتآكل'),
    D('cert', 'Certification / Compliance', 'الشهادات والمطابقة',
      'ISO 9001, ISO 14001, CE, ASTM Certified, BS EN Certified, '
      'GSO Conformity, Civil Defence Approved, Green Building Certified, None'),
    D('origin', 'Country of Origin', 'بلد المنشأ', ORIGIN),
    D('spec', 'Minimum Order Quantity', 'الحد الأدنى للطلب',
      '1 Unit, 10 Units, 50 Units, 100 Units, 1 Pallet, 1 Ton, 1 Truck Load, Negotiable'),
    D('warr', 'Warranty Period', 'مدة الضمان', WARR_PERIOD),
], COLOR)

# ------------------------------------------------------------------ tiles / flooring
FAM['tiles'] = blk(IDENT, [
    D('spec', 'Product Type', 'نوع المنتج',
      'Ceramic Tile, Porcelain Tile, Marble, Granite, Natural Stone, '
      'Vitrified Tile, Mosaic, Parquet / Wood Flooring, Laminate Flooring, '
      'Vinyl / LVT Flooring, Carpet Tile, Epoxy Flooring, Terrazzo, Skirting, Trim',
      required='Yes'),
    D('dims', 'Tile Size (cm)', 'مقاس البلاطة (سم)',
      '10x10, 15x15, 20x20, 25x40, 30x30, 30x60, 33x33, 40x40, 45x45, 60x60, '
      '60x120, 75x150, 80x80, 90x90, 100x100, 120x240, Custom',
      required='Yes', option='Yes'),
    N('dims', 'Thickness (mm)', 'السماكة (ملم)',
      '6 mm, 8 mm, 9 mm, 10 mm, 12 mm, 15 mm, 20 mm, 30 mm'),
    D('design', 'Surface Finish', 'تشطيب السطح',
      'Glossy / Polished, Matte, Satin, Rustic, Textured, Lappato / Semi-Polished, '
      'Honed, Anti-Slip, Structured, Glazed, Unglazed'),
    D('design', 'Design / Pattern', 'التصميم',
      'Plain / Solid, Marble Effect, Wood Effect, Stone Effect, Concrete / Cement Effect, '
      'Geometric, Mosaic, Decorative, Terrazzo, Metallic, Arabic / Oriental'),
    D('perf', 'PEI Wear Rating', 'تصنيف مقاومة التآكل',
      'Not Applicable, PEI I, PEI II, PEI III, PEI IV, PEI V'),
    D('perf', 'Slip Resistance (R Rating)', 'مقاومة الانزلاق',
      'Not Rated, R9, R10, R11, R12, R13'),
    N('perf', 'Water Absorption (%)', 'امتصاص الماء (%)',
      'Under 0.5% (Porcelain), 0.5-3%, 3.1-6%, 6.1-10%, Above 10%'),
    N('spec', 'Coverage per Box (m²)', 'التغطية لكل صندوق (م²)',
      '0.5 m², 1.0 m², 1.08 m², 1.2 m², 1.44 m², 1.5 m², 1.8 m², 2.0 m², 2.16 m²'),
    I('pack', 'Pieces per Box', 'عدد القطع في الصندوق', '1, 2, 3, 4, 5, 6, 8, 9, 10, 12, 20, 25'),
    N('pack', 'Box Weight (kg)', 'وزن الصندوق (كجم)',
      'Under 10 kg, 10-20 kg, 21-30 kg, 31-40 kg, Above 40 kg'),
    D('spec', 'Edge Type', 'نوع الحافة',
      'Rectified, Non-Rectified, Bevelled, Rounded, Straight'),
    D('usage', 'Application Area', 'مكان الاستخدام',
      'Floor - Indoor, Floor - Outdoor, Wall - Indoor, Wall - Outdoor, '
      'Bathroom, Kitchen, Living Area, Pool / Wet Area, Commercial, '
      'High Traffic, Facade'),
    D('usage', 'Traffic Level', 'مستوى الاستخدام',
      'Light Residential, Residential, Heavy Residential, Light Commercial, '
      'Commercial, Heavy Commercial / Industrial'),
    B('feat', 'Frost Resistant', 'مقاوم للتجمد'),
    B('feat', 'Stain Resistant', 'مقاوم للبقع'),
    B('feat', 'Scratch Resistant', 'مقاوم للخدش'),
    B('feat', 'Underfloor Heating Compatible', 'متوافق مع التدفئة الأرضية'),
    B('feat', 'Anti-Bacterial Coating', 'طلاء مضاد للبكتيريا'),
    D('spec', 'Grade / Quality', 'الجودة', 'Premium / First Grade, Second Grade, Commercial Grade'),
    D('spec', 'Unit of Sale', 'وحدة البيع', 'Per Piece, Per Box, Per Square Metre, Per Pallet'),
    D('origin', 'Country of Origin', 'بلد المنشأ', ORIGIN),
    D('warr', 'Warranty Period', 'مدة الضمان', WARR_PERIOD),
], COLOR)

# ------------------------------------------------------------------ paint
FAM['paint'] = blk(IDENT, [
    D('spec', 'Paint Type', 'نوع الدهان',
      'Emulsion / Water-Based, Oil-Based / Alkyd, Enamel, Primer, Undercoat, '
      'Sealer, Epoxy, Polyurethane, Acrylic, Anti-Rust, Wood Stain, '
      'Varnish / Lacquer, Textured Coating, Spray Paint, Waterproof Coating',
      required='Yes'),
    D('spec', 'Finish', 'اللمعان',
      'Matte, Flat, Eggshell, Satin, Semi-Gloss, Gloss, High Gloss, Textured, Metallic'),
    N('cap', 'Volume (Litres)', 'الحجم (لتر)',
      '0.25 L, 0.5 L, 1 L, 2.5 L, 3.6 L, 4 L, 5 L, 10 L, 18 L, 20 L',
      required='Yes', option='Yes'),
    D('design', 'Colour Family', 'عائلة اللون',
      'White, Off-White / Cream, Beige, Grey, Black, Blue, Green, Yellow, '
      'Orange, Red, Pink, Purple, Brown, Metallic, Clear / Transparent, '
      'Tintable Base', option='Yes'),
    T('design', 'Colour Code / Name', 'رمز اللون / اسمه'),
    N('spec', 'Coverage (m² per Litre)', 'التغطية (م² لكل لتر)',
      'Under 8 m²/L, 8-11 m²/L, 12-14 m²/L, 15-18 m²/L, Above 18 m²/L'),
    I('spec', 'Drying Time (hours)', 'زمن الجفاف (ساعة)',
      'Under 1 Hour, 1-2 Hours, 3-4 Hours, 5-8 Hours, 12 Hours, 24 Hours'),
    I('spec', 'Recoat Time (hours)', 'زمن إعادة الطلاء (ساعة)',
      '1 Hour, 2 Hours, 4 Hours, 6 Hours, 8 Hours, 12 Hours, 24 Hours'),
    I('spec', 'Number of Coats Recommended', 'عدد الطبقات الموصى بها', '1, 2, 3, 4'),
    D('spec', 'Application Method', 'طريقة التطبيق',
      'Brush, Roller, Spray Gun, Airless Spray, Aerosol, Trowel, Brush & Roller'),
    D('usage', 'Surface Type', 'نوع السطح',
      'Interior Wall, Exterior Wall, Ceiling, Wood, Metal, Concrete, Plaster, '
      'Gypsum Board, Floor, Roof, Marine, Multi-Surface'),
    D('usage', 'Indoor / Outdoor', 'داخلي / خارجي', 'Interior, Exterior, Interior & Exterior'),
    B('feat', 'Washable', 'قابل للغسل'),
    B('feat', 'Anti-Fungal / Anti-Mould', 'مضاد للفطريات والعفن'),
    B('feat', 'Anti-Bacterial', 'مضاد للبكتيريا'),
    B('feat', 'Low VOC / Odourless', 'منخفض الانبعاثات / عديم الرائحة'),
    B('feat', 'Lead Free', 'خالٍ من الرصاص'),
    B('feat', 'Heat Reflective', 'عاكس للحرارة'),
    B('feat', 'Weather Resistant', 'مقاوم للعوامل الجوية'),
    B('feat', 'Stain Resistant', 'مقاوم للبقع'),
    N('spec', 'Shelf Life (months)', 'مدة الصلاحية (شهر)',
      '12 Months, 24 Months, 36 Months, 60 Months', dtype='Integer'),
    D('cert', 'Certification / Compliance', 'الشهادات والمطابقة',
      'ISO 9001, Green Building / LEED, GSO Conformity, ASTM, BS EN, Low VOC Certified, None'),
    D('origin', 'Country of Origin', 'بلد المنشأ', ORIGIN),
    D('warr', 'Warranty Period', 'مدة الضمان', WARR_PERIOD),
])

# ------------------------------------------------------------------ sanitary / plumbing
FAM['sanitary'] = blk(IDENT, [
    D('spec', 'Product Type', 'نوع المنتج',
      'Toilet / WC, Toilet Seat, Washbasin, Basin Mixer, Sink Mixer, Shower Mixer, '
      'Shower Head, Shower Set, Bathtub, Bidet / Shattaf, Urinal, Floor Drain, '
      'Angle Valve, Water Pipe, Pipe Fitting, Water Pump, Water Heater, '
      'Water Filter, Water Tank, Flush Tank, Towel Rail, Bathroom Accessory',
      required='Yes'),
    D('mat', 'Material', 'الخامة',
      'Ceramic / Vitreous China, Porcelain, Brass, Chrome-Plated Brass, '
      'Stainless Steel, Acrylic, ABS Plastic, PVC, CPVC, PPR, HDPE, '
      'Cast Iron, Copper, Glass, Stone / Marble', required='Yes'),
    D('design', 'Finish', 'التشطيب',
      'Chrome, Brushed Nickel, Matte Black, Brushed Gold, Rose Gold, '
      'Stainless Steel, White, Bronze, Gunmetal, Copper', option='Yes'),
    D('inst', 'Installation Type', 'نوع التركيب',
      'Wall Mounted, Floor Mounted, Countertop, Under-Counter, Semi-Recessed, '
      'Deck Mounted, Concealed / Built-In, Free Standing, In-Line'),
    N('spec', 'Size / Diameter', 'المقاس / القطر',
      'Not Applicable, 1/2 inch, 3/4 inch, 1 inch, 1.5 inch, 2 inch, 3 inch, '
      '4 inch, 20 mm, 25 mm, 32 mm, 40 mm, 50 mm, 63 mm, 110 mm', option='Yes'),
    T('dims', 'Dimensions (L x W x H mm)', 'الأبعاد (طول×عرض×ارتفاع ملم)'),
    D('spec', 'Flush Type', 'نوع السيفون',
      'Not Applicable, Single Flush, Dual Flush, Wash Down, Siphonic, '
      'Rimless, Pressure Assisted'),
    N('env', 'Flush Volume (Litres)', 'كمية الشطف (لتر)',
      'Not Applicable, 3/4.5 L, 3/6 L, 4.5 L, 6 L, 9 L'),
    N('perf', 'Flow Rate (L/min)', 'معدل التدفق (لتر/دقيقة)',
      'Not Applicable, Under 6 L/min, 6-9 L/min, 10-15 L/min, 16-25 L/min, Above 25 L/min'),
    N('perf', 'Working Pressure (Bar)', 'ضغط التشغيل (بار)',
      'Not Applicable, 0.5-3 Bar, 1-6 Bar, 1-10 Bar, Up to 16 Bar, Up to 20 Bar'),
    N('perf', 'Maximum Temperature (°C)', 'أقصى درجة حرارة (°م)',
      'Not Applicable, 60°C, 70°C, 80°C, 90°C, 95°C'),
    N('cap', 'Capacity (Litres)', 'السعة (لتر)',
      'Not Applicable, 6 L, 10 L, 15 L, 30 L, 50 L, 80 L, 100 L, 150 L, '
      '200 L, 500 L, 1000 L, 2000 L, 5000 L', option='Yes'),
    D('power', 'Power (Watts)', 'القدرة (واط)',
      'Not Applicable, 370 W, 550 W, 750 W, 1100 W, 1500 W, 2000 W, 3000 W, 4500 W'),
    B('feat', 'Thermostatic Control', 'تحكم حراري'),
    B('feat', 'Water Saving', 'موفّر للمياه'),
    B('feat', 'Anti-Scale', 'مضاد للترسبات'),
    B('feat', 'Soft Close', 'إغلاق ناعم'),
    B('feat', 'Anti-Bacterial Glaze', 'طلاء مضاد للبكتيريا'),
    B('feat', 'Ceramic Cartridge', 'خرطوشة سيراميك'),
    B('feat', 'Insulated', 'معزول'),
    B('pack', 'Installation Kit Included', 'يشمل طقم التركيب'),
    D('cert', 'Certification / Compliance', 'الشهادات والمطابقة',
      'ISO 9001, CE, WRAS Approved, NSF, WaterMark, GSO Conformity, KIWA, None'),
    D('warr', 'Warranty Period', 'مدة الضمان', WARR_PERIOD),
    D('origin', 'Country of Origin', 'بلد المنشأ', ORIGIN),
], COLOR)

# ------------------------------------------------------------------ electrical component
FAM['electrical'] = blk(IDENT, [
    D('spec', 'Product Type', 'نوع المنتج',
      'Wall Switch, Power Socket, Dimmer Switch, Smart Switch, Socket Adapter, '
      'Extension Cord, Circuit Breaker (MCB), RCCB / RCD, Distribution Board, '
      'Contactor, Relay, Cable / Wire, Conduit, Junction Box, Timer, '
      'Voltage Stabiliser, UPS, Inverter, Transformer, Generator', required='Yes'),
    D('elec', 'Rated Voltage', 'الجهد المقنن',
      '12V, 24V, 110V, 220-240V, 380-415V, 415V 3-Phase, 12/24V DC', required='Yes'),
    D('elec', 'Rated Current (Amps)', 'التيار المقنن (أمبير)',
      '6A, 10A, 13A, 16A, 20A, 25A, 32A, 40A, 45A, 50A, 63A, 80A, 100A, 125A',
      option='Yes'),
    D('elec', 'Power Rating (Watts / kVA)', 'القدرة',
      'Not Applicable, 300 W, 600 W, 1000 W, 1500 W, 2000 W, 3000 W, 5 kVA, '
      '10 kVA, 15 kVA, 20 kVA, 30 kVA, 50 kVA, 100 kVA'),
    D('elec', 'Frequency', 'التردد', '50 Hz, 60 Hz, 50/60 Hz, DC'),
    I('spec', 'Number of Gangs / Poles', 'عدد المفاتيح / الأقطاب',
      'Not Applicable, 1, 2, 3, 4, 6, 8, 12'),
    I('spec', 'Number of Ways / Modules', 'عدد الخطوط',
      'Not Applicable, 4, 6, 8, 12, 16, 18, 24, 36, 48'),
    D('spec', 'Breaking Capacity (kA)', 'قدرة القطع',
      'Not Applicable, 3 kA, 4.5 kA, 6 kA, 10 kA, 15 kA, 25 kA'),
    D('spec', 'Tripping Curve', 'منحنى الفصل', 'Not Applicable, Type B, Type C, Type D, Type K'),
    N('spec', 'Cable Cross Section (mm²)', 'مقطع الكابل (ملم²)',
      'Not Applicable, 1.0 mm², 1.5 mm², 2.5 mm², 4 mm², 6 mm², 10 mm², '
      '16 mm², 25 mm², 35 mm², 50 mm², 70 mm², 95 mm², 120 mm²', option='Yes'),
    I('spec', 'Number of Cores', 'عدد النواقل', 'Not Applicable, 1, 2, 3, 4, 5, 7, 12'),
    N('spec', 'Cable Length (m)', 'طول الكابل (متر)',
      'Not Applicable, 1 m, 1.5 m, 3 m, 5 m, 10 m, 20 m, 50 m, 100 m, 500 m',
      option='Yes'),
    D('mat', 'Conductor Material', 'خامة الموصل',
      'Not Applicable, Copper, Tinned Copper, Aluminium, Copper Clad Aluminium'),
    D('mat', 'Insulation Material', 'مادة العزل',
      'Not Applicable, PVC, XLPE, LSZH (Low Smoke Zero Halogen), Rubber, Silicone, PTFE'),
    D('mat', 'Body Material', 'خامة الهيكل',
      'PC (Polycarbonate), ABS, PVC, Bakelite, Thermoplastic, Metal, Stainless Steel, Glass'),
    D('inst', 'Mounting Type', 'طريقة التركيب',
      'Flush / Recessed, Surface Mounted, DIN Rail, Panel Mount, Portable, In-Line'),
    D('safety', 'IP Rating', 'درجة الحماية IP', IP_RATING),
    B('safety', 'Child Safety Shutters', 'حماية أطفال'),
    B('safety', 'Surge Protection', 'حماية من التيار المفاجئ'),
    B('feat', 'USB Charging Ports', 'منافذ شحن USB'),
    B('feat', 'LED Indicator', 'مؤشر LED'),
    B('smart', 'Smart / App Controlled', 'ذكي / يتحكم به عبر التطبيق'),
    B('feat', 'Fire Retardant Material', 'مادة مقاومة للحريق'),
    D('cert', 'Certification / Compliance', 'الشهادات والمطابقة',
      'IEC, BS EN, VDE, CE, RoHS, SASO, GSO Conformity, KEMA, ISO 9001, None'),
    D('warr', 'Warranty Period', 'مدة الضمان', WARR_PERIOD),
    D('origin', 'Country of Origin', 'بلد المنشأ', ORIGIN),
], COLOR)

# ------------------------------------------------------------------ industrial machine
FAM['industrial'] = blk(IDENT, [
    D('spec', 'Machine Type', 'نوع الآلة',
      'CNC Machine, Lathe, Milling Machine, Drilling Machine, Grinding Machine, '
      'Welding Machine, Plasma Cutter, Forklift, Pallet Jack, Conveyor, '
      'Hoist / Crane, Industrial Trolley, Filling Machine, Sealing Machine, '
      'Labelling Machine, Shrink Wrap Machine, Generator, Air Compressor, '
      'Industrial Pump, Electric Motor, Pneumatic Tool, Measuring Instrument',
      required='Yes'),
    D('power', 'Power Rating', 'القدرة',
      'Under 1 kW, 1-3 kW, 3.1-7.5 kW, 7.6-15 kW, 16-30 kW, 31-75 kW, '
      '76-150 kW, Above 150 kW'),
    D('elec', 'Voltage / Phase', 'الجهد / الأطوار',
      '220V Single Phase, 380V Three Phase, 415V Three Phase, 440V Three Phase, '
      'Diesel Powered, Petrol Powered, Hydraulic'),
    N('perf', 'Load / Lifting Capacity (kg)', 'قدرة التحميل (كجم)',
      'Not Applicable, Up to 500 kg, 501-1500 kg, 1501-3000 kg, 3001-5000 kg, '
      '5001-10000 kg, Above 10000 kg', option='Yes'),
    D('perf', 'Working Speed / RPM', 'سرعة التشغيل',
      'Not Applicable, Under 500 RPM, 500-1500 RPM, 1501-3000 RPM, '
      '3001-8000 RPM, Above 8000 RPM'),
    T('perf', 'Working Area / Travel (mm)', 'مساحة العمل (ملم)'),
    D('spec', 'Control System', 'نظام التحكم',
      'Manual, Semi-Automatic, Fully Automatic, CNC, PLC Controlled, '
      'Touchscreen HMI, Remote Controlled'),
    I('spec', 'Number of Axes', 'عدد المحاور', 'Not Applicable, 2, 3, 4, 5, 6, 7'),
    N('perf', 'Accuracy / Tolerance (mm)', 'الدقة (ملم)',
      'Not Applicable, ±0.001 mm, ±0.01 mm, ±0.05 mm, ±0.1 mm, ±0.5 mm'),
    N('perf', 'Output / Capacity per Hour', 'الإنتاجية بالساعة',
      'Not Applicable, Under 100 Units, 100-500 Units, 501-2000 Units, '
      '2001-10000 Units, Above 10000 Units'),
    N('cap', 'Tank / Reservoir Capacity (L)', 'سعة الخزان (لتر)',
      'Not Applicable, 10 L, 24 L, 50 L, 100 L, 200 L, 300 L, 500 L, 1000 L'),
    N('perf', 'Working Pressure (Bar)', 'ضغط التشغيل (بار)',
      'Not Applicable, Up to 8 Bar, 9-12 Bar, 13-20 Bar, 21-50 Bar, Above 50 Bar'),
    D('spec', 'Cooling System', 'نظام التبريد',
      'Not Applicable, Air Cooled, Water Cooled, Oil Cooled, Fan Cooled'),
    D('spec', 'Duty Cycle', 'دورة التشغيل',
      'Not Applicable, S1 Continuous, S3 25%, S3 35%, S3 60%, Intermittent'),
    T('dims', 'Machine Dimensions (L x W x H mm)', 'أبعاد الآلة (ملم)'),
    N('pack', 'Machine Weight (kg)', 'وزن الآلة (كجم)',
      'Under 50 kg, 50-200 kg, 201-500 kg, 501-1500 kg, 1501-5000 kg, Above 5000 kg'),
    D('spec', 'Automation Level', 'مستوى الأتمتة',
      'Manual, Semi-Automatic, Automatic, Fully Automated Line, Robotic'),
    B('safety', 'Emergency Stop', 'زر إيقاف طوارئ'),
    B('safety', 'Safety Guard / Enclosure', 'حاجز أمان'),
    B('safety', 'Overload Protection', 'حماية من الحمل الزائد'),
    B('service', 'Installation Service Available', 'تتوفر خدمة التركيب'),
    B('service', 'Training Provided', 'يشمل تدريباً'),
    B('service', 'Spare Parts Available', 'تتوفر قطع غيار'),
    D('cert', 'Certification / Compliance', 'الشهادات والمطابقة',
      'CE, ISO 9001, ISO 45001, OSHA, ANSI, EN Standards, GSO Conformity, None'),
    D('warr', 'Warranty Period', 'مدة الضمان', WARR_PERIOD),
    D('general', 'Condition', 'الحالة', COND, required='Yes'),
    D('origin', 'Country of Origin', 'بلد المنشأ', ORIGIN),
    D('spec', 'Minimum Order Quantity', 'الحد الأدنى للطلب', '1 Unit, 2 Units, 5 Units, 10 Units, Negotiable'),
])

# ------------------------------------------------------------------ safety / PPE
FAM['safety_ppe'] = blk(IDENT, [
    D('spec', 'Product Type', 'نوع المنتج',
      'Safety Helmet, Safety Goggles, Face Shield, Ear Protection, Respirator, '
      'Dust Mask, Safety Gloves, Cut-Resistant Gloves, Chemical Gloves, '
      'Safety Shoes, Safety Boots, High-Visibility Vest, Coverall, '
      'Fire-Retardant Clothing, Safety Harness, Knee Pads, First Aid Kit, '
      'Fire Extinguisher, Safety Sign', required='Yes'),
    D('mat', 'Material', 'الخامة',
      'HDPE, ABS, Polycarbonate, Nitrile, Latex, PVC, Leather, Cotton, '
      'Polyester, Kevlar / Aramid, Nomex, Neoprene, Steel, Rubber, Polypropylene'),
    D('spec', 'Size', 'المقاس',
      'XS, S, M, L, XL, XXL, 3XL, One Size / Universal, '
      'EU 39, EU 40, EU 41, EU 42, EU 43, EU 44, EU 45, EU 46', option='Yes'),
    D('cert', 'Safety Standard', 'معيار السلامة',
      'EN 397 (Helmet), EN 166 (Eye), EN 352 (Hearing), EN 149 FFP1, '
      'EN 149 FFP2, EN 149 FFP3, EN 388 (Mechanical), EN ISO 20345 (Footwear), '
      'EN ISO 20471 (Hi-Vis), EN 361 (Harness), ANSI Z87.1, ANSI Z89.1, '
      'NIOSH N95, CE Marked, None', required='Yes'),
    D('spec', 'Protection Level', 'مستوى الحماية',
      'Not Applicable, S1, S1P, S3, S5, FFP1, FFP2, FFP3, N95, Class 1, '
      'Class 2, Class 3, Level A, Level B, Level C'),
    D('spec', 'Protection Against', 'الحماية من',
      'Impact, Cut, Abrasion, Puncture, Chemical, Heat & Flame, Cold, '
      'Electrical / Arc Flash, Dust & Particles, Chemical Vapour, '
      'UV Radiation, Noise, Falls from Height, Water'),
    D('spec', 'Toe Cap Type', 'نوع مقدمة الحذاء',
      'Not Applicable, Steel Toe, Composite Toe, Aluminium Toe, Soft Toe'),
    I('perf', 'Noise Reduction Rating (dB)', 'خفض الضوضاء (ديسيبل)',
      'Not Applicable, 20 dB, 25 dB, 28 dB, 30 dB, 33 dB, 37 dB'),
    D('spec', 'Filter Class', 'فئة الفلتر',
      'Not Applicable, P1, P2, P3, A1, A2, ABEK1, ABEK2, Combined'),
    N('spec', 'Fire Extinguisher Capacity (kg)', 'سعة الطفاية (كجم)',
      'Not Applicable, 1 kg, 2 kg, 4 kg, 6 kg, 9 kg, 12 kg, 25 kg, 50 kg'),
    D('spec', 'Extinguisher Type', 'نوع الطفاية',
      'Not Applicable, Dry Powder (ABC), CO2, Foam, Water, Wet Chemical, Clean Agent'),
    I('pack', 'Quantity per Pack', 'الكمية في العبوة',
      '1, 2, 5, 10, 12, 20, 25, 50, 100, 200', option='Yes'),
    B('feat', 'Reusable', 'قابل لإعادة الاستخدام'),
    B('feat', 'Disposable / Single Use', 'للاستخدام مرة واحدة'),
    B('feat', 'Adjustable', 'قابل للتعديل'),
    B('feat', 'Anti-Fog Coating', 'طلاء مضاد للضباب'),
    B('feat', 'Anti-Static', 'مضاد للكهرباء الساكنة'),
    B('feat', 'Waterproof', 'مقاوم للماء'),
    B('feat', 'Breathable', 'قابل للتهوية'),
    B('feat', 'Reflective Strips', 'شرائط عاكسة'),
    D('usage', 'Industry / Application', 'المجال',
      'Construction, Oil & Gas, Manufacturing, Electrical Work, Welding, '
      'Chemical Handling, Healthcare, Food Processing, Laboratory, '
      'Warehouse & Logistics, Firefighting, General Purpose'),
    D('spec', 'Expiry / Service Life', 'مدة الصلاحية',
      'Not Applicable, 1 Year, 2 Years, 3 Years, 5 Years, 10 Years, Check Label'),
], COLOR, COMMERCE)
