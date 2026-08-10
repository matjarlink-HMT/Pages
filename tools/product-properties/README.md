# Product Properties Expansion

Generates an expanded version of the `Product Properties` and `Properties + Options`
sheets from `MatjarLink_Master_Data_File (LAST_UPDATE)`.

## What it does

The source file carries ~6 properties per category (7,007 in total across 1,172 leaf
categories). This tool expands that to **43,660 properties** — a minimum of 21 and an
average of 37 per category, with technology-heavy categories such as mobile phones
reaching 66.

Existing properties are never dropped or rewritten: they are read from the source,
de-duplicated by name, and kept first in the output. New properties are appended only
when the property name does not already exist for that category.

## How it works

1. `build.py` reads the master workbook and the `Categories` sheet.
2. Every leaf category is matched to its `Top (L1) > Sub (L2)` taxonomy path.
3. `classify.py` maps the category to one of ~60 **property families** using ordered
   keyword rules, falling back to the L2 and then L1 taxonomy level.
4. The `lib_*.py` modules define each family's property block — English and Arabic
   names, data type, option list, required flag, and whether the property can act as a
   product variant option.
5. Properties are grouped and sorted by a fixed group order (Main, General,
   Specifications, Display, Performance, … , Warranty, Packaging, Origin).

## Output

`data/MatjarLink_Product_Properties_Expanded.xlsx`

| Sheet | Contents |
| --- | --- |
| `Product Properties` | Category / Property Group / Property (EN) / Property (AR) / Data_Type / Item_List / Required |
| `Properties + Options` | Same, plus `Data` (List or Free), `Values (Item List)` and `Option` |
| `Summary` | Per-category family assignment and before/after property counts |

Both property sheets keep the exact column layout and the category / group / property
row nesting used by the source file.

## Running it

```bash
pip install openpyxl
cd tools/product-properties
# place the master workbook next to the scripts as master.xlsx
python3 build.py
```

## Property families

Families are defined across `lib_core.py` (shared blocks and value lists) and the
`lib_*.py` modules:

| Module | Families |
| --- | --- |
| `lib_tech.py` | mobile_phone, tablet, laptop, desktop, monitor, television |
| `lib_tech2.py` | camera, headphones, speaker, smartwatch, console, printer, network, storage_device, powerbank |
| `lib_home.py` | washer, fridge, ac, cooking_appliance, small_appliance, vacuum, lighting, furniture, kitchenware, home_textile, cleaning |
| `lib_auto.py` | auto_part, auto_light, auto_brake, auto_filter, auto_accessory, tyre, vehicle, auto_consumable |
| `lib_misc.py` | apparel, footwear, bag, jewellery, watch, eyewear, makeup, perfume, personal_care, baby, toy, pet, livestock |
| `lib_misc2.py` | medicine, supplement, medical_device, sports_equipment, stationery, book, craft, gift |
| `lib_ind.py` | power_tool, hand_tool, construction, tiles, paint, sanitary, electrical, industrial, safety_ppe |
| `lib_last.py` | camping, food, beverage, decor, garden, course, service, generic |
| `lib_extra.py` | phone_accessory, pc_peripheral, dishwasher, video_game |

## Known source-data issue

`Mirrors | مرايا` in the source file mixes home mirror properties with vehicle mirror
properties (Adjustment Type, Position, Integrated Indicator, Compatible Vehicle Make).
The tool does not attempt to split it — the duplicate `Mirror Type` rows are merged,
but the vehicle-specific properties are carried through as they appear in the source.
