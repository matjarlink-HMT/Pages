# -*- coding: utf-8 -*-
"""Health, sports, stationery, crafts, gifts, tools, construction, industry, services."""
from lib_core import *

FAM = {}

# ------------------------------------------------------------------ medicine (OTC)
FAM['medicine'] = blk(IDENT, [
    T('main', 'Active Ingredient', 'المادة الفعالة', required='Yes'),
    T('main', 'Generic Name', 'الاسم العلمي'),
    D('spec', 'Dosage Form', 'الشكل الصيدلاني',
      'Tablet, Film-Coated Tablet, Effervescent Tablet, Capsule, Soft Gel Capsule, '
      'Syrup, Oral Suspension, Oral Drops, Sachet / Powder, Injection, '
      'Cream, Ointment, Gel, Eye Drops, Ear Drops, Nasal Spray, Inhaler, '
      'Suppository, Patch, Solution', required='Yes'),
    D('dosage', 'Strength', 'التركيز',
      '5 mg, 10 mg, 20 mg, 25 mg, 40 mg, 50 mg, 100 mg, 200 mg, 250 mg, 400 mg, '
      '500 mg, 600 mg, 850 mg, 1000 mg, 5 mg/5 ml, 100 mg/5 ml, 125 mg/5 ml, '
      '250 mg/5 ml, Other', required='Yes', option='Yes'),
    I('pack', 'Pack Quantity', 'عدد الوحدات في العبوة',
      '10, 12, 14, 16, 20, 21, 24, 28, 30, 50, 60, 90, 100', option='Yes'),
    N('spec', 'Volume (ml)', 'الحجم (مل)',
      'Not Applicable, 5 ml, 10 ml, 15 ml, 30 ml, 60 ml, 100 ml, 120 ml, 150 ml, 200 ml'),
    D('dosage', 'Route of Administration', 'طريقة الإعطاء',
      'Oral, Topical, Ophthalmic (Eye), Otic (Ear), Nasal, Inhalation, '
      'Rectal, Intramuscular, Intravenous, Subcutaneous, Transdermal'),
    D('spec', 'Therapeutic Class', 'التصنيف العلاجي',
      'Analgesic / Pain Relief, Antipyretic, Anti-Inflammatory (NSAID), Antibiotic, '
      'Antihistamine / Allergy, Antacid / Digestive, Antidiabetic, Antihypertensive, '
      'Cough & Cold, Antifungal, Antiviral, Vitamin & Mineral, Laxative, '
      'Antiemetic, Dermatological, Respiratory', required='Yes'),
    D('dosage', 'Prescription Requirement', 'اشتراط الوصفة',
      'Over-the-Counter (OTC), Prescription Only (POM), Pharmacy Only, Controlled',
      required='Yes'),
    D('usage', 'Age Group', 'الفئة العمرية',
      'Adults, Adults & Children Above 12, Children (2-12 Years), Infants (Under 2), '
      'Elderly, All Ages'),
    T('dosage', 'Recommended Dosage', 'الجرعة الموصى بها'),
    T('spec', 'Indications / Uses', 'دواعي الاستعمال'),
    T('safety', 'Contraindications', 'موانع الاستعمال'),
    T('safety', 'Side Effects', 'الآثار الجانبية'),
    T('safety', 'Warnings & Precautions', 'التحذيرات والاحتياطات'),
    B('safety', 'Safe During Pregnancy', 'آمن أثناء الحمل'),
    B('safety', 'Safe During Breastfeeding', 'آمن أثناء الرضاعة'),
    B('safety', 'May Cause Drowsiness', 'قد يسبب النعاس'),
    D('spec', 'Storage Condition', 'ظروف التخزين',
      'Store Below 25°C, Store Below 30°C, Refrigerate (2-8°C), '
      'Protect from Light, Cool & Dry Place, Do Not Freeze'),
    N('spec', 'Shelf Life (months)', 'مدة الصلاحية (شهر)',
      '12 Months, 18 Months, 24 Months, 36 Months, 48 Months, 60 Months', dtype='Integer'),
    T('cert', 'Registration Number (MOH)', 'رقم التسجيل لدى وزارة الصحة'),
    T('main', 'Manufacturer', 'الشركة المصنّعة'),
    D('origin', 'Country of Origin', 'بلد المنشأ', ORIGIN),
    B('cert', 'Halal Certified', 'حاصل على شهادة حلال'),
    T('pack', 'Package Contents', 'محتويات العبوة'),
])

# ------------------------------------------------------------------ supplements
FAM['supplement'] = blk(IDENT, [
    D('spec', 'Supplement Type', 'نوع المكمّل',
      'Multivitamin, Vitamin C, Vitamin D, Vitamin B Complex, Omega-3 / Fish Oil, '
      'Calcium, Iron, Zinc, Magnesium, Probiotic, Collagen, Biotin, '
      'Herbal Supplement, Protein Powder, Amino Acids / BCAA, Creatine, '
      'Pre-Workout, Fat Burner, Mass Gainer, Meal Replacement, Fibre',
      required='Yes'),
    D('spec', 'Form', 'الشكل',
      'Tablet, Capsule, Soft Gel, Gummy, Powder, Liquid, Effervescent Tablet, '
      'Sachet, Chewable, Drops, Ready-to-Drink'),
    D('dosage', 'Strength / Dosage', 'التركيز / الجرعة',
      '400 IU, 1000 IU, 2000 IU, 5000 IU, 100 mg, 250 mg, 500 mg, 1000 mg, '
      '1200 mg, 2000 mg, 5 g, 10 g, 25 g, 30 g, Other', option='Yes'),
    I('pack', 'Count per Pack', 'عدد الوحدات',
      '30, 60, 90, 100, 120, 150, 180, 200, 250, 300', option='Yes'),
    N('spec', 'Net Weight (g)', 'الوزن الصافي (جم)',
      'Not Applicable, 300 g, 450 g, 500 g, 900 g, 1 kg, 2 kg, 2.27 kg, 4.5 kg, 5 kg',
      option='Yes'),
    I('spec', 'Number of Servings', 'عدد الحصص',
      '15, 20, 25, 30, 40, 50, 60, 75, 100, 120'),
    N('nutr', 'Protein per Serving (g)', 'البروتين لكل حصة (جم)',
      'Not Applicable, Under 15 g, 15-20 g, 21-25 g, 26-30 g, Above 30 g'),
    N('nutr', 'Calories per Serving (kcal)', 'السعرات لكل حصة',
      'Not Applicable, Under 100 kcal, 100-150 kcal, 151-250 kcal, '
      '251-500 kcal, Above 500 kcal'),
    D('spec', 'Flavour', 'النكهة',
      'Unflavoured, Vanilla, Chocolate, Strawberry, Banana, Cookies & Cream, '
      'Mango, Orange, Lemon, Mixed Berry, Coffee, Salted Caramel, Watermelon, Grape'),
    D('usage', 'Target Benefit', 'الفائدة المستهدفة',
      'Immunity Support, Bone & Joint Health, Muscle Building, Weight Management, '
      'Energy & Performance, Hair Skin & Nails, Heart Health, Digestive Health, '
      'Brain & Memory, Sleep Support, Eye Health, General Wellness'),
    D('dosage', 'Recommended Serving', 'الجرعة الموصى بها',
      '1 Daily, 2 Daily, 3 Daily, 1 Scoop, 2 Scoops, As Directed'),
    D('usage', 'Gender / Target User', 'الفئة المستهدفة',
      'Adults, Men, Women, Kids, Teens, Seniors, Pregnant Women, Athletes'),
    B('nutr', 'Vegan / Vegetarian', 'نباتي'),
    B('nutr', 'Gluten Free', 'خالٍ من الغلوتين'),
    B('nutr', 'Sugar Free', 'خالٍ من السكر'),
    B('nutr', 'Lactose Free', 'خالٍ من اللاكتوز'),
    B('nutr', 'Non-GMO', 'غير معدّل وراثياً'),
    B('cert', 'Halal Certified', 'حاصل على شهادة حلال'),
    B('cert', 'Third-Party Tested', 'مُختبر من جهة مستقلة'),
    B('cert', 'GMP Certified', 'مطابق لمعايير التصنيع الجيد'),
    B('cert', 'Informed Sport / Banned Substance Tested', 'مُختبر من المواد المحظورة'),
    T('ingr', 'Key Ingredients', 'المكونات الرئيسية'),
    T('safety', 'Allergen Information', 'معلومات مسببات الحساسية'),
    T('safety', 'Warnings', 'التحذيرات'),
    D('spec', 'Storage Condition', 'ظروف التخزين',
      'Cool & Dry Place, Below 25°C, Refrigerate After Opening, Protect from Light'),
    N('spec', 'Shelf Life (months)', 'مدة الصلاحية (شهر)',
      '12 Months, 18 Months, 24 Months, 36 Months', dtype='Integer'),
    D('origin', 'Country of Origin', 'بلد المنشأ', ORIGIN),
])

# ------------------------------------------------------------------ medical device
FAM['medical_device'] = blk(IDENT, [
    D('spec', 'Device Type', 'نوع الجهاز',
      'Blood Pressure Monitor, Glucometer / Blood Glucose Meter, Pulse Oximeter, '
      'Thermometer, Nebuliser, Oxygen Concentrator, CPAP Machine, ECG Monitor, '
      'Wheelchair, Walker / Rollator, Crutches, Cane, Hospital Bed, '
      'Orthopaedic Support, Brace / Splint, TENS Unit, Massage Device, '
      'Surgical Instrument, Examination Tool, Sterilizer, Medical Furniture',
      required='Yes'),
    D('spec', 'Measurement Type', 'نوع القياس',
      'Not Applicable, Upper Arm, Wrist, Finger, Forehead / Temporal, Ear, '
      'Oral, Rectal, Underarm, Non-Contact Infrared'),
    D('spec', 'Display Type', 'نوع الشاشة',
      'LCD Display, LED Display, Backlit LCD, Colour Display, Analog Gauge, No Display'),
    D('perf', 'Measurement Accuracy', 'دقة القياس',
      'Not Specified, ±1%, ±2%, ±3 mmHg, ±0.1°C, ±0.2°C, ±2% SpO2, ±5 mg/dL'),
    I('spec', 'Memory Storage (readings)', 'سعة الذاكرة (قراءات)',
      'No Memory, 30 Readings, 60 Readings, 90 Readings, 120 Readings, '
      '200 Readings, 500 Readings, 1000+ Readings'),
    I('spec', 'Number of User Profiles', 'عدد المستخدمين', 'Not Applicable, 1, 2, 4, 8'),
    D('power', 'Power Source', 'مصدر الطاقة',
      'AA Batteries, AAA Batteries, Button Cell, Rechargeable Battery, '
      'Mains Adapter, USB, Battery & Mains, Manual / No Power'),
    D('conn', 'Connectivity', 'الاتصال',
      'None, Bluetooth, Wi-Fi, USB, Mobile App Sync, Cloud Sync'),
    B('feat', 'Mobile App Support', 'دعم تطبيق الجوال'),
    B('feat', 'Voice Guidance', 'إرشاد صوتي'),
    B('feat', 'Irregular Heartbeat Detection', 'كشف عدم انتظام ضربات القلب'),
    B('feat', 'Automatic Shut-Off', 'إيقاف تلقائي'),
    B('feat', 'Portable / Travel Friendly', 'محمول ومناسب للسفر'),
    D('mat', 'Material', 'الخامة',
      'ABS Plastic, Medical Grade Plastic, Stainless Steel, Aluminium, '
      'Silicone, Latex Free Rubber, Neoprene, Fabric, Carbon Fibre'),
    D('spec', 'Size', 'المقاس',
      'Not Applicable, XS, S, M, L, XL, XXL, Universal / One Size, '
      'Adult, Paediatric, Large Adult', option='Yes'),
    N('spec', 'Weight Capacity (kg)', 'قدرة التحمل (كجم)',
      'Not Applicable, Up to 100 kg, 101-120 kg, 121-150 kg, 151-200 kg, Above 200 kg'),
    D('cert', 'Medical Certification', 'الاعتماد الطبي',
      'CE Marked, FDA Approved, ISO 13485, MDR Compliant, MOH Registered, '
      'ESMA Registered, SFDA Registered, None'),
    B('safety', 'Latex Free', 'خالٍ من اللاتكس'),
    B('safety', 'Sterile', 'معقّم'),
    B('safety', 'Single Use / Disposable', 'للاستخدام مرة واحدة'),
    D('pack', 'Accessories Included', 'الملحقات المرفقة',
      'Carrying Case, Cuff, Test Strips, Lancets, Batteries, Power Adapter, '
      'Mask & Tubing, Probe Covers, User Manual, None'),
    T('spec', 'Technical Specifications', 'المواصفات الفنية'),
    D('usage', 'Intended User', 'المستخدم المستهدف',
      'Home Use, Professional / Clinical, Hospital, Ambulance / Emergency, Both'),
], COLOR, COMMERCE)

# ------------------------------------------------------------------ sports equipment
FAM['sports_equipment'] = blk(IDENT, [
    D('spec', 'Equipment Type', 'نوع المعدة',
      'Treadmill, Exercise Bike, Elliptical, Rowing Machine, Multi Gym, '
      'Dumbbell, Barbell, Weight Plate, Kettlebell, Resistance Band, '
      'Yoga Mat, Exercise Ball, Jump Rope, Pull-Up Bar, Bench, '
      'Football, Basketball, Volleyball, Tennis Racket, Padel Racket, '
      'Badminton Set, Table Tennis, Swimming Gear, Diving Gear, '
      'Bicycle, Skateboard, Boxing Equipment', required='Yes'),
    D('spec', 'Sport / Activity', 'الرياضة / النشاط',
      'Gym & Fitness, Running, Cycling, Football, Basketball, Volleyball, '
      'Tennis, Padel, Badminton, Swimming, Diving, Boxing & MMA, Yoga & Pilates, '
      'Hiking & Trekking, CrossFit, Weightlifting, Athletics, Table Tennis'),
    D('mat', 'Material', 'الخامة',
      'Steel, Stainless Steel, Cast Iron, Aluminium, Rubber, Neoprene, '
      'PVC, TPE, EVA Foam, Carbon Fibre, Fibreglass, Graphite, Wood, '
      'Leather, Synthetic Leather, Nylon, Polyester'),
    N('spec', 'Weight (kg)', 'الوزن (كجم)',
      '0.5 kg, 1 kg, 2 kg, 3 kg, 4 kg, 5 kg, 7.5 kg, 10 kg, 12.5 kg, 15 kg, '
      '20 kg, 25 kg, 30 kg, 40 kg, 50 kg', option='Yes'),
    D('spec', 'Size', 'المقاس',
      'Not Applicable, XS, S, M, L, XL, XXL, One Size, Size 3, Size 4, Size 5, '
      'Junior, Senior, Adult', option='Yes'),
    N('spec', 'Maximum User Weight (kg)', 'أقصى وزن للمستخدم (كجم)',
      'Not Applicable, Up to 90 kg, 91-110 kg, 111-130 kg, 131-150 kg, Above 150 kg'),
    D('perf', 'Resistance Type', 'نوع المقاومة',
      'Not Applicable, Magnetic, Air, Water, Friction, Electromagnetic, '
      'Elastic / Band, Free Weight, Hydraulic'),
    I('perf', 'Resistance Levels', 'مستويات المقاومة',
      'Not Applicable, 8 Levels, 12 Levels, 16 Levels, 20 Levels, 24 Levels, 32 Levels'),
    D('power', 'Motor Power (HP)', 'قدرة المحرك (حصان)',
      'Not Applicable, 1.0 HP, 1.5 HP, 2.0 HP, 2.5 HP, 3.0 HP, 3.5 HP, 4.0 HP'),
    D('perf', 'Speed Range (km/h)', 'نطاق السرعة (كم/س)',
      'Not Applicable, 1-10 km/h, 1-12 km/h, 1-16 km/h, 1-18 km/h, 1-20 km/h, 1-22 km/h'),
    D('perf', 'Incline Levels', 'مستويات الميل',
      'Not Applicable, Manual 3 Levels, Auto 12 Levels, Auto 15 Levels, '
      'Auto 20 Levels, 0-15%, 0-20%'),
    D('display', 'Console / Display', 'الشاشة',
      'Not Applicable, LED Display, LCD Display, Touchscreen, Bluetooth Console, No Display'),
    B('smart', 'App Connectivity', 'اتصال بالتطبيق'),
    B('feat', 'Heart Rate Monitor', 'مراقب نبضات القلب'),
    B('feat', 'Foldable', 'قابل للطي'),
    B('feat', 'Adjustable', 'قابل للتعديل'),
    B('feat', 'Transport Wheels', 'عجلات نقل'),
    B('feat', 'Anti-Slip Surface', 'سطح مانع للانزلاق'),
    B('feat', 'Shock Absorption', 'امتصاص الصدمات'),
    T('dims', 'Assembled Dimensions (L x W x H cm)', 'الأبعاد بعد التركيب (سم)'),
    B('inst', 'Assembly Required', 'يتطلب تركيباً'),
    D('usage', 'Skill Level', 'المستوى',
      'Beginner, Intermediate, Advanced, Professional, All Levels'),
    D('usage', 'Gender', 'الجنس', 'Men, Women, Unisex, Kids'),
    D('usage', 'Indoor / Outdoor', 'داخلي / خارجي', 'Indoor, Outdoor, Indoor & Outdoor'),
    D('cert', 'Certification / Compliance', 'الشهادات والمطابقة',
      'CE, EN 957, ISO 20957, FIFA Quality, ITF Approved, BSCI, None'),
], COLOR, COMMERCE)

# ------------------------------------------------------------------ stationery
FAM['stationery'] = blk(IDENT, [
    D('spec', 'Product Type', 'نوع المنتج',
      'Ballpoint Pen, Gel Pen, Fountain Pen, Rollerball Pen, Marker, Highlighter, '
      'Whiteboard Marker, Permanent Marker, Pencil, Mechanical Pencil, '
      'Colour Pencil, Crayon, Eraser, Sharpener, Correction Pen, Correction Tape, '
      'Notebook, Exercise Book, Diary, Sketchbook, Sticky Notes, File & Folder, '
      'Stapler, Scissors, Glue, Ruler, Calculator, Ink Bottle, Paper Ream',
      required='Yes'),
    D('spec', 'Ink Colour', 'لون الحبر',
      'Not Applicable, Black, Blue, Red, Green, Assorted, Multicolour', option='Yes'),
    N('spec', 'Tip / Point Size (mm)', 'مقاس السن (ملم)',
      'Not Applicable, 0.3 mm, 0.38 mm, 0.5 mm, 0.7 mm, 1.0 mm, 1.2 mm, '
      '1.5 mm, 2.0 mm, 5.0 mm'),
    D('spec', 'Ink Type', 'نوع الحبر',
      'Not Applicable, Oil-Based, Water-Based, Gel Ink, Pigment Ink, '
      'Alcohol-Based, Dry Erase, Permanent'),
    D('spec', 'Pencil Grade', 'درجة القلم الرصاص',
      'Not Applicable, 9H, 6H, 4H, 2H, H, HB, B, 2B, 4B, 6B, 8B, 9B'),
    D('spec', 'Paper Size', 'مقاس الورق',
      'Not Applicable, A3, A4, A5, A6, A7, B5, Letter, Legal, Custom', option='Yes'),
    I('spec', 'Number of Pages / Sheets', 'عدد الصفحات / الأوراق',
      'Not Applicable, 40, 60, 80, 96, 100, 120, 160, 192, 200, 250, 500'),
    I('spec', 'Paper Weight (GSM)', 'وزن الورق (جرام/م²)',
      'Not Applicable, 60 GSM, 70 GSM, 80 GSM, 100 GSM, 120 GSM, 160 GSM, '
      '200 GSM, 250 GSM, 300 GSM'),
    D('spec', 'Ruling Type', 'نوع التسطير',
      'Not Applicable, Ruled / Lined, Squared / Grid, Dotted, Plain / Blank, '
      'Music, Graph'),
    D('spec', 'Binding Type', 'نوع التجليد',
      'Not Applicable, Spiral Bound, Wire-O, Perfect Bound, Stapled, '
      'Hardcover, Softcover, Glue Bound, Ring Binder'),
    D('pack', 'Pack Quantity', 'الكمية في العبوة',
      '1 Piece, 2 Pieces, 3 Pieces, 4 Pieces, 5 Pieces, 6 Pieces, 10 Pieces, '
      '12 Pieces, 20 Pieces, 24 Pieces, 36 Pieces, 48 Pieces, 50 Pieces, 100 Pieces',
      option='Yes'),
    D('mat', 'Material', 'الخامة',
      'Plastic, Metal, Aluminium, Stainless Steel, Wood, Paper / Cardboard, '
      'Rubber, Silicone, Leather, PU Leather, Recycled Material'),
    B('feat', 'Refillable', 'قابل للتعبئة'),
    B('feat', 'Retractable', 'قابل للسحب'),
    B('feat', 'Quick Dry Ink', 'حبر سريع الجفاف'),
    B('feat', 'Waterproof / Smudge Proof', 'مقاوم للماء واللطخ'),
    B('feat', 'Non-Toxic', 'غير سام'),
    B('feat', 'Eco-Friendly / Recycled', 'صديق للبيئة / معاد التدوير'),
    D('usage', 'Recommended Use', 'الاستخدام الموصى به',
      'School, University, Office, Home, Art & Drawing, Technical Drawing, '
      'Professional, Kids'),
    D('usage', 'Age Group', 'الفئة العمرية',
      'Kids (3-6 Years), Kids (7-12 Years), Teens, Adults, All Ages'),
], COLOR, COMMERCE)

# ------------------------------------------------------------------ books
FAM['book'] = blk([
    T('main', 'Title', 'العنوان', required='Yes'),
    T('main', 'Author', 'المؤلف', required='Yes'),
    T('main', 'Publisher', 'دار النشر'),
    T('main', 'ISBN', 'الرقم الدولي المعياري (ISBN)'),
    D('spec', 'Language', 'اللغة',
      'Arabic, English, Arabic & English, French, Urdu, Hindi, Malayalam, '
      'Bengali, Turkish, German, Spanish, Other', required='Yes'),
    D('spec', 'Format / Binding', 'نوع التجليد',
      'Paperback, Hardcover, Board Book, Spiral Bound, eBook (PDF), '
      'eBook (EPUB), Audiobook, Boxed Set', required='Yes'),
    D('spec', 'Genre / Category', 'التصنيف',
      'Novel / Fiction, Non-Fiction, Children Story, Educational / Textbook, '
      'Language Learning, History, Biography, Religion & Islamic, Science, '
      'Self Development, Business & Economics, Psychology, Poetry, '
      'Cooking, Health, Travel, Comics & Manga, Reference / Dictionary'),
    I('spec', 'Number of Pages', 'عدد الصفحات',
      'Under 50, 50-100, 101-200, 201-300, 301-450, 451-700, Above 700'),
    D('spec', 'Edition', 'الطبعة',
      'First Edition, Second Edition, Third Edition, Revised Edition, '
      'Illustrated Edition, Anniversary Edition, International Edition'),
    D('main', 'Publication Year', 'سنة النشر',
      'Before 2000, 2000-2010, 2011-2015, 2016-2020, 2021, 2022, 2023, 2024, 2025, 2026'),
    D('spec', 'Book Size', 'مقاس الكتاب',
      'Pocket Size, A5, B5, A4, Large Format, Square, Custom'),
    D('usage', 'Reading Age / Level', 'العمر / المستوى',
      'Baby (0-2 Years), Toddler (3-5 Years), Kids (6-8 Years), Kids (9-12 Years), '
      'Young Adult (13-17), Adult, Beginner, Intermediate, Advanced, All Ages'),
    D('spec', 'Curriculum / Grade', 'المنهج / الصف',
      'Not Applicable, KG, Grade 1-3, Grade 4-6, Grade 7-9, Grade 10-12, '
      'University, Professional Certification'),
    B('spec', 'Illustrated', 'مصوّر'),
    B('spec', 'Colour Printing', 'طباعة ملونة'),
    B('spec', 'Includes CD / Digital Access', 'يشمل قرصاً أو محتوى رقمياً'),
    B('spec', 'Part of a Series', 'ضمن سلسلة'),
    T('spec', 'Series Name', 'اسم السلسلة'),
    I('pack', 'Number of Volumes', 'عدد المجلدات', '1, 2, 3, 4, 5, 6, 8, 10, 12+'),
    D('general', 'Condition', 'الحالة', 'New, Like New, Very Good, Good, Acceptable, Used'),
    D('origin', 'Country of Origin', 'بلد المنشأ', ORIGIN),
    N('pack', 'Item Weight (kg)', 'وزن المنتج (كجم)', WEIGHT_KG),
])

# ------------------------------------------------------------------ craft / art supply
FAM['craft'] = blk(IDENT, [
    D('spec', 'Product Type', 'نوع المنتج',
      'Acrylic Paint, Watercolour, Oil Paint, Gouache, Poster Colour, '
      'Paint Brush, Palette, Canvas, Drawing Paper, Sketch Pad, '
      'Charcoal, Pastel, Marker Set, Clay, Air Dry Clay, Polymer Clay, '
      'Pottery Glaze, Yarn, Thread, Fabric, Needle, Crochet Hook, '
      'Knitting Needles, Beads, Wire, Glue, Craft Paper, Stickers, '
      'Craft Kit, Carving Tool, Wood Blank, Wax, Wick, Fragrance Oil, Dye, Mould',
      required='Yes'),
    D('spec', 'Craft Category', 'نوع الحرفة',
      'Painting & Drawing, Pottery & Ceramics, Knitting, Crochet, Embroidery, '
      'Cross-Stitch, Sewing, Scrapbooking, Candle Making, Soap Making, '
      'Jewellery Making, Woodworking & Carving, Leather Craft, Macrame, '
      'Model Building, Calligraphy, Origami, Glassblowing, Resin Art'),
    D('mat', 'Material', 'الخامة',
      'Acrylic, Cotton, Wool, Acrylic Yarn, Polyester, Silk, Linen, Wood, '
      'Bamboo, Metal, Stainless Steel, Aluminium, Plastic, Glass, Clay / Ceramic, '
      'Paper, Cardboard, Leather, Silicone, Resin, Soy Wax, Paraffin Wax, Beeswax'),
    D('spec', 'Colour / Shade', 'اللون / الدرجة',
      'Single Colour, Assorted Colours, Primary Colours, Pastel Shades, '
      'Metallic, Neon / Fluorescent, Earth Tones, Black & White', option='Yes'),
    I('pack', 'Number of Pieces / Colours', 'عدد القطع / الألوان',
      '1, 2, 3, 5, 6, 8, 10, 12, 18, 24, 36, 48, 60, 72, 100+', option='Yes'),
    N('spec', 'Volume (ml)', 'الحجم (مل)',
      'Not Applicable, 10 ml, 20 ml, 30 ml, 50 ml, 75 ml, 100 ml, 200 ml, '
      '250 ml, 500 ml, 1 L', option='Yes'),
    N('spec', 'Net Weight (g)', 'الوزن الصافي (جم)',
      'Not Applicable, 25 g, 50 g, 100 g, 200 g, 250 g, 500 g, 1 kg, 2 kg, 5 kg',
      option='Yes'),
    T('dims', 'Size / Dimensions', 'المقاس / الأبعاد'),
    D('spec', 'Grade / Quality', 'الجودة',
      'Student Grade, Artist Grade, Professional Grade, Hobby / Craft Grade'),
    D('spec', 'Finish', 'اللمسة النهائية',
      'Not Applicable, Matte, Satin, Glossy, Metallic, Pearlescent, '
      'Transparent, Opaque, Textured'),
    D('spec', 'Yarn Weight / Thickness', 'سماكة الخيط',
      'Not Applicable, Lace, Super Fine (1), Fine (2), Light (3), Medium / Worsted (4), '
      'Bulky (5), Super Bulky (6), Jumbo (7)'),
    D('spec', 'Needle / Hook Size', 'مقاس الإبرة / السنارة',
      'Not Applicable, 2.0 mm, 2.5 mm, 3.0 mm, 3.5 mm, 4.0 mm, 4.5 mm, 5.0 mm, '
      '6.0 mm, 8.0 mm, 10.0 mm, Assorted Set', option='Yes'),
    B('safety', 'Non-Toxic', 'غير سام'),
    B('safety', 'Washable', 'قابل للغسل'),
    B('feat', 'Quick Drying', 'سريع الجفاف'),
    B('feat', 'Water Resistant', 'مقاوم للماء'),
    B('feat', 'Beginner Friendly', 'مناسب للمبتدئين'),
    B('pack', 'Instructions Included', 'يشمل تعليمات'),
    D('usage', 'Skill Level', 'المستوى', 'Beginner, Intermediate, Advanced, Professional, All Levels'),
    D('usage', 'Age Group', 'الفئة العمرية',
      'Kids (3-6 Years), Kids (7-12 Years), Teens, Adults, All Ages'),
    D('cert', 'Certification / Compliance', 'الشهادات والمطابقة',
      'CE, EN 71-3, ASTM D-4236, AP Non-Toxic Seal, None'),
], COMMERCE)

# ------------------------------------------------------------------ gifts & flowers
FAM['gift'] = blk([
    D('spec', 'Product Type', 'نوع المنتج',
      'Fresh Flower Bouquet, Flowers in Vase, Flowers in Basket, Letterbox Flowers, '
      'Potted Plant, Cake, Cupcakes, Chocolate Box, Sweets, Gift Basket, '
      'Gift Set, Greeting Card, Gift Voucher, Balloon, Teddy Bear, Perfume Gift Set',
      required='Yes'),
    D('spec', 'Occasion', 'المناسبة',
      'Birthday, Anniversary, Wedding, Engagement, New Baby, Graduation, '
      'Congratulations, Get Well Soon, Sympathy / Condolence, Thank You, '
      'I Love You, Just Because, Ramadan, Eid, National Day, Mother\'s Day, '
      'Father\'s Day, Valentine\'s Day, Corporate', required='Yes', option='Yes'),
    D('spec', 'Flower Type', 'نوع الزهور',
      'Not Applicable, Roses, Tulips, Lilies, Orchids, Sunflowers, Carnations, '
      'Gerberas, Hydrangeas, Peonies, Chrysanthemums, Baby\'s Breath, Mixed Flowers'),
    I('spec', 'Number of Stems', 'عدد الزهور',
      'Not Applicable, 5, 10, 12, 15, 20, 24, 30, 50, 99, 100'),
    D('spec', 'Colour Theme', 'لون التنسيق',
      'Red, Pink, White, Yellow, Purple, Orange, Blue, Peach, Mixed / Rainbow, Pastel',
      option='Yes'),
    D('spec', 'Size', 'الحجم', 'Mini, Small, Medium, Large, Extra Large, Deluxe', option='Yes'),
    N('spec', 'Cake Weight (kg)', 'وزن الكيك (كجم)',
      'Not Applicable, 0.5 kg, 1 kg, 1.5 kg, 2 kg, 3 kg, 4 kg, 5 kg', option='Yes'),
    D('spec', 'Cake Flavour', 'نكهة الكيك',
      'Not Applicable, Chocolate, Vanilla, Red Velvet, Strawberry, Lotus / Biscoff, '
      'Cheesecake, Nutella, Caramel, Pistachio, Fruit, Mixed'),
    D('spec', 'Dietary Options', 'الخيارات الغذائية',
      'Not Applicable, Regular, Sugar Free, Gluten Free, Eggless, Vegan, Halal'),
    B('spec', 'Personalisation Available', 'إمكانية التخصيص'),
    T('spec', 'Personalisation Message', 'رسالة التخصيص'),
    B('pack', 'Greeting Card Included', 'يشمل بطاقة تهنئة'),
    B('pack', 'Gift Wrapping Included', 'يشمل تغليف هدية'),
    B('pack', 'Vase Included', 'يشمل مزهرية'),
    D('service', 'Delivery Type', 'نوع التوصيل',
      'Same Day Delivery, Next Day Delivery, Scheduled Delivery, '
      'Standard Delivery, Express Delivery, Self Pickup'),
    D('service', 'Delivery Time Slot', 'وقت التوصيل',
      'Morning (9 AM - 12 PM), Afternoon (12 PM - 4 PM), Evening (4 PM - 8 PM), '
      'Night (8 PM - 11 PM), Any Time'),
    N('spec', 'Freshness / Shelf Life (days)', 'مدة البقاء (يوم)',
      'Not Applicable, 1 Day, 2 Days, 3 Days, 5 Days, 7 Days, 14 Days, 30 Days'),
    T('care', 'Care Instructions', 'تعليمات العناية'),
    D('spec', 'Voucher Value', 'قيمة القسيمة',
      'Not Applicable, 5 OMR, 10 OMR, 20 OMR, 25 OMR, 50 OMR, 100 OMR, '
      '200 OMR, Custom Amount', option='Yes'),
    T('main', 'Brand', 'العلامة التجارية'),
])
