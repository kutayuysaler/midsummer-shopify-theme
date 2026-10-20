"""Round 28: Bellini's bouclé tile in its own colour, from the house's bouclé tile (the Wish photograph the
generator cut it from now shows the pinked chips). Each pixel keeps its light against the tile's mean,
in the new colour: vendor/r16/tex/ms-tex-boucle-<colour>.jpg"""
import os, sys
from PIL import Image, ImageStat
HERE = os.path.dirname(os.path.abspath(__file__))
TEX = os.path.join(HERE, '..', 'vendor', 'r16', 'tex')
src, col = sys.argv[1:3] if len(sys.argv) > 2 else ('ms-tex-boucle-d8cfc1.jpg', 'cfb693')
im = Image.open(os.path.join(TEX, src)).convert('RGB')
mean = ImageStat.Stat(im).mean
tgt = [int(col[i:i + 2], 16) for i in (0, 2, 4)]
bands = [b.point(lambda v, m=m, t=t: max(0, min(255, round(v * t / m)))) for b, m, t in zip(im.split(), mean, tgt)]
out = os.path.join(TEX, 'ms-tex-boucle-%s.jpg' % col)
Image.merge('RGB', bands).save(out, quality=80, optimize=True, progressive=True)
print(out, ImageStat.Stat(Image.open(out)).mean)
