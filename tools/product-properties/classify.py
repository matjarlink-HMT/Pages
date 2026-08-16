# -*- coding: utf-8 -*-
"""Map each leaf category to a property family."""
import re

# Ordered rules: (regex on lowercased English leaf name, family). First match wins.
RULES = [
    # ---------------- explicit overrides (must precede the broad rules below)
    # personal-care items that are tools or paper goods, not formulations
    (r'^(nail clipper|foot file|toothbrush|floss)$', 'care_tool'),
    (r'^expansion joints$', 'construction'),
    (r'^tissue$', 'paper_goods'),
    (r'^camera parts$', 'camera'),
    (r'^(mobile and tablets spare parts|mobile & tablets repair tools|'
     r'mobile and tablets accessories|charging cables and converters|'
     r'phone & tablets charger|phone and tablets holder base|phone bag and cover|'
     r'phone battery|phone screen protection|tablets bag and cover|'
     r'tablets screen protection|laptops accessories|cleaning kit)$', 'phone_accessory'),
    (r'^(keyboard|mouse|computer accessories)$', 'pc_peripheral'),
    (r'^(air filter & parts|household spare parts)$', 'small_appliance'),
    (r'^dishwasher$', 'dishwasher'),
    (r'^home consoles games$', 'video_game'),
    (r'^measuring instruments$', 'industrial'),
    (r'^(float valves|pump spare parts|water filters|sediment filters|'
     r'carbon filters|whole-house filters|filter cartridges|ro systems)$', 'sanitary'),
    (r'^(trowels & floats|flooring installation tools & accessories)$', 'hand_tool'),
    (r'^(bottled olives & pickles)$', 'food'),
    (r'^(kilns & torches|embroidery floss|decorative materials|decorative paper|'
     r'acting|glassblowing|handicraft|painting & drawing|wood carving|'
     r'woodworking|writing|instructional media)$', 'craft'),
    (r'^(notebooks|notebooks & journals)$', 'stationery'),
    (r'^(indoor|outdoor|primer)$', 'paint'),
    (r'^(porcelain adhesive)$', 'construction'),
    (r'^(water bottles & jugs)$', 'kitchenware'),
    (r'^(thermoses and flasks for children and babies)$', 'baby'),
    (r'^(sender unit, coolant temperature|coolant water preheating)$', 'auto_part'),
    (r'^(coolant filters)$', 'auto_filter'),
    (r'^(electrical products)$', 'electrical'),
    (r'^(studio equipment’s & lighting|studio equipment\'s & lighting)$', 'lighting'),

    # ---------------- education / training (topic-style leaves)
    (r'^(business analytics|business law|business strategy|communication|e-commerce|'
     r'entrepreneurship|human resources|industry|management|media|operations|'
     r'other business|project management|real estate|sales)$', 'course'),
    (r'^(3d & animation|architectural design|design tools|fashion design|game design|'
     r'graphic design|interior design|other design|user experience design|web design)$', 'course'),
    (r'^(data science|database design|game development|mobile development|no-code development|'
     r'programming languages|software development tools|software engineering|software testing|'
     r'web development)$', 'course'),
    (r'^(accounting & bookkeeping|compliance|cryptocurrency & blockchain|economics|finance|'
     r'finance cert|financial modeling|investing & trading|money management tools|'
     r'other finance|taxes)$', 'course'),
    (r'^(dance|fitness|general health|martial arts|meditation|mental health|nutrition & diet|'
     r'other health & fitness|sports|yoga|safety & first aid)$', 'course'),
    (r'^(hardware|it certifications|network & security|operating systems & servers|'
     r'other it & software)$', 'course'),
    (r'^(arts & crafts|beauty & makeup|esoteric practices|food & beverage|gaming|'
     r'home improvement & gardening|other lifestyle|pet care & training|travel)$', 'course'),
    (r'^(affiliate marketing|branding|content marketing|digital marketing|growth hacking|'
     r'marketing analytics|marketing fundamentals|other marketing|paid advertising|'
     r'product marketing|public relations|search engine optimization|social media marketing|'
     r'video & mobile marketing)$', 'course'),
    (r'^(apple|google|microsoft|oracle|other office productivity|sap)$', 'course'),
    (r'^(career development|creativity|happiness|influence|leadership|memory & study skills|'
     r'motivation|other personal development|parenting & relationships|personal brand|'
     r'personal productivity|personal transformation|religion & spirituality|'
     r'self esteem|stress management)$', 'course'),
    (r'^(commercial photography|digital photography|other photography|photography|'
     r'photography tools|portrait photography|video design)$', 'course'),
    (r'^(engineering|humanities|language learning|math|other teaching|science|'
     r'social science|teacher training|test prep)$', 'course'),

    # ---------------- services
    (r'(car rent|car service|car wash|kids salon|salon|clinic|architectural engineering)', 'service'),

    # ---------------- vehicles (whole)
    (r'^(sedan|suv|hatchback|coupe|pickup|electric cars|hybrid cars|classic & vintage|'
     r'sport bikes|cruisers|scooters|off-road & dirt bikes|touring|electric motorcycles|'
     r'light trucks|heavy trucks|trailers|tankers|refrigerated trucks|excavators|loaders|'
     r'bulldozers|cranes|dump trucks|motorboats|yachts|jet skis|fishing boats|'
     r'inflatable boats|kayaks & canoes|cars|motorcycles|boats & yachts|heavy vehical|'
     r'trucks & trailers)$', 'vehicle'),

    # ---------------- tyres & auto consumables
    (r'(tyre|tire grips|snow chains|snow socks)', 'tyre'),
    (r'(antifreeze|engine oil|gear oil|brake fluid|coolant|adblue|car batter)', 'auto_consumable'),

    # ---------------- auto systems
    (r'(brake|abs parts|handbrake|disc brake|drum brake|wear indicator)', 'auto_brake'),
    (r'(oil filter|air filter|fuel filter|pollen filter|coolant filter|hydraulic filter|'
     r'filter set|soot/particulate|particulate filter|air filters|filters)$', 'auto_filter'),
    (r'(headlight|taillight|tail light|fog light|rear fog|reverse light|marker light|'
     r'licence plate light|license plate|car bulbs|drl |xenon ballast|door light|'
     r'combination rear light|additional lighting|stop light|indicator ?/|'
     r'parts, headlight|headlight wa)', 'auto_light'),

    # ---------------- auto accessories
    (r'(floor mats|trunk liner|cargo mats|trunk mats|all-weather mats|custom-fit mats|'
     r'ice scraper|de-icer|windshield cover|snow brush|jump starter|trickle charger|'
     r'smart charger|portable charger|standard cables|heavy-duty cables|tow rope|'
     r'warning triangle|fire extinguisher|towbar|roof bar|roof basket|roof-mounted|'
     r'hitch-mounted|trunk-mounted|dash cam|parking mode cam|front sensors|rear sensors|'
     r'sensor kits|wired cameras|wireless cameras|camera kits|conventional blades|'
     r'beam blades|hybrid blades|rear wiper|modified sine wave|pure sine wave|'
     r'high-power inverters|infant seats|convertible seats|booster seats|indoor covers|'
     r'outdoor covers|waterproof covers|uv-protection covers|car tools|car baby seat)',
     'auto_accessory'),

    # ---------------- remaining vehicle spare parts
    (r'(alternator|starter system|spark|glow ignition|crankshaft|crankcase|cylinder head|'
     r'engine air supply|engine electrics|engine mounting|engine timing|exhaust|'
     r'gaskets|lubrication|catalytic converter|manifold|silencer|turbocharger|'
     r'urea injection|lambda sensor|carburettor|fuel supply|mixture formation|'
     r'radiator|thermostat|water pump ?/|relay|sender unit|hoses|expansion joints|'
     r'clutch|drive shaft|propshaft|transmission|axle|cv joint|bellow|tripod hub|'
     r'steering|suspension|wheel nuts|window lift|window seals|windscreen cleaning|'
     r'locking system|gas springs|handles|interior equipment|body parts|'
     r'air conditioning|blower|heat exchanger|heater flap|valves|actuators|'
     r'coolant water preheating|comfort systems|control units|flasher unit|harness|'
     r'instruments|light switches|multifunctional relay|sensors|air/electric horn|'
     r'air / electric horn|belt drive|vacuum pump|pressure accumulator|control levers|'
     r'sensor ?/ ?probe|individual assembly parts|exhaust gas door|parts)$', 'auto_part'),

    # ---------------- digital / tech
    (r'(mobile phone|smartphone)', 'mobile_phone'),
    (r'^tablets$', 'tablet'),
    (r'(laptop)', 'laptop'),
    (r'(desktop|all-in-one computers|small computers|computer pieces)', 'desktop'),
    (r'^monitor', 'monitor'),
    (r'(television|^tv$)', 'television'),
    (r'(video camera|^camera|^cameras$|camera parts|photography accessories|'
     r'cameras accessories|studio equipment|video recorder)', 'camera'),
    (r'(headset & microphones|headphone case)', 'headphones'),
    (r'^speaker', 'speaker'),
    (r'(smartwatch|smart wristband)', 'smartwatch'),
    (r'(game consoles|home consoles|portable consoles)', 'console'),
    (r'(printer|copying machine|^fax$|scanner)', 'printer'),
    (r'(network & communication)', 'network'),
    (r'(information storage|memory card)', 'storage_device'),
    (r'(power bank)', 'powerbank'),
    (r'(keyboard|^mouse$|computer accessories)', 'generic'),

    # ---------------- appliances
    (r'(washing machine|dryer)', 'washer'),
    (r'(refrigerator|freezer)', 'fridge'),
    (r'(air conditioner)', 'ac'),
    (r'(cooker|^oven$|microwave|fryer|toaster|sandwich & waffle|waffle maker|'
     r'built-in appliance|electric cooker)', 'cooking_appliance'),
    (r'(coffee & tea maker|electric kettle|mixers & juice|blender|water cooler|'
     r'water dispenser)', 'small_appliance'),
    (r'(vacuum cleaner)', 'vacuum'),
    (r'(dishwasher|ironing devices|^fan$|air filter & parts|household spare parts)',
     'small_appliance'),
    (r'(water heater|water heaters|electric water heaters|gas water heaters|'
     r'instant water heaters|solar water heaters|storage water heaters)', 'sanitary'),
    (r'(water filter|water filters|sediment filters|carbon filters|ro systems|'
     r'filter cartridges|whole-house filters|water pumps|submersible pumps|'
     r'booster pumps|circulation pumps|pump controllers|pump spare parts|'
     r'water storage tanks|float)', 'sanitary'),

    # ---------------- lighting
    (r'(luminaire|led |lamp|lighting|light with motion|lights with motion|'
     r'pendant|chandelier|recessed|track frames|spike|bollard|flood light|'
     r'high bay|projector luminaire|smart lamp|torch|headlamp|lantern|'
     r'ceiling light|floor luminaire|table luminaire|wall luminaire|'
     r'surface-mounted frames|aluminum profile)', 'lighting'),

    # ---------------- construction / building
    (r'(cement|concrete|sand & aggregate|^steel$|bricks|blocks|^wood$|'
     r'cement products|insulation|protectors|expansion joints|stainless trim|'
     r'tile corner bit|primer)', 'construction'),
    (r'(granite|marble|parquet|porcelain|^tiles$|flooring)', 'tiles'),
    (r'(acrylic paints|oil paints|watercolors|^paints$|^paint$|glazes)', 'craft'),
    (r'(ceramic adhesive|porcelain adhesive|grout|silicone|silicone gun)', 'construction'),
    (r'(shataf|shower accessories|toilet seats|washbasins|^mixers$|water drainage|'
     r'angle valve|^pipes$|sanitary)', 'sanitary'),
    (r'(switches & sockets|wall switches|power sockets|dimmer switches|smart switches|'
     r'socket adapters|extension cords|circuit breakers|distribution boards|'
     r'wires and cables|wires & cables)', 'electrical'),

    # ---------------- tools
    (r'(drills & drivers|angle grinders|electric saws|heat guns|soldering tools|'
     r'testers & multimeters|power tool accessories|power tools|welding machines|'
     r'plasma cutters|soldering equipment|pneumatic tools)', 'power_tool'),
    (r'(hammers|screwdrivers|wrenches|pliers|measuring tools|trowels & floats|'
     r'ladders & scaffolding|hand tools|flooring installation tools)', 'hand_tool'),

    # ---------------- industrial
    (r'(forklifts|cnc machines|lathes|milling machines|drilling machines|'
     r'grinding machines|welding consumables|pallet jacks|conveyors|hoists & cranes|'
     r'industrial trolleys|filling machines|sealing machines|labeling machines|'
     r'shrink wrap|industrial generators|air compressors|industrial pumps|'
     r'electric motors|measuring instruments|bearings|belts & pulleys|'
     r'hydraulic components|pneumatic components|fasteners|manufacturing equipment)',
     'industrial'),
    (r'(helmets|industrial gloves|safety goggles|protective clothing|respirators|'
     r'safety gear)', 'safety_ppe'),

    # ---------------- health / medical
    (r'(antacids|ibuprofen|paracetamol|amoxicillin|lisinopril|metformin|'
     r'pain relief|cold & flu|digestive health|allergy relief|first aid medicines)',
     'medicine'),
    (r'(multivitamins|omega-3|vitamin d|vitamins & minerals|^minerals$|'
     r'herbal supplements|amino acids|carbohydrate|fat burners|pre-workout|'
     r'gainer protein|iso protein|whey protein|proteins|carbohydrates)', 'supplement'),
    (r'(blood pressure monitor|glucose meter|glucometer|pulse oximeter|nebulizer|'
     r'respiratory & breathing|surgical instruments|thermometer|wheelchair|'
     r'walkers|braces & splints|mobility aids|orthopedic supports|'
     r'physical therapy|medical & aesthetic lasers|examination tools|'
     r'diagnostic equipment|medical furniture)', 'medical_device'),
    (r'(bandages & dressings|disinfectants & sanitizers|medical masks|face masks|'
     r'medical gloves|hand sanitizers|antiseptics|first aid kits)', 'safety_ppe'),

    # ---------------- baby & kids
    (r'(diapers|baby formula|baby shampoo|baby wipes|rash cream|feeding bottles|'
     r'milk & feeding bottle|milk bottle essentials|pacifier|breast pump|'
     r'sterilize|baby food maker|breastfeeding pillow|child and baby dining chair|'
     r'child & baby dining chair|spoons, forks|thermoses & flasks|milkmaid|'
     r'baby bag|carriage & carrier|baby carrier|hug baby pillow|'
     r'baby room monitor|baby and child safety|baby & child safety|child care|'
     r'cradle|baby and child bed|baby & child bed|baby bed hanger|'
     r'mattress, blanket|mosquito nets)', 'baby'),
    (r'(^toys$|children play tent|motor tricycle|play mats|scooter and walker|'
     r'scooter & walker|swings and slides|swings & slides|kid play|'
     r"children's room decorations)", 'toy'),

    # ---------------- pets
    (r'^(birds|camels|cats|chickens|cows|dears|deer|dogs|donkeys|fish|hamsters|'
     r'houres|horses|parrots|pigeons|rabbits|sheep & goats|turtles)$', 'livestock'),
    (r'(aquarium|birdhouse|doghouse|pets house|canned food|dry food|packaged feed|'
     r'cat food|dog food|bird food|fish food|small pet food|treats & snacks)', 'pet'),

    # ---------------- beauty
    (r'(eye makeup|eyebrow makeup|face makeup|lip makeup|manicure|hairdressing|'
     r'stage makeup)', 'makeup'),
    (r'(perfume|incense|bakhoor|furniture freshener)', 'perfume'),
    (r'(anti-sweat|body lifting|body lotion|cracked leg|hair remover|hygiene gel|'
     r'oral & dental|shampoo|skin care|slimming cream|^soap$|sunblock|sunscreen|'
     r'body scrub|liquid soap|body wash|body cream|body oil|^stick$|^roll-on$|'
     r'^spray$|foot cream|foot file|heel repair|hand cream|^sanitizer$|floss|'
     r'mouthwash|toothbrush|toothpaste|moisturizer|acne treatment|cleanser|'
     r'face mask|face scrub|^serum$|^toner$|nail clipper|^wipes$|^tissue$)',
     'personal_care'),

    # ---------------- fashion
    (r'(boots|clogs & slippers|dress shoes|loafers|flip flops|sandals|shoes|'
     r'sneakers|dance shoes|^slippers$)', 'footwear'),
    (r'(basketball|^bike$|fitness & trainers|^football$|^running$|^swimming$)', 'footwear'),
    (r'(hand watches|^watches$)', 'watch'),
    (r'(earring|necklaces|^rings$|jewelry|jewellery|earrings)', 'jewellery'),
    (r'(glasses & eyewear|eyewear|sunglasses)', 'eyewear'),
    (r'(backpack|handbag|luggage|travel bags|bag accessories|wallets|keychains|'
     r'^backpacks$|fitness backpacks|duffle bags|hiking backpacks)', 'bag'),
    (r'(belts & suspenders|dresses|gloves & scarves|^hats$|jackets|jeans|'
     r'long sleeves|^pants$|shirts|shorts|skirts|socks|sportswear|^ties$|'
     r't-shirts|two-piece|underwear|v-neck|activewear|biker suits|hiking clothes|'
     r'swimming suits|workout|dance wear|costumes|robes)', 'apparel'),

    # ---------------- sports
    (r'(badel|padel|^diving$|^gym$|^hiking$|^tennis$|sports armband|sports headband|'
     r'practice equipment)', 'sports_equipment'),
    (r'(snacks & healthy food)', 'supplement'),

    # ---------------- camping / travel
    (r'(chairs & stools|^tables$|cookware$|coolers|dinnerware|stoves|isothermal|'
     r'water bottles|air pumps|hammocks|mattresses|sleeping bags|camping tents|'
     r'shelters|tent accessories|torches)', 'camping'),

    # ---------------- home
    (r'(bathmats|bathroom accessories|^storage$|towels)', 'home_textile'),
    (r'(bed set|bed toppers|bedsheets|carpets & rugs|curtain|cushion|doormats|'
     r'^mattress$|^pillows$|quilts & blankets)', 'home_textile'),
    (r'(candles|clocks & frames|decorative|diffusers & sprays|gift sets|mirrors|'
     r'photo frames|plants & flowers|wall arts|lighting & lamps)', 'decor'),
    (r'(bedrooms sets|clothes & dressing|dinning & consoles|dining & consoles|'
     r'office desks|office sofa|reception & coffee|shelfs and library|'
     r'shelves & library|sofas & chairs|tvs studio|tv units)', 'furniture'),
    (r'(air freshener|bathroom cleaning|floor cleaning|glass cleaning|kitchen cleaning|'
     r'liquid detergent|sanitizer / disinfectant|washing clothes|cleaning products|'
     r'cleaning kit)', 'cleaning'),
    (r'(bakeware|cooking tools|cookware sets|cutlery|dishes|^flask|hot pot|'
     r'knife & cutting|mugs|pots & pans|serve ware|serving dishes|'
     r'storage & organization|tea pots|water bottles & jugs)', 'kitchenware'),
    (r'(artificial plants|balcony sets|fountains|garden ornaments|gazebo|loungers|'
     r'outdoor bbq|outdoor bench|outdoor cushions|outdoor dining|outdoor sofa|'
     r'outdoor umbrella|^pots$|^swings$|^indoor$|^outdoor$)', 'garden'),

    # ---------------- food & beverage
    (r'(coffee|dairy alternatives|juices|long life milk|milk powder|powdered drinks|'
     r'soft drinks|sports & energy drinks|^tea$|^water$)', 'beverage'),
    (r'(biscuits|chocolates|gums & breath|cereals|jams & spreads|oats & bars|'
     r'canned |chips|nuts & dates|popcorn|snacks|condiment|cooking sauces|'
     r'oils & ghee|pulses|salt & pepper|bottled olives|salad dressing|'
     r'^chicken$|burgers|fish & seafood|frozen |fruits & vegetables|ice cream|'
     r'meat & poultry|pastry sheets|ready meals|home baking|^baking$|'
     r'sugar & other|pasta & noodles|^rice$|soups|gluten free|lactose free|'
     r'^organic$|plant based|sugar free|^vegan$|arabic food|chinese food|'
     r'filipino food|indian food|italian food|japanese food|korean food|'
     r'mexican food|other ethnic|sri lankan food|thai food|condiments)', 'food'),

    # ---------------- gifts
    (r'(congratulations|get well soon|i love you|just because|sympathy|thank you|'
     r'flowers in|hand-tied|letterbox|only flowers|^plants$|cakes|'
     r'sweets & chocolate|vouchers|anniversary|birthday|graduation|new baby born|'
     r'wedding congratulations)', 'gift'),

    # ---------------- books & stationery
    (r'(books|^novels$|kids story|kids stories|educational books|history books|'
     r'language books|scripts & plays|guide books|instruction books|writing guides|'
     r'acting guides|pattern guides)', 'book'),
    (r'(eraser|^ink$|^inks$|markers|notebooks|painting and colouring|'
     r'painting & colouring|^pencil$|^pencils$|^pens$|sketching pencils|'
     r'pens & ink|calligraphy pens|calligraphy sets|notebooks & journals|'
     r'practice pads)', 'stationery'),

    # ---------------- crafts / hobbies
    (r'(brushes & tools|canvases & paper|^clay$|pottery|kilns|crochet|^yarn$|'
     r'^patterns$|cross-stitch|embroidery|aida fabric|hoops & frames|craft |'
     r'glue|decorative materials|carving knives|chisels|wood blanks|'
     r'finishing supplies|^needles$|^threads$|^fabric$|needlework|knitting|'
     r'scrapbook|stickers|cutting tools|decorative paper|lumber & boards|'
     r'finishes & stains|glass rods|blowpipes|origami paper|display stands|'
     r'^wax$|wicks|molds|fragrance oils|^dyes$|soap base|fragrances|colorants|'
     r'^beads$|wire & findings|^tools$|stringing materials|model kits|'
     r'modeling tools|leather sheets|stamping tools|macram|rings & dowels|'
     r'instructional media)', 'craft'),
]

L2_FALLBACK = {
    'Books': 'book', 'Stationery': 'stationery',
    'Body Care': 'personal_care', 'Cosmetics': 'makeup', 'Perfume & Aromatic': 'perfume',
    'Mobile & Tablets': 'generic', 'Laptops': 'laptop', 'Cameras': 'camera',
    'Computers & Peripherals': 'generic', 'Game Consoles': 'console',
    'Office Machines': 'printer', 'Smartwatches & Wristband': 'smartwatch',
    'Furniture': 'furniture', 'Home Appliance': 'small_appliance',
    'Kitchen & Dining': 'kitchenware', 'Bedding': 'home_textile',
    'Bath': 'home_textile', 'Home Decor': 'decor', 'Outdoor': 'garden',
    'Cleaning': 'cleaning', 'Lighting (Indoor)': 'lighting', 'Lighting (Outdoor)': 'lighting',
    'Construction Materials': 'construction', 'Flooring & Wall Coverings': 'tiles',
    'Flooring Accessories': 'construction', 'Sanitary Items': 'sanitary',
    'Silicones & Adhesives': 'construction', 'Insulation Materials': 'construction',
    'Paints': 'paint', 'Hygiene & Protection': 'safety_ppe',
    'Extensions & Connections': 'electrical',
}

L1_FALLBACK = {
    'Education & Training': 'course',
    'Vehicle Spare Parts': 'auto_part',
    'Vehicle Accessories': 'auto_accessory',
    'Vehicles': 'vehicle',
    'Construction Materials & Equipment': 'construction',
    'Home & Garden': 'generic',
    'Hobbies & Arts': 'craft',
    'Food': 'food',
    'Digital Products': 'generic',
    'Fashion & Clothing': 'apparel',
    'Manufacturing Equipment & Machinery': 'industrial',
    'Fitness & Health': 'sports_equipment',
    'Children Products, Toys & Accessories': 'toy',
    'Beauty and Care': 'personal_care',
    'Pets & Pets Stuff': 'pet',
    'Medicines & Medical Equipment': 'medical_device',
    'Electrical Products': 'electrical',
    'Gift & Flower': 'gift',
    'Travel & Camping': 'camping',
    'Books & Stationery': 'book',
}

_COMPILED = [(re.compile(p), f) for p, f in RULES]


def classify(leaf_en, l1=None, l2=None):
    name = leaf_en.strip().lower().replace('’', "'")
    for rx, fam in _COMPILED:
        if rx.search(name):
            return fam
    if l2 and l2 in L2_FALLBACK:
        return L2_FALLBACK[l2]
    if l1 and l1 in L1_FALLBACK:
        return L1_FALLBACK[l1]
    return 'generic'
