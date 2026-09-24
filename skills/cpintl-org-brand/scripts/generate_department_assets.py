#!/usr/bin/env python3
"""
CPI Bangladesh brand asset generator (v2 — Font Awesome powered).

Generates, purely from data (never from stored "hardcoded" copies):

  1. Department badge icons (SVG + PNG, committed in assets/icons/):
     an accent-colored rounded badge carrying the department's assigned
     Font Awesome Free 7.3.1 solid glyph in white, plus the program code.
     This is a separate, original supporting graphic system — never a
     redraw of the official CPI logo mark.
  2. Cover-page backgrounds (SVG + PNG, A4 portrait and 16:9 slide),
     written to build/ (gitignored) for upload into Drive as needed:
     official logo placed with clear space, accent bar, CPI Purple bar,
     a low-opacity Font Awesome watermark glyph, and brand typography.

Only the official CPI logo files under assets/logos/ are pixel resources;
everything else is regenerated on demand so the repository never stores
stale derived artwork.

PNG rendering requires cairo (pycairo) — SVG output always works with the
Python standard library alone. cairosvg is NOT required by this script.

Run from the skill root:
    python3 scripts/generate_department_assets.py [--icons] [--covers]
        [--codes WASH CleanEnergy] [--doc-type MonthlyReport]
        [--no-png] [--output build]
"""
import argparse
import base64
import json
import math
import os
import re
import sys
from xml.sax.saxutils import escape as xml_escape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COLORS_PATH = os.path.join(ROOT, "assets", "colors", "cpi-palette.json")
DEPTS_PATH = os.path.join(ROOT, "assets", "colors", "department-directory.json")
ICON_MAP_PATH = os.path.join(ROOT, "assets", "icons", "fontawesome", "department-icon-map.json")
FA_DIR = os.path.join(ROOT, "assets", "icons", "fontawesome")
LOGO_STACKED = os.path.join(ROOT, "assets", "logos", "full-color", "cpi-logo-stacked-600.png")
ICON_OUT = os.path.join(ROOT, "assets", "icons")

FA_VIEWBOX = 512.0  # every Font Awesome solid glyph in the free set uses 512x512

try:
    import cairo  # type: ignore
    HAVE_CAIRO = True
except Exception:  # pragma: no cover - exercised only on machines without pycairo
    HAVE_CAIRO = False

with open(COLORS_PATH) as f:
    PALETTE = json.load(f)["colors"]
with open(DEPTS_PATH) as f:
    DIRECTORY = json.load(f)["themes"]
with open(ICON_MAP_PATH) as f:
    ICON_MAP = json.load(f)["icons"]


def hexcolor(key):
    return PALETTE[key]["hex"]


# ---------------------------------------------------------------------------
# SVG mini-parser (only what Font Awesome Free "solid" paths use: M/L/H/V/C/S/
# Q/T/A/Z plus lowercase relatives). Used solely to rasterize with pycairo;
# the SVG output emits the original path string unchanged.
# ---------------------------------------------------------------------------

_TOKEN_RE = re.compile(r"[MmLlHhVvCcSsQqTtAaZz]|-?\d*\.?\d+(?:[eE][+-]?\d+)?")


def parse_path(d):
    """Yield (command, [args...]) tokens from an SVG path string."""
    tokens = _TOKEN_RE.findall(d)
    i = 0
    out = []
    while i < len(tokens):
        tok = tokens[i]
        if tok in "MmLlHhVvCcSsQqTtAaZz":
            n = {"M": 2, "L": 2, "H": 1, "V": 1, "C": 6, "S": 4, "Q": 4, "T": 2, "A": 7, "Z": 0}[tok.upper()]
            if tok in "Zz":
                out.append((tok, []))
                i += 1
                continue
            args = []
            j = i + 1
            while j < len(tokens) and len(args) < n:
                try:
                    args.append(float(tokens[j]))
                except ValueError:
                    break
                j += 1
            out.append((tok, args))
            i = j
        else:
            # implicit repeat of last command
            if not out:
                raise ValueError("path starts with a number")
            last = out[-1][0]
            exp = {"M": 2, "L": 2, "H": 1, "V": 1, "C": 6, "S": 4, "Q": 4, "T": 2, "A": 7}[last.upper()]
            k = 0
            while i + k < len(tokens) and k < exp:
                try:
                    float(tokens[i + k])
                except ValueError:
                    break
                k += 1
            out.append((last if last not in "Mm" else ("L" if last == "M" else "l"), [float(t) for t in tokens[i:i + k]]))
            i += k
    return out


def _rotate(x, y, cosphi, sinphi):
    return x * cosphi - y * sinphi, x * sinphi + y * cosphi


def _arc_to_cubics(x1, y1, rx, ry, phi_deg, large_arc, sweep, x2, y2):
    """SVG 1.1 F.6.5 endpoint-to-center conversion; returns cubic segments."""
    if x1 == x2 and y1 == y2:
        return []
    rx, ry = abs(rx), abs(ry)
    phi = math.radians(phi_deg % 360.0)
    cosphi, sinphi = math.cos(phi), math.sin(phi)
    dx2, dy2 = (x1 - x2) / 2.0, (y1 - y2) / 2.0
    x1p = cosphi * dx2 + sinphi * dy2
    y1p = -sinphi * dx2 + cosphi * dy2
    lam = (x1p * x1p) / (rx * rx) + (y1p * y1p) / (ry * ry)
    if lam > 1.0:
        s = math.sqrt(lam)
        rx, ry = rx * s, ry * s
    den = rx * rx * y1p * y1p + ry * ry * x1p * x1p
    num = rx * rx * ry * ry - rx * rx * y1p * y1p - ry * ry * x1p * x1p
    coef = math.sqrt(max(0.0, num / den)) if den else 0.0
    if large_arc == sweep:
        coef = -coef
    cxp = coef * (rx * y1p / ry)
    cyp = -coef * (ry * x1p / rx)

    def _ang(ux, uy, vx, vy):
        dot = ux * vx + uy * vy
        length = math.hypot(ux, uy) * math.hypot(vx, vy)
        a = math.acos(max(-1.0, min(1.0, dot / length)))
        if ux * vy - uy * vx < 0:
            a = -a
        return a

    theta1 = _ang(1.0, 0.0, (x1p - cxp) / rx, (y1p - cyp) / ry)
    dtheta = _ang((x1p - cxp) / rx, (y1p - cyp) / ry, (-x1p - cxp) / rx, (-y1p - cyp) / ry)
    if not sweep and dtheta > 0:
        dtheta -= 2.0 * math.pi
    elif sweep and dtheta < 0:
        dtheta += 2.0 * math.pi
    segments = max(1, int(math.ceil(abs(dtheta) / (math.pi / 2.0))))
    delta = dtheta / segments
    k = 4.0 / 3.0 * math.tan(delta / 4.0)
    cubics = []
    t = theta1
    for _ in range(segments):
        t2 = t + delta
        p0x = cxp + rx * math.cos(t)
        p0y = cyp + ry * math.sin(t)
        p3x = cxp + rx * math.cos(t2)
        p3y = cyp + ry * math.sin(t2)
        p1x = p0x - k * rx * math.sin(t)
        p1y = p0y + k * ry * math.cos(t)
        p2x = p3x + k * rx * math.sin(t2)
        p2y = p3y - k * ry * math.cos(t2)
        # rotate back and translate
        q0 = _rotate(p0x, p0y, cosphi, sinphi)
        q1 = _rotate(p1x, p1y, cosphi, sinphi)
        q2 = _rotate(p2x, p2y, cosphi, sinphi)
        q3 = _rotate(p3x, p3y, cosphi, sinphi)
        cx, cy = (x1 + x2) / 2.0, (y1 + y2) / 2.0
        cubics.append((
            (q0[0] + cx, q0[1] + cy),
            (q1[0] + cx, q1[1] + cy),
            (q2[0] + cx, q2[1] + cy),
            (q3[0] + cx, q3[1] + cy),
        ))
        t = t2
    return cubics


def draw_path(ctx, d):
    """Walk an SVG path and issue the equivalent pycairo drawing calls."""
    cur = [0.0, 0.0]
    start = [0.0, 0.0]
    prev_cmd = None
    prev_cubic_ctrl = None
    prev_quad_ctrl = None
    for cmd, args in parse_path(d):
        upper = cmd.upper()
        rel = cmd.islower() and cmd not in "Zz"
        if upper == "M":
            x, y = args
            if rel:
                cur[0] += x
                cur[1] += y
            else:
                cur = [x, y]
            start = list(cur)
            ctx.move_to(*cur)
            prev_cubic_ctrl = prev_quad_ctrl = None
        elif upper == "L":
            x, y = args
            if rel:
                cur[0] += x
                cur[1] += y
            else:
                cur = [x, y]
            ctx.line_to(*cur)
            prev_cubic_ctrl = prev_quad_ctrl = None
        elif upper == "H":
            x = args[0]
            if rel:
                cur[0] += x
            else:
                cur[0] = x
            ctx.line_to(*cur)
            prev_cubic_ctrl = prev_quad_ctrl = None
        elif upper == "V":
            y = args[0]
            if rel:
                cur[1] += y
            else:
                cur[1] = y
            ctx.line_to(*cur)
            prev_cubic_ctrl = prev_quad_ctrl = None
        elif upper == "C":
            x1, y1, x2, y2, x3, y3 = args
            if rel:
                x1 += cur[0]; y1 += cur[1]; x2 += cur[0]; y2 += cur[1]; x3 += cur[0]; y3 += cur[1]
            ctx.curve_to(x1, y1, x2, y2, x3, y3)
            prev_cubic_ctrl = [x2, y2]
            prev_quad_ctrl = None
            cur = [x3, y3]
        elif upper == "S":
            x2, y2, x3, y3 = args
            if rel:
                x2 += cur[0]; y2 += cur[1]; x3 += cur[0]; y3 += cur[1]
            if prev_cubic_ctrl is not None:
                x1 = 2 * cur[0] - prev_cubic_ctrl[0]
                y1 = 2 * cur[1] - prev_cubic_ctrl[1]
            else:
                x1, y1 = cur
            ctx.curve_to(x1, y1, x2, y2, x3, y3)
            prev_cubic_ctrl = [x2, y2]
            prev_quad_ctrl = None
            cur = [x3, y3]
        elif upper == "Q":
            x1, y1, x2, y2 = args
            if rel:
                x1 += cur[0]; y1 += cur[1]; x2 += cur[0]; y2 += cur[1]
            ctx.curve_to(*_quad_to_cubic(cur[0], cur[1], x1, y1, x2, y2))
            prev_quad_ctrl = [x1, y1]
            prev_cubic_ctrl = None
            cur = [x2, y2]
        elif upper == "T":
            x2, y2 = args
            if rel:
                x2 += cur[0]; y2 += cur[1]
            if prev_quad_ctrl is not None:
                x1 = 2 * cur[0] - prev_quad_ctrl[0]
                y1 = 2 * cur[1] - prev_quad_ctrl[1]
            else:
                x1, y1 = cur
            ctx.curve_to(*_quad_to_cubic(cur[0], cur[1], x1, y1, x2, y2))
            prev_quad_ctrl = [x1, y1]
            prev_cubic_ctrl = None
            cur = [x2, y2]
        elif upper == "A":
            rx, ry, phi, laf, sf, x2, y2 = args
            if rel:
                x2 += cur[0]
                y2 += cur[1]
            for seg in _arc_to_cubics(cur[0], cur[1], rx, ry, phi, bool(laf), bool(sf), x2, y2):
                ctx.curve_to(*(seg[1] + seg[2] + seg[3]))
            prev_cubic_ctrl = prev_quad_ctrl = None
            cur = [x2, y2]
        elif upper == "Z":
            ctx.close_path()
            cur = list(start)
            prev_cubic_ctrl = prev_quad_ctrl = None
        prev_cmd = cmd
    return cur


def _quad_to_cubic(x0, y0, x1, y1, x2, y2):
    c1x = x0 + 2.0 / 3.0 * (x1 - x0)
    c1y = y0 + 2.0 / 3.0 * (y1 - y0)
    c2x = x2 + 2.0 / 3.0 * (x1 - x2)
    c2y = y2 + 2.0 / 3.0 * (y1 - y2)
    return (c1x, c1y, c2x, c2y, x2, y2)


def fa_glyph_path(icon_name):
    """Return the raw <path d=...> payload of a vendored FA solid icon."""
    p = os.path.join(FA_DIR, icon_name + ".svg")
    if not os.path.isfile(p):
        raise FileNotFoundError(f"Font Awesome icon not vendored: {icon_name} (expected {p})")
    text = open(p, encoding="utf-8").read()
    m = re.search(r'<path[^>]*\bd="([^"]+)"', text)
    if not m:
        raise ValueError(f"no path found in {p}")
    return m.group(1)


# ---------------------------------------------------------------------------
# Data helpers
# ---------------------------------------------------------------------------

def flat_program_list():
    out = []
    for theme, data in DIRECTORY.items():
        for prog in data["programs"]:
            code = prog["code"]
            if code not in ICON_MAP:
                raise KeyError(f"department code '{code}' is missing from department-icon-map.json")
            out.append({
                "theme": theme,
                "code": code,
                "slug": prog.get("slug", code),
                "name": prog["name"],
                "accent": data["accent_color"],
                "icon": ICON_MAP[code],
            })
    return out


# ---------------------------------------------------------------------------
# Badge (department icon)
# ---------------------------------------------------------------------------

def make_icon_svg(code, accent_hex, icon_name):
    safe_code = xml_escape(code)
    glyph = fa_glyph_path(icon_name)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120">
  <rect x="4" y="4" width="112" height="112" rx="24" fill="{accent_hex}"/>
  <g transform="translate(28,26) scale(0.125)">
    <path fill="#FFFFFF" d="{glyph}"/>
  </g>
  <text x="60" y="108" text-anchor="middle" font-family="Arial, sans-serif"
        font-weight="bold" font-size="15" fill="#FFFFFF">{safe_code}</text>
</svg>'''


def render_badge_png(ctx, accent_rgb, code, icon_name, size):
    """Draw the same badge directly with pycairo at `size` px."""
    w = h = float(size)
    margin = w * 4.0 / 120.0
    r = w * 24.0 / 120.0
    ctx.set_source_rgb(*accent_rgb)
    ctx.new_path()
    ctx.arc(margin + r, margin + r, r, math.pi, 1.5 * math.pi)
    ctx.arc(w - margin - r, margin + r, r, 1.5 * math.pi, 2 * math.pi)
    ctx.arc(w - margin - r, h - margin - r, r, 0, 0.5 * math.pi)
    ctx.arc(margin + r, h - margin - r, r, 0.5 * math.pi, math.pi)
    ctx.close_path()
    ctx.fill()
    # glyph, white, scaled from the 512 viewBox
    glyph_scale = 0.125 * w / 120.0
    ctx.save()
    ctx.translate(28.0 * w / 120.0, 26.0 * w / 120.0)
    ctx.scale(glyph_scale, glyph_scale)
    ctx.set_source_rgb(1, 1, 1)
    draw_path(ctx, fa_glyph_path(icon_name))
    ctx.fill()
    ctx.restore()
    # program code label
    ctx.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(w * 15.0 / 120.0)
    ctx.set_source_rgb(1, 1, 1)
    xb = w / 2.0
    yb = h * 108.0 / 120.0
    ctx.text_path(code)
    ext = ctx.text_extents(code)
    ctx.new_path()
    ctx.move_to(xb - ext.width / 2.0, yb)
    ctx.text_path(code)
    ctx.fill()


# ---------------------------------------------------------------------------
# Covers
# ---------------------------------------------------------------------------

def wrap_title(name, max_chars=22):
    words = name.split()
    line1, line2 = [], []
    cur = line1
    length = 0
    for word in words:
        if cur is line1 and length + len(word) + 1 > max_chars and line1:
            cur = line2
            length = 0
        cur.append(word)
        length += len(word) + 1
    return " ".join(line1), " ".join(line2)


def make_cover_svg(theme, code, name, accent_hex, icon_name, w, h, doc_type_label):
    purple = hexcolor("cpi_purple")
    red = hexcolor("cpi_red")
    black = hexcolor("cpi_black")
    grey = hexcolor("cpi_mid_grey")
    theme = xml_escape(theme)
    code = xml_escape(code)
    name = xml_escape(name)
    doc_type_label = xml_escape(doc_type_label)
    glyph = fa_glyph_path(icon_name)
    logo_w = w * 0.16
    logo_h = logo_w
    logo_x = w * 0.07
    logo_y = h * 0.08
    with open(LOGO_STACKED, "rb") as f:
        logo_b64 = base64.b64encode(f.read()).decode("ascii")
    title_size = h * 0.042
    max_chars = max(14, int(w / (title_size * 0.62)))
    line1, line2 = wrap_title(name, max_chars=max_chars)
    title_y1 = h * 0.50
    title_y2 = h * 0.50 + title_size * 1.15
    tag_y = (title_y2 if line2 else title_y1) + h * 0.06
    id_y = tag_y + h * 0.045
    title_tspans = f'<tspan x="{w*0.07}" dy="0">{line1}</tspan>'
    if line2:
        title_tspans += f'<tspan x="{w*0.07}" dy="{title_size*1.15}">{line2}</tspan>'
    # FA watermark glyph, right side, vertically centered, low opacity
    glyph_h = h * 0.22
    glyph_scale = glyph_h / FA_VIEWBOX
    gx = w - w * 0.02 - glyph_h
    gy = (h - glyph_h) / 2.0
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
  <rect width="{w}" height="{h}" fill="#FFFFFF"/>
  <rect x="0" y="0" width="{w}" height="{h*0.06}" fill="{accent_hex}"/>
  <rect x="0" y="{h-h*0.06}" width="{w}" height="{h*0.06}" fill="{purple}"/>
  <image x="{logo_x}" y="{logo_y}" width="{logo_w}" height="{logo_h}"
         href="data:image/png;base64,{logo_b64}" />
  <g transform="translate({gx},{gy}) scale({glyph_scale})" opacity="0.08" fill="{accent_hex}">
    <path d="{glyph}"/>
  </g>
  <text x="{w*0.07}" y="{title_y1}" font-family="Arial, sans-serif" font-weight="bold"
        font-size="{title_size}" fill="{purple}">{title_tspans}</text>
  <text x="{w*0.07}" y="{tag_y}" font-family="Arial, sans-serif" font-weight="bold"
        font-size="{h*0.03}" fill="{red}">{doc_type_label}</text>
  <text x="{w*0.07}" y="{id_y}" font-family="Arial, sans-serif"
        font-size="{h*0.02}" fill="{grey}">CPI-BGD-{code}-{doc_type_label}-YYYYMM-v01</text>
  <text x="{w*0.07}" y="{h - h*0.09}" font-family="Arial, sans-serif" font-style="italic"
        font-size="{h*0.02}" fill="{grey}">Community Partners International — {theme}</text>
</svg>'''


def render_cover_png(out_path, theme, code, name, accent_rgb, icon_name, w, h, doc_type_label):
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, int(w), int(h))
    ctx = cairo.Context(surface)
    ctx.set_source_rgb(1, 1, 1)
    ctx.paint()
    # accent top bar
    ctx.set_source_rgb(*accent_rgb)
    ctx.rectangle(0, 0, w, h * 0.06)
    ctx.fill()
    # purple bottom bar
    ctx.set_source_rgb(*_hex_to_rgb(hexcolor("cpi_purple")))
    ctx.rectangle(0, h - h * 0.06, w, h * 0.06)
    ctx.fill()
    # logo (composited in transformed user space so the transparent PNG scales cleanly)
    if os.path.isfile(LOGO_STACKED):
        logo = cairo.ImageSurface.create_from_png(LOGO_STACKED)
        lw = w * 0.16
        lh = lw * logo.get_height() / logo.get_width()
        ctx.save()
        ctx.translate(w * 0.07, h * 0.08)
        ctx.scale(lw / logo.get_width(), lh / logo.get_height())
        ctx.set_source_surface(logo, 0, 0)
        ctx.paint()
        ctx.restore()
    # FA watermark
    glyph_h = h * 0.22
    ctx.save()
    ctx.translate(w - w * 0.02 - glyph_h, (h - glyph_h) / 2.0)
    ctx.scale(glyph_h / FA_VIEWBOX, glyph_h / FA_VIEWBOX)
    ctx.set_source_rgba(*(accent_rgb + (0.08,)))
    draw_path(ctx, fa_glyph_path(icon_name))
    ctx.fill()
    ctx.restore()
    # title
    ctx.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    title_size = h * 0.042
    ctx.set_font_size(title_size)
    ctx.set_source_rgb(*_hex_to_rgb(hexcolor("cpi_purple")))
    line1, line2 = wrap_title(name, max_chars=max(14, int(w / (title_size * 0.62))))
    ctx.move_to(w * 0.07, h * 0.50)
    ctx.show_text(line1)
    if line2:
        ctx.move_to(w * 0.07, h * 0.50 + title_size * 1.15)
        ctx.show_text(line2)
    # red doc-type label
    ctx.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(h * 0.03)
    ctx.set_source_rgb(*_hex_to_rgb(hexcolor("cpi_red")))
    ctx.move_to(w * 0.07, (h * 0.50 + title_size * (1.15 if line2 else 0)) + h * 0.06)
    ctx.show_text(doc_type_label)
    # grey id line
    ctx.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(h * 0.02)
    ctx.set_source_rgb(*_hex_to_rgb(hexcolor("cpi_mid_grey")))
    ctx.move_to(w * 0.07, (h * 0.50 + title_size * (1.15 if line2 else 0)) + h * 0.105)
    ctx.show_text(f"CPI-BGD-{code}-{doc_type_label}-YYYYMM-v01")
    # italic footer
    ctx.select_font_face("Arial", cairo.FONT_SLANT_ITALIC, cairo.FONT_WEIGHT_NORMAL)
    ctx.move_to(w * 0.07, h - h * 0.09)
    ctx.show_text(f"Community Partners International — {theme}")
    surface.write_to_png(out_path)


def _hex_to_rgb(hexv):
    hexv = hexv.lstrip("#")
    return tuple(int(hexv[i:i + 2], 16) / 255.0 for i in (0, 2, 4))


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--icons", action="store_true", help="generate department badge icons into assets/icons/")
    ap.add_argument("--covers", action="store_true", help="generate cover pages into build/ (default output dir)")
    ap.add_argument("--codes", nargs="*", help="restrict to these program codes (default: all 16)")
    ap.add_argument("--doc-type", default="CoverPage")
    ap.add_argument("--no-png", action="store_true", help="skip PNG rasterization even if pycairo is present")
    ap.add_argument("--output", default=os.path.join(ROOT, "build"))
    args = ap.parse_args(argv)

    if not args.icons and not args.covers:
        args.icons = True
        args.covers = True
    programs = flat_program_list()
    if args.codes:
        wanted = set(args.codes)
        missing = wanted - {p["code"] for p in programs}
        if missing:
            raise SystemExit(f"unknown program codes: {sorted(missing)}")
        programs = [p for p in programs if p["code"] in wanted]

    png_ok = HAVE_CAIRO and not args.no_png
    if not HAVE_CAIRO and not args.no_png:
        print("note: pycairo not available — writing SVG only (PNG skipped)")

    os.makedirs(ICON_OUT, exist_ok=True)
    os.makedirs(os.path.join(args.output, "covers"), exist_ok=True)

    for p in programs:
        accent_hex = hexcolor(p["accent"])
        accent_rgb = _hex_to_rgb(accent_hex)
        if args.icons:
            icon_svg = make_icon_svg(p["code"], accent_hex, p["icon"])
            svg_path = os.path.join(ICON_OUT, f"icon-{p['slug']}.svg")
            with open(svg_path, "w", encoding="utf-8") as f:
                f.write(icon_svg)
            if png_ok:
                surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 256, 256)
                cctx = cairo.Context(surf)
                render_badge_png(cctx, accent_rgb, p["code"], p["icon"], 256)
                surf.write_to_png(os.path.join(ICON_OUT, f"icon-{p['slug']}.png"))
            print(f"icon    {p['code']:<16} {p['slug']} ({p['icon']})")
        if args.covers:
            for kind, dims, label in (("doc", (1240, 1754), args.doc_type), ("slide", (1920, 1080), "TitleSlide")):
                w, h = dims
                svg = make_cover_svg(p["theme"], p["code"], p["name"], accent_hex, p["icon"], w, h, label)
                out = os.path.join(args.output, "covers", f"cover-{kind}-{p['slug']}.svg")
                with open(out, "w", encoding="utf-8") as f:
                    f.write(svg)
                if png_ok:
                    png_path = os.path.join(args.output, "covers", f"cover-{kind}-{p['slug']}.png")
                    render_cover_png(png_path, p["theme"], p["code"], p["name"], accent_rgb, p["icon"], w, h, label)
                print(f"cover   {kind:<5} {p['code']:<16} -> {os.path.relpath(out, ROOT)}")

    print(f"\nDone. {len(programs)} departments processed into {args.output}/")


if __name__ == "__main__":
    main()