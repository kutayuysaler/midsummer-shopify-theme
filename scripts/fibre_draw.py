"""Each fibre drawn as under the glass: a few strands crossing the plate, each with the surface that
tells it apart. The animal hairs carry their cuticle scales (wool crimped and boldly scaled, mohair
almost smooth, horsehair thick with a core); silk runs as a pair of smooth filaments; linen is straight
with its nodes; cotton is a flat, twisting ribbon; vegetable horsehair is ridged; Ingeo and Orange Fiber
are smooth, even filaments. Each in its own natural colour, lit as on a microscope's bright field: the
strands in front sharp and rounded by the light, those behind softly out of focus. Deterministic;
written as small SVG files (assets/ms-fibre-draw-<slug>.svg) by bin/build_more.py."""
import math, random

W, H = 800, 1000
INK = '#5E5244'
# each fibre's own colour, as it is before any dye: (body, edge ink)
COLOR = {
    'vicuna': '#C99D6E', 'cashmere': '#E0CFB2', 'camel': '#C9A47B', 'yak': '#7A6250', 'alpaca': '#CDB28A',
    'mohair': '#F1ECE2', 'silk': '#EEDDB4', 'wool': '#EEE4CF', 'horsehair': '#3F3631', 'linen': '#CFC2A6',
    'cotton': '#F5F2EB', 'vegetable': '#5E4C34', 'ingeo': '#F2F0EA', 'orange': '#EECDA4',
}
FIELD = ('#FBF6EC', '#EFE5D3', '#D9CBB3')     # the bright field: centre, middle, edge

# r: strand radius; n: strands; scale: spacing of the cuticle scales (0 none); crimp: (amplitude, wavelength)
STYLE = {
    'vicuna':    dict(r=13, n=7, scale=14, scale_amp=4, crimp=(5, 260)),
    'cashmere':  dict(r=16, n=6, scale=18, scale_amp=5, crimp=(7, 300)),
    'camel':     dict(r=19, n=6, scale=19, scale_amp=5, crimp=(6, 340), core=0.25),
    'yak':       dict(r=18, n=6, scale=17, scale_amp=5, crimp=(6, 320), shade=0.12),
    'alpaca':    dict(r=21, n=5, scale=24, scale_amp=4, crimp=(4, 420), core=0.3),
    'mohair':    dict(r=24, n=5, scale=40, scale_amp=2, crimp=(10, 520)),
    'wool':      dict(r=24, n=5, scale=22, scale_amp=8, crimp=(28, 170)),
    'horsehair': dict(r=40, n=3, scale=30, scale_amp=4, crimp=(0, 1), core=0.35),
    'silk':      dict(r=11, n=4, pair=True, crimp=(0, 1), sheen=True),
    'linen':     dict(r=17, n=6, nodes=70, crimp=(0, 1), straight=True),
    'cotton':    dict(r=20, n=5, twist=58, crimp=(3, 400)),
    'vegetable': dict(r=34, n=3, ridges=5, crimp=(16, 300)),
    'ingeo':     dict(r=12, n=8, crimp=(0, 1), straight=True, sheen=True),
    'orange':    dict(r=10, n=8, crimp=(2, 500), sheen=True),
}

def shade(hexc, k):
    """lighter (k > 0, toward white) or darker (k < 0, toward a warm black)"""
    c = [int(hexc[i:i + 2], 16) for i in (1, 3, 5)]
    t = (255, 252, 246) if k > 0 else (34, 26, 20)
    k = abs(k)
    return '#%02X%02X%02X' % tuple(round(a + (b - a) * k) for a, b in zip(c, t))

def f(v):
    return ('%.1f' % v).rstrip('0').rstrip('.')

def poly(pts, close=False):
    return 'M' + ' '.join('%s %s' % (f(x), f(y)) for x, y in pts) + ('Z' if close else '')

def strand(rng, st, a0, off):
    """centre line across the plate at angle a0, offset off; returns points, normals"""
    ux, uy = math.cos(a0), math.sin(a0)
    nx, ny = -uy, ux
    cx, cy = W / 2 + nx * off, H / 2 + ny * off
    span = 1500
    amp, wl = st['crimp']
    bend = 0 if st.get('straight') else rng.uniform(-60, 60)
    ph = rng.uniform(0, 6.28)
    steps = 120
    pts = []
    for k in range(steps + 1):
        s = -span / 2 + span * k / steps
        o = bend * math.sin(math.pi * (k / steps)) + amp * math.sin(ph + s / wl * 6.28)
        pts.append((cx + ux * s + nx * o, cy + uy * s + ny * o))
    nrm = []
    for k in range(len(pts)):
        x0, y0 = pts[max(0, k - 1)]; x1, y1 = pts[min(len(pts) - 1, k + 1)]
        dx, dy = x1 - x0, y1 - y0; d = math.hypot(dx, dy) or 1
        nrm.append((-dy / d, dx / d))
    return pts, nrm

def inside(x, y, m=120):
    return -m < x < W + m and -m < y < H + m

def draw(slug):
    st = STYLE[slug]
    rng = random.Random(sum(map(ord, slug)) * 7 + 3)
    col = COLOR.get(slug, '#EDE6DA')
    dark = sum(int(col[i:i + 2], 16) for i in (1, 3, 5)) < 330
    ink = shade(col, -.62 if not dark else -.55)
    lite = shade(col, .55 if not dark else .38)
    out = []
    base = math.radians(rng.choice([-32, -28, 24, 30]))
    n = st['n']
    for i in range(n):
        a0 = base + math.radians(rng.uniform(-14, 14))
        off = (i - (n - 1) / 2) * (H / (n + 1)) * 0.95 + rng.uniform(-30, 30)
        pts, nrm = strand(rng, st, a0, off)
        rr = st['r'] * rng.uniform(0.82, 1.15)
        tw = st.get('twist')
        def rad(k):
            if tw:
                return rr * (0.35 + 0.65 * abs(math.cos(k * math.pi / tw * 6)))
            return rr * (1 + 0.04 * math.sin(k * 0.21 + i))
        reps = [0] if not st.get('pair') else [-rr * 1.05, rr * 1.05]
        back = n > 3 and rng.random() < 0.34
        out.append('<g stroke="%s"%s>' % (ink, ' opacity=".55" filter="url(#b)"' if back else ''))
        for sh in reps:
            e1 = [(x + nx * (sh + rad(k)), y + ny * (sh + rad(k))) for k, ((x, y), (nx, ny)) in enumerate(zip(pts, nrm))]
            e2 = [(x + nx * (sh - rad(k)), y + ny * (sh - rad(k))) for k, ((x, y), (nx, ny)) in enumerate(zip(pts, nrm))]
            keep = [k for k in range(len(pts)) if inside(*pts[k])]
            if not keep:
                continue
            k0, k1 = keep[0], keep[-1]
            e1, e2 = e1[k0:k1 + 1], e2[k0:k1 + 1]
            P, N = pts[k0:k1 + 1], nrm[k0:k1 + 1]
            # the strand: a pale body over what lies beneath, its two edges in ink
            body_d = poly(e1 + e2[::-1], True)
            out.append('<path d="%s" fill="%s" stroke="none"/>' % (body_d, col))
            # rounded by the light: darker towards both edges, a bright line a little off the centre
            out.append('<path d="%s" stroke="%s" stroke-width="%s" stroke-opacity=".22"/>' % (poly(e1), shade(col, -.45), f(rr * .55)))
            out.append('<path d="%s" stroke="%s" stroke-width="%s" stroke-opacity=".3"/>' % (poly(e2), shade(col, -.45), f(rr * .7)))
            hl = [(x + nx * (sh + rr * 0.3), y + ny * (sh + rr * 0.3)) for (x, y), (nx, ny) in zip(P, N)]
            out.append('<path d="%s" stroke="%s" stroke-width="%s" stroke-opacity="%s"/>' % (poly(hl), lite, f(rr * .32), '.85' if st.get('sheen') else '.55'))
            out.append('<path d="%s" stroke-width="1"/>' % poly(e1))
            out.append('<path d="%s" stroke-width="1"/>' % poly(e2))
            if st.get('core'):
                c = [(x + nx * sh, y + ny * sh) for (x, y), (nx, ny) in zip(P, N)]
                out.append('<path d="%s" stroke-width="%s" stroke-opacity=".2" stroke-dasharray="26 7 11 5 18 9"/>' % (poly(c), f(rr * st['core'])))
            # cuticle scales: the overlapping edges of the hair's surface, like roof tiles: irregular,
            # leaning one way, a little wavy
            if st.get('scale'):
                seg = 0.0
                nxt = st['scale'] * rng.uniform(0.7, 1.3)
                for k in range(1, len(P)):
                    seg += math.hypot(P[k][0] - P[k - 1][0], P[k][1] - P[k - 1][1])
                    if seg >= nxt:
                        seg = 0
                        nxt = st['scale'] * rng.uniform(0.7, 1.3)
                        (x, y), (nx, ny) = P[k], N[k]
                        r = rad(k) * 0.97
                        tx, ty = ny, -nx
                        lean = st['scale_amp'] * rng.uniform(1.2, 2.6)
                        w1, w2 = rng.uniform(-0.5, 0.5) * lean, rng.uniform(-0.5, 0.5) * lean
                        a = (x + nx * (sh + r), y + ny * (sh + r))
                        b = (x + nx * (sh - r), y + ny * (sh - r))
                        c1 = (x + nx * (sh + r * 0.35) + tx * (lean + w1), y + ny * (sh + r * 0.35) + ty * (lean + w1))
                        c2 = (x + nx * (sh - r * 0.35) + tx * (lean * 0.4 + w2), y + ny * (sh - r * 0.35) + ty * (lean * 0.4 + w2))
                        out.append('<path d="M%s %sC%s %s %s %s %s %s" stroke-width=".55" stroke-opacity=".55"/>' % (
                            f(a[0]), f(a[1]), f(c1[0]), f(c1[1]), f(c2[0]), f(c2[1]), f(b[0]), f(b[1])))
            if st.get('nodes'):
                seg = 0.0
                for k in range(1, len(P)):
                    seg += math.hypot(P[k][0] - P[k - 1][0], P[k][1] - P[k - 1][1])
                    if seg >= st['nodes'] * rng.uniform(0.6, 1.5):
                        seg = 0
                        (x, y), (nx, ny) = P[k], N[k]
                        r = rad(k); tx, ty = ny, -nx; d = r * 0.5
                        out.append('<path d="M%s %sL%s %sM%s %sL%s %s" stroke-width=".7" stroke-opacity=".75"/>' % (
                            f(x + nx * r - tx * d), f(y + ny * r - ty * d), f(x - nx * r + tx * d), f(y - ny * r + ty * d),
                            f(x + nx * r + tx * d), f(y + ny * r + ty * d), f(x - nx * r - tx * d), f(y - ny * r - ty * d)))
            if tw:
                for k in range(len(P)):
                    if abs(math.cos(k * math.pi / tw * 6)) < 0.06:
                        (x, y), (nx, ny) = P[k], N[k]
                        r = rad(k) + 2; tx, ty = ny, -nx
                        out.append('<path d="M%s %sL%s %s" stroke-width=".6" stroke-opacity=".7"/>' % (
                            f(x + nx * r + tx * 6), f(y + ny * r + ty * 6), f(x - nx * r - tx * 6), f(y - ny * r - ty * 6)))
            if st.get('ridges'):
                m = st['ridges']
                for j in range(1, m):
                    q = -1 + 2 * j / m
                    rl = [(x + nx * (sh + rad(k) * q), y + ny * (sh + rad(k) * q)) for k, ((x, y), (nx, ny)) in enumerate(zip(P, N))]
                    out.append('<path d="%s" stroke-width=".5" stroke-opacity=".5"/>' % poly(rl))
        out.append('</g>')
    # the bright field behind, and the strands behind drawn first, out of focus
    back_first = sorted(out_groups(out), key=lambda g: 0 if 'filter=' in g[0] else 1)
    field = ('<defs><radialGradient id="f" cx=".5" cy=".46" r=".72"><stop offset="0" stop-color="%s"/><stop offset=".62" stop-color="%s"/><stop offset="1" stop-color="%s"/></radialGradient>'
             '<filter id="b" x="-10%%" y="-10%%" width="120%%" height="120%%"><feGaussianBlur stdDeviation="3.2"/></filter></defs>'
             '<rect width="%d" height="%d" fill="url(#f)"/>' % (FIELD[0], FIELD[1], FIELD[2], W, H))
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" preserveAspectRatio="xMidYMid slice">%s'
            '<g fill="none" stroke-linecap="round" stroke-linejoin="round">%s</g></svg>' % (W, H, field, ''.join(''.join(g) for g in back_first)))

def out_groups(out):
    """the drawing's parts, one list per strand group (from its <g> to its </g>)"""
    groups, cur = [], None
    for x in out:
        if x.startswith('<g '):
            cur = [x]
        elif x == '</g>':
            cur.append(x)
            groups.append(cur)
            cur = None
        elif cur is not None:
            cur.append(x)
    return groups



if __name__ == '__main__':
    import sys, os
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    for slug in STYLE:
        s = draw(slug)
        open(os.path.join(out, 'ms-fibre-draw-%s.svg' % slug), 'w').write(s)
        print(slug, len(s))
