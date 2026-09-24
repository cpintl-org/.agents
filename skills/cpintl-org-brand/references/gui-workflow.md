# CPI Branding — 100% Click-Based Workflow (no coding)

This is the primary, always-available way to apply CPI branding natively inside Google Slides, Docs, and Sheets. It works on every Google Workspace edition, needs no admin permissions, and needs nothing installed. Use `scripts/apps_script/` only if you specifically want to generate all 16 department templates automatically in one go later.

Every asset referenced below lives in `assets/` in this skill folder — upload those exact files to Drive first (Section 0).

---

## 0. Upload the brand assets to Drive once

1. In Google Drive, create a folder: **CPI-BGD-Brand-Assets**.
2. Inside it, create subfolders: **Logos**, **Icons**, **Covers**.
3. Drag the contents of this skill's `assets/logos/` and `assets/icons/` folders into the matching Drive subfolders. (The badge icons — `icon-<Slug>.png` — live in `assets/icons/`; the Font Awesome glyphs they came from are in `assets/icons/fontawesome/` and are **CC BY 4.0** — internal use needs no visible credit line, but never strip the license files when redistributing outside CPI.)
4. **Cover pages are not stored in this skill** — they are generated on demand so they can never go stale. To fill the **Covers** folder, run one command from this skill's folder (or simply ask your AI assistant to run it and drop the finished files into the Drive **Covers** folder for you):
   ```bash
   python3 scripts/generate_department_assets.py --covers
   ```
   That produces `build/covers/cover-doc-*.svg|png` (A4) and `cover-slide-*.svg|png` (16:9) for all 16 departments. Upload the ones you need — use the **PNG** for Docs, the **SVG** (or PNG) for Slides. See `assets/covers/README.md`.
5. Right-click **CPI-BGD-Brand-Assets** → **Share** → set to "Anyone at [your organization] with the link — Viewer", so every staff member can reuse these without asking you each time.

---

## 1. Google Slides — native branded theme

1. Open **slides.google.com** → **Blank presentation**.
2. Menu: **Slide → Edit theme**. This opens the real Slides theme editor (not a picture — actual theme settings everyone's new slides will follow).
3. In the theme editor's left panel, click the **master slide** (top thumbnail).
4. Click the background rectangle → **Fill color → Custom** → enter `#41273B` (CPI Purple) for a dark cover option, or leave white for standard pages.
5. Click each placeholder text ("Click to edit Master title style", etc.) and set:
   - Font: **Arial**
   - Title style → Bold, size 24, color `#41273B`
   - Body style → Regular, size 11, color `#2D2926`
6. Insert the logo: **Insert → Image → Drive** → pick `assets/logos/full-color/cpi-logo-stacked-600.png` from your uploaded Brand Assets folder → resize to keep clear space (roughly 10% of slide width) → position top-left.
7. Add a thin colored bar: **Insert → Shape → Rectangle**, draw a thin bar across the top, **Fill color** → your department's accent (see table below) → **Border → None**.
8. Optional department badge: **Insert → Image → Drive** → the matching `icon-<Slug>.svg` from your uploaded **Icons** folder → drop it bottom-right or next to the title. (Slides accepts SVG directly; Docs needs the PNG instead — see the Docs section.)
9. Click **X** to close the theme editor — every new slide in this file now uses these settings automatically.
10. **File → Save as template** is not a native Slides menu item; instead: **File → Make a copy** whenever starting a new deck from this branded file, or (if your Workspace edition has it enabled) ask your Workspace admin to add this file to **Template Gallery** via **Apps → Google Workspace → Drive and Docs → Templates** in the Admin console, so it shows up under **+ New → From template** for everyone.

---

## 2. Google Docs — native branded styles

1. Open **docs.google.com** → **Blank document**.
2. Insert the logo: **Insert → Image → Upload from computer / Drive** → the stacked logo PNG → resize to ~2.5cm tall, place top-left.
3. Type your title, select it, then set font **Arial**, size **24**, bold, and font color → **Custom → #41273B**.
4. With the title still selected: **Format → Paragraph styles → Title → Update 'Title' to match** — this saves it as the document's actual Title style for reuse.
5. Repeat for Heading 1 (Arial Bold 18pt, `#D91E4D`), Heading 2 (Arial Bold 14pt, `#41273B`), Heading 3 (Arial Bold 12pt, `#41273B`), Normal text (Arial Regular 11pt, `#2D2926`, line spacing 1.25 via **Format → Line & paragraph spacing → 1.25**).
6. Once all five are set and updated to match, go to **Format → Paragraph styles → Options → Save as my default styles** — now every new Google Doc you personally create starts with CPI's styles already loaded.
7. Optional department badge: **Insert → Image → Drive** → the matching `icon-<Slug>.png` from your **Icons** folder → resize to ~1.5cm, place right of the logo or above the title.
8. Save this file itself as **CPI-BGD-Template-CoverPage-YYYYMM-v01** and keep it in the shared Brand Assets folder so colleagues can **File → Make a copy** instead of rebuilding styles from scratch.

---

## 3. Google Sheets — native branded formatting

1. Open **sheets.google.com** → **Blank spreadsheet**.
2. Type your column headers in row 1.
3. Select row 1 → **Format → Fill color → Custom → #41273B** → **Format → Text color → Custom → #FFFFFF** → **Bold**.
4. Select your full data range → **Format → Alternating colors**. In the panel that opens, click **Custom colors** and set:
   - Header color: `#41273B`
   - Color 1 (odd rows): white
   - Color 2 (even rows): `#D0C4C5` at reduced opacity — Sheets' alternating-colors panel doesn't expose opacity directly, so instead use a slightly lighter manual tint of `#D0C4C5` (e.g. `#EDE8E8`) as Color 2 to approximate the guide's "30% opacity" instruction while staying inside Sheets' native tool.
5. **View → Freeze → 1 row** to lock the header row.
6. **File → Make a copy** whenever you need a fresh sheet with this formatting.

---

## Department accent color quick-reference

| Accent color | Hex | Departments |
|---|---|---|
| CPI Red | `#D91E4D` | HOP, HPP, HSS (Health and Nutrition) |
| CPI Blue/Teal | `#4298B5` | WASH, Clean Energy, Education, Livelihood (Sustainable Development) |
| CPI Secondary Purple | `#615E9B` | RD (Research and Development) |
| CPI Purple | `#41273B` | M&E, HIMS, Finance, Logistics, Warehouse, HR, Field Coordination, Media & Comms |

(This mapping is proposed by this skill, not stated verbatim in the brand guide — see `assets/colors/department-directory.json` for the full explanation, and confirm with CPI leadership before wide rollout. Note: the M&E department's on-page label is written "M&E" per CPI's actual approved program code, but its asset **filenames** use `MonEval` instead — the `&` character causes "invalid path" errors in some Windows unzip tools, so it's kept out of every file/folder name while still appearing correctly in the visible text.)

## File naming — every saved template/document must follow

```
CPI-BGD-{ProgramCode}-{DocumentType}-{YYYYMM}-v{Version}.{ext}
```
Example: `CPI-BGD-WASH-MonthlyReport-202609-v01`
