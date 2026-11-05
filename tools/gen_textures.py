"""Generate all procedural textures for skin.marquee.

Usage: python3 gen_textures.py <skin_dir> <fonts_dir>
"""
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

SKIN = sys.argv[1]
FONTS = sys.argv[2]
MEDIA = os.path.join(SKIN, "media", "marquee")
os.makedirs(MEDIA, exist_ok=True)
rng = np.random.default_rng(1031)


def save(img, name):
    path = os.path.join(MEDIA, name)
    img.save(path, optimize=True)
    return path


# ---------------------------------------------------------------- noise utils
def periodic_fbm(h, w, beta=2.2, seed=0, low_cut=1.0):
    """Noise that tiles seamlessly in both axes (FFT-filtered white noise)."""
    r = np.random.default_rng(seed)
    white = r.standard_normal((h, w))
    fy = np.fft.fftfreq(h)[:, None] * h
    fx = np.fft.fftfreq(w)[None, :] * w
    # stretch horizontally so fog forms long banks rather than blobs
    f = np.sqrt((fx / 1.9) ** 2 + (fy * 1.0) ** 2)
    f[0, 0] = 1.0
    amp = 1.0 / np.power(np.maximum(f, low_cut), beta / 2.0)
    amp[0, 0] = 0.0
    spec = np.fft.fft2(white) * amp
    n = np.real(np.fft.ifft2(spec))
    n = (n - n.min()) / (n.max() - n.min())
    return n


def fog_layer(w, h, seed, density_profile, contrast=2.2, threshold=0.35, rgb=(232, 238, 236)):
    n = periodic_fbm(h, w, beta=3.4, seed=seed)
    n2 = periodic_fbm(h, w, beta=2.4, seed=seed + 7)
    n = 0.85 * n + 0.15 * n2
    n = np.clip((n - threshold) / (1 - threshold), 0, 1)
    n = n ** (1.0 / contrast) * n  # soften but keep holes
    y = np.linspace(0, 1, h)[:, None]
    prof = density_profile(y)
    a = np.clip(n * prof, 0, 1)
    a = (a / max(a.max(), 1e-6)) * 255
    img = np.zeros((h, w, 4), np.uint8)
    img[..., 0] = rgb[0]
    img[..., 1] = rgb[1]
    img[..., 2] = rgb[2]
    img[..., 3] = a.astype(np.uint8)
    im = Image.fromarray(img, "RGBA")
    # wrap-safe blur: pad horizontally with wrapped content, blur, crop
    pad = 80
    big = Image.new("RGBA", (w + 2 * pad, h))
    big.paste(im, (pad, 0))
    big.paste(im.crop((w - pad, 0, w, h)), (0, 0))
    big.paste(im.crop((0, 0, pad, h)), (w + pad, 0))
    big = big.filter(ImageFilter.GaussianBlur(14))
    return big.crop((pad, 0, pad + w, h))


def smoothstep(e0, e1, x):
    t = np.clip((x - e0) / (e1 - e0), 0, 1)
    return t * t * (3 - 2 * t)


# fog that hugs the ground (bottom of screen)
save(fog_layer(2048, 640, 11, lambda y: smoothstep(0.0, 0.75, y) * 1.0), "fog_ground.png")
# a looser, mid-height bank that drifts across the rows
save(fog_layer(2048, 560, 23, lambda y: np.sin(np.clip(y, 0, 1) * math.pi) ** 1.2, threshold=0.38),
     "fog_bank.png")
# thin wisps that roll over the top menu
save(fog_layer(2048, 360, 37, lambda y: np.sin(np.clip(y, 0, 1) * math.pi) ** 1.4, threshold=0.45, contrast=1.6),
     "fog_wisp.png")


# ------------------------------------------------------------------ snow
def snow_layer(w, h, count, rmin, rmax, blur, seed, alpha=(150, 255)):
    r = np.random.default_rng(seed)
    im = Image.new("RGBA", (w, h), (255, 255, 255, 0))
    d = ImageDraw.Draw(im)
    for _ in range(count):
        x, y = r.uniform(0, w), r.uniform(0, h)
        rad = r.uniform(rmin, rmax)
        a = int(r.uniform(*alpha))
        for dx in (-w, 0, w):
            for dy in (-h, 0, h):
                d.ellipse((x + dx - rad, y + dy - rad, x + dx + rad, y + dy + rad), fill=(255, 255, 255, a))
    return im.filter(ImageFilter.GaussianBlur(blur))


save(snow_layer(1920, 1080, 260, 1.5, 3.2, 0.8, 5), "snow_small.png")
save(snow_layer(1920, 1080, 70, 3.5, 6.5, 1.6, 6, alpha=(120, 220)), "snow_large.png")


# ------------------------------------------------------------------ leaves
def leaf_shape(size, color, angle, seed):
    r = np.random.default_rng(seed)
    s = size
    im = Image.new("RGBA", (s * 2, s * 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    cx, cy = s, s
    pts = []
    lobes = 5
    for i in range(lobes * 2 * 6 + 1):
        t = i / (lobes * 2 * 6) * 2 * math.pi
        lobe = 0.62 + 0.38 * abs(math.cos(lobes * t / 2))
        jag = 1 + 0.06 * math.sin(t * 22 + r.uniform(0, 1))
        rr = s * 0.48 * lobe * jag
        pts.append((cx + rr * math.sin(t), cy - rr * math.cos(t) * 0.95))
    d.polygon(pts, fill=color)
    dark = tuple(max(0, c - 60) for c in color[:3]) + (255,)
    d.line((cx, cy + s * 0.15, cx, cy + s * 0.75), fill=dark, width=max(2, s // 18))
    for a in (-50, 0, 50):
        ang = math.radians(a)
        d.line((cx, cy + s * 0.15, cx + math.sin(ang) * s * 0.4, cy + s * 0.15 - math.cos(ang) * s * 0.4),
               fill=dark, width=max(1, s // 26))
    return im.rotate(angle, resample=Image.BICUBIC)


def leaves_layer(w, h, count, seed):
    r = np.random.default_rng(seed)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    palette = [(196, 82, 26), (224, 132, 36), (168, 52, 32), (232, 176, 58), (140, 70, 30)]
    for i in range(count):
        size = int(r.uniform(18, 40))
        col = palette[int(r.integers(0, len(palette)))] + (230,)
        leaf = leaf_shape(size, col, r.uniform(0, 360), seed * 100 + i)
        x, y = int(r.uniform(0, w)), int(r.uniform(0, h))
        for dx in (-w, 0, w):
            for dy in (-h, 0, h):
                im.paste(leaf, (x + dx - size, y + dy - size), leaf)  # PIL clips out-of-bounds
    return im


save(leaves_layer(1920, 1080, 22, 3), "leaves.png")

# ----------------------------------------------------------- UI primitives
def rounded_mask(w, h, r, name):
    sc = 4
    im = Image.new("L", (w * sc, h * sc), 0)
    ImageDraw.Draw(im).rounded_rectangle((0, 0, w * sc - 1, h * sc - 1), r * sc, fill=255)
    im = im.resize((w, h), Image.LANCZOS)
    out = Image.new("RGBA", (w, h), (255, 255, 255, 0))
    out.putalpha(im)
    save(out, name)


rounded_mask(64, 64, 14, "rounded_fill.png")     # 9-slice background (border=16)
rounded_mask(220, 330, 10, "mask_poster.png")
rounded_mask(384, 216, 10, "mask_landscape.png")
rounded_mask(260, 260, 10, "mask_square.png")
rounded_mask(64, 8, 4, "underline.png")


def rounded_ring(size, r, thick, name):
    sc = 4
    im = Image.new("L", (size * sc, size * sc), 0)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, size * sc - 1, size * sc - 1), r * sc, fill=255)
    d.rounded_rectangle((thick * sc, thick * sc, size * sc - 1 - thick * sc, size * sc - 1 - thick * sc),
                        max(1, (r - thick)) * sc, fill=0)
    im = im.resize((size, size), Image.LANCZOS)
    out = Image.new("RGBA", (size, size), (255, 255, 255, 0))
    out.putalpha(im)
    save(out, name)


rounded_ring(64, 16, 5, "focus_ring.png")  # 9-slice border=20


def gradient(w, h, axis, stops, name):
    """stops: list of (pos 0..1, alpha 0..255) along axis ('x' or 'y'); black."""
    n = w if axis == "x" else h
    t = np.linspace(0, 1, n)
    pos = [s[0] for s in stops]
    al = [s[1] for s in stops]
    a = np.interp(t, pos, al)
    # ease for nicer falloff
    arr = np.zeros((h, w, 4), np.uint8)
    if axis == "x":
        arr[..., 3] = a[None, :].astype(np.uint8)
    else:
        arr[..., 3] = a[:, None].astype(np.uint8)
    save(Image.fromarray(arr, "RGBA"), name)


gradient(1200, 32, "x", [(0, 255), (0.3, 235), (0.62, 120), (1, 0)], "grad_left.png")
gradient(32, 700, "y", [(0, 0), (0.45, 150), (0.8, 240), (1, 255)], "grad_bottom.png")
gradient(32, 260, "y", [(0, 230), (0.5, 120), (1, 0)], "grad_top.png")
gradient(32, 200, "y", [(0, 0), (1, 220)], "grad_tile.png")

# ------------------------------------------------------------ season icons
def icon_canvas(s=256):
    return Image.new("RGBA", (s, s), (0, 0, 0, 0))


def draw_pumpkin(s=256):
    sc = 4
    im = Image.new("RGBA", (s * sc, s * sc), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    S = s * sc
    body = [(0.18, 0.30, 0.52, 0.92), (0.48, 0.30, 0.82, 0.92), (0.30, 0.26, 0.70, 0.94)]
    cols = [(214, 98, 18, 255), (214, 98, 18, 255), (240, 128, 32, 255)]
    for (x0, y0, x1, y1), c in zip(body, cols):
        d.ellipse((x0 * S, y0 * S, x1 * S, y1 * S), fill=c)
    d.rounded_rectangle((0.47 * S, 0.14 * S, 0.56 * S, 0.33 * S), 0.03 * S, fill=(74, 96, 40, 255))
    # face
    fc = (255, 214, 92, 255)
    d.polygon([(0.33 * S, 0.52 * S), (0.43 * S, 0.52 * S), (0.38 * S, 0.43 * S)], fill=fc)
    d.polygon([(0.57 * S, 0.52 * S), (0.67 * S, 0.52 * S), (0.62 * S, 0.43 * S)], fill=fc)
    d.polygon([(0.30 * S, 0.66 * S), (0.70 * S, 0.66 * S), (0.62 * S, 0.80 * S), (0.56 * S, 0.74 * S),
               (0.50 * S, 0.81 * S), (0.44 * S, 0.74 * S), (0.38 * S, 0.80 * S)], fill=fc)
    return im.resize((s, s), Image.LANCZOS)


def draw_leaf_icon(s=256):
    leaf = leaf_shape(s // 2 * 2, (222, 112, 30, 255), 0, 77)
    return leaf.resize((s, s), Image.LANCZOS)


def draw_tree(s=256):
    sc = 4
    S = s * sc
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    g = (36, 140, 72, 255)
    for top, bot, half in ((0.16, 0.46, 0.20), (0.30, 0.64, 0.28), (0.46, 0.84, 0.36)):
        d.polygon([(0.5 * S, top * S), ((0.5 - half) * S, bot * S), ((0.5 + half) * S, bot * S)], fill=g)
    d.rectangle((0.45 * S, 0.84 * S, 0.55 * S, 0.95 * S), fill=(110, 70, 40, 255))
    # star
    cx, cy, R = 0.5 * S, 0.13 * S, 0.09 * S
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = R if i % 2 == 0 else R * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=(255, 214, 92, 255))
    r = np.random.default_rng(9)
    for _ in range(14):
        y = r.uniform(0.32, 0.8)
        half = 0.20 + (y - 0.3) * 0.32
        x = 0.5 + r.uniform(-half * 0.7, half * 0.7)
        c = [(230, 50, 50, 255), (255, 214, 92, 255), (90, 170, 255, 255)][int(r.integers(0, 3))]
        d.ellipse(((x - 0.022) * S, (y - 0.022) * S, (x + 0.022) * S, (y + 0.022) * S), fill=c)
    return im.resize((s, s), Image.LANCZOS)


def draw_play(s=256):
    sc = 4
    S = s * sc
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.polygon([(0.3 * S, 0.2 * S), (0.3 * S, 0.8 * S), (0.8 * S, 0.5 * S)], fill=(255, 255, 255, 255))
    return im.resize((s, s), Image.LANCZOS)


save(draw_pumpkin(), "icon_halloween.png")
save(draw_leaf_icon(), "icon_thanksgiving.png")
save(draw_tree(), "icon_christmas.png")
save(draw_play(), "icon_default.png")


# ------------------------------------------------------------- wordmark
def wordmark(text, name, h=120):
    f = ImageFont.truetype(os.path.join(FONTS, "ofl_bebasneue_BebasNeue-Regular.ttf"), h)
    bbox = f.getbbox(text)
    w = bbox[2] - bbox[0] + 20
    hh = bbox[3] - bbox[1] + 20
    im = Image.new("RGBA", (w, hh), (255, 255, 255, 0))
    d = ImageDraw.Draw(im)
    d.text((10 - bbox[0], 10 - bbox[1]), text, font=f, fill=(255, 255, 255, 255))
    save(im, name)


wordmark("MARQUEE", "wordmark.png")
print("textures done")


def menu_focus(name):
    # 64x64: transparent, with a rounded 5px bar along the bottom (9-slice border 24,0,24,0)
    sc = 4
    im = Image.new("L", (64 * sc, 64 * sc), 0)
    ImageDraw.Draw(im).rounded_rectangle((14 * sc, 54 * sc, 50 * sc - 1, 59 * sc), 2.5 * sc, fill=255)
    im = im.resize((64, 64), Image.LANCZOS)
    out = Image.new("RGBA", (64, 64), (255, 255, 255, 0))
    out.putalpha(im)
    save(out, name)


menu_focus("menu_focus.png")
print("menu focus done")


# ---------------------------------------------------------- July fireworks
def burst(color, seed, name, size=512):
    r = np.random.default_rng(seed)
    sc = 2
    S = size * sc
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    cx = cy = S / 2
    rays = 52
    head = tuple(min(255, c + 70) for c in color)
    for i in range(rays):
        ang = i / rays * 2 * math.pi + r.uniform(-0.05, 0.05)
        L = S * 0.46 * r.uniform(0.55, 1.0)
        # streak fading toward the centre, drawn as short segments with rising alpha
        segs = 14
        for k in range(segs):
            t0, t1 = 0.25 + 0.75 * k / segs, 0.25 + 0.75 * (k + 1) / segs
            a = int(255 * (k + 1) / segs * 0.85)
            d.line((cx + math.cos(ang) * L * t0, cy + math.sin(ang) * L * t0,
                    cx + math.cos(ang) * L * t1, cy + math.sin(ang) * L * t1), fill=color + (a,), width=3 * sc)
        hx, hy = cx + math.cos(ang) * L, cy + math.sin(ang) * L
        rad = r.uniform(2.5, 5) * sc
        d.ellipse((hx - rad, hy - rad, hx + rad, hy + rad), fill=head + (255,))
        for j in range(3):  # a few drooping sparks trailing each star
            tx, ty = hx + r.uniform(-6, 6) * sc, hy + (j + 1) * r.uniform(6, 11) * sc
            rr = rad * (0.6 - j * 0.15)
            d.ellipse((tx - rr, ty - rr, tx + rr, ty + rr), fill=head + (int(200 - j * 55),))
    for _ in range(90):  # sparkle dust
        ang, rr = r.uniform(0, 2 * math.pi), S * 0.46 * math.sqrt(r.uniform(0.05, 1))
        x, y, rad = cx + math.cos(ang) * rr, cy + math.sin(ang) * rr, r.uniform(1, 3) * sc
        d.ellipse((x - rad, y - rad, x + rad, y + rad), fill=color + (int(r.uniform(120, 230)),))
    glow = im.filter(ImageFilter.GaussianBlur(10 * sc))
    out = Image.alpha_composite(glow, im).resize((size, size), Image.LANCZOS)
    save(out, name)


burst((235, 50, 64), 1, "burst_red.png")
burst((245, 245, 255), 2, "burst_white.png")
burst((80, 130, 255), 3, "burst_blue.png")
burst((255, 205, 90), 4, "burst_gold.png")

tr = Image.new("RGBA", (8, 140), (255, 255, 255, 0))
for y in range(140):
    a = int(255 * (1 - y / 139) ** 1.6)
    for x in range(8):
        edge = 1 - abs(x - 3.5) / 4
        tr.putpixel((x, y), (255, 235, 200, int(a * edge)))
save(tr, "trail.png")


# ------------------------------------------------------------ Easter petals
def petals_layer(w, h, count, seed):
    r = np.random.default_rng(seed)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    palette = [(250, 190, 215), (255, 240, 248), (215, 190, 245), (255, 220, 235), (200, 235, 215)]
    for i in range(count):
        s = int(r.uniform(12, 24))
        p = Image.new("RGBA", (s * 3, s * 3), (0, 0, 0, 0))
        pd = ImageDraw.Draw(p)
        col = palette[int(r.integers(0, len(palette)))]
        pd.polygon([(s * 1.5, s * 0.5), (s * 2.2, s * 1.4), (s * 1.9, s * 2.3), (s * 1.5, s * 2.5),
                    (s * 1.1, s * 2.3), (s * 0.8, s * 1.4)], fill=col + (235,))
        pd.line((s * 1.5, s * 0.9, s * 1.5, s * 2.2), fill=tuple(max(0, c - 25) for c in col) + (150,), width=max(1, s // 10))
        p = p.rotate(r.uniform(0, 360), resample=Image.BICUBIC).filter(ImageFilter.GaussianBlur(0.6))
        x, y = int(r.uniform(0, w)), int(r.uniform(0, h))
        for dx in (-w, 0, w):
            for dy in (-h, 0, h):
                im.paste(p, (x + dx - s, y + dy - s), p)
    return im


save(petals_layer(1920, 1080, 34, 9), "petals.png")


# --------------------------------------------------------------- new icons
def draw_egg(s=256):
    sc = 4
    S = s * sc
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    mask = Image.new("L", (S, S), 0)
    md_ = ImageDraw.Draw(mask)
    md_.ellipse((0.24 * S, 0.08 * S, 0.76 * S, 0.94 * S), fill=255)
    body = Image.new("RGBA", (S, S), (249, 180, 210, 255))
    bd = ImageDraw.Draw(body)
    bands = [(0.30, (201, 160, 240)), (0.46, (143, 217, 182)), (0.62, (255, 236, 150)), (0.76, (201, 160, 240))]
    for y, c in bands:
        pts = [(x / 40 * S, (y + 0.025 * math.sin(x / 40 * 2 * math.pi * 4)) * S) for x in range(41)]
        bd.line(pts, fill=c + (255,), width=int(0.055 * S))
    for x, y in ((0.40, 0.38), (0.58, 0.38), (0.50, 0.54), (0.42, 0.70), (0.60, 0.70)):
        bd.ellipse(((x - 0.02) * S, (y - 0.02) * S, (x + 0.02) * S, (y + 0.02) * S), fill=(255, 255, 255, 255))
    im.paste(body, (0, 0), mask)
    return im.resize((s, s), Image.LANCZOS)


def draw_poppy(s=256):
    sc = 4
    S = s * sc
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for i in range(4):
        ang = i * math.pi / 2 + math.pi / 4
        cx, cy = 0.5 * S + math.cos(ang) * 0.17 * S, 0.5 * S + math.sin(ang) * 0.17 * S
        d.ellipse((cx - 0.24 * S, cy - 0.24 * S, cx + 0.24 * S, cy + 0.24 * S), fill=(214, 40, 57, 255))
    d.ellipse((0.36 * S, 0.36 * S, 0.64 * S, 0.64 * S), fill=(30, 20, 22, 255))
    d.ellipse((0.45 * S, 0.45 * S, 0.55 * S, 0.55 * S), fill=(70, 120, 60, 255))
    return im.resize((s, s), Image.LANCZOS)


def draw_flag(s=256):
    sc = 4
    S = s * sc
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    x0, y0, x1, y1 = 0.06 * S, 0.22 * S, 0.94 * S, 0.78 * S
    sh = (y1 - y0) / 13
    for i in range(13):
        d.rectangle((x0, y0 + i * sh, x1, y0 + (i + 1) * sh), fill=(214, 40, 57, 255) if i % 2 == 0 else (250, 250, 250, 255))
    cw, ch = (x1 - x0) * 0.42, sh * 7
    d.rectangle((x0, y0, x0 + cw, y0 + ch), fill=(40, 70, 150, 255))
    for row in range(4):
        for col in range(5):
            sx, sy = x0 + cw * (col + 0.5) / 5, y0 + ch * (row + 0.5) / 4
            d.ellipse((sx - 0.012 * S, sy - 0.012 * S, sx + 0.012 * S, sy + 0.012 * S), fill=(255, 255, 255, 255))
    return im.resize((s, s), Image.LANCZOS)


save(draw_egg(), "icon_easter.png")
save(draw_poppy(), "icon_memorial.png")
save(draw_flag(), "icon_july4.png")
print("holiday textures done")


# ------------------------------------------------- Valentine / St. Patrick / New Year
def heart_shape(size, color, alpha=230):
    sc = 4
    S = size * sc
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    pts = []
    for i in range(200):
        t = i / 200 * 2 * math.pi
        x = 16 * math.sin(t) ** 3
        y = 13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)
        pts.append((S / 2 + x * S / 36, S / 2 - y * S / 36 - S * 0.02))
    d.polygon(pts, fill=color + (alpha,))
    return im.resize((size, size), Image.LANCZOS)


def scatter_layer(w, h, count, seed, maker, smin, smax, rotate=True, blur=0):
    r = np.random.default_rng(seed)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    for i in range(count):
        s = int(r.uniform(smin, smax))
        p = maker(s, r)
        if rotate:
            p = p.rotate(r.uniform(-35, 35) if rotate == "small" else r.uniform(0, 360), resample=Image.BICUBIC, expand=True)
        if blur:
            p = p.filter(ImageFilter.GaussianBlur(blur))
        x, y = int(r.uniform(0, w)), int(r.uniform(0, h))
        for dx in (-w, 0, w):
            for dy in (-h, 0, h):
                im.paste(p, (x + dx - p.size[0] // 2, y + dy - p.size[1] // 2), p)
    return im


HEART_COLS = [(232, 69, 122), (244, 112, 154), (255, 182, 200), (214, 40, 70), (255, 230, 236)]
save(scatter_layer(1920, 1080, 30, 14, lambda s, r: heart_shape(s, HEART_COLS[int(r.integers(0, 5))], int(r.uniform(150, 230))),
                   18, 46, rotate="small", blur=0.4), "hearts.png")


def shamrock(size, r):
    sc = 4
    S = size * sc
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    green = [(46, 168, 79), (76, 201, 110), (32, 130, 60)][int(r.integers(0, 3))]
    ImageDraw.Draw(im).line((S / 2, S / 2, S * 0.62, S * 0.95), fill=green + (255,), width=int(S * 0.05))
    for k in range(3):
        ang = -math.pi / 2 + k * 2 * math.pi / 3
        h = heart_shape(int(S * 0.5), green, 240).rotate(-math.degrees(ang) - 90, resample=Image.BICUBIC)
        cx, cy = S / 2 + math.cos(ang) * S * 0.2, S / 2 + math.sin(ang) * S * 0.2
        im.paste(h, (int(cx - h.size[0] / 2), int(cy - h.size[1] / 2)), h)
    return im.resize((size, size), Image.LANCZOS)


save(scatter_layer(1920, 1080, 24, 17, shamrock, 26, 50), "shamrocks.png")


def confetti_piece(s, r):
    cols = [(232, 194, 90), (240, 206, 106), (201, 209, 224), (255, 255, 255), (214, 170, 70)]
    c = cols[int(r.integers(0, 5))]
    im = Image.new("RGBA", (s * 2, s * 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    if r.uniform() < 0.6:
        d.rectangle((s * 0.6, s * 0.85, s * 1.4, s * 1.15), fill=c + (235,))
    else:
        d.ellipse((s * 0.75, s * 0.75, s * 1.25, s * 1.25), fill=c + (235,))
    return im


save(scatter_layer(1920, 1080, 240, 21, confetti_piece, 6, 10), "confetti_small.png")
save(scatter_layer(1920, 1080, 70, 22, confetti_piece, 12, 18), "confetti_large.png")


def crystal_ball(size=240):
    sc = 2
    S = size * sc
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    glow = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    ImageDraw.Draw(glow).ellipse((S * 0.08, S * 0.08, S * 0.92, S * 0.92), fill=(255, 225, 140, 170))
    glow = glow.filter(ImageFilter.GaussianBlur(S * 0.06))
    im.alpha_composite(glow)
    ball = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    bd = ImageDraw.Draw(ball)
    r = np.random.default_rng(31)
    R = S * 0.36
    cx = cy = S / 2
    rows = 9
    for i in range(rows):  # faceted tiles in latitude bands
        lat0, lat1 = -math.pi / 2 + i * math.pi / rows, -math.pi / 2 + (i + 1) * math.pi / rows
        cols = max(3, int(14 * math.cos((lat0 + lat1) / 2)))
        for j in range(cols):
            lo0, lo1 = -math.pi / 2 + j * math.pi / cols, -math.pi / 2 + (j + 1) * math.pi / cols
            pts = [(cx + R * math.cos(la) * math.sin(lo), cy + R * math.sin(la)) for la, lo in ((lat0, lo0), (lat0, lo1), (lat1, lo1), (lat1, lo0))]
            shade = r.uniform(0.72, 1.0)
            tint = [(255, 250, 235), (255, 226, 150), (235, 240, 255), (255, 255, 255)][int(r.integers(0, 4))]
            bd.polygon(pts, fill=tuple(int(c * shade) for c in tint) + (255,), outline=(120, 110, 90, 255))
    ball = ball.filter(ImageFilter.GaussianBlur(0.8))
    im.alpha_composite(ball)
    hl = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    ImageDraw.Draw(hl).ellipse((cx - R * 0.55, cy - R * 0.7, cx - R * 0.05, cy - R * 0.25), fill=(255, 255, 255, 120))
    im.alpha_composite(hl.filter(ImageFilter.GaussianBlur(S * 0.02)))
    return im.resize((size, size), Image.LANCZOS)


save(crystal_ball(), "ball.png")


def draw_heart_icon(s=256):
    return heart_shape(s, (232, 69, 122), 255)


def draw_shamrock_icon(s=256):
    return shamrock(s, np.random.default_rng(1))


def draw_ball_icon(s=256):
    return crystal_ball(s)


save(draw_heart_icon(), "icon_valentine.png")
save(draw_shamrock_icon(), "icon_stpatrick.png")
save(draw_ball_icon(), "icon_newyear.png")
print("more holiday textures done")


# ------------------------------------------------------------ more holiday icons
def _canvas(s=256):
    sc = 4
    S = s * sc
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    return im, ImageDraw.Draw(im), S


def _star_pts(cx, cy, R, r_in=0.42, n=5, rot=-math.pi / 2):
    pts = []
    for i in range(n * 2):
        ang = rot + i * math.pi / n
        rr = R if i % 2 == 0 else R * r_in
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    return pts


def icon_sunrise(s=256):
    im, d, S = _canvas(s)
    for i in range(9):
        a = math.pi + i * math.pi / 8
        d.line((S / 2 + math.cos(a) * S * 0.24, S * 0.66 + math.sin(a) * S * 0.24,
                S / 2 + math.cos(a) * S * 0.42, S * 0.66 + math.sin(a) * S * 0.42), fill=(240, 210, 122, 255), width=int(S * 0.035))
    d.pieslice((S * 0.28, S * 0.44, S * 0.72, S * 0.88), 180, 360, fill=(240, 196, 90, 255))
    d.rectangle((S * 0.12, S * 0.66, S * 0.88, S * 0.70), fill=(240, 210, 122, 255))
    return im.resize((s, s), Image.LANCZOS)


def icon_star_circle(s=256, bg=(61, 90, 168), fg=(255, 255, 255), ring=(200, 16, 46)):
    im, d, S = _canvas(s)
    d.ellipse((S * 0.06, S * 0.06, S * 0.94, S * 0.94), fill=ring + (255,))
    d.ellipse((S * 0.13, S * 0.13, S * 0.87, S * 0.87), fill=bg + (255,))
    d.polygon(_star_pts(S / 2, S * 0.52, S * 0.3), fill=fg + (255,))
    return im.resize((s, s), Image.LANCZOS)


def icon_tulip(s=256):
    im, d, S = _canvas(s)
    d.line((S * 0.5, S * 0.5, S * 0.5, S * 0.95), fill=(70, 140, 80, 255), width=int(S * 0.04))
    d.ellipse((S * 0.5, S * 0.62, S * 0.78, S * 0.74), fill=(80, 160, 90, 255))
    d.polygon([(S * 0.30, S * 0.22), (S * 0.40, S * 0.36), (S * 0.50, S * 0.16), (S * 0.60, S * 0.36), (S * 0.70, S * 0.22),
               (S * 0.70, S * 0.44), (S * 0.62, S * 0.56), (S * 0.38, S * 0.56), (S * 0.30, S * 0.44)], fill=(244, 120, 160, 255))
    return im.resize((s, s), Image.LANCZOS)


def icon_burst_star(s=256):
    im, d, S = _canvas(s)
    d.polygon(_star_pts(S / 2, S / 2, S * 0.46, r_in=0.72, n=12), outline=(255, 255, 255, 255), width=int(S * 0.025))
    d.polygon(_star_pts(S / 2, S * 0.52, S * 0.26), fill=(255, 255, 255, 255))
    d.ellipse((S * 0.0, S * 0.0, S, S), outline=(211, 58, 58, 255), width=int(S * 0.03))
    return im.resize((s, s), Image.LANCZOS)


def icon_tie(s=256):
    im, d, S = _canvas(s)
    d.polygon([(S * 0.40, S * 0.08), (S * 0.60, S * 0.08), (S * 0.56, S * 0.22), (S * 0.44, S * 0.22)], fill=(60, 100, 170, 255))
    d.polygon([(S * 0.44, S * 0.22), (S * 0.56, S * 0.22), (S * 0.66, S * 0.78), (S * 0.50, S * 0.94), (S * 0.34, S * 0.78)],
              fill=(74, 120, 184, 255))
    for k in range(4):
        y = S * (0.34 + k * 0.13)
        d.line((S * 0.42, y + S * 0.04, S * 0.60, y - S * 0.04), fill=(200, 160, 96, 255), width=int(S * 0.025))
    return im.resize((s, s), Image.LANCZOS)


def icon_hammer(s=256):
    im, d, S = _canvas(s)
    hd = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    h = ImageDraw.Draw(hd)
    h.rounded_rectangle((S * 0.46, S * 0.28, S * 0.54, S * 0.92), radius=S * 0.03, fill=(196, 140, 80, 255))
    h.rounded_rectangle((S * 0.24, S * 0.14, S * 0.76, S * 0.32), radius=S * 0.03, fill=(150, 160, 175, 255))
    h.polygon([(S * 0.76, S * 0.14), (S * 0.86, S * 0.10), (S * 0.86, S * 0.20), (S * 0.76, S * 0.24)], fill=(150, 160, 175, 255))
    hd = hd.rotate(-35, resample=Image.BICUBIC)
    im.alpha_composite(hd)
    return im.resize((s, s), Image.LANCZOS)


def icon_skull(s=256):
    im, d, S = _canvas(s)
    w = (240, 236, 224, 255)
    for a, b in (((S * 0.14, S * 0.62), (S * 0.86, S * 0.92)), ((S * 0.14, S * 0.92), (S * 0.86, S * 0.62))):
        d.line((a, b), fill=w, width=int(S * 0.07))
        for p in (a, b):
            d.ellipse((p[0] - S * 0.05, p[1] - S * 0.05, p[0] + S * 0.05, p[1] + S * 0.05), fill=w)
    d.ellipse((S * 0.26, S * 0.08, S * 0.74, S * 0.56), fill=w)
    d.rounded_rectangle((S * 0.36, S * 0.46, S * 0.64, S * 0.66), radius=S * 0.04, fill=w)
    k = (30, 24, 24, 255)
    d.ellipse((S * 0.34, S * 0.26, S * 0.46, S * 0.40), fill=k)
    d.ellipse((S * 0.54, S * 0.26, S * 0.66, S * 0.40), fill=k)
    d.polygon([(S * 0.50, S * 0.42), (S * 0.46, S * 0.50), (S * 0.54, S * 0.50)], fill=k)
    for x in (0.42, 0.50, 0.58):
        d.line((S * x, S * 0.56, S * x, S * 0.65), fill=k, width=int(S * 0.015))
    return im.resize((s, s), Image.LANCZOS)


def icon_compass(s=256):
    im, d, S = _canvas(s)
    d.ellipse((S * 0.06, S * 0.06, S * 0.94, S * 0.94), outline=(232, 194, 90, 255), width=int(S * 0.035))
    c = S / 2
    for i in range(8):
        a = -math.pi / 2 + i * math.pi / 4
        L = S * (0.40 if i % 2 == 0 else 0.25)
        p = (c + math.cos(a) * L, c + math.sin(a) * L)
        l = (c + math.cos(a - 0.5) * S * 0.07, c + math.sin(a - 0.5) * S * 0.07)
        r = (c + math.cos(a + 0.5) * S * 0.07, c + math.sin(a + 0.5) * S * 0.07)
        d.polygon([l, p, r, (c, c)], fill=((232, 194, 90, 255) if i % 2 == 0 else (120, 170, 210, 255)))
    return im.resize((s, s), Image.LANCZOS)


def icon_medal(s=256):
    im, d, S = _canvas(s)
    d.polygon([(S * 0.30, S * 0.04), (S * 0.46, S * 0.04), (S * 0.56, S * 0.40), (S * 0.40, S * 0.40)], fill=(61, 90, 168, 255))
    d.polygon([(S * 0.54, S * 0.04), (S * 0.70, S * 0.04), (S * 0.60, S * 0.40), (S * 0.44, S * 0.40)], fill=(214, 40, 57, 255))
    d.ellipse((S * 0.24, S * 0.36, S * 0.76, S * 0.88), fill=(232, 194, 90, 255))
    d.polygon(_star_pts(S / 2, S * 0.63, S * 0.18), fill=(255, 244, 200, 255))
    return im.resize((s, s), Image.LANCZOS)


save(icon_sunrise(), "icon_mlk.png")
def icon_capitol(s=256):
    im, d, S = _canvas(s)
    wcol = (236, 236, 242, 255)
    d.pieslice((S * 0.30, S * 0.14, S * 0.70, S * 0.54), 180, 360, fill=wcol)          # dome
    d.rectangle((S * 0.47, S * 0.06, S * 0.53, S * 0.16), fill=wcol)                    # lantern
    d.rectangle((S * 0.26, S * 0.34, S * 0.74, S * 0.40), fill=wcol)                    # drum base
    d.polygon([(S * 0.10, S * 0.52), (S * 0.50, S * 0.40), (S * 0.90, S * 0.52)], fill=wcol)  # pediment
    for i in range(6):                                                                  # columns
        x = S * (0.16 + i * 0.136)
        d.rectangle((x, S * 0.54, x + S * 0.05, S * 0.82), fill=wcol)
    d.rectangle((S * 0.08, S * 0.82, S * 0.92, S * 0.90), fill=wcol)
    d.rectangle((S * 0.30, S * 0.88, S * 0.70, S * 0.94), fill=(61, 90, 168, 255))
    return im.resize((s, s), Image.LANCZOS)


save(icon_capitol(), "icon_presidents.png")
save(icon_tulip(), "icon_mothers.png")
save(icon_burst_star(), "icon_juneteenth.png")
save(icon_tie(), "icon_fathers.png")
save(icon_hammer(), "icon_labor.png")
save(icon_skull(), "icon_pirate.png")
save(icon_compass(), "icon_columbus.png")
save(icon_medal(), "icon_veterans.png")
print("icons for 9 holidays done")


def icon_custom(s=256):
    """Generic 'your own holiday' icon: a four-point sparkle with two small ones."""
    im, d, S = _canvas(s)
    def sparkle(cx, cy, R, col):
        d.polygon(_star_pts(cx, cy, R, r_in=0.22, n=4, rot=-math.pi / 2), fill=col)
    sparkle(S * 0.44, S * 0.54, S * 0.40, (255, 255, 255, 255))
    sparkle(S * 0.80, S * 0.20, S * 0.15, (255, 214, 120, 255))
    sparkle(S * 0.82, S * 0.80, S * 0.10, (255, 214, 120, 255))
    return im.resize((s, s), Image.LANCZOS)


save(icon_custom(), "icon_custom.png")


def icon_groundhog(s=256):
    """Groundhog face: wide brown head, small ears, pale muzzle, buck teeth."""
    im, d, S = _canvas(s)
    fur, dark, light = (150, 104, 66, 255), (98, 66, 44, 255), (226, 196, 160, 255)
    d.ellipse((S * 0.12, S * 0.10, S * 0.32, S * 0.30), fill=dark)           # ears
    d.ellipse((S * 0.68, S * 0.10, S * 0.88, S * 0.30), fill=dark)
    d.ellipse((S * 0.06, S * 0.16, S * 0.94, S * 0.90), fill=fur)            # head
    d.ellipse((S * 0.26, S * 0.46, S * 0.74, S * 0.86), fill=light)          # muzzle
    d.ellipse((S * 0.26, S * 0.34, S * 0.38, S * 0.46), fill=(24, 16, 12, 255))   # eyes
    d.ellipse((S * 0.62, S * 0.34, S * 0.74, S * 0.46), fill=(24, 16, 12, 255))
    d.ellipse((S * 0.41, S * 0.48, S * 0.59, S * 0.60), fill=(40, 26, 22, 255))   # nose
    d.rounded_rectangle((S * 0.40, S * 0.66, S * 0.60, S * 0.86), radius=S * 0.03, fill=(255, 255, 250, 255))  # teeth
    d.line((S * 0.50, S * 0.66, S * 0.50, S * 0.86), fill=light, width=int(S * 0.012))
    return im.resize((s, s), Image.LANCZOS)


save(icon_groundhog(), "icon_groundhog.png")
