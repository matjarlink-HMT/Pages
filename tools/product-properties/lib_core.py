# -*- coding: utf-8 -*-
"""Core helpers + shared property blocks for MatjarLink expanded product properties."""

# ---------------------------------------------------------------- groups
G = {
    'main':    'Main  |  الرئيسية',
    'general': 'General  |  عام',
    'spec':    'Specifications  |  المواصفات',
    'design':  'Design  |  التصميم',
    'dims':    'Dimensions  |  الأبعاد',
    'mat':     'Material  |  الخامة',
    'perf':    'Performance  |  الأداء',
    'mem':     'Memory  |  الذاكرة والتخزين',
    'storage': 'Storage  |  التخزين',
    'display': 'Display  |  الشاشة',
    'cam':     'Camera  |  الكاميرا',
    'batt':    'Battery  |  البطارية',
    'conn':    'Connectivity  |  الاتصال',
    'audio':   'Audio  |  الصوت',
    'sensors': 'Sensors  |  المستشعرات',
    'feat':    'Features  |  الميزات',
    'smart':   'Smart Features  |  الميزات الذكية',
    'compat':  'Compatibility  |  التوافق',
    'power':   'Power  |  الطاقة',
    'elec':    'Electrical  |  الكهرباء',
    'health':  'Health  |  الصحة',
    'scent':   'Scent  |  الرائحة',
    'ingr':    'Ingredients  |  المكونات',
    'safety':  'Safety  |  السلامة',
    'care':    'Care  |  العناية والغسيل',
    'fit':     'Fit & Size  |  المقاس والقصة',
    'nutr':    'Nutrition  |  القيمة الغذائية',
    'usage':   'Usage  |  الاستخدام',
    'origin':  'Origin  |  المنشأ',
    'cert':    'Certification  |  الشهادات والمطابقة',
    'warr':    'Warranty  |  الضمان',
    'pack':    'Packaging  |  التغليف والتعبئة',
    'fitment': 'Vehicle Fitment  |  التوافق مع المركبة',
    'engine':  'Engine  |  المحرك',
    'cap':     'Capacity  |  السعة',
    'env':     'Environment  |  البيئة والكفاءة',
    'course':  'Course Info  |  معلومات الدورة',
    'service': 'Service Info  |  معلومات الخدمة',
    'inst':    'Installation  |  التركيب',
    'animal':  'Animal Info  |  معلومات الحيوان',
    'dosage':  'Dosage  |  الجرعة والتناول',
}

# ---------------------------------------------------------------- builders
# property tuple = (group, en, ar, pp_type, pp_list, po_data, po_list, required, option)


def D(group, en, ar, options, required='No', option='No'):
    """Dropdown / list property."""
    return (G[group], en, ar, 'Dropdown', options, 'List', options, required, option)


def B(group, en, ar, required='No', option='No'):
    """Boolean property."""
    return (G[group], en, ar, 'Boolean', 'Yes, No', 'List', 'Yes, No', required, option)


def N(group, en, ar, buckets, dtype='Decimal', required='No', option='No'):
    """Numeric property -- free numeric in Product Properties, bucketed list in Options."""
    return (G[group], en, ar, dtype, None, 'List', buckets, required, option)


def I(group, en, ar, buckets, required='No', option='No'):
    return N(group, en, ar, buckets, dtype='Integer', required=required, option=option)


def T(group, en, ar, required='No'):
    """Free text property."""
    return (G[group], en, ar, 'Text', None, 'Free', None, required, 'No')


def blk(*parts):
    """Flatten and de-duplicate property blocks, keeping first occurrence."""
    out, seen = [], set()
    for part in parts:
        for p in part:
            k = p[1].strip().lower()
            if k in seen:
                continue
            seen.add(k)
            out.append(p)
    return out


# ---------------------------------------------------------------- shared value lists
COLORS = ('Black, White, Grey, Silver, Gold, Rose Gold, Beige, Brown, Navy, Blue, '
          'Sky Blue, Turquoise, Green, Olive, Yellow, Orange, Red, Maroon, Pink, '
          'Purple, Multicolor, Transparent')
COND = 'New, Open Box, Refurbished, Pre-Owned - Excellent, Pre-Owned - Good, Pre-Owned - Fair'
WARR_TYPE = ('Manufacturer Warranty, Local Agent Warranty, Seller Warranty, '
             'International Warranty, No Warranty')
WARR_PERIOD = ('No Warranty, 3 Months, 6 Months, 1 Year, 2 Years, 3 Years, 5 Years, '
               '10 Years, Lifetime')
ORIGIN = ('Oman, Saudi Arabia, UAE, Qatar, Kuwait, Bahrain, Egypt, Jordan, Turkey, '
          'China, India, Japan, South Korea, Taiwan, Vietnam, Thailand, Malaysia, '
          'Germany, Italy, France, Spain, United Kingdom, USA, Canada, Brazil, Other')
WEIGHT_KG = ('Under 0.5 kg, 0.5 - 1 kg, 1 - 3 kg, 3 - 5 kg, 5 - 10 kg, 10 - 25 kg, '
             '25 - 50 kg, Above 50 kg')
IP_RATING = ('None, IPX2, IPX4, IPX5, IPX7, IPX8, IP53, IP54, IP55, IP65, IP66, IP67, IP68, IP69K')
ENERGY = ('A+++, A++, A+, A, B, C, D, E, F, G, Not Rated')
GCC_CERT = ('GCC Conformity Tracking (GCTS), G-Mark, SASO / SABER, ESMA (UAE), '
            'CE, RoHS, FCC, ISO 9001, Halal Certified, SFDA Registered, None')
PACK_QTY = '1 Piece, 2 Pieces, 3 Pieces, 4 Pieces, 5 Pieces, 6 Pieces, 10 Pieces, 12 Pieces, 24 Pieces, Bulk Pack'

# ---------------------------------------------------------------- shared blocks
IDENT = [
    D('main', 'Brand', 'العلامة التجارية', 'Refer to Brands sheet', required='Yes'),
    T('main', 'Model Name', 'اسم الموديل'),
    T('main', 'Model Number', 'رقم الموديل'),
    T('main', 'Manufacturer Part Number (MPN)', 'رقم القطعة لدى الشركة المصنّعة'),
]

COMMERCE = [
    D('general', 'Condition', 'الحالة', COND, required='Yes'),
    D('origin', 'Country of Origin', 'بلد المنشأ', ORIGIN),
    D('warr', 'Warranty Type', 'نوع الضمان', WARR_TYPE),
    D('warr', 'Warranty Period', 'مدة الضمان', WARR_PERIOD),
    T('pack', 'Package Contents', 'محتويات العبوة'),
    N('pack', 'Item Weight (kg)', 'وزن المنتج (كجم)', WEIGHT_KG),
    T('dims', 'Product Dimensions (L x W x H cm)', 'أبعاد المنتج (طول×عرض×ارتفاع سم)'),
]

COLOR = [D('general', 'Color', 'اللون', COLORS, option='Yes')]

CERT = [D('cert', 'Certification / Compliance', 'الشهادات والمطابقة', GCC_CERT)]

# Electronics-flavoured commerce block
ELEC_COMMERCE = blk(COMMERCE, [
    D('cert', 'Certification / Compliance', 'الشهادات والمطابقة', GCC_CERT),
    B('general', 'Bundle Offer', 'عرض مجمّع'),
])

# Beauty / personal-care shared block
BEAUTY_BASE = [
    D('spec', 'Formulation', 'التركيبة',
      'Cream, Lotion, Gel, Serum, Oil, Foam, Balm, Liquid, Spray, Powder, Stick, '
      'Bar, Mousse, Mask, Wipes, Capsule'),
    N('spec', 'Volume / Size (ml)', 'الحجم / السعة (مل)',
      '15 ml, 30 ml, 50 ml, 75 ml, 100 ml, 150 ml, 200 ml, 250 ml, 300 ml, 400 ml, '
      '500 ml, 750 ml, 1 L'),
    N('spec', 'Net Weight (g)', 'الوزن الصافي (جم)',
      '10 g, 25 g, 50 g, 75 g, 100 g, 150 g, 200 g, 250 g, 500 g, 1 kg'),
    D('health', 'Skin Type', 'نوع البشرة',
      'Normal, Dry, Oily, Combination, Sensitive, Acne-Prone, Mature, All Skin Types'),
    D('health', 'Concern Addressed', 'المشكلة المستهدفة',
      'Hydration, Anti-Ageing, Brightening, Acne & Blemishes, Dark Spots, Pores, '
      'Redness, Dryness, Oil Control, Firmness, Dark Circles, Sun Protection, '
      'Hair Fall, Dandruff, Odour Control'),
    D('scent', 'Scent', 'الرائحة',
      'Unscented, Fresh, Floral, Citrus, Fruity, Musk, Vanilla, Powder, Aloe Vera, '
      'Lavender, Rose, Oud, Ocean, Mint, Coconut'),
    T('ingr', 'Key Ingredients', 'المكونات الرئيسية'),
    D('ingr', 'Free From', 'خالٍ من',
      'Parabens, Sulphates (SLS/SLES), Alcohol, Silicones, Mineral Oil, Fragrance, '
      'Gluten, Not Specified'),
    B('ingr', 'Vegan', 'نباتي (فيغن)'),
    B('ingr', 'Cruelty-Free', 'غير مُختبر على الحيوانات'),
    B('ingr', 'Organic / Natural', 'عضوي / طبيعي'),
    B('ingr', 'Halal Certified', 'حاصل على شهادة حلال'),
    D('usage', 'Gender / Target User', 'الفئة المستهدفة',
      'Men, Women, Unisex, Kids, Babies'),
    D('usage', 'Application Area', 'منطقة الاستخدام',
      'Face, Body, Hands, Feet, Hair, Scalp, Underarms, Lips, Eyes, Nails, Full Body'),
    D('usage', 'Usage Time', 'وقت الاستخدام', 'Morning, Night, Day & Night, After Shower, As Needed'),
    D('spec', 'Packaging Type', 'نوع العبوة',
      'Tube, Bottle, Jar, Pump Bottle, Spray Bottle, Sachet, Stick, Roll-On, Tin, '
      'Refill Pouch, Box'),
    N('spec', 'Shelf Life (months)', 'مدة الصلاحية (شهر)',
      '6 Months, 12 Months, 18 Months, 24 Months, 36 Months, 60 Months', dtype='Integer'),
    D('spec', 'Period After Opening (PAO)', 'مدة الاستخدام بعد الفتح',
      '3M, 6M, 9M, 12M, 18M, 24M, 36M, Not Specified'),
    D('pack', 'Pack Size', 'حجم العبوة', PACK_QTY, option='Yes'),
]

# Apparel shared block
# Verified 2026-08-10 against Ounass UAE server-rendered facets:
#   https://www.ounass.ae/women/clothing  ·  https://www.ounass.ae/men/clothing
#   https://www.ounass.ae/women/clothing/dresses
# Ounass sizes run XXS..XXXXXL (not 3XL/4XL/5XL), and its Sleeve Length facet includes
# Strapless / Off-Shoulder / One Shoulder, which a plain length scale cannot express.
APPAREL_BASE = [
    D('fit', 'Size (International)', 'المقاس (عالمي)',
      'One Size, XXS, XS, S, M, L, XL, XXL, XXXL, XXXXL, XXXXXL',
      required='Yes', option='Yes'),
    D('fit', 'Size (EU)', 'المقاس (أوروبي)',
      '32, 34, 36, 38, 40, 42, 44, 46, 48, 50, 52, 54, 56, 58, 60', option='Yes'),
    D('fit', 'Fit Type', 'نوع القصّة',
      'Slim Fit, Regular Fit, Relaxed Fit, Loose Fit, Oversized, Skinny, '
      'Straight, Tailored, Bodycon, A-Line'),
    D('fit', 'Size Type', 'نوع المقاس', 'Regular, Plus Size, Petite, Tall, Maternity'),
    D('mat', 'Main Material', 'الخامة الأساسية',
      'Cotton, Organic Cotton, Polyester, Cotton Blend, Linen, Viscose, Rayon, '
      'Denim, Wool, Cashmere, Silk, Satin, Chiffon, Velvet, Leather, Faux Leather, '
      'Nylon, Spandex / Elastane, Modal, Fleece, Jersey, Knit, Lace'),
    T('mat', 'Fabric Composition', 'تركيب النسيج'),
    D('design', 'Pattern', 'النقشة',
      'Solid, Striped, Checked, Plaid, Floral, Polka Dot, Geometric, Animal Print, '
      'Camouflage, Tie Dye, Graphic Print, Embroidered, Colour Block'),
    D('design', 'Style', 'الستايل',
      'Casual, Formal, Business, Sportswear, Streetwear, Classic, Bohemian, '
      'Vintage, Elegant, Party, Loungewear, Modest'),
    D('design', 'Occasion', 'المناسبة',
      'Everyday, Work / Office, Party & Evening, Wedding, Formal Event, Sports & Gym, '
      'Beach & Holiday, Home & Lounge, Ramadan & Eid, Travel'),
    D('design', 'Sleeve Length', 'طول الكم',
      'Sleeveless, Strapless, One Shoulder, Off-Shoulder, Cap Sleeve, Short Sleeve, '
      'Three-Quarter Sleeve, Long Sleeve, Extra Long Sleeve, Not Applicable'),
    D('design', 'Neckline', 'فتحة الرقبة',
      'Crew Neck, V-Neck, Round Neck, Square Neck, Sweetheart, Halter Neck, '
      'High Neck / Turtleneck, Boat Neck, Off-Shoulder, Collared, Hooded, '
      'Plunge Neck, Not Applicable'),
    D('design', 'Closure Type', 'نوع الإغلاق',
      'Pull-On, Button, Zipper, Hook & Eye, Drawstring, Elastic Waist, Belt, '
      'Snap Button, Lace-Up, Velcro, None'),
    D('fit', 'Length', 'الطول',
      'Cropped, Short, Regular, Midi, Long, Maxi, Ankle Length, Floor Length'),
    # Ounass splits dresses by occasion-driven type and by a three-step length scale;
    # Abayas, Jalabiyas and Kaftans are first-class types in the Gulf market.
    D('design', 'Dress Type', 'نوع الفستان',
      'Not Applicable, Day Dress, Evening Dress, Cocktail Dress, Gown, '
      'Bridal Dress, Abaya, Jalabiya, Kaftan'),
    D('fit', 'Dress Length', 'طول الفستان', 'Not Applicable, Mini, Midi, Maxi'),
    D('fit', 'Waist Rise', 'ارتفاع الخصر', 'Low Rise, Mid Rise, High Rise, Not Applicable'),
    D('usage', 'Gender', 'الجنس', 'Men, Women, Unisex, Boys, Girls, Baby', required='Yes'),
    D('usage', 'Age Group', 'الفئة العمرية',
      'Adult, Teen, Kids (4-12 Years), Toddler (1-3 Years), Baby (0-12 Months)'),
    D('usage', 'Season', 'الموسم', 'Summer, Winter, Spring, Autumn, All Season'),
    D('care', 'Care Instructions', 'تعليمات العناية',
      'Machine Wash, Hand Wash, Dry Clean Only, Do Not Bleach, Tumble Dry Low, '
      'Iron Low Heat, Do Not Iron, Wash Cold'),
    B('design', 'Lined', 'مبطّن'),
    B('design', 'Pockets', 'يحتوي على جيوب'),
    B('design', 'Stretchable', 'قابل للتمدد'),
]

# Footwear shared block
# Verified 2026-08-10 against Ounass UAE server-rendered facets:
#   https://www.ounass.ae/women/shoes  ·  https://www.ounass.ae/men/shoes
# Ounass stocks EU half sizes (34.5, 35.5, ... 46.5); a whole-number-only list cannot
# represent most of its women's footwear inventory.
FOOTWEAR_BASE = [
    D('fit', 'Size (EU)', 'المقاس (أوروبي)',
      '20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 34.5, 35, 35.5, '
      '36, 36.5, 37, 37.5, 38, 38.5, 39, 39.5, 40, 40.5, 41, 41.5, 42, 42.5, 43, '
      '43.5, 44, 44.5, 45, 45.5, 46, 46.5, 47, 48', required='Yes', option='Yes'),
    D('fit', 'Size (UK)', 'المقاس (بريطاني)',
      '3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10, 10.5, 11, 12, 13',
      option='Yes'),
    D('fit', 'Size (US)', 'المقاس (أمريكي)',
      '4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10, 10.5, 11, 11.5, 12, 13, 14',
      option='Yes'),
    D('fit', 'Width', 'العرض', 'Narrow, Medium / Standard, Wide, Extra Wide'),
    D('mat', 'Upper Material', 'خامة الجزء العلوي',
      'Genuine Leather, Faux Leather, Suede, Nubuck, Canvas, Mesh, Textile, '
      'Knit, Synthetic, Rubber, PVC, EVA'),
    D('mat', 'Sole Material', 'خامة النعل',
      'Rubber, EVA, PU (Polyurethane), TPR, PVC, Leather, Phylon, Vibram, Gum Rubber'),
    D('mat', 'Lining Material', 'خامة البطانة',
      'Textile, Leather, Mesh, Fleece, Synthetic, Unlined'),
    D('design', 'Closure Type', 'نوع الإغلاق',
      'Lace-Up, Slip-On, Velcro / Hook & Loop, Buckle, Zipper, Elastic, '
      'Ankle Strap, Toe Post'),
    D('design', 'Toe Shape', 'شكل مقدمة الحذاء',
      'Round Toe, Pointed Toe, Square Toe, Almond Toe, Open Toe, Peep Toe, Steel Toe'),
    N('design', 'Heel Height (cm)', 'ارتفاع الكعب (سم)',
      'Flat (0-1 cm), Low (1-4 cm), Mid (4-7 cm), High (7-10 cm), Very High (Above 10 cm)'),
    D('design', 'Heel Type', 'نوع الكعب',
      'Flat, Block Heel, Stiletto, Wedge, Platform, Kitten Heel, Chunky, No Heel'),
    # Ounass footwear categories, women's and men's lists merged.
    D('spec', 'Footwear Type', 'نوع الحذاء',
      'Sneakers, Sports Shoes, Sandals, Slides, Flip Flops, Mules, Pumps, '
      'Ballerinas, Loafers, Slip Ons, Boots, Espadrilles, Formal Shoes, '
      'Driving Shoes, Slippers'),
    D('design', 'Shaft Height', 'ارتفاع الساق',
      'Low Top, Mid Top, High Top, Ankle, Mid-Calf, Knee High, Over the Knee, Not Applicable'),
    D('usage', 'Gender', 'الجنس', 'Men, Women, Unisex, Boys, Girls', required='Yes'),
    D('usage', 'Age Group', 'الفئة العمرية',
      'Adult, Teen, Kids (4-12 Years), Toddler (1-3 Years), Baby (0-12 Months)'),
    D('design', 'Occasion', 'المناسبة',
      'Casual, Formal, Sports, Outdoor / Hiking, Beach, Work / Safety, Party, Home'),
    B('feat', 'Water Resistant', 'مقاوم للماء'),
    B('feat', 'Breathable', 'قابل للتهوية'),
    B('feat', 'Anti-Slip Sole', 'نعل مانع للانزلاق'),
    B('feat', 'Arch Support', 'دعم لقوس القدم'),
    B('feat', 'Removable Insole', 'نعل داخلي قابل للإزالة'),
    D('design', 'Pattern', 'النقشة',
      'Solid, Two-Tone, Printed, Animal Print, Metallic, Perforated, Embroidered'),
]

# Food shared block
FOOD_BASE = [
    N('spec', 'Net Weight (g)', 'الوزن الصافي (جم)',
      '25 g, 50 g, 100 g, 150 g, 200 g, 250 g, 400 g, 500 g, 750 g, 1 kg, 2 kg, 5 kg, 10 kg',
      option='Yes'),
    N('spec', 'Volume (ml)', 'الحجم (مل)',
      '100 ml, 200 ml, 250 ml, 330 ml, 500 ml, 750 ml, 1 L, 1.5 L, 2 L, 5 L', option='Yes'),
    D('pack', 'Packaging Type', 'نوع التغليف',
      'Bottle, Can, Carton / Tetra Pak, Pouch, Sachet, Jar, Box, Tin, Bag, '
      'Vacuum Pack, Tray, Bulk'),
    D('pack', 'Pack Size', 'عدد العبوة', PACK_QTY, option='Yes'),
    D('spec', 'Storage Condition', 'ظروف التخزين',
      'Ambient / Room Temperature, Chilled (0-4°C), Frozen (-18°C), Cool & Dry Place, '
      'Refrigerate After Opening'),
    N('spec', 'Shelf Life (months)', 'مدة الصلاحية (شهر)',
      '1 Month, 3 Months, 6 Months, 9 Months, 12 Months, 18 Months, 24 Months, 36 Months',
      dtype='Integer'),
    B('cert', 'Halal Certified', 'حاصل على شهادة حلال'),
    B('nutr', 'Organic', 'عضوي'),
    B('nutr', 'Gluten Free', 'خالٍ من الغلوتين'),
    B('nutr', 'Sugar Free', 'خالٍ من السكر'),
    B('nutr', 'Lactose Free', 'خالٍ من اللاكتوز'),
    B('nutr', 'Vegan', 'نباتي (فيغن)'),
    D('nutr', 'Dietary Preference', 'التفضيل الغذائي',
      'None, Keto, Low Fat, Low Sodium, High Protein, High Fibre, Diabetic Friendly, '
      'Plant Based, Vegetarian'),
    T('ingr', 'Ingredients', 'المكونات'),
    T('ingr', 'Allergen Information', 'معلومات مسببات الحساسية'),
    N('nutr', 'Energy per 100 g/ml (kcal)', 'السعرات لكل 100 جم/مل (سعرة)',
      'Under 50 kcal, 50-100 kcal, 101-200 kcal, 201-350 kcal, 351-500 kcal, Above 500 kcal'),
    D('spec', 'Flavour', 'النكهة',
      'Original / Plain, Vanilla, Chocolate, Strawberry, Banana, Mango, Orange, '
      'Lemon, Mixed Fruit, Coffee, Caramel, Mint, Honey, Spicy, Salted, Cheese, '
      'Barbecue, Unflavoured'),
    D('origin', 'Country of Origin', 'بلد المنشأ', ORIGIN),
    D('main', 'Brand', 'العلامة التجارية', 'Refer to Brands sheet', required='Yes'),
]
