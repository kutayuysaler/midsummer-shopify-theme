"""Round 25: the summer face of the seasons: the atelier's photograph of a linen weave (IMG_3196), cropped
clear of the clips along its top, its grey room light taken out and lifted to a pale flax.
usage: python3 summer_linen_r25.py SRC.jpg OUT.jpg"""
import sys
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
im = Image.open(sys.argv[1]).convert('RGB')               # landscape as stored: the clips run along the top
c = im.crop((0, 262, 3700, 262 + 1940)).resize((1600, 839), Image.LANCZOS)
a = np.asarray(c, float) / 255
lum = a.mean(2, keepdims=True)
a = lum + (a - lum) * .4                                   # the grey-green cast of the room, taken out
a = a * np.array([1.10, 1.055, .955])                      # towards flax
a = np.clip(1 - (1 - a) * .72, 0, 1)                       # lifted: a summer cloth, light in the hand
c = Image.fromarray((a * 255).astype('uint8'))
c = ImageEnhance.Contrast(c).enhance(1.10).filter(ImageFilter.UnsharpMask(radius=1.0, percent=45, threshold=2))
c.save(sys.argv[2], quality=82, optimize=True, progressive=True)
