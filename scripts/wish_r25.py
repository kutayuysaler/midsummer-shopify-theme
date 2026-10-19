"""Round 25: the Wish bouclé, from the two photographs in the house's Drive (wish-2.jpeg, ivory;
wish.jpeg, navy). The ivory fills the frame, a little closer than before so the loops read; the navy
lies over its lower corner as a cut sample with pinked edges, like the colour chips on the page.
usage: python3 wish_r25.py OUT.jpg"""
import sys, os
import numpy as np
from PIL import Image, ImageFilter, ImageDraw, ImageEnhance

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, '..', 'fib2', 'src')
S = 1200


def cloth(f, crop, bright=1.0, contrast=1.0):
    im = Image.open(os.path.join(SRC, f)).convert('RGB').crop(crop).resize((S, S), Image.LANCZOS)
    im = im.filter(ImageFilter.UnsharpMask(radius=14, percent=38, threshold=0))   # relief of the loops
    im = im.filter(ImageFilter.UnsharpMask(radius=1.2, percent=60, threshold=2))
    im = ImageEnhance.Brightness(im).enhance(bright)
    return ImageEnhance.Contrast(im).enhance(contrast)


def pinked(w, h, tooth=14):
    """a rectangle with zigzag (pinking-shear) edges, as a mask"""
    m = Image.new('L', (w, h), 0)
    pts = []
    for x in range(0, w + 1, tooth):  # top
        pts.append((x, 0 if (x // tooth) % 2 == 0 else tooth // 2))
    for y in range(0, h + 1, tooth):  # right
        pts.append((w - (0 if (y // tooth) % 2 == 0 else tooth // 2), y))
    for x in range(w, -1, -tooth):  # bottom
        pts.append((x, h - (0 if (x // tooth) % 2 == 0 else tooth // 2)))
    for y in range(h, -1, -tooth):  # left
        pts.append((0 if (y // tooth) % 2 == 0 else tooth // 2, y))
    ImageDraw.Draw(m).polygon(pts, fill=255)
    return m


if __name__ == '__main__':
    out = sys.argv[1]
    ivory = cloth('wish-2.jpeg', (360, 360, 1560, 1560), bright=.97, contrast=1.06)
    navy = cloth('wish.jpeg', (300, 300, 1500, 1500), bright=1.18, contrast=1.05)
    w, h = 640, 520
    x0, y0 = S - w + 70, S - h + 70     # the sample runs off the frame at the bottom right
    mask = pinked(w, h)
    shadow = Image.new('L', (S, S), 0)
    shadow.paste(mask, (x0 - 10, y0 + 12))
    shadow = shadow.filter(ImageFilter.GaussianBlur(16))
    base = Image.composite(Image.new('RGB', (S, S), (120, 108, 92)), ivory, shadow.point(lambda v: int(v * .35)))
    sample = navy.crop((80, 80, 80 + w, 80 + h))
    base.paste(sample, (x0, y0), mask)
    base.save(out, quality=82, optimize=True, progressive=True)
    print(out, base.size)
