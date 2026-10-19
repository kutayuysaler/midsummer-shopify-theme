"""Round 25: the atelier's rooms (Inside Via Andegari) and beds made up for the night (Sleep Culture),
from the house's own shoot at Via Andegari and the Tulip shoot: each 1240 px tall, as the gallery shows
them at up to 620 px, lightly sharpened. usage: python3 gallery_photos_r25.py SRC_DIR OUT_DIR"""
import sys, os
from PIL import Image, ImageOps, ImageFilter
PICK = {
    'ms-photo-atelier-leopard.jpg': 'sede___DSC4605.JPG',
    'ms-photo-atelier-teal.jpg': 'sede___DSC4662.JPG',
    'ms-photo-atelier-parrot-room.jpg': 'sede_parrots___DSC4911.JPG',
    'ms-photo-atelier-blue-gold-made.jpg': 'sede_pure___DSC4884.JPG',
    'ms-photo-atelier-lacquer.jpg': 'sede___DSC4832.JPG',
    'ms-photo-atelier-red-wall.jpg': 'sede___DSC4761.JPG',
    'ms-photo-atelier-edge.jpg': 'sede___DSC4500.JPG',
    'ms-photo-atelier-linen.jpg': 'sede___DSC4581.JPG',
    'ms-photo-sleep-tulip.jpg': 'tulip___DSC5613.JPG',
    'ms-photo-sleep-pillows.jpg': 'sede_pure___DSC4852.JPG',
    'ms-photo-sleep-turned-down.jpg': 'sede___DSC4737.JPG',
    'ms-photo-sleep-throw.jpg': 'tulip___DSC5759.JPG',
    'ms-photo-sleep-made-up.jpg': 'sede_pure___DSC4869.JPG',
}
# the Tulip shoot: a studio cable along the right-hand edge, cropped out
CROP = {'ms-photo-sleep-tulip.jpg': lambda s: (0, 0, int(s[0] * .885), s[1])}
src, out = sys.argv[1], sys.argv[2]
for name, f in PICK.items():
    im = ImageOps.exif_transpose(Image.open(os.path.join(src, f))).convert('RGB')
    if name in CROP:
        im = im.crop(CROP[name](im.size))
    h = 1240
    w = round(im.size[0] * h / im.size[1])
    im = im.resize((w, h), Image.LANCZOS).filter(ImageFilter.UnsharpMask(radius=1.0, percent=35, threshold=2))
    im.save(os.path.join(out, name), quality=82, optimize=True, progressive=True)
    print(name, im.size, os.path.getsize(os.path.join(out, name)) // 1024, 'KB')
