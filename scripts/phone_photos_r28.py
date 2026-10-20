"""Round 28: the openings' photographs for a phone, upright and at their own resolution or below.
A wide photograph cropped to a phone's tall frame was enlarged two to three and a half times; these are
cut from the full-height originals in Drive, each held to the colour of the photograph the wide screen
shows (a curve per channel, measured where the two pictures show the same thing).
  python3 phone_photos_r28.py <photos dir> <theme assets dir> <out dir>"""
import os, sys
import numpy as np
from PIL import Image

SRC, ASSETS, OUT = sys.argv[1:4]
ASP = .5625  # a phone's opening, about 9 by 16


def curves(src, ref):
    """per channel, the curve that gives src the tones of ref (two pictures of the same scene)"""
    s, r = np.asarray(src, float), np.asarray(ref, float)
    lut = []
    for c in range(3):
        sv, rv = np.sort(s[..., c].ravel()), np.sort(r[..., c].ravel())
        q = np.linspace(0, 1, 257)
        lut.append(np.interp(np.arange(256), np.quantile(sv, q), np.quantile(rv, q)))
    return lut


def apply(im, lut):
    a = np.asarray(im, float)
    out = np.stack([np.interp(a[..., c], np.arange(256), lut[c]) for c in range(3)], -1)
    return Image.fromarray(np.clip(out + .5, 0, 255).astype('uint8'))


def upright(im, cx):
    w = round(im.height * ASP)
    x = max(0, min(im.width - w, round(im.width * cx - w / 2)))
    return im.crop((x, 0, x + w, im.height))


def save(im, name, maxw=1200):
    if im.width > maxw:
        im = im.resize((maxw, round(im.height * maxw / im.width)), Image.LANCZOS)
    im.save(os.path.join(OUT, name), quality=82, optimize=True, progressive=True)
    print(name, im.size)


# 15+15 on the home page: the same room, upright (AMB_02 FRONTE DSC9600), the bed under the drapes;
# its light is already the wide photograph's
save(upright(Image.open(os.path.join(SRC, 'AMB_02_FRONTE_DSC9600.jpg')).convert('RGB'), .5), 'ms-photo-drapes-fireplace-m.jpg')

# Loro Piana Interiors: Paisley in its room, the whole height of the photograph the wide one is cut from
pa = Image.open(os.path.join(SRC, 'Paisley_IMG_5180_low.jpg')).convert('RGB')
wide = Image.open(os.path.join(ASSETS, 'ms-photo-lp-paisley-room.jpg')).convert('RGB')
lut = curves(pa.crop((0, 932, wide.width, 932 + wide.height)), wide)
save(apply(upright(pa, .62), lut), 'ms-photo-lp-paisley-room-m.jpg')

# Sleep Culture: the horse over Bellini, from the full-size original, in the graded photograph's tones
ho = Image.open(os.path.join(SRC, 'Bellini.jpg')).convert('RGB')
gr = Image.open(os.path.join(ASSETS, 'ms-graded-horse.jpg')).convert('RGB')
lut = curves(ho.resize(gr.size, Image.LANCZOS), gr)
save(apply(upright(ho, .55), lut), 'ms-graded-horse-m.jpg')
