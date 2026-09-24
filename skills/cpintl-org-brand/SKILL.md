---
name: cpintl-org-brand
description: Applies Community Partners International (CPI) Bangladesh Mission's official brand identity — colors (#D91E4D red, #41273B purple, #2D2926 black, #948794 mid-grey, #4298B5 teal, #615E9B secondary purple, #D0C4C5 light grey), Arial/Raleway typography, official logo files, the CPI-BGD file naming convention, and a Font Awesome Free 7.3.1 department-icon system — to Google Docs, Google Sheets, Google Slides, cover pages, department icons, and any other CPI Bangladesh material. Use this skill any time the user asks to create, brand, style, or template a CPI document, report, presentation, spreadsheet, cover page, logo placement, or department-specific asset (e.g. HOP, HPP, HSS, WASH, Clean Energy, Education, Livelihood, RD, M&E, HIMS, Finance, Logistics, Warehouse, HR, Field Coordination, Media and Communication) — even if the user just says "make this look like CPI" or "brand this" without naming the guide explicitly.
license: Internal use — Community Partners International Bangladesh Mission brand assets. Do not redistribute the official logo files outside CPI-authorized use. Vendored Font Awesome Free 7.3.1 icons are CC BY 4.0 — see assets/icons/fontawesome/ATTRIBUTION.md.
---

# CPI Bangladesh Brand & Google Workspace Template Skill

## What this skill contains

```
cpintl-org-brand/
├── SKILL.md                          <- you are here
├── references/
│   └── gui-workflow.md               <- exact click-by-click steps for Slides/Docs/Sheets (READ THIS for any manual/GUI request)
├── assets/
│   ├── colors/
│   │   ├── cpi-palette.json          <- the only approved colors + typography spec, machine-readable
│   │   └── department-directory.json <- all 16 program codes + proposed accent-color grouping
│   ├── logos/
│   │   ├── full-color/               <- official logo, various sizes (stacked, circle badge, horizontal)
│   │   ├── icon-mark/                <- standalone CPI icon mark, 5 sizes (32–512 px)
│   │   └── reversed-white/           <- white version for use on Purple/Red/Black backgrounds (generated from the official files via alpha-mask, not redrawn)
│   ├── icons/
│   │   ├── fontawesome/              <- vendored Font Awesome Free 7.3.1 solid icons (16, one per department),
│   │   │                                department-icon-map.json, ATTRIBUTION.md, FONT-AWESOME-FREE-LICENSE.txt
│   │   ├── icon-<Slug>.svg           <- committed branded badges (accent badge + white FA glyph + code)
│   │   └── icon-<Slug>.png           <- same badges rasterized for Docs/Sheets (Docs cannot take SVG)
│   └── covers/
│       └── README.md                 <- intentionally EMPTY: cover pages are generated on demand, never stored
└── scripts/
    ├── generate_department_assets.py <- regenerates badges + covers purely from data (SVG always; PNG via pycairo if present)
    ├── validate_brand_assets.py      <- CI-style guard: palette, 16 depts, FA map, badges, "no stored covers" policy
    └── apps_script/
        ├── BrandSlides.gs            <- builds real, native Google Slides decks with brand theme colors/fonts
        ├── BrandDocs.gs              <- builds real, native Google Docs with brand paragraph styles
        └── BrandSheets.gs            <- builds real, native Google Sheets with brand header/row formatting
```

Generated cover pages land in `build/covers/` (gitignored — copy what you need into Drive). Nothing derived is ever committed; the JSON data files and this generator are the single source of truth.

## Core rule: the logo itself is never redrawn or recolored

The brand guide explicitly forbids rotating, distorting, recoloring, or adding effects to the CPI logo. Everything in this skill respects that:

- `assets/logos/` contains only the **official uploaded files**, resized, or alpha-masked to solid white (a mechanical, lossless operation — same pixels, just recolored to white for dark backgrounds, per the guide's own "reversed logo" rule).
- The department **badges** in `assets/icons/` are a **separate, original graphic system**: a rounded badge in the department's accent color carrying a white **Font Awesome Free** glyph (heart-pulse for HOP, faucet-drip for WASH, solar-panel for Clean Energy, etc.). They are not a redraw of the real logo mark. Never present them as "the CPI logo."

## Font Awesome integration

- The 16 department glyphs come from **Font Awesome Free 7.3.1** (solid style) and are vendored unchanged under `assets/icons/fontawesome/`, each carrying its inline license comment.
- **License:** icons are **CC BY 4.0** — free forever, including commercial/internal use, but the attribution notice must be preserved. `ATTRIBUTION.md` explains exactly how to attribute in public-facing materials. Internal-only CPI Workspace docs do not need a visible credit line.
- The mapping lives in `assets/icons/fontawesome/department-icon-map.json` — change the mapping there, not in the badge files.
- The desktop OTF fonts from the same package were reviewed but deliberately **not** vendored: native Google Docs/Sheets/Slides cannot embed custom fonts, so self-contained SVGs are the only usable form. Revisit only if CPI adopts a print/desktop design workflow.

## Two ways to use this skill

### A. GUI / click-based (default — use this unless the user asks for automation)
Read **`references/gui-workflow.md`** and walk the user through it step by step in Slides, Docs, or Sheets directly in their browser. For cover pages, generate the needed cover(s) first (one command, see "Regenerating assets") and upload the output PNGs/SVGs into the shared Drive folder — or offer to run the generator and place the files in Drive for them.

### B. Apps Script automation (only if the user wants all 16 department templates generated at once, or has already set up a coding dev environment)
The three `.gs` files in `scripts/apps_script/` use the official Slides API / Docs API / Sheets API service objects (`SlidesApp`, `DocumentApp`, `SpreadsheetApp`) to build real, native Workspace files — not inserted pictures of a branded page. This is the Google-documented best-practice pattern: set theme colors and paragraph/text styles as real properties so they persist and are editable, rather than flattening the design into an image.

- Before running `BrandDocs.gs`, the user must upload a logo file to Drive and paste its file ID into `LOGO_DRIVE_FILE_ID` — walk them through **right-click file in Drive → Get link → copy the ID from the URL**.
- `buildAllDepartmentDecks()` in `BrandSlides.gs` loops over all 16 departments in one run.
- If the user has not set up Node/clasp yet, point them to Section 5–7 of their existing dev-workspace setup (nvm, `npm install -g @google/clasp`, `clasp login`, `clasp create --type standalone`) before pasting in these files.

## Regenerating assets if the brand guide changes

If CPI issues an updated brand guide (new color, new department, revised logo):

1. Update `assets/colors/cpi-palette.json` and/or `assets/colors/department-directory.json` by hand.
2. Replace files in `assets/logos/full-color/` with the new official files if the logo changed.
3. Update `assets/icons/fontawesome/department-icon-map.json` if a department's glyph should change (pick from the vendored set, or vendor a new glyph from the FA package).
4. Re-run from the skill root:
   ```bash
   python3 scripts/generate_department_assets.py     # rebuilds committed badges + on-demand covers
   python3 scripts/validate_brand_assets.py          # CI-style verification of everything
   ```
   SVG output needs only Python 3; PNG rendering also uses pycairo when present (no pip installs required by this skill). Covers are written to `build/covers/` and are gitignored — upload the ones you need into Drive.

## Validation / guardrails

`scripts/validate_brand_assets.py` (standard library only) checks the palette, the 16-department directory, the Font Awesome mapping and vendored files, the presence of every badge, and — critically — that **no generated cover `.svg`/`.png` is ever committed** under `assets/covers/`. Run it before pushing any change to this skill.

## Known gaps — confirm with the user before treating as final

- **Department accent-color mapping** (`department-directory.json`) is this skill's proposed extension of the brand guide, not something stated verbatim in the PDF for 14 of the 16 departments. Flag this to CPI leadership before wide rollout.
- **Custom Template Gallery** (native "+ New → From template" menu) requires a Workspace admin to enable it in the Admin console under Apps → Google Workspace → Drive and Docs → Templates — this may not be available on every CPI Workspace edition. The shared Drive folder approach in `gui-workflow.md` Section 0 works regardless of edition and is the safe default.
- **Raleway** (the guide's font for designed/printed materials) is a Google Font, free to use, but is not the correct choice *inside* native Google Docs/Sheets/Slides per the guide itself — Arial is specified for "Office, Digital & Google Workspace Docs." Only use Raleway if the user is exporting a PDF/poster via Slides or Docs specifically for print, not for on-screen collaborative documents.