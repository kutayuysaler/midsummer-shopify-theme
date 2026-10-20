"""Inside the bed, drawn for each system: each part in its own cloth, from photographs of the cloths
themselves (lp/tex_tiles.py): Shadan's paisley on the Paisley topper, Katai silk on its boxspring,
Cardi's damask and Wish's bouclé on Flora, Mystic River on Roma, linen elsewhere; with their
piping, the tufts of the top, the stitched border, the brass vents and handles, the legs. The parts
a mattress or a topper does not include are drawn as a light outline. Nothing of the inside is drawn.

drawing(key) returns the SVG for snippets/ms-craft-svg.liquid, with {{U}} for the section id and
[t1] [t2] [t3] for the three parts' names; the structure and classes are those ms-craft expects.
tiles() lists the cloth tiles the drawings use: (asset name, kind, colour)."""
import colorsys, math
from lp_data import CRAFT_PARTS as PARTS, CRAFT_OPT as OPT

PINK, ORANGE, CARAMEL, RED = '#E3A79C', '#D2643C', '#A87648', '#7B2631'
IVORY, LINEN, RAW = '#F2EEE6', '#E3DACB', '#DCD1BF'


def shade(hexc, l=0.0, s=0.0):
    h = hexc.lstrip('#')
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    hh, ll, ss = colorsys.rgb_to_hls(r, g, b)
    ll = max(0, min(1, ll + l))
    ss = max(0, min(1, ss + s))
    r, g, b = colorsys.hls_to_rgb(hh, ll, ss)
    return '#%02X%02X%02X' % (round(r * 255), round(g * 255), round(b * 255))


def mix(a, b, t):
    """a blended toward b by t (0: a, 1: b)"""
    pa = [int(a.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4)]
    pb = [int(b.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4)]
    return '#%02X%02X%02X' % tuple(round(x + (y - x) * t) for x, y in zip(pa, pb))


def P(col, h, tex='linen', **kw):
    d = dict(col=col, h=h, tex=tex)
    d.update(kw)
    return d


# per system: topper, mattress, base, each in its cloth (tex: linen, mystic, silk, boucle, nap,
# damask, paisley; own=True keeps the photographed cloth's own colour). ribbon: the piping; rows:
# the stitched rows of the border; handles, vents; band: a coloured band on the border (Top's
# coral, Brera's Altai edge); legs: wood, leather, fabric (in the cloth), none; drawers.
# The rows, handles and vents follow each product's finishes in the 2026 catalogue (Round 22): two rows
# on Raffaello, Flora, Amalfi, Paisley, Bellagio, Ultra Dry; three on Top, Dreamy, Bellini, Vivaldi,
# Vivaldi Plus, Roma, My Dream, Monteverdi; four on Dreamy Springs and Vicuña. Handles with the
# Midsummer logo wherever the catalogue lists them (not on Bellagio, My Dream or Vicuña).
SYS = {
    'essenziale': dict(topper=P(IVORY, 18), mattress=P(IVORY, 50, ribbon=PINK, rows=2, vents=2), base=P(LINEN, 44)),
    'raffaello': dict(topper=P(IVORY, 18), mattress=P(IVORY, 62, ribbon=PINK, rows=2, handles=True, vents=3), base=P(LINEN, 48)),
    'amalfi': dict(topper=P('#C9D3D6', 20, ribbon='#7E98A3'), mattress=P('#BCC9CD', 56, rows=2, handles=True, vents=2), base=P('#8FA6AF', 48)),
    'capri': dict(topper=P('#D3C9BC', 22, 'mystic', ribbon=PINK), mattress=P('#EEE9E1', 58, 'mystic', rows=3, handles=True, vents=3), base=P('#B8A18F', 48, 'mystic')),
    'bellagio': dict(topper=P(RAW, 18), mattress=P(RAW, 60, ribbon=ORANGE, rows=2, rowcol=ORANGE, vents=2), base=P(LINEN, 48)),
    'vivaldi-2': dict(topper=P(IVORY, 18), mattress=P(LINEN, 62, ribbon=PINK, rows=3, handles=True, vents=3), base=P('#D5C9B5', 48)),
    'vivaldi-plus': dict(topper=P(IVORY, 18), mattress=P(LINEN, 66, ribbon=PINK, rows=3, handles=True, vents=3), base=P('#CBBDA7', 48)),
    'monteverdi': dict(topper=P(RAW, 18), mattress=P('#D6CAB4', 58, ribbon='#C9B48F', rows=3, handles=True, vents=2), base=P('#C9BBA2', 48)),
    'ultra-dry': dict(topper=P(RAW, 18), mattress=P(RAW, 60, ribbon=PINK, rows=2, handles=True, vents=2), base=P(LINEN, 48)),
    'dreamy-2': dict(topper=P('#D3D0CB', 24, 'mystic', ribbon=PINK), mattress=P('#EEEAE4', 60, 'mystic', rows=3, handles=True, vents=3), base=P('#A2B2B9', 48, 'mystic')),
    'brera': dict(topper=P('#F2EFEA', 22), mattress=P('#F2EFEA', 30, band='#22233A', rows=1, handles=True, vents=2), base=P('#B8A18F', 34, legs='leather')),
    'roma': dict(topper=P('#F3F0EA', 18, 'mystic', ribbon=PINK), mattress=P('#F3F0EA', 62, 'mystic', ribbon=PINK, rows=3, handles=True, vents=3), base=P('#A09B97', 48, 'mystic')),
    'dreamy-springs': dict(topper=P(IVORY, 18), mattress=P('#EFEBE4', 66, ribbon=PINK, rows=4, handles=True, vents=3), base=P('#BCAF9C', 48)),
    'my-dream': dict(topper=P(IVORY, 18, 'silk'), mattress=P('#F5F2EC', 56, 'silk', ribbon=PINK, rows=3, vents=2), base=P(LINEN, 46)),
    'bellini': dict(topper=P('#ECE6DB', 22, ribbon='#CDBFA9'), mattress=P('#F1ECE4', 58, rows=3, handles=True, vents=3), base=P('#DCD3C5', 48, 'boucle')),
    'giotto': dict(shape='round', topper=P('#F1ECE3', 16, ribbon='#B98A47'), mattress=P('#EEE8DE', 40, rows=2), base=P('#B98A47', 52, legs='none')),
    'vicuna': dict(topper=P(IVORY, 18), mattress=P('#F6F3EE', 66, ribbon='#B4875B', rows=4, vents=3), base=P('#A87A50', 50)),
    'flora': dict(topper=P('#DED5C6', 24, 'damask', ribbon='#9A6E4C'), mattress=P('#F0EBE3', 58, ribbon='#9A6E4C', rows=2, handles=True, vents=3), base=P('#D6CDBF', 48, 'boucle')),
    'top-2': dict(topper=P('#F4F0E9', 26, ribbon='#C55A48'), mattress=P('#F1ECE4', 58, band='#C55A48', rows=3, handles=True, vents=3), base=P('#B54A3F', 50, legs='fabric')),
    'storage': dict(topper=P('#D3C9BC', 20, 'mystic', ribbon=PINK), mattress=P('#EEE9E1', 54, 'mystic', rows=3, handles=True, vents=3), base=P('#BCAF9C', 56, 'mystic', legs='none', drawers=2)),
    # Paisley, as its photograph shows it: Shadan on the topper, piped in Katai; the border piped
    # likewise; the low boxspring all in Katai silk, down to the floor
    'paisley': dict(topper=P('#E0CCB3', 24, 'paisley', ribbon=RED), mattress=P('#E3D2BC', 58, 'paisley', ribbon=RED, rows=2, handles=True, vents=3, top=('linen', '#F2EEE6')),
                    base=P('#8C2D35', 42, 'linen', legs='none')),
    'topper-roma': dict(topper=P('#E6DFD3', 22, 'mystic', ribbon=PINK), mattress=P(IVORY, 58), base=P(LINEN, 48)),
    'topper-high': dict(topper=P('#EAE3D7', 26, ribbon='#CDBFA9'), mattress=P(IVORY, 58), base=P(LINEN, 48)),
    'topper-thin': dict(topper=P(IVORY, 12), mattress=P(IVORY, 58), base=P(LINEN, 48)),
    'first-dream': dict(topper=P(IVORY, 18), mattress=P('#F2EEE7', 50, ribbon=CARAMEL, rows=2, vents=2), base=P(LINEN, 44)),
}
GENERIC = dict(topper=P('#F4EEE6', 22, ribbon='#D9A495'), mattress=P('#F4EEE6', 62, ribbon='#D9A495', rows=3, handles=True, vents=3), base=P('#CFA28C', 50))

X0, W, DX, DY = 40.0, 360.0, 129.9, -75.0
L = (DX * DX + DY * DY) ** .5
UX, UY = DX / L, DY / L
TOPS = {'topper': 128.0, 'mattress': 222.0, 'base': 330.0}
NUM = {'topper': 'I', 'mattress': 'II', 'base': 'III'}
LABEL = {'topper': '[t1]', 'mattress': '[t2]', 'base': '[t3]'}
# the drawn size of one tile of each cloth (the motifs at their scale on a bed, the weaves finer)
TILE = {'linen': 30, 'mystic': 26, 'silk': 24, 'boucle': 30, 'nap': 40, 'damask': 84, 'paisley': 120}
PAPER = '#F3EDE4'


def f(v):
    return ('%.1f' % v).rstrip('0').rstrip('.')


def cfg_of(key):
    """a system's parts; a boxspring (base-<system>) is drawn as that system's base"""
    if key.startswith('base-'):
        key = key[5:]
    return SYS.get(key, GENERIC)


def tint(key):
    """the section's ground for a system: the house's warm paper, touched by the colour of its base"""
    c = cfg_of(key)['base']['col']
    return '--cr-g1:%s;--cr-g2:%s;--cr-g3:%s' % (mix(c, '#F2E8E0', .9), mix(c, '#E8DCD1', .86), mix(c, '#DDCEC1', .82))


def soft(col, by=.06):
    """the cloth's colour a touch quieter, so it sits on the section's paper"""
    return mix(col, PAPER, by)


def tile_name(p, face=''):
    """the asset of a part's cloth: ms-tex-<kind>-<colour>.jpg (a top in another cloth: p['top'])"""
    if face == 't' and p.get('top'):
        tex, col = p['top'][0], soft(p['top'][1])
    else:
        tex, col = p['tex'], (None if p.get('own') else soft(p['col']))
    return 'ms-tex-%s-%s.jpg' % (tex, (col or 'own').lstrip('#').lower())


def tiles():
    seen = {}
    for cfg in list(SYS.values()) + [GENERIC]:
        for part in ('topper', 'mattress', 'base'):
            p = cfg[part]
            seen[tile_name(p)] = (p['tex'], None if p.get('own') else soft(p['col']))
            if p.get('top'):
                seen[tile_name(p, 't')] = (p['top'][0], soft(p['top'][1]))
    return sorted((k, v[0], v[1]) for k, v in seen.items())


def cloth(part, p, u):
    """a part's cloth as three patterns: the front as it is, the side and the top receding"""
    out = []
    mats = {
        'f': '',
        's': ' patternTransform="matrix(%s %s 0 1 0 0)"' % (f(UX * .62), f(UY * .62)),
        't': ' patternTransform="matrix(1 0 %s %s 0 0)"' % (f(UX * .52), f(UY * .52)),
    }
    for nm, tr in mats.items():
        href = "{{ '%s' | asset_url }}" % tile_name(p, nm)
        t = TILE.get(p['top'][0] if (nm == 't' and p.get('top')) else p['tex'], 30)
        out.append('<pattern id="cr-%s-%s-x%s" width="%s" height="%s" patternUnits="userSpaceOnUse"%s>'
                   '<image href="%s" width="%s" height="%s" preserveAspectRatio="none"/></pattern>' % (u, part, nm, t, t, tr, href, t, t))
    return ''.join(out)


def grads(part, col, u, round_=False):
    """the flat colour under the cloth (and the whole of an outlined part), lit from the top left"""
    g = []
    g.append('<linearGradient id="cr-%s-%s-t" x1="0" y1="1" x2="1" y2="0"><stop offset="0" stop-color="%s"/><stop offset="1" stop-color="%s"/></linearGradient>' % (u, part, shade(col, .06), shade(col, .02)))
    if round_:
        stops = ((0, -.15), (.16, -.05), (.4, .045), (.66, -.01), (.9, -.1), (1, -.16))
        g.append('<linearGradient id="cr-%s-%s-f" x1="0" y1="0" x2="1" y2="0">%s</linearGradient>' % (u, part, ''.join('<stop offset="%s" stop-color="%s"/>' % (o, shade(col, d)) for o, d in stops)))
        g.append('<radialGradient id="cr-%s-%s-r" cx=".42" cy=".38" r=".7"><stop offset="0" stop-color="%s"/><stop offset="1" stop-color="%s"/></radialGradient>' % (u, part, shade(col, .07), shade(col, .01)))
    else:
        g.append('<linearGradient id="cr-%s-%s-f" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="%s"/><stop offset=".14" stop-color="%s"/><stop offset=".86" stop-color="%s"/><stop offset="1" stop-color="%s"/></linearGradient>' % (u, part, shade(col, .05), col, shade(col, -.03), shade(col, -.07)))
    g.append('<linearGradient id="cr-%s-%s-s" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="%s"/><stop offset="1" stop-color="%s"/></linearGradient>' % (u, part, shade(col, -.08), shade(col, -.13)))
    return ''.join(g)


def light_defs(u):
    """the light over every cloth: a soft sheen on the tops, a turn of the cloth on the fronts, the
    sides in shade; and the brass of the vents"""
    return ''.join([
        '<linearGradient id="cr-%s-lt" x1="0" y1="1" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity=".26"/><stop offset=".55" stop-color="#fff" stop-opacity=".05"/><stop offset="1" stop-color="#2A1F19" stop-opacity=".05"/></linearGradient>' % u,
        '<linearGradient id="cr-%s-lf" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".34"/><stop offset=".12" stop-color="#fff" stop-opacity=".06"/><stop offset=".6" stop-color="#2A1F19" stop-opacity="0"/><stop offset="1" stop-color="#2A1F19" stop-opacity=".16"/></linearGradient>' % u,
        '<linearGradient id="cr-%s-lf2" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#2A1F19" stop-opacity=".07"/><stop offset=".3" stop-color="#2A1F19" stop-opacity="0"/><stop offset=".8" stop-color="#fff" stop-opacity=".04"/><stop offset="1" stop-color="#2A1F19" stop-opacity=".05"/></linearGradient>' % u,
        '<linearGradient id="cr-%s-ls" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2A1F19" stop-opacity=".1"/><stop offset="1" stop-color="#2A1F19" stop-opacity=".24"/></linearGradient>' % u,
        '<linearGradient id="cr-%s-sheen" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".3" stop-color="#fff" stop-opacity=".07"/><stop offset=".36" stop-color="#fff" stop-opacity=".02"/><stop offset=".66" stop-color="#fff" stop-opacity=".06"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>' % u,
        '<linearGradient id="cr-%s-lr" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#2A1F19" stop-opacity=".2"/><stop offset=".3" stop-color="#2A1F19" stop-opacity="0"/><stop offset=".45" stop-color="#fff" stop-opacity=".1"/><stop offset=".66" stop-color="#2A1F19" stop-opacity="0"/><stop offset="1" stop-color="#2A1F19" stop-opacity=".24"/></linearGradient>' % u,
        '<radialGradient id="cr-%s-brass" cx=".38" cy=".35" r=".7"><stop offset="0" stop-color="#F4DDA4"/><stop offset=".55" stop-color="#B98A43"/><stop offset="1" stop-color="#6E4F25"/></radialGradient>' % u,
        # Round 26: the crown of a cushion's top, the light gathered where it swells
        '<radialGradient id="cr-%s-crown" cx=".36" cy=".46" r=".66"><stop offset="0" stop-color="#fff" stop-opacity=".24"/><stop offset=".6" stop-color="#fff" stop-opacity=".04"/><stop offset="1" stop-color="#2A1F19" stop-opacity=".07"/></radialGradient>' % u,
        '<radialGradient id="cr-%s-tuft" cx=".4" cy=".35" r=".75"><stop offset="0" stop-color="#fff" stop-opacity=".95"/><stop offset=".6" stop-color="#fff" stop-opacity=".55"/><stop offset="1" stop-color="#2A1F19" stop-opacity=".25"/></radialGradient>' % u,
    ])


def lerp(a, b, t):
    return a + (b - a) * t


LX = 570.0     # the label column


def label(part, x, y, ghost=False, num=None, note='[t0]'):
    """a hairline from the part to its numeral and name, as on an architect's drawing; a part the
    product does not include (or that is optional) says so beneath its name"""
    nm = LABEL[part]
    if num and part != 'topper':
        # a part in one piece with another has a longer name ("Mattress and boxspring, in one"): set
        # in short lines, word by word and after a comma, so it never runs past the drawing's edge,
        # in any language
        v = 't2' if part == 'mattress' else 't3'
        nm = ('{%%- assign tw = %s | split: \' \' -%%}{%%- assign tl = \'\' -%%}{%%- assign tls = \'\' -%%}'
              '{%%- for w in tw -%%}{%%- assign tc = tl | append: \' \' | append: w | strip -%%}'
              '{%%- if tc.size > 14 and tl != blank -%%}{%%- assign tls = tls | append: tl | append: \'|\' -%%}{%%- assign tl = w -%%}{%%- else -%%}{%%- assign tl = tc -%%}{%%- endif -%%}'
              '{%%- assign wl = w | slice: -1 -%%}{%%- if wl == \',\' -%%}{%%- assign tls = tls | append: tl | append: \'|\' -%%}{%%- assign tl = \'\' -%%}{%%- endif -%%}{%%- endfor -%%}'
              '{%%- if tl != blank -%%}{%%- assign tls = tls | append: tl -%%}{%%- endif -%%}{%%- assign tls = tls | split: \'|\' -%%}{%%- assign tup = tls.size | minus: 1 | times: -7.5 -%%}'
              '{%%- for l in tls -%%}<tspan x="%s" dy="{%%- if forloop.first -%%}{{ tup }}{%%- else -%%}15{%%- endif -%%}">{{ l | escape }}</tspan>{%%- endfor -%%}') % (v, f(LX + 26))
    out = ('<g class="ms-cr__lbl" pointer-events="none"><path class="ms-cr__lead" d="M%s,%s H%s"/><circle class="ms-cr__dot" cx="%s" cy="%s" r="1.6"/>'
           '<text x="%s" y="%s" class="ms-cr__num">%s</text><text x="%s" y="%s" class="ms-cr__nm">%s</text>'
           % (f(x), f(y), f(LX - 6), f(x), f(y), f(LX), f(y + 5), num or NUM[part], f(LX + 26), f(y + 4.5), nm))
    if ghost:
        out += '<text x="%s" y="%s" class="ms-cr__abs">%s</text>' % (f(LX + 26), f(y + 21), note)
    return out + '</g>'


def piping(pts, col, w=2.4):
    """a corded edge: its shadow, the cord, the light along it"""
    d = 'M' + ' L'.join('%s,%s' % (f(x), f(y)) for x, y in pts)
    return ('<path d="%s" fill="none" stroke="#2A1F19" stroke-opacity=".18" stroke-width="%s" stroke-linecap="round" stroke-linejoin="round" transform="translate(0 .9)"/>'
            '<path class="ms-cr__pipe" style="stroke: %s; stroke-width: %s" d="%s"/>'
            '<path d="%s" fill="none" stroke="#fff" stroke-opacity=".45" stroke-width="%s" stroke-linecap="round" transform="translate(0 -.55)"/>') % (
        d, f(w + .6), col, f(w), d, d, f(w * .28))


def box(part, p, u, kind, gap=0.0, inner=False):
    """one part of a rectangular bed, seen from above and to the side, in its own cloth"""
    y0 = p.get('y0', TOPS[part])
    h = p['h']
    if part == 'base':
        y0 = 380.0 - h
    x1 = X0 + W
    col = soft(p['col'])
    ink = shade(col, -.3)
    g = []
    opt = p.get('opt', False)
    ghost = (kind != 'system' and part != kind) or opt
    cls = 'ms-cr__slab' + (' is-ghost' if ghost else '') + (' is-opt' if opt else '')
    if not inner:
        g.append('<g class="%s" data-part="%s" tabindex="0" role="button" aria-label="%s" aria-controls="cr-{{U}}-%s" aria-expanded="false">' % (cls, part, LABEL[part], part))
    soft_edge = part != 'base'     # a topper and a mattress are cushions, their edges rounded
    r = min(5.0, h * .22) if soft_edge else 1.2
    # legs first, so the base stands on them
    if part == 'base' and not ghost:
        legs = p.get('legs', 'wood')
        if legs == 'wood':
            for lx, ly in ((X0 + 18, y0 + h), (x1 - 26, y0 + h), (x1 + DX - 22, y0 + h + DY)):
                g.append('<path d="M%s,%s h11 l-1.8,11 c-.3,2.2 -1.1,3.3 -2.4,3.7 h-2.6 c-1.3,-.4 -2.1,-1.5 -2.4,-3.7 Z" fill="url(#cr-{{U}}-wood)"/>'
                         '<path d="M%s,%s v12" stroke="#FFF1DC" stroke-opacity=".35" stroke-width=".8"/>' % (f(lx - 5.5), f(ly), f(lx - 1.8), f(ly + 1)))
        elif legs == 'leather':
            for lx, ly in ((X0 + 18, y0 + h), (x1 - 28, y0 + h), (x1 + DX - 24, y0 + h + DY)):
                g.append('<path d="M%s,%s h9 l-1.4,19 h-6.2 Z" fill="#8E6141"/><path d="M%s,%s h7.6" stroke="#C99B6D" stroke-width="1"/><path d="M%s,%s v18" stroke="#2A1F19" stroke-opacity=".2" stroke-width="1.4"/>' % (f(lx - 4.5), f(ly), f(lx - 3.8), f(ly + 6), f(lx + 3.4), f(ly)))
        elif legs == 'fabric':
            for lx in (X0 + 10, x1 - 36):
                g.append('<rect x="%s" y="%s" width="26" height="13" fill="url(#cr-{{U}}-%s-xf)"/><rect x="%s" y="%s" width="26" height="13" fill="#2A1F19" fill-opacity=".12"/>' % (f(lx), f(y0 + h - 1), part, f(lx), f(y0 + h - 1)))
            g.append('<path d="M%s,%s l14,-8 v13 l-14,8 Z" fill="%s"/>' % (f(x1 + DX - 30), f(y0 + h + DY - 1), shade(col, -.15)))
    # the three faces; a cushion's front bows a little at the top and bottom
    side = 'M%s,%s L%s,%s L%s,%s L%s,%s Z' % (f(x1), f(y0), f(x1 + DX), f(y0 + DY), f(x1 + DX), f(y0 + DY + h), f(x1), f(y0 + h))
    if soft_edge:
        front = ('M%s,%s Q%s,%s %s,%s L%s,%s Q%s,%s %s,%s L%s,%s Q%s,%s %s,%s L%s,%s Q%s,%s %s,%s Z' % (
            f(X0), f(y0 + r), f(X0), f(y0), f(X0 + r), f(y0), f(x1 - r * .4), f(y0), f(x1), f(y0), f(x1), f(y0 + r * .6),
            f(x1), f(y0 + h - r * .6), f(x1), f(y0 + h), f(x1 - r * .4), f(y0 + h), f(X0 + r), f(y0 + h), f(X0), f(y0 + h), f(X0), f(y0 + h - r)))
    else:
        front = 'M%s,%s L%s,%s L%s,%s Q%s,%s %s,%s Z' % (f(X0), f(y0), f(x1), f(y0), f(x1), f(y0 + h), f((X0 + x1) / 2), f(y0 + h + 1.5), f(X0), f(y0 + h))
    top = 'M%s,%s L%s,%s L%s,%s L%s,%s Z' % (f(X0 + r * .6), f(y0), f(x1), f(y0), f(x1 + DX), f(y0 + DY), f(X0 + DX + r * .4), f(y0 + DY))
    if ghost:
        g.append('<path class="ms-cr__face ms-cr__face--side" fill="url(#cr-{{U}}-%s-s)" d="%s"/>' % (part, side))
        g.append('<path class="ms-cr__face" fill="url(#cr-{{U}}-%s-f)" d="%s"/>' % (part, front))
        g.append('<path class="ms-cr__face ms-cr__face--top" fill="url(#cr-{{U}}-%s-t)" d="%s"/>' % (part, top))
    else:
        g.append('<path class="ms-cr__face ms-cr__face--side" fill="url(#cr-{{U}}-%s-xs)" d="%s"/><path d="%s" fill="url(#cr-{{U}}-ls)" pointer-events="none"/>' % (part, side, side))
        g.append('<path class="ms-cr__face" fill="url(#cr-{{U}}-%s-xf)" d="%s"/><path d="%s" fill="url(#cr-{{U}}-lf)" pointer-events="none"/><path d="%s" fill="url(#cr-{{U}}-lf2)" pointer-events="none"/>' % (part, front, front, front))
        g.append('<path class="ms-cr__face ms-cr__face--top" fill="url(#cr-{{U}}-%s-xt)" d="%s"/><path d="%s" fill="url(#cr-{{U}}-lt)" pointer-events="none"/>' % (part, top, top))
        if soft_edge:
            g.append('<path d="%s" fill="url(#cr-{{U}}-crown)" pointer-events="none"/>' % top)
        # Round 26: the lower edges drawn in a fine shade, the front corner caught by the light
        g.append('<path d="M%s,%s L%s,%s L%s,%s" fill="none" stroke="#2A1F19" stroke-opacity=".2" stroke-width=".9" stroke-linecap="round" pointer-events="none"/>' % (
            f(X0 + r * .8), f(y0 + h - .45), f(x1 - .5), f(y0 + h - .45), f(x1 + DX - .6), f(y0 + h + DY - .45)))
        g.append('<path d="M%s,%s V%s" stroke="#fff" stroke-opacity=".24" stroke-width=".7" pointer-events="none"/>' % (f(x1 - .8), f(y0 + r + .5), f(y0 + h - r - .5)))
        if p.get('sheen'):
            # silk: a light that runs along it
            g.append('<path d="%s" fill="url(#cr-{{U}}-sheen)" pointer-events="none"/>' % front)
    if part != 'topper' and not ghost:
        sx, sy = X0 + 26, y0 - 4
        g.append('<path class="ms-cr__cast" d="M%s,%s L%s,%s L%s,%s L%s,%s Z" filter="url(#cr-{{U}}-soft)"/>' % (
            f(sx), f(sy), f(x1 - 14), f(sy), f(x1 + DX - 30), f(sy + DY + 10), f(sx + DX - 8), f(sy + DY + 10)))
    if not ghost:
        def at(uu, vv):
            return X0 + uu * W + vv * DX, y0 + vv * DY
        fold = '#2A1F19'
        # where the cloth turns over the edge, it catches the light
        g.append('<path d="M%s,%s L%s,%s L%s,%s" fill="none" stroke="#fff" stroke-opacity=".55" stroke-width="1.1" stroke-linecap="round"/>' % (f(X0 + r), f(y0 + 1.4), f(x1 - 1), f(y0 + 1.4), f(x1 + DX - 2), f(y0 + DY + 1.4)))
        g.append('<path d="M%s,%s L%s,%s" fill="none" stroke="#2A1F19" stroke-opacity=".14" stroke-width="1.2"/>' % (f(x1), f(y0 + 1), f(x1), f(y0 + h - 1)))
        if part in ('mattress', 'topper'):
            # tufts: the cloth drawn down to each, softly, in a grid that follows the top
            nu, nv = (6, 3) if part == 'mattress' else (7, 3)
            pts = {}
            for j in range(nv):
                for i in range(nu):
                    uu = (i + .5 + (.5 if j % 2 else 0)) / (nu + .5)
                    vv = (j + .7) / (nv + .4)
                    pts[(i, j)] = at(uu, vv)
            dep = .09 if part == 'mattress' else .06
            for (x, y) in pts.values():
                # a dimple where the tuft draws the cloth down, a few soft folds, the tuft itself
                g.append('<ellipse cx="%s" cy="%s" rx="5.5" ry="2.4" fill="%s" fill-opacity="%s"/>' % (f(x + .5), f(y + .5), fold, f(dep)))
                folds = []
                for ang in (20, 160, 200, 340):
                    a = math.radians(ang)
                    folds.append('M%s,%s L%s,%s' % (f(x + math.cos(a) * 2), f(y + math.sin(a) * .9), f(x + math.cos(a) * 6.5), f(y + math.sin(a) * 2.9)))
                g.append('<path d="%s" stroke="%s" stroke-opacity="%s" stroke-width=".55" stroke-linecap="round"/>' % (' '.join(folds), fold, f(dep * .8)))
                g.append('<ellipse class="ms-cr__tuft" style="fill: %s" cx="%s" cy="%s" rx="1.7" ry="1"/><ellipse cx="%s" cy="%s" rx="1.7" ry="1" fill="url(#cr-{{U}}-tuft)"/>' % (shade(col, -.04), f(x), f(y), f(x), f(y)))
        if part == 'mattress':
            # the border: stitched by hand in columns, and in rows across them
            n = 34
            cols = []
            for i in range(1, n):
                xx = X0 + W * i / n
                cols.append('M%s,%s V%s' % (f(xx), f(y0 + 5), f(y0 + h - 5)))
            nsd = 12
            scol = []
            for i in range(1, nsd):
                tt = i / nsd
                xx, yy = x1 + DX * tt, y0 + DY * tt
                scol.append('M%s,%s V%s' % (f(xx), f(yy + 5), f(yy + h - 5)))
            g.append('<path d="%s" stroke="%s" stroke-opacity=".075" stroke-width=".9" fill="none"/><path d="%s" stroke="#fff" stroke-opacity=".3" stroke-width=".6" fill="none" transform="translate(1.1 0)"/>' % (' '.join(cols), fold, ' '.join(cols)))
            g.append('<path d="%s" stroke="%s" stroke-opacity=".12" stroke-width=".8" fill="none"/>' % (' '.join(scol), fold))
            rows = p.get('rows', 2)
            rc = p.get('rowcol') or shade(col, -.36)
            for rr in range(rows):
                yy = y0 + 7 + (h - 14) * (rr + 1) / (rows + 1)
                g.append('<path d="M%s,%s L%s,%s L%s,%s" fill="none" stroke="%s" stroke-width="1.15" stroke-linecap="round" stroke-dasharray=".1 4.4" stroke-opacity=".7"/>' % (f(X0 + 6), f(yy), f(x1 - 3), f(yy), f(x1 + DX - 5), f(yy + DY), rc))
            # brass vents, and the house's label
            nvn = p.get('vents', 0)
            for i in range(nvn):
                vx = X0 + W * (i + .62) / (nvn + .4)
                vy = y0 + h * .5
                g.append('<circle cx="%s" cy="%s" r="2.5" fill="url(#cr-{{U}}-brass)"/><circle cx="%s" cy="%s" r=".9" fill="#4A3418" fill-opacity=".6"/>' % (f(vx), f(vy), f(vx), f(vy)))
            lx, ly = x1 - 78, y0 + h * .5 - 7
            g.append('<rect x="%s" y="%s" width="34" height="14" rx="1" fill="%s" stroke="%s" stroke-width=".6"/><path d="M%s,%s h20" stroke="%s" stroke-width=".8"/><path d="M%s,%s h12" stroke="%s" stroke-width=".5"/>' % (
                f(lx), f(ly), shade(col, .04), shade(col, -.24), f(lx + 7), f(ly + 6), shade(col, -.42), f(lx + 11), f(ly + 9.5), shade(col, -.3)))
            if p.get('handles'):
                # a fabric handle on the side, and one on the front
                hx, hy = x1 + DX * .5, y0 + DY * .5 + h * .5
                ux, uy = UX * 22, UY * 22
                g.append('<path d="M%s,%s l%s,%s v7 l%s,%s Z" fill="%s" stroke="%s" stroke-width=".7"/>' % (f(hx - ux / 2), f(hy - 3.5 - uy / 2), f(ux), f(uy), f(-ux), f(-uy), shade(col, -.04), shade(col, -.3)))
                fx = X0 + W * .3
                g.append('<rect x="%s" y="%s" width="26" height="8" rx="1.2" fill="%s" stroke="%s" stroke-width=".7"/><path d="M%s,%s h22" stroke="%s" stroke-width=".5" stroke-dasharray="1 1.4"/>' % (
                    f(fx), f(y0 + h * .5 - 4), shade(col, -.03), shade(col, -.3), f(fx + 2), f(y0 + h * .5), shade(col, -.32)))
        if part == 'topper':
            # a pillowed top: the cushion swells a little between its piped edges
            g.append('<path d="M%s,%s L%s,%s" stroke="#fff" stroke-opacity=".14" stroke-width="3" stroke-linecap="round"/>' % (f(X0 + 14), f(y0 + h * .4), f(x1 - 14), f(y0 + h * .4)))
        if p.get('band'):
            bt = 5 if part == 'topper' else 8
            yb = y0 + (5 if part == 'topper' else h * .36)
            g.append('<path d="M%s,%s L%s,%s L%s,%s L%s,%s L%s,%s L%s,%s Z" fill="%s"/><path d="M%s,%s L%s,%s L%s,%s" fill="none" stroke="#fff" stroke-opacity=".25" stroke-width=".8"/>' % (
                f(X0), f(yb), f(x1), f(yb), f(x1 + DX), f(yb + DY), f(x1 + DX), f(yb + DY + bt), f(x1), f(yb + bt), f(X0), f(yb + bt), p['band'], f(X0), f(yb + .6), f(x1), f(yb + .6), f(x1 + DX), f(yb + DY + .6)))
        if part == 'base' and p.get('drawers'):
            nd = p['drawers']
            wdr = (W - 30) / nd
            for i in range(nd):
                dx0 = X0 + 12 + i * (wdr + 6)
                g.append('<rect x="%s" y="%s" width="%s" height="%s" rx="1.5" fill="#fff" fill-opacity=".08" stroke="%s" stroke-width=".9"/>' % (f(dx0), f(y0 + 12), f(wdr), f(h - 20), shade(col, -.28)))
                g.append('<path d="M%s,%s h22" stroke="%s" stroke-width="2" stroke-linecap="round"/>' % (f(dx0 + wdr / 2 - 11), f(y0 + 12 + (h - 20) / 2), shade(col, -.4)))
        if part == 'base':
            # the welt where the upholstery turns over the top
            g.append('<path d="M%s,%s L%s,%s L%s,%s" fill="none" stroke="#2A1F19" stroke-opacity=".22" stroke-width="1"/><path d="M%s,%s L%s,%s L%s,%s" fill="none" stroke="#fff" stroke-opacity=".22" stroke-width=".8"/>' % (
                f(X0 + 2), f(y0 + 9), f(x1 - 1), f(y0 + 9), f(x1 + DX - 2), f(y0 + 9 + DY), f(X0 + 2), f(y0 + 10.2), f(x1 - 1), f(y0 + 10.2), f(x1 + DX - 2), f(y0 + 10.2 + DY)))
        rib = p.get('ribbon')
        if rib:
            rib = soft(rib, .04)
            for yy in ((y0, y0 + h) if part != 'base' else (y0,)):
                g.append(piping([(X0 + r * .7, yy), (x1, yy), (x1 + DX, yy + DY)], rib))
            if part != 'base':
                g.append(piping([(x1 + DX, y0 + DY), (X0 + DX + r * .4, y0 + DY)], rib, 1.8))
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


def cyl(part, p, u, kind, gap=0.0, inner=False):
    """one part of a round bed: a cylinder in its cloth, its top lit from the left"""
    CX, RX, RY = 285.0, 222.0, 58.0
    CY = p.get('y0', {'topper': 82.0, 'mattress': 176.0, 'base': 296.0}[part])
    h = p['h']
    col = soft(p['col'])
    fold = '#2A1F19'
    ghost = (kind != 'system' and part != kind)
    g = [] if inner else ['<g class="ms-cr__slab%s" data-part="%s" tabindex="0" role="button" aria-label="%s" aria-controls="cr-{{U}}-%s" aria-expanded="false">' % (' is-ghost' if ghost else '', part, LABEL[part], part)]
    band = 'M%s,%s A%s,%s 0 0 0 %s,%s V%s A%s,%s 0 0 1 %s,%s Z' % (f(CX - RX), f(CY), f(RX), f(RY), f(CX + RX), f(CY), f(CY + h), f(RX), f(RY), f(CX - RX), f(CY + h))
    st = shade(col, -.22)
    if ghost:
        g.append('<path class="ms-cr__face" fill="url(#cr-{{U}}-%s-f)" stroke="%s" d="%s"/>' % (part, st, band))
        g.append('<ellipse class="ms-cr__face ms-cr__face--top" fill="url(#cr-{{U}}-%s-r)" stroke="%s" cx="%s" cy="%s" rx="%s" ry="%s"/>' % (part, st, f(CX), f(CY), f(RX), f(RY)))
    else:
        g.append('<path class="ms-cr__face" fill="url(#cr-{{U}}-%s-xf)" stroke="%s" d="%s"/><path d="%s" fill="url(#cr-{{U}}-lr)" pointer-events="none"/>' % (part, st, band, band))
        g.append('<ellipse class="ms-cr__face ms-cr__face--top" fill="url(#cr-{{U}}-%s-xt)" stroke="%s" cx="%s" cy="%s" rx="%s" ry="%s"/><ellipse fill="url(#cr-{{U}}-lt)" cx="%s" cy="%s" rx="%s" ry="%s" pointer-events="none"/>' % (
            part, st, f(CX), f(CY), f(RX), f(RY), f(CX), f(CY), f(RX), f(RY)))
        if part != 'base':
            g.append('<ellipse fill="url(#cr-{{U}}-crown)" cx="%s" cy="%s" rx="%s" ry="%s" pointer-events="none"/>' % (f(CX), f(CY), f(RX), f(RY)))
    front_arc = lambda y, k=1.0: 'M%s,%s A%s,%s 0 0 0 %s,%s' % (f(CX - RX * k), f(y), f(RX * k), f(RY * k), f(CX + RX * k), f(y))
    if not ghost:
        if part == 'topper':
            g.append('<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="none" stroke="%s" stroke-width=".7" stroke-dasharray="2.2 2.6" stroke-opacity=".3"/>' % (f(CX), f(CY), f(RX * .62), f(RY * .62), fold))
            g.append('<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="none" stroke="%s" stroke-width=".7" stroke-dasharray="2.2 2.6" stroke-opacity=".22" />' % (f(CX), f(CY), f(RX * .3), f(RY * .3), fold))
        if part == 'mattress':
            pts = []
            for ring, n in ((.32, 6), (.66, 12)):
                for a in range(n):
                    t = (a + (.5 if ring > .5 else 0)) / n * 2 * math.pi
                    pts.append((CX + math.cos(t) * RX * ring, CY + math.sin(t) * RY * ring))
            for (x, y) in pts:
                g.append('<ellipse cx="%s" cy="%s" rx="8" ry="3.6" fill="%s" fill-opacity=".06"/><ellipse class="ms-cr__tuft" style="fill: %s" cx="%s" cy="%s" rx="1.8" ry="1"/><ellipse cx="%s" cy="%s" rx="1.8" ry="1" fill="url(#cr-{{U}}-tuft)"/>' % (f(x + .5), f(y + .4), fold, shade(col, -.06), f(x), f(y), f(x), f(y)))
            rows = p.get('rows', 2)
            for rr in range(rows):
                yy = CY + 5 + (h - 10) * (rr + 1) / (rows + 1)
                g.append('<path d="%s" fill="none" stroke="%s" stroke-width="1.1" stroke-linecap="round" stroke-dasharray=".1 4.2" stroke-opacity=".7"/>' % (front_arc(yy), shade(col, -.34)))
        g.append('<path d="%s" fill="none" stroke="#2A1F19" stroke-opacity=".18" stroke-width=".9" pointer-events="none"/>' % front_arc(CY + h - .45))
        if part == 'base':
            # a recessed plinth, so the round base floats a little above the floor
            g.append('<path d="%s" fill="none" stroke="%s" stroke-width="5" stroke-opacity=".35"/>' % (front_arc(CY + h - 3, .985), shade(col, -.3)))
        rib = p.get('ribbon')
        if rib:
            for yy in ((CY,) if part == 'base' else (CY, CY + h)):
                g.append('<path class="ms-cr__pipe" style="stroke: %s; stroke-width: 2.2" d="%s"/><path d="%s" fill="none" stroke="#fff" stroke-opacity=".4" stroke-width=".6" transform="translate(0 -.6)"/>' % (soft(rib, .04), front_arc(yy), front_arc(yy)))
        if gap > 6:
            gl = ''.join('M%s,%s v%s ' % (f(x), f(CY + h + 4), f(gap - 8)) for x in (CX - RX, CX + RX))
            g.append('<path class="ms-cr__guide" d="%s" stroke="%s" stroke-width=".7" stroke-dasharray="1.5 3.5" stroke-opacity=".5" fill="none" pointer-events="none"/>' % (gl, shade(col, -.35)))
    if inner:
        return ''.join(g)
    g.append(label(part, CX + RX + 8, CY + (p.get('ly') if p.get('ly') is not None else h * .5), ghost, num=p.get('num')))
    g.append('</g>')
    return ''.join(g)


def drawing(key, kind='system'):
    import copy
    cfg = copy.deepcopy(cfg_of(key))
    u = '{{U}}'
    round_ = cfg.get('shape') == 'round'
    defs = ['<filter id="cr-%s-blur" x="-20%%" y="-200%%" width="140%%" height="500%%"><feGaussianBlur stdDeviation="8"/></filter>' % u,
            '<filter id="cr-%s-soft" x="-20%%" y="-60%%" width="140%%" height="220%%"><feGaussianBlur stdDeviation="5"/></filter>' % u,
            '<filter id="cr-%s-near" x="-10%%" y="-200%%" width="120%%" height="500%%"><feGaussianBlur stdDeviation="2.6"/></filter>' % u,
            '<linearGradient id="cr-%s-wood" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#5E3E2A"/><stop offset=".45" stop-color="#8A5E3F"/><stop offset="1" stop-color="#4E3322"/></linearGradient>' % u,
            light_defs(u)]
    shown = PARTS.get(key, 'topper,mattress,base').split(',')
    for o in OPT.get(key, '').split(','):
        if o in cfg:
            cfg[o]['opt'] = True
    for part in ('topper', 'mattress', 'base'):
        defs.append(grads(part, soft(cfg[part]['col']), u, round_))
        ghost = (kind != 'system' and part != kind) or cfg[part].get('opt')
        inside = part == 'mattress' and shown == ['topper', 'base']     # drawn within the boxspring
        if (part in shown or inside) and not ghost:
            defs.append(cloth(part, cfg[part], u))
    # the round bed's cloth follows its curve only roughly: its patterns are drawn flat
    if round_:
        defs = [d.replace('patternTransform="matrix(1 0 %s %s 0 0)"' % (f(UX * .52), f(UY * .52)), 'patternTransform="matrix(1 0 0 .3 0 0)"') for d in defs]
    if round_:
        cy = {'topper': 82.0, 'mattress': 176.0, 'base': 296.0}
        gaps = {'topper': cy['mattress'] - (cy['topper'] + cfg['topper']['h']), 'mattress': cy['base'] - (cy['mattress'] + cfg['mattress']['h']), 'base': 0}
    else:
        tops = {'topper': TOPS['topper'], 'mattress': TOPS['mattress'], 'base': 380.0 - cfg['base']['h']}
        gaps = {'topper': tops['mattress'] - (tops['topper'] + cfg['topper']['h']), 'mattress': tops['base'] - (tops['mattress'] + cfg['mattress']['h']), 'base': 0}
    body = []
    shadow = '<ellipse class="ms-cr__shadow" cx="%s" cy="398" rx="%s" ry="12" filter="url(#cr-%s-blur)"/>' % ('285' if round_ else '290', '236' if round_ else '262', u)
    # Round 26: and a closer, darker one where the bed meets the floor
    shadow += '<ellipse class="ms-cr__near" cx="%s" cy="%s" rx="%s" ry="4.5" fill="#46281A" fill-opacity=".2" filter="url(#cr-%s-near)"/>' % ('285' if round_ else '296', '392' if round_ else '395', '214' if round_ else '246', u)
    # closed, the bed is whole: the mattress lies on the base, the topper on the mattress
    close = {'base': 0, 'mattress': gaps['mattress'], 'topper': gaps['mattress'] + gaps['topper']}
    depth = {'base': 1, 'mattress': 2.2, 'topper': 3.6}
    delay = {'base': 0, 'mattress': .12, 'topper': .24}
    draw = cyl if round_ else box
    if shown == ['topper', 'base']:
        # the mattress and the boxspring in one piece: drawn as one, the mattress's face over the
        # boxspring's, joined by a single seam; the topper floats above it when opened
        mp, bp = cfg['mattress'], cfg['base']
        if round_:
            bp['y0'] = 296.0 + bp['h'] - (mp['h'] + bp['h'])
            tot = mp['h'] + bp['h']
            mp_inner = dict(mp, y0=bp['y0'])
            bp_full = dict(bp, h=tot, y0=bp['y0'], num='II', ly=tot * .5)
            whole = draw('base', bp_full, u, kind, 0)
            inside = draw('mattress', mp_inner, u, kind, 0, inner=True)
            jy = bp['y0'] + mp['h']
            inside += '<path d="M%s,%s A%s,%s 0 0 0 %s,%s" fill="none" stroke="%s" stroke-width="1.3" stroke-opacity=".8"/>' % (
                f(285.0 - 222.0), f(jy), f(222.0), f(58.0), f(285.0 + 222.0), f(jy), shade(soft(bp['col']), -.28))
            cfg['topper']['y0'] = bp['y0'] - 64.0 - cfg['topper']['h']
            gtop = 64.0
        else:
            tot = mp['h'] + bp['h']
            top = 380.0 - tot
            mp_inner = dict(mp, y0=top)
            bp_full = dict(bp, h=tot, num='II', ly=tot * .5)
            whole = draw('base', bp_full, u, kind, 0)
            inside = draw('mattress', mp_inner, u, kind, 0, inner=True)
            # the one seam where the mattress's face meets the boxspring's
            jy = top + mp['h']
            inside += '<path d="M%s,%s L%s,%s L%s,%s" fill="none" stroke="%s" stroke-width="1.3" stroke-opacity=".8"/>' % (
                f(X0), f(jy), f(X0 + W), f(jy), f(X0 + W + DX), f(jy + DY), shade(soft(bp['col']), -.28))
            cfg['topper']['y0'] = top - 70.0 - cfg['topper']['h']
            gtop = 70.0
        i = whole.index('<g class="ms-cr__lbl"')
        whole = whole[:i] + inside + whole[i:]
        cfg['topper']['num'] = 'I'
        tp = draw('topper', cfg['topper'], u, kind, gtop)
        for part, s, c in (('base', whole, 0), ('topper', tp, gtop)):
            s = s.replace('<g class="ms-cr__slab', '<g style="--cr-c: %spx; --cr-delay: %ss" class="ms-cr__slab' % (f(c), delay[part]), 1)
            body.append('<g class="ms-cr__depth" style="--d: %s">%s</g>' % (depth[part], s))
    else:
        if shown == ['mattress', 'base']:
            cfg['mattress']['num'], cfg['base']['num'] = 'I', 'II'
        for part in ('base', 'mattress', 'topper'):
            if part not in shown:
                continue
            s = draw(part, cfg[part], u, kind, gaps[part])
            s = s.replace('<g class="ms-cr__slab', '<g style="--cr-c: %spx; --cr-delay: %ss" class="ms-cr__slab' % (f(close[part]), delay[part]), 1)
            body.append('<g class="ms-cr__depth" style="--d: %s">%s</g>' % (depth[part], s))
    return ('<svg class="ms-cr__svg" viewBox="0 0 700 440" role="group" aria-label="[aria]"><defs>%s</defs>%s%s</svg>' % (''.join(defs), shadow, ''.join(body)))
