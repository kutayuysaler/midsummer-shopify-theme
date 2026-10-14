"""Inside the bed's three cards, each a photograph of that part: a topper that is a topper, a
mattress, a boxspring; for the systems photographed (Roma, Flora, Paisley, First Dream, Dreamy) their
own, for the others the house's studio photographs. Cut at 4:5 into vendor/r16/parts.
usage: python3 part_photos.py [--sheet]"""
import os, sys
from PIL import Image, ImageOps, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, '..', 'fib2', 'src')
AS = os.path.join(HERE, '..', 'v5', 'assets')
OUT = os.path.join(HERE, '..', 'vendor', 'r16', 'parts')
CUTS = {
    # the house's studio photographs: any system's parts
    'topper-pure': (SRC + '/PURE_TOPPER_DSC4462 APRILE 2021.jpg', (0, 0, 1637, 2046)),
    'mattress-detail': (AS + '/ms-photo-mattress-detail.jpg', (810, 0, 1920, 1387)),
    'base-studio': (SRC + '/SOMMIER_02_A4.jpg', (320, 1150, 3520, 5150)),
    'base-pure': (SRC + '/PURE_TOPPER_DSC4462 APRILE 2021.jpg', (555, 1100, 1637, 2453)),
    # Dreamy, First Dream
    'topper-dreamy': (SRC + '/DREAMY_TOPPER_ALTO-IMG_7459.jpg', (0, 0, 1011, 1264)),
    'mattress-dreamy': (SRC + '/DREAMY_TOPPER_ALTO-IMG_7459.jpg', (150, 480, 861, 1369)),
    'base-dreamy': (SRC + '/DREAMY_TOPPER_ALTO-IMG_7459.jpg', (411, 750, 1011, 1500)),
    'topper-firstdream': (SRC + '/FIRST_DREAM_IMG_9742 TOPPER.jpg', (0, 0, 1041, 1301)),
    'mattress-firstdream': (SRC + '/FIRST_DREAM_IMG_9742 TOPPER MEDIUM.jpg', (200, 600, 1000, 1600)),
    'base-firstdream': (SRC + '/FIRST_DREAM_IMG_9742 TOPPER MEDIUM.jpg', (649, 1000, 1249, 1750)),
    # Roma, in Loro Piana Interiors
    'topper-roma': (SRC + '/LOROPIANA_IMG_9596.jpg', (0, 0, 1500, 1875)),
    'mattress-roma': (SRC + '/loropiana_IMG_0184.jpg', (0, 0, 1512, 1890)),
    'base-roma': (SRC + '/loropiana_IMG_0181.jpg', (1000, 480, 1800, 1480)),
    # Flora, Cardi and Wish
    'topper-flora': (AS + '/ms-photo-flora-wide.jpg', (500, 0, 1310, 1012)),
    'mattress-flora': (AS + '/ms-photo-flora-side.jpg', (0, 0, 1000, 1250)),
    'base-flora': (AS + '/ms-photo-flora-corner.jpg', (360, 450, 1000, 1250)),
    # Paisley, Shadan and Katai
    'topper-paisley': (SRC + '/Paisley_IMG_4918_low.jpg', (0, 0, 1428, 1785)),
    'mattress-paisley': (SRC + '/Paisley dettaglio.jpg', (0, 154, 1192, 1644)),
    'base-paisley': (SRC + '/Paisley_IMG_5161_low.jpg', (300, 1020, 1109, 2032)),
}


def cut(name):
    f, box = CUTS[name]
    im = ImageOps.exif_transpose(Image.open(f)).convert('RGB').crop(box)
    w = 720 if im.width >= 640 else 640
    out = im.resize((w, w * 5 // 4), Image.LANCZOS)
    if im.width < w:
        out = out.filter(ImageFilter.UnsharpMask(radius=1.2, percent=60, threshold=2))
    return out


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    names = sorted(CUTS)
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
