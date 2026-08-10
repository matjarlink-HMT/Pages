# -*- coding: utf-8 -*-
"""Camping, food, beverages, decor, garden, courses, services, generic fallback."""
from lib_core import *

FAM = {}

# ------------------------------------------------------------------ camping / outdoor gear
FAM['camping'] = blk(IDENT, [
    D('spec', 'Product Type', 'نوع المنتج',
      'Tent, Shelter / Canopy, Sleeping Bag, Sleeping Mat, Air Mattress, '
      'Camping Chair, Camping Table, Camping Stove, Cooler Box, Ice Box, '
      'Camping Cookware, Camping Lantern, Headlamp, Torch / Flashlight, '
      'Hammock, Air Pump, Water Container, Backpack, Tent Accessory, '
      'Isothermal Case, Portable Toilet, Camping Shower', required='Yes'),
    I('spec', 'Capacity (Persons)', 'السعة (عدد الأشخاص)',
      'Not Applicable, 1 Person, 2 Persons, 3 Persons, 4 Persons, 5 Persons, '
      '6 Persons, 8 Persons, 10 Persons, 12+ Persons', option='Yes'),
    D('mat', 'Material', 'الخامة',
      'Polyester, Nylon, Ripstop Nylon, Oxford Fabric, Canvas / Cotton, '
      'PVC Coated, PU Coated, Aluminium, Steel, Fibreglass, Plastic / PP, '
      'EVA Foam, Stainless Steel, TPU'),
    N('spec', 'Water Resistance (mm Hydrostatic Head)', 'مقاومة الماء (ملم)',
      'Not Applicable, 1000 mm, 1500 mm, 2000 mm, 3000 mm, 5000 mm, Above 5000 mm'),
    D('spec', 'Season Rating', 'التصنيف الموسمي',
      'Not Applicable, 1 Season, 2 Season, 3 Season, 4 Season, All Season'),
    N('spec', 'Temperature Rating (°C)', 'درجة الحرارة المناسبة (°م)',
      'Not Applicable, +15°C, +10°C, +5°C, 0°C, -5°C, -10°C, -20°C'),
    T('dims', 'Dimensions (L x W x H cm)', 'الأبعاد (طول×عرض×ارتفاع سم)'),
    T('dims', 'Packed Size (cm)', 'المقاس عند الطي (سم)'),
    N('pack', 'Weight (kg)', 'الوزن (كجم)',
      'Under 1 kg, 1-3 kg, 3.1-5 kg, 5.1-10 kg, 10.1-20 kg, Above 20 kg'),
    N('cap', 'Capacity (Litres)', 'السعة (لتر)',
      'Not Applicable, 5 L, 10 L, 20 L, 25 L, 30 L, 40 L, 50 L, 60 L, 80 L, 100 L',
      option='Yes'),
    D('power', 'Power Source', 'مصدر الطاقة',
      'Not Applicable, AA Batteries, AAA Batteries, Rechargeable Battery, '
      'USB Charging, Solar, Gas Cartridge, Charcoal, Petrol, Manual'),
    I('perf', 'Brightness (Lumens)', 'السطوع (لومن)',
      'Not Applicable, Under 100 lm, 100-300 lm, 301-600 lm, 601-1000 lm, Above 1000 lm'),
    N('batt', 'Runtime (hours)', 'مدة التشغيل (ساعة)',
      'Not Applicable, Up to 5 Hours, 6-12 Hours, 13-24 Hours, 25-48 Hours, Above 48 Hours'),
    N('perf', 'Ice Retention (hours)', 'مدة حفظ الثلج (ساعة)',
      'Not Applicable, 12 Hours, 24 Hours, 48 Hours, 72 Hours, 96 Hours, Above 96 Hours'),
    B('feat', 'Waterproof', 'مقاوم للماء'),
    B('feat', 'Windproof', 'مقاوم للرياح'),
    B('feat', 'UV Protection', 'حماية من الأشعة فوق البنفسجية'),
    B('feat', 'Fire Retardant', 'مقاوم للحريق'),
    B('feat', 'Foldable / Collapsible', 'قابل للطي'),
    B('feat', 'Quick Setup / Pop-Up', 'تركيب سريع'),
    B('feat', 'Insulated', 'معزول'),
    B('feat', 'Mosquito Net Included', 'يشمل ناموسية'),
    B('feat', 'Carry Bag Included', 'يشمل حقيبة حمل'),
    D('usage', 'Recommended Use', 'الاستخدام الموصى به',
      'Camping, Hiking & Trekking, Beach, Desert / Sand, Mountain, '
      'Fishing, Picnic, Festival, Backpacking, Car Camping, Emergency'),
    D('spec', 'Setup Type', 'طريقة النصب',
      'Not Applicable, Pole Tent, Pop-Up / Instant, Inflatable, Tunnel, '
      'Dome, Geodesic, Cabin, Rooftop'),
], COLOR, COMMERCE)

# ------------------------------------------------------------------ food (general)
FAM['food'] = blk(FOOD_BASE, [
    D('spec', 'Product Form', 'شكل المنتج',
      'Whole, Sliced, Diced, Minced / Ground, Powder, Paste, Puree, Liquid, '
      'Granules, Flakes, Cubes, Fillet, Ready to Eat, Ready to Cook'),
    D('spec', 'Preparation Required', 'التحضير المطلوب',
      'Ready to Eat, Heat and Serve, Requires Cooking, Requires Soaking, '
      'Add Water, Add Milk, No Preparation'),
    D('nutr', 'Protein per 100 g (g)', 'البروتين لكل 100 جم',
      'Under 1 g, 1-5 g, 5.1-10 g, 10.1-20 g, Above 20 g'),
    D('nutr', 'Fat per 100 g (g)', 'الدهون لكل 100 جم',
      'Under 1 g, 1-5 g, 5.1-15 g, 15.1-30 g, Above 30 g'),
    D('nutr', 'Sugar per 100 g (g)', 'السكر لكل 100 جم',
      'Under 1 g, 1-5 g, 5.1-15 g, 15.1-30 g, Above 30 g'),
    D('nutr', 'Salt / Sodium Content', 'محتوى الملح / الصوديوم',
      'Salt Free, Low Sodium, Medium, High'),
    B('nutr', 'Vegetarian', 'نباتي'),
    B('nutr', 'No Preservatives', 'خالٍ من المواد الحافظة'),
    B('nutr', 'No Artificial Colours', 'خالٍ من الألوان الصناعية'),
    B('nutr', 'Non-GMO', 'غير معدّل وراثياً'),
    D('spec', 'Grade / Quality', 'الدرجة',
      'Premium, Grade A, Grade B, Standard, Economy, Export Quality'),
    D('cert', 'Certification', 'الشهادات',
      'Halal, Organic Certified, ISO 22000, HACCP, FSSC 22000, BRC, '
      'Kosher, Fair Trade, None'),
    D('usage', 'Meal Type', 'نوع الوجبة',
      'Breakfast, Lunch, Dinner, Snack, Dessert, Beverage, Ingredient, Anytime'),
    D('spec', 'Cuisine Type', 'نوع المطبخ',
      'Not Applicable, Arabic / Middle Eastern, Indian, Chinese, Japanese, '
      'Korean, Thai, Filipino, Italian, Mexican, Sri Lankan, Turkish, '
      'American, International'),
    T('spec', 'Serving Suggestion', 'طريقة التقديم المقترحة'),
    N('spec', 'Number of Servings', 'عدد الحصص',
      '1, 2, 3, 4, 5, 6, 8, 10, 12, 20+', dtype='Integer'),
])

# ------------------------------------------------------------------ beverage
FAM['beverage'] = blk(FOOD_BASE, [
    D('spec', 'Beverage Type', 'نوع المشروب',
      'Still Water, Sparkling Water, Soft Drink / Soda, Fruit Juice, '
      'Nectar, Concentrate / Squash, Energy Drink, Sports Drink, '
      'Iced Tea, Tea (Loose), Tea Bags, Ground Coffee, Coffee Beans, '
      'Instant Coffee, Coffee Capsules, Milk, Long Life Milk, Milk Powder, '
      'Flavoured Milk, Plant-Based Milk, Powdered Drink, Malt Drink, '
      'Yoghurt Drink, Mocktail', required='Yes'),
    B('spec', 'Carbonated', 'غازي'),
    D('spec', 'Concentration', 'التركيز',
      'Ready to Drink, Concentrate, Powder, From Concentrate, Not From Concentrate, Freshly Squeezed'),
    N('nutr', 'Caffeine Content (mg)', 'محتوى الكافيين (مجم)',
      'Caffeine Free, Under 30 mg, 30-80 mg, 81-150 mg, 151-250 mg, Above 250 mg'),
    D('spec', 'Fat Content (Dairy)', 'نسبة الدسم',
      'Not Applicable, Full Fat / Full Cream, Semi-Skimmed / Low Fat, '
      'Skimmed / Fat Free, Double Cream'),
    D('spec', 'Roast Level (Coffee)', 'درجة التحميص',
      'Not Applicable, Light Roast, Medium Roast, Medium-Dark Roast, Dark Roast, Espresso Roast'),
    D('spec', 'Grind Type (Coffee)', 'نوع الطحن',
      'Not Applicable, Whole Bean, Coarse Grind, Medium Grind, Fine Grind, '
      'Extra Fine / Turkish, Capsule / Pod'),
    D('spec', 'Tea Type', 'نوع الشاي',
      'Not Applicable, Black Tea, Green Tea, White Tea, Oolong, Herbal / Infusion, '
      'Chamomile, Mint, Karak / Masala, Earl Grey, Jasmine, Hibiscus'),
    B('nutr', 'No Added Sugar', 'بدون سكر مضاف'),
    B('nutr', 'Diet / Zero Calorie', 'دايت / خالٍ من السعرات'),
    B('nutr', 'Vitamin Fortified', 'مدعّم بالفيتامينات'),
    B('nutr', 'Natural / 100% Pure', 'طبيعي 100%'),
    D('spec', 'Serving Temperature', 'درجة حرارة التقديم',
      'Serve Chilled, Serve Hot, Room Temperature, Hot or Cold'),
    D('spec', 'Water Source Type', 'مصدر المياه',
      'Not Applicable, Natural Mineral Water, Spring Water, Purified / RO, '
      'Distilled, Alkaline, Zamzam'),
    N('nutr', 'pH Level', 'درجة الحموضة',
      'Not Applicable, Under 6, 6-7, 7.1-8, 8.1-9, Above 9'),
    B('cert', 'Alcohol Free', 'خالٍ من الكحول'),
])

# ------------------------------------------------------------------ home decor
FAM['decor'] = blk(IDENT, [
    D('spec', 'Product Type', 'نوع المنتج',
      'Wall Art / Painting, Photo Frame, Mirror, Clock, Vase, Candle, '
      'Candle Holder, Decorative Figurine, Decorative Box, Diffuser, '
      'Room Spray, Artificial Plant, Artificial Flower, Plant Pot, '
      'Wall Shelf, Wall Sticker, Curtain Accessory, Table Decor, '
      'Sculpture, Lantern, Tray, Bookend', required='Yes'),
    D('mat', 'Material', 'الخامة',
      'Wood, MDF, Metal, Iron, Brass, Stainless Steel, Aluminium, Glass, '
      'Crystal, Ceramic, Porcelain, Resin, Plastic, Canvas, Fabric, '
      'Rattan, Bamboo, Marble, Stone, Concrete, Paper, Wax, Silk (Artificial)',
      required='Yes'),
    T('dims', 'Dimensions (L x W x H cm)', 'الأبعاد (طول×عرض×ارتفاع سم)'),
    D('spec', 'Size', 'الحجم', 'Mini, Small, Medium, Large, Extra Large, Set', option='Yes'),
    I('pack', 'Number of Pieces', 'عدد القطع', '1, 2, 3, 4, 5, 6, 8, 12'),
    D('design', 'Style', 'الستايل',
      'Modern, Contemporary, Classic, Vintage / Retro, Scandinavian, '
      'Industrial, Bohemian, Minimalist, Luxury / Glam, Oriental / Arabic, '
      'Islamic Calligraphy, Rustic, Coastal, Abstract'),
    D('design', 'Shape', 'الشكل',
      'Round, Square, Rectangular, Oval, Irregular, Geometric, Heart, Star, Arch'),
    D('design', 'Finish', 'التشطيب',
      'Matte, Glossy, Metallic, Antique, Distressed, Brushed, Hammered, '
      'Painted, Natural, Lacquered, Gold Leaf'),
    D('inst', 'Mounting Type', 'طريقة التثبيت',
      'Free Standing, Wall Mounted, Hanging, Table Top, Adhesive, Ceiling Hung'),
    B('inst', 'Mounting Hardware Included', 'يشمل أدوات التثبيت'),
    D('spec', 'Scent', 'الرائحة',
      'Not Applicable, Unscented, Oud, Amber, Vanilla, Lavender, Rose, '
      'Jasmine, Sandalwood, Musk, Citrus, Fresh Linen, Ocean, Coffee'),
    N('spec', 'Burn Time (hours)', 'مدة الاشتعال (ساعة)',
      'Not Applicable, Under 10 Hours, 10-25 Hours, 26-45 Hours, 46-70 Hours, Above 70 Hours'),
    D('power', 'Power Source', 'مصدر الطاقة',
      'Not Applicable, No Power Required, AA Batteries, AAA Batteries, '
      'Button Cell, USB, Mains Adapter, Rechargeable'),
    B('feat', 'LED Lighting', 'إضاءة LED'),
    B('feat', 'Battery Operated', 'يعمل بالبطارية'),
    B('feat', 'Handmade', 'صناعة يدوية'),
    B('feat', 'Personalisable', 'قابل للتخصيص'),
    D('usage', 'Room Type', 'نوع الغرفة',
      'Living Room, Bedroom, Dining Room, Kitchen, Bathroom, Home Office, '
      'Kids Room, Majlis, Entryway, Outdoor / Garden, Office'),
    D('usage', 'Occasion', 'المناسبة',
      'Everyday, Ramadan & Eid, Wedding, Birthday, National Day, '
      'Housewarming, Gift, Seasonal'),
    T('care', 'Care Instructions', 'تعليمات العناية'),
], COLOR, COMMERCE)

# ------------------------------------------------------------------ garden / outdoor living
FAM['garden'] = blk(IDENT, [
    D('spec', 'Product Type', 'نوع المنتج',
      'Outdoor Sofa Set, Outdoor Dining Set, Outdoor Chair, Outdoor Bench, '
      'Sun Lounger, Balcony Set, Gazebo, Pergola, Outdoor Umbrella, '
      'Outdoor Cushion, Garden Ornament, Fountain, Plant Pot, Planter, '
      'Artificial Grass, Garden Fence, Swing, BBQ Grill, Fire Pit, '
      'Garden Tool, Hose & Irrigation, Outdoor Storage', required='Yes'),
    D('mat', 'Material', 'الخامة',
      'PE Rattan / Wicker, Natural Rattan, Aluminium, Powder-Coated Steel, '
      'Stainless Steel, Teak Wood, Acacia Wood, Eucalyptus Wood, '
      'HDPE Plastic, Polypropylene, Concrete, Ceramic, Terracotta, '
      'Fibreglass, Tempered Glass, Textilene Fabric, Olefin Fabric', required='Yes'),
    D('mat', 'Frame Material', 'خامة الهيكل',
      'Not Applicable, Aluminium, Powder-Coated Steel, Stainless Steel, '
      'Wood, PVC, Fibreglass'),
    T('dims', 'Dimensions (L x W x H cm)', 'الأبعاد (طول×عرض×ارتفاع سم)'),
    D('spec', 'Seating Capacity', 'عدد المقاعد',
      'Not Applicable, 1 Seater, 2 Seater, 3 Seater, 4 Seater, 6 Seater, '
      '8 Seater, 10 Seater, 12+ Seater', option='Yes'),
    I('pack', 'Number of Pieces', 'عدد القطع', '1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 13'),
    B('feat', 'Weather Resistant', 'مقاوم للعوامل الجوية'),
    B('feat', 'UV Resistant', 'مقاوم للأشعة فوق البنفسجية'),
    B('feat', 'Waterproof', 'مقاوم للماء'),
    B('feat', 'Rust Resistant', 'مقاوم للصدأ'),
    B('feat', 'Fade Resistant', 'مقاوم لبهتان اللون'),
    B('feat', 'Foldable / Stackable', 'قابل للطي / التكديس'),
    B('feat', 'Cushions Included', 'يشمل وسائد'),
    B('feat', 'Cover Included', 'يشمل غطاء واقياً'),
    B('inst', 'Assembly Required', 'يتطلب تركيباً'),
    N('spec', 'Maximum Load (kg)', 'أقصى حمولة (كجم)',
      'Not Applicable, Up to 100 kg, 101-150 kg, 151-200 kg, 201-300 kg, Above 300 kg'),
    D('power', 'Fuel / Power Type', 'نوع الوقود / الطاقة',
      'Not Applicable, Charcoal, Gas / LPG, Electric, Solar, Wood, Manual'),
    N('spec', 'Grill Area (cm²)', 'مساحة الشواية (سم²)',
      'Not Applicable, Under 1000 cm², 1000-2000 cm², 2001-3500 cm², Above 3500 cm²'),
    D('design', 'Style', 'الستايل',
      'Modern, Classic, Tropical, Mediterranean, Minimalist, Rustic, Luxury, Arabic'),
    D('usage', 'Suitable For', 'مناسب لـ',
      'Garden, Patio, Balcony, Terrace, Poolside, Beach, Rooftop, '
      'Restaurant / Cafe, Farm / Estate'),
    T('care', 'Care Instructions', 'تعليمات العناية'),
], COLOR, COMMERCE)

# ------------------------------------------------------------------ online course / training
FAM['course'] = blk([
    T('main', 'Course Title', 'عنوان الدورة', required='Yes'),
    T('main', 'Provider / Instructor', 'الجهة المقدّمة / المدرّب'),
    D('course', 'Skill Level', 'المستوى',
      'Beginner, Intermediate, Advanced, Expert, All Levels', required='Yes'),
    D('course', 'Course Language', 'لغة الدورة',
      'Arabic, English, Arabic & English, French, Hindi, Urdu, Multilingual',
      required='Yes'),
    D('service', 'Delivery Format', 'صيغة التقديم',
      'Self-Paced Video, Live Online (Virtual Classroom), In-Person / Classroom, '
      'Hybrid / Blended, eBook / PDF, Audio Course, One-to-One Coaching, Bootcamp',
      required='Yes'),
    N('course', 'Course Duration (hours)', 'مدة الدورة (ساعة)',
      'Under 2 Hours, 2-5 Hours, 6-10 Hours, 11-20 Hours, 21-40 Hours, '
      '41-80 Hours, Above 80 Hours', option='Yes'),
    D('course', 'Course Duration (weeks)', 'مدة الدورة (أسابيع)',
      'Not Applicable, 1 Week, 2 Weeks, 4 Weeks, 6 Weeks, 8 Weeks, '
      '12 Weeks, 16 Weeks, 6 Months, 12 Months'),
    I('course', 'Number of Lessons / Modules', 'عدد الدروس / الوحدات',
      'Under 10, 10-25, 26-50, 51-100, Above 100'),
    D('course', 'Access Duration', 'مدة الوصول',
      'Lifetime Access, 1 Month, 3 Months, 6 Months, 1 Year, 2 Years, Subscription'),
    B('course', 'Certificate of Completion', 'شهادة إتمام'),
    D('course', 'Certification Type', 'نوع الشهادة',
      'No Certificate, Certificate of Completion, Accredited Certificate, '
      'Professional Certification, University Credit, Diploma'),
    T('course', 'Accreditation Body', 'جهة الاعتماد'),
    D('course', 'Subtitles Available', 'الترجمة المتوفرة',
      'None, Arabic, English, Arabic & English, Multiple Languages'),
    B('course', 'Downloadable Resources', 'موارد قابلة للتحميل'),
    B('course', 'Practical Projects / Assignments', 'مشاريع وتطبيقات عملية'),
    B('course', 'Quizzes & Assessments', 'اختبارات وتقييمات'),
    B('course', 'Instructor Q&A Support', 'دعم ومتابعة من المدرّب'),
    B('course', 'Community / Discussion Access', 'وصول إلى مجتمع الدارسين'),
    B('course', 'Mobile Access', 'إمكانية الوصول عبر الجوال'),
    T('course', 'Prerequisites', 'المتطلبات السابقة'),
    T('course', 'Learning Outcomes', 'مخرجات التعلم'),
    T('course', 'Target Audience', 'الفئة المستهدفة'),
    D('course', 'Topic Category', 'مجال الدورة',
      'Business & Management, Marketing, Finance & Accounting, IT & Software, '
      'Programming & Development, Design & Creative, Data Science, '
      'Personal Development, Health & Fitness, Language Learning, '
      'Teaching & Academics, Photography & Video, Lifestyle, Office Productivity'),
    T('course', 'Software / Tools Covered', 'البرامج والأدوات المشمولة'),
    D('service', 'Class Schedule', 'جدول الحضور',
      'Not Applicable, Weekdays, Weekends, Evenings, Flexible, On Demand'),
    I('service', 'Class Size', 'عدد المشاركين',
      'Not Applicable, One-to-One, Up to 10, 11-25, 26-50, Above 50, Unlimited'),
    D('service', 'Pricing Model', 'نموذج التسعير',
      'One-Time Payment, Monthly Subscription, Annual Subscription, '
      'Per Session, Instalment Plan, Free'),
    D('service', 'Location', 'الموقع',
      'Online / Remote, Muscat, Salalah, Sohar, Nizwa, Sur, On-Site (Client Premises), Multiple Locations'),
    B('service', 'Money-Back Guarantee', 'ضمان استرداد المبلغ'),
])

# ------------------------------------------------------------------ service
FAM['service'] = blk([
    T('main', 'Service Name', 'اسم الخدمة', required='Yes'),
    T('main', 'Provider Name', 'اسم مقدّم الخدمة'),
    D('service', 'Service Category', 'فئة الخدمة',
      'Automotive Services, Beauty & Salon, Health & Medical, Home Maintenance, '
      'Cleaning Services, Engineering & Design, Marketing & Advertising, '
      'IT & Technical Support, Legal & Consulting, Events & Catering, '
      'Logistics & Delivery, Rental Services, Education & Tutoring, '
      'Photography & Video', required='Yes'),
    D('service', 'Service Type', 'نوع الخدمة',
      'One-Time Service, Recurring / Subscription, Package / Bundle, '
      'Retainer, Emergency / On-Demand, Project Based, Hourly'),
    D('service', 'Pricing Model', 'نموذج التسعير',
      'Fixed Price, Hourly Rate, Daily Rate, Per Session, Per Unit / Item, '
      'Monthly Retainer, Per Square Metre, Quotation Based, Free Consultation',
      required='Yes'),
    D('service', 'Service Duration', 'مدة الخدمة',
      'Under 30 Minutes, 30-60 Minutes, 1-2 Hours, 2-4 Hours, Half Day, '
      'Full Day, 2-3 Days, 1 Week, 2-4 Weeks, Above 1 Month, Ongoing'),
    D('service', 'Service Location', 'مكان تقديم الخدمة',
      'At Provider Premises, At Customer Location (Home Service), Online / Remote, '
      'Hybrid, Mobile / On-the-Go', required='Yes'),
    D('service', 'Coverage Area', 'نطاق التغطية',
      'Muscat, Seeb, Bausher, Muttrah, Amerat, Quriyat, Sohar, Salalah, '
      'Nizwa, Sur, Ibri, Barka, Rustaq, Buraimi, Duqm, All Oman, GCC, International'),
    D('service', 'Availability', 'أوقات التوفر',
      'Weekdays, Weekends, Weekdays & Weekends, 24/7, By Appointment, '
      'Morning Only, Evening Only, Seasonal'),
    D('service', 'Booking Method', 'طريقة الحجز',
      'Online Booking, Phone Call, WhatsApp, Walk-In, Mobile App, Email'),
    D('service', 'Advance Notice Required', 'مدة الحجز المسبق',
      'Immediate / Same Day, 1 Day, 2-3 Days, 1 Week, 2 Weeks, 1 Month'),
    D('service', 'Target Customer', 'العميل المستهدف',
      'Individuals, Families, Businesses / B2B, Government, Schools, '
      'Hotels & Restaurants, Contractors, All Customers'),
    D('usage', 'Gender Served', 'الفئة المخدومة',
      'Men, Women, Unisex, Kids, Families, Not Applicable'),
    T('service', 'Service Inclusions', 'ما تشمله الخدمة'),
    T('service', 'Service Exclusions', 'ما لا تشمله الخدمة'),
    B('service', 'Materials / Parts Included', 'يشمل المواد وقطع الغيار'),
    B('service', 'Free Consultation', 'استشارة مجانية'),
    B('service', 'Warranty on Service', 'ضمان على الخدمة'),
    D('warr', 'Service Warranty Period', 'مدة ضمان الخدمة',
      'No Warranty, 7 Days, 15 Days, 1 Month, 3 Months, 6 Months, 1 Year, 2 Years'),
    B('service', 'Licensed / Certified Provider', 'مقدّم خدمة مرخّص'),
    T('cert', 'License / Registration Number', 'رقم الترخيص'),
    B('service', 'Insured', 'مؤمّن'),
    I('service', 'Years of Experience', 'سنوات الخبرة',
      'Under 1 Year, 1-3 Years, 4-7 Years, 8-15 Years, Above 15 Years'),
    B('service', 'Emergency / Same Day Service', 'خدمة طارئة / في نفس اليوم'),
    D('service', 'Payment Methods', 'طرق الدفع',
      'Cash, Card, Bank Transfer, Online Payment, Mobile Wallet, '
      'Instalments, Cash on Delivery'),
    B('service', 'Cancellation / Refund Policy', 'سياسة إلغاء واسترداد'),
    D('spec', 'Language of Service', 'لغة الخدمة',
      'Arabic, English, Arabic & English, Hindi, Urdu, Multilingual'),
])

# ------------------------------------------------------------------ generic physical product
FAM['generic'] = blk(IDENT, [
    T('spec', 'Product Type', 'نوع المنتج', required='Yes'),
    D('mat', 'Main Material', 'الخامة الأساسية',
      'Plastic, ABS, PVC, Metal, Steel, Stainless Steel, Aluminium, Iron, '
      'Brass, Copper, Wood, Bamboo, Glass, Ceramic, Rubber, Silicone, '
      'Fabric / Textile, Cotton, Polyester, Leather, Paper / Cardboard, '
      'Composite, Mixed Materials'),
    D('spec', 'Size', 'المقاس',
      'Extra Small, Small, Medium, Large, Extra Large, One Size / Universal, Custom',
      option='Yes'),
    T('dims', 'Dimensions (L x W x H cm)', 'الأبعاد (طول×عرض×ارتفاع سم)'),
    N('pack', 'Item Weight (kg)', 'وزن المنتج (كجم)', WEIGHT_KG),
    D('pack', 'Pack Quantity', 'الكمية في العبوة', PACK_QTY, option='Yes'),
    D('design', 'Style / Design', 'الستايل / التصميم',
      'Modern, Classic, Minimalist, Traditional, Industrial, Decorative, '
      'Functional, Luxury, Casual'),
    D('design', 'Pattern', 'النقشة',
      'Solid / Plain, Printed, Striped, Checked, Floral, Geometric, Textured, Multicolour'),
    D('design', 'Finish', 'التشطيب',
      'Matte, Glossy, Satin, Brushed, Polished, Powder Coated, Painted, '
      'Natural, Chrome, Anodised'),
    D('usage', 'Recommended Use', 'الاستخدام الموصى به',
      'Home Use, Office Use, Commercial Use, Industrial Use, Outdoor Use, '
      'Travel, Personal Use, Professional Use'),
    D('usage', 'Indoor / Outdoor', 'داخلي / خارجي', 'Indoor, Outdoor, Indoor & Outdoor'),
    D('usage', 'Gender', 'الجنس', 'Men, Women, Unisex, Kids, Not Applicable'),
    D('usage', 'Age Group', 'الفئة العمرية',
      'Adults, Teens, Kids, Babies, Seniors, All Ages'),
    D('power', 'Power Source', 'مصدر الطاقة',
      'Not Applicable, Manual / No Power, Battery Operated, Rechargeable, '
      'Mains Electric, USB Powered, Solar, Gas'),
    B('feat', 'Water Resistant', 'مقاوم للماء'),
    B('feat', 'Portable', 'محمول'),
    B('feat', 'Foldable', 'قابل للطي'),
    B('feat', 'Reusable', 'قابل لإعادة الاستخدام'),
    B('feat', 'Eco-Friendly', 'صديق للبيئة'),
    B('inst', 'Assembly Required', 'يتطلب تركيباً'),
    T('care', 'Care Instructions', 'تعليمات العناية'),
    D('cert', 'Certification / Compliance', 'الشهادات والمطابقة', GCC_CERT),
], COLOR, COMMERCE)
