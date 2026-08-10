# -*- coding: utf-8 -*-
"""Fashion, beauty, baby, pets, health, sports, stationery, crafts, gifts, services."""
from lib_core import *

FAM = {}

# ------------------------------------------------------------------ apparel
FAM['apparel'] = blk(IDENT, APPAREL_BASE, COLOR, [
    D('design', 'Collar Type', 'نوع الياقة',
      'Not Applicable, Classic / Point, Button-Down, Spread, Mandarin, Polo, '
      'Shawl, Notch Lapel, Peak Lapel, Stand Collar'),
    D('design', 'Hem Style', 'نوع الحاشية',
      'Straight Hem, Curved Hem, Asymmetric, Ruffled, Slit, Elastic, Raw Edge'),
    D('design', 'Embellishment', 'الزخارف',
      'None, Embroidery, Sequins, Beads, Lace Trim, Studs, Rhinestones, '
      'Applique, Fringe, Ruffles'),
    B('design', 'Sheer / Transparent', 'شفاف'),
    B('care', 'Wrinkle Resistant', 'مقاوم للتجعد'),
    B('care', 'Quick Dry', 'سريع الجفاف'),
    B('feat', 'Breathable Fabric', 'قماش قابل للتهوية'),
    T('fit', 'Model Measurements / Fit Note', 'قياسات العارض / ملاحظة المقاس'),
    D('spec', 'Collection', 'المجموعة',
      'New Arrival, Basic / Essentials, Premium, Limited Edition, Seasonal, Sale'),
], COMMERCE)

FAM['footwear'] = blk(IDENT, FOOTWEAR_BASE, COLOR, [
    D('spec', 'Shoe Type', 'نوع الحذاء',
      'Sneakers, Running Shoes, Training Shoes, Football Boots, Basketball Shoes, '
      'Hiking Boots, Work Boots, Dress Shoes, Loafers, Oxfords, Sandals, '
      'Flip Flops, Slippers, Clogs, Ankle Boots, Knee High Boots, Heels, '
      'Flats, Wedges, Espadrilles, Water Shoes', required='Yes'),
    D('design', 'Fastening Detail', 'تفاصيل الإغلاق',
      'Standard Laces, Elastic Laces, Speed Lacing, Boa Dial, Buckle Strap, '
      'Double Strap, Ankle Strap, T-Strap, None'),
    B('feat', 'Cushioned Midsole', 'نعل أوسط ممتص للصدمات'),
    B('feat', 'Steel Toe Cap', 'مقدمة حديدية واقية'),
    B('feat', 'Orthopaedic', 'طبي / تقويمي'),
    T('care', 'Care Instructions', 'تعليمات العناية'),
], COMMERCE)

# ------------------------------------------------------------------ bags
FAM['bag'] = blk(IDENT, [
    D('spec', 'Bag Type', 'نوع الحقيبة',
      'Backpack, Laptop Backpack, School Bag, Handbag, Tote Bag, Shoulder Bag, '
      'Crossbody Bag, Clutch, Satchel, Messenger Bag, Duffle Bag, Gym Bag, '
      'Travel Trolley / Suitcase, Cabin Bag, Waist / Belt Bag, Sling Bag, '
      'Wallet, Cardholder, Cosmetic Bag, Camera Bag, Diaper Bag', required='Yes'),
    D('mat', 'Main Material', 'الخامة الأساسية',
      'Genuine Leather, Faux Leather / PU, Suede, Canvas, Polyester, Nylon, '
      'Cotton, Denim, Jute, Polycarbonate (Hard Shell), ABS, Aluminium, '
      'Neoprene, Mesh, Straw / Raffia', required='Yes'),
    D('mat', 'Lining Material', 'خامة البطانة',
      'Polyester, Cotton, Satin, Nylon, Suede, Microfibre, Unlined'),
    D('spec', 'Size', 'المقاس',
      'Mini, Small, Medium, Large, Extra Large, Cabin (20-22 inch), '
      'Medium Check-In (24-26 inch), Large Check-In (28-32 inch), Set', option='Yes'),
    N('cap', 'Capacity (Litres)', 'السعة (لتر)',
      'Under 10 L, 10-20 L, 21-30 L, 31-45 L, 46-65 L, 66-90 L, Above 90 L'),
    T('dims', 'Dimensions (L x W x H cm)', 'الأبعاد (طول×عرض×ارتفاع سم)'),
    D('compat', 'Laptop Compartment Size', 'مقاس جيب اللابتوب',
      'Not Applicable, Up to 13 inch, Up to 14 inch, Up to 15.6 inch, '
      'Up to 16 inch, Up to 17 inch'),
    I('spec', 'Number of Compartments', 'عدد الجيوب الداخلية', '1, 2, 3, 4, 5, 6, 7, 8+'),
    D('design', 'Closure Type', 'نوع الإغلاق',
      'Zipper, Magnetic Snap, Drawstring, Buckle, Flap, Clasp, Open Top, '
      'Combination Lock, TSA Lock'),
    D('design', 'Strap Type', 'نوع الحزام',
      'Adjustable Shoulder Strap, Detachable Strap, Double Handle, Single Handle, '
      'Padded Backpack Straps, Chain Strap, Telescopic Handle, No Strap'),
    I('spec', 'Number of Wheels', 'عدد العجلات', 'Not Applicable, 2, 4, 8'),
    D('spec', 'Wheel Type', 'نوع العجلات',
      'Not Applicable, Spinner (360°), Inline Skate Wheels, Fixed Wheels, Silent Wheels'),
    B('feat', 'Expandable', 'قابل للتوسعة'),
    B('feat', 'Water Resistant', 'مقاوم للماء'),
    B('feat', 'RFID Blocking', 'حماية RFID'),
    B('feat', 'USB Charging Port', 'منفذ شحن USB'),
    B('feat', 'Anti-Theft Design', 'تصميم مضاد للسرقة'),
    B('feat', 'Trolley Sleeve', 'حزام تثبيت على الحقيبة'),
    B('feat', 'Laptop Padded Sleeve', 'جيب مبطن للابتوب'),
    D('design', 'Pattern', 'النقشة',
      'Solid, Printed, Monogram, Striped, Floral, Camouflage, Animal Print, '
      'Geometric, Quilted, Textured'),
    D('usage', 'Gender', 'الجنس', 'Men, Women, Unisex, Boys, Girls'),
    D('usage', 'Occasion', 'المناسبة',
      'Everyday, Work / Business, School & University, Travel, Sports & Gym, '
      'Party & Evening, Outdoor / Hiking, Beach'),
    N('pack', 'Item Weight (kg)', 'وزن المنتج (كجم)',
      'Under 0.5 kg, 0.5-1 kg, 1.1-2 kg, 2.1-3.5 kg, 3.6-5 kg, Above 5 kg'),
], COLOR, COMMERCE)

# ------------------------------------------------------------------ jewellery
FAM['jewellery'] = blk(IDENT, [
    D('spec', 'Jewellery Type', 'نوع المجوهرات',
      'Ring, Necklace, Pendant, Bracelet, Bangle, Earrings, Anklet, Brooch, '
      'Chain, Charm, Cufflinks, Jewellery Set, Nose Pin, Toe Ring', required='Yes'),
    D('mat', 'Metal Type', 'نوع المعدن',
      'Gold, White Gold, Rose Gold, Yellow Gold, Silver, Sterling Silver 925, '
      'Platinum, Stainless Steel, Titanium, Brass, Copper, Alloy, '
      'Gold Plated, Silver Plated, Rhodium Plated', required='Yes'),
    D('spec', 'Metal Purity / Karat', 'العيار / النقاء',
      'Not Applicable, 24K, 22K, 21K, 18K, 14K, 10K, 9K, 925 Sterling, 950 Platinum'),
    N('spec', 'Metal Weight (grams)', 'وزن المعدن (جرام)',
      'Under 2 g, 2-5 g, 5.1-10 g, 10.1-20 g, 20.1-50 g, Above 50 g'),
    D('spec', 'Gemstone Type', 'نوع الحجر الكريم',
      'None, Diamond, Cubic Zirconia, Moissanite, Pearl, Ruby, Sapphire, Emerald, '
      'Topaz, Amethyst, Opal, Turquoise, Onyx, Garnet, Aquamarine, Crystal'),
    N('spec', 'Total Carat Weight', 'الوزن القيراطي الإجمالي',
      'Not Applicable, Under 0.25 ct, 0.25-0.50 ct, 0.51-1.00 ct, 1.01-2.00 ct, '
      '2.01-5.00 ct, Above 5.00 ct'),
    D('spec', 'Stone Cut', 'قصّة الحجر',
      'Not Applicable, Round Brilliant, Princess, Oval, Emerald, Pear, Marquise, '
      'Cushion, Heart, Radiant, Asscher, Baguette'),
    D('spec', 'Diamond Clarity', 'نقاء الألماس',
      'Not Applicable, FL, IF, VVS1, VVS2, VS1, VS2, SI1, SI2, I1, I2'),
    D('spec', 'Diamond Colour Grade', 'درجة لون الألماس',
      'Not Applicable, D, E, F, G, H, I, J, K, L, M'),
    I('spec', 'Number of Stones', 'عدد الأحجار', '0, 1, 2, 3, 5, 7, 10, 20, 50, 100+'),
    D('spec', 'Ring Size', 'مقاس الخاتم',
      'Not Applicable, 5, 6, 7, 8, 9, 10, 11, 12, 13, Adjustable, Custom', option='Yes'),
    N('dims', 'Chain Length (cm)', 'طول السلسلة (سم)',
      'Not Applicable, 35 cm, 40 cm, 45 cm, 50 cm, 55 cm, 60 cm, 70 cm, 80 cm',
      option='Yes'),
    D('design', 'Closure / Clasp Type', 'نوع القفل',
      'Not Applicable, Lobster Clasp, Spring Ring, Toggle, Magnetic, Box Clasp, '
      'Hook, Push Back, Screw Back, Hoop / Huggie, Slide'),
    D('design', 'Style', 'الستايل',
      'Classic, Modern, Minimalist, Statement, Vintage, Bohemian, Oriental / Arabic, '
      'Bridal, Religious, Charm, Personalised'),
    D('design', 'Finish', 'التشطيب',
      'Polished / High Shine, Matte, Brushed, Hammered, Antique, Textured, Two-Tone'),
    D('usage', 'Gender', 'الجنس', 'Women, Men, Unisex, Kids'),
    D('usage', 'Occasion', 'المناسبة',
      'Everyday, Engagement, Wedding, Anniversary, Birthday, Graduation, '
      'Eid & Ramadan, Party, Gift'),
    B('cert', 'Certificate Included', 'يشمل شهادة'),
    D('cert', 'Certification Body', 'جهة الشهادة',
      'Not Applicable, GIA, IGI, HRD, AGS, Local Hallmark, Manufacturer Certificate'),
    B('feat', 'Hypoallergenic / Nickel Free', 'مضاد للحساسية / خالٍ من النيكل'),
    B('feat', 'Tarnish Resistant', 'مقاوم للبهتان'),
    B('feat', 'Engraving Available', 'إمكانية النقش'),
    B('pack', 'Gift Box Included', 'يشمل علبة هدية'),
], COMMERCE)

# ------------------------------------------------------------------ watch (traditional)
FAM['watch'] = blk(IDENT, [
    D('spec', 'Movement Type', 'نوع الحركة',
      'Quartz (Battery), Automatic (Self-Winding), Manual Mechanical, '
      'Solar Powered, Kinetic, Digital, Analog-Digital', required='Yes'),
    D('spec', 'Display Type', 'نوع العرض', 'Analog, Digital, Analog-Digital, Chronograph'),
    D('design', 'Case Diameter (mm)', 'قطر العلبة (ملم)',
      '26 mm, 28 mm, 30 mm, 32 mm, 34 mm, 36 mm, 38 mm, 40 mm, 41 mm, 42 mm, '
      '44 mm, 45 mm, 46 mm, 48 mm', option='Yes'),
    N('design', 'Case Thickness (mm)', 'سماكة العلبة (ملم)',
      'Under 7 mm, 7-9 mm, 10-12 mm, 13-15 mm, Above 15 mm'),
    D('mat', 'Case Material', 'خامة العلبة',
      'Stainless Steel, Gold Plated Steel, Solid Gold, Titanium, Ceramic, '
      'Aluminium, Brass, Resin / Plastic, Carbon Fibre, Bronze'),
    D('mat', 'Strap / Bracelet Material', 'خامة السوار',
      'Stainless Steel Bracelet, Genuine Leather, Faux Leather, Silicone / Rubber, '
      'Nylon / NATO, Fabric, Ceramic, Mesh / Milanese, Resin', option='Yes'),
    N('design', 'Strap Width (mm)', 'عرض السوار (ملم)',
      '14 mm, 16 mm, 18 mm, 20 mm, 22 mm, 24 mm, 26 mm'),
    D('mat', 'Glass / Crystal Type', 'نوع الزجاج',
      'Mineral Glass, Sapphire Crystal, Hardlex, Acrylic / Resin, Anti-Reflective Sapphire'),
    D('design', 'Dial Colour', 'لون الميناء',
      'Black, White, Silver, Blue, Green, Brown, Grey, Gold, Champagne, '
      'Mother of Pearl, Red, Skeleton', option='Yes'),
    D('design', 'Dial Shape', 'شكل الميناء',
      'Round, Square, Rectangular, Oval, Tonneau, Cushion'),
    D('design', 'Index / Marker Type', 'نوع المؤشرات',
      'Arabic Numerals, Roman Numerals, Stick / Baton Markers, Dot Markers, '
      'Diamond Markers, No Markers, Mixed'),
    D('safety', 'Water Resistance', 'مقاومة الماء',
      'Not Water Resistant, 3 ATM (30 m), 5 ATM (50 m), 10 ATM (100 m), '
      '20 ATM (200 m), 30 ATM (300 m), Diver 200 m+'),
    D('feat', 'Complications / Functions', 'الوظائف الإضافية',
      'Date Display, Day-Date, Chronograph / Stopwatch, Moon Phase, GMT / Dual Time, '
      'Alarm, Tachymeter, Power Reserve Indicator, World Time, Backlight, None'),
    B('feat', 'Luminous Hands / Markers', 'عقارب مضيئة'),
    B('feat', 'Screw-Down Crown', 'تاج لولبي'),
    B('feat', 'Rotating Bezel', 'إطار دوّار'),
    B('feat', 'Skeleton / Exhibition Case Back', 'ظهر شفاف'),
    N('batt', 'Power Reserve (hours)', 'احتياطي الطاقة (ساعة)',
      'Not Applicable, 38 Hours, 40 Hours, 42 Hours, 48 Hours, 70 Hours, 80 Hours, 120 Hours'),
    D('batt', 'Battery Type', 'نوع البطارية',
      'Not Applicable, SR626SW, SR920SW, CR2016, CR2025, CR2032, Rechargeable'),
    D('usage', 'Gender', 'الجنس', 'Men, Women, Unisex, Kids'),
    D('usage', 'Style', 'الستايل',
      'Classic / Dress, Sport, Diver, Pilot / Aviator, Military, Casual, '
      'Luxury, Fashion, Digital Casual'),
    B('pack', 'Gift Box Included', 'يشمل علبة هدية'),
], COMMERCE)

# ------------------------------------------------------------------ eyewear
FAM['eyewear'] = blk(IDENT, [
    D('spec', 'Eyewear Type', 'نوع النظارة',
      'Sunglasses, Optical / Prescription Frames, Reading Glasses, '
      'Blue Light Blocking Glasses, Sports Glasses, Swimming Goggles, '
      'Safety Glasses, Ski Goggles, Contact Lenses', required='Yes'),
    D('design', 'Frame Shape', 'شكل الإطار',
      'Aviator, Wayfarer, Round, Square, Rectangular, Cat Eye, Oval, Butterfly, '
      'Shield, Wrap Around, Clubmaster, Geometric, Rimless, Sport'),
    D('mat', 'Frame Material', 'خامة الإطار',
      'Acetate, Plastic / TR90, Metal, Stainless Steel, Titanium, Aluminium, '
      'Memory Metal, Wood, Carbon Fibre, Mixed'),
    D('spec', 'Lens Material', 'خامة العدسة',
      'Polycarbonate, CR-39 Plastic, Glass, Nylon, Trivex, High Index'),
    D('spec', 'Lens Colour / Tint', 'لون العدسة',
      'Clear, Black / Smoke, Brown / Tortoise, Green, Blue, Grey, Pink, Yellow, '
      'Mirrored Silver, Mirrored Blue, Mirrored Gold, Gradient, Photochromic',
      option='Yes'),
    B('spec', 'Polarised', 'مستقطبة'),
    D('safety', 'UV Protection', 'الحماية من الأشعة',
      'UV400 (100% UVA/UVB), UV380, Category 0, Category 1, Category 2, '
      'Category 3, Category 4, Not Specified'),
    B('feat', 'Anti-Reflective Coating', 'طلاء مضاد للانعكاس'),
    B('feat', 'Scratch Resistant Coating', 'طلاء مقاوم للخدش'),
    B('feat', 'Blue Light Filter', 'مرشّح الضوء الأزرق'),
    B('feat', 'Photochromic / Transition', 'عدسات متغيرة اللون'),
    B('feat', 'Anti-Fog', 'مضاد للضباب'),
    B('spec', 'Prescription Ready (Rx-able)', 'قابلة للعدسات الطبية'),
    N('dims', 'Lens Width (mm)', 'عرض العدسة (ملم)',
      '45 mm, 48 mm, 50 mm, 52 mm, 54 mm, 55 mm, 56 mm, 58 mm, 60 mm, 62 mm'),
    N('dims', 'Bridge Width (mm)', 'عرض الجسر (ملم)',
      '14 mm, 15 mm, 16 mm, 17 mm, 18 mm, 19 mm, 20 mm, 21 mm, 22 mm'),
    N('dims', 'Temple Length (mm)', 'طول الذراع (ملم)',
      '125 mm, 130 mm, 135 mm, 140 mm, 145 mm, 150 mm'),
    D('spec', 'Frame Size', 'مقاس الإطار', 'Small, Medium, Large, Extra Large, One Size'),
    D('usage', 'Gender', 'الجنس', 'Men, Women, Unisex, Kids'),
    D('design', 'Frame Colour', 'لون الإطار',
      'Black, Tortoise, Brown, Gold, Silver, Gunmetal, Rose Gold, Blue, '
      'Transparent, Red, Green, Pink, White, Multicolor', option='Yes'),
    B('pack', 'Case Included', 'يشمل جراب'),
    B('pack', 'Cleaning Cloth Included', 'يشمل قطعة تنظيف'),
    D('spec', 'Power / Diopter', 'القوة (ديوبتر)',
      'Not Applicable, +1.00, +1.50, +2.00, +2.50, +3.00, +3.50, +4.00, '
      '-1.00, -2.00, -3.00, -4.00, -5.00, -6.00', option='Yes'),
], COMMERCE)

# ------------------------------------------------------------------ makeup
FAM['makeup'] = blk(IDENT, [
    D('spec', 'Product Type', 'نوع المنتج',
      'Foundation, Concealer, Primer, Powder, Blush, Bronzer, Highlighter, '
      'Contour, Setting Spray, BB / CC Cream, Eyeshadow, Eyeliner, Mascara, '
      'Eyebrow Pencil, Eyebrow Gel, False Lashes, Lipstick, Liquid Lipstick, '
      'Lip Gloss, Lip Liner, Lip Balm, Nail Polish, Nail Care, Makeup Brush, '
      'Beauty Sponge, Makeup Remover, Makeup Set', required='Yes'),
    D('spec', 'Finish', 'اللمسة النهائية',
      'Matte, Satin, Dewy, Natural, Radiant, Shimmer, Metallic, Glitter, '
      'Glossy, Velvet, Sheer'),
    D('spec', 'Coverage', 'درجة التغطية',
      'Not Applicable, Sheer, Light, Medium, Medium to Full, Full, Buildable'),
    T('spec', 'Shade Name', 'اسم الدرجة'),
    D('spec', 'Shade Family', 'عائلة الدرجة',
      'Fair, Light, Light Medium, Medium, Medium Tan, Tan, Deep, Rich, '
      'Nude, Pink, Red, Berry, Coral, Brown, Plum, Orange, Neutral, '
      'Cool Tone, Warm Tone, Multicolour', option='Yes'),
    D('spec', 'Undertone', 'الدرجة الأساسية',
      'Not Applicable, Cool, Warm, Neutral, Olive, Golden, Pink'),
    D('spec', 'Form', 'الشكل',
      'Liquid, Cream, Powder, Pressed Powder, Loose Powder, Stick, Pencil, '
      'Gel, Balm, Mousse, Palette, Compact'),
    N('spec', 'Volume / Size (ml)', 'الحجم (مل)',
      '2 ml, 3 ml, 5 ml, 8 ml, 10 ml, 15 ml, 30 ml, 50 ml, 100 ml', option='Yes'),
    N('spec', 'Net Weight (g)', 'الوزن الصافي (جم)',
      '1 g, 2 g, 3 g, 5 g, 8 g, 10 g, 12 g, 15 g, 20 g, 30 g, 50 g'),
    D('health', 'Skin Type', 'نوع البشرة',
      'Normal, Dry, Oily, Combination, Sensitive, Acne-Prone, Mature, All Skin Types'),
    D('spec', 'SPF Protection', 'الحماية من الشمس',
      'No SPF, SPF 15, SPF 20, SPF 25, SPF 30, SPF 50, SPF 50+'),
    B('feat', 'Long Lasting / Transfer Proof', 'ثبات طويل / لا ينتقل'),
    B('feat', 'Waterproof', 'مقاوم للماء'),
    B('feat', 'Smudge Proof', 'مقاوم للتلطخ'),
    B('feat', 'Non-Comedogenic', 'لا يسد المسام'),
    B('feat', 'Fragrance Free', 'خالٍ من العطور'),
    B('feat', 'Hypoallergenic', 'مضاد للحساسية'),
    B('ingr', 'Vegan', 'نباتي (فيغن)'),
    B('ingr', 'Cruelty-Free', 'غير مُختبر على الحيوانات'),
    B('ingr', 'Paraben Free', 'خالٍ من البارابين'),
    B('cert', 'Halal Certified', 'حاصل على شهادة حلال'),
    T('ingr', 'Key Ingredients', 'المكونات الرئيسية'),
    D('spec', 'Applicator Type', 'نوع الأداة',
      'Not Applicable, Doe Foot Wand, Brush Applicator, Sponge Tip, Pump, '
      'Twist-Up Stick, Dropper, Spray, Built-In Mirror'),
    D('spec', 'Packaging Type', 'نوع العبوة',
      'Tube, Bottle, Compact, Palette, Stick, Jar, Pencil, Pot, Spray, Kit / Set'),
    D('spec', 'Period After Opening (PAO)', 'مدة الاستخدام بعد الفتح',
      '3M, 6M, 9M, 12M, 18M, 24M, 36M, Not Specified'),
    D('usage', 'Application Area', 'منطقة الاستخدام',
      'Face, Eyes, Lips, Cheeks, Brows, Nails, Body, Multi-Use'),
    D('usage', 'Gender / Target User', 'الفئة المستهدفة', 'Women, Men, Unisex, Teens'),
    D('origin', 'Country of Origin', 'بلد المنشأ', ORIGIN),
    D('pack', 'Pack Size', 'حجم العبوة', PACK_QTY, option='Yes'),
])

# ------------------------------------------------------------------ perfume
FAM['perfume'] = blk(IDENT, [
    D('spec', 'Fragrance Type', 'نوع العطر',
      'Eau de Parfum (EDP), Eau de Toilette (EDT), Eau de Cologne (EDC), '
      'Parfum / Extrait, Eau Fraiche, Body Mist, Perfume Oil / Attar, '
      'Solid Perfume, Hair Mist, Deodorant Spray, Bakhoor, Oud, Incense',
      required='Yes'),
    N('spec', 'Volume (ml)', 'الحجم (مل)',
      '5 ml, 10 ml, 15 ml, 20 ml, 30 ml, 50 ml, 60 ml, 75 ml, 90 ml, 100 ml, '
      '125 ml, 150 ml, 200 ml, 250 ml', required='Yes', option='Yes'),
    D('scent', 'Fragrance Family', 'عائلة العطر',
      'Floral, Oriental / Amber, Woody, Fresh, Citrus, Aquatic, Fougere, '
      'Chypre, Gourmand, Spicy, Musky, Leather, Green, Fruity', required='Yes'),
    T('scent', 'Top Notes', 'النفحات العليا'),
    T('scent', 'Middle / Heart Notes', 'النفحات الوسطى'),
    T('scent', 'Base Notes', 'النفحات القاعدية'),
    D('scent', 'Key Accords', 'المكونات البارزة',
      'Oud, Rose, Amber, Musk, Vanilla, Sandalwood, Saffron, Jasmine, Bergamot, '
      'Lavender, Patchouli, Cedar, Vetiver, Tobacco, Leather, Citrus, '
      'Coconut, Praline, Iris, Oakmoss'),
    D('spec', 'Concentration', 'تركيز العطر',
      'Parfum (20-30%), Eau de Parfum (15-20%), Eau de Toilette (5-15%), '
      'Eau de Cologne (2-4%), Eau Fraiche (1-3%), Pure Oil (100%)'),
    D('spec', 'Longevity', 'مدة الثبات',
      'Up to 2 Hours, 2-4 Hours, 4-6 Hours, 6-8 Hours, 8-12 Hours, Above 12 Hours'),
    D('spec', 'Sillage / Projection', 'انتشار العطر',
      'Intimate / Skin Scent, Moderate, Strong, Enormous'),
    D('usage', 'Gender', 'الجنس', 'Men, Women, Unisex, Kids', required='Yes'),
    D('usage', 'Season', 'الموسم', 'Summer, Winter, Spring, Autumn, All Season'),
    D('usage', 'Occasion', 'المناسبة',
      'Daily Wear, Office / Work, Evening, Special Occasion, Wedding, '
      'Sports, Ramadan & Eid, Gift'),
    D('spec', 'Application Type', 'طريقة الاستخدام',
      'Spray / Atomiser, Roll-On, Splash, Dab-On, Stick, Burner / Incense'),
    D('spec', 'Packaging Type', 'نوع العبوة',
      'Glass Bottle, Crystal Bottle, Plastic Bottle, Metal Bottle, Travel Spray, '
      'Refill, Gift Set, Tin Box'),
    B('pack', 'Gift Set', 'طقم هدية'),
    B('pack', 'Tester / Unboxed', 'تستر / بدون علبة'),
    B('feat', 'Alcohol Free', 'خالٍ من الكحول'),
    B('feat', 'Refillable Bottle', 'زجاجة قابلة لإعادة التعبئة'),
    D('main', 'Launch Year', 'سنة الإطلاق',
      'Before 2000, 2000-2009, 2010-2015, 2016-2020, 2021, 2022, 2023, 2024, 2025, 2026'),
    D('origin', 'Country of Origin', 'بلد المنشأ', ORIGIN),
    D('general', 'Condition', 'الحالة', COND),
], COMMERCE)

# ------------------------------------------------------------------ personal care (skin/hair/oral/body)
FAM['personal_care'] = blk(IDENT, BEAUTY_BASE, [
    D('spec', 'SPF Protection', 'الحماية من الشمس',
      'No SPF, SPF 15, SPF 20, SPF 30, SPF 50, SPF 50+, SPF 100'),
    B('feat', 'Dermatologically Tested', 'مختبر جلدياً'),
    B('feat', 'Non-Comedogenic', 'لا يسد المسام'),
    B('feat', 'Hypoallergenic', 'مضاد للحساسية'),
    B('feat', 'Suitable for Sensitive Skin', 'مناسب للبشرة الحساسة'),
    B('feat', 'Waterproof / Water Resistant', 'مقاوم للماء'),
    D('spec', 'Hair Type', 'نوع الشعر',
      'Not Applicable, All Hair Types, Dry Hair, Oily Hair, Normal Hair, '
      'Curly Hair, Straight Hair, Coloured Hair, Damaged Hair, Fine Hair, '
      'Thick Hair, Frizzy Hair, Dandruff-Prone'),
    D('spec', 'Benefit', 'الفائدة',
      'Moisturising, Cleansing, Exfoliating, Anti-Ageing, Whitening / Brightening, '
      'Anti-Acne, Soothing, Nourishing, Strengthening, Volumising, Smoothing, '
      'Anti-Dandruff, Colour Protection, Sun Protection, Odour Protection, Whitening (Teeth)'),
    D('cert', 'Certification / Compliance', 'الشهادات والمطابقة', GCC_CERT),
    D('origin', 'Country of Origin', 'بلد المنشأ', ORIGIN),
    D('general', 'Condition', 'الحالة', COND),
    D('warr', 'Warranty Period', 'مدة الضمان', WARR_PERIOD),
])

# ------------------------------------------------------------------ baby product
FAM['baby'] = blk(IDENT, [
    D('spec', 'Product Type', 'نوع المنتج',
      'Diapers, Baby Wipes, Baby Bottle, Sterilizer, Breast Pump, Pacifier, '
      'High Chair, Car Seat, Stroller, Baby Carrier, Cot / Crib, Baby Monitor, '
      'Playmat, Baby Bath, Changing Mat, Baby Walker, Bouncer, Safety Gate, '
      'Baby Food Maker, Feeding Set', required='Yes'),
    D('usage', 'Age Range', 'الفئة العمرية',
      '0-3 Months, 3-6 Months, 6-12 Months, 1-2 Years, 2-3 Years, 3-5 Years, '
      '5+ Years, Newborn, All Ages', required='Yes', option='Yes'),
    D('spec', 'Size', 'المقاس',
      'Not Applicable, Newborn (NB), Size 1, Size 2, Size 3, Size 4, Size 5, '
      'Size 6, Size 7, Small, Medium, Large, One Size', option='Yes'),
    N('spec', 'Suitable Weight Range (kg)', 'نطاق الوزن المناسب (كجم)',
      'Up to 4 kg, 3-6 kg, 4-8 kg, 6-11 kg, 9-14 kg, 11-18 kg, 15-25 kg, '
      '15-36 kg, Above 25 kg'),
    D('pack', 'Count per Pack', 'العدد في العبوة',
      '1 Piece, 2 Pieces, 20 Pieces, 30 Pieces, 40 Pieces, 50 Pieces, '
      '60 Pieces, 72 Pieces, 80 Pieces, 100 Pieces, 120 Pieces, 200 Pieces', option='Yes'),
    D('mat', 'Material', 'الخامة',
      'BPA-Free Plastic, Polypropylene (PP), PPSU, Silicone, Glass, Stainless Steel, '
      'Cotton, Organic Cotton, Bamboo Fibre, Foam, Aluminium, Wood, Fabric'),
    B('safety', 'BPA Free', 'خالٍ من البيسفينول A'),
    B('safety', 'Phthalate Free', 'خالٍ من الفثالات'),
    B('safety', 'Lead Free', 'خالٍ من الرصاص'),
    B('safety', 'Hypoallergenic', 'مضاد للحساسية'),
    B('safety', 'Dermatologically Tested', 'مختبر جلدياً'),
    D('cert', 'Safety Certification', 'شهادة السلامة',
      'EN 71, ASTM F963, ECE R44/04, UN R129 (i-Size), EN 1888, CE, '
      'GCC Conformity, ISO 8124, None'),
    D('spec', 'Car Seat Group', 'فئة كرسي السيارة',
      'Not Applicable, Group 0 (0-10 kg), Group 0+ (0-13 kg), Group 1 (9-18 kg), '
      'Group 2 (15-25 kg), Group 3 (22-36 kg), Group 0+/1, Group 1/2/3, i-Size'),
    D('spec', 'Installation Method', 'طريقة التركيب',
      'Not Applicable, Seat Belt, ISOFIX, ISOFIX + Top Tether, ISOFIX + Support Leg'),
    B('feat', 'Foldable', 'قابل للطي'),
    B('feat', 'Adjustable Height', 'ارتفاع قابل للتعديل'),
    B('feat', 'Reclining', 'قابل للاستلقاء'),
    B('feat', 'Machine Washable', 'قابل للغسل في الغسالة'),
    B('feat', 'Wheels Included', 'يشمل عجلات'),
    B('feat', 'Safety Harness', 'حزام أمان'),
    I('feat', 'Harness Point', 'نقاط حزام الأمان', 'Not Applicable, 3-Point, 5-Point'),
    B('feat', 'Anti-Colic', 'مضاد للمغص'),
    D('spec', 'Flow Rate (Teats)', 'معدل التدفق (الحلمات)',
      'Not Applicable, Slow Flow, Medium Flow, Fast Flow, Variable Flow, Newborn Flow'),
    B('feat', 'Absorbency - Overnight', 'امتصاص ليلي طويل'),
    B('feat', 'Wetness Indicator', 'مؤشر البلل'),
    B('feat', 'Fragrance Free', 'خالٍ من العطور'),
    B('feat', 'Alcohol Free', 'خالٍ من الكحول'),
    D('usage', 'Gender', 'الجنس', 'Unisex, Boys, Girls'),
    T('care', 'Care Instructions', 'تعليمات العناية'),
], COLOR, COMMERCE)

# ------------------------------------------------------------------ toys
FAM['toy'] = blk(IDENT, [
    D('spec', 'Toy Type', 'نوع اللعبة',
      'Building Blocks, Puzzle, Board Game, Card Game, Action Figure, Doll, '
      'Plush / Soft Toy, Ride-On, Tricycle, Scooter, Bicycle, Remote Control Toy, '
      'Educational Toy, STEM Kit, Musical Toy, Art & Craft Kit, Outdoor Play, '
      'Water Toy, Swing, Slide, Play Tent, Trampoline, Bath Toy, Role Play Set',
      required='Yes'),
    D('usage', 'Age Range', 'الفئة العمرية',
      '0-6 Months, 6-12 Months, 1-2 Years, 2-3 Years, 3-5 Years, 5-7 Years, '
      '8-11 Years, 12-14 Years, 14+ Years, All Ages', required='Yes', option='Yes'),
    D('mat', 'Material', 'الخامة',
      'ABS Plastic, PP Plastic, Wood, Plush Fabric, Cotton, Foam, Rubber, '
      'Silicone, Metal, Cardboard, EVA, Mixed Materials'),
    I('spec', 'Number of Pieces', 'عدد القطع',
      '1, 2-10, 11-50, 51-100, 101-250, 251-500, 501-1000, Above 1000'),
    D('power', 'Power Source', 'مصدر الطاقة',
      'No Power Required, AA Batteries, AAA Batteries, Rechargeable Battery, '
      'USB Charging, Mains Adapter, Solar, Manual / Wind-Up'),
    I('power', 'Number of Batteries Required', 'عدد البطاريات المطلوبة', '0, 1, 2, 3, 4, 6, 8'),
    B('pack', 'Batteries Included', 'يشمل بطاريات'),
    D('spec', 'Skill Development', 'المهارات المستهدفة',
      'Motor Skills, Cognitive Development, Creativity, Problem Solving, '
      'Language & Communication, Social Skills, Hand-Eye Coordination, '
      'STEM / Logic, Sensory Development, Imagination'),
    D('cert', 'Safety Certification', 'شهادة السلامة',
      'EN 71, ASTM F963, CE, CPSIA, ISO 8124, GCC Conformity, None'),
    B('safety', 'Non-Toxic Materials', 'خامات غير سامة'),
    B('safety', 'Small Parts Warning', 'تحذير من القطع الصغيرة'),
    B('safety', 'BPA Free', 'خالٍ من البيسفينول A'),
    B('feat', 'Assembly Required', 'يتطلب تركيباً'),
    B('feat', 'Remote Controlled', 'يعمل بجهاز تحكم'),
    B('feat', 'Lights & Sounds', 'أضواء وأصوات'),
    B('feat', 'Foldable', 'قابل للطي'),
    B('feat', 'Indoor / Outdoor Use', 'للاستخدام الداخلي والخارجي'),
    N('spec', 'Maximum Load (kg)', 'أقصى حمولة (كجم)',
      'Not Applicable, Up to 20 kg, 21-35 kg, 36-50 kg, 51-80 kg, Above 80 kg'),
    D('spec', 'Language', 'اللغة',
      'Not Applicable, Arabic, English, Arabic & English, French, Multilingual'),
    D('usage', 'Gender', 'الجنس', 'Unisex, Boys, Girls'),
    I('spec', 'Number of Players', 'عدد اللاعبين',
      'Not Applicable, 1, 2, 2-4, 2-6, 3-8, 4+'),
    T('dims', 'Assembled Dimensions (cm)', 'الأبعاد بعد التركيب (سم)'),
], COLOR, COMMERCE)

# ------------------------------------------------------------------ pet supplies
FAM['pet'] = blk(IDENT, [
    D('animal', 'Pet Type', 'نوع الحيوان',
      'Dog, Cat, Bird, Fish, Hamster, Rabbit, Turtle, Parrot, Pigeon, Horse, '
      'Camel, Sheep & Goat, Cow, Chicken, Small Pets, All Pets', required='Yes'),
    D('spec', 'Product Type', 'نوع المنتج',
      'Dry Food, Wet / Canned Food, Treats & Snacks, Supplements, Litter, '
      'Bed / House, Cage, Aquarium, Carrier, Collar & Leash, Toy, Grooming Tool, '
      'Feeding Bowl, Water Dispenser, Health Care, Clothing', required='Yes'),
    D('animal', 'Life Stage', 'المرحلة العمرية',
      'Puppy / Kitten, Junior, Adult, Senior, All Life Stages'),
    D('animal', 'Pet Size / Breed Size', 'حجم الحيوان',
      'Extra Small, Small Breed, Medium Breed, Large Breed, Giant Breed, All Sizes'),
    N('spec', 'Net Weight (kg)', 'الوزن الصافي (كجم)',
      '0.1 kg, 0.4 kg, 1 kg, 1.5 kg, 2 kg, 3 kg, 5 kg, 7 kg, 10 kg, 15 kg, 20 kg',
      option='Yes'),
    D('spec', 'Flavour / Protein Source', 'النكهة / مصدر البروتين',
      'Not Applicable, Chicken, Beef, Lamb, Salmon, Tuna, Fish, Turkey, Duck, '
      'Rabbit, Vegetable, Mixed'),
    D('nutr', 'Special Diet', 'نظام غذائي خاص',
      'None, Grain Free, Hypoallergenic, Weight Control, Indoor Formula, '
      'Sensitive Stomach, Hairball Control, Urinary Care, Dental Care, '
      'Joint Support, High Protein'),
    I('nutr', 'Protein Content (%)', 'نسبة البروتين',
      'Not Applicable, Under 20%, 20-25%, 26-30%, 31-40%, Above 40%'),
    T('ingr', 'Ingredients', 'المكونات'),
    D('mat', 'Material', 'الخامة',
      'Not Applicable, Plastic, Stainless Steel, Ceramic, Wood, Metal Wire, '
      'Fabric, Nylon, Leather, Rubber, Glass, Acrylic'),
    D('spec', 'Size', 'المقاس',
      'Not Applicable, XS, S, M, L, XL, XXL, One Size', option='Yes'),
    T('dims', 'Dimensions (L x W x H cm)', 'الأبعاد (طول×عرض×ارتفاع سم)'),
    B('feat', 'Machine Washable', 'قابل للغسل في الغسالة'),
    B('feat', 'Foldable / Portable', 'قابل للطي / محمول'),
    B('feat', 'Non-Slip Base', 'قاعدة مانعة للانزلاق'),
    B('feat', 'Automatic / Electric', 'أوتوماتيكي / كهربائي'),
    B('feat', 'Adjustable', 'قابل للتعديل'),
    B('cert', 'Veterinarian Approved', 'معتمد من الطبيب البيطري'),
    N('spec', 'Shelf Life (months)', 'مدة الصلاحية (شهر)',
      'Not Applicable, 6 Months, 12 Months, 18 Months, 24 Months, 36 Months', dtype='Integer'),
    D('spec', 'Storage Condition', 'ظروف التخزين',
      'Not Applicable, Cool & Dry Place, Refrigerate After Opening, Room Temperature'),
    D('origin', 'Country of Origin', 'بلد المنشأ', ORIGIN),
], COLOR, COMMERCE)

# ------------------------------------------------------------------ live animal
FAM['livestock'] = blk([
    D('animal', 'Animal Type', 'نوع الحيوان',
      'Camel, Horse, Cow, Sheep, Goat, Chicken, Pigeon, Parrot, Bird, Rabbit, '
      'Dog, Cat, Fish, Turtle, Hamster, Deer, Donkey', required='Yes'),
    T('animal', 'Breed', 'السلالة'),
    D('animal', 'Sex', 'الجنس', 'Male, Female, Mixed / Group', required='Yes'),
    D('animal', 'Age', 'العمر',
      'Under 3 Months, 3-6 Months, 6-12 Months, 1-2 Years, 2-4 Years, '
      '4-7 Years, Above 7 Years'),
    N('animal', 'Weight (kg)', 'الوزن (كجم)',
      'Under 5 kg, 5-20 kg, 21-50 kg, 51-100 kg, 101-300 kg, 301-600 kg, Above 600 kg'),
    D('animal', 'Colour / Markings', 'اللون والعلامات',
      'White, Black, Brown, Grey, Golden, Cream, Spotted, Striped, Mixed, Other'),
    D('animal', 'Health Status', 'الحالة الصحية',
      'Healthy, Vaccinated, Under Treatment, Requires Check-Up'),
    B('animal', 'Vaccinated', 'مُطعّم'),
    B('animal', 'Dewormed', 'خالٍ من الديدان'),
    B('animal', 'Health Certificate Available', 'تتوفر شهادة صحية'),
    B('animal', 'Pedigree / Registration Papers', 'أوراق نسب مسجلة'),
    B('animal', 'Microchipped', 'مزروع بشريحة'),
    D('animal', 'Purpose', 'الغرض',
      'Breeding, Dairy / Milk Production, Meat, Racing, Show / Competition, '
      'Companionship / Pet, Work, Egg Production'),
    D('animal', 'Training Level', 'مستوى التدريب',
      'Not Trained, Basic Training, Fully Trained, Racing Trained, Show Trained'),
    B('animal', 'Pregnant / In Milk', 'حامل / حلوب'),
    I('animal', 'Quantity Available', 'الكمية المتوفرة', '1, 2, 3, 5, 10, 20, 50, 100+'),
    D('animal', 'Temperament', 'الطباع', 'Calm, Friendly, Active, Aggressive, Shy, Trained'),
    T('animal', 'Feeding Requirements', 'متطلبات التغذية'),
    D('origin', 'Country of Origin', 'بلد المنشأ', ORIGIN),
    D('spec', 'Delivery / Transport', 'التوصيل والنقل',
      'Buyer Collects, Seller Delivers, Specialised Transport Required, Negotiable'),
])
