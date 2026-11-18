#!/usr/bin/env python3
"""Draw entry.png — one image summing up 18 November 2026's world news.

Original artwork drawn from scratch with PIL only. No network, no randomness:
every run produces the same pixels. Canvas is drawn at 2x and downscaled with
LANCZOS for clean edges and text.

Layout (1024 x 1024, all coordinates in final-image pixels, scaled by S):
  header   0..212    date, huge and unmistakable
  hero   228..556    Gulf tanker scene + top-story headline
  rows   576..920    three stories, each with a small drawn picture + label
  footer 936..1008   news sources
"""

import os

from PIL import Image, ImageDraw, ImageFont

S = 2                      # supersample factor
W, H = 1024, 1024          # final size
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

# --- palette ---------------------------------------------------------------
NAVY = (10, 26, 46)
NAVY2 = (16, 38, 62)
GOLD = (232, 178, 74)
WHITE = (255, 255, 255)
MIST = (205, 220, 232)
DIM = (148, 168, 186)
RED = (198, 52, 44)
ORANGE = (238, 120, 34)
YELLOW = (250, 196, 70)
SEA = (13, 47, 74)
SKY = (27, 58, 92)
INK = (8, 12, 18)
TEAL = (18, 122, 110)
WINE = (122, 30, 44)
SLATE = (52, 68, 86)
PANEL = (21, 48, 76)

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(size, bold=True):
    return ImageFont.truetype(BOLD if bold else REG, int(size * S))


def x(v):
    return int(v * S)


def box(d, x0, y0, x1, y1, fill):
    d.rectangle([x(x0), x(y0), x(x1), x(y1)], fill=fill)


def text_c(d, cx, y, s, f, fill):
    w = d.textlength(s, font=f)
    d.text((x(cx) - w / 2, x(y)), s, font=f, fill=fill)


def text_l(d, px, y, s, f, fill):
    d.text((x(px), x(y)), s, font=f, fill=fill)


def shrink_to_fit(d, s, f, max_w):
    """Return (string, font) with the font shrunk until the string fits."""
    size = f.size // S
    while d.textlength(s, font=f) > x(max_w) and size > 10:
        size -= 1
        f = ImageFont.truetype(BOLD, int(size * S))
    return s, f


# --- mini pictures ---------------------------------------------------------

def draw_tanker_scene(d, x0, y0, x1, y1):
    """Gulf of Oman: a tanker on the sea, smoke and fire on deck."""
    box(d, x0, y0, x1, y1, SKY)
    box(d, x0, y0 + 150, x1, y1, SEA)
    # horizon glow
    box(d, x0, y0 + 146, x1, y0 + 152, (64, 104, 138))
    # distant waves
    for i, wy in enumerate((168, 190, 212)):
        yy = y0 + wy
        for k in range(5):
            wx = x0 + 40 + k * 190 + (i * 60)
            d.arc([x(wx), x(yy), x(wx + 90), x(yy + 22)],
                  180, 360, fill=(38, 84, 116), width=x(3))
    # smoke plumes rising from the deck (kept inside the scene)
    smoke = [(300, 92, 40), (350, 62, 50), (405, 96, 36),
             (330, 116, 30), (390, 126, 26)]
    for sx, sy, sr in smoke:
        d.ellipse([x(x0 + sx - sr), x(y0 + sy - sr),
                   x(x0 + sx + sr), x(y0 + sy + sr)], fill=(96, 104, 112))
    # flames on deck (two triangles + glow)
    d.polygon([(x(x0 + 620), x(y0 + 150)), (x(x0 + 660), x(y0 + 62)),
               (x(x0 + 700), x(y0 + 150))], fill=ORANGE)
    d.polygon([(x(x0 + 640), x(y0 + 150)), (x(x0 + 660), x(y0 + 96)),
               (x(x0 + 680), x(y0 + 150))], fill=YELLOW)
    d.polygon([(x(x0 + 730), x(y0 + 150)), (x(x0 + 752), x(y0 + 100)),
               (x(x0 + 774), x(y0 + 150))], fill=ORANGE)
    # hull: long dark ship, bow dipping low on the right
    d.polygon([(x(x0 + 90), x(y0 + 150)), (x(x0 + 830), x(y0 + 150)),
               (x(x0 + 800), x(y0 + 214)), (x(x0 + 120), x(y0 + 214))],
              fill=INK)
    # deck line and containers
    box(d, x0 + 92, y0 + 150, x0 + 828, y0 + 158, (40, 52, 64))
    for cx in (150, 210, 270, 460, 520, 580):
        box(d, x0 + cx, y0 + 118, x0 + cx + 44, y0 + 150, (74, 92, 108))
    # funnel
    box(d, x0 + 340, y0 + 96, x0 + 396, y0 + 150, RED)
    box(d, x0 + 340, y0 + 96, x0 + 396, y0 + 108, WHITE)


def draw_bridge(d, x0, y0, size):
    """Kerch bridge: deck snapped, road arch fallen into the water."""
    box(d, x0, y0, x0 + size, y0 + size, (176, 208, 226))
    box(d, x0, y0 + 66, x0 + size, y0 + size, (32, 84, 122))
    # fallen arch piece in the water
    d.polygon([(x(x0 + 44), x(y0 + 82)), (x(x0 + 66), x(y0 + 62)),
               (x(x0 + 76), x(y0 + 92)), (x(x0 + 52), x(y0 + 98))],
              fill=(120, 128, 136))
    # left deck + pillar
    box(d, x0 + 4, y0 + 44, x0 + 44, y0 + 52, SLATE)
    box(d, x0 + 18, y0 + 52, x0 + 26, y0 + 92, SLATE)
    # right deck + pillar
    box(d, x0 + 60, y0 + 44, x0 + 100, y0 + 52, SLATE)
    box(d, x0 + 78, y0 + 52, x0 + 86, y0 + 92, SLATE)
    # broken arch stubs, leaning into the gap
    d.line([x(x0 + 44), x(y0 + 44), x(x0 + 50), x(y0 + 20)],
           fill=SLATE, width=x(5))
    d.line([x(x0 + 60), x(y0 + 44), x(x0 + 54), x(y0 + 20)],
           fill=SLATE, width=x(5))
    # gap marker: red dashes over the break
    for gy in (30, 46, 62):
        d.line([x(x0 + 50), x(y0 + gy), x(x0 + 54), x(y0 + gy)],
               fill=RED, width=x(3))


def draw_ebola(d, x0, y0, size):
    """Medical cross with virus dots on a deep-red field."""
    box(d, x0, y0, x0 + size, y0 + size, WINE)
    cx, cy = x0 + size // 2, y0 + size // 2
    box(d, cx - 10, cy - 30, cx + 10, cy + 30, WHITE)
    box(d, cx - 30, cy - 10, cx + 30, cy + 10, WHITE)
    for vx, vy, vr in ((16, 16, 6), (86, 20, 5), (14, 84, 5),
                       (88, 86, 6), (52, 12, 4), (52, 92, 4)):
        d.ellipse([x(x0 + vx - vr), x(y0 + vy - vr),
                   x(x0 + vx + vr), x(y0 + vy + vr)], fill=(232, 120, 110))


def draw_measles(d, x0, y0, size):
    """Vaccine vial with red rash dots on a teal field."""
    box(d, x0, y0, x0 + size, y0 + size, TEAL)
    # vial
    box(d, x0 + 38, y0 + 30, x0 + 66, y0 + 84, WHITE)
    box(d, x0 + 44, y0 + 22, x0 + 60, y0 + 30, (200, 210, 218))
    box(d, x0 + 44, y0 + 58, x0 + 60, y0 + 84, (120, 200, 190))
    # rash dots
    for vx, vy, vr in ((16, 20, 5), (84, 16, 6), (88, 52, 5),
                       (14, 56, 6), (18, 88, 5), (86, 88, 5)):
        d.ellipse([x(x0 + vx - vr), x(y0 + vy - vr),
                   x(x0 + vx + vr), x(y0 + vy + vr)], fill=(250, 90, 80))


# --- full image ------------------------------------------------------------

def build():
    img = Image.new("RGB", (W * S, H * S), NAVY)
    d = ImageDraw.Draw(img)

    # header
    text_c(d, 512, 26, "THE WORLD IN ONE IMAGE", font(26), GOLD)
    _, df = shrink_to_fit(d, "18 NOVEMBER 2026", font(96), 950)
    text_c(d, 512, 62, "18 NOVEMBER 2026", df, WHITE)
    box(d, 332, 178, 692, 182, GOLD)
    text_c(d, 512, 190, "WEDNESDAY  •  WHAT HAPPENED TODAY", font(24), MIST)

    # hero: tanker scene on top, headline band below it
    draw_tanker_scene(d, 32, 228, 992, 452)
    box(d, 32, 452, 992, 556, NAVY2)
    box(d, 32, 452, 992, 456, GOLD)
    _, hf = shrink_to_fit(d, "U.S. SINKS 5 IRANIAN TANKERS", font(50), 920)
    text_c(d, 512, 466, "U.S. SINKS 5 IRANIAN TANKERS", hf, WHITE)
    text_c(d, 512, 522, "Iran hits back at ships and a U.S. base in Jordan",
           font(26, bold=False), MIST)

    # three story rows
    rows = [
        (576, draw_bridge, "CRIMEA BRIDGE FALLS",
         "Road arch collapses into the sea after two days of strikes"),
        (696, draw_ebola, "EBOLA DOUBLES IN CONGO",
         "11,000+ cases, 5,400+ deaths — children hit hardest"),
        (816, draw_measles, "U.S. LOSES MEASLES-FREE STATUS",
         "5,400+ cases in 2026 — status held for 26 years"),
    ]
    for y, drawer, title, sub in rows:
        box(d, 32, y, 992, y + 104, PANEL)
        drawer(d, 32, y, 104)
        _, tf = shrink_to_fit(d, title, font(36), 820)
        text_l(d, 152, y + 12, title, tf, WHITE)
        _, sf = shrink_to_fit(d, sub, font(24, bold=False), 820)
        text_l(d, 152, y + 58, sub, sf, MIST)

    # footer
    text_c(d, 512, 944,
           "Sources: Al Jazeera  •  Reuters  •  UN News / WHO  •  PAHO",
           font(21, bold=False), DIM)
    text_c(d, 512, 972, "Reported 18 November 2026", font(21, bold=False), DIM)

    img = img.resize((W, H), Image.LANCZOS)
    img.save(OUT, optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    build()
