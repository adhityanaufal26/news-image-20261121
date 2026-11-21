#!/usr/bin/env python3
"""Draw entry.png: Saturday 21 November 2026 in one 1024x1024 image.
Deterministic Pillow drawing. No network, no randomness, no timestamps."""
from PIL import Image, ImageDraw, ImageFont
import os

W = H = 1024
CREAM = (247, 241, 222)
INK = (26, 26, 26)
RED = (185, 28, 28)
NAVY = (30, 58, 95)
TEAL = (13, 118, 110)
GOLD = (180, 83, 9)
GREY = (90, 85, 75)
CARD = (255, 253, 245)
LAND = (196, 172, 120)
LAND2 = (170, 190, 150)
SEA = (214, 230, 238)

FONT_PATHS = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
]


def font(size, bold=True, serif=False):
    names = []
    if serif and bold:
        names = ["DejaVuSerif-Bold.ttf"]
    elif serif:
        names = ["DejaVuSerif.ttf"]
    elif bold:
        names = ["DejaVuSans-Bold.ttf"]
    else:
        names = ["DejaVuSans.ttf"]
    for base in ["/usr/share/fonts/truetype/dejavu/", "/usr/share/fonts/TTF/"]:
        for n in names:
            p = base + n
            if os.path.exists(p):
                return ImageFont.truetype(p, size)
    try:
        return ImageFont.load_default(size=size)
    except TypeError:
        return ImageFont.load_default()


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, text, fnt, fill, max_w, leading=None, max_lines=None):
    if leading is None:
        leading = int(fnt.size * 1.22)
    lines = wrap(draw, text, fnt, max_w)
    if max_lines:
        lines = lines[:max_lines]
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def badge(draw, x, y, n, fill=RED):
    r = 13
    draw.ellipse([x, y, x + 2 * r, y + 2 * r], fill=fill)
    f = font(15, bold=True)
    s = str(n)
    tw = draw.textlength(s, font=f)
    draw.text((x + r - tw / 2, y + r - 9), s, font=f, fill=(255, 255, 255))
    return x + 2 * r + 6


def draw_quake(d, x, y, w, h):
    # cracked building with window grid + seismograph line
    d.rectangle([x, y, x + w, y + h], fill=(235, 228, 205), outline=INK, width=2)
    bx, by, bw, bh = x + 28, y + 14, 92, h - 40
    d.rectangle([bx, by, bx + bw, by + bh], fill=(210, 180, 140), outline=INK, width=2)
    for r in range(4):
        for c in range(3):
            wx = bx + 10 + c * 28
            wy = by + 6 + r * 11
            d.rectangle([wx, wy, wx + 16, wy + 8], fill=(70, 90, 120), outline=INK)
    # crack
    pts = [(bx + 46, by), (bx + 38, by + 30), (bx + 52, by + 55), (bx + 40, by + 82), (bx + 50, by + bh)]
    d.line(pts, fill=RED, width=3)
    # ground + seismograph
    gy = y + h - 14
    d.line([(x + 8, gy), (x + w - 8, gy)], fill=INK, width=2)
    sx = x + 140
    wave = [(sx, gy - 4), (sx + 18, gy - 4), (sx + 26, gy - 26), (sx + 36, gy + 4),
            (sx + 46, gy - 34), (sx + 56, gy + 4), (sx + 66, gy - 16), (sx + 76, gy - 4),
            (sx + 110, gy - 4)]
    d.line(wave, fill=RED, width=3)
    d.text((x + 140, y + 8), "M6.7", font=font(28, bold=True), fill=RED)
    d.text((x + 140, y + 40), "00:09 UTC", font=font(13, bold=True), fill=INK)


def draw_cop(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(225, 236, 230), outline=INK, width=2)
    # conference table
    tx, ty = x + 26, y + h - 30
    d.rectangle([tx, ty, tx + w - 52, ty + 18], fill=(120, 85, 50), outline=INK, width=2)
    for i in range(5):
        cx = tx + 22 + i * ((w - 52) // 5)
        d.ellipse([cx, ty - 26, cx + 20, ty - 6], fill=(240, 205, 160), outline=INK)
        d.rectangle([cx + 2, ty - 6, cx + 18, ty], fill=NAVY, outline=INK)
    # thermometer
    thx = x + w - 52
    d.rounded_rectangle([thx, y + 12, thx + 18, y + h - 60], radius=8, fill=(255, 255, 255), outline=INK, width=2)
    d.rectangle([thx + 4, y + 30, thx + 14, y + h - 62], fill=RED)
    d.ellipse([thx - 3, y + h - 76, thx + 21, y + h - 52], fill=RED, outline=INK)
    d.text((x + 14, y + 8), "COP31 OVERTIME", font=font(17, bold=True), fill=TEAL)
    d.text((x + 14, y + 30), "Antalya talks", font=font(12, bold=False), fill=INK)


def draw_cricket(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(220, 235, 210), outline=INK, width=2)
    # pitch
    px = x + 30
    d.rectangle([px, y + 16, px + 70, y + h - 16], fill=(232, 214, 170), outline=INK, width=2)
    # stumps
    for i in range(3):
        sx = px + 26 + i * 10
        d.rectangle([sx, y + h - 44, sx + 6, y + h - 20], fill=GOLD, outline=INK)
    # bat
    d.polygon([(px + 8, y + h - 60), (px + 22, y + h - 60), (px + 34, y + 30), (px + 24, y + 24)], fill=(200, 160, 100), outline=INK)
    # ball
    d.ellipse([px + 44, y + 30, px + 62, y + 48], fill=RED, outline=INK)
    # scoreboard
    sbx = x + 118
    d.rectangle([sbx, y + 16, x + w - 14, y + 78], fill=NAVY, outline=INK, width=2)
    d.text((sbx + 10, y + 22), "IND 309/2", font=font(20, bold=True), fill=(255, 255, 255))
    d.text((sbx + 10, y + 48), "Rahul 117*", font=font(16, bold=True), fill=(255, 220, 120))


# Simplified continent polygons in 100x52 map space (x: lon-ish, y: lat-ish flipped)
CONTINENTS = [
    # North America
    [(3, 14), (8, 7), (17, 4), (26, 4), (30, 8), (29, 13), (31, 17), (27, 21), (23, 23), (20, 27), (17, 26), (14, 21), (9, 20), (4, 18)],
    # South America
    [(21, 28), (26, 27), (30, 30), (30, 36), (27, 43), (24, 47), (22, 41), (20, 34)],
    # Africa
    [(45, 23), (52, 21), (59, 24), (60, 31), (56, 39), (52, 44), (49, 38), (46, 30)],
    # Europe (kept separate from Asia)
    [(44, 9), (48, 5), (53, 5), (55, 8), (53, 12), (50, 11), (47, 13), (44, 12)],
    # Asia
    [(56, 6), (68, 3), (82, 3), (90, 6), (89, 12), (84, 15), (82, 21), (76, 25), (71, 21), (65, 19), (59, 17), (56, 11)],
    # SE Asia / Indonesia hint
    [(75, 27), (81, 27), (83, 30), (77, 31)],
    # Australia
    [(80, 33), (88, 32), (92, 36), (90, 42), (84, 43), (79, 38)],
]

PINS = [  # story no, map-x, map-y (100x52 space), label
    (1, 24.5, 36, "Peru"),
    (20, 20, 16, "US banks"),
    (29, 13, 15, "Nvidia"),
    (2, 55, 16, "Antalya"),
    (5, 48, 10, "Brussels"),
    (13, 53, 8, "Poland"),
    (4, 58, 10, "Kryvyi Rih"),
    (32, 62, 19, "Iran"),
    (6, 54, 40, "S. Africa"),
    (9, 71, 24, "Odisha"),
    (7, 84, 14, "APAC media"),
    (10, 85, 37, "Australia"),
    (3, 93, 44, "Wellington"),
    (11, 92, 39, "NZ vote"),
]


def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SEA, outline=INK, width=2)
    def mx(v):
        return x + v / 100.0 * w
    def my(v):
        return y + v / 52.0 * h
    fills = [LAND, LAND2, LAND, LAND2, LAND, LAND2, LAND]
    for i, poly in enumerate(CONTINENTS):
        pts = [(mx(px), my(py)) for px, py in poly]
        d.polygon(pts, fill=fills[i % len(fills)], outline=(120, 100, 60))
    # NZ islands
    d.ellipse([mx(90), my(39), mx(93), my(42)], fill=LAND, outline=(120, 100, 60))
    d.ellipse([mx(91.5), my(42.5), mx(94), my(45.5)], fill=LAND, outline=(120, 100, 60))
    for n, px, py, lab in PINS:
        cx, cy = mx(px), my(py)
        r = 11
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED, outline=(255, 255, 255), width=2)
        f = font(12, bold=True)
        s = str(n)
        tw = d.textlength(s, font=f)
        d.text((cx - tw / 2, cy - 8), s, font=f, fill=(255, 255, 255))
        lf = font(10, bold=True)
        lw2 = d.textlength(lab, font=lf)
        lx = cx + r + 2
        if lx + lw2 > x + w - 4:
            lx = cx - r - 2 - lw2
        d.text((lx, cy - 6), lab, font=lf, fill=INK)


def main():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W - 1, H - 1], outline=INK, width=3)

    # Masthead
    d.text((24, 10), "Saturday 21 November 2026", font=font(46, bold=True, serif=True), fill=INK)
    d.text((24, 64), "THE DAY IN ONE PICTURE  •  32 dated stories  •  World news, Saturday edition",
           font=font(15, bold=True), fill=GREY)
    d.line([(24, 88), (1000, 88)], fill=INK, width=2)
    d.rectangle([24, 92, 1000, 120], fill=RED)
    d.text((32, 98), "PERU QUAKE  •  COP31 RUNS INTO SATURDAY  •  RAHUL CENTURY IN WELLINGTON",
           font=font(16, bold=True), fill=(255, 255, 255))

    # Timeline
    d.rectangle([24, 126, 1000, 158], fill=CARD, outline=INK, width=1)
    d.text((32, 130), "UTC TIMELINE — SAT 21 NOV", font=font(12, bold=True), fill=NAVY)
    tl = "00:03 Russia NATO line  •  00:09 Peru M6.7  •  00:25 Melania wish  •  00:35 Ukraine barrage  •  01:06 Trump-Putin  •  01:12 Denmark expulsion  •  01:34 RAF Barnham"
    d.text((32, 144), tl, font=font(11, bold=False), fill=INK)

    # Region strip
    d.rectangle([24, 164, 1000, 190], fill=NAVY)
    d.text((32, 170), "EUROPE 12  •  AMERICAS 8  •  OCEANIA 4  •  ASIA-PACIFIC 3  •  WORLD 3  •  AFRICA 1  •  MIDEAST 1",
           font=font(14, bold=True), fill=(255, 255, 255))

    # Day in numbers
    nums = [("M6.7", "Peru quake"), ("42", "Kryvyi Rih hurt"), ("100k", "EU youth visas"),
            ("31%", "ANC vote"), ("310", "media members"), ("117*", "Rahul score"),
            ("A$604m", "Mayne deal"), ("+898", "Sensex pts")]
    bw = (1000 - 24 - 7 * 6) // 8
    for i, (big, small) in enumerate(nums):
        x = 24 + i * (bw + 6)
        d.rectangle([x, 196, x + bw, 238], fill=CARD, outline=INK, width=1)
        d.text((x + 8, 200), big, font=font(19, bold=True), fill=RED)
        d.text((x + 8, 222), small, font=font(10, bold=False), fill=INK)

    # Leads
    leads = [
        (1, "PERU SHAKEN AT 00:09 UTC", "M6.7 quake near Carhuamayo, 108 km deep. Felt in Lima; green alert, no damage reported.", draw_quake),
        (2, "COP31 MISSES ITS DEADLINE", "Antalya talks spill into Saturday. Draft drops fossil-fuel language; Panama threatens objection.", draw_cop),
        (3, "RAHUL HUNDRED, DAY 3", "India 309/2 chasing NZ 368 in Wellington. Rahul 117* leads fightback on Saturday.", draw_cricket),
    ]
    lw = (1000 - 24 - 2 * 10) // 3
    for i, (n, title, body, fn) in enumerate(leads):
        x = 24 + i * (lw + 10)
        y = 246
        d.rectangle([x, y, x + lw, y + 168], fill=CARD, outline=INK, width=2)
        fn(d, x + 10, y + 10, lw - 20, 92)
        tx = badge(d, x + 10, y + 108, n)
        text_block(d, tx, y + 108, title, font(15, bold=True), INK, x + lw - tx - 8, max_lines=2)
        text_block(d, x + 10, y + 136, body, font(11, bold=False), INK, lw - 20, max_lines=3)

    # Map
    d.text((24, 422), "WHERE IT HAPPENED — pins = story numbers", font=font(13, bold=True), fill=NAVY)
    draw_map(d, 24, 440, 976, 168)

    # Mid cards 4-13
    mids = [
        (4, "KRYVYI RIH AFTERMATH", "Fri strike toll: 2 dead, 42 hurt. Rescue today."),
        (5, "UK-EU DEAL FALLOUT", "Burnham: year of talks. Tuition row blocks start."),
        (6, "ANC SCRAMBLES FOR CITIES", "31% vote. Coalition deals due by 27 Nov."),
        (7, "310 MEDIA OUTLETS JOIN", "APAC partnership launches today, 41 countries."),
        (8, "WALL ST CORRECTION", "S&P in correction Fri; Sensex +898 defies rout."),
        (9, "AKVAN RAIN LINGERS", "Heavy rain N. Odisha today after Fri landfall."),
        (10, "STORMS + HEAT, AUSTRALIA", "NSW storms Sat; ex-Cat-5 Xavier fades."),
        (11, "NZ STILL UNCALLED", "7 Nov vote: 67 seats vs 66. Result 27 Nov."),
        (12, "DENMARK EXPULSION ROW", "Russia vows response over Kyivstoner plot claim."),
        (13, "NATO CHIEF TO WARSAW", "Rutte due Sat after Fri missile crashes."),
    ]
    mw = (1000 - 24 - 4 * 8) // 5
    for i, (n, title, body) in enumerate(mids):
        row, col = divmod(i, 5)
        x = 24 + col * (mw + 8)
        y = 616 + row * 84
        d.rectangle([x, y, x + mw, y + 78], fill=CARD, outline=INK, width=1)
        tx = badge(d, x + 6, y + 6, n, fill=NAVY)
        text_block(d, tx, y + 6, title, font(12, bold=True), INK, x + mw - tx - 6, max_lines=2)
        text_block(d, x + 6, y + 40, body, font(10, bold=False), INK, mw - 12, max_lines=3)

    # Briefs 14-32
    d.text((24, 788), "BRIEFS — numbered, dated today unless labelled", font=font(13, bold=True), fill=NAVY)
    briefs = [
        (14, "Russia overnight barrage hits Ukraine targets."),
        (15, "Moscow: no guarantees until Kyiv drops NATO."),
        (16, "Trump calls Putin friend; accuses Iran."),
        (17, "Melania wants Christmas ceasefire."),
        (18, "US court 9-8: 2022 proxy vote unconstitutional."),
        (19, "IndusInd sacks ex-CEO, seeks clawback."),
        (20, "Bank vendors hit by cyberattack; cores safe."),
        (21, "Hyundai Elantra debuts at LA Auto Show."),
        (22, "RAF Barnham village votes on leaving UK."),
        (23, "Migrant bail scams: $811m fines, abuse went on."),
        (24, "Mamdani: close Rikers Island by 2032."),
        (25, "NI doctors plan further strike over pay."),
        (26, "Cost-of-living protests continue Saturday."),
        (27, "French police sentenced for Zecler beating."),
        (28, "Depardieu investigated over allegations."),
        (29, "Trump urges Nvidia: reinstate Jensen Huang."),
        (30, "Pochettino begins at Man Utd; drone films it."),
        (31, "Mayne Pharma accepts A$604m takeover."),
        (32, "US sanctions 4 Iranians (filed Fri, reported today)."),
    ]
    colw = (1000 - 24 - 2 * 12) // 3
    per_col = 7
    for i, (n, txt) in enumerate(briefs):
        col = i // per_col
        row = i % per_col
        x = 24 + col * (colw + 12)
        y = 806 + row * 21
        d.text((x, y), f"{n}.", font=font(11, bold=True), fill=RED)
        text_block(d, x + 30, y, txt, font(11, bold=False), INK, colw - 30, max_lines=1)

    # Date check
    d.rectangle([24, 956, 1000, 1004], fill=(254, 226, 226), outline=RED, width=2)
    d.text((32, 960), "DATE CHECK — LEFT OUT ON PURPOSE (not 21 Nov news):", font=font(12, bold=True), fill=RED)
    dc = "ICJ Myanmar genocide ruling Thu 19 Nov  •  Shenzhen Trump-Xi-Putin summit Thu 19 Nov  •  Akvan landfall Fri 20 Nov  •  Poland missiles Fri 20 Nov  •  Palisades verdict Fri 20 Nov  •  Fiona hippo died Thu 19 Nov"
    text_block(d, 32, 977, dc, font(10, bold=False), INK, 960, leading=12, max_lines=2)

    d.text((24, 1008), "Sources: Reuters • AP • BBC • Al Jazeera • UN News • USGS • IMD • Xinhua • IANS.  All drawings original.",
           font=font(10, bold=False), fill=GREY)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, format="PNG", optimize=True)
    print(out)


if __name__ == "__main__":
    main()
