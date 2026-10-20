"""Round 29: the Milano atelier page without the blue-and-gold room. Its opening, three of the four visit
steps, the second photograph of the pair, and the first and sixth of The rooms, from the house's own
shoot at Via Andegari: the parrot, leopard and teal rooms, a folding screen, the wool of a blanket.
The opening and the steps keep the shoot's full 1335 x 2000; the rooms are 1240 px tall, as the gallery
shows them. The two darker frames are lifted in the midtones only.
usage: python3 atelier_photos_r29.py SRC_DIR OUT_DIR"""
import sys, os
from PIL import Image, ImageOps, ImageFilter
PICK = {  # name: (frame, height, midtone gamma)
    'ms-photo-atelier-parrot-front.jpg': ('_DSC4929.JPG', 2000, 1.0),
    'ms-photo-atelier-screen.jpg': ('_DSC4807.JPG', 2000, 1.0),
    'ms-photo-atelier-leopard-side.jpg': ('_DSC4608.JPG', 2000, .9),
    'ms-photo-atelier-wool-edge.jpg': ('_DSC4782.JPG', 2000, 1.0),
    'ms-photo-atelier-leopard-above.jpg': ('_DSC4601.JPG', 2000, 1.0),
    'ms-photo-atelier-teal-room.jpg': ('_DSC4937.JPG', 1240, 1.0),
    'ms-photo-atelier-blanket.jpg': ('_DSC4746.JPG', 1240, .84),
}
src, out = sys.argv[1], sys.argv[2]
for name, (f, h, g) in PICK.items():
    im = ImageOps.exif_transpose(Image.open(os.path.join(src, f))).convert('RGB')
    if g != 1.0:
        lut = [round(255 * (i / 255) ** g) for i in range(256)]
        im = im.point(lut * 3)
    if im.size[1] != h:
        im = im.resize((round(im.size[0] * h / im.size[1]), h), Image.LANCZOS)
    im = im.filter(ImageFilter.UnsharpMask(radius=1.0, percent=30, threshold=2))
    im.save(os.path.join(out, name), quality=82, optimize=True, progressive=True)
    print(name, im.size, os.path.getsize(os.path.join(out, name)) // 1024, 'KB')
