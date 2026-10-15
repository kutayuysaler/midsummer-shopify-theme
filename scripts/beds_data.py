"""The beds with headboards and the outdoor Tangram: what each is, from the 2026 catalogue and the
store's own product texts, and a front drawing of each, to one scale.

Nothing here says how a bed is built inside: the headboard, the cloth, the wood, the legs, the
sizes, and the house's boxsprings by name only."""

# store handle -> system key (the product templates); only handles that are the system itself
HANDLE_KEY = {
    'capri': 'capri', 'amalfi': 'amalfi', 'bellini': 'bellini', 'brera': 'brera', 'flora': 'flora',
    'storage': 'storage', 'raffaello': 'raffaello', 'vivaldi-plus': 'vivaldi-plus', 'bellagio': 'bellagio',
    'my-dream': 'my-dream', 'roma': 'roma', 'monteverdi': 'monteverdi', 'topper-roma': 'topper-roma',
    'paisley': 'paisley', 'essenziale': 'essenziale',
    'dreamy': 'dreamy-2', 'dreamy-2': 'dreamy-2', 'top': 'top-2', 'top-2': 'top-2', 'vivaldi': 'vivaldi-2', 'vivaldi-2': 'vivaldi-2',
    'giotto-round': 'giotto', 'dreamy-springs-1': 'dreamy-springs', 'dreamy-springs-mattress': 'dreamy-springs',
    'ultra-dry-mattress': 'ultra-dry', 'ultra-dry': 'ultra-dry', 'vicuna-mattress': 'vicuna', 'vicuna': 'vicuna',
    'first-dream-mattress': 'first-dream', 'mystic-river': 'roma',
}
SYSTEM_KEYS = ['amalfi', 'bellagio', 'bellini', 'brera', 'capri', 'dreamy-2', 'dreamy-springs', 'essenziale', 'first-dream', 'flora',
               'giotto', 'monteverdi', 'my-dream', 'paisley', 'raffaello', 'roma', 'storage', 'top-2', 'topper-high', 'topper-roma', 'topper-thin', 'ultra-dry',
               'vicuna', 'vivaldi-2', 'vivaldi-plus']
BOXSPRING_HANDLES = ['dreamy-springs', 'first-dream-1', 'my-dream-1', 'storage-boxspring', 'top-dream']

BOX3 = 'On a Midsummer boxspring of your choice, Dreamy Springs, Top Dream or My Dream, upholstered to match.'
# handle (and the store's spellings) -> headboard bed
HEADBOARD = {
    'cashmere-couture': dict(
        title='Cashmere Couture', draw='couture', height=137,
        line='A headboard of padded folds, parted by a band of pure silk.',
        hb='Padded folds in cashmere, velvet or Nubuck, parted at the centre by a band of pure silk: grey and orange, a flame in the fire.',
        uph='Cashmere, velvet or Nubuck; the band in pure silk', width='As wide as the bed; a larger headboard on request',
        base=BOX3, legs='Wooden legs',
        quote='Nothing happens unless first we dream.', author='Carl Sandburg'),
    'silk-flowers': dict(
        title='Silk Flowers', draw='flowers', height=154,
        line='A bas-relief of flowers and their leaves, worked by hand.',
        hb='Slim and architectural, its front a bas-relief of flowers among their leaves, made by hand, slowly, for a quiet, modern elegance.',
        uph='Nubuck, leather or a Loro Piana Interiors cloth', width='As wide as the bed; 144 cm high for Queen and King, and a low version, 108 cm, on request',
        base=BOX3, legs='Wooden legs, in several finishes',
        quote='One of the most attractive things about the flowers is their beautiful reserve.', author='Henry David Thoreau'),
    'soft-to-the-touch': dict(
        title='Soft to the Touch', draw='soft', height=107,
        line='Soft cushions curled around the headboard, on an inlay of Canaletto walnut.',
        hb='Two rich, soft cushions curled around the headboard, resting on a precious inlay of Canaletto walnut: the detail that makes the bed.',
        uph='Natural cloths, chosen with you', width='The padded bed frame runs around the bed, 30 cm longer than the mattress',
        base='On a slim First Dream boxspring, inside a padded bed frame.', legs='Beech stained walnut, or metal; Canaletto walnut on request',
        quote='Fashion passes, style remains.', author='Coco Chanel'),
    'beating-of-wings': dict(
        title='Beating of Wings', draw='wings', height=130,
        line='A sculptural headboard whose wings fold on hidden brass hinges.',
        hb='Solid poplar, upholstered and embroidered ton-sur-ton; its wings fold on hidden brass hinges, to embrace the bed or open the room.',
        uph='Nubuck, leather or a Loro Piana Interiors cloth', width='Without wings, 30 cm wider than the bed; with wings, up to 330 cm',
        base=BOX3, legs='Wooden legs',
        quote='I must have flowers next to me, always, always!', author='Claude Monet'),
    'jungle-dreams': dict(
        title='Jungle Dreams', draw='jungle', height=103,
        line='A wraparound headboard, quilted with leaves large and small.',
        hb='A wraparound headboard, padded and quilted with leaves that interweave and make way, sprout and grow, repair and protect.',
        uph='Natural cloths and leathers, chosen with you', width='Wraps the bed: 48 cm wider than the mattress',
        base=BOX3, legs='Wooden legs',
        quote='The lioness has been reunited with her cub, and all is well in the jungle.', author='Kill Bill, Vol. 3 (still in our dreams)'),
    'tulip': dict(
        title='Tulip', draw='tulip', height=105,
        line='Rounded shapes, and a capitonné made with stitches alone, no buttons.',
        hb='The rounded shapes of a classic headboard, tufted as the old upholsterers did, but without buttons: stitches alone soften the lines.',
        uph='Velvet, or a natural cloth chosen with you', width='As wide as the bed',
        base='On a slim First Dream boxspring.', legs='Slender metal legs',
        quote='Inside a sea of tulips, I would like to go on a wave of wonder.', author='Fabrizio Caramagna'),
    'pure': dict(
        title='Pure', draw='pure', height=101,
        line='Simple and precious, with room for a discreet embroidery.',
        hb='A plain, precious headboard that can carry a discreet embroidery: simple to look at, and a work that reveals itself over years of living with it.',
        uph='Natural cloths and leathers, chosen with you', width='As wide as the bed',
        base=BOX3, legs='Wooden legs',
        quote='Black as the devil, hot as hell, pure as an angel, sweet as love.', author='Talleyrand, on coffee. We think it fits a bed too'),
    'giotto': dict(
        title='Giotto', draw='giotto', height=100,
        line='A round bed in Canaletto walnut, beautiful from every side.',
        hb='A curved headboard of Canaletto walnut enclosing a panel of Vienna straw; the beveled frame is walnut too, in a natural matt finish.',
        uph='Canaletto walnut and Vienna straw', width='Ø 255 cm, to stand in the middle of the room',
        base='On a slim boxspring, inside the walnut frame.', legs='The walnut frame, close to the floor',
        quote='In the circle of a thought, sometimes I rest dreaming.', author='Alda Merini'),
}
HB_ALIASES = {'silk-fowers': 'silk-flowers', 'silk-flower': 'silk-flowers', 'jungle-dream': 'jungle-dreams', 'soft-to-touch': 'soft-to-the-touch',
              'cashmere-couture-bed': 'cashmere-couture', 'giotto-bed': 'giotto'}

TANGRAM = dict(
    facts=[('Wood', 'Of marine quality, made for sun, salt and rain'),
           ('Cushions', 'In Loro Piana Interiors outdoor cloth, in a wide palette of colours'),
           ('Padding', 'Austrian horsehair: it lets water and warmth through and dries in the sun. No foam, anywhere'),
           ('Leather', 'Water-repellent handles and cuffs, stitched by hand by Michele Cesareo, Genoa'),
           ('Design', 'With Daniela Puppa'),
           ('Bases', '100 × 100, 180 × 80 and 80 × 50 cm; alone, a base is a side table. Other sizes on request')],
)


# ── drawings: the bed seen from its foot, to one scale (1 cm = 1.75 units), on a common floor
S, G, CX = 1.75, 372.0, 320.0


def y(cm):
    return round(G - cm * S, 1)


def x(cm):
    return round(CX + cm * S, 1)


def rect(x0, y0, x1, y1, fill, extra=''):
    return '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s"%s/>' % (x0, y0, x1 - x0, y1 - y0, fill, extra)


def legs(kind, half, color, lh=9, u='hb'):
    """two legs seen from the foot, at the corners of the base; wood tapers, metal is slender"""
    out = []
    for sx in (-1, 1):
        cx_ = x(sx * (half - 8))
        if kind == 'metal':
            out.append('<path d="M%.1f %.1f L%.1f %.1f L%.1f %.1f L%.1f %.1f Z" fill="%s"/>' % (cx_ - 3.2, y(lh), cx_ + 3.2, y(lh), cx_ + 1, G, cx_ - 1, G, color))
        elif kind == 'none':
            pass
        else:
            out.append('<path d="M%.1f %.1f H%.1f L%.1f %.1f H%.1f Z" fill="url(#%s-lg)"/>' % (cx_ - 4.6, y(lh), cx_ + 4.6, cx_ + 3, G, cx_ - 3, u))
            out.append('<path d="M%.1f %.1f L%.1f %.1f" stroke="#FFF" stroke-opacity=".18" stroke-width="1"/>' % (cx_ - 2.6, y(lh) + 2, cx_ - 1.8, G - 1))
    return ''.join(out)


def bedding(cfg, u, half, top, mh):
    """pillows against the headboard, and a throw laid across the foot, hanging over the mattress"""
    out = []
    yb = y(top + mh) + 3
    for sx in (-1, 1):
        c = sx * min(44, half * .49)
        pw = min(34, half * .38)
        x0, x1, yt = x(c - pw), x(c + pw), yb - 16 * S
        out.append('<path d="M%.1f %.1f C%.1f %.1f %.1f %.1f %.1f %.1f Q%.1f %.1f %.1f %.1f C%.1f %.1f %.1f %.1f %.1f %.1f Z" fill="url(#%s-pl)" stroke="#D8CFC1" stroke-width=".8"/>' % (
            x0 + 3, yb, x0 - 3, yb - 9, x0 + 1, yt + 5, x0 + 13, yt + 1.5, (x0 + x1) / 2, yt - 4.5, x1 - 13, yt + 1.5, x1 - 1, yt + 5, x1 + 3, yb - 9, x1 - 3, yb, u))
        out.append('<path d="M%.1f %.1f Q%.1f %.1f %.1f %.1f" fill="none" stroke="#E2DACD" stroke-width="1"/>' % (x0 + 16, yt + 9, (x0 + x1) / 2, yt + 4, x1 - 16, yt + 9))
    tc = cfg.get('throw')
    if tc:
        ya, yh = y(top + mh) - 1, y(top + mh * .6)
        xa, xb = x(-half - 3), x(half + 3)
        w = xb - xa
        hem = 'L%.1f %.1f C%.1f %.1f %.1f %.1f %.1f %.1f C%.1f %.1f %.1f %.1f %.1f %.1f' % (
            xb + 1.5, yh + 2, xb - w * .2, yh + 5, xb - w * .38, yh + .5, xb - w * .55, yh + 3, xb - w * .72, yh + 5.5, xa + w * .12, yh + 1, xa - 1, yh + 3.5)
        out.append('<path d="M%.1f %.1f Q%.1f %.1f %.1f %.1f H%.1f Q%.1f %.1f %.1f %.1f %s L%.1f %.1f Z" fill="url(#%s-th)"/>' % (
            xa + 2, ya + 2, xa + 2, ya, xa + 6, ya, xb - 6, xb - 2, ya, xb - 2, ya + 2, hem, xa - 1.5, ya + 3, u))
        folds = ' '.join('M%.1f %.1f q%.1f %.1f %.1f %.1f' % (xa + w * f, ya + 4, (-1.5 if k % 2 else 1.5), (yh - ya) / 2, 0, yh - ya - 1) for k, f in enumerate((.18, .46, .79)))
        out.append('<path d="%s" fill="none" stroke="#000" stroke-opacity=".07" stroke-width="3"/>' % folds)
        out.append('<path d="M%.1f %.1f H%.1f" stroke="#FFF" stroke-opacity=".22" stroke-width="1.2"/>' % (xa + 6, ya + 1.5, xb - 6))

    return ''.join(out)


def base_and_mattress(cfg, u):
    """the boxspring (or the padded frame) and the mattress, seen from the foot, with its bedding"""
    half = cfg.get('half', 90)
    lh, bh, mh = cfg.get('leg_h', 9), cfg.get('base_h', 24), cfg.get('mat_h', 24)
    bdark = cfg['base_dark']
    # boxspring, or the padded frame round it
    b = ['<g class="ms-ba__part" data-part="base" tabindex="0" role="button" aria-label="[base]">']
    b.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="url(#%s-us)"/>' % (x(-half + 4), y(lh), (2 * half - 8) * S, lh * S, u))
    b.append(legs(cfg.get('legs', 'wood'), half, cfg.get('leg_col', '#8A6545'), lh, u))
    fh = half + (1 if cfg.get('frame') else 0)
    b.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%s" fill="url(#%s-bf)"/>' % (x(-fh), y(lh + bh), 2 * fh * S, bh * S, 5 if cfg.get('frame') else 3, u))
    if cfg.get('frame'):
        b.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="5" fill="url(#%s-tx)"/>' % (x(-fh), y(lh + bh), 2 * fh * S, bh * S, u))
    b.append('<path d="M%.1f %.1f H%.1f" stroke="#FFF" stroke-opacity=".35" stroke-width="1.2"/>' % (x(-fh + 2), y(lh + bh) + 1.6, x(fh - 2)))
    b.append('<path d="M%.1f %.1f H%.1f" stroke="%s" stroke-opacity=".5" stroke-width=".8"/>' % (x(-fh + 2), y(lh) - 1.5, x(fh - 2), bdark))
    b.append('</g>')
    # mattress, piped at both edges, rounder at its ends
    top = lh + bh
    m = ['<g class="ms-ba__part" data-part="mattress" tabindex="0" role="button" aria-label="[mattress]">']
    m.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="6" fill="url(#%s-mf)"/>' % (x(-half + 1), y(top + mh), (2 * half - 2) * S, mh * S, u))
    m.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="6" fill="url(#%s-ms)"/>' % (x(-half + 1), y(top + mh), (2 * half - 2) * S, mh * S, u))
    m.append('<path d="M%.1f %.1f H%.1f M%.1f %.1f H%.1f" stroke="#C9BDA9" stroke-width="1.1" stroke-linecap="round"/>' % (x(-half + 3), y(top + mh) + 2.2, x(half - 3), x(-half + 3), y(top) - 2.2, x(half - 3)))
    m.append(bedding(cfg, u, half, top, mh))
    m.append('</g>')
    return ''.join(b), ''.join(m), top + mh


def shade(c, k):
    """a colour made lighter (k > 0) or darker (k < 0)"""
    r, g, b = (int(c[i:i + 2], 16) for i in (1, 3, 5))
    f = (lambda v: v + (255 - v) * k) if k > 0 else (lambda v: v * (1 + k))
    return '#%02X%02X%02X' % tuple(max(0, min(255, int(round(f(v))))) for v in (r, g, b))


def grad(id_, c1, c2, vertical=True):
    return '<linearGradient id="%s" x1="0" y1="0" x2="%s" y2="%s"><stop offset="0" stop-color="%s"/><stop offset="1" stop-color="%s"/></linearGradient>' % (id_, 0 if vertical else 1, 1 if vertical else 0, c1, c2)


def headboard(key, u):
    """the headboard itself, behind the bed; one drawing per bed"""
    d = HEADBOARD[key]
    H = d['height']
    k = d['draw']
    out, defs = [], []
    if k == 'couture':
        half = 92
        x0, x1, yt = x(-half), x(half), y(H)
        defs.append(grad(u + '-hb', '#B5B4AE', '#8F8E87'))
        out.append('<path d="M%.1f %.1f V%.1f q0 -8 8 -8 H%.1f q8 0 8 8 V%.1f Z" fill="url(#%s-hb)"/>' % (x0, G, yt + 8, x1 - 8, G, u))
        # the silk band, behind the folds
        out.append(rect(x(-5), yt + 4, x(5), G, '#D2643C'))
        out.append(rect(x(-1.6), yt + 4, x(0.4), G, '#E78A62', ' opacity=".7"'))
        # padded folds, scalloped at the top
        n = 18
        w = (x1 - x0) / n
        for i in range(n):
            fx = x0 + i * w
            if abs((fx + w / 2) - CX) < 9:
                continue
            out.append('<path d="M%.1f %.1f q%.1f -6 %.1f 0 V%.1f H%.1f Z" fill="#000" opacity="%s"/>' % (fx, yt + 6, w / 2, w, G, fx, '.05' if i % 2 else '.0'))
            out.append('<path d="M%.1f %.1f V%.1f" stroke="#7D7C75" stroke-width="1" opacity=".55"/>' % (fx + w, yt + 7, G))
            out.append('<path d="M%.1f %.1f V%.1f" stroke="#D3D2CC" stroke-width="1.4" opacity=".55"/>' % (fx + w * .35, yt + 10, G))
    elif k == 'flowers':
        half = 92
        x0, x1, yt = x(-half), x(half), y(H)
        defs.append(grad(u + '-hb', '#D6CDC1', '#BDB1A2'))
        out.append(rect(x0, yt, x1, G, 'url(#%s-hb)' % u, ' rx="3"'))
        out.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="none" stroke="#A89A88" stroke-width=".8" stroke-dasharray="2.5 2.5" rx="2"/>' % (x0 + 6, yt + 6, x1 - x0 - 12, G - yt - 12))
        out.append('<clipPath id="%s-hc"><rect x="%.1f" y="%.1f" width="%.1f" height="%.1f"/></clipPath><g clip-path="url(#%s-hc)">' % (u, x0 + 8, yt + 8, x1 - x0 - 16, G - yt - 16, u))
        import math
        roses = [(-58, 128, 22), (-10, 140, 15), (34, 118, 26), (72, 140, 14), (-70, 86, 13), (-28, 98, 20), (16, 78, 14), (62, 92, 18), (-50, 50, 16), (40, 50, 12)]
        for (rx_, ry_, r) in roses:
            cx_, cy_, R = x(rx_), y(ry_), r * S * .5
            for j in range(12):
                a = j * math.pi / 6
                ex, ey = cx_ + math.cos(a) * R * .55, cy_ + math.sin(a) * R * .55
                deg = math.degrees(a)
                out.append('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" transform="rotate(%.0f %.1f %.1f)" fill="none" stroke="#EFE8DE" stroke-width="1.1"/>' % (ex, ey, R * .48, R * .2, deg, ex, ey))
                out.append('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" transform="rotate(%.0f %.1f %.1f)" fill="none" stroke="#9C8E7B" stroke-width=".8" opacity=".75"/>' % (ex + .8, ey + .9, R * .48, R * .2, deg, ex + .8, ey + .9))
            out.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="none" stroke="#E6DED3" stroke-width="1"/>' % (cx_, cy_, R * .18))
        out.append('</g>')
    elif k == 'wings':
        half, wing = 102, 52
        x0, x1, yt = x(-half), x(half), y(H)
        defs.append(grad(u + '-hb', '#EFEAE1', '#DDD5C7'))
        defs.append(grad(u + '-hw', '#D9D1C2', '#C6BCAB'))
        # the wings fold on their hinges (they beat, when you ask them)
        for sx in (-1, 1):
            hx = x0 if sx < 0 else x1
            ox = hx + sx * wing * S * .62
            out.append('<g class="ms-ba__wing" style="transform-origin: %.1fpx %.1fpx"><path d="M%.1f %.1f L%.1f %.1f L%.1f %.1f L%.1f %.1f Z" fill="url(#%s-hw)"/>' % (hx, G, hx, yt + 2, ox, yt + 14, ox, G, hx, G, u))
            for j in range(3):
                fx = hx + sx * (j + 1) * wing * S * .62 / 4
                out.append('<path d="M%.1f %.1f q2 -3 0 -6 q-2 3 0 6 Z" fill="none" stroke="#EDE7DC" stroke-width=".9"/>' % (fx, yt + 50 + j * 30))
            out.append('</g>')
            out.append('<circle cx="%.1f" cy="%.1f" r="1.8" fill="#B8954F"/><circle cx="%.1f" cy="%.1f" r="1.8" fill="#B8954F"/>' % (hx, yt + 30, hx, G - 60))
        out.append('<path d="M%.1f %.1f V%.1f q0 -6 6 -6 H%.1f q6 0 6 6 V%.1f Z" fill="url(#%s-hb)"/>' % (x0, G, yt + 6, x1 - 6, G, u))
        # ton-sur-ton embroidery: small flowers, in thread the colour of the leather
        import random
        rnd = random.Random(7)
        for _ in range(26):
            fx, fy = rnd.uniform(x0 + 14, x1 - 14), rnd.uniform(yt + 14, y(70))
            for j in range(5):
                out.append('<ellipse cx="%.1f" cy="%.1f" rx="2.6" ry="1.1" transform="rotate(%d %.1f %.1f)" fill="none" stroke="#D5CCBC" stroke-width=".8"/>' % (fx + 2.3, fy, j * 72, fx, fy))
    elif k == 'jungle':
        half = 114
        x0, x1, yt = x(-half), x(half), y(H)
        defs.append(grad(u + '-hb', '#EAE2D3', '#D6CBB6'))
        out.append('<path d="M%.1f %.1f V%.1f q0 -22 22 -22 H%.1f q22 0 22 22 V%.1f Z" fill="url(#%s-hb)"/>' % (x0, G, yt + 22, x1 - 22, G, u))
        # the returns, wrapping round the bed
        out.append('<path d="M%.1f %.1f V%.1f q0 -22 22 -22 h4 q-14 4 -14 26 V%.1f Z" fill="#C9BCA4" opacity=".55"/>' % (x0, G, yt + 22, G, ))
        out.append('<path d="M%.1f %.1f V%.1f q0 -22 -22 -22 h-4 q14 4 14 26 V%.1f Z" fill="#C9BCA4" opacity=".55"/>' % (x1, G, yt + 22, G))
        out.append('<clipPath id="%s-hc"><path d="M%.1f %.1f V%.1f q0 -22 22 -22 H%.1f q22 0 22 22 V%.1f Z"/></clipPath><g clip-path="url(#%s-hc)" fill="none" stroke="#C7B99F" stroke-width=".9">' % (u, x0 + 6, G, yt + 28, x1 - 28, G, u))
        import random
        rnd = random.Random(3)
        for _ in range(44):
            lx, ly = rnd.uniform(x0, x1), rnd.uniform(yt, G)
            L, a = rnd.uniform(14, 34), rnd.uniform(-70, 70)
            out.append('<g transform="translate(%.1f %.1f) rotate(%.0f)"><path d="M0 0 Q%.1f -%.1f %.1f 0 Q%.1f %.1f 0 0 Z M0 0 L%.1f 0"/></g>' % (lx, ly, a, L / 2, L * .32, L, L / 2, L * .32, L * .9))
        out.append('</g>')
    elif k == 'tulip':
        half = 92
        x0, x1, yt = x(-half), x(half), y(H)
        R = 40
        defs.append(grad(u + '-hb', '#3B4876', '#1F2742'))
        defs.append(grad(u + '-hs', 'rgba(255,255,255,0)', 'rgba(255,255,255,.16)', vertical=False))
        shape = 'M%.1f %.1f V%.1f q0 -%.1f %.1f -%.1f H%.1f q%.1f 0 %.1f %.1f V%.1f Z' % (x0, G, yt + R, R, R, R, x1 - R, R, R, R, G)
        out.append('<path d="%s" fill="url(#%s-hb)"/>' % (shape, u))
        out.append('<clipPath id="%s-hc"><path d="%s"/></clipPath><g clip-path="url(#%s-hc)">' % (u, shape, u))
        n = 13
        w = (x1 - x0) / n
        for i in range(n):
            fx = x0 + i * w
            out.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="url(#%s-hs)"/>' % (fx + w * .15, yt, w * .55, G - yt, u))
            out.append('<path d="M%.1f %.1f V%.1f" stroke="#141A2E" stroke-width="1.1" opacity=".7"/>' % (fx, yt, G))
        out.append('</g>')
    elif k == 'soft':
        # as in the house's front photograph: a slim upholstered headboard, narrower than the bed, and two soft
        # cushions curled over its top, resting on a thin inlay of Canaletto walnut
        cl, cd = '#B7AEA2', '#968C7F'
        defs.append(grad(u + '-hb', cl, cd))
        defs.append(grad(u + '-hp', shade(cd, -.12), shade(cd, -.28)))
        defs.append('<radialGradient id="%s-hl" cx=".38" cy=".18" r=".75"><stop offset="0" stop-color="#FFF" stop-opacity=".30"/><stop offset=".6" stop-color="#FFF" stop-opacity="0"/></radialGradient>' % u)
        defs.append(grad(u + '-wn', '#7A5236', '#4E3322'))
        defs.append('<pattern id="%s-tc" width="5" height="5" patternUnits="userSpaceOnUse"><circle cx="1.2" cy="1.4" r=".55" fill="#FFF" fill-opacity=".22"/><circle cx="3.6" cy="3.5" r=".5" fill="#000" fill-opacity=".10"/></pattern>' % u)
        ph, top = 66, 97
        # the headboard behind, with the walnut inlay along its top
        out.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="4" fill="url(#%s-hp)"/>' % (x(-ph), y(top), 2 * ph * S, (top - 56) * S, u))
        out.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="2" fill="url(#%s-wn)"/>' % (x(-ph - .5), y(top + 2.6), (2 * ph + 1) * S, 2.6 * S, u))
        out.append('<path d="M%.1f %.1f H%.1f" stroke="#B88A62" stroke-opacity=".55" stroke-width=".7"/>' % (x(-ph), y(top + 2.6) + 1.1, x(ph)))
        # the two cushions, soft at every edge, the curl over the top read as a welt and a highlight
        for sx in (-1, 1):
            c, hw = sx * 33.5, 31.5
            x0, x1 = x(c - hw), x(c + hw)
            yt, yb = y(H), y(55)
            r = 12 * S
            d = ('M%.1f %.1f L%.1f %.1f C%.1f %.1f %.1f %.1f %.1f %.1f Q%.1f %.1f %.1f %.1f C%.1f %.1f %.1f %.1f %.1f %.1f L%.1f %.1f Z' % (
                x0 + 1.5, yb, x0 - 1, yt + r, x0 - 1, yt + r * .35, x0 + r * .35, yt, x0 + r, yt + 1.2,
                (x0 + x1) / 2, yt - 3.2, x1 - r, yt + 1.2, x1 - r * .35, yt, x1 + 1, yt + r * .35, x1 + 1, yt + r, x1 - 1.5, yb))
            out.append('<path d="%s" fill="url(#%s-hb)"/>' % (d, u))
            out.append('<path d="%s" fill="url(#%s-tc)"/>' % (d, u))
            out.append('<path d="%s" fill="url(#%s-hl)"/>' % (d, u))
            out.append('<path d="M%.1f %.1f Q%.1f %.1f %.1f %.1f" fill="none" stroke="#FFF" stroke-opacity=".35" stroke-width="1.3"/>' % (x0 + 9, yt + 9, (x0 + x1) / 2, yt + 4.5, x1 - 9, yt + 9))
            out.append('<path d="M%.1f %.1f Q%.1f %.1f %.1f %.1f" fill="none" stroke="%s" stroke-opacity=".55" stroke-width=".9" stroke-dasharray="2.2 1.8"/>' % (x0 + 7, yt + 14, (x0 + x1) / 2, yt + 9, x1 - 7, yt + 14, shade(cd, -.3)))
            # the soft fall of the cloth at the cushion's foot
            out.append('<path d="M%.1f %.1f Q%.1f %.1f %.1f %.1f" fill="none" stroke="#000" stroke-opacity=".10" stroke-width="2.4"/>' % (x0 + 6, yb - 6, (x0 + x1) / 2, yb - 10, x1 - 6, yb - 6))
    elif k == 'pure':
        half = 92
        x0, x1, yt = x(-half), x(half), y(H)
        defs.append(grad(u + '-hb', '#F1ECE3', '#DED6C9'))
        out.append(rect(x0, yt, x1, G, 'url(#%s-hb)' % u, ' rx="4"'))
        out.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="none" stroke="#CFC5B6" stroke-width=".8" rx="3"/>' % (x0 + 5, yt + 5, x1 - x0 - 10, G - yt - 10))
        # the discreet embroidery
        cx_, cy_ = CX, yt + 26
        for j in range(6):
            out.append('<ellipse cx="%.1f" cy="%.1f" rx="4.2" ry="1.7" transform="rotate(%d %.1f %.1f)" fill="none" stroke="#B9A98F" stroke-width=".8"/>' % (cx_ + 4, cy_, j * 60, cx_, cy_))
        out.append('<circle cx="%.1f" cy="%.1f" r="1.3" fill="#B9A98F"/>' % (cx_, cy_))
    elif k == 'giotto':
        half = 127
        x0, x1, yt = x(-half + 18), x(half - 18), y(H)
        defs.append(grad(u + '-hb', '#8A5E3D', '#6A4529'))
        shape = 'M%.1f %.1f V%.1f q0 -26 40 -30 Q%.1f %.1f %.1f %.1f q40 4 40 30 V%.1f Z' % (x0, G, yt + 30, CX, yt - 4, x1 - 40, yt, G)
        out.append('<path d="%s" fill="url(#%s-hb)"/>' % (shape, u))
        # Vienna straw, inside the walnut
        ix0, ix1, iy0 = x0 + 12, x1 - 12, yt + 14
        out.append('<clipPath id="%s-hc"><path d="M%.1f %.1f V%.1f q0 -18 34 -22 Q%.1f %.1f %.1f %.1f q34 4 34 22 V%.1f Z"/></clipPath>' % (u, ix0, G, iy0 + 22, CX, iy0 - 4, ix1 - 34, iy0, G))
        out.append('<g clip-path="url(#%s-hc)"><rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="#DCC69B"/>' % (u, ix0, iy0 - 6, ix1 - ix0, G - iy0 + 6))
        step = 7
        lines = []
        xx = ix0 - (G - iy0)
        while xx < ix1:
            lines.append('M%.1f %.1f L%.1f %.1f M%.1f %.1f L%.1f %.1f' % (xx, G, xx + (G - iy0 + 6), iy0 - 6, xx + (G - iy0 + 6), G, xx, iy0 - 6))
            xx += step
        out.append('<path d="%s" stroke="#B89C68" stroke-width=".8" fill="none"/>' % ' '.join(lines))
        hx = ix0 + 3.5
        holes = []
        while hx < ix1:
            hy = iy0 + 3.5
            while hy < G:
                holes.append('M%.1f %.1f m-1.5 0 a1.5 1.5 0 1 0 3 0 a1.5 1.5 0 1 0 -3 0' % (hx, hy))
                hy += step
            hx += step
        out.append('<path d="%s" fill="#C2A675" opacity=".55"/>' % ' '.join(holes))
        out.append('</g>')
    return ''.join(defs), ''.join(out)


BED = {   # base and mattress look, per headboard bed
    'cashmere-couture': dict(base='#A4A39D', base_dark='#76756F', throw='#D2643C', legs='wood', leg_col='#6F5139'),
    'silk-flowers': dict(base='#CBC1B4', base_dark='#9E9282', throw='#8D8F94', legs='wood', leg_col='#7A5A3E'),
    'soft-to-the-touch': dict(base='#A9A095', base_dark='#8A8176', throw='#7E3B33', legs='wood', leg_col='#5E4330', frame=True, half=90, leg_h=19, base_h=14, mat_h=21, mat=('#CFC8BD', '#B9B1A5')),
    'beating-of-wings': dict(base='#E5DED2', base_dark='#B5AA98', throw='#B8A88E', legs='wood', leg_col='#8A6545', half=90),
    'jungle-dreams': dict(base='#E2D9C8', base_dark='#B2A58D', throw='#2F5E63', legs='wood', leg_col='#7A5A3E'),
    'tulip': dict(base='#2B3558', base_dark='#141A2E', throw='#F4EFE6', legs='metal', leg_col='#A39A8C', base_h=16),
    'pure': dict(base='#E7E0D4', base_dark='#B7AB98', throw='#6F747B', legs='wood', leg_col='#8A6545'),
    'giotto': dict(base='#7A5236', base_dark='#4E3220', throw='#C9A46A', legs='none', half=118, leg_h=4, base_h=30, mat_h=20),
}


def drawing(key, u='hb'):
    """the whole bed: headboard behind, then the boxspring and the mattress; [base]/[mattress]/[headboard] are labels"""
    cfg = BED[key]
    hdefs, hb = headboard(key, u)
    mat = cfg.get('mat', ('#F7F2EA', '#E3D8C6'))
    lc = cfg.get('leg_col', '#8A6545')
    defs = (hdefs + grad(u + '-bf', cfg['base'], cfg['base_dark']) + grad(u + '-mf', mat[0], mat[1]) + grad(u + '-lg', lc, shade(lc, -.35), vertical=False)
            + grad(u + '-pl', '#FFFFFF', '#EAE3D7')
            + '<linearGradient id="%s-us" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#17140F" stop-opacity=".16"/><stop offset="1" stop-color="#17140F" stop-opacity="0"/></linearGradient>' % u
            + '<linearGradient id="%s-ms" x1="0" x2="1"><stop offset="0" stop-color="#000" stop-opacity=".10"/><stop offset=".08" stop-color="#000" stop-opacity="0"/>'
              '<stop offset=".92" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".12"/></linearGradient>' % u
            + (grad(u + '-th', shade(cfg['throw'], .12), shade(cfg['throw'], -.12)) if cfg.get('throw') else '')
            + ('<pattern id="%s-tx" width="5" height="5" patternUnits="userSpaceOnUse"><circle cx="1.2" cy="1.4" r=".55" fill="#FFF" fill-opacity=".22"/><circle cx="3.6" cy="3.5" r=".5" fill="#000" fill-opacity=".10"/></pattern>' % u))
    b, m, mtop = base_and_mattress(cfg, u)
    H = HEADBOARD[key]['height']
    # the headboard's height, written like a drawing
    dx = x(cfg.get('half', 90) + 34 if key not in ('jungle-dreams', 'beating-of-wings', 'giotto') else 140)
    dim = ('<g class="ms-ba__dim" aria-hidden="true"><path d="M%.1f %.1f h10 M%.1f %.1f V%.1f M%.1f %.1f h10" />'
           '<text x="%.1f" y="%.1f">%d cm</text></g>') % (dx - 5, y(H), dx, y(H), G, dx - 5, G, dx + 8, (y(H) + G) / 2 + 4, H)
    svg = ('<svg class="ms-ba__svg" viewBox="0 0 640 392" role="group" aria-label="[aria]"><defs>%s</defs>'
           '<ellipse cx="320" cy="374" rx="250" ry="7" fill="rgba(23,20,15,.08)"/>'
           '<g class="ms-ba__part" data-part="headboard" tabindex="0" role="button" aria-label="[headboard]">%s</g>%s%s%s'
           '<path d="M40 %.1f H600" stroke="rgba(23,20,15,.25)" stroke-width=".8"/></svg>') % (defs, hb, b, m, dim, G + .5)
    return svg
