"""The fourteen fibre plates for the Natural materials specimen viewer: licensed photographs of
each fibre at its source (Shutterstock and Unsplash, from the company's own library), cropped
square around the subject and toned alike: a warm monochrome, as one series of plates."""
import sys, os
from PIL import Image, ImageOps, ImageEnhance, ImageFilter
src, out = sys.argv[1], sys.argv[2]
mode = sys.argv[3] if len(sys.argv) > 3 else 'tone'
# name: (file, centre x, centre y as a share of the image, side as a share of the short edge)
SPEC = {
  'vicuna':    ('shutterstock_109093589.jpg',            .44, .5, 1.0),
  'yak':       ('toomas-tartes-4QTBhzYm7Z8-unsplash.jpeg', .47, .5, 1.0),
  'cashmere':  ('shutterstock_535793413.jpg',            .66, .5, 1.0),
  'wool':      ('shutterstock_104115377-3393434.jpg',    .40, .5, 1.0),
  # Round 21: the raw material, silk floss as it comes from the cocoon, not a satin cloth
  'silk':      ('seta_floss.jpg',                        .55, .42, .62),
  'horsehair': ('shutterstock_356083304-5878250.jpg',    .60, .5, 1.0),
  'cotton':    ('shutterstock_127061399-3624055.jpg',    .56, .5, 1.0),
  # Round 15: the seven that had only their drawing
  'camel':     ('shutterstock_390845494.jpg',            .47, .5, 1.0),
  # Round 17: the animal itself, the cloth itself, the fruit itself
  'alpaca':    ('sebastien-goldberg-xgQZ1rXbYa4-unsplash-2.jpg', .5, .56, .96),
  'mohair':    ('COPERTA_Mohair.jpg',                    .225, .262, .30),
  'linen':     ('lino.jpg',                              .35, .55, .35),
  'vegetable': ('nika-akin-b9UKi6t3xh0-unsplash (1).jpg', .5, .3, 1.0),
  # Round 22: Ingeo at its source, the maize in the field at summer's end (the wadding, white on black, said little)
  'ingeo':     ('shutterstock_313649711.jpg',            .33, .5, 1.0),
  'orange':    ('joshua-earle-a9bpgsbdknw-unsplash.jpg', .5, .5, 1.0),
}
# warm monochrome: shadows of dark walnut, light of the page's ivory
STOPS = [(0.0, (34, 28, 22)), (0.42, (122, 106, 88)), (0.78, (205, 192, 172)), (1.0, (247, 242, 233))]
def lut():
    t = []
    for c in range(3):
        for i in range(256):
            x = i / 255
            for (a, ca), (b, cb) in zip(STOPS, STOPS[1:]):
                if a <= x <= b:
                    k = (x - a) / (b - a); t.append(int(round(ca[c] + (cb[c] - ca[c]) * k))); break
    return t
LUT = lut()
def tone(im, keep=.14, soft=False):
    g = im.convert('L')
    if soft:
        # a cloth photographed in folds (the satin, until Round 21): keep its light, only deepen the folds a little
        g = ImageOps.autocontrast(g.filter(ImageFilter.GaussianBlur(2.4)), cutoff=(1, .3))
        g = g.point(lambda v: int(255 * (.30 + .68 * (v / 255) ** 1.15)))
    else:
        g = ImageOps.autocontrast(g, cutoff=(.4, .2))
    mono = Image.merge('RGB', (g, g, g)).point(LUT)
    if im.mode == 'RGB' and keep:
        mono = Image.blend(mono, im, keep)
    return mono
ONLY = sys.argv[4].split(',') if len(sys.argv) > 4 else None
for name, (f, cx, cy, s) in SPEC.items():
    if ONLY and name not in ONLY:
        continue
    im = ImageOps.exif_transpose(Image.open(os.path.join(src, f)))
    w, h = im.size; side = int(min(w, h) * s)
    x0 = min(max(0, int(cx * w - side / 2)), w - side); y0 = min(max(0, int(cy * h - side / 2)), h - side)
    c = im.crop((x0, y0, x0 + side, y0 + side))
    # the orange keeps a little more of its colour: in monochrome alone a citrus cut reads as anything
    c = tone(c, keep=(.30 if name == 'orange' else .14), soft=False) if mode == 'tone' else c.convert('RGB')
    for suffix, width in (('', 1400), ('-sm', 720)):
        o = c.resize((width, width), Image.LANCZOS)
        o = o.filter(ImageFilter.UnsharpMask(radius=1.1, percent=40 if width < side else 25, threshold=2))
        p = os.path.join(out, 'ms-fibre-photo-%s%s.jpg' % (name, suffix))
        o.save(p, 'JPEG', quality=82, optimize=True, progressive=True)
        print(name, suffix or 'lg', o.size, os.path.getsize(p) // 1024, 'KB')
