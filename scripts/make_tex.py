"""write every cloth tile the bed drawings use (bin/craft_draw.tiles()) into vendor/r16/tex, once"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'bin')); sys.path.insert(0, HERE)
from craft_draw import tiles
from tex_tiles import tile
OUT = os.path.join(HERE, '..', 'vendor', 'r16', 'tex')
os.makedirs(OUT, exist_ok=True)
n = 0
for name, kind, col in tiles():
    p = os.path.join(OUT, name)
    if os.path.exists(p) and '--force' not in sys.argv:
        continue
    tile(kind, col, 256).save(p, quality=80, optimize=True, progressive=True)
    n += 1
print('cloth tiles: %d written, %d in all' % (n, len(tiles())))
