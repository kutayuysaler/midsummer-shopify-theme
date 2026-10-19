"""Round 25: trim each press mark's viewBox to its ink, so that every mark on the press line is
measured the same way (some came with wide margins and were shown tiny). The large clear-ground
renders come from tools/press_boxes_r25.js; the originals stay in vendor/r25/press_orig.
usage: python3 scripts/press_trim_r25.py <originals dir> <renders dir> <out dir>"""
import os, re, sys
import numpy as np
from PIL import Image

src, renders, out = sys.argv[1:4]
os.makedirs(out, exist_ok=True)
for fn in sorted(os.listdir(src)):
    if not fn.endswith('.svg'):
        continue
    svg = open(os.path.join(src, fn), encoding='utf-8').read()
    m = re.search(r'<svg\b[^>]*>', svg)
    tag = m.group(0)
    vb = re.search(r'viewBox="([^"]+)"', tag)
    if vb:
        x0, y0, w0, h0 = [float(v) for v in vb.group(1).replace(',', ' ').split()]
    else:
        w0 = float(re.search(r'\swidth="([\d.]+)', tag).group(1)); h0 = float(re.search(r'\sheight="([\d.]+)', tag).group(1)); x0 = y0 = 0
    a = np.asarray(Image.open(os.path.join(renders, fn[:-4] + '.png')).convert('RGBA')).astype(float)
    ink = (a[..., 3] > 24) & (a[..., :3].mean(2) < 246)
    ys, xs = np.where(ink)
    H, W = ink.shape
    s = W / w0
    pad = 0.012 * max(xs.max() - xs.min(), ys.max() - ys.min())
    l, t = max(0, xs.min() - pad), max(0, ys.min() - pad)
    r, b = min(W, xs.max() + 1 + pad), min(H, ys.max() + 1 + pad)
    nx, ny, nw, nh = x0 + l / s, y0 + t / s, (r - l) / s, (b - t) / s
    keep = re.sub(r'\s(width|height|viewBox|enable-background)="[^"]*"', '', tag)
    new = keep.replace('<svg', '<svg width="%.2f" height="60" viewBox="%.3f %.3f %.3f %.3f"' % (60 * nw / nh, nx, ny, nw, nh), 1)
    open(os.path.join(out, fn), 'w', encoding='utf-8').write(svg.replace(tag, new, 1))
    print('%-38s %5.1f%% x %5.1f%% of its box kept, aspect %.2f' % (fn, 100 * nw / w0, 100 * nh / h0, nw / nh))
