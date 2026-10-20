"""Round 27: Sleep Culture's rooms kept for rest, from the house's own palazzo shoot (the A8447 series):
a different room or moment in each photograph, none of them shown elsewhere on the site. Each at most
1240 px tall and never enlarged, lightly sharpened, as scripts/gallery_photos_r26.py.
usage: python3 gallery_photos_r27.py SRC_DIR OUT_DIR   (SRC_DIR holds the files named below)"""
import sys, os
from PIL import Image, ImageOps, ImageFilter
PICK = {
    'ms-photo-sleep-glass.jpg': 'FOTO3_cashmere_dett_amb_A8447405_lettoconfinestra.png',
    'ms-photo-sleep-tea.jpg': 'A8447699.jpg',
    'ms-photo-sleep-throws.jpg': 'A8447462_DEF.jpg',
    'ms-photo-sleep-late-light.jpg': 'A8447661-2.jpg',
    'ms-photo-sleep-tulips.jpg': 'A8447702_(1).jpg',
    'ms-photo-sleep-woven-throw.jpg': 'A8447464.jpg',
}
src, out = sys.argv[1], sys.argv[2]
for name, f in PICK.items():
    im = ImageOps.exif_transpose(Image.open(os.path.join(src, f))).convert('RGB')
    h = min(1240, im.size[1])
    w = round(im.size[0] * h / im.size[1])
    if (w, h) != im.size:
        im = im.resize((w, h), Image.LANCZOS)
    im = im.filter(ImageFilter.UnsharpMask(radius=1.0, percent=30, threshold=2))
    im.save(os.path.join(out, name), quality=84, optimize=True, progressive=True)
    print(name, im.size, round(w / h, 3), os.path.getsize(os.path.join(out, name)) // 1024, 'KB')
