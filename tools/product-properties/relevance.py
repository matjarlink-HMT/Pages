# -*- coding: utf-8 -*-
"""Relevance gates.

A property family gives every leaf category the same block. That is wrong whenever a
family spans several kinds of product: a nail clipper is not a formulation, a body
cream has no nutrition panel, and a tube of toothpaste carries no warranty.

Each rule is (required tags, families the rule applies to). A rule is enforced ONLY
inside its own families, because the same property name means different things
elsewhere -- "Application Area" is where you rub a cream, but also where a luminaire
gets installed. Outside its scope a property is always kept.
"""
import re

# ---------------------------------------------------------------- domain tags
_TAG_RULES = [
    ('hair',      r'shampoo|hair|conditioner|hairdress|scalp|dandruff'),
    ('oral',      r'toothpaste|mouthwash|dental|oral|floss|toothbrush|breath'),
    ('sun',       r'sunblock|sunscreen|sun care|after ?sun'),
    ('nail',      r'nail|manicure|pedicure|cuticle'),
    ('skin',      r'skin|face|facial|cream|lotion|serum|moistur|cleanser|toner|scrub|'
                  r'mask|acne|soap|body wash|body oil|hygiene gel|sanitiz|sanitis|'
                  r'balm|heel|hand cream|shaving|hair remover|sweat|roll-?on|'
                  r'slimming|lifting|wipes|deodorant|stick|spray'),
    ('implement', r'clipper|foot file|^nail file|toothbrush|tweezer|razor|comb|'
                  r'^floss$|pumice'),
    ('paper',     r'^tissue|napkin|kitchen towel|toilet paper'),
    # craft sub-domains
    ('craft_liquid', r'paint|watercolo|glaze|ink|dye|glue|adhesive|varnish|stain|'
                     r'finish|wax|fragrance oil|soap base|colorant|resin|medium'),
    ('craft_yarn',   r'yarn|thread|floss|cord|macram|string|fibre|fiber'),
    ('craft_tool',   r'needle|hook|chisel|knife|knives|wheel|kiln|blowpipe|tool|'
                     r'stand|frame|hoop|cutter|torch|pen$|brush'),
    # medical-device sub-domains
    ('med_monitor',  r'monitor|glucomet|oximet|thermomet|ecg|diagnostic|examination|'
                     r'blood pressure|glucose|pulse'),
    ('med_mobility', r'wheelchair|walker|cane|crutch|rollator|mobility|scooter'),
    ('med_support',  r'brace|splint|orthopedic|orthopaedic|support|belt'),
    ('med_sterile',  r'surgical|sterile|instrument|glove|mask|dressing|bandage|syringe'),
    ('cosmetic',  r'makeup|make-?up|lipstick|mascara|eyeshadow|foundation|concealer|'
                  r'blush|bronzer|highlighter|eyeliner|eyebrow|lip |manicure|hairdress'),
]
_TAG_RX = [(t, re.compile(p, re.I)) for t, p in _TAG_RULES]

FAMILY_TAGS = {
    'food': {'edible'}, 'beverage': {'edible'}, 'supplement': {'edible'},
    'personal_care': {'topical'}, 'makeup': {'topical', 'cosmetic'},
    'perfume': {'topical'}, 'cleaning': {'chemical'},
}

# families whose products are consumed or applied -- no warranty, no "refurbished"
CONSUMABLE_FAMILIES = {
    'food', 'beverage', 'supplement', 'medicine',
    'personal_care', 'makeup', 'perfume', 'cleaning',
    # low-value supplies: they are not repaired and not sold refurbished
    'craft', 'stationery', 'paper_goods', 'care_tool', 'gift',
    'paint', 'auto_consumable',
}
# families where the personal-care formulation rules apply
CARE_FAMILIES = {'personal_care', 'makeup', 'perfume'}
# inside the personal-care tool family, oral-care attributes belong to oral items only
TOOL_FAMILY = {'care_tool'}
CRAFT_FAMILY = {'craft'}
MED_FAMILY = {'medical_device'}


def tags_for(cat_en, family):
    name = cat_en.lower()
    tags = set(FAMILY_TAGS.get(family, ()))
    for tag, rx in _TAG_RX:
        if rx.search(name):
            tags.add(tag)
    if {'implement', 'paper'} & tags:     # a tool or a paper good is not a formulation
        tags -= {'skin', 'topical', 'hair', 'sun'}
    return tags


# ---------------------------------------------------------------- gates
# normalised property name -> (tags the category must have, families where enforced)
_RAW = {
    # formulation attributes -- only for things you actually apply to the body
    'formulation':                 ({'topical'},                    CARE_FAMILIES),
    'skin type':                   ({'skin', 'cosmetic', 'sun'},    CARE_FAMILIES),
    'concern addressed':           ({'skin', 'hair', 'cosmetic'},   CARE_FAMILIES),
    'hair type':                   ({'hair'},                       CARE_FAMILIES),
    'spf protection':              ({'sun', 'cosmetic'},            CARE_FAMILIES),
    'waterproof water resistant':  ({'sun', 'cosmetic'},            CARE_FAMILIES),
    'non comedogenic':             ({'skin', 'cosmetic'},           CARE_FAMILIES),
    'suitable for sensitive skin': ({'skin', 'cosmetic'},           CARE_FAMILIES),
    'dermatologically tested':     ({'topical'},                    CARE_FAMILIES),
    'period after opening':        ({'topical'},                    CARE_FAMILIES),
    'usage time':                  ({'topical'},                    CARE_FAMILIES),
    'application area':            ({'topical'},                    CARE_FAMILIES),
    'benefit':                     ({'topical', 'oral'},            CARE_FAMILIES),
    'free from':                   ({'topical'},                    CARE_FAMILIES),
    'cruelty free':                ({'topical'},                    CARE_FAMILIES),
    'key ingredients':             ({'topical'},                    CARE_FAMILIES),
    'scent':                       ({'topical', 'chemical'},        CARE_FAMILIES),
    'volume size':                 ({'topical'},                    CARE_FAMILIES),
    'net weight':                  ({'topical'},                    CARE_FAMILIES),
    'packaging type':              ({'topical'},                    CARE_FAMILIES),
    'vegan':                       ({'topical'},                    CARE_FAMILIES),
    'organic natural':             ({'topical'},                    CARE_FAMILIES),
    'halal certified':             ({'topical'},                    CARE_FAMILIES),
    # commerce attributes that make no sense on something you consume
    'warranty type':               (set(),                          CONSUMABLE_FAMILIES),
    'warranty period':             (set(),                          CONSUMABLE_FAMILIES),
    'condition':                   (set(),                          CONSUMABLE_FAMILIES),
    # a toothbrush has bristles and a flavour; a nail clipper has neither
    'bristle type':                ({'oral'},                       TOOL_FAMILY),
    'head size':                   ({'oral'},                       TOOL_FAMILY),
    'replaceable head':            ({'oral'},                       TOOL_FAMILY),
    'flavour':                     ({'oral'},                       TOOL_FAMILY),
    'coating treatment':           ({'oral'},                       TOOL_FAMILY),
    'length':                      ({'oral'},                       TOOL_FAMILY),
    'power source':                ({'oral'},                       TOOL_FAMILY),
    # craft supplies: a skein of yarn has no volume, a chisel has no drying time
    'volume':                      ({'craft_liquid'},               CRAFT_FAMILY),
    'quick drying':                ({'craft_liquid'},               CRAFT_FAMILY),
    'water resistant':             ({'craft_liquid'},               CRAFT_FAMILY),
    'finish':                      ({'craft_liquid'},               CRAFT_FAMILY),
    'yarn weight thickness':       ({'craft_yarn'},                 CRAFT_FAMILY),
    'needle hook size':            ({'craft_yarn', 'craft_tool'},   CRAFT_FAMILY),
    'net weight':                  ({'craft_liquid', 'craft_yarn'}, CRAFT_FAMILY),
    # a wheelchair does not take readings; a blood-pressure monitor has no seat
    'measurement type':            ({'med_monitor'},                MED_FAMILY),
    'display type':                ({'med_monitor'},                MED_FAMILY),
    'memory storage':              ({'med_monitor'},                MED_FAMILY),
    'number of user profiles':     ({'med_monitor'},                MED_FAMILY),
    'measurement accuracy':        ({'med_monitor'},                MED_FAMILY),
    'irregular heartbeat detection': ({'med_monitor'},              MED_FAMILY),
    'voice guidance':              ({'med_monitor'},                MED_FAMILY),
    'mobile app support':          ({'med_monitor'},                MED_FAMILY),
    'connectivity':                ({'med_monitor'},                MED_FAMILY),
    'automatic shut off':          ({'med_monitor'},                MED_FAMILY),
    'sterile':                     ({'med_sterile'},                MED_FAMILY),
    'single use disposable':       ({'med_sterile'},                MED_FAMILY),
    'weight capacity':             ({'med_mobility', 'med_support'}, MED_FAMILY),
    # nutrition panel -- only for things you eat
    'energy per 100 g ml':         ({'edible'}, None),
    'protein per 100 g':           ({'edible'}, None),
    'fat per 100 g':               ({'edible'}, None),
    'sugar per 100 g':             ({'edible'}, None),
    'salt sodium content':         ({'edible'}, None),
    'dietary preference':          ({'edible'}, None),
    'calories per serving':        ({'edible'}, None),
    'protein per serving':         ({'edible'}, None),
    'number of servings':          ({'edible'}, None),
    'serving suggestion':          ({'edible'}, None),
    'meal type':                   ({'edible'}, None),
    'cuisine type':                ({'edible'}, None),
}


def keep(prop_name_norm, tags, family):
    for need, scope in RULES.get(prop_name_norm, ()):
        if scope is not None and family not in scope:
            continue                      # this rule is for a different family
        if not (need & tags):
            return False                  # every applicable rule must be satisfied
    return True


RULES = {k: [v] for k, v in _RAW.items()}


def _merge(d):
    """Add rules without letting one family's rule overwrite another's."""
    for k, v in d.items():
        RULES.setdefault(k, []).append(v)


# ---------------------------------------------------------------- second wave
# The same "one block for a mixed family" flaw appears in seven more families.
# Tag rules are matched against the leaf category name; keys are norm_name() output,
# so the unit in parentheses is already stripped.
_TAG_RULES2 = [
    # sanitary
    ('wc',        r'toilet|\bwc\b|flush|bidet|shataf|urinal'),
    ('tap',       r'mixer|tap|faucet|shower|basin|sink'),
    ('heater',    r'water heater'),
    ('pump',      r'pump'),
    ('tank',      r'tank|storage'),
    # lighting: a frame or a profile emits no light
    ('fitting',   r'frame|profile|holder|track frames|lamps holders|trimless'),
    ('portable_light', r'torch|headlamp|lantern'),
    # baby
    ('carseat',   r'car seat|car baby seat|infant seat|convertible seat|booster seat'),
    ('feeding',   r'bottle|teat|pacifier|milk|feeding|steriliz|sterilis|breast pump|'
                  r'food maker|spoon|fork|dish|thermos|flask|formula|milkmaid'),
    ('diaper',    r'diaper|wipes|rash|shampoo|baby bath'),
    ('babygear',  r'stroller|carrier|carriage|cot|cradle|bed|chair|walker|monitor|'
                  r'playmat|play mat|gate|tent|swing|slide|scooter|tricycle|hanger|'
                  r'mosquito|pillow|mattress|blanket|safety'),
    # pet
    ('petfood',   r'food|feed|treat|snack|nutrition'),
    ('petgear',   r'house|cage|aquarium|bed|bowl|carrier|collar|leash|toy|grooming|'
                  r'birdhouse|doghouse'),
    # camping
    ('tent',      r'tent|shelter|canopy|gazebo'),
    ('sleep',     r'sleeping bag|mat\b|mattress|hammock|air pump'),
    ('camplight', r'lantern|torch|headlamp|ceiling light'),
    ('cooler',    r'cooler|ice box|isothermal'),
    ('campfurn',  r'chair|stool|table'),
    ('drinkware', r'water bottle|flask|cookware|dinnerware|stove'),
    # gift
    ('flower',    r'flower|bouquet|plant|letterbox|vase|basket'),
    ('cake',      r'cake|sweet|chocolate'),
    ('voucher',   r'voucher'),
    # auto accessory
    ('auto_elec', r'camera|dash cam|sensor|jump starter|charger|inverter|inflator|'
                  r'vacuum|purifier|wiring'),
    ('auto_mat',  r'mat|liner|cover'),
    ('auto_rack', r'roof bar|basket|carrier|towbar|hitch|mounted'),
]
_TAG_RX2 = [(t, re.compile(p, re.I)) for t, p in _TAG_RULES2]

SANITARY = {'sanitary'}
LIGHTING = {'lighting'}
BABY     = {'baby'}
PETS     = {'pet'}
CAMPING  = {'camping'}
GIFTS    = {'gift'}
AUTOACC  = {'auto_accessory'}

_merge({
    # --- sanitary: a storage tank has no flush, a valve has no ceramic cartridge
    'flush type':              ({'wc'},                    SANITARY),
    'flush volume':            ({'wc'},                    SANITARY),
    'soft close':              ({'wc'},                    SANITARY),
    'anti bacterial glaze':    ({'wc', 'tap'},             SANITARY),
    'ceramic cartridge':       ({'tap'},                   SANITARY),
    'thermostatic control':    ({'tap', 'heater'},         SANITARY),
    'flow rate':               ({'tap', 'pump', 'heater'}, SANITARY),
    'power':                   ({'heater', 'pump'},        SANITARY),
    'water saving':            ({'wc', 'tap'},             SANITARY),
    'anti scale':              ({'tap', 'heater'},         SANITARY),
    'maximum temperature':     ({'tap', 'heater', 'pump'}, SANITARY),
    # --- lighting: photometric data belongs to things that emit light
})
# lighting rules are "must NOT be a bare fitting"
_LIGHT_PHOTOMETRIC = [
    'colour temperature', 'colour rendering index', 'beam angle', 'luminous flux',
    'luminous efficacy', 'dimmable', 'lamp base cap', 'light source', 'lifespan',
    'motion sensor', 'daylight sensor', 'emergency battery backup', 'solar powered',
    'diffuser material', 'smart app controlled', 'smart protocol', 'power',
]
for _k in _LIGHT_PHOTOMETRIC:
    _merge({_k: ({'emits'}, LIGHTING)})
_merge({'cut out size': ({'recessed'}, LIGHTING)})

_merge({
    # --- baby
    'car seat group':          ({'carseat'},               BABY),
    'installation method':     ({'carseat'},               BABY),
    'flow rate teats':         ({'feeding'},               BABY),
    'anti colic':              ({'feeding'},               BABY),
    'absorbency overnight':    ({'diaper'},                BABY),
    'wetness indicator':       ({'diaper'},                BABY),
    'fragrance free':          ({'diaper'},                BABY),
    'alcohol free':            ({'diaper'},                BABY),
    'dermatologically tested': ({'diaper'},                BABY),
    'safety harness':          ({'carseat', 'babygear'},   BABY),
    'harness point':           ({'carseat', 'babygear'},   BABY),
    'wheels included':         ({'babygear'},              BABY),
    'reclining':               ({'carseat', 'babygear'},   BABY),
    # --- pet
    'flavour protein source':  ({'petfood'},               PETS),
    'protein content':         ({'petfood'},               PETS),
    'ingredients':             ({'petfood'},               PETS),
    'special diet':            ({'petfood'},               PETS),
    'shelf life':              ({'petfood'},               PETS),
    'storage condition':       ({'petfood'},               PETS),
    'machine washable':        ({'petgear'},               PETS),
    'foldable portable':       ({'petgear'},               PETS),
    'non slip base':           ({'petgear'},               PETS),
    'automatic electric':      ({'petgear'},               PETS),
    # --- camping
    'capacity persons':        ({'tent'},                  CAMPING),
    'water resistance':        ({'tent', 'sleep'},         CAMPING),
    'season rating':           ({'tent', 'sleep'},         CAMPING),
    'temperature rating':      ({'sleep'},                 CAMPING),
    'setup type':              ({'tent'},                  CAMPING),
    'mosquito net included':   ({'tent'},                  CAMPING),
    'windproof':               ({'tent'},                  CAMPING),
    'fire retardant':          ({'tent'},                  CAMPING),
    'brightness':              ({'camplight'},             CAMPING),
    'runtime':                 ({'camplight'},             CAMPING),
    'ice retention':           ({'cooler'},                CAMPING),
    'insulated':               ({'cooler', 'drinkware'},   CAMPING),
    'packed size':             ({'tent', 'sleep', 'campfurn'}, CAMPING),
    # --- gift
    'cake weight':             ({'cake', 'occasion'},      GIFTS),
    'cake flavour':            ({'cake', 'occasion'},      GIFTS),
    'dietary options':         ({'cake', 'occasion'},      GIFTS),
    'flower type':             ({'flower', 'occasion'},    GIFTS),
    'number of stems':         ({'flower', 'occasion'},    GIFTS),
    'vase included':           ({'flower', 'occasion'},    GIFTS),
    'voucher value':           ({'voucher', 'occasion'},   GIFTS),
    # --- auto accessory
    'power source':            ({'auto_elec'},             AUTOACC),
    'voltage':                 ({'auto_elec'},             AUTOACC),
    'load capacity':           ({'auto_rack'},             AUTOACC),
    'anti slip':               ({'auto_mat'},              AUTOACC),
})

_base_tags_for = tags_for


def tags_for(cat_en, family):          # noqa: F811 - extends the first-wave tagger
    tags = _base_tags_for(cat_en, family)
    name = cat_en.lower()
    for tag, rx in _TAG_RX2:
        if rx.search(name):
            tags.add(tag)
    if family == 'lighting':
        if 'fitting' not in tags:
            tags.add('emits')          # anything that is not a bare fitting emits light
        if re.search(r'recessed|downlight|frame|spot', name, re.I):
            tags.add('recessed')
    if family == 'gift' and not ({'flower', 'cake', 'voucher'} & tags):
        tags.add('occasion')           # occasion pages can carry any gift type
    return tags


# ---------------------------------------------------------------- third wave
# Fixes found by sampling the rebuilt file: keys must match norm_name() output,
# which strips the unit in parentheses ("Flow Rate (Teats)" -> "flow rate").
_merge({
    # baby: teat flow rate, not a tap flow rate
    'flow rate':               ({'feeding'},                 BABY),
    # pet: physical attributes belong to gear, not to a bag of food
    'material':                ({'petgear'},                 PETS),
    'dimensions':              ({'petgear'},                 PETS),
    'adjustable':              ({'petgear'},                 PETS),
    'net weight':              ({'petfood'},                 PETS),
    'size':                    ({'petgear'},                 PETS),
    # camping: keep each attribute with the gear type it describes
    'power source':            ({'camplight'},               CAMPING),
    'waterproof':              ({'tent', 'sleep'},           CAMPING),
    'uv protection':           ({'tent'},                    CAMPING),
    'quick setup pop up':      ({'tent'},                    CAMPING),
    'foldable collapsible':    ({'tent', 'campfurn', 'sleep'}, CAMPING),
    'carry bag included':      ({'tent', 'sleep', 'campfurn'}, CAMPING),
    'capacity':               ({'cooler', 'drinkware'},      CAMPING),
    # lighting: a handheld torch has no ceiling cut-out, driver or sensors
    'mounting type':           ({'fixed_light'},             LIGHTING),
    'diffuser material':       ({'fixed_light'},             LIGHTING),
    'emergency battery backup': ({'fixed_light'},            LIGHTING),
    'solar powered':           ({'fixed_light'},             LIGHTING),
    'motion sensor':           ({'fixed_light'},             LIGHTING),
    'daylight sensor':         ({'fixed_light'},             LIGHTING),
    'dimmable':                ({'fixed_light'},             LIGHTING),
    'lamp base cap':           ({'fixed_light'},             LIGHTING),
    'smart app controlled':    ({'fixed_light'},             LIGHTING),
    'smart protocol':          ({'fixed_light'},             LIGHTING),
    'input voltage':           ({'fixed_light'},             LIGHTING),
    'colour rendering index':  ({'fixed_light'},             LIGHTING),
    'luminous efficacy':       ({'fixed_light'},             LIGHTING),
    'beam angle':              ({'fixed_light'},             LIGHTING),
})

_wave2_tags_for = tags_for


def tags_for(cat_en, family):          # noqa: F811
    tags = _wave2_tags_for(cat_en, family)
    if family == 'lighting' and 'portable_light' not in tags:
        tags.add('fixed_light')        # mains-installed luminaire, not a handheld torch
    return tags


# ---------------------------------------------------------------- fourth wave
_TAG_RULES4 = [
    ('candle',    r'candle|wax|diffuser|spray|incense'),
    ('wallart',   r'wall art|painting|photo frame|mirror|clock|frame'),
    ('bbq',       r'bbq|grill|fire pit'),
    ('gardenseat', r'sofa|chair|bench|lounger|dining|balcony|gazebo|swing'),
    ('ride_on',   r'tricycle|scooter|bike|swing|slide|playground|play mat|walker|tent|ride'),
    ('boardgame', r'game|puzzle|board|card'),
    ('rc_toy',    r'remote|musical|electronic|game machine'),
    ('ppe_shoe',  r'shoe|boot'),
    ('ppe_resp',  r'respirator|mask|filter'),
    ('ppe_fire',  r'extinguisher'),
    ('ppe_ear',   r'\bear\b|hearing'),
    ('ppe_eye',   r'goggle|glasses|shield|visor'),
    ('ppe_cloth', r'vest|coverall|clothing|apron|suit'),
    ('cookware',  r'pan|pot|wok|casserole|cookware|bakeware|kettle|teapot|cooking'),
    ('kw_store',  r'container|storage|flask|bottle|jug|thermos'),
    ('machine',   r'machine|cnc|lathe|mill|drill|grind|weld|press|generator|compressor|'
                  r'pump|motor|conveyor|forklift|crane|hoist|jack|cutter|trolley'),
    ('el_breaker', r'breaker|distribution board|rccb|\bmcb\b'),
    ('el_switch', r'switch|socket|dimmer|adapter|extension'),
    ('el_cable',  r'wire|cable|conduit'),
    ('cardio',    r'treadmill|exercise bike|elliptical|rowing|multi gym|\bgym\b|machine'),
    ('bedding',   r'bed|sheet|duvet|comforter|quilt|pillow|mattress|blanket|topper'),
    ('curtain',   r'curtain'),
    ('rug',       r'carpet|rug|\bmat\b|doormat|bathmat'),
    ('liquidfood', r'sauce|oil|juice|drink|syrup|vinegar|milk|water|ghee|cream|honey'),
]
_TAG_RX4 = [(t, re.compile(p, re.I)) for t, p in _TAG_RULES4]

DECOR={'decor'}; GARDEN={'garden'}; TOY={'toy'}; PPE={'safety_ppe'}
KITCHEN={'kitchenware'}; INDUS={'industrial'}; ELEC={'electrical'}
SPORTS={'sports_equipment'}; TEXTILE={'home_textile'}; FOODF={'food','beverage'}

_merge({
    'scent':                   ({'candle'},        DECOR),
    'burn time':               ({'candle'},        DECOR),
    'mounting type':           ({'wallart'},       DECOR),
    'mounting hardware included': ({'wallart'},    DECOR),
    'grill area':              ({'bbq'},           GARDEN),
    'fuel power type':         ({'bbq'},           GARDEN),
    'seating capacity':        ({'gardenseat'},    GARDEN),
    'cushions included':       ({'gardenseat'},    GARDEN),
    'maximum load':            ({'ride_on', 'gardenseat'}, TOY | GARDEN),
    'number of players':       ({'boardgame'},     TOY),
    'language':                ({'boardgame', 'rc_toy'}, TOY),
    'remote controlled':       ({'rc_toy'},        TOY),
    'toe cap type':            ({'ppe_shoe'},      PPE),
    'filter class':            ({'ppe_resp'},      PPE),
    'fire extinguisher capacity': ({'ppe_fire'},   PPE),
    'extinguisher type':       ({'ppe_fire'},      PPE),
    'noise reduction rating':  ({'ppe_ear'},       PPE),
    'anti fog coating':        ({'ppe_eye'},       PPE),
    'reflective strips':       ({'ppe_cloth'},     PPE),
    'compatible hob types':    ({'cookware'},      KITCHEN),
    'induction compatible':    ({'cookware'},      KITCHEN),
    'oven safe':               ({'cookware'},      KITCHEN),
    'non stick':               ({'cookware'},      KITCHEN),
    'coating type':            ({'cookware'},      KITCHEN),
    'heat resistant handle':   ({'cookware'},      KITCHEN),
    'vacuum insulated':        ({'kw_store'},      KITCHEN),
    'heat retention':          ({'kw_store'},      KITCHEN),
    'leak proof':              ({'kw_store'},      KITCHEN),
    'number of axes':          ({'machine'},       INDUS),
    'cooling system':          ({'machine'},       INDUS),
    'duty cycle':              ({'machine'},       INDUS),
    'working speed rpm':       ({'machine'},       INDUS),
    'machine weight':          ({'machine'},       INDUS),
    'machine dimensions':      ({'machine'},       INDUS),
    'control system':          ({'machine'},       INDUS),
    'automation level':        ({'machine'},       INDUS),
    'output capacity per hour': ({'machine'},      INDUS),
    'tank reservoir capacity': ({'machine'},       INDUS),
    'breaking capacity':       ({'el_breaker'},    ELEC),
    'tripping curve':          ({'el_breaker'},    ELEC),
    'number of gangs poles':   ({'el_switch', 'el_breaker'}, ELEC),
    'child safety shutters':   ({'el_switch'},     ELEC),
    'usb charging ports':      ({'el_switch'},     ELEC),
    'cable cross section':     ({'el_cable'},      ELEC),
    'number of cores':         ({'el_cable'},      ELEC),
    'conductor material':      ({'el_cable'},      ELEC),
    'insulation material':     ({'el_cable'},      ELEC),
    'cable length':            ({'el_cable'},      ELEC),
    'motor power':             ({'cardio'},        SPORTS),
    'speed range':             ({'cardio'},        SPORTS),
    'incline levels':          ({'cardio'},        SPORTS),
    'console display':         ({'cardio'},        SPORTS),
    'resistance levels':       ({'cardio'},        SPORTS),
    'resistance type':         ({'cardio'},        SPORTS),
    'transport wheels':        ({'cardio'},        SPORTS),
    'heart rate monitor':      ({'cardio'},        SPORTS),
    'app connectivity':        ({'cardio'},        SPORTS),
    'thread count':            ({'bedding'},       TEXTILE),
    'firmness':                ({'bedding'},       TEXTILE),
    'filling material':        ({'bedding'},       TEXTILE),
    'curtain header type':     ({'curtain'},       TEXTILE),
    'light filtering':         ({'curtain'},       TEXTILE),
    'pile height':             ({'rug'},           TEXTILE),
    'anti slip backing':       ({'rug'},           TEXTILE),
    'volume':                  ({'liquidfood'},    FOODF),
})

_wave3_tags_for = tags_for


def tags_for(cat_en, family):          # noqa: F811
    tags = _wave3_tags_for(cat_en, family)
    for tag, rx in _TAG_RX4:
        if rx.search(cat_en.lower()):
            tags.add(tag)
    return tags


# ---------------------------------------------------------------- fifth wave
# A bolt is not a machine; a cable is not a switchboard.
_merge({
    'machine type':                ({'machine'}, INDUS),
    'power rating':                ({'machine'}, INDUS),
    'voltage phase':               ({'machine'}, INDUS),
    'load lifting capacity':       ({'machine'}, INDUS),
    'working area travel':         ({'machine'}, INDUS),
    'accuracy tolerance':          ({'machine'}, INDUS),
    'working pressure':            ({'machine'}, INDUS),
    'emergency stop':              ({'machine'}, INDUS),
    'safety guard enclosure':      ({'machine'}, INDUS),
    'overload protection':         ({'machine'}, INDUS),
    'installation service available': ({'machine'}, INDUS),
    'training provided':           ({'machine'}, INDUS),
    'spare parts available':       ({'machine'}, INDUS),
    'number of ways modules':      ({'el_breaker'}, ELEC),
    'mounting type':               ({'el_switch', 'el_breaker'}, ELEC),
    'rated current':               ({'el_switch', 'el_breaker', 'el_cable'}, ELEC),
    'power rating watts kva':      ({'el_switch', 'el_breaker'}, ELEC),
    'frequency':                   ({'el_switch', 'el_breaker'}, ELEC),
    'smart app controlled':        ({'el_switch'}, ELEC),
    'led indicator':               ({'el_switch', 'el_breaker'}, ELEC),
    'surge protection':            ({'el_switch', 'el_breaker'}, ELEC),
})
