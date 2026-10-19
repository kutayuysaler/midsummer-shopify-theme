"""Round 25: the press marks that came as PNG pictures, redrawn as one ink on a clear ground, so they
sit with the drawn (SVG) marks: white marks (Rent) made dark, marks printed on a white or coloured box
(Gaaf Goed, Hospitality Design, Interiors Monthly) lifted off it, pale ones (Pěkné bydlení) deepened,
and every mark trimmed to its edges. usage: python3 press_ink_r25.py SRC_DIR OUT_DIR"""
import sys, os, glob
import numpy as np
from PIL import Image

INK = (30, 27, 23)
src, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
for f in sorted(glob.glob(os.path.join(src, 'ms-press-*.png'))):
    im = Image.open(f).convert('RGBA')
    a = np.asarray(im, float) / 255
    rgb, al = a[..., :3], a[..., 3]
    lum = rgb @ [.2126, .7152, .0722]
    if al.mean() > .97:
        # printed on a box: the box is the commonest colour along the border; the mark is what differs from it
        edge = np.concatenate([rgb[0], rgb[-1], rgb[:, 0], rgb[:, -1]])
        box = np.median(edge, axis=0)
        d = np.sqrt(((rgb - box) ** 2).sum(-1))
        ink = np.clip((d - .08) / .45, 0, 1)
    else:
        # on a clear ground already: keep the shape, whatever its colour
        ink = al * np.clip(.35 + .65 * np.abs(lum - .5) * 2, 0, 1) if lum[al > .2].mean() > .7 else al
        ink = np.where(al > 0, np.maximum(ink, al * .85), 0)
    m = np.zeros(a.shape)
    m[..., 0], m[..., 1], m[..., 2] = INK[0] / 255, INK[1] / 255, INK[2] / 255
    m[..., 3] = ink
    o = Image.fromarray((m * 255).astype(np.uint8), 'RGBA')
    bb = o.getchannel('A').point(lambda v: 255 if v > 18 else 0).getbbox()
    if bb:
        pad = 2
        o = o.crop((max(0, bb[0] - pad), max(0, bb[1] - pad), min(o.size[0], bb[2] + pad), min(o.size[1], bb[3] + pad)))
    o.save(os.path.join(out, os.path.basename(f)), optimize=True)
    print(os.path.basename(f), im.size, '->', o.size)
