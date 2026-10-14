"""Cloth tiles for the bed drawings (Inside the bed): small seamless squares cut from photographs of
the cloths themselves, so a drawn topper or boxspring shows its own weave, bouclé, damask or paisley.

tile(kind, colour) returns a PIL image: the photograph's relief (or, for a printed or woven motif,
the motif itself) carried by the colour given; with colour None the photograph keeps its own.
usage: python3 tex_tiles.py OUTDIR   (writes a preview sheet of every kind)"""
import os, sys
import numpy as np
from scipy import ndimage
from PIL import Image, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, '..', 'fib2', 'src')
ASSETS = os.path.join(HERE, '..', 'v5', 'assets')

# kind: (file, crop box, tile size in pixels, relief amplitude, how much of the motif to keep)
KINDS = {
    'linen':   (os.path.join(HERE, 'raw', 'tess-3196.jpg'), (700, 800, 1700, 1800), 192, .20, 0),
    'mystic':  (os.path.join(SRC, 'Biancore-min.jpeg'), (200, 120, 1100, 1020), 192, .26, 0),
    'silk':    (os.path.join(SRC, 'Biancore-min.jpeg'), (200, 120, 1100, 1020), 192, .11, 0),
    'boucle':  (os.path.join(ASSETS, 'ms-lp-wish-l.jpg'), (100, 100, 1100, 1100), 192, .30, 0),
    'nap':     (os.path.join(SRC, 'ALPACA_BEIGE.jpg'), (200, 80, 1300, 1180), 192, .18, 0),
    'damask':  (os.path.join(ASSETS, 'ms-lp-cardi-l.jpg'), None, 256, .10, 1),
    'paisley': (os.path.join(SRC, 'Shadan-paisley.jpeg'), (0, 0, 1920, 1920), 320, .06, 1),
}


def srgb_to_lin(c):
    c = c / 255.0
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def lin_to_srgb(c):
    c = np.clip(c, 0, 1)
    return np.where(c <= 0.0031308, c * 12.92, 1.055 * c ** (1 / 2.4) - 0.055) * 255


def seamless(a):
    """blend the square with itself shifted by half, so its edges meet when repeated"""
    n = a.shape[0]
    b = np.roll(np.roll(a, n // 2, 0), n // 2, 1)
    t = np.linspace(-1, 1, n)
    w = 1 - np.clip(np.abs(t) * 1.25 - .25, 0, 1)        # 1 in the middle, 0 at the edges
    m = np.outer(w, w)
    if a.ndim == 3:
        m = m[:, :, None]
    return a * m + b * (1 - m)


def quiet_box(im, side):
    """for the damask: the square of the photograph with the fewest tufts (its brightest spots)"""
    g = np.asarray(ImageOps.grayscale(im), float)
    hot = g > np.percentile(g, 99.3)
    best, bb = None, None
    for y in range(0, g.shape[0] - side, 12):
        for x in range(0, g.shape[1] - side, 12):
            s = hot[y:y + side, x:x + side].sum()
            if best is None or s < best:
                best, bb = s, (x, y, x + side, y + side)
    return bb


_cache = {}


def mirror(a):
    """a motif repeated by reflection: seamless by construction, no ghost where copies overlap"""
    top = np.concatenate([a, a[:, ::-1]], 1)
    return np.concatenate([top, top[::-1]], 0)


def source(kind):
    if kind in _cache:
        return _cache[kind]
    f, box, n, amp, motif = KINDS[kind]
    im = ImageOps.exif_transpose(Image.open(f)).convert('RGB')
    if box is None:
        box = quiet_box(im, int(min(im.size) * .5))
    if motif:
        im = im.crop(box).resize((n // 2, n // 2), Image.LANCZOS)
        a = mirror(srgb_to_lin(np.asarray(im, float)))
    else:
        im = im.crop(box).resize((n, n), Image.LANCZOS)
        a = srgb_to_lin(np.asarray(im, float))
    lum = a @ np.array([.2126, .7152, .0722])
    # the broad light of the photograph goes; its weave (and motif) stays
    broad = ndimage.gaussian_filter(lum, n / (6 if motif else 14), mode='wrap')
    rel = lum / (broad + 1e-6) - 1
    mean = a / (broad[:, :, None] + 1e-6) * float(lum.mean())
    if not motif:
        # edges that meet: blended with itself shifted by half, keeping the weave's contrast
        n2 = rel.shape[0]
        tt = np.linspace(-1, 1, n2)
        w = 1 - np.clip(np.abs(tt) * 1.25 - .25, 0, 1)
        m = np.outer(w, w)
        sh = lambda x: np.roll(np.roll(x, n2 // 2, 0), n2 // 2, 1)
        k = np.sqrt(m ** 2 + (1 - m) ** 2)
        rel = (m * rel + (1 - m) * sh(rel)) / k
        mean = mean.mean(axis=(0, 1))[None, None, :] * (1 + rel[:, :, None])    # its own colour, its weave
    rel = rel / (rel.std() + 1e-9)
    if kind == 'damask':
        # the tufts in the photograph are its brightest spots: held down to the cloth's own light
        rel = np.clip(rel, -2.4, 1.1)
    _cache[kind] = (rel, mean, amp, motif)
    return _cache[kind]


def tile(kind, colour=None, size=None):
    rel, mean, amp, motif = source(kind)
    if colour is None:
        out = mean
    else:
        rgb = srgb_to_lin(np.array([int(colour[i:i + 2], 16) for i in (1, 3, 5)], float))
        lumc = float(rgb @ [.2126, .7152, .0722])
        a = amp * (.8 if lumc > .55 else 1.0 if lumc > .15 else 1.4)
        if motif:
            a = amp * {'paisley': 2.4, 'damask': 1.25}.get(kind, 2.0)
        out = rgb[None, None, :] * (1 + a * rel)[:, :, None]
        over = np.clip(out - .92, 0, None)
        out = out - over * .7
    im = Image.fromarray(lin_to_srgb(out).astype(np.uint8), 'RGB')
    if size and size != im.size[0]:
        im = im.resize((size, size), Image.LANCZOS)
    return im


def name(kind, colour):
    return 'ms-tex-%s-%s.jpg' % (kind, (colour or 'own').lstrip('#').lower())


if __name__ == '__main__':
    out = sys.argv[1] if len(sys.argv) > 1 else 'out'
    os.makedirs(out, exist_ok=True)
    tiles = [(k, None) for k in KINDS] + [('paisley', '#D7C2A6'), ('silk', '#8B2D35'), ('boucle', '#CFC3B1'), ('mystic', '#9E9893'), ('damask', '#D8CDBB')]
    sheet = Image.new('RGB', (256 * 6, 256 * 2 * ((len(tiles) + 5) // 6)), 'white')
    for i, (k, c) in enumerate(tiles):
        t = tile(k, c, 256)
        two = Image.new('RGB', (256, 512))
        two.paste(t.resize((128, 128)), (0, 0)); two.paste(t.resize((128, 128)), (128, 0))
        two.paste(t.resize((128, 128)), (0, 128)); two.paste(t.resize((128, 128)), (128, 128))
        two.paste(t, (0, 256))
        sheet.paste(two, ((i % 6) * 256, (i // 6) * 512))
    sheet.save(os.path.join(out, 'tex-sheet.jpg'), quality=85)
    print('ok', len(tiles))
