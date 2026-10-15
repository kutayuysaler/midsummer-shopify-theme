# Round 21, run at the end of bin/build_more.py in its scope (THEME, SP, tpl_load, tpl_save...), after
# Round 20. Every step is an exact replacement or a guarded copy, so a second build changes nothing.
import shutil as _sh

_r21_n = 0


def _r21_sub(path, pairs):
    """Replace each (old, new) in the file at path; a pair already applied is skipped."""
    global _r21_n
    _t = open(path, encoding='utf-8').read()
    _u = _t
    for _a, _b in pairs:
        if _a in _u:
            _u = _u.replace(_a, _b)
    if _u != _t:
        open(path, 'w', encoding='utf-8').write(_u)
        _r21_n += 1


# ── Handmade in Italy opens on an artisan at work on a mattress (the shop's photograph showed a panel
#    being upholstered): the fibre opened by hand over the wool, in black and white so it is not the
#    home page's photograph again. The last stage, the cloth, shows a bed dressed in Loro Piana
#    Interiors (Paisley, in Katai and Shadan) rather than a terrace on the coast.
_src = SP + '/vendor/r21/ms-photo-artisan-fibre-bw.jpg'
_dst = THEME + '/assets/ms-photo-artisan-fibre-bw.jpg'
if not os.path.exists(_dst) or open(_src, 'rb').read() != open(_dst, 'rb').read():
    _sh.copy(_src, _dst)
_SHOP_HERO = 'shopify://shop_images/Untitled_Project_5_b49a7740-07fa-45f1-8b4f-464d951b0772.jpg'
_SHOP_HERO_FB = 'https://midsummer-milano.com/cdn/shop/files/Untitled_Project_5_b49a7740-07fa-45f1-8b4f-464d951b0772.jpg?width=2400'
for _name in ('page.handmade-in-italy', 'collection.ms-handmade'):
    _p = THEME + '/templates/%s.json' % _name
    if not os.path.exists(_p):
        continue
    _h, _d = tpl_load(_name + '.json')
    _ch = False
    for _sec in _d['sections'].values():
        _st = _sec.get('settings', {})
        if _sec.get('type') == 'ms-banner' and _st.get('image') == _SHOP_HERO:
            _st.pop('image')
            _st['image_fallback'] = 'ms-photo-artisan-fibre-bw.jpg'
            _ch = True
        if _sec.get('type') == 'ms-banner' and _st.get('image_fallback') == _SHOP_HERO_FB:
            _st['image_fallback'] = 'ms-photo-artisan-fibre-bw.jpg'
            _ch = True
        # the claims audit: no count of artisans
        if _st.get('text') == 'Two Italian artisans. Two or three full days. One bed.':
            _st['text'] = 'Italian artisans. Two or three full days. One bed.'
            _ch = True
        _t = _st.get('text', '')
        if 'Because one pair of hands follows the bed through every stage, ' in _t:
            _st['text'] = _t.replace('Because one pair of hands follows the bed through every stage, ',
                                     'Because the bed is made by hand at every stage, ')
            _ch = True
        for _b in _sec.get('blocks', {}).values():
            _bs = _b.get('settings', {})
            if _bs.get('title') == 'The cloth' and _bs.get('image_fallback') == 'ms-graded-bougainvillea.jpg':
                _bs['image_fallback'] = 'ms-photo-lp-paisley-side.jpg'
                _ch = True
    if _ch:
        tpl_save(_name + '.json', _h, _d)
        _r21_n += 1

# ── The home page's delivery line: a check-up at fifteen years, without calling it free.
_r21_sub(THEME + '/sections/ms-home-09.liquid', [
    ('Brought into the room, assembled and dressed. Then a free check-up when year fifteen arrives.',
     'Brought into the room, assembled and dressed. Then a check-up when year fifteen arrives.')])

# ── The atelier in figures (Our story): products, not systems; no count of artisans (the claims audit:
#    two or three full days of handwork is what the Handmade page says); and under "Made to order", the
#    choice that reaches down to the fibres, for winter and for summer.
_r21_sub(THEME + '/sections/ms-home-06.liquid', [
    ('"label": "Systems across three collections",\n      "default": "Systems across three collections"',
     '"label": "Figure 2 · what",\n      "default": "Products across three collections"'),
    ('"label": "Under vicuña and cashmere, fully u…",\n      "default": "Under vicuña and cashmere, fully upholstered."',
     '"label": "Figure 3 · note",\n      "default": "Down to the fibres: the warmest for winter, the freshest for summer."'),
    ('"label": "2",\n      "default": "2"', '"label": "Figure 1",\n      "default": "2–3"'),
    ('"label": "Artisans build each system, start …",\n      "default": "Artisans build each system, start to finish"',
     '"label": "Figure 1 · what",\n      "default": "Full days of handwork in every mattress"'),
])

# ── 15 + 15: the regeneration is the house's; the transport, both ways, the owner's. Said once, quietly,
#    in the paragraph that invites the owner to write.
_r21_sub(THEME + '/sections/ms-regen-05.liquid', [
    ('oversee its regeneration with our Italian artisans."',
     'oversee its regeneration with our Italian artisans. The regeneration is offered by the house; the transport, there and back, is at your charge."')])

# ── The house tone on every photograph, product photographs included. It used to pass over any picture
#    whose address held the word "logo" (meant for logos), and product photographs exported as
#    "… no logo.jpg" slipped through with it; logos are now told by their markup (SVG files, the press
#    marks, the header's and footer's logo, which carry ms-no-tone), never by a file name. And it now
#    reaches the pages drawn by the base theme's layout too (the cart), whose body is not .ms-site.
_r21_sub(THEME + '/snippets/ms-photo-tone.liquid', [
    ('    .ms-site img:not([src*=".svg"]):not([src*="ms-press-"]):not([src*="ms-fibre-draw"]):not([src*="logo"]):not(.ms-no-tone),\n    .ms-site video {',
     '    body img:not([src*=".svg"]):not([src*="ms-press-"]):not([src*="ms-fibre-draw"]):not([data-ms-logo]):not(.ms-no-tone),\n    body video {'),
    ('    .ms-site .ms-lf img, .ms-site .ms-pr img,',
     '    .header-logo img, .logo-block__image-wrapper img { filter: none !important; }\n    .ms-site .ms-lf img, .ms-site .ms-pr img,'),
])
_r21_sub(THEME + '/assets/ms-site.css', [
    ('.ms-site img:not([src*="graded"]):not([src*="logo"]), .ms-site video { filter: var(--ms-grade); }',
     '.ms-site img:not([src*="graded"]):not([src*=".svg"]):not([data-ms-logo]):not(.ms-no-tone), .ms-site video { filter: var(--ms-grade); }')])
_r21_sub(THEME + '/sections/ms-header.liquid', [
    ('<img width="577" height="136" alt="Midsummer Milano" data-ms-logo="" src=', '<img class="ms-no-tone" width="577" height="136" alt="Midsummer Milano" data-ms-logo="" src='),
    ('<img width="577" height="136" alt="Midsummer Milano" loading="lazy" src=', '<img class="ms-no-tone" width="577" height="136" alt="Midsummer Milano" loading="lazy" src=')])
_r21_sub(THEME + '/sections/ms-footer.liquid', [
    ('<img loading="lazy" width="577" height="136" alt="Midsummer Milano" src=', '<img class="ms-no-tone" loading="lazy" width="577" height="136" alt="Midsummer Milano" src=')])

# ── A Loro Piana Interiors cloth is named as a fabric wherever a product is described: "Mystic River
#    fabric", "Mystic River and Connemara fabrics", unless a material already follows the name (Connemara
#    linen, Katai silk, Wish bouclé) or the name is data (the cloth list a section reads, the anchors).
#    The Loro Piana Interiors page itself, where each name is the title of a cloth, keeps them bare.
#    In Italian "tessuto", in Russian "ткань", said once at the head of the phrase.
import glob as _gl
_CL = r"(?:Mystic River|Connemara|Altai|Wish|Cardi|Ely[’']s Harbour|Bangor|Shadan|Katai)"
_CL_RX = _re.compile(r"(?<![\w-])(" + _CL + r"(?:(?:, | and | or )" + _CL + r")*)(?![\w’'-])")
_NOUN_RX = _re.compile(r"\s+(?:linen|silk|bouclé|wool|cashmere|fabrics?|cloths?|colours?)\b")


def _r21_fabric(t):
    out = []
    for ln in t.split('\n'):
        out.append(ln if ('"label":' in ln or '"name":' in ln or '_name"' in ln) else _CL_RX.sub(lambda m, ln=ln: _r21_one(ln, m), ln))
    return '\n'.join(out)


def _r21_one(ln, m):
    a = m.start()
    if ln[max(0, a - 12):a].endswith("'lp' -%}"):
        return m.group(0)
    if _NOUN_RX.match(ln, m.end()):
        return m.group(0)
    lst = m.group(1)
    many = (' and ' in lst or ', ' in lst) and ' or ' not in lst
    return lst + (' fabrics' if many else ' fabric')


_fab_files = [THEME + '/snippets/ms-sys-data.liquid', THEME + '/snippets/ms-product-cloth.liquid',
              THEME + '/sections/ms-home-04.liquid', THEME + '/sections/ms-quiz.liquid']
_fab_files += sorted(_gl.glob(THEME + '/templates/product.*.json'))
_fab_files += [THEME + '/templates/%s.json' % n for n in ('collection.ms-compare', 'page.compare', 'collection.ms-hospitality', 'page.hospitality',
                                                         'collection.ms-professionals', 'page.professionals', 'page.salone-2026')]
for _f in _fab_files:
    if not os.path.exists(_f):
        continue
    _t = open(_f, encoding='utf-8').read()
    _u = _r21_fabric(_t)
    if _u != _t:
        open(_f, 'w', encoding='utf-8').write(_u)
        _r21_n += 1
# the product notes: English after the last "else", Italian and Russian by hand
_f = THEME + '/snippets/ms-product-note.liquid'
_t = open(_f, encoding='utf-8').read()
_i = _t.rindex('{%- else -%}')
_u = _t[:_i] + _r21_fabric(_t[_i:])
for _a, _b in (("in un’unica linea pulita, in Mystic River.", "in un’unica linea pulita, in tessuto Mystic River."),
               ("Il comfort del capitonné, in Loro Piana Interiors Mystic River.", "Il comfort del capitonné, in tessuto Loro Piana Interiors Mystic River."),
               ("Un contenitore senza linee visibili, in Mystic River.", "Un contenitore senza linee visibili, in tessuto Mystic River."),
               ("-%}Cardi e Wish di Loro Piana Interiors, in lana e cashmere.", "-%}Tessuti Cardi e Wish di Loro Piana Interiors, in lana e cashmere."),
               ("-%}Loro Piana Interiors Mystic River, bordato in rosa Midsummer.", "-%}Tessuto Loro Piana Interiors Mystic River, bordato in rosa Midsummer."),
               ("-%}Loro Piana Interiors Mystic River с окантовкой", "-%}Ткань Loro Piana Interiors Mystic River с окантовкой")):
    _u = _u.replace(_a, _b)
if _u != _t:
    open(_f, 'w', encoding='utf-8').write(_u)
    _r21_n += 1

# ── The Loro Piana Interiors colours, true to the cards: Connemara and Altai measured again on the
#    cards from the atelier's swatch folder (lp/card_swatches.py: each swatch balanced against the paper
#    beside it, its mean taken in linear light, drawn with the card's own weave). And no house tone on
#    the cloths: a colour chosen from the screen is the colour of the card, not a warmer one.
for _f in sorted(_gl.glob(SP + '/vendor/lp21/ms-lp-*.jpg')):
    _d = THEME + '/assets/' + os.path.basename(_f)
    if not os.path.exists(_d) or open(_f, 'rb').read() != open(_d, 'rb').read():
        _sh.copy(_f, _d)
        _r21_n += 1
_r21_sub(THEME + '/snippets/ms-photo-tone.liquid', [
    ('):not([src*="ms-fibre-draw"]):not([data-ms-logo]):not(.ms-no-tone),', '):not([src*="ms-fibre-draw"]):not([src*="ms-lp-"]):not([data-ms-logo]):not(.ms-no-tone),')])
_r21_sub(THEME + '/assets/ms-site.css', [
    ('.ms-site img:not([src*="graded"]):not([src*=".svg"]):not([data-ms-logo]):not(.ms-no-tone),', '.ms-site img:not([src*="graded"]):not([src*=".svg"]):not([src*="ms-lp-"]):not([data-ms-logo]):not(.ms-no-tone),')])

# ── Sizes named again (the owner's request), one rule for every product, by width: Single under 110 cm,
#    Small double 120, Double 140, Queen 160, King 180, Super King from 190 (the American 153 × 203 and 193 × 203
#    are US Queen and US King, so no two sizes share a name); each with its width × length
#    beneath. Round beds (Giotto) keep their diameters. The names are the theme's translations.
_r21_sub(THEME + '/sections/ms-product-reasons.liquid', [
    ('<section data-dc-tpl="764" data-ms-round="{{ ms_round }}"',
     '<section data-dc-tpl="764" data-ms-round="{{ ms_round }}" data-ms-size-names="{{ \'ms.product.size_single\' | t | escape }}|{{ \'ms.product.size_small_double\' | t | escape }}|{{ \'ms.product.size_double\' | t | escape }}|{{ \'ms.product.size_queen\' | t | escape }}|{{ \'ms.product.size_king\' | t | escape }}|{{ \'ms.product.size_super_king\' | t | escape }}|{{ \'ms.product.size_us_queen\' | t | escape }}|{{ \'ms.product.size_us_king\' | t | escape }}"'),
    ('aria-pressed="false">{{ section.settings[kw] }} × {{ section.settings[kl] }}</button>',
     'aria-pressed="false">{%- liquid\n    assign ms_sw = section.settings[kw] | plus: 0\n    assign ms_sl = section.settings[kl] | plus: 0\n    if ms_sl >= 202 and ms_sl <= 204 and ms_sw >= 150 and ms_sw <= 155\n      assign ms_sn = \'ms.product.size_us_queen\' | t\n    elsif ms_sl >= 202 and ms_sl <= 204 and ms_sw >= 190 and ms_sw <= 195\n      assign ms_sn = \'ms.product.size_us_king\' | t\n    elsif ms_sw < 110\n      assign ms_sn = \'ms.product.size_single\' | t\n    elsif ms_sw < 130\n      assign ms_sn = \'ms.product.size_small_double\' | t\n    elsif ms_sw < 150\n      assign ms_sn = \'ms.product.size_double\' | t\n    elsif ms_sw < 170\n      assign ms_sn = \'ms.product.size_queen\' | t\n    elsif ms_sw < 190\n      assign ms_sn = \'ms.product.size_king\' | t\n    else\n      assign ms_sn = \'ms.product.size_super_king\' | t\n    endif\n  -%}<span class="ms-szp__n">{{ ms_sn }}</span><span class="ms-szp__d">{{ section.settings[kw] }} × {{ section.settings[kl] }}</span></button>'),
    ("  function fmt(w, l) { return ROUND ? 'Ø ' + Math.round(w) : Math.round(w) + ' × ' + Math.round(l); }",
     "  function fmt(w, l) { return ROUND ? 'Ø ' + Math.round(w) : Math.round(w) + ' × ' + Math.round(l); }\n"
     "  // the name of a size, by its width, the same on every product: Single … Super King\n"
     "  var NAMES = (root.getAttribute('data-ms-size-names') || 'Single|Small double|Double|Queen|King|Super King|US Queen|US King').split('|');\n"
     "  function nameOf(w, l) { w = +w; l = +l; if (l >= 202 && l <= 204 && w >= 150 && w <= 155) return NAMES[6] || ''; if (l >= 202 && l <= 204 && w >= 190 && w <= 195) return NAMES[7] || '';\n"
     "    return NAMES[w < 110 ? 0 : w < 130 ? 1 : w < 150 ? 2 : w < 170 ? 3 : w < 190 ? 4 : 5] || ''; }"),
    ("      b.textContent = fmt(o.w, o.l);",
     "      if (ROUND) { b.textContent = fmt(o.w, o.l); } else {  // a round bed keeps its diameter alone\n"
     "        var n = document.createElement('span'); n.className = 'ms-szp__n'; n.textContent = nameOf(o.w, o.l);\n"
     "        var dd = document.createElement('span'); dd.className = 'ms-szp__d'; dd.textContent = fmt(o.w, o.l);\n"
     "        b.appendChild(n); b.appendChild(dd);\n"
     "      }"),
    ("    say(fmt(d[0], d[1]) + ' cm', d[2]);",
     "    say((ROUND ? '' : nameOf(d[0], d[1]) + ' · ') + fmt(d[0], d[1]) + ' cm', d[2]);"),
    ('      .ms-site .ms-szp__c { background: none; border: 0; border-bottom: 1px solid transparent; padding: 12px 0 6px; cursor: pointer;',
     '      .ms-szp__n, .ms-szp__d { display: block; }\n'
     '      .ms-szp__d { margin-top: 3px; font-family: "Red Hat Text", system-ui, sans-serif; font-size: 10.5px; letter-spacing: .1em; color: #7A7266; }\n'
     '      .ms-site .ms-szp__c[aria-pressed="true"] .ms-szp__d { color: #4A443B; }\n'
     '      .ms-site .ms-szp__c { text-align: left; background: none; border: 0; border-bottom: 1px solid transparent; padding: 12px 0 6px; cursor: pointer;'),
    ('"content": "Every bed is made to measure: the sizes below are examples, shown as width × length in cm. A product that lists its own sizes in its description shows those instead."',
     '"content": "Every bed is made to measure: the sizes below are examples, each named by its width (Single under 110 cm, Small double 120, Double 140, Queen 160, King 180, Super King from 190; the American 153 × 203 and 193 × 203 are US Queen and US King) with its width × length in cm beneath. A product that lists its own sizes in its description shows those instead."'),
])

print('round 21: %d files changed' % _r21_n)
