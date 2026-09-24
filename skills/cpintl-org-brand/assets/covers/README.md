# `assets/covers/` — intentionally empty (covers are generated, never stored)

Cover-page backgrounds are **generated on demand** from the brand data — they are not checked
into this repository.

- Why: the old static set was 64 files / ~3.9 MB of "hardcoded" PNG + SVG covers that could
  silently drift out of date whenever the palette, department list, naming convention, or logo
  changed. Nothing stored here is ever the single source of truth.
- Source of truth: `../colors/cpi-palette.json`, `../colors/department-directory.json`,
  `../icons/fontawesome/department-icon-map.json`, and `../logos/`.

## How to produce covers for the department you need

Run the generator from the skill root (Python 3, no third-party packages required for SVG;
PNG also works out of the box if `cairosvg` is installed):

```bash
# All 16 departments, both A4-doc and 16:9-slide covers, SVG + PNG
python3 scripts/generate_department_assets.py --covers

# Just one department / document type, e.g. the WASH Monthly Report cover (A4)
python3 scripts/generate_department_assets.py --covers --codes WASH --doc-type MonthlyReport

# SVG answers land in:  build/covers/cover-doc-<Slug>.svg | cover-slide-<Slug>.svg
# PNG answers land in:  build/covers/cover-doc-<Slug>.png | cover-slide-<Slug>.png
```

`build/` is gitignored. Copy the generated files for the department you need into Drive
(see `../../references/gui-workflow.md` Section 0) and use them in Docs (use the **PNG**) or
Slides (use the **SVG** — or the PNG if your browser uploads it more reliably).

> Building the covers for all 16 departments only needs one command and no design skills.
> If you cannot run terminal commands, ask your AI assistant to run the generator and put the
> finished files into the shared `CPI-BGD-Brand-Assets/Covers` Drive folder for you.

## Guard

`scripts/validate_brand_assets.py` fails loudly if any generated cover (`*.svg` / `*.png`)
is committed into this folder again — the repository policy is "generate, don't store."