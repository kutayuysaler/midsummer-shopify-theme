"""Round 24: the three photographs of Inside the bed (assets/ms-part-*-house.jpg), from the owner's
photographs. Each is cropped to the cards' 4:5 frame (1000 × 1250), its subject placed as in the
others, and its brightness matched to the mattress (kept from Round 21).
usage: python3 part_photos_r24.py <boxspring photo> <topper photo> <mattress 1000×1250> <out dir>"""
import sys
from PIL import Image, ImageFilter, ImageStat, ImageEnhance

box, top, mat, out = sys.argv[1:5]
b, t, m = (Image.open(x).convert('RGB') for x in (box, top, mat))


def crop45(im, x0, y0, w):
    return im.crop((x0, y0, x0 + w, y0 + int(w * 5 / 4)))


def mean(im):
    return ImageStat.Stat(im.convert('L')).mean[0]


def finish(im, target):
    im = im.resize((1000, 1250), Image.LANCZOS)
    im = ImageEnhance.Brightness(im).enhance(max(0.92, min(1.12, target / mean(im))))
    im = ImageEnhance.Contrast(im).enhance(1.03)
    return im.filter(ImageFilter.UnsharpMask(radius=1.2, percent=40, threshold=3))


lm = mean(m)
bc = crop45(b, 100, 370, 860)   # the boxspring's corner, the mattress edge above it
tc = crop45(t, 0, 140, 1040)    # the tufted topper and its piping, the base below
finish(bc, max(mean(bc), lm * 0.93)).save(out + '/ms-part-base-house.jpg', quality=84, optimize=True, progressive=True)
finish(tc, max(mean(tc), lm * 0.95)).save(out + '/ms-part-topper-house.jpg', quality=84, optimize=True, progressive=True)
m.save(out + '/ms-part-mattress-house.jpg', quality=88, optimize=True, progressive=True)
