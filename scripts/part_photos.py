"""Inside the bed's three cards, each a photograph of that part: a topper that is a topper, a
mattress, a boxspring; for the systems photographed (Roma, Flora, Paisley, First Dream, Dreamy) their
own, for the others the house's studio photographs. Cut at 4:5 into vendor/r16/parts.
usage: python3 part_photos.py [--sheet] [--only name,name]  (--only: cut just those; some Round 16 sources
were later retired from the theme's assets, so their cuts are kept as they are in vendor/r16/parts)"""
import os, sys
from PIL import Image, ImageOps, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, '..', 'fib2', 'src')
AS = os.path.join(HERE, '..', 'v5', 'assets')
OUT = os.path.join(HERE, '..', 'vendor', 'r16', 'parts')
CUTS = {
    # the house's photographs of any system's parts: one session at the atelier, one room, one low
    # sun (the Pure bed, its ochre base, the gold and blue wallpaper): the topper strapped on its
    # mattress, the mattress at its label, the boxspring on its walnut legs (Round 21, second choice)
    'topper-house': (SRC + '/PURE_atelier_DSC4466.jpg', (0, 0, 1335, 1669)),
    'mattress-house': (SRC + '/PURE_atelier_DSC4424.jpg', (0, 166, 1335, 1835)),
    'base-house': (SRC + '/PURE_atelier_DSC4415.jpg', (0, 331, 1335, 2000)),
    # Dreamy Springs, at its corner (Round 21: the whole corner rather than the side alone)
    'mattress-detail': (SRC + '/MATERASSO_DREAMY_SPRINGS_DETTAGLIO.jpg', (300, 0, 1180, 1100)),
    # Dreamy, First Dream
    'topper-dreamy': (SRC + '/DREAMY_TOPPER_ALTO-IMG_7459.jpg', (0, 0, 1011, 1264)),
    'base-dreamy': (SRC + '/DREAMY_TOPPER_ALTO-IMG_7459.jpg', (411, 750, 1011, 1500)),
    'topper-firstdream': (SRC + '/FIRST_DREAM_IMG_9742 TOPPER.jpg', (0, 0, 1041, 1301)),
    'base-firstdream': (SRC + '/FIRST_DREAM_IMG_9742 TOPPER MEDIUM.jpg', (649, 1000, 1249, 1750)),
    # Roma, in Loro Piana Interiors
    'topper-roma': (SRC + '/LOROPIANA_IMG_9596.jpg', (0, 0, 1500, 1875)),
    'mattress-roma': (SRC + '/loropiana_IMG_0184.jpg', (0, 0, 1512, 1890)),
    # Flora, Cardi and Wish
    'topper-flora': (AS + '/ms-photo-flora-wide.jpg', (500, 0, 1310, 1012)),
    'mattress-flora': (AS + '/ms-photo-flora-side.jpg', (0, 0, 1000, 1250)),
    'base-flora': (AS + '/ms-photo-flora-corner.jpg', (360, 450, 1000, 1250)),
    # Paisley, Shadan and Katai
    'topper-paisley': (SRC + '/Paisley_IMG_4918_low.jpg', (0, 0, 1428, 1785)),
    'mattress-paisley': (SRC + '/Paisley dettaglio.jpg', (0, 154, 1192, 1644)),
    # Round 17: the boxspring card, the whole bed in its room (the edge close-up is the mattress's)
    'base-paisley': (AS + '/ms-photo-lp-paisley-front.jpg', (0, 0, 1209, 1511)),
}


def cut(name):
    f, box = CUTS[name]
    im = ImageOps.exif_transpose(Image.open(f)).convert('RGB').crop(box)
    # Round 21: sharper on dense screens, up to 1000 wide where the photograph allows
    w = next(x for x in (1000, 880, 720, 640) if im.width >= x or x == 640)
    out = im.resize((w, w * 5 // 4), Image.LANCZOS)
    if im.width < w:
        out = out.filter(ImageFilter.UnsharpMask(radius=1.2, percent=60, threshold=2))
    return out


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    names = sorted(CUTS)
    if '--only' in sys.argv:
        names = sys.argv[sys.argv.index('--only') + 1].split(',')
    for n in names:
        cut(n).save(os.path.join(OUT, 'ms-part-%s.jpg' % n), quality=82, optimize=True, progressive=True)
    if '--sheet' in sys.argv:
        W = 240
        sheet = Image.new('RGB', (W * 7, (W * 5 // 4 + 20) * 3), 'white')
        from PIL import ImageDraw
        d = ImageDraw.Draw(sheet)
        for i, n in enumerate(names):
            im = Image.open(os.path.join(OUT, 'ms-part-%s.jpg' % n)).resize((W, W * 5 // 4))
            x, y = (i % 7) * W, (i // 7) * (W * 5 // 4 + 20)
            sheet.paste(im, (x, y)); d.text((x + 4, y + W * 5 // 4 + 4), n, fill='black')
        sheet.save(os.path.join(HERE, '..', 'rt5', 'parts-cut.jpg'), quality=85)
    print(len(names))
