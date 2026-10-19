"""Each Loro Piana Interiors colour drawn as cloth rather than a flat chip. The surface comes from
real photographs: a linen plain weave (atelier photograph IMG_3196) for Connemara and Bangor; the
house's photograph of a milled wool and cashmere cloth (Cashmere_grigio) for Altai, since Round 25;
the alpaca close-up and the linen together for Ely's Harbour, linen and cashmere. The photograph gives only its relief; the colour is the tone
measured on the Loro Piana card, and a soft light falls across the sample.
Writes the chip (240 px) and the large view (1000 px).
usage: python3 cloth_render.py OUTDIR"""
import json, os, sys
import numpy as np
from scipy import ndimage
from PIL import Image, ImageOps

OUT = sys.argv[1] if len(sys.argv) > 1 else 'out'
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = {
    'linen': (os.path.join(HERE, 'raw', 'tess-3196.jpg'), (250, 350, 2650, 2750)),
    'nap': (os.path.join(HERE, '..', 'fib2', 'src', 'ALPACA_BEIGE.jpg'), (100, 40, 1340, 1280)),
    'cash': (os.path.join(HERE, 'raw', 'cashmere_grigio.jpg'), (160, 260, 1760, 2660)),
}


def srgb_to_lin(c):
    c = c / 255.0
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def lin_to_srgb(c):
    c = np.clip(c, 0, 1)
    return np.where(c <= 0.0031308, c * 12.92, 1.055 * c ** (1 / 2.4) - 0.055) * 255


_cache = {}


def detail(name, size, scale):
    """the relief of a photograph, at the given size: zero mean, unit spread, no broad light"""
    key = (name, size, scale)
    if key in _cache:
        return _cache[key]
    f, box = SRC[name]
    im = ImageOps.exif_transpose(Image.open(f)).convert('L').crop(box)
    side = int(min(im.size) * scale)
    im = im.crop((0, 0, side, side)).resize((size, size), Image.LANCZOS)
    a = np.asarray(im, float)
    a = a - ndimage.gaussian_filter(a, size / 18)
    a = a / (a.std() + 1e-9)
    _cache[key] = a
    return a


def light(size, amount):
    """a broad, soft light across the sample, brighter towards the top left"""
    y, x = np.mgrid[0:size, 0:size].astype(float) / size
    return 1 + amount * (.5 - (x * .55 + y * .45)) + amount * .4 * np.exp(-((x - .3) ** 2 + (y - .25) ** 2) * 3)


RECIPES = {
    # weave: list of (photograph, share of the photograph shown, weight); relief amplitude
    'linen': ([('linen', 1.0, 1.0)], .22),
    'wool': ([('cash', .62, 1.0)], .10),
    'soft': ([('linen', .8, .8), ('nap', .5, .45)], .19),
}


def render(hexc, recipe, size, chip=False):
    rgb = np.array([int(hexc[i:i + 2], 16) for i in (1, 3, 5)], float)
    base = srgb_to_lin(rgb)
    parts, amp = RECIPES[recipe]
    d = sum(detail(n, size, sc * (.42 if chip else 1)) * w for n, sc, w in parts)
    d = d / (d.std() + 1e-9)
    lum = float(base @ [.2126, .7152, .0722])
    if recipe == 'wool' and lum > .78:
        # a white wool photographed is never paper white: brought down so its nap shows
        base = base * (.78 / lum) ** .8
        lum = float(base @ [.2126, .7152, .0722])
    # pale cloth shows its weave in the shadows, dark cloth in the light on its threads
    a = amp * (.75 if lum > .6 else 1.0 if lum > .2 else 1.35)
    s = (1 + a * d) * light(size, .07 if chip else .10)
    out = base[None, None, :] * s[:, :, None]
    over = np.clip(out - .9, 0, None)
    out = out - over * .65
    return Image.fromarray(lin_to_srgb(out).astype(np.uint8), 'RGB')


CLOTHS = {'connemara': 'linen', 'altai': 'wool'}
PLAIN = {
    # cloths shown without listed colours: their natural ground, drawn
    'elys': ('soft', '#D8CEC1'),
    'bangor': ('linen', '#DCD4C6'),
}

if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    cards = json.load(open(os.path.join(HERE, 'cards.json')))
    for key, recipe in CLOTHS.items():
        for name, hexc, fn in cards[key]:
            stem = fn[:-4]
            render(hexc, recipe, 1000).save(os.path.join(OUT, stem + '-l.jpg'), quality=78, optimize=True, progressive=True)
            render(hexc, recipe, 240, chip=True).save(os.path.join(OUT, fn), quality=88, optimize=True, progressive=True)
            print(key, name, hexc)
    for key, (recipe, hexc) in PLAIN.items():
        render(hexc, recipe, 1000).save(os.path.join(OUT, 'ms-lp-%s-l.jpg' % key), quality=78, optimize=True, progressive=True)
        print(key, hexc)
