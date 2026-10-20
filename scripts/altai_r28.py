"""Round 28: Altai drawn as the cloth it is, a milled wool and cashmere: a felted face of fine, short
fibres lying every way, a soft play of light across it, and in the three mélange colours (1 Biancore,
2 Natural Brown, 7 Light Marengo) fibres lighter and darker than the ground. The colours are the ones
measured on the Loro Piana Interiors card (bin/lp_cards.json, Round 21); the card's own large swatch,
a phone photograph, carried more noise than weave, which is what made the old swatches look clouded.
Writes ms-lp-al-NN.jpg (the chip, 240 px) and ms-lp-al-NN-l.jpg (the large view, 1000 px).
  python3 altai_r28.py <lp_cards.json> <out dir>"""
import json, os, sys
import numpy as np
from PIL import Image
from scipy import ndimage

CARDS, OUT = sys.argv[1:3]
MELANGE = {'1 Biancore', '2 Natural Brown', '7 Light Marengo'}


def lin(c):
    c = np.asarray(c, float) / 255.0
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def srgb(c):
    c = np.clip(c, 0, 1)
    return np.where(c <= 0.0031308, c * 12.92, 1.055 * c ** (1 / 2.4) - 0.055) * 255


def fibres(size, n, rng, length, sigma):
    """short fibres lying every way, as a height field (and a field of which fibres are lighter)"""
    h = np.zeros((size, size)); tone = np.zeros((size, size))
    L = rng.uniform(length * .5, length * 1.5, n); a = rng.uniform(0, np.pi, n)
    x = rng.uniform(0, size, n); y = rng.uniform(0, size, n); s = rng.normal(0, 1, n); bend = rng.normal(0, .5, n)
    steps = int(length * 1.5) + 1
    for k in range(steps):
        t = k / (steps - 1) - .5
        ang = a + bend * t
        xx = (x + np.cos(ang) * L * t).astype(int) % size
        yy = (y + np.sin(ang) * L * t).astype(int) % size
        ok = np.abs(t) * 2 <= L / (length * 1.5)
        np.add.at(h, (yy[ok], xx[ok]), 1.0)
        np.add.at(tone, (yy[ok], xx[ok]), s[ok])
    return ndimage.gaussian_filter(h, sigma, mode='wrap'), ndimage.gaussian_filter(tone, sigma, mode='wrap')


def cloth(hexcol, size, melange, seed):
    rng = np.random.default_rng(seed)
    base = lin([int(hexcol[i:i + 2], 16) for i in (1, 3, 5)])
    k = size / 1000.0
    # the face: many fine fibres, felted together, and a fine grain under them
    h, _ = fibres(size, int(110000 * k * k) + 900, rng, 8 * k + 2, .6)
    h = (h - h.mean()) / (h.std() + 1e-9)
    grain = ndimage.gaussian_filter(rng.normal(0, 1, (size, size)), .9, mode='wrap')
    grain = grain / (grain.std() + 1e-9)
    # the felt: a soft, slow unevenness of the milled surface, and the light across its fibres
    felt = ndimage.gaussian_filter(rng.normal(0, 1, (size, size)), 26 * k + 2, mode='wrap')
    felt = felt / (felt.std() + 1e-9)
    gy, gx = np.gradient(ndimage.gaussian_filter(h + .5 * grain, 1.0, mode='wrap'))
    shade = 1 + .045 * h + .035 * grain + .11 * (-gx * .7 - gy * .7) + .028 * felt
    y, x = np.mgrid[0:size, 0:size] / size
    shade *= 1 + .035 * (.5 - (x * .55 + y * .45))
    # a dark cloth shows its fibres in the light, a pale one in the shadows
    lum = float(base @ [.2126, .7152, .0722])
    shade = 1 + (shade - 1) * (1.6 if lum < .05 else 1.25 if lum < .2 else 1.0)
    out = base[None, None, :] * shade[:, :, None]
    if melange:
        # fibres lighter and darker than the ground, as a mélange is spun: fine flecks, every way
        _, tone = fibres(size, int(60000 * k * k) + 600, rng, 7 * k + 2, .5)
        tone = np.tanh(tone / (tone.std() + 1e-9) * .9)
        out = out * (1 + .16 * tone)[:, :, None]
    out = np.clip(out, 0, None)
    over = np.clip(out - .92, 0, None)
    return Image.fromarray(srgb(out - over * .6).astype(np.uint8), 'RGB')


cards = json.load(open(CARDS))['altai']
for i, row in enumerate(cards):
    name, hexcol, chip = row[0], row[1], row[2]
    mel = name in MELANGE
    cloth(hexcol, 1000, mel, 100 + i).save(os.path.join(OUT, chip.replace('.jpg', '-l.jpg')), quality=86, optimize=True, progressive=True)
    cloth(hexcol, 240, mel, 200 + i).save(os.path.join(OUT, chip), quality=88, optimize=True, progressive=True)
    print(chip, name, hexcol, 'mélange' if mel else '')
