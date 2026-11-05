"""Placeholder seasonal backdrops for skin.marquee (user can replace them).

Usage: python3 gen_backdrops.py <skin_dir>
"""
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

SKIN = sys.argv[1]
W, H = 1920, 1080
OUT = os.path.join(SKIN, "extras", "seasons")


def vgrad(top, bottom, h=H, w=W, gamma=1.0):
    t = np.linspace(0, 1, h)[:, None, None] ** gamma
    a = np.array(top)[None, None, :]
    b = np.array(bottom)[None, None, :]
    arr = (a * (1 - t) + b * t).repeat(w, axis=1)
    return Image.fromarray(arr.astype(np.uint8), "RGB")


def glow(img, cx, cy, radius, color, strength=1.0):
    y, x = np.mgrid[0:H, 0:W]
    d = np.sqrt((x - cx) ** 2 + (y - cy) ** 2) / radius
    g = np.clip(np.exp(-d * d * 2.2) * strength, 0, 1)[..., None]
    base = np.asarray(img).astype(np.float32)
    col = np.array(color, np.float32)[None, None, :]
    out = base + (col - base) * g * 0.85
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8), "RGB")


def ridge(rng, y0, amp, rough, n=W + 1):
    xs = np.arange(n)
    y = np.full(n, float(y0))
    for k, a in ((1, amp), (3, amp * 0.5), (7, amp * rough), (17, amp * rough * 0.4)):
        ph = rng.uniform(0, 2 * math.pi)
        y += a * np.sin(xs / W * 2 * math.pi * k / 2 + ph)
    return y


def stars(draw, rng, count, ymax, alpha=200):
    for _ in range(count):
        x, y = rng.uniform(0, W), rng.uniform(0, ymax)
        r = rng.uniform(0.6, 1.8)
        a = int(rng.uniform(80, alpha))
        draw.ellipse((x - r, y - r, x + r, y + r), fill=(255, 255, 255, a))


def bare_tree(draw, x, y, length, angle, depth, width, color, rng):
    if depth == 0 or length < 6:
        return
    x2 = x + length * math.cos(angle)
    y2 = y - length * math.sin(angle)
    draw.line((x, y, x2, y2), fill=color, width=max(1, int(width)))
    n = 2 if depth > 2 else int(rng.integers(2, 4))
    for i in range(n):
        da = rng.uniform(0.25, 0.65) * (1 if i % 2 == 0 else -1)
        bare_tree(draw, x2, y2, length * rng.uniform(0.62, 0.8), angle + da, depth - 1, width * 0.68, color, rng)


def tombstone(draw, x, base, w, h, color, kind):
    if kind == 0:  # rounded top
        draw.rectangle((x, base - h + w / 2, x + w, base), fill=color)
        draw.ellipse((x, base - h, x + w, base - h + w), fill=color)
    elif kind == 1:  # cross
        t = w * 0.28
        draw.rectangle((x + w / 2 - t / 2, base - h, x + w / 2 + t / 2, base), fill=color)
        draw.rectangle((x, base - h * 0.72, x + w, base - h * 0.72 + t), fill=color)
    else:  # slab, slightly tilted
        pts = [(x, base), (x + w, base), (x + w * 1.08, base - h), (x + w * 0.08, base - h)]
        draw.polygon(pts, fill=color)


def halloween():
    rng = np.random.default_rng(31)
    img = vgrad((26, 10, 46), (6, 4, 12), gamma=0.9)
    img = glow(img, 1460, 300, 520, (90, 60, 120), 0.8)
    img = glow(img, 1460, 300, 180, (235, 230, 205), 1.0)
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    stars(d, rng, 160, 600)
    # moon
    d.ellipse((1460 - 135, 300 - 135, 1460 + 135, 300 + 135), fill=(244, 238, 214, 255))
    for _ in range(6):  # craters
        cx, cy, r = 1460 + rng.uniform(-80, 80), 300 + rng.uniform(-80, 80), rng.uniform(10, 26)
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(226, 220, 196, 255))
    img = Image.alpha_composite(img.convert("RGBA"), ov)
    # hills
    sil = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(sil)
    far = ridge(rng, 840, 30, 0.3)
    d.polygon([(0, H)] + [(x, far[x]) for x in range(W)] + [(W, H)], fill=(20, 12, 28, 255))
    near = ridge(rng, 930, 22, 0.2)
    col = (5, 3, 8, 255)
    d.polygon([(0, H)] + [(x, near[x]) for x in range(W)] + [(W, H)], fill=col)
    bare_tree(d, 1730, near[1730] + 6, 190, math.pi / 2 + 0.05, 8, 26, col, rng)
    bare_tree(d, 1050, near[1050] + 6, 110, math.pi / 2 - 0.08, 7, 14, col, rng)
    for i, x in enumerate(range(980, 1880, 95)):
        x += int(rng.uniform(-25, 25))
        w = rng.uniform(34, 56)
        h = rng.uniform(60, 110)
        tombstone(d, x, near[min(x, W - 1)] + 14, w, h, col, int(rng.integers(0, 3)))
    # bats
    for _ in range(5):
        bx, by, s = rng.uniform(1100, 1800), rng.uniform(120, 420), rng.uniform(10, 18)
        d.polygon([(bx - 2.2 * s, by - 0.6 * s), (bx - s, by), (bx - 0.5 * s, by - 0.3 * s), (bx, by + 0.2 * s),
                   (bx + 0.5 * s, by - 0.3 * s), (bx + s, by), (bx + 2.2 * s, by - 0.6 * s), (bx + 1.2 * s, by + 0.4 * s),
                   (bx, by + 0.7 * s), (bx - 1.2 * s, by + 0.4 * s)], fill=(8, 4, 10, 255))
    img = Image.alpha_composite(img, sil)
    return img.convert("RGB")


def thanksgiving():
    rng = np.random.default_rng(1126)
    img = vgrad((58, 30, 40), (150, 74, 26), gamma=1.3)
    img = glow(img, 1400, 820, 700, (255, 170, 70), 0.9)
    img = glow(img, 1400, 820, 160, (255, 226, 160), 1.0)
    img = img.convert("RGBA")
    sil = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(sil)
    for y0, amp, col in ((760, 50, (110, 50, 28, 255)), (840, 40, (72, 32, 20, 255)), (930, 30, (36, 16, 12, 255))):
        r = ridge(rng, y0, amp, 0.15)
        d.polygon([(0, H)] + [(x, r[x]) for x in range(W)] + [(W, H)], fill=col)
    # wheat / grass tufts on the nearest hill
    for x in range(900, 1920, 9):
        base = 930 + rng.uniform(-6, 30)
        h = rng.uniform(30, 80)
        lean = rng.uniform(-14, 14)
        d.line((x, base, x + lean, base - h), fill=(30, 14, 10, 255), width=2)
        d.ellipse((x + lean - 3, base - h - 10, x + lean + 3, base - h + 4), fill=(30, 14, 10, 255))
    img = Image.alpha_composite(img, sil)
    return img.convert("RGB")


def christmas():
    rng = np.random.default_rng(1225)
    img = vgrad((8, 18, 40), (4, 22, 18), gamma=1.0)
    img = glow(img, 1450, 380, 620, (40, 70, 120), 0.7)
    img = img.convert("RGBA")
    bok = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(bok)
    cols = [(255, 80, 80), (255, 210, 110), (120, 220, 140), (140, 180, 255)]
    for _ in range(70):
        x, y = rng.uniform(900, 1920), rng.uniform(40, 760)
        r = rng.uniform(10, 46)
        c = cols[int(rng.integers(0, 4))]
        d.ellipse((x - r, y - r, x + r, y + r), fill=c + (int(rng.uniform(40, 110)),))
    bok = bok.filter(ImageFilter.GaussianBlur(6))
    img = Image.alpha_composite(img, bok)
    sil = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(sil)
    stars(d, rng, 90, 500)
    r1 = ridge(rng, 880, 30, 0.2)
    d.polygon([(0, H)] + [(x, r1[x]) for x in range(W)] + [(W, H)], fill=(92, 108, 134, 255))
    r2 = ridge(rng, 960, 24, 0.2)
    d.polygon([(0, H)] + [(x, r2[x]) for x in range(W)] + [(W, H)], fill=(124, 140, 166, 255))
    for x in list(range(1000, 1900, 70)):
        x += int(rng.uniform(-20, 20))
        h = rng.uniform(140, 300)
        base = r1[min(x, W - 1)] + 10
        w = h * 0.42
        for k in range(4):
            t0 = base - h + k * h * 0.22
            hw = w * (0.35 + k * 0.22)
            d.polygon([(x, t0), (x - hw, t0 + h * 0.34), (x + hw, t0 + h * 0.34)], fill=(6, 30, 22, 255))
            d.polygon([(x, t0), (x - hw * 0.5, t0 + h * 0.16), (x + hw * 0.5, t0 + h * 0.16)], fill=(150, 168, 196, 200))
    img = Image.alpha_composite(img, sil)
    return img.convert("RGB")


def default():
    img = vgrad((20, 20, 20), (8, 8, 8))
    img = glow(img, 1650, 120, 900, (110, 12, 18), 0.75)
    img = glow(img, 300, 1100, 700, (40, 6, 10), 0.5)
    return img


def easter_bg():
    rng = np.random.default_rng(404)
    img = vgrad((52, 44, 92), (236, 170, 168), gamma=1.25)
    img = glow(img, 1430, 760, 620, (255, 214, 170), 0.9)
    img = glow(img, 1430, 760, 150, (255, 244, 214), 1.0)
    img = img.convert("RGBA")
    sil = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(sil)
    far = ridge(rng, 790, 40, 0.15)
    d.polygon([(0, H)] + [(x, far[x]) for x in range(W)] + [(W, H)], fill=(96, 120, 104, 255))
    # three crosses on the far hill, small and quiet
    for cx, h in ((1600, 118), (1545, 92), (1655, 92)):
        base = far[cx] + 4
        w = h * 0.09
        d.rectangle((cx - w / 2, base - h, cx + w / 2, base), fill=(58, 52, 70, 255))
        d.rectangle((cx - h * 0.28, base - h * 0.78, cx + h * 0.28, base - h * 0.78 + w), fill=(58, 52, 70, 255))
    near = ridge(rng, 905, 26, 0.15)
    d.polygon([(0, H)] + [(x, near[x]) for x in range(W)] + [(W, H)], fill=(70, 104, 76, 255))
    # tulips and pastel eggs in the grass on the right
    flower = [(246, 150, 190), (250, 236, 150), (196, 160, 236), (255, 255, 255)]
    for _ in range(70):
        x = rng.uniform(950, 1920)
        base = near[min(int(x), W - 1)] + rng.uniform(10, 120)
        hgt = rng.uniform(20, 50)
        d.line((x, base, x, base - hgt), fill=(54, 96, 60, 255), width=3)
        c = flower[int(rng.integers(0, len(flower)))]
        d.ellipse((x - 7, base - hgt - 12, x + 7, base - hgt + 4), fill=c + (255,))
    eggs = [(196, 160, 236), (143, 217, 182), (249, 180, 210), (255, 236, 150), (160, 200, 250)]
    for i, x in enumerate((1150, 1290, 1420, 1720, 1840)):
        y = near[x] + 70 + (i % 2) * 40
        c = eggs[i]
        d.ellipse((x - 22, y - 30, x + 22, y + 30), fill=c + (255,))
        d.line((x - 20, y - 4, x + 20, y - 4), fill=(255, 255, 255, 200), width=5)
    # Easter bunny sitting among the eggs
    bx, by = 1570, near[1570] + 112
    fur = (246, 240, 236, 255)
    d.ellipse((bx - 46, by - 70, bx + 46, by + 8), fill=fur)          # body
    d.ellipse((bx + 18, by - 104, bx + 70, by - 54), fill=fur)        # head
    d.ellipse((bx + 26, by - 178, bx + 44, by - 92), fill=fur)        # ears
    d.ellipse((bx + 46, by - 172, bx + 64, by - 90), fill=fur)
    d.ellipse((bx + 30, by - 166, bx + 40, by - 104), fill=(246, 190, 205, 255))
    d.ellipse((bx + 50, by - 160, bx + 60, by - 100), fill=(246, 190, 205, 255))
    d.ellipse((bx - 60, by - 40, bx - 30, by - 10), fill=(255, 255, 255, 255))  # tail
    d.ellipse((bx + 52, by - 86, bx + 59, by - 79), fill=(60, 50, 60, 255))     # eye
    img = Image.alpha_composite(img, sil)
    return img.convert("RGB")


def memorial_bg():
    rng = np.random.default_rng(530)
    img = vgrad((14, 22, 52), (186, 96, 60), gamma=1.5)
    img = glow(img, 1500, 860, 600, (240, 150, 90), 0.8)
    img = img.convert("RGBA")
    sil = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(sil)
    stars(d, rng, 60, 380, alpha=160)
    hill = ridge(rng, 800, 18, 0.1)
    d.polygon([(0, H)] + [(x, hill[x]) for x in range(W)] + [(W, H)], fill=(30, 40, 34, 255))
    # rows of white headstones in perspective, each with a tiny flag
    for row in range(5):
        t = row / 4
        y = 832 + (t ** 1.5) * 220
        sz = 9 + t * 30
        gap = sz * 3.4
        x = 960 - row * 60 + (row % 2) * gap / 2
        while x < W + 40:
            d.rectangle((x, y - sz * 1.15, x + sz, y), fill=(226, 228, 232, 255))
            d.ellipse((x, y - sz * 1.15 - sz * 0.5, x + sz, y - sz * 1.15 + sz * 0.5), fill=(226, 228, 232, 255))
            fx = x + sz * 1.25
            d.line((fx, y, fx, y - sz * 1.9), fill=(60, 60, 60, 255), width=max(1, int(sz / 12)))
            fw, fh = sz * 0.65, sz * 0.42
            for k in range(3):
                d.rectangle((fx, y - sz * 1.9 + k * fh / 3, fx + fw, y - sz * 1.9 + (k + 1) * fh / 3),
                            fill=(214, 40, 57, 255) if k != 1 else (245, 245, 245, 255))
            d.rectangle((fx, y - sz * 1.9, fx + fw * 0.4, y - sz * 1.9 + fh * 0.55), fill=(40, 70, 150, 255))
            x += gap
    img = Image.alpha_composite(img, sil)
    return img.convert("RGB")


def july4_bg():
    rng = np.random.default_rng(704)
    img = vgrad((6, 10, 34), (30, 26, 70), gamma=1.0)
    img = glow(img, 1450, 380, 700, (60, 50, 120), 0.6)
    img = img.convert("RGBA")
    sky = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(sky)
    stars(d, rng, 120, 700)
    # a few faint painted bursts (the live fireworks animate on top of these)
    for cx, cy, R, col in ((1250, 260, 170, (214, 60, 70)), (1650, 200, 140, (240, 240, 255)), (1450, 470, 120, (80, 130, 255))):
        for i in range(40):
            a = i / 40 * 2 * math.pi
            r1 = R * rng.uniform(0.6, 1.0)
            d.line((cx + math.cos(a) * R * 0.2, cy + math.sin(a) * R * 0.2, cx + math.cos(a) * r1, cy + math.sin(a) * r1),
                   fill=col + (90,), width=3)
    sky = sky.filter(ImageFilter.GaussianBlur(1.2))
    img = Image.alpha_composite(img, sky)
    sil = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(sil)
    x = 700
    while x < W:  # city skyline
        w = rng.uniform(40, 110)
        h = rng.uniform(80, 300)
        d.rectangle((x, 1080 - 150 - h, x + w, 1080), fill=(10, 10, 22, 255))
        for wy in range(int(1080 - 150 - h + 12), 1080 - 160, 22):
            for wx in range(int(x + 8), int(x + w - 8), 16):
                if rng.uniform() < 0.25:
                    d.rectangle((wx, wy, wx + 6, wy + 9), fill=(255, 214, 140, 170))
        x += w + rng.uniform(2, 14)
    d.rectangle((0, 1080 - 150, W, H), fill=(8, 8, 18, 255))
    img = Image.alpha_composite(img, sil)
    return img.convert("RGB")


def newyear_bg():
    rng = np.random.default_rng(101)
    img = vgrad((6, 8, 22), (26, 22, 48), gamma=1.0)
    img = glow(img, 1500, 300, 650, (90, 70, 40), 0.55)
    img = img.convert("RGBA")
    bok = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(bok)
    for _ in range(60):
        x, y, r = rng.uniform(900, 1920), rng.uniform(30, 700), rng.uniform(8, 40)
        c = [(240, 206, 106), (255, 240, 200), (201, 209, 224)][int(rng.integers(0, 3))]
        d.ellipse((x - r, y - r, x + r, y + r), fill=c + (int(rng.uniform(30, 90)),))
    img = Image.alpha_composite(img, bok.filter(ImageFilter.GaussianBlur(5)))
    sil = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(sil)
    stars(d, rng, 80, 500)
    x = 760
    while x < W:
        w, h = rng.uniform(50, 120), rng.uniform(120, 360)
        if 1440 < x < 1560:
            w, h = 120, 520  # the tower the ball sits on
        d.rectangle((x, 1080 - 120 - h, x + w, 1080), fill=(8, 8, 18, 255))
        for wy in range(int(1080 - 120 - h + 12), 1080 - 130, 22):
            for wx in range(int(x + 8), int(x + w - 8), 16):
                if rng.uniform() < 0.3:
                    d.rectangle((wx, wy, wx + 6, wy + 9), fill=(255, 220, 150, 160))
        x += w + rng.uniform(2, 12)
    d.rectangle((0, 960, W, H), fill=(6, 6, 14, 255))
    img = Image.alpha_composite(img, sil)
    return img.convert("RGB")


def valentine_bg():
    rng = np.random.default_rng(214)
    img = vgrad((40, 8, 24), (110, 20, 52), gamma=1.1)
    img = glow(img, 1450, 420, 700, (220, 70, 120), 0.65)
    img = img.convert("RGBA")
    bok = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(bok)
    for _ in range(55):
        x, y, r = rng.uniform(850, 1920), rng.uniform(20, 1000), rng.uniform(10, 46)
        c = [(255, 160, 190), (255, 220, 230), (230, 80, 120)][int(rng.integers(0, 3))]
        d.ellipse((x - r, y - r, x + r, y + r), fill=c + (int(rng.uniform(30, 80)),))
    img = Image.alpha_composite(img, bok.filter(ImageFilter.GaussianBlur(7)))
    hearts = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hd = ImageDraw.Draw(hearts)
    for cx, cy, sz, a in ((1480, 430, 520, 120), (1260, 640, 260, 90), (1760, 700, 220, 80)):
        pts = []
        for i in range(200):
            t = i / 200 * 2 * math.pi
            px = 16 * math.sin(t) ** 3
            py = 13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)
            pts.append((cx + px * sz / 34, cy - py * sz / 34))
        hd.polygon(pts, fill=(255, 120, 160, a))
    img = Image.alpha_composite(img, hearts.filter(ImageFilter.GaussianBlur(3)))
    return img.convert("RGB")


def stpatrick_bg():
    rng = np.random.default_rng(317)
    img = vgrad((40, 70, 110), (170, 200, 190), gamma=1.2)
    img = img.convert("RGBA")
    rb = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(rb)
    cols = [(230, 70, 70), (240, 150, 60), (245, 220, 90), (90, 190, 100), (70, 130, 220), (130, 90, 190)]
    for i, c in enumerate(cols):  # rainbow arc
        r = 640 - i * 26
        d.arc((1420 - r, 900 - r, 1420 + r, 900 + r), 180, 360, fill=c + (120,), width=26)
    img = Image.alpha_composite(img, rb.filter(ImageFilter.GaussianBlur(4)))
    sil = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(sil)
    for y0, amp, col in ((780, 50, (60, 140, 80, 255)), (860, 40, (40, 115, 62, 255)), (950, 28, (28, 90, 48, 255))):
        r = ridge(rng, y0, amp, 0.15)
        d.polygon([(0, H)] + [(x, r[x]) for x in range(W)] + [(W, H)], fill=col)
    # pot of gold at the rainbow's end
    px, py = 1820, 905
    d.ellipse((px - 70, py - 30, px + 70, py + 80), fill=(24, 24, 28, 255))
    d.rectangle((px - 76, py - 34, px + 76, py - 18), fill=(40, 40, 46, 255))
    for _ in range(40):
        gx, gy = px + rng.uniform(-62, 62), py - 30 - rng.uniform(0, 34)
        d.ellipse((gx - 10, gy - 6, gx + 10, gy + 6), fill=(250, 205, 70, 255), outline=(200, 150, 30, 255))
    img = Image.alpha_composite(img, sil)
    return img.convert("RGB")


def ship(d, x, base, s, col, sail_col=None, flag=None):
    """Simple sailing-ship silhouette; s = scale (1 ~ 300px wide)."""
    sail_col = sail_col or col
    d.polygon([(x - 150 * s, base - 30 * s), (x + 150 * s, base - 30 * s), (x + 115 * s, base + 18 * s), (x - 110 * s, base + 18 * s)], fill=col)
    d.polygon([(x + 150 * s, base - 30 * s), (x + 190 * s, base - 48 * s), (x + 150 * s, base - 22 * s)], fill=col)
    for mx, h in ((x - 70 * s, 190), (x + 10 * s, 230), (x + 85 * s, 170)):
        d.line((mx, base - 30 * s, mx, base - (30 + h) * s), fill=col, width=max(2, int(5 * s)))
        for k, (w, top) in enumerate(((52, 0.28), (60, 0.55), (66, 0.82))):
            ty = base - (30 + h * (1 - top + 0.22)) * s
            d.polygon([(mx - w * s, ty), (mx + w * s, ty), (mx + w * 1.08 * s, ty + 50 * s), (mx - w * 1.08 * s, ty + 50 * s)], fill=sail_col)
    if flag:
        fx, fy = x + 10 * s, base - 262 * s
        d.rectangle((fx, fy, fx + 46 * s, fy + 30 * s), fill=flag)


def water(img, y0, top, bottom, rng, glint=None):
    d = ImageDraw.Draw(img)
    for y in range(y0, H):
        t = (y - y0) / max(1, H - y0)
        c = tuple(int(top[i] * (1 - t) + bottom[i] * t) for i in range(3))
        d.line((0, y, W, y), fill=c + (255,))
    if glint:
        gx, gc = glint
        for _ in range(140):
            y = rng.uniform(y0 + 4, H)
            w = rng.uniform(10, 60) * (1 + (y - y0) / 300)
            x = gx + rng.normal(0, 60 + (y - y0) * 0.5)
            d.line((x - w, y, x + w, y), fill=gc + (int(rng.uniform(60, 150)),), width=2)


def mlk_bg():
    rng = np.random.default_rng(115)
    img = vgrad((30, 36, 78), (238, 176, 102), gamma=1.3)
    img = glow(img, 1460, 760, 640, (255, 214, 140), 0.9)
    img = glow(img, 1460, 760, 150, (255, 240, 200), 1.0)
    img = img.convert("RGBA")
    sil = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(sil)
    for y0, amp, rough, col in ((700, 120, 0.5, (60, 56, 92, 255)), (790, 70, 0.35, (40, 38, 66, 255)), (880, 30, 0.2, (24, 24, 40, 255))):
        r = ridge(rng, y0, amp, rough)
        d.polygon([(0, H)] + [(x, r[x]) for x in range(W)] + [(W, H)], fill=col)
    d.polygon([(1380, 880), (1540, 880), (1900, H), (1020, H)], fill=(52, 50, 70, 255))  # road to the horizon
    for k in range(6):
        y = 900 + k * 30
        d.rectangle((1455 + (y - 880) * 0.05, y, 1465 + (y - 880) * 0.07, y + 14), fill=(230, 200, 120, 255))
    img = Image.alpha_composite(img, sil)
    return img.convert("RGB")


def presidents_bg():
    rng = np.random.default_rng(222)
    img = vgrad((14, 22, 56), (120, 84, 110), gamma=1.3)
    img = glow(img, 1450, 720, 600, (210, 150, 130), 0.6)
    img = img.convert("RGBA")
    d = ImageDraw.Draw(img)
    stars(d, rng, 70, 400)
    water(img, 860, (60, 50, 80), (12, 12, 26), rng, glint=(1450, (240, 230, 220)))
    sil = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(sil)
    wc = (226, 224, 230, 255)
    cx = 1450
    d.pieslice((cx - 150, 430, cx + 150, 730), 180, 360, fill=wc)
    d.rectangle((cx - 12, 380, cx + 12, 440), fill=wc)
    d.rectangle((cx - 190, 570, cx + 190, 600), fill=wc)
    d.polygon([(cx - 330, 660), (cx, 600), (cx + 330, 660)], fill=wc)
    for i in range(10):
        x = cx - 300 + i * 64
        d.rectangle((x, 664, x + 22, 830), fill=wc)
    d.rectangle((cx - 350, 830, cx + 350, 860), fill=wc)
    d.rectangle((cx - 410, 760, cx - 350, 860), fill=(200, 198, 206, 255))
    d.rectangle((cx + 350, 760, cx + 410, 860), fill=(200, 198, 206, 255))
    img = Image.alpha_composite(img, sil)
    # soft reflection
    refl = sil.crop((0, 380, W, 860)).transpose(Image.FLIP_TOP_BOTTOM).filter(ImageFilter.GaussianBlur(4))
    refl.putalpha(refl.getchannel("A").point(lambda a: a * 0.25))
    img.alpha_composite(refl.crop((0, 0, W, 220)), (0, 860))
    return img.convert("RGB")


def mothers_bg():
    rng = np.random.default_rng(510)
    img = vgrad((92, 58, 92), (246, 196, 206), gamma=1.2)
    img = glow(img, 1450, 380, 620, (255, 230, 236), 0.7)
    img = img.convert("RGBA")
    bok = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(bok)
    for _ in range(50):
        x, y, r = rng.uniform(850, 1920), rng.uniform(20, 760), rng.uniform(12, 50)
        c = [(255, 200, 220), (255, 240, 246), (220, 190, 245)][int(rng.integers(0, 3))]
        d.ellipse((x - r, y - r, x + r, y + r), fill=c + (int(rng.uniform(30, 80)),))
    img = Image.alpha_composite(img, bok.filter(ImageFilter.GaussianBlur(7)))
    fl = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(fl)
    d.rectangle((0, 880, W, H), fill=(76, 120, 82, 255))
    cols = [(244, 120, 160), (250, 196, 210), (201, 160, 240), (255, 236, 150), (240, 90, 120)]
    for _ in range(140):
        x = rng.uniform(820, 1940)
        base = rng.uniform(900, 1100)
        h = rng.uniform(60, 160)
        d.line((x, base, x, base - h), fill=(60, 110, 66, 255), width=4)
        c = cols[int(rng.integers(0, 5))]
        sz = rng.uniform(14, 24)
        top = base - h
        d.polygon([(x - sz, top - sz * 0.6), (x - sz * 0.5, top - sz * 0.1), (x, top - sz * 1.1), (x + sz * 0.5, top - sz * 0.1),
                   (x + sz, top - sz * 0.6), (x + sz, top + sz * 0.5), (x - sz, top + sz * 0.5)], fill=c + (255,))
    img = Image.alpha_composite(img, fl)
    return img.convert("RGB")


def juneteenth_bg():
    rng = np.random.default_rng(619)
    img = vgrad((12, 26, 78), (34, 44, 110), gamma=1.0)
    img = img.convert("RGBA")
    d = ImageDraw.Draw(img)
    stars(d, rng, 90, 700)
    # arc horizon in red, like the Juneteenth flag
    d.ellipse((-600, 820, W + 1200, 2200), fill=(178, 34, 52, 255))
    cx, cy = 1450, 560
    burst = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bd = ImageDraw.Draw(burst)
    pts = []
    for i in range(24):
        a = -math.pi / 2 + i * math.pi / 12
        rr = 230 if i % 2 == 0 else 170
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    bd.polygon(pts, outline=(255, 255, 255, 230), width=10)
    sp = []
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5
        rr = 120 if i % 2 == 0 else 50
        sp.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    bd.polygon(sp, fill=(255, 255, 255, 255))
    img = Image.alpha_composite(img, burst.filter(ImageFilter.GaussianBlur(1)))
    img = Image.alpha_composite(img, glow(Image.new("RGB", (W, H), (0, 0, 0)), cx, cy, 300, (255, 255, 255), 0.25).convert("RGBA").point(lambda v: v) if False else img)
    return img.convert("RGB")


def fathers_bg():
    rng = np.random.default_rng(621)
    img = vgrad((40, 60, 96), (230, 190, 140), gamma=1.4)
    img = glow(img, 1500, 760, 520, (255, 214, 160), 0.8)
    img = img.convert("RGBA")
    sil = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(sil)
    tr = ridge(rng, 740, 22, 0.6)
    d.polygon([(0, 790)] + [(x, tr[x]) for x in range(W)] + [(W, 790)], fill=(36, 50, 52, 255))
    for x in range(0, W, 26):  # pine tops along the shore
        h = rng.uniform(20, 70)
        d.polygon([(x, tr[min(x, W - 1)] - h), (x - 14, tr[min(x, W - 1)] + 6), (x + 14, tr[min(x, W - 1)] + 6)], fill=(30, 44, 46, 255))
    img = Image.alpha_composite(img, sil)
    water(img, 790, (120, 120, 130), (30, 40, 60), rng, glint=(1500, (255, 220, 170)))
    sil = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(sil)
    k = (20, 22, 30, 255)
    d.rectangle((1150, 930, 1920, 952), fill=k)  # dock
    for x in range(1180, 1920, 120):
        d.rectangle((x, 952, x + 12, 1080), fill=k)
    d.polygon([(1280, 905), (1460, 905), (1430, 935), (1310, 935)], fill=k)  # boat
    d.ellipse((1352, 838, 1376, 862), fill=k)  # dad
    d.rectangle((1354, 862, 1374, 905), fill=k)
    d.line((1374, 870, 1520, 760), fill=k, width=4)  # rod
    d.line((1520, 760, 1540, 905), fill=(20, 22, 30, 160), width=1)
    img = Image.alpha_composite(img, sil)
    return img.convert("RGB")


def labor_bg():
    rng = np.random.default_rng(901)
    img = vgrad((52, 40, 90), (250, 150, 80), gamma=1.3)
    img = glow(img, 1500, 800, 560, (255, 200, 120), 0.9)
    img = img.convert("RGBA")
    water(img, 820, (200, 120, 90), (40, 30, 60), rng, glint=(1500, (255, 210, 150)))
    sil = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(sil)
    k = (22, 18, 28, 255)
    d.polygon([(800, H), (800, 960)] + [(x, 960 - 25 * math.sin((x - 800) / 300)) for x in range(800, W + 1, 20)] + [(W, H)], fill=k)
    d.rectangle((1180, 900, 1420, 914), fill=k)  # picnic table
    for x in (1200, 1390):
        d.line((x, 914, x - 18, 970), fill=k, width=8)
        d.line((x, 914, x + 18, 970), fill=k, width=8)
    d.ellipse((1560, 880, 1640, 920), fill=k)  # grill
    d.line((1600, 920, 1580, 975), fill=k, width=5)
    d.line((1600, 920, 1620, 975), fill=k, width=5)
    for i in range(3):  # smoke
        d.ellipse((1590 + i * 12, 840 - i * 40, 1620 + i * 12, 866 - i * 40), fill=(220, 210, 220, 60))
    d.line((900, 600, 900, 980), fill=k, width=8)  # string lights between two poles
    d.line((1880, 600, 1880, 980), fill=k, width=8)
    for t in np.linspace(0, 1, 26):
        x = 900 + t * 980
        y = 610 + math.sin(t * math.pi) * 110
        d.ellipse((x - 6, y - 6, x + 6, y + 6), fill=(255, 226, 150, 255))
    img = Image.alpha_composite(img, sil)
    glowl = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glowl)
    for t in np.linspace(0, 1, 26):
        x = 900 + t * 980
        y = 610 + math.sin(t * math.pi) * 110
        gd.ellipse((x - 18, y - 18, x + 18, y + 18), fill=(255, 220, 140, 90))
    img = Image.alpha_composite(img, glowl.filter(ImageFilter.GaussianBlur(8)))
    return img.convert("RGB")


def pirate_bg():
    rng = np.random.default_rng(919)
    img = vgrad((8, 12, 30), (24, 36, 60), gamma=1.0)
    img = glow(img, 1650, 230, 420, (90, 100, 140), 0.6)
    img = img.convert("RGBA")
    d = ImageDraw.Draw(img)
    stars(d, rng, 110, 600)
    d.ellipse((1590, 170, 1710, 290), fill=(238, 232, 210, 255))
    water(img, 840, (30, 44, 70), (6, 10, 22), rng, glint=(1650, (220, 220, 200)))
    sil = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(sil)
    ship(d, 1350, 860, 1.25, (8, 10, 16, 255), sail_col=(20, 24, 34, 255), flag=(8, 10, 16, 255))
    # skull on the flag
    fx, fy = 1350 + 10 * 1.25, 860 - 262 * 1.25
    d.rectangle((fx, fy, fx + 46 * 1.25, fy + 30 * 1.25), fill=(14, 14, 18, 255))
    d.ellipse((fx + 20, fy + 6, fx + 38, fy + 22), fill=(230, 226, 214, 255))
    img = Image.alpha_composite(img, sil)
    return img.convert("RGB")


def columbus_bg():
    rng = np.random.default_rng(1012)
    img = vgrad((40, 70, 120), (242, 186, 120), gamma=1.4)
    img = glow(img, 1500, 780, 520, (255, 220, 160), 0.85)
    img = img.convert("RGBA")
    water(img, 800, (110, 120, 150), (20, 40, 70), rng, glint=(1500, (255, 220, 170)))
    sil = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(sil)
    for x, base, sc in ((1180, 820, 0.55), (1790, 826, 0.62), (1480, 850, 0.9)):
        ship(d, x, base, sc, (30, 30, 44, 255), sail_col=(60, 58, 70, 255))
    img = Image.alpha_composite(img, sil)
    return img.convert("RGB")


def veterans_bg():
    rng = np.random.default_rng(1111)
    img = vgrad((26, 36, 70), (232, 168, 120), gamma=1.4)
    img = glow(img, 1350, 820, 600, (255, 210, 160), 0.8)
    img = img.convert("RGBA")
    sil = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(sil)
    r = ridge(rng, 900, 18, 0.1)
    d.polygon([(0, H)] + [(x, r[x]) for x in range(W)] + [(W, H)], fill=(24, 30, 32, 255))
    px = 1480
    d.rectangle((px, 260, px + 12, r[px] + 10), fill=(200, 200, 205, 255))
    d.ellipse((px - 6, 248, px + 18, 272), fill=(232, 194, 90, 255))
    # waving flag
    fw, fh = 380, 220
    for i in range(13):
        for x in range(0, fw, 4):
            wave = 12 * math.sin(x / 60.0)
            y0 = 270 + i * fh / 13 + wave
            d.rectangle((px + 12 + x, y0, px + 16 + x, y0 + fh / 13 + 1),
                        fill=(200, 30, 50, 255) if i % 2 == 0 else (240, 240, 244, 255))
    for x in range(0, int(fw * 0.42), 4):
        wave = 12 * math.sin(x / 60.0)
        d.rectangle((px + 12 + x, 270 + wave, px + 16 + x, 270 + fh * 7 / 13 + wave), fill=(40, 62, 130, 255))
    for row in range(5):
        for col in range(6):
            x = int(fw * 0.42 * (col + 0.5) / 6)
            y = 270 + 12 * math.sin(x / 60.0) + fh * 7 / 13 * (row + 0.5) / 5
            d.ellipse((px + 12 + x - 3, y - 3, px + 12 + x + 3, y + 3), fill=(255, 255, 255, 255))
    img = Image.alpha_composite(img, sil)
    return img.convert("RGB")


def groundhog_bg():
    rng = np.random.default_rng(202)
    img = vgrad((22, 34, 64), (226, 176, 150), gamma=1.25)
    img = glow(img, 1560, 700, 560, (255, 214, 170), 0.9)
    img = img.convert("RGBA")
    sil = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(sil)
    # far hills with bare trees
    far = ridge(rng, 690, 26, 0.15)
    d.polygon([(0, H)] + [(x, far[x]) for x in range(W)] + [(W, H)], fill=(96, 104, 140, 255))
    for _ in range(46):
        x = int(rng.uniform(700, W - 10))
        h_ = rng.uniform(40, 120)
        y0 = far[x] + 4
        d.line((x, y0, x, y0 - h_), fill=(62, 66, 96, 255), width=3)
        for j in range(4):
            yy = y0 - h_ * (0.45 + j * 0.13)
            dx = rng.uniform(10, 26) * (1 if j % 2 else -1)
            d.line((x, yy, x + dx, yy - rng.uniform(10, 22)), fill=(62, 66, 96, 255), width=2)
    # snowfield
    near = ridge(rng, 820, 14, 0.1)
    snow = np.zeros((H, W, 4), np.uint8)
    for y in range(H):
        t = (y - 760) / (H - 760)
        snow[y, :, :3] = np.array((170, 182, 214)) * (1 - 0.35 * max(0, t)) 
        snow[y, :, 3] = 255
    mask = Image.new("L", (W, H), 0)
    ImageDraw.Draw(mask).polygon([(0, H)] + [(x, near[x]) for x in range(W)] + [(W, H)], fill=255)
    sil.paste(Image.fromarray(snow, "RGBA"), (0, 0), mask)
    d = ImageDraw.Draw(sil)
    gx, gy = 1500, int(near[1500]) + 50
    # long shadow stretching away from the sunrise
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).polygon([(gx - 30, gy + 6), (gx - 420, gy + 40), (gx - 440, gy + 62), (gx + 30, gy + 14)],
                                   fill=(60, 70, 110, 150))
    sil = Image.alpha_composite(sil, shadow.filter(ImageFilter.GaussianBlur(6)))
    d = ImageDraw.Draw(sil)
    # burrow mound and hole
    d.ellipse((gx - 120, gy - 24, gx + 120, gy + 40), fill=(150, 158, 190, 255))
    d.ellipse((gx - 58, gy - 12, gx + 58, gy + 18), fill=(40, 34, 40, 255))
    # the groundhog, half out of its burrow: squat pear body, flat wide head, tiny ears, buck teeth
    fur, dark, light = (104, 74, 50, 255), (70, 48, 34, 255), (168, 136, 104, 255)
    d.ellipse((gx - 52, gy - 96, gx + 52, gy + 30), fill=fur)            # body
    d.ellipse((gx - 40, gy - 140, gx + 40, gy - 82), fill=fur)           # head (wider than tall)
    d.ellipse((gx - 38, gy - 140, gx - 24, gy - 128), fill=dark)         # ears
    d.ellipse((gx + 24, gy - 140, gx + 38, gy - 128), fill=dark)
    d.ellipse((gx - 22, gy - 116, gx + 22, gy - 88), fill=light)         # muzzle
    d.ellipse((gx - 6, gy - 116, gx + 6, gy - 108), fill=(30, 20, 18, 255))      # nose
    d.rectangle((gx - 5, gy - 100, gx + 5, gy - 88), fill=(240, 236, 220, 255))  # buck teeth
    d.line((gx, gy - 100, gx, gy - 88), fill=light, width=1)
    d.ellipse((gx - 24, gy - 126, gx - 15, gy - 117), fill=(20, 14, 12, 255))    # eyes
    d.ellipse((gx + 15, gy - 126, gx + 24, gy - 117), fill=(20, 14, 12, 255))
    d.ellipse((gx - 30, gy - 70, gx - 10, gy - 54), fill=dark)                   # paws at the chest
    d.ellipse((gx + 10, gy - 70, gx + 30, gy - 54), fill=dark)
    # front lip of the burrow hides the bottom of the body
    d.chord((gx - 120, gy - 24, gx + 120, gy + 40), 0, 180, fill=(150, 158, 190, 255))
    d.arc((gx - 58, gy - 12, gx + 58, gy + 18), 0, 180, fill=(40, 34, 40, 255), width=6)
    img = Image.alpha_composite(img, sil)
    # keep the left third dark for text
    arr = np.asarray(img.convert("RGB")).astype(np.float32)
    xs = np.linspace(0, 1, W)[None, :, None]
    arr *= np.clip(0.45 + xs * 1.2, 0.45, 1.0)
    return Image.fromarray(arr.astype(np.uint8), "RGB")


for name, fn in (("halloween", halloween), ("thanksgiving", thanksgiving), ("christmas", christmas), ("default", default),
                 ("easter", easter_bg), ("memorial", memorial_bg), ("july4", july4_bg),
                 ("newyear", newyear_bg), ("valentine", valentine_bg), ("stpatrick", stpatrick_bg),
                 ("mlk", mlk_bg), ("presidents", presidents_bg), ("mothers", mothers_bg), ("juneteenth", juneteenth_bg),
                 ("fathers", fathers_bg), ("labor", labor_bg), ("pirate", pirate_bg), ("columbus", columbus_bg),
                 ("veterans", veterans_bg), ("groundhog", groundhog_bg)):
    os.makedirs(os.path.join(OUT, name), exist_ok=True)
    fn().save(os.path.join(OUT, name, "marquee_%s.jpg" % name), quality=90)
    print("wrote", name)
