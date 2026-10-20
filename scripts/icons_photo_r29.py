"""Round 29: the Icons opening on one photograph, Top in the gallery of the Paris Opera: for a wide screen
the lower part of the gallery, its chandeliers and the bed (it sits beside the collection's name, on the
dark ground); for a phone, upright. Each at its own resolution or below.
  python3 icons_photo_r29.py <dir with top_opera_colori.jpg> <out dir>"""
import os, sys
from PIL import Image

SRC, OUT = sys.argv[1:3]
top = Image.open(os.path.join(SRC, 'top_opera_colori.jpg')).convert('RGB')


def crop(im, asp, bottom_gap):
    """the full width, asp wide to high, its foot bottom_gap of the height above the photograph's foot"""
    w = im.width
    h = round(w / asp)
    y1 = im.height - round(im.height * bottom_gap)
    return im.crop((0, max(0, y1 - h), w, y1))


wide = crop(top, 1.135, .015)
wide.save(os.path.join(OUT, 'ms-photo-icons-opera.jpg'), quality=84, optimize=True, progressive=True)
phone = crop(top, 1000 / 1430, 0).resize((1000, 1430), Image.LANCZOS)
phone.save(os.path.join(OUT, 'ms-photo-icons-opera-m.jpg'), quality=82, optimize=True, progressive=True)
for n in ('ms-photo-icons-opera.jpg', 'ms-photo-icons-opera-m.jpg'):
    print(n, Image.open(os.path.join(OUT, n)).size, os.path.getsize(os.path.join(OUT, n)) // 1024, 'KB')
