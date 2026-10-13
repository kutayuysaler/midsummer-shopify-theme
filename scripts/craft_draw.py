"""Inside the bed, drawn for each system: its own cloths, ribbons, stitching, legs, drawers or round
shape, from the 2026 catalogue's fittings and the house's photographs. The parts a mattress or a
topper does not include are drawn as a light outline. Nothing of the inside is drawn.

drawing(key) returns the SVG for snippets/ms-craft-svg.liquid, with {{U}} for the section id and
[t1] [t2] [t3] for the three parts' names; the structure and classes are those ms-craft expects."""
import colorsys
from lp_data import CRAFT_PARTS as PARTS, CRAFT_OPT as OPT

PINK, ORANGE, BEIGE, VICUNA, CARAMEL, RED = '#E2A49B', '#D2643C', '#CBB596', '#B4875B', '#A87648', '#9E2A33'
IVORY, LINEN, RAW = '#F3EEE4', '#E3D9C8', '#D9CDB8'


def shade(hexc, l=0.0, s=0.0):
    h = hexc.lstrip('#')
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    hh, ll, ss = colorsys.rgb_to_hls(r, g, b)
    ll = max(0, min(1, ll + l))
    ss = max(0, min(1, ss + s))
    r, g, b = colorsys.hls_to_rgb(hh, ll, ss)
    return '#%02X%02X%02X' % (round(r * 255), round(g * 255), round(b * 255))


def P(col, h, **kw):
    d = dict(col=col, h=h)
    d.update(kw)
    return d


# per system: topper, mattress, base. ribbon: the edge ribbon; rows: hand side stitching;
# band: a coloured band on the mattress (Top's coral, Brera's Altai edge); legs: wood, leather,
# fabric (covered in the cloth), none; drawers: upholstered drawers; pattern: paisley, boucle
SYS = {
    'essenziale': dict(topper=P(IVORY, 18), mattress=P(IVORY, 50, ribbon=PINK, rows=2), base=P(LINEN, 44)),
    'raffaello': dict(topper=P(IVORY, 18), mattress=P(IVORY, 62, ribbon=PINK, rows=3, handles=True), base=P(LINEN, 48)),
    'amalfi': dict(topper=P('#C9D3D6', 20, ribbon='#7E98A3'), mattress=P('#BCC9CD', 56, rows=2), base=P('#8FA6AF', 48)),
    'capri': dict(topper=P('#CFC4B7', 22, ribbon=PINK), mattress=P('#EDE7DE', 58, rows=3, handles=True), base=P('#B8A18F', 48)),
    'bellagio': dict(topper=P(RAW, 18), mattress=P(RAW, 60, ribbon=ORANGE, rows=2, rowcol=ORANGE), base=P(LINEN, 48)),
    'vivaldi-2': dict(topper=P(IVORY, 18), mattress=P(LINEN, 62, ribbon=PINK, rows=3, handles=True), base=P('#D5C9B5', 48)),
    'vivaldi-plus': dict(topper=P(IVORY, 18), mattress=P(LINEN, 66, ribbon=PINK, rows=4, handles=True), base=P('#CBBDA7', 48)),
    'monteverdi': dict(topper=P(RAW, 18), mattress=P('#D6CAB4', 58, ribbon=BEIGE, rows=2), base=P('#C9BBA2', 48)),
    'ultra-dry': dict(topper=P(RAW, 18), mattress=P(RAW, 60, ribbon=PINK, rows=2), base=P(LINEN, 48)),
    'dreamy-2': dict(topper=P('#CFCBC6', 24, ribbon=PINK), mattress=P('#EDE9E3', 60, rows=3, handles=True), base=P('#A2B2B9', 48)),
    'brera': dict(topper=P('#F2EFEA', 22), mattress=P('#F2EFEA', 30, band='#191A2F', rows=1), base=P('#B8A18F', 34, legs='leather')),
    'roma': dict(topper=P(IVORY, 18), mattress=P(IVORY, 62, ribbon=PINK, rows=3, handles=True), base=P('#A19793', 48)),
    'dreamy-springs': dict(topper=P(IVORY, 18), mattress=P('#EFEBE4', 66, ribbon=PINK, rows=4, handles=True), base=P('#BCAF9C', 48)),
    'my-dream': dict(topper=P(IVORY, 18), mattress=P('#F5F2EC', 56, ribbon=PINK, rows=2), base=P(LINEN, 46)),
    'bellini': dict(topper=P('#E9E2D6', 22, ribbon='#CDBFA9', pattern='boucle'), mattress=P('#F1ECE4', 58, rows=3, handles=True), base=P('#D9CFC0', 48, pattern='boucle')),
    'giotto': dict(shape='round', topper=P('#F1ECE3', 16, ribbon='#B98A47'), mattress=P('#EEE8DE', 40, rows=2), base=P('#B98A47', 52, legs='none', pattern='linen')),
    'vicuna': dict(topper=P(IVORY, 18), mattress=P('#F6F3EE', 66, ribbon=VICUNA, rows=4, handles=True), base=P('#A87A50', 50)),
    'flora': dict(topper=P('#D8CDBB', 24, ribbon='#B9A27F'), mattress=P('#EFE9E0', 58, rows=3, handles=True), base=P('#CFC3B1', 48, pattern='boucle')),
    'top-2': dict(topper=P('#F4F0E9', 26, ribbon='#C55A48'), mattress=P('#F1ECE4', 58, band='#C55A48', rows=3, handles=True), base=P('#B54A3F', 50, legs='fabric')),
    'storage': dict(topper=P('#CFC4B7', 20, ribbon=PINK), mattress=P('#EDE7DE', 54, rows=3, handles=True), base=P('#BCAF9C', 56, legs='none', drawers=2)),
    'paisley': dict(topper=P('#F3EDE5', 22, ribbon=RED), mattress=P('#F1EBE3', 58, ribbon=RED, rows=2, handles=True), base=P('#9B2B32', 50, pattern='paisley')),
    'topper-roma': dict(topper=P('#E4DCCF', 22, ribbon=PINK), mattress=P(IVORY, 58), base=P(LINEN, 48)),
    'topper-high': dict(topper=P('#E9E2D6', 26, ribbon='#CDBFA9'), mattress=P(IVORY, 58), base=P(LINEN, 48)),
    'topper-thin': dict(topper=P(IVORY, 12), mattress=P(IVORY, 58), base=P(LINEN, 48)),
    'first-dream': dict(topper=P(IVORY, 18), mattress=P('#F2EEE7', 50, ribbon=CARAMEL, rows=2), base=P(LINEN, 44)),
}
GENERIC = dict(topper=P('#F6EEE6', 22), mattress=P('#F5ECE3', 62), base=P('#D2A28C', 50))

X0, W, DX, DY = 40.0, 360.0, 129.9, -75.0
TOPS = {'topper': 128.0, 'mattress': 222.0, 'base': 330.0}     # front top edge of each part, as drawn today
NUM = {'topper': 'I', 'mattress': 'II', 'base': 'III'}
LABEL = {'topper': '[t1]', 'mattress': '[t2]', 'base': '[t3]'}


def f(v):
    return ('%.1f' % v).rstrip('0').rstrip('.')


def mix(a, b, t):
    """a blended toward b by t (0: a, 1: b)"""
    pa = [int(a.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4)]
    pb = [int(b.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4)]
    return '#%02X%02X%02X' % tuple(round(x + (y - x) * t) for x, y in zip(pa, pb))


def cfg_of(key):
    """a system's parts; a boxspring (base-<system>) is drawn as that system's base"""
    if key.startswith('base-'):
        key = key[5:]
    return SYS.get(key, GENERIC)


def tint(key):
    """the section's ground for a system: the house's warm paper, touched by the colour of its base"""
    cfg = cfg_of(key)
    c = cfg['base']['col']
    return '--cr-g1:%s;--cr-g2:%s;--cr-g3:%s' % (mix(c, '#F2E8E0', .9), mix(c, '#E8DCD1', .86), mix(c, '#DDCEC1', .82))


def grads(part, col, u, round_=False):
    """the light on each face: from the top left, soft, as on paper"""
    ink = shade(col, -.26)
    g = []
    g.append('<linearGradient id="cr-%s-%s-t" x1="0" y1="1" x2="1" y2="0"><stop offset="0" stop-color="%s"/><stop offset="1" stop-color="%s"/></linearGradient>' % (u, part, shade(col, .075), shade(col, .025)))
    if round_:
        stops = ((0, -.15), (.16, -.05), (.4, .045), (.66, -.01), (.9, -.1), (1, -.16))
        g.append('<linearGradient id="cr-%s-%s-f" x1="0" y1="0" x2="1" y2="0">%s</linearGradient>' % (u, part, ''.join('<stop offset="%s" stop-color="%s"/>' % (o, shade(col, d)) for o, d in stops)))
        g.append('<radialGradient id="cr-%s-%s-r" cx=".42" cy=".38" r=".7"><stop offset="0" stop-color="%s"/><stop offset="1" stop-color="%s"/></radialGradient>' % (u, part, shade(col, .09), shade(col, .01)))
    else:
        g.append('<linearGradient id="cr-%s-%s-f" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="%s"/><stop offset=".14" stop-color="%s"/><stop offset=".86" stop-color="%s"/><stop offset="1" stop-color="%s"/></linearGradient>' % (u, part, shade(col, .06), col, shade(col, -.035), shade(col, -.085)))
    g.append('<linearGradient id="cr-%s-%s-s" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="%s"/><stop offset="1" stop-color="%s"/></linearGradient>' % (u, part, shade(col, -.085), shade(col, -.14)))
    return ''.join(g), ink


def patterns(part, p, u):
    """the cloth, as a fine texture: linen's weave, bouclé's loops, Paisley's own motif; one for the
    front, one sheared for the side so the texture follows the face"""
    kind = p.get('pattern') or ('weave' if part == 'base' else '')
    if not kind:
        return '', ''
    ink = shade(p['col'], .14 if kind == 'paisley' else -.2)
    if kind == 'paisley':
        cell = ('<path d="M11,23c-7-3-6.5-14 1.5-15.5c7.5-1.4 11 5.5 7 10c-2.6 3-6.6 2.2-6-1.2c.4-2.4 3.4-2.6 3.6-.6" fill="none" stroke="%s" stroke-width=".7" stroke-linecap="round"/>'
                '<path d="M11,23c-3,2-6,5-5,8" fill="none" stroke="%s" stroke-width=".7" stroke-linecap="round"/><circle cx="26" cy="9" r=".9" fill="%s"/><circle cx="29" cy="25" r=".7" fill="%s"/>'
                '<path d="M30,3c-2.5,1-2.5,4 0,5c2.5-1 2.5-4 0-5z" fill="none" stroke="%s" stroke-width=".6"/>') % (ink, ink, ink, ink, ink)
        w, h, op = 34, 32, .55
    elif kind == 'boucle':
        cell = '<circle cx="2" cy="2" r=".9" fill="%s"/><circle cx="5.5" cy="5" r=".9" fill="%s"/>' % (ink, ink)
        w, h, op = 7, 6, .4
    elif kind == 'linen':
        cell = '<path d="M0,1.5h6M0,4h6" stroke="%s" stroke-width=".35"/><path d="M1.5,0v6M4.5,0v6" stroke="%s" stroke-width=".2"/>' % (ink, ink)
        w, h, op = 6, 5, .45
    else:   # a close weave
        cell = '<path d="M0,2h4M2,0v4" stroke="%s" stroke-width=".3"/>' % ink
        w, h, op = 4, 4, .28
    out = ''
    for nm, tr in (('pf', ''), ('ps', ' patternTransform="matrix(1 %s 0 1 0 0)"' % f(DY / DX))):
        out += '<pattern id="cr-%s-%s-%s" width="%s" height="%s" patternUnits="userSpaceOnUse"%s><g opacity="%s">%s</g></pattern>' % (u, part, nm, w, h, tr, op, cell)
    return out, kind


def lerp(a, b, t):
    return a + (b - a) * t


LX = 570.0     # the label column


def label(part, x, y, ghost=False, num=None, note='[t0]'):
    """a hairline from the part to its numeral and name, as on an architect's drawing; a part the
    product does not include (or that is optional) says so beneath its name"""
    nm = LABEL[part]
    if num and part != 'topper':
        # a part in one piece with another has a longer name: on two lines, broken at "and"
        v = 't2' if part == 'mattress' else 't3'
        nm = ('{%%- assign tw = %s | split: \' and \' -%%}{%%- if tw.size > 1 -%%}<tspan x="%s" dy="-7">{{ tw[0] | escape }} and</tspan><tspan x="%s" dy="14">{{ tw[1] | escape }}</tspan>'
              '{%%- else -%%}{{ %s | escape }}{%%- endif -%%}') % (v, f(LX + 26), f(LX + 26), v)
    out = ('<g class="ms-cr__lbl" pointer-events="none"><path class="ms-cr__lead" d="M%s,%s H%s"/><circle class="ms-cr__dot" cx="%s" cy="%s" r="1.6"/>'
           '<text x="%s" y="%s" class="ms-cr__num">%s</text><text x="%s" y="%s" class="ms-cr__nm">%s</text>'
           % (f(x), f(y), f(LX - 6), f(x), f(y), f(LX), f(y + 5), num or NUM[part], f(LX + 26), f(y + 4.5), nm))
    if ghost:
        out += '<text x="%s" y="%s" class="ms-cr__abs">%s</text>' % (f(LX + 26), f(y + 21), note)
    return out + '</g>'


def box(part, p, u, kind, gap=0.0, pat='', inner=False):
    """one part of a rectangular bed, seen from above and to the side"""
    y0 = p.get('y0', TOPS[part])
    h = p['h']
    if part == 'base':
        y0 = 380.0 - h
    x1 = X0 + W
    col = p['col']
    ink = shade(col, -.3)
    g = []
    opt = p.get('opt', False)
    ghost = (kind != 'system' and part != kind) or opt
    cls = 'ms-cr__slab' + (' is-ghost' if ghost else '') + (' is-opt' if opt else '')
    if not inner:
        g.append('<g class="%s" data-part="%s" tabindex="0" role="button" aria-label="%s" aria-controls="cr-{{U}}-%s" aria-expanded="false">' % (cls, part, LABEL[part], part))
    # legs first, so the base sits on them
    if part == 'base' and not ghost:
        legs = p.get('legs', 'wood')
        if legs == 'wood':
            for lx, ly in ((X0 + 16, y0 + h), (x1 - 24, y0 + h), (x1 + DX - 20, y0 + h + DY)):
                g.append('<path d="M%s,%s h10 l-1.6,10 c-.3,2.2 -1,3.2 -2.2,3.6 h-3 c-1.2,-.4 -1.9,-1.4 -2.2,-3.6 Z" fill="url(#cr-{{U}}-wood)"/>'
                         '<path d="M%s,%s v11" stroke="rgba(255,240,220,.35)" stroke-width=".8"/>' % (f(lx - 5), f(ly), f(lx - 1.5), f(ly + 1)))
        elif legs == 'leather':
            for lx, ly in ((X0 + 18, y0 + h), (x1 - 28, y0 + h), (x1 + DX - 24, y0 + h + DY)):
                g.append('<path d="M%s,%s h9 l-1.4,19 h-6.2 Z" fill="#8E6141"/><path d="M%s,%s h7.6" stroke="#C99B6D" stroke-width="1"/>' % (f(lx - 4.5), f(ly), f(lx - 3.8), f(ly + 6)))
        elif legs == 'fabric':
            lc = shade(col, -.07)
            for lx in (X0 + 10, x1 - 36):
                g.append('<rect x="%s" y="%s" width="26" height="13" fill="%s"/>' % (f(lx), f(y0 + h - 1), lc))
            g.append('<path d="M%s,%s l14,-8 v13 l-14,8 Z" fill="%s"/>' % (f(x1 + DX - 30), f(y0 + h + DY - 1), shade(lc, -.08)))
    side = 'M%s,%s L%s,%s L%s,%s L%s,%s Z' % (f(x1), f(y0), f(x1 + DX), f(y0 + DY), f(x1 + DX), f(y0 + DY + h), f(x1), f(y0 + h))
    front = 'M%s,%s L%s,%s L%s,%s Q%s,%s %s,%s Z' % (f(X0), f(y0), f(x1), f(y0), f(x1), f(y0 + h), f((X0 + x1) / 2), f(y0 + h + 2), f(X0), f(y0 + h))
    top = 'M%s,%s L%s,%s L%s,%s L%s,%s Z' % (f(X0), f(y0), f(x1), f(y0), f(x1 + DX), f(y0 + DY), f(X0 + DX), f(y0 + DY))
    stroke = ''
    g.append('<path class="ms-cr__face ms-cr__face--side" fill="url(#cr-{{U}}-%s-s)"%s d="%s"/>' % (part, stroke, side))
    g.append('<path class="ms-cr__face" fill="url(#cr-{{U}}-%s-f)"%s d="%s"/>' % (part, stroke, front))
    if not ghost and pat:
        g.append('<path fill="url(#cr-{{U}}-%s-pf)" d="%s" pointer-events="none"/><path fill="url(#cr-{{U}}-%s-ps)" d="%s" pointer-events="none"/>' % (part, front, part, side))
    g.append('<path class="ms-cr__face ms-cr__face--top" fill="url(#cr-{{U}}-%s-t)"%s d="%s"/>' % (part, stroke, top))
    if part != 'topper' and not ghost:
        sx, sy = X0 + 26, y0 - 4
        g.append('<path class="ms-cr__cast" d="M%s,%s L%s,%s L%s,%s L%s,%s Z" filter="url(#cr-{{U}}-soft)"/>' % (
            f(sx), f(sy), f(x1 - 14), f(sy), f(x1 + DX - 30), f(sy + DY + 10), f(sx + DX - 8), f(sy + DY + 10)))
    if not ghost:
        # a soft roll along the front top edge, where the cloth turns over
        g.append('<path d="M%s,%s L%s,%s L%s,%s" fill="none" stroke="rgba(255,255,255,.5)" stroke-width="1.2"/>' % (f(X0 + 2), f(y0 + 1.6), f(x1 - 1), f(y0 + 1.6), f(x1 + DX - 2), f(y0 + DY + 1.6)))
        def at(uu, vv):
            return X0 + uu * W + vv * DX, y0 + vv * DY
        fold = shade(col, -.17)
        if part == 'mattress':
            # capitonné: buttons on a grid that follows the top, joined by the folds of the cloth
            nu, nv = 6, 3
            pts = {}
            for j in range(nv):
                for i in range(nu):
                    uu = (i + .5 + (.5 if j % 2 else 0)) / (nu + .5)
                    vv = (j + .7) / (nv + .4)
                    pts[(i, j)] = at(uu, vv)
            folds = []
            for (i, j), (x, y) in pts.items():
                for di in (0, 1):
                    q = pts.get((i + di - (0 if j % 2 else 1), j + 1)) if j % 2 == 0 else pts.get((i + di, j + 1))
                    if q:
                        folds.append('M%s,%s L%s,%s' % (f(x), f(y), f(q[0]), f(q[1])))
            g.append('<path d="%s" stroke="%s" stroke-width=".7" stroke-opacity=".32" fill="none"/>' % (' '.join(folds), fold))
            for (x, y) in pts.values():
                g.append('<ellipse cx="%s" cy="%s" rx="3.6" ry="2" fill="%s" fill-opacity=".22"/><ellipse class="ms-cr__tuft" style="fill: %s" cx="%s" cy="%s" rx="1.5" ry=".85"/><ellipse cx="%s" cy="%s" rx="1.6" ry=".6" fill="#fff" fill-opacity=".6"/>' % (f(x), f(y), fold, shade(col, -.2), f(x), f(y + .2), f(x - 1.6), f(y - 1.2)))
            # hand stitching round the border, in rows
            rows = p.get('rows', 2)
            rc = p.get('rowcol') or shade(col, -.34)
            for r in range(rows):
                yy = y0 + 6 + (h - 12) * (r + 1) / (rows + 1)
                g.append('<path d="M%s,%s L%s,%s L%s,%s" fill="none" stroke="%s" stroke-width="1.1" stroke-linecap="round" stroke-dasharray=".1 4.2" stroke-opacity=".75"/>' % (f(X0 + 6), f(yy), f(x1 - 3), f(yy), f(x1 + DX - 5), f(yy + DY), rc))
            # the house label, on the front
            lx, ly = x1 - 74, y0 + h * .5 - 6
            g.append('<rect x="%s" y="%s" width="30" height="12" rx="1" fill="%s" stroke="%s" stroke-width=".6"/><path d="M%s,%s h18" stroke="%s" stroke-width=".7"/>' % (f(lx), f(ly), shade(col, .05), shade(col, -.22), f(lx + 6), f(ly + 6), shade(col, -.3)))
            if p.get('handles'):
                hx, hy = x1 + DX * .5, y0 + DY * .5 + h * .5
                # a fabric handle, lying along the side
                L = 22 / (DX * DX + DY * DY) ** .5
                ux, uy = DX * L, DY * L
                g.append('<path d="M%s,%s l%s,%s v6 l%s,%s Z" fill="%s" stroke="%s" stroke-width=".7"/>' % (f(hx - ux / 2), f(hy - 3 - uy / 2), f(ux), f(uy), f(-ux), f(-uy), shade(col, -.06), shade(col, -.28)))
        if part == 'topper':
            # quilted by hand: a light diamond of stitches over the top
            lines = []
            for i in range(-3, 9):
                a, b = at(i / 6, 0), at(i / 6 + .5, 1)
                c, d = at(i / 6, 0), at(i / 6 - .5, 1)
                lines.append('M%s,%s L%s,%s M%s,%s L%s,%s' % (f(a[0]), f(a[1]), f(b[0]), f(b[1]), f(c[0]), f(c[1]), f(d[0]), f(d[1])))
            g.append('<clipPath id="cr-{{U}}-qc"><path d="%s"/></clipPath><path clip-path="url(#cr-{{U}}-qc)" d="%s" fill="none" stroke="%s" stroke-width=".7" stroke-dasharray="2.2 2.6" stroke-opacity=".45"/>' % (top, ' '.join(lines), fold))
        if p.get('band'):
            bt = 5 if part == 'topper' else 8
            yb = y0 + (5 if part == 'topper' else h * .36)
            g.append('<path d="M%s,%s L%s,%s L%s,%s L%s,%s L%s,%s L%s,%s Z" fill="%s"/>' % (f(X0), f(yb), f(x1), f(yb), f(x1 + DX), f(yb + DY), f(x1 + DX), f(yb + DY + bt), f(x1), f(yb + bt), f(X0), f(yb + bt), p['band']))
        if part == 'base' and p.get('drawers'):
            n = p['drawers']
            wdr = (W - 30) / n
            for i in range(n):
                dx0 = X0 + 12 + i * (wdr + 6)
                g.append('<rect x="%s" y="%s" width="%s" height="%s" rx="1.5" fill="%s" fill-opacity=".25" stroke="%s" stroke-width=".8"/>' % (f(dx0), f(y0 + 10), f(wdr), f(h - 18), shade(col, .08), shade(col, -.24)))
                g.append('<path d="M%s,%s h22" stroke="%s" stroke-width="2" stroke-linecap="round"/>' % (f(dx0 + wdr / 2 - 11), f(y0 + 10 + (h - 18) / 2), shade(col, -.34)))
        if part == 'base':
            # the welt where the upholstery turns over the top
            g.append('<path d="M%s,%s L%s,%s L%s,%s" fill="none" stroke="%s" stroke-width="1" stroke-opacity=".7"/>' % (f(X0 + 2), f(y0 + 9), f(x1 - 1), f(y0 + 9), f(x1 + DX - 2), f(y0 + 9 + DY), shade(col, -.2)))
        rib = p.get('ribbon')
        if rib:
            for yy in ((y0, y0 + h) if part != 'base' else (y0,)):
                g.append('<path d="M%s,%s L%s,%s L%s,%s" fill="none" stroke="%s" stroke-width=".8" stroke-opacity=".5"/><path class="ms-cr__pipe" style="stroke: %s; stroke-width: 2.2" d="M%s,%s L%s,%s L%s,%s"/>' % (
                    f(X0), f(yy + 1.4), f(x1), f(yy + 1.4), f(x1 + DX), f(yy + DY + 1.4), shade(rib, -.25), rib, f(X0), f(yy), f(x1), f(yy), f(x1 + DX), f(yy + DY)))
        # the exploded view's guides: from this part's lower corners down to the next
        if gap > 6:
            gl = []
            for (x, y) in ((X0, y0 + h), (x1, y0 + h), (x1 + DX, y0 + h + DY)):
                gl.append('M%s,%s v%s' % (f(x), f(y + 4), f(gap - 8)))
            g.append('<path class="ms-cr__guide" d="%s" stroke="%s" stroke-width=".7" stroke-dasharray="1.5 3.5" stroke-opacity=".5" fill="none" pointer-events="none"/>' % (' '.join(gl), shade(col, -.35)))
    if inner:
        return ''.join(g)
    ly = y0 + DY + (p.get('ly') if p.get('ly') is not None else h * .5)
    g.append(label(part, x1 + DX + 6, ly, ghost, p.get('num'), '[to]' if opt else '[t0]'))
    g.append('</g>')
    return ''.join(g)


def cyl(part, p, u, kind, gap=0.0, pat='', inner=False):
    """one part of a round bed: a shaded cylinder, its top lit from the left"""
    import math
    CX, RX, RY = 285.0, 222.0, 58.0
    CY = p.get('y0', {'topper': 82.0, 'mattress': 176.0, 'base': 296.0}[part])
    h = p['h']
    col = p['col']
    fold = shade(col, -.17)
    g = [] if inner else ['<g class="ms-cr__slab" data-part="%s" tabindex="0" role="button" aria-label="%s" aria-controls="cr-{{U}}-%s" aria-expanded="false">' % (part, LABEL[part], part)]
    band = 'M%s,%s A%s,%s 0 0 0 %s,%s V%s A%s,%s 0 0 1 %s,%s Z' % (f(CX - RX), f(CY), f(RX), f(RY), f(CX + RX), f(CY), f(CY + h), f(RX), f(RY), f(CX - RX), f(CY + h))
    st = shade(col, -.22)
    g.append('<path class="ms-cr__face" fill="url(#cr-{{U}}-%s-f)" stroke="%s" d="%s"/>' % (part, st, band))
    if pat:
        g.append('<path fill="url(#cr-{{U}}-%s-pf)" d="%s" pointer-events="none"/>' % (part, band))
    g.append('<ellipse class="ms-cr__face ms-cr__face--top" fill="url(#cr-{{U}}-%s-r)" stroke="%s" cx="%s" cy="%s" rx="%s" ry="%s"/>' % (part, st, f(CX), f(CY), f(RX), f(RY)))
    front_arc = lambda y, k=1.0: 'M%s,%s A%s,%s 0 0 0 %s,%s' % (f(CX - RX * k), f(y), f(RX * k), f(RY * k), f(CX + RX * k), f(y))
    if part == 'topper':
        g.append('<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="none" stroke="%s" stroke-width=".7" stroke-dasharray="2.2 2.6" stroke-opacity=".45"/>' % (f(CX), f(CY), f(RX * .62), f(RY * .62), fold))
        g.append('<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="none" stroke="%s" stroke-width=".7" stroke-dasharray="2.2 2.6" stroke-opacity=".35"/>' % (f(CX), f(CY), f(RX * .3), f(RY * .3), fold))
    if part == 'mattress':
        pts = []
        for ring, n in ((.32, 6), (.66, 12)):
            for a in range(n):
                t = (a + (.5 if ring > .5 else 0)) / n * 2 * math.pi
                pts.append((CX + math.cos(t) * RX * ring, CY + math.sin(t) * RY * ring, t, ring))
        folds = []
        for (x, y, t, ring) in pts:
            folds.append('M%s,%s L%s,%s' % (f(x), f(y), f(CX + math.cos(t) * RX * (ring + .16)), f(CY + math.sin(t) * RY * (ring + .16))))
        g.append('<path d="%s" stroke="%s" stroke-width=".7" stroke-opacity=".3" fill="none"/>' % (' '.join(folds), fold))
        for (x, y, t, ring) in pts:
            g.append('<ellipse cx="%s" cy="%s" rx="3.2" ry="1.7" fill="%s" fill-opacity=".22"/><ellipse class="ms-cr__tuft" style="fill: %s" cx="%s" cy="%s" rx="1.4" ry=".8"/>' % (f(x), f(y), fold, shade(col, -.2), f(x), f(y + .2)))
        rows = p.get('rows', 2)
        for r in range(rows):
            yy = CY + 5 + (h - 10) * (r + 1) / (rows + 1)
            g.append('<path d="%s" fill="none" stroke="%s" stroke-width="1.1" stroke-linecap="round" stroke-dasharray=".1 4.2" stroke-opacity=".75"/>' % (front_arc(yy), shade(col, -.34)))
    if part == 'base':
        # a recessed plinth, so the round base floats a little above the floor
        g.append('<path d="%s" fill="none" stroke="%s" stroke-width="5" stroke-opacity=".35"/>' % (front_arc(CY + h - 3, .985), shade(col, -.3)))
    rib = p.get('ribbon')
    if rib:
        for yy in ((CY,) if part == 'base' else (CY, CY + h)):
            g.append('<path class="ms-cr__pipe" style="stroke: %s; stroke-width: 2.2" d="%s"/>' % (rib, front_arc(yy)))
    if gap > 6:
        gl = ''.join('M%s,%s v%s ' % (f(x), f(CY + h + 4), f(gap - 8)) for x in (CX - RX, CX + RX))
        g.append('<path class="ms-cr__guide" d="%s" stroke="%s" stroke-width=".7" stroke-dasharray="1.5 3.5" stroke-opacity=".5" fill="none" pointer-events="none"/>' % (gl, shade(col, -.35)))
    if inner:
        return ''.join(g)
    g.append(label(part, CX + RX + 8, CY + (p.get('ly') if p.get('ly') is not None else h * .5), num=p.get('num')))
    g.append('</g>')
    return ''.join(g)


PAPER = '#F3EDE4'


def soft(col, by=.16):
    """the cloth's colour as a wash on paper: a little lighter, a little quieter"""
    return shade(mix(col, PAPER, by), 0, -.1)


def drawing(key, kind='system'):
    import copy
    cfg = copy.deepcopy(cfg_of(key))
    for part in ('topper', 'mattress', 'base'):
        pp = cfg[part]
        pp['col'] = soft(pp['col'])
        for k in ('ribbon', 'band', 'rowcol'):
            if pp.get(k):
                pp[k] = soft(pp[k], .1)
    u = '{{U}}'
    round_ = cfg.get('shape') == 'round'
    defs = ['<filter id="cr-%s-blur" x="-20%%" y="-200%%" width="140%%" height="500%%"><feGaussianBlur stdDeviation="8"/></filter>' % u,
            '<filter id="cr-%s-soft" x="-20%%" y="-60%%" width="140%%" height="220%%"><feGaussianBlur stdDeviation="5"/></filter>' % u,
            '<linearGradient id="cr-%s-wood" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#5E3E2A"/><stop offset=".45" stop-color="#8A5E3F"/><stop offset="1" stop-color="#4E3322"/></linearGradient>' % u]
    pats = {}
    for part in ('topper', 'mattress', 'base'):
        gr, _ = grads(part, cfg[part]['col'], u, round_)
        defs.append(gr)
        pd, pk = patterns(part, cfg[part], u)
        defs.append(pd)
        pats[part] = pk
    # how far each part floats above the next, for the guides
    if round_:
        cy = {'topper': 82.0, 'mattress': 176.0, 'base': 296.0}
        gaps = {'topper': cy['mattress'] - (cy['topper'] + cfg['topper']['h']), 'mattress': cy['base'] - (cy['mattress'] + cfg['mattress']['h']), 'base': 0}
    else:
        tops = {'topper': TOPS['topper'], 'mattress': TOPS['mattress'], 'base': 380.0 - cfg['base']['h']}
        gaps = {'topper': tops['mattress'] - (tops['topper'] + cfg['topper']['h']), 'mattress': tops['base'] - (tops['mattress'] + cfg['mattress']['h']), 'base': 0}
    body = []
    shadow = '<ellipse class="ms-cr__shadow" cx="%s" cy="398" rx="%s" ry="12" filter="url(#cr-%s-blur)"/>' % ('285' if round_ else '290', '236' if round_ else '262', u)
    # closed, the bed is whole: the mattress lies on the base, the topper on the mattress
    close = {'base': 0, 'mattress': gaps['mattress'], 'topper': gaps['mattress'] + gaps['topper']}
    depth = {'base': 1, 'mattress': 2.2, 'topper': 3.6}
    delay = {'base': 0, 'mattress': .12, 'topper': .24}
    shown = PARTS.get(key, 'topper,mattress,base').split(',')
    for o in OPT.get(key, '').split(','):
        if o in cfg:
            cfg[o]['opt'] = True
    draw = cyl if round_ else box
    if shown == ['topper', 'base']:
        # the mattress and the boxspring in one piece: drawn as one, the mattress's face over the
        # boxspring's, joined by a single seam; the topper floats above it when opened
        mp, bp = cfg['mattress'], cfg['base']
        if round_:
            bp['y0'] = 296.0 + bp['h'] - (mp['h'] + bp['h'])
            mp['y0'] = bp['y0']
            tot = mp['h'] + bp['h']
            mp_inner = dict(mp, y0=bp['y0'])
            bp_full = dict(bp, h=tot, y0=bp['y0'], num='II', ly=tot * .5)
            whole = draw('base', bp_full, u, kind, 0, pats['base'])
            inside = draw('mattress', mp_inner, u, kind, 0, '', inner=True)
            jy = bp['y0'] + mp['h']
            inside += '<path d="M%s,%s A%s,%s 0 0 0 %s,%s" fill="none" stroke="%s" stroke-width="1.3" stroke-opacity=".8"/>' % (
                f(285.0 - 222.0), f(jy), f(222.0), f(58.0), f(285.0 + 222.0), f(jy), shade(bp['col'], -.28))
            cfg['topper']['y0'] = bp['y0'] - 64.0 - cfg['topper']['h']
            gtop = 64.0
        else:
            tot = mp['h'] + bp['h']
            top = 380.0 - tot
            mp_inner = dict(mp, y0=top)
            bp_full = dict(bp, h=tot, num='II', ly=tot * .5)
            whole = draw('base', bp_full, u, kind, 0, pats['base'])
            inside = draw('mattress', mp_inner, u, kind, 0, '', inner=True)
            # the one seam where the mattress's face meets the boxspring's
            jy = top + mp['h']
            inside += '<path d="M%s,%s L%s,%s L%s,%s" fill="none" stroke="%s" stroke-width="1.3" stroke-opacity=".8"/>' % (
                f(X0), f(jy), f(X0 + W), f(jy), f(X0 + W + DX), f(jy + DY), shade(bp['col'], -.28))
            cfg['topper']['y0'] = top - 70.0 - cfg['topper']['h']
            gtop = 70.0
        i = whole.index('<g class="ms-cr__lbl"')
        whole = whole[:i] + inside + whole[i:]
        cfg['topper']['num'] = 'I'
        tp = draw('topper', cfg['topper'], u, kind, gtop, pats['topper'])
        for part, s, c in (('base', whole, 0), ('topper', tp, gtop)):
            s = s.replace('<g class="ms-cr__slab', '<g style="--cr-c: %spx; --cr-delay: %ss" class="ms-cr__slab' % (f(c), delay[part]), 1)
            body.append('<g class="ms-cr__depth" style="--d: %s">%s</g>' % (depth[part], s))
    else:
        if shown == ['mattress', 'base']:
            cfg['mattress']['num'], cfg['base']['num'] = 'I', 'II'
        for part in ('base', 'mattress', 'topper'):
            if part not in shown:
                continue
            s = draw(part, cfg[part], u, kind, gaps[part], pats[part])
            s = s.replace('<g class="ms-cr__slab', '<g style="--cr-c: %spx; --cr-delay: %ss" class="ms-cr__slab' % (f(close[part]), delay[part]), 1)
            body.append('<g class="ms-cr__depth" style="--d: %s">%s</g>' % (depth[part], s))
    return ('<svg class="ms-cr__svg" viewBox="0 0 700 440" role="group" aria-label="[aria]"><defs>%s</defs>%s%s</svg>' % (''.join(defs), shadow, ''.join(body)))
