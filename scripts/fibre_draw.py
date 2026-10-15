"""Each fibre drawn as under the glass, to scale (Round 18).

Every fibre is drawn at the same magnification, 2 px to the micrometre, so the round field is 400 µm
across, and behind it lies a human hair (about 70 µm), pale, at the same scale: a visitor sees at once
that vicuña is a sixth of a hair and horsehair twice one. The surface is each fibre's own, as textile
microscopy shows it:
  - the animal hairs carry their cuticle scales, at their own spacing and with their own margins: wool
    close and jagged, cashmere and vicuña smooth and far apart, mohair thin and flat, almost unseen;
    horsehair and some alpaca fibres have a core (the medulla);
  - silk is a pair of smooth filaments, as the silkworm lays them, in a faint coat of its gum;
  - linen is straight, with the small nodes across it and a narrow channel down its centre;
  - cotton is a flat ribbon that twists on itself;
  - vegetable horsehair is a broad, ridged palm fibre; Ingeo and Orange Fiber are smooth, even filaments.
At 400 µm the crimp of wool (millimetres long) is only a gentle bend, so none is exaggerated.
A 100 µm bar sits at the foot of the field. Deterministic; written as small SVG files
(assets/ms-fibre-draw-<slug>.svg) by bin/build_more.py."""
import math, random

W, H = 800, 1000          # the field shows the middle 800 x 800: 400 µm across
PX = 2.0                  # px per µm
CX, CY, R = W / 2, H / 2, 400
COLOR = {
    'vicuna': '#C99D6E', 'cashmere': '#E0CFB2', 'camel': '#C9A47B', 'yak': '#7A6250', 'alpaca': '#CDB28A',
    'mohair': '#F1ECE2', 'silk': '#EEDDB4', 'wool': '#EEE4CF', 'horsehair': '#3F3631', 'linen': '#CFC2A6',
    'cotton': '#F5F2EB', 'vegetable': '#5E4C34', 'ingeo': '#F2F0EA', 'orange': '#EECDA4',
}
FIELD = ('#FBF6EC', '#EFE5D3', '#D9CBB3')
HAIR = '#D6C9B4'          # the human hair behind, for scale

# d: diameter (µm, drawn); n: strands; scale: spacing of the cuticle scales (µm); margin: their edge;
# core: medulla (share of the width), 'solid' or 'broken'; bend: how much a strand curves over the field (px)
STYLE = {
    'vicuna':    dict(d=12, n=7, scale=15, margin='smooth', bend=70),
    'cashmere':  dict(d=15, n=7, scale=17, margin='smooth', bend=60),
    'yak':       dict(d=17, n=7, scale=14, margin='wavy', bend=60),
    'camel':     dict(d=19, n=6, scale=13, margin='wavy', bend=55),
    'alpaca':    dict(d=21, n=6, scale=11, margin='faint', core=0.28, core_kind='broken', core_share=0.4, bend=55),
    'mohair':    dict(d=30, n=5, scale=19, margin='flat', bend=45, sheen=True),
    'wool':      dict(d=28, n=5, scale=9, margin='jagged', bend=70),
    'silk':      dict(d=11, n=4, pair=True, bend=50, sheen=True),
    'horsehair': dict(d=150, n=2, scale=8, margin='wavy', core=0.32, core_kind='solid', bend=25),
    'linen':     dict(d=18, n=6, nodes=34, lumen=True, bend=8),
    'cotton':    dict(d=16, n=6, twist=95, bend=40),
    'vegetable': dict(d=170, n=2, ridges=9, bend=10),
    'ingeo':     dict(d=20, n=7, bend=12, sheen=True),
    'orange':    dict(d=14, n=8, striae=2, bend=30, sheen=True),
}

def shade(hexc, k):
    """lighter (k > 0, toward white) or darker (k < 0, toward a warm black)"""
    c = [int(hexc[i:i + 2], 16) for i in (1, 3, 5)]
    t = (255, 252, 246) if k > 0 else (34, 26, 20)
    k = abs(k)
    return '#%02X%02X%02X' % tuple(round(a + (b - a) * k) for a, b in zip(c, t))

def f(v):
    return str(int(round(v))) if abs(v) >= 100 else ('%.1f' % v).rstrip('0').rstrip('.')

def poly(pts, close=False):
    return 'M' + ' '.join('%s %s' % (f(x), f(y)) for x, y in pts) + ('Z' if close else '')

def strand(rng, a0, off, bend):
    """a centre line across the field at angle a0, offset off: points every 4 px, and their normals"""
    ux, uy = math.cos(a0), math.sin(a0)
    nx, ny = -uy, ux
    cx, cy = CX + nx * off, CY + ny * off
    span = 1300
    b = rng.uniform(-bend, bend)
    w2 = rng.uniform(-bend, bend) * 0.35
    ph = rng.uniform(0, 6.28)
    steps = int(span / 9)
    pts = []
    for k in range(steps + 1):
        t = k / steps
        s = -span / 2 + span * t
        o = b * math.sin(math.pi * t) + w2 * math.sin(ph + t * 6.28 * 1.3)
        pts.append((cx + ux * s + nx * o, cy + uy * s + ny * o))
    nrm = []
    for k in range(len(pts)):
        x0, y0 = pts[max(0, k - 1)]; x1, y1 = pts[min(len(pts) - 1, k + 1)]
        dx, dy = x1 - x0, y1 - y0; dd = math.hypot(dx, dy) or 1
        nrm.append((-dy / dd, dx / dd))
    return pts, nrm

def visible(x, y, m=60):
    return math.hypot(x - CX, y - CY) < R + m

def clip(pts, nrm, m=60):
    # keep the strand wherever any of its width could show in the field
    keep = [k for k in range(len(pts)) if visible(pts[k][0], pts[k][1], m)]
    if not keep:
        return None, None
    return pts[keep[0]:keep[-1] + 1], nrm[keep[0]:keep[-1] + 1]

def body(out, P, N, rad, col, sh=0.0, sheen=False, alpha=1.0):
    """a rounded strand: a pale body, darker toward both edges, a bright line a little off the centre"""
    e1 = [(x + nx * (sh + rad(k)), y + ny * (sh + rad(k))) for k, ((x, y), (nx, ny)) in enumerate(zip(P, N))]
    e2 = [(x + nx * (sh - rad(k)), y + ny * (sh - rad(k))) for k, ((x, y), (nx, ny)) in enumerate(zip(P, N))]
    r0 = rad(0)
    out.append('<path d="%s" fill="%s" stroke="none"%s/>' % (poly(e1 + e2[::-1], True), col, '' if alpha == 1 else ' fill-opacity="%s"' % alpha))
    out.append('<path d="%s" stroke="%s" stroke-width="%s" stroke-opacity="%s"/>' % (poly(e1), shade(col, -.45), f(max(1, r0 * .45)), f(.22 * alpha)))
    out.append('<path d="%s" stroke="%s" stroke-width="%s" stroke-opacity="%s"/>' % (poly(e2), shade(col, -.45), f(max(1, r0 * .6)), f(.3 * alpha)))
    hl = [(x + nx * (sh + rad(k) * 0.32), y + ny * (sh + rad(k) * 0.32)) for k, ((x, y), (nx, ny)) in enumerate(zip(P, N))]
    out.append('<path d="%s" stroke="%s" stroke-width="%s" stroke-opacity="%s"/>' % (poly(hl), shade(col, .6), f(max(1, r0 * .28)), f((.85 if sheen else .5) * alpha)))
    out.append('<path d="%s" stroke-width="%s" stroke-opacity="%s"/>' % (poly(e1), f(min(1.4, .5 + r0 / 40)), f(alpha)))
    out.append('<path d="%s" stroke-width="%s" stroke-opacity="%s"/>' % (poly(e2), f(min(1.4, .5 + r0 / 40)), f(alpha)))
    return e1, e2

def scales(out, rng, P, N, rad, spacing_um, margin, alpha=1.0, sh=0.0, stroke=None):
    """the cuticle: the free edges of the scales, crossing the hair and leaning toward its tip"""
    step = spacing_um * PX
    seg, nxt = 0.0, step * rng.uniform(0.3, 1.0)
    jit = {'smooth': .08, 'flat': .1, 'faint': .18, 'wavy': .3, 'jagged': .35}[margin]
    op = {'smooth': .55, 'flat': .22, 'faint': .3, 'wavy': .5, 'jagged': .7}[margin]
    sk = ' stroke="%s"' % stroke if stroke else ''
    for k in range(1, len(P)):
        seg += math.hypot(P[k][0] - P[k - 1][0], P[k][1] - P[k - 1][1])
        if seg < nxt:
            continue
        seg, nxt = 0.0, step * rng.uniform(1 - jit, 1 + jit)
        (x, y), (nx, ny) = P[k], N[k]
        tx, ty = ny, -nx
        r = rad(k) * 0.98
        lean = step * {'smooth': .45, 'flat': .6, 'faint': .4, 'wavy': .45, 'jagged': .35}[margin]
        a = (x + nx * (sh + r), y + ny * (sh + r)); b = (x + nx * (sh - r), y + ny * (sh - r))
        if margin == 'jagged':
            m = 4 + int(r > 40) * 4
            pts = []
            for j in range(m + 1):
                q = 1 - 2 * j / m
                bow = lean * (1 - q * q) * 0.8 + rng.uniform(-.35, .35) * lean
                pts.append((x + nx * (sh + r * q) + tx * bow, y + ny * (sh + r * q) + ty * bow))
            out.append('<path d="%s"%s stroke-width=".7" stroke-opacity="%s"/>' % (poly(pts), sk, f(op * alpha)))
            # the scale edges stand proud of the outline
            for s in (1, -1):
                ex, ey = x + nx * (sh + s * r), y + ny * (sh + s * r)
                out.append('<path d="M%s %sL%s %s" stroke-width=".8" stroke-opacity="%s"/>' % (
                    f(ex), f(ey), f(ex + nx * s * 1.6 + tx * 2.4), f(ey + ny * s * 1.6 + ty * 2.4), f(op * alpha)))
        elif margin == 'wavy':
            m = 6 if r > 30 else 3
            pts = []
            for j in range(m + 1):
                q = 1 - 2 * j / m
                bow = lean * (1 - q * q) * 0.7 + (rng.uniform(-.3, .3) * lean if 0 < j < m else 0)
                pts.append((x + nx * (sh + r * q) + tx * bow, y + ny * (sh + r * q) + ty * bow))
            out.append('<path d="%s"%s stroke-width="%s" stroke-opacity="%s"/>' % (poly(pts), sk, '.6' if r < 30 else '1', f(op * alpha)))
        else:
            c1 = (x + nx * (sh + r * .4) + tx * lean, y + ny * (sh + r * .4) + ty * lean)
            c2 = (x + nx * (sh - r * .4) + tx * lean, y + ny * (sh - r * .4) + ty * lean)
            out.append('<path d="M%s %sC%s %s %s %s %s %s"%s stroke-width=".55" stroke-opacity="%s"/>' % (
                f(a[0]), f(a[1]), f(c1[0]), f(c1[1]), f(c2[0]), f(c2[1]), f(b[0]), f(b[1]), sk, f(op * alpha)))

def medulla(out, rng, P, N, rad, share, kind, col, alpha=1.0):
    c = [(x, y) for (x, y), _ in zip(P, N)]
    w = max(1.2, rad(0) * 2 * share)
    dash = '' if kind == 'solid' else ' stroke-dasharray="%s"' % ' '.join(f(rng.uniform(14, 60)) for _ in range(8))
    out.append('<path d="%s" stroke="%s" stroke-width="%s" stroke-opacity="%s"%s/>' % (poly(c), shade(col, -.5) if kind == 'broken' else shade(col, .22), f(w), f(.45 * alpha), dash))

def hair(rng, angle):
    """a human hair, about 70 µm, pale, behind the fibre: the yardstick"""
    out = ['<g stroke="%s" opacity=".62">' % shade(HAIR, -.45)]
    r = 70 * PX / 2
    pts, nrm = strand(rng, angle, rng.uniform(-90, 90), 20)
    P, N = clip(pts, nrm, r + 60)
    rad = lambda k: r
    body(out, P, N, rad, HAIR, alpha=.8)
    scales(out, rng, P, N, rad, 8, 'wavy', alpha=.55)
    medulla(out, rng, P, N, rad, .22, 'broken', HAIR, alpha=.6)
    out.append('</g>')
    return out

def draw(slug):
    st = STYLE[slug]
    rng = random.Random(sum(map(ord, slug)) * 7 + 3)
    col = COLOR.get(slug, '#EDE6DA')
    dark = sum(int(col[i:i + 2], 16) for i in (1, 3, 5)) < 330
    ink = shade(col, -.62 if not dark else -.5)
    base = math.radians(rng.choice([-30, -24, 22, 28]))
    groups = []
    groups.append(hair(rng, base + math.radians(rng.choice([-52, 50]))))
    n, r0 = st['n'], st['d'] * PX / 2
    spread = min(R * 1.5, max(r0 * 2.6 * n, 260))
    for i in range(n):
        a0 = base + math.radians(rng.uniform(-9, 9))
        off = (i - (n - 1) / 2) * spread / max(1, n - 1) + rng.uniform(-r0, r0) * 0.6 if n > 1 else rng.uniform(-40, 40)
        pts, nrm = strand(rng, a0, off, st.get('bend', 40))
        P, N = clip(pts, nrm, r0 * 1.2 + 60)
        if not P:
            continue
        rr = r0 * rng.uniform(0.9, 1.1)
        if st.get('twist'):
            tw = st['twist'] * PX
            ph = rng.uniform(0, tw)
            def rad(k, rr=rr, tw=tw, ph=ph):
                return rr * (0.42 + 0.58 * abs(math.cos(math.pi * (k * 4 + ph) / tw)))
        elif st.get('lumen'):
            ph = rng.uniform(0, 6.28)
            def rad(k, rr=rr, ph=ph):
                return rr * (1 + 0.1 * math.sin(k * 0.05 + ph))
        else:
            def rad(k, rr=rr):
                return rr
        back = n > 3 and i in (0, n - 1) and rng.random() < 0.5
        g = ['<g stroke="%s"%s>' % (ink, ' opacity=".6" filter="url(#b)"' if back else '')]
        reps = [0.0] if not st.get('pair') else [-rr * 1.02, rr * 1.02]
        if st.get('pair'):
            # the gum that binds the pair, a faint coat around both
            g.append('<path d="%s" stroke="%s" stroke-width="%s" stroke-opacity=".16"/>' % (poly(P), shade(col, -.2), f(rr * 4.6)))
        for sh in reps:
            body(g, P, N, rad, col, sh=sh, sheen=st.get('sheen'))
            if st.get('scale'):
                scales(g, rng, P, N, rad, st['scale'], st['margin'], sh=sh, stroke=shade(col, .5) if dark else None)
        if st.get('core') and (st.get('core_kind') == 'solid' or rng.random() < st.get('core_share', 1)):
            medulla(g, rng, P, N, rad, st['core'], st.get('core_kind', 'solid'), col)
        if st.get('lumen'):
            g.append('<path d="%s" stroke-width=".7" stroke-opacity=".38"/>' % poly(P))
        if st.get('nodes'):
            seg = 0.0
            for k in range(1, len(P)):
                seg += math.hypot(P[k][0] - P[k - 1][0], P[k][1] - P[k - 1][1])
                if seg >= st['nodes'] * PX * rng.uniform(0.6, 1.5):
                    seg = 0
                    (x, y), (nx, ny) = P[k], N[k]
                    r = rad(k); tx, ty = ny, -nx; dd = r * 0.55
                    g.append('<path d="M%s %sL%s %sM%s %sL%s %s" stroke-width=".8" stroke-opacity=".7"/>' % (
                        f(x + nx * r - tx * dd), f(y + ny * r - ty * dd), f(x - nx * r + tx * dd), f(y - ny * r + ty * dd),
                        f(x + nx * r + tx * dd), f(y + ny * r + ty * dd), f(x - nx * r - tx * dd), f(y - ny * r - ty * dd)))
        if st.get('twist'):
            tw = st['twist'] * PX
            for k in range(1, len(P)):
                if rad(k) < rad(k - 1) and rad(k) <= rad(min(len(P) - 1, k + 1)):
                    (x, y), (nx, ny) = P[k], N[k]
                    r = rad(k) + 1.5; tx, ty = ny, -nx
                    g.append('<path d="M%s %sL%s %s" stroke-width=".7" stroke-opacity=".7"/>' % (
                        f(x + nx * r + tx * 5), f(y + ny * r + ty * 5), f(x - nx * r - tx * 5), f(y - ny * r - ty * 5)))
            # the thickened edges of the collapsed ribbon
            for q in (.72, -.72):
                g.append('<path d="%s" stroke-width=".5" stroke-opacity=".4"/>' % poly([(x + nx * rad(k) * q, y + ny * rad(k) * q) for k, ((x, y), (nx, ny)) in enumerate(zip(P, N))]))
        if st.get('ridges'):
            m = st['ridges']
            for j in range(1, m):
                q = -1 + 2 * j / m
                g.append('<path d="%s" stroke-width=".7" stroke-opacity=".45"/>' % poly([(x + nx * rad(k) * q, y + ny * rad(k) * q) for k, ((x, y), (nx, ny)) in enumerate(zip(P, N))]))
        if st.get('striae'):
            for q in [(-1 + 2 * (j + 1) / (st['striae'] + 1)) * .6 for j in range(st['striae'])]:
                g.append('<path d="%s" stroke-width=".45" stroke-opacity=".35"/>' % poly([(x + nx * rad(k) * q, y + ny * rad(k) * q) for k, ((x, y), (nx, ny)) in enumerate(zip(P, N))]))
        g.append('</g>')
        groups.append(g)
    # the blurred strands lie behind the sharp ones; the hair first of all
    order = [groups[0]] + sorted(groups[1:], key=lambda g: 0 if 'filter=' in g[0] else 1)
    # 100 µm, at the head of the field, clear of the caption that the page lays over its foot
    by, bx0, bx1 = 182, CX - 50 * PX, CX + 50 * PX
    bar = ('<rect x="%s" y="%s" width="%s" height="46" rx="4" fill="#FBF6EC" fill-opacity=".82"/>' % (f(CX - 66 * PX), by - 40, f(132 * PX))) + ('<g stroke="#4A3F34" stroke-width="2" stroke-linecap="butt"><path d="M%s %sH%s"/><path d="M%s %sv-12M%s %sv-12" stroke-width="1.5"/></g>'
           '<text x="%s" y="%s" text-anchor="middle" font-family="Georgia, \'Times New Roman\', serif" font-size="22" fill="#4A3F34" letter-spacing="1">100 µm</text>') % (
        f(bx0), by, f(bx1), f(bx0), by + 6, f(bx1), by + 6, f(CX), by - 16)
    field = ('<defs><radialGradient id="f" cx=".5" cy=".5" r=".6"><stop offset="0" stop-color="%s"/><stop offset=".7" stop-color="%s"/><stop offset="1" stop-color="%s"/></radialGradient>'
             '<filter id="b" x="-10%%" y="-10%%" width="120%%" height="120%%"><feGaussianBlur stdDeviation="2.6"/></filter></defs>'
             '<rect width="%d" height="%d" fill="url(#f)"/>' % (FIELD[0], FIELD[1], FIELD[2], W, H))
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" preserveAspectRatio="xMidYMid slice">%s'
            '<g fill="none" stroke-linecap="round" stroke-linejoin="round">%s</g>%s</svg>' % (W, H, field, ''.join(''.join(g) for g in order), bar))


if __name__ == '__main__':
    import sys, os
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    for slug in STYLE:
        s = draw(slug)
        open(os.path.join(out, 'ms-fibre-draw-%s.svg' % slug), 'w').write(s)
        print(slug, len(s))
