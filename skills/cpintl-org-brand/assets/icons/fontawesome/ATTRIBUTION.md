# Font Awesome Free 7.3.1 — Attribution Notice

The SVG icons in this folder are from **Font Awesome Free 7.3.1** by **Fonticons, Inc.**

- Website: https://fontawesome.com
- Free license page: https://fontawesome.com/license/free
- Icons (SVG files): **CC BY 4.0** (Creative Commons Attribution 4.0 International) — https://creativecommons.org/licenses/by/4.0/
- The full license text is preserved in `FONT-AWESOME-FREE-LICENSE.txt` (copied unchanged from the official `fontawesome-free-7.3.1-web` package).

Each `.svg` file also carries Font Awesome's own inline license comment, and no attribution notice or license text has been stripped.

## How to attribute (what CPI must keep doing)

Font Awesome Free is free to use commercially and internally, **as long as the CC BY 4.0 attribution is preserved**:

1. **Keep this folder intact** when distributing, copying, or embedding the icons (the license file and this notice travel with the icons).
2. In any public-facing material that features these icons (website, publication, poster, public template pack), include a credit line such as:
   > Icons by [Font Awesome](https://fontawesome.com), licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
3. Internal-only CPI Workspace documents (Docs/Sheets/Slides) do not need a visible credit line, but CPI must not strip the license when the icons are reused outside the organization.

## What was adapted, and what was deliberately not vendored

- **Adapted:** the 16 `solid` SVG glyphs below were copied unchanged from the official package into this skill. The brand generator recolors them (`fill` → CPI white on accent badges) and embeds them into branded badges and cover pages at generation time — this is a permitted modification under CC BY 4.0 (with attribution preserved).
- **Not vendored:** the desktop package's OTF fonts (`Font Awesome 7 Free-Solid-900.otf`, etc.) and the web package's webfonts/CSS/JS were reviewed but are intentionally **not** committed. Native Google Docs, Sheets, and Slides cannot embed custom fonts, so the self-contained SVG files are the only form these icons can take inside Workspace documents. Add the font files only if CPI later builds a print/desktop design workflow that needs them.