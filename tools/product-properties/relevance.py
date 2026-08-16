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
}
# families where the personal-care formulation rules apply
CARE_FAMILIES = {'personal_care', 'makeup', 'perfume'}
# inside the personal-care tool family, oral-care attributes belong to oral items only
TOOL_FAMILY = {'care_tool'}


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
RULES = {
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
    rule = RULES.get(prop_name_norm)
    if rule is None:
        return True
    need, scope = rule
    if scope is not None and family not in scope:
        return True                       # rule does not apply to this family
    return bool(need & tags)
