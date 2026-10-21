"""Round 29: the Icons opening on one photograph, Top in the gallery of the Paris Opera, from the
full-resolution original (4480 x 6720): for a wide screen a band across the whole gallery, its far
doors, the foot of the chandeliers and the bed, shown across the full width like the other collections'
openings; for a phone, upright. Each at the original's resolution or below.
  python3 icons_photo_r29.py <dir with top_opera_colori_4480.jpg> <out dir>"""
import os, sys
from PIL import Image, ImageFilter

SRC, OUT = sys.argv[1:3]
top = Image.open(os.path.join(SRC, 'top_opera_colori_4480.jpg')).convert('RGB')
W, H = top.size

# wide: the lower gallery, from the chandeliers to just under the bed (1.85 : 1)
wide = top.crop((0, round(H * .585), W, round(H * .95))).resize((3200, round(3200 * (H * .365) / W)), Image.LANCZOS)
wide = wide.filter(ImageFilter.UnsharpMask(radius=1.0, percent=30, threshold=2))
wide.save(os.path.join(OUT, 'ms-photo-icons-opera.jpg'), quality=82, optimize=True, progressive=True)
# phone: upright, the bed near the foot, the chandeliers above (1000 : 1430)
ph = round(W * 1430 / 1000)
phone = top.crop((0, H - ph - round(H * .02), W, H - round(H * .02))).resize((1290, 1845), Image.LANCZOS)
phone.save(os.path.join(OUT, 'ms-photo-icons-opera-m.jpg'), quality=80, optimize=True, progressive=True)
for n in ('ms-photo-icons-opera.jpg', 'ms-photo-icons-opera-m.jpg'):
    print(n, Image.open(os.path.join(OUT, n)).size, os.path.getsize(os.path.join(OUT, n)) // 1024, 'KB')
