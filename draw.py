#!/usr/bin/env python3
"""Draw the news-image-20261120 entry: a newspaper-style infographic
summarising six major stories from Friday 20 November 2026.

Output: entry.png (1024x1024) next to this file.
Only Pillow + the standard library are used, and only at build time;
the submitted entrypoint (main.py) just copies the finished PNG.
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W = H = 1024
PAPER = (246, 241, 231)
INK = (26, 26, 26)
WHITE = (255, 253, 248)
GOLD = (232, 179, 60)
GREY = (70, 70, 70)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = "DejaVuSerif-Bold.ttf"
SANS_B = "DejaVuSans-Bold.ttf"
SANS = "DejaVuSans.ttf"


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap using real text widths."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def star_points(cx, cy, r_out, r_in, n=5, rot=-90):
    pts = []
    for i in range(2 * n):
        r = r_out if i % 2 == 0 else r_in
        a = math.radians(rot + i * 180 / n)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


# ---------------------------------------------------------------- icons
def icon_radar(d, x, y, s):
    """Radar sweep with an incoming missile (Poland airspace)."""
    cx, cy = x + s // 2, y + s // 2
    for r in (s * 0.46, s * 0.32, s * 0.18):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(146, 43, 33), width=3)
    d.line([cx, cy, cx + s * 0.34, cy - s * 0.30], fill=(146, 43, 33), width=4)
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(146, 43, 33))
    # missile: diagonal body + fins + flame
    mx, my = cx + s * 0.30, cy - s * 0.28
    d.polygon([(mx, my), (mx - 26, my + 6), (mx - 6, my + 26)], fill=INK)
    d.polygon([(mx - 26, my + 6), (mx - 40, my - 2), (mx - 34, my + 14)], fill=INK)
    d.polygon([(mx - 6, my + 26), (mx + 2, my + 40), (mx - 14, my + 34)], fill=INK)
    d.polygon([(mx - 22, my + 22), (mx - 38, my + 38), (mx - 12, my + 34)],
              fill=(230, 126, 34))


def icon_skyline(d, x, y, s):
    """Skyscrapers with a burst (Riyadh strike)."""
    base = y + s - 6
    towers = [(0.06, 0.42, 0.16), (0.26, 0.66, 0.18), (0.48, 0.52, 0.15),
              (0.67, 0.78, 0.17), (0.88, 0.36, 0.11)]
    for fx, fh, fw in towers:
        tx = x + fx * s
        th = fh * s
        d.rectangle([tx, base - th, tx + fw * s, base], fill=(40, 55, 71))
        for wy in range(int(base - th) + 8, int(base) - 8, 14):
            d.rectangle([tx + 4, wy, tx + fw * s - 4, wy + 5], fill=(249, 231, 159))
    bx, by = x + s * 0.76, y + s * 0.16
    d.polygon(star_points(bx, by, s * 0.17, s * 0.07, n=8), fill=(231, 76, 60))
    d.polygon(star_points(bx, by, s * 0.10, s * 0.045, n=8), fill=(243, 156, 18))


def icon_eu_uk(d, x, y, s):
    """Circle of stars beside a cross flag (EU-UK summit)."""
    cx, cy, r = x + s * 0.30, y + s * 0.5, s * 0.26
    d.ellipse([cx - r - 8, cy - r - 8, cx + r + 8, cy + r + 8], fill=(26, 82, 118))
    for i in range(12):
        a = math.radians(i * 30)
        sx, sy = cx + r * 0.78 * math.cos(a), cy + r * 0.78 * math.sin(a)
        d.polygon(star_points(sx, sy, 6, 2.6), fill=GOLD)
    fx, fy, fw, fh = x + s * 0.58, y + s * 0.24, s * 0.38, s * 0.52
    d.rectangle([fx, fy, fx + fw, fy + fh], fill=(36, 64, 140), outline=INK, width=2)
    d.rectangle([fx + fw * 0.38, fy, fx + fw * 0.62, fy + fh], fill=WHITE)
    d.rectangle([fx, fy + fh * 0.38, fx + fw, fy + fh * 0.62], fill=WHITE)
    d.rectangle([fx + fw * 0.44, fy, fx + fw * 0.56, fy + fh], fill=(192, 57, 43))
    d.rectangle([fx, fy + fh * 0.44, fx + fw, fy + fh * 0.56], fill=(192, 57, 43))


def icon_chart(d, x, y, s):
    """Falling market chart."""
    ox, oy = x + 10, y + s - 12
    d.line([ox, y + 8, ox, oy], fill=INK, width=4)
    d.line([ox, oy, x + s - 6, oy], fill=INK, width=4)
    pts = [(ox + 6, y + s * 0.30), (ox + s * 0.28, y + s * 0.22),
           (ox + s * 0.46, y + s * 0.44), (ox + s * 0.64, y + s * 0.38),
           (ox + s * 0.82, y + s * 0.66), (x + s - 10, y + s * 0.80)]
    d.line(pts, fill=(192, 57, 43), width=6)
    ex, ey = pts[-1]
    d.polygon([(ex, ey), (ex - 20, ey - 4), (ex - 6, ey - 18)], fill=(192, 57, 43))
    for px, py in pts:
        d.ellipse([px - 5, py - 5, px + 5, py + 5], fill=(192, 57, 43))


def icon_thermo(d, x, y, s):
    """Thermometer under a sun (climate talks)."""
    sx, sy = x + s * 0.72, y + s * 0.26
    for i in range(8):
        a = math.radians(i * 45)
        d.line([sx + 16 * math.cos(a), sy + 16 * math.sin(a),
                sx + 26 * math.cos(a), sy + 26 * math.sin(a)],
               fill=(230, 126, 34), width=5)
    d.ellipse([sx - 15, sy - 15, sx + 15, sy + 15], fill=(243, 156, 18))
    tx = x + s * 0.34
    d.rounded_rectangle([tx - 13, y + 10, tx + 13, y + s * 0.74], radius=13,
                        outline=INK, width=4)
    d.rectangle([tx - 7, y + s * 0.30, tx + 7, y + s * 0.74], fill=(231, 76, 60))
    d.ellipse([tx - 20, y + s * 0.68, tx + 20, y + s * 0.68 + 40], fill=(231, 76, 60),
              outline=INK, width=4)


def icon_mercury(d, x, y, s):
    """Planet with an orbiting probe (BepiColombo)."""
    cx, cy, r = x + s * 0.46, y + s * 0.54, s * 0.30
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(169, 160, 148), outline=INK, width=3)
    for dx, dy, cr in [(-0.35, -0.2, 0.16), (0.25, 0.1, 0.22), (-0.05, 0.38, 0.13),
                       (0.42, -0.34, 0.11)]:
        px, py = cx + dx * r * 1.6, cy + dy * r * 1.6
        d.ellipse([px - cr * r, py - cr * r, px + cr * r, py + cr * r],
                  fill=(140, 131, 119))
    d.ellipse([cx - r * 1.42, cy - r * 0.58, cx + r * 1.42, cy + r * 0.58],
              outline=(40, 55, 71), width=3)
    px, py = cx + r * 1.18, cy - r * 0.38
    d.rectangle([px - 7, py - 7, px + 7, py + 7], fill=(40, 55, 71))
    d.rectangle([px - 24, py - 4, px - 9, py + 4], fill=(93, 173, 226))
    d.rectangle([px + 9, py - 4, px + 24, py + 4], fill=(93, 173, 226))


# ---------------------------------------------------------------- stories
STORIES = [
    {
        "kicker": "EUROPE · SECURITY",
        "color": (146, 43, 33),
        "icon": icon_radar,
        "headline": "Russian missiles & drone breach Polish airspace",
        "caption": "Warsaw says three objects crossed overnight as NATO "
                   "allies hold drills nearby.",
    },
    {
        "kicker": "MIDDLE EAST",
        "color": (147, 81, 22),
        "icon": icon_skyline,
        "headline": "Houthi missiles strike Riyadh towers",
        "caption": "Financial-district buildings hit; Saudi defences "
                   "intercept more over the capital.",
    },
    {
        "kicker": "EUROPE · DIPLOMACY",
        "color": (26, 82, 118),
        "icon": icon_eu_uk,
        "headline": "EU–UK summit agrees youth mobility",
        "caption": "Up to 100,000 young people a year to live, work "
                   "and study across the Channel.",
    },
    {
        "kicker": "MARKETS",
        "color": (77, 86, 86),
        "icon": icon_chart,
        "headline": "AI doubts drag world stocks lower",
        "caption": "Nikkei falls 4.8%; S&P 500 down a fifth straight "
                   "day after Anthropic's debut.",
    },
    {
        "kicker": "CLIMATE",
        "color": (202, 111, 30),
        "icon": icon_thermo,
        "headline": "COP31 draft drops fossil-fuel phase-out",
        "caption": "Antalya text removes the call to end fossil fuels "
                   "as the talks near their close.",
    },
    {
        "kicker": "SPACE",
        "color": (40, 55, 71),
        "icon": icon_mercury,
        "headline": "BepiColombo at Mercury's doorstep",
        "caption": "ESA–JAXA twin orbiters, eight years en route, set "
                   "to enter orbit on 21 Nov.",
    },
]

TICKER = ("ALSO TODAY — Estonia shuts its Russia border for 6 months · "
          "Russian strikes on Kyiv bridges kill 8 · US Senate passes "
          "energy-permitting bill 62–33 · Tanker ablaze in the "
          "Strait of Hormuz")


def draw_panel(d, story, x, y, w, h):
    d.rounded_rectangle([x, y, x + w, y + h], radius=10, fill=WHITE,
                        outline=INK, width=3)
    # header strip
    d.rounded_rectangle([x, y, x + w, y + 38], radius=10, fill=story["color"])
    d.rectangle([x, y + 24, x + w, y + 38], fill=story["color"])
    d.text((x + 16, y + 8), story["kicker"], font=font(SANS_B, 23), fill=WHITE)
    # icon
    story["icon"](d, x + 16, y + 58, 104)
    # headline + caption
    tx = x + 136
    tw = w - 136 - 16
    ty = y + 50
    for line in wrap(d, story["headline"], font(SANS_B, 30), tw)[:3]:
        d.text((tx, ty), line, font=font(SANS_B, 30), fill=INK)
        ty += 34
    ty += 2
    for line in wrap(d, story["caption"], font(SANS, 22), tw)[:3]:
        d.text((tx, ty), line, font=font(SANS, 22), fill=GREY)
        ty += 26


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # masthead
    d.rectangle([0, 0, W, 134], fill=INK)
    title = "THE WORLD IN ONE IMAGE"
    tf = font(SERIF_B, 52)
    tw = d.textlength(title, font=tf)
    d.text(((W - tw) / 2, 14), title, font=tf, fill=WHITE)
    date = "FRIDAY · 20 NOVEMBER 2026"
    df = font(SANS_B, 30)
    dw = d.textlength(date, font=df)
    d.text(((W - dw) / 2, 82), date, font=df, fill=GOLD)
    d.rectangle([0, 134, W, 140], fill=GOLD)

    # panels: 2 columns x 3 rows
    margin, gap = 26, 18
    pw = (W - 2 * margin - gap) // 2
    top, bottom = 156, 916
    ph = (bottom - top - 2 * gap) // 3
    for i, story in enumerate(STORIES):
        col, row = i % 2, i // 2
        x = margin + col * (pw + gap)
        y = top + row * (ph + gap)
        draw_panel(d, story, x, y, pw, ph)

    # ticker
    d.rectangle([0, 928, W, 984], fill=INK)
    lines = wrap(d, TICKER, font(SANS, 21), W - 48)[:2]
    ty = 936
    for line in lines:
        d.text((24, ty), line, font=font(SANS, 21), fill=WHITE)
        ty += 25

    # footer
    foot = "Compiled from Reuters, BBC, AP and agency reports of 20 November 2026."
    ff = font(SANS, 19)
    fw = d.textlength(foot, font=ff)
    d.text(((W - fw) / 2, 992), foot, font=ff, fill=GREY)

    img.save(OUT, "PNG", optimize=True)
    print(f"wrote {OUT} ({os.path.getsize(OUT)} bytes)")


if __name__ == "__main__":
    main()
