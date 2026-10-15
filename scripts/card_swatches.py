"""Round 21: the Connemara and Altai colours, measured again on the Loro Piana Interiors cards held at
the atelier (the same cards as lp/cards.py, from the swatch folder on Drive), and drawn with each card's
own cloth.

What changed from Round 12: each swatch is white-balanced against the paper right beside it (the
photograph of the card is lit unevenly, so one paper tone for the whole card left the far swatches
dull); its colour is the mean in linear light, as the eye averages a weave (an sRGB mean comes out
darker); and the weave is the card's own large swatch of that cloth (Connemara's open linen, Altai's
milled wool), not a linen photographed elsewhere. Each colour keeps the depth of relief it shows on
the card, so the white shows its weave in the shadows and the dark ones on the threads.

Writes, into vendor/lp21: ms-lp-co-NN.jpg / ms-lp-al-NN.jpg (the chip, 240 px), their -l.jpg (the large
view, 1000 px), and a check sheet; and rewrites the hex values of bin/lp_cards.json.
usage: python3 card_swatches.py"""
import json, os, sys
import numpy as np
import pymupdf
from PIL import Image, ImageDraw
from scipy import ndimage

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'vendor', 'lp21')
CARDS_JSON = os.path.join(HERE, '..', 'bin', 'lp_cards.json')
DPI = 360
S = DPI / 72


def srgb_to_lin(c):
    c = np.asarray(c, float) / 255.0
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def lin_to_srgb(c):
    c = np.clip(c, 0, 1)
    return np.where(c <= 0.0031308, c * 12.92, 1.055 * c ** (1 / 2.4) - 0.055) * 255


def page(pdf):
    p = pymupdf.open(pdf)[0]
    pix = p.get_pixmap(dpi=DPI)
    return np.asarray(Image.frombytes('RGB', (pix.width, pix.height), pix.samples), float)


def boxes(img, region, ncols, nrows):
    """the swatches of a grid on the card, as pixel boxes, found where the cloth departs from the paper"""
    x0, y0, x1, y1 = [int(v * S) for v in region]
    reg = img[y0:y1, x0:x1]
    q = (reg[::5, ::5] // 6).reshape(-1, 3)
    vals, counts = np.unique(q, axis=0, return_counts=True)
    paper = vals[counts.argmax()] * 6 + 3
    dark = np.abs(reg - paper).sum(2) > 70
    colsf = dark.mean(0); rowsf = dark.mean(1)

    def runs(f, thr, minlen):
        r = []; s = None
        for i, v in enumerate(list(f) + [0]):
            if v > thr and s is None:
                s = i
            if v <= thr and s is not None:
                if i - s >= minlen:
                    r.append((s, i))
                s = None
        return r
    cr = runs(colsf, 0.12, 40); rr = runs(rowsf, 0.08, 40)
    assert len(cr) == ncols, cr
    hs = sorted(b - a for a, b in rr); hmed = hs[len(hs) // 2]
    if len(rr) > 2 and rr[-1][1] - rr[-1][0] < 0.6 * hmed:
        pitch = rr[-2][0] - rr[-3][0]; a = rr[-2][0] + pitch; rr[-1] = (a, a + hmed)
    if len(rr) < nrows:  # a last row of near-white cloth: the same pitch as the rows above
        pitch = rr[1][0] - rr[0][0] if len(rr) > 1 else 0
        while len(rr) < nrows:
            a, b = rr[-1]; rr.append((a + pitch, b + pitch))
    return [(x0 + ca, y0 + ra, x0 + cb, y0 + rb) for (ra, rb) in rr[:nrows] for (ca, cb) in cr]


def paper_beside(img, box):
    """the paper in a band just outside the swatch, left, right and above (the label is below)"""
    a, b, c, d = box; w = c - a; g = int(w * .06); band = int(w * .10)
    parts = [img[b:d, max(0, a - g - band):a - g], img[b:d, c + g:c + g + band], img[max(0, b - g - band):b - g, a:c]]
    px = np.concatenate([p.reshape(-1, 3) for p in parts if p.size])
    lum = px.mean(1)
    px = px[lum > np.percentile(lum, 40)]  # the paper, not a neighbour's pinked edge
    return np.median(px, 0)


def measure(img, box):
    a, b, c, d = box; m = int(min(c - a, d - b) * .18)
    sw = img[b + m:d - m, a + m:c - m]
    paper = paper_beside(img, box)
    gain = 251.0 / np.maximum(paper, 1)  # the card is white paper: it reads as the page (#FBF9F5) does
    bal = np.clip(sw * gain, 0, 255)
    lin = srgb_to_lin(bal)
    mean = lin.reshape(-1, 3).mean(0)
    lum = lin @ [.2126, .7152, .0722]
    rel = lum - ndimage.gaussian_filter(lum, lum.shape[0] / 6)
    relief = float(rel.std() / max(lum.mean(), 1e-4))
    return mean, relief, Image.fromarray(bal.astype(np.uint8))


def weave(img, box, inset=.1):
    """the large swatch of the card, as relief only: zero mean, unit spread, no broad light"""
    a, b, c, d = box; m = int(min(c - a, d - b) * inset)
    sw = img[b + m:d - m, a + m:c - m]
    side = min(sw.shape[:2]); sw = sw[:side, :side]
    lum = srgb_to_lin(sw) @ [.2126, .7152, .0722]
    return lum


def detail(lum, size, share):
    side = int(lum.shape[0] * share)
    im = Image.fromarray((np.clip(lum[:side, :side] / max(lum.max(), 1e-6), 0, 1) * 65535).astype(np.uint16).astype(np.int32), 'I')
    a = np.asarray(im.resize((size, size), Image.LANCZOS), float)
    a = a - ndimage.gaussian_filter(a, size / 18)
    return a / (a.std() + 1e-9)


def light(size, amount):
    y, x = np.mgrid[0:size, 0:size].astype(float) / size
    return 1 + amount * (.5 - (x * .55 + y * .45)) + amount * .4 * np.exp(-((x - .3) ** 2 + (y - .25) ** 2) * 3)


def render(mean, relief, lum, size, chip):
    d = detail(lum, size, .45 if chip else 1.0)
    amp = float(np.clip(relief * 1.6, .08, .34))
    s = (1 + amp * d) * light(size, .05 if chip else .08)
    s = s / s.mean()
    out = mean[None, None, :] * s[:, :, None]
    over = np.clip(out - .92, 0, None)
    out = out - over * .6
    return Image.fromarray(lin_to_srgb(out).astype(np.uint8), 'RGB')


def big_box(img, region):
    x0, y0, x1, y1 = [int(v * S) for v in region]
    reg = img[y0:y1, x0:x1]
    q = (reg[::5, ::5] // 6).reshape(-1, 3)
    vals, counts = np.unique(q, axis=0, return_counts=True)
    paper = vals[counts.argmax()] * 6 + 3
    dark = np.abs(reg - paper).sum(2) > 70
    ys, xs = np.where(dark)
    return (x0 + int(np.percentile(xs, 1)), y0 + int(np.percentile(ys, 1)), x0 + int(np.percentile(xs, 99)), y0 + int(np.percentile(ys, 99)))


CARDS = {
    # card, its grids (region in points, columns, rows, names), the region of its large swatch, prefix
    'connemara': ('raw/connemara.pdf', [((50, 285, 215, 450), 3, 3, ['1 Dark Indigo', '2 Indaco Oxus', '5 Zen', '6 Biancore', '8 Dark Zen', '10 Malachite', '12 Sassicaia', '14 Cowes', '16 Camargue'])],
                  (400, 270, 580, 440), 'co'),
    'altai': ('raw/Altai_.pdf', [((50, 262, 215, 525), 3, 5, ['11 Shaded White', '15 Midnight', '21 Eucalyptus', '24 Diaspro', '25 Rosso Lacca', '26 Granato', '28 Cammello', '37 Paprika', '38 Henné', '45 Polvere', '46 Lovat', '47 Green Blue', '51 Pergamena']),
                              ((240, 420, 400, 470), 3, 1, ['1 Biancore', '2 Natural Brown', '7 Light Marengo'])],
              (400, 260, 580, 430), 'al'),
}

if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    cards = json.load(open(CARDS_JSON, encoding='utf-8'))
    sheet = []
    for key, (pdf, grids, bigreg, pre) in CARDS.items():
        img = page(os.path.join(HERE, pdf))
        bb = big_box(img, bigreg)
        lum = weave(img, bb)
        print(key, 'large swatch', bb, lum.shape, file=sys.stderr)
        names = []; bxs = []
        for region, nc, nr, nm in grids:
            b = boxes(img, region, nc, nr)[:len(nm)]
            names += nm; bxs += b
        rows = []
        for i, (n, bx) in enumerate(zip(names, bxs), 1):
            mean, relief, bal = measure(img, bx)
            hexc = '#%02X%02X%02X' % tuple(int(round(v)) for v in lin_to_srgb(mean))
            fn = 'ms-lp-%s-%02d.jpg' % (pre, i)
            render(mean, relief, lum, 240, True).save(os.path.join(OUT, fn), quality=88, optimize=True, progressive=True)
            render(mean, relief, lum, 1000, False).save(os.path.join(OUT, fn[:-4] + '-l.jpg'), quality=80, optimize=True, progressive=True)
            rows.append([n, hexc, fn])
            sheet.append((key, n, hexc, bal, fn))
            print(key, n, hexc, 'relief %.3f' % relief)
        old = {r[0]: r[1] for r in cards.get(key, [])}
        for r in rows:
            r_old = old.get(r[0])
            print('   %-18s %s -> %s' % (r[0], r_old, r[1]))
        cards[key] = rows
    json.dump(cards, open(CARDS_JSON, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    # the check sheet: the card's swatch (balanced), the chip, the large view
    W = 150
    sh = Image.new('RGB', (W * 3 + 180, (W * 2 // 3 + 6) * len(sheet)), '#FBF9F5')
    dr = ImageDraw.Draw(sh)
    for i, (key, n, hexc, bal, fn) in enumerate(sheet):
        y = i * (W * 2 // 3 + 6)
        dr.text((4, y + 30), '%s %s %s' % (key[:4], n, hexc), fill='black')
        for j, im in enumerate([bal, Image.open(os.path.join(OUT, fn)), Image.open(os.path.join(OUT, fn[:-4] + '-l.jpg'))]):
            t = im.copy(); t.thumbnail((W * 4, W * 4))
            s = min(t.size); t = t.crop(((t.width - s) // 2, (t.height - s) * 0 // 2, (t.width - s) // 2 + s, s * 2 // 3)).resize((W, W * 2 // 3))
            sh.paste(t, (180 + j * W, y))
    sh.save(os.path.join(OUT, 'check.jpg'), quality=85)
