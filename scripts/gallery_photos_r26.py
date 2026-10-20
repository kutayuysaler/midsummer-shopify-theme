"""Round 26: Sleep Culture's rooms kept for rest, all from the house's own shoot at Via Andegari (the older
Tulip pictures retired): each 1240 px tall, lightly sharpened, as scripts/gallery_photos_r25.py.
usage: python3 gallery_photos_r26.py SRC_DIR OUT_DIR"""
import sys, os
from PIL import Image, ImageOps, ImageFilter
PICK = {
    'ms-photo-sleep-turned-down.jpg': 'sede___DSC4689.JPG',
    'ms-photo-sleep-blanket.jpg': 'sede_pure___DSC4834.JPG',
    'ms-photo-sleep-bedside.jpg': 'sede___DSC4922.JPG',
    'ms-photo-sleep-armchair.jpg': '_DSC4773.JPG',
}
# the bedside: a cable under the little table, cropped out at the foot
CROP = {'ms-photo-sleep-bedside.jpg': lambda s: (0, 0, s[0], int(s[1] * .775))}
src, out = sys.argv[1], sys.argv[2]
for name, f in PICK.items():
    p = os.path.join(src, f)
    if not os.path.exists(p):
        p = os.path.join(os.path.dirname(src.rstrip('/')), 'raw', f)
    im = ImageOps.exif_transpose(Image.open(p)).convert('RGB')
    if name in CROP:
        im = im.crop(CROP[name](im.size))
    h = 1240
    w = round(im.size[0] * h / im.size[1])
    im = im.resize((w, h), Image.LANCZOS).filter(ImageFilter.UnsharpMask(radius=1.0, percent=35, threshold=2))
    im.save(os.path.join(out, name), quality=82, optimize=True, progressive=True)
    print(name, im.size, round(w / h, 3), os.path.getsize(os.path.join(out, name)) // 1024, 'KB')
