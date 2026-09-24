#!/usr/bin/env python3
"""
Validates the CPI Bangladesh brand-skill asset data and guards the
"generate, don't store" policy. Runs with the Python standard library only
(no third-party packages), so it can execute anywhere, including CI.

Checks:
  1. cpi-palette.json      — exactly the 7 approved colors, valid #RRGGBB hex,
                             typography spec (Raleway for print, Arial workspace).
  2. department-directory  — every program has a unique code/slug, accent is a
                             palette key, and the FA icon map covers every code.
  3. Font Awesome set      — the department-icon-map values all resolve to a
                             vendored, unmodified (fill="currentColor" + inline
                             license comment) .svg in assets/icons/fontawesome/.
  4. Badge icons           — icon-<slug>.{svg,png} exist for all 16 departments.
  5. Covers guard          — assets/covers/ contains no generated .svg/.png
                             (hardcoded covers must not return to the repo).

Exit code 0 = all checks pass, 1 = at least one failure (with a message).
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AST = os.path.join(ROOT, "assets")

APPROVED_COLORS = {
    "cpi_red": "#D91E4D",
    "cpi_purple": "#41273B",
    "cpi_black": "#2D2926",
    "cpi_mid_grey": "#948794",
    "cpi_blue_teal": "#4298B5",
    "cpi_secondary_purple": "#615E9B",
    "cpi_light_grey": "#D0C4C5",
}
HEX_RE = re.compile(r"^#[0-9A-Fa-f]{6}$")

failures = []


def check(name, ok, detail=""):
    if ok:
        print(f"  PASS  {name}")
    else:
        failures.append(name if not detail else f"{name}: {detail}")
        print(f"  FAIL  {name}" + (f"  -> {detail}" if detail else ""))


# ---------------------------------------------------------------------------
# 1. Palette
# ---------------------------------------------------------------------------
def validate_palette():
    path = os.path.join(AST, "colors", "cpi-palette.json")
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    colors = data.get("colors", {})
    check("palette: exactly the 7 approved colors", set(colors) == set(APPROVED_COLORS),
          f"found keys {sorted(colors)}, expected {sorted(APPROVED_COLORS)}")
    hex_ok = all(isinstance(v, dict) and HEX_RE.match(v.get("hex", "")) for v in colors.values())
    check("palette: all hex values are valid #RRGGBB", hex_ok)
    match = all(v.get("hex", "").upper() == APPROVED_COLORS[k].upper() for k, v in colors.items())
    check("palette: hex values match the approved CPI palette", match)
    typo = data.get("typography", {})
    check("palette: typography lists Raleway (print) + Arial (workspace)",
          "Raleway" in typo.get("designed_printed_materials", {}).get("font", "")
          and "Arial" in typo.get("office_digital_workspace_docs", {}).get("font", ""))


# ---------------------------------------------------------------------------
# 2. Department directory + 3. Font Awesome map
# ---------------------------------------------------------------------------
def validate_departments_and_icons():
    with open(os.path.join(AST, "colors", "department-directory.json"), encoding="utf-8") as f:
        directory = json.load(f)["themes"]
    with open(os.path.join(AST, "icons", "fontawesome", "department-icon-map.json"), encoding="utf-8") as f:
        icon_map = json.load(f)["icons"]

    programs = []
    seen_codes, seen_slugs = set(), set()
    for theme, data in directory.items():
        for prog in data["programs"]:
            code, slug = prog["code"], prog.get("slug", prog["code"])
            programs.append({"code": code, "slug": slug, "accent": data["accent_color"]})
            seen_codes.add(code)
            seen_slugs.add(slug)

    check("directory: 16 approved program codes", len(seen_codes) == 16,
          f"found {len(seen_codes)} codes")
    check("directory: codes are unique", len(seen_codes) == len(programs))
    check("directory: slugs are unique", len(seen_slugs) == len(programs))
    check("directory: accents are palette keys",
          all(p["accent"] in APPROVED_COLORS for p in programs))

    map_keys = set(icon_map)
    check("icon map: covers every directory code exactly", map_keys == seen_codes,
          f"map has {sorted(map_keys - seen_codes)} extra, missing {sorted(seen_codes - map_keys)}")

    fa_dir = os.path.join(AST, "icons", "fontawesome")
    for code, icon in icon_map.items():
        p = os.path.join(fa_dir, icon + ".svg")
        exists = os.path.isfile(p)
        check(f"icon map: {code} -> {icon}.svg vendored", exists)
        if exists:
            text = open(p, encoding="utf-8").read()
            check(f"icon map: {icon}.svg is unmodified FA (fill=currentColor)",
                  'fill="currentColor"' in text)
            check(f"icon map: {icon}.svg keeps its inline license comment",
                  "Font Awesome Free" in text and "fontawesome.com" in text)
    check("fontawesome: ATTRIBUTION.md + license present",
          os.path.isfile(os.path.join(fa_dir, "ATTRIBUTION.md"))
          and os.path.isfile(os.path.join(fa_dir, "FONT-AWESOME-FREE-LICENSE.txt")))

    return programs


# ---------------------------------------------------------------------------
# 4. Badge icons
# ---------------------------------------------------------------------------
def validate_badge_icons(programs):
    icon_dir = os.path.join(AST, "icons")
    for p in programs:
        for ext in ("svg", "png"):
            f = os.path.join(icon_dir, f"icon-{p['slug']}.{ext}")
            check(f"badge: icon-{p['slug']}.{ext} exists", os.path.isfile(f))


# ---------------------------------------------------------------------------
# 5. Covers guard (generate, don't store)
# ---------------------------------------------------------------------------
def validate_covers_guard():
    covers_dir = os.path.join(AST, "covers")
    stray = []
    if os.path.isdir(covers_dir):
        for name in sorted(os.listdir(covers_dir)):
            if name.lower().endswith((".svg", ".png")):
                stray.append(name)
    check("covers guard: no generated .svg/.png stored in assets/covers/", not stray,
          f"found {stray}")
    check("covers guard: covers/README.md explains the policy",
          os.path.isfile(os.path.join(covers_dir, "README.md")))


def main():
    print("Validating cpintl-org-brand assets...")
    validate_palette()
    programs = validate_departments_and_icons()
    validate_badge_icons(programs)
    validate_covers_guard()
    print()
    if failures:
        print(f"{len(failures)} check(s) FAILED:")
        for f in failures:
            print(f"  - {f}")
        return 1
    print("All checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())