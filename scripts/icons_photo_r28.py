"""Round 28: the Icons opening, two of the house's campaign photographs side by side (Top in the gallery
of the Paris Opera, Flora at a palace's ironwork windows), each panel at its own resolution or below;
on a phone, Top alone, upright.
  python3 icons_photo_r28.py <dir with top_opera_colori.jpg and flora.jpg> <out dir>"""
import os, sys
from PIL import Image

SRC, OUT = sys.argv[1:3]
W, H, SEAM = 2400, 1100, 6
PW = (W - SEAM) // 2


def panel(im, cy, w=PW, h=H):
    """the largest box of w:h in im, its centre at cy of the height, scaled to w x h"""
    cw = im.width
    ch = round(cw * h / w)
    if ch > im.height:
        ch, cw = im.height, round(im.height * w / h)
    y = max(0, min(im.height - ch, round(im.height * cy - ch / 2)))
    x = (im.width - cw) // 2
    return im.crop((x, y, x + cw, y + ch)).resize((w, h), Image.LANCZOS)


top = Image.open(os.path.join(SRC, 'top_opera_colori.jpg')).convert('RGB')
flora = Image.open(os.path.join(SRC, 'flora.jpg')).convert('RGB')
pair = Image.new('RGB', (W, H), (23, 20, 15))
pair.paste(panel(top, .70), (0, 0))
pair.paste(panel(flora, .62), (PW + SEAM, 0))
pair.save(os.path.join(OUT, 'ms-photo-icons-pair.jpg'), quality=82, optimize=True, progressive=True)
phone = panel(top, .86, 1000, 1430)
phone.save(os.path.join(OUT, 'ms-photo-icons-pair-m.jpg'), quality=82, optimize=True, progressive=True)
for n in ('ms-photo-icons-pair.jpg', 'ms-photo-icons-pair-m.jpg'):
    print(n, Image.open(os.path.join(OUT, n)).size, os.path.getsize(os.path.join(OUT, n)) // 1024, 'KB')
