# Product Properties Expansion

Generates an expanded version of the `Product Properties` and `Properties + Options`
sheets from `MatjarLink_Master_Data_File (LAST_UPDATE)`.

## What it does

The source file carries ~6 properties per category (7,007 in total across 1,172 leaf
categories). This tool expands that to **38,802 properties** — a minimum of 19 and an
average of 33 per category, with technology-heavy categories such as mobile phones
reaching 62.

Source properties are preserved: they are read from the source, kept first in the
output, and win over any added property they duplicate. New properties are appended
only when the attribute does not already exist for that category.

## Identity properties are excluded

Per-product identifiers are **not** emitted as category properties — they belong on the
product record and, for brands, on the `Brands` / `Category Brands` sheets:

> Brand · Manufacturer · Model Name · Model Number · Manufacturer Part Number (MPN) ·
> OEM Part Number · Trim / Variant · Title · Author · Publisher · ISBN · Series Name ·
> Course Title · Provider / Instructor · Provider Name · Service Name · Game Title ·
> Shade Name · Colour Code / Name · registration and licence numbers

Deliberately **kept**, because they are specifications rather than identity:

- compatibility / fitment fields (`Compatible Make`, `Compatible Model`,
  `Compatible Year From` / `To`, …) — an auto part without them cannot be matched to a car
- component specs that merely contain the word "model" (`Processor Model`, `Console Model`)
- year classifications (`Model Year`, `Year of Manufacture`) and business terms (`Pricing Model`)

Brand names that appear as *values* inside technical option lists (Intel Core i5,
Snapdragon, Dolby Atmos, Toyota under `Compatible Make`, …) are left intact — removing
them would destroy the accuracy of the specification.

## Relevance gates (`relevance.py`)

A family hands every leaf category the same property block, which is wrong whenever a
family spans different kinds of product. The gate layer derives domain tags from the
leaf category name and drops properties whose domain the category does not have:

| Removed | From | Because |
| --- | --- | --- |
| `Hair Type` | body creams, soaps, oral care | not a hair product |
| `SPF Protection`, `Waterproof` | lifting cream, body lotion | only sun care and makeup |
| `Skin Type`, `Non-Comedogenic` | non-skin items | no skin contact |
| `Warranty Type` / `Period`, `Condition` | food, beauty, medicine, cleaning | consumables are not repaired or sold refurbished |
| nutrition panel fields | anything not edible | no nutrition label exists |
| `Bristle Type`, `Flavour`, `Power Source` | nail clippers, foot files | oral-care attributes |

Every rule is scoped to the families where it applies, because the same property name
means different things elsewhere — `Application Area` is where you rub a cream, but
also where a luminaire is installed, so lighting keeps it.

Two families were added for products that were being treated as formulations:
`care_tool` (nail clipper, foot file, toothbrush, floss) and `paper_goods` (tissue).

**The gates never touch a property that came from the source workbook** — they only
filter properties this tool adds.

## Review pass

After merging, a normalisation pass repairs inconsistencies that exist in the source
workbook. Every value it applies is one that already occurs in the data — nothing is
invented:

| Fix | Rows |
| --- | --- |
| Property group unified per attribute | 3,539 |
| Arabic label unified per attribute | 2,177 |
| Duplicate attributes collapsed (`Material` / `Main Material`) | 528 |
| `Option = Yes` cleared on free-text fields (cannot be a variant) | 90 |
| Integer/Decimal type unified per attribute | 77 |
| Value lists repaired (`1,000,000:1` split by the comma delimiter) | 6 |

Duplicate collapsing always keeps the source-file property. Across all 7,007 source
properties exactly one is absorbed: `Soap` carries both `Type` and `Product Type` in the
source, and these collapse into one.

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
pip install openpyxl xlsxwriter
cd tools/product-properties
# place the master workbook next to the scripts as master.xlsx
python3 build.py     # generates the workbook
python3 repack.py    # re-packs it with a shared-strings table (~29% smaller)
```

`repack.py` exists because openpyxl writes every cell value inline, so an option list
shared by 200 categories is stored 200 times. Re-packing pools them in
`sharedStrings.xml`, cutting the file by roughly 30% with identical content and
formatting.

Each packaging run also issues a new file name:

```
MatjarLink_Product_Properties_v<N>_<YYYY-MM-DD>.xlsx
```

`N` comes from the `VERSION` file, which `repack.py` increments on every run, so a
freshly downloaded build never overwrites or gets confused with the previous one.

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
