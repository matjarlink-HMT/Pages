# Instrument Flight Procedures — merged deck

`Instrument_Flight_Procedures_Complete.pptx` — the six source `.ppt` modules merged
into one 88-slide presentation, in order, on a single redesigned template.

| # | Module | Source slides | Merged slides |
|---|--------|---------------|---------------|
| 1 | Introduction to IFP | 15 | 1–15 |
| 2 | Arcs & Radials | 20 | 16–35 |
| 3 | Fix to Fix | 5 | 36–40 |
| 4 | Holding | 22 | 41–62 |
| 5 | Terminal Approach Plates | 12 | 63–74 |
| 6 | Instrument Approach Procedures | 14 | 75–88 |

## Design system

- **Canvas** 16:9 (13.33 × 7.5 in). The 4:3 source content is recentred, never rescaled,
  so every diagram keeps its original proportions.
- **Palette** navy `#10263F` (headings), ink `#1F2C3A` (body), amber `#9A6510` (labels),
  red `#B3261E` (warnings), on white. Module openers and closers run dark.
- **Type** Cambria for headings, Calibri for body. Symbol fonts used by diagram
  glyphs and bullets are left untouched.
- **Titles** normalised to one position, size and colour across the deck.
- **Tables** navy header row, zebra body, hairline horizontal rules, rows sized to
  content so the dense airspace tables fit on the slide.

## Content

Slide text is byte-identical to the sources apart from the page number added to each
slide, and a module title added to slides 41 and 63 (both were empty in the source —
see below). Speaker notes (37 of them) are carried over.

## Rebuilding

Put the six `.ppt` files in `build/src/` (converted to `.pptx` first via
`soffice --convert-to pptx`), then:

```sh
./build/build.sh
```

`merge.py` assembles the package on one clean master/layout/theme; `style.py` applies
the design system; `textdump.py` backs the content-parity check.

## Notes on the sources

- Slide 59 (Aircraft Holding Speeds) is **hidden**, exactly as it was in the source
  deck. Unhide it in PowerPoint if it should be taught.
- Slides 41 and 63 held nothing but an empty embedded sub-presentation — a blank pink
  placeholder frame with no text. That empty frame was dropped and the slides now open
  their modules.
