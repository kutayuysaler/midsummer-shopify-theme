# Round 28, run at the end of bin/build_more.py in its scope (THEME, tpl_load, tpl_save, and Round 27's
# helpers), after Round 27. Every step is an exact replacement or a guarded write, so a second build
# changes nothing.
#  · The press line: no dark disc under the cursor; the system's own hand (grab, grabbing) over it.
#  · Vanity Fair's mark without the white ground drawn behind it.

_r28_n = 0


def _r28_sub(path, pairs):
    global _r28_n
    _t = open(path, encoding='utf-8').read()
    _u = _t
    for _a, _b in pairs:
        # a replacement that holds what it replaces is made once, when its result is not there yet
        if _a in _b and _b in _u:
            continue
        if _a in _u:
            _u = _u.replace(_a, _b)
        else:
            assert _b in _u, (path, _a[:80])
    if _u != _t:
        open(path, 'w', encoding='utf-8').write(_u)
        _r28_n += 1


def _r28_copy(src, dst):
    global _r28_n
    if not os.path.exists(dst) or open(src, 'rb').read() != open(dst, 'rb').read():
        shutil.copy(src, dst)
        _r28_n += 1


# ── the press line: the hand of the system over it, nothing drawn under the cursor
_PRP28 = THEME + '/sections/ms-hp-proof.liquid'
_t = open(_PRP28, encoding='utf-8').read()
_u = re.sub(r'        <span class="ms-pr__cursor" aria-hidden="true">.*?</span></span>\n', '', _t)
_u = re.sub(r"  \.ms-pr__cursor \{ position: absolute;.*?  @media \(hover: none\), \(pointer: coarse\) \{ \.ms-pr__cursor \{ display: none; \} \}\n",
            """  /* Round 28: the system's own hand over the line, held while it is moved */
  .ms-pr__rail { cursor: grab; }
  .ms-pr__rail.is-dragging, .ms-pr__rail.is-dragging * { cursor: grabbing !important; }
""", _u, flags=re.S)
_u = _u.replace(", cur = root.querySelector('.ms-pr__cursor');", ';')
_u = re.sub(r"      if \(cur && fine\.matches && rail\.classList\.contains\('is-cursor'\)\) \{\n.*?\n      \}\n", '', _u, flags=re.S)
_u = _u.replace("held = rail.classList.contains('is-cursor')", "held = rail.classList.contains('is-hover')")
_u = re.sub(r"    if \(cur\) \{\n      rail\.addEventListener\('pointerenter'.*?\n    \}\n",
            """    // under the mouse the line waits; a finger moves it
    rail.addEventListener('pointerenter', function (e) { if (e.pointerType === 'mouse') { rail.classList.add('is-hover'); held = true; } });
    rail.addEventListener('pointerleave', function () { rail.classList.remove('is-hover'); if (!drag) held = false; });
""", _u, flags=re.S)
_u = re.sub(r"    // a longer word for \"drag\" \(in another language\).*?\n    \}\n", '', _u, flags=re.S)
assert 'ms-pr__cursor' not in _u and 'is-cursor' not in _u and 'cur.' not in _u and 'cursor: grab;' in _u and "classList.add('is-hover')" in _u, 'press r28'
if _u != _t:
    open(_PRP28, 'w', encoding='utf-8').write(_u)
    _r28_n += 1
_r28_sub(THEME + '/assets/ms-press-vanity-fair.svg', [('<rect width="328" height="72" fill="white"/>', '')])

# ── the corner: an enquiry instead of WhatsApp (WhatsApp stays among the socials). It opens the
#    enquiry sheet; on, and named, from Theme settings → Midsummer · Social
_r28_copy(SP + '/bin/r28/ms-whatsapp.liquid', THEME + '/snippets/ms-whatsapp.liquid')
_SS28 = THEME + '/config/settings_schema.json'
_t = open(_SS28, encoding='utf-8').read()
_ss = json.loads(_t)
for _grp in _ss:
    _st = _grp.get('settings', [])
    for _i, _x in enumerate(_st):
        if _x.get('id') == 'ms_whatsapp_button':
            _st[_i] = {'type': 'checkbox', 'id': 'ms_enquiry_bubble', 'label': 'Show the enquiry button in the corner',
                       'info': 'A small button that opens the enquiry form, once the visitor has scrolled a little.', 'default': True}
        elif _x.get('id') == 'ms_whatsapp_label':
            _st[_i] = {'type': 'text', 'id': 'ms_enquiry_bubble_label', 'label': 'Enquiry button label', 'default': 'Enquire'}
_u = json.dumps(_ss, indent=2, ensure_ascii=False) + '\n'
assert 'ms_enquiry_bubble_label' in _u and 'ms_whatsapp_button' not in _u, 'enquiry bubble settings'
if _u != _t:
    open(_SS28, 'w', encoding='utf-8').write(_u)
    _r28_n += 1
_SD28 = THEME + '/config/settings_data.json'
_t = open(_SD28, encoding='utf-8').read()
_u = _t.replace('    "ms_whatsapp_button": true,\n    "ms_whatsapp_label": "Chat with the atelier",\n',
                '    "ms_enquiry_bubble": true,\n    "ms_enquiry_bubble_label": "Enquire",\n')
assert '"ms_enquiry_bubble": true' in _u and 'ms_whatsapp_button' not in _u, 'enquiry bubble data'
if _u != _t:
    open(_SD28, 'w', encoding='utf-8').write(_u)
    _r28_n += 1

# on a product page the bar at the foot already asks for a proposal: the corner keeps clear of it
_r28_sub(THEME + '/sections/ms-product-main.liquid', [
    ('    body.ms-bar-on .ms-wa { bottom: calc(var(--ms-bar-h, 80px) + 12px) !important; }',
     '    body.ms-bar-on .ms-wa { opacity: 0 !important; pointer-events: none !important; }'),
])

# ── Top: the award's label out at the section's top-right corner, clear of the drawing (on a phone,
#    above the drawing at the right)
_AW_HEAD = _SEAL[:_SEAL.index('        {%- if cr_award -%}')]
assert _AW_HEAD.startswith('      <figure class="ms-cr__draw">\n')
_AW_LIQ = _AW_HEAD[len('      <figure class="ms-cr__draw">\n'):]
_r28_sub(THEME + '/sections/ms-craft.liquid', [
    (_AW_HEAD + _LABEL, '      <figure class="ms-cr__draw">\n'),
    ('    <div class="ms-cr__top">\n', '    <div class="ms-cr__top">\n' + _AW_LIQ + _LABEL),
    ("  .ms-site a.ms-cr__award { position: relative; z-index: 1; display: flex; width: max-content; max-width: 100%; align-items: center; gap: 14px; margin: 0 0 -4% 6%;",
     "  .ms-cr__top { position: relative; }\n  .ms-site a.ms-cr__award { position: absolute; top: 0; right: 0; z-index: 1; display: flex; width: max-content; max-width: 100%; align-items: center; gap: 14px; margin: 0;"),
    ("  @media (max-width: 760px) { .ms-site a.ms-cr__award { gap: 12px; padding: 9px 14px 9px 10px; }",
     "  @media (max-width: 900px) { .ms-site a.ms-cr__award { position: static; order: -2; justify-self: end; margin: 0 0 clamp(4px, 2vw, 14px); } }\n  @media (max-width: 760px) { .ms-site a.ms-cr__award { gap: 12px; padding: 9px 14px 9px 10px; }"),
])
_u = open(THEME + '/sections/ms-craft.liquid', encoding='utf-8').read()
assert _u.count('class="ms-cr__award"') == 1 and _u.index('class="ms-cr__award"') < _u.index('<figure class="ms-cr__draw">'), 'award at the corner'

# ── phones: the openings sharp and well framed. A wide photograph in a phone's tall frame is shown at
#    about one and a half to two screen heights wide, so it is fetched at that width (sizes); and an
#    opening may have an upright photograph of its own for phones (scripts/phone_photos_r28.py)
# (with them, Altai's sixteen colours drawn again as a milled wool, scripts/altai_r28.py, over Round 21's)
for _f in sorted(glob.glob(SP + '/vendor/r28/*.jpg')):
    _r28_copy(_f, THEME + '/assets/' + os.path.basename(_f))
_PHONE_CAP = """{%- comment -%} Round 28: on a phone, the upright photograph when there is one {%- endcomment -%}
{%- liquid
  assign ph_set = ''
  if PFX.image_mobile != blank or PFX.image_fallback_mobile != blank
    capture ph_set
      render 'ms-srcset', image: PFX.image_mobile, fallback: PFX.image_fallback_mobile, width: 1200, sizes: '100vw'
    endcapture
    assign ph_set = ph_set | strip
    if ph_set == ''
      capture ph_set
        echo 'srcset="'
        render 'ms-img', image: PFX.image_mobile, fallback: PFX.image_fallback_mobile, width: 1200
        echo '"'
      endcapture
    endif
  endif
-%}
"""
_PHONE_SCHEMA = """    { "type": "image_picker", "id": "image_mobile", "label": "Photograph on a phone (optional)", "info": "An upright photograph for phones; without one, phones crop the photograph above." },
    { "type": "text", "id": "image_fallback_mobile", "label": "Phone photograph address (optional)", "info": "Used when no phone photograph is picked." },
"""
_r28_sub(THEME + '/sections/ms-banner.liquid', [
    ('<section class="ms-bn ms-bn--{{ section.settings.align }}" style="{{ h }}">',
     _PHONE_CAP.replace('PFX', 'section.settings') + """{%- liquid
  case section.settings.height
    when 'full'
      assign bn_sizes = '(max-width: 760px) 180vh, 100vw'
    when 'tall'
      assign bn_sizes = '(max-width: 760px) 150vh, 100vw'
    else
      assign bn_sizes = '(max-width: 760px) 120vh, 100vw'
  endcase
-%}
<section class="ms-bn ms-bn--{{ section.settings.align }}" style="{{ h }}">"""),
    ("""    <img class="ms-bn__media" src="{% render 'ms-img', image: section.settings.image, fallback: section.settings.image_fallback, width: 2400 %}" {% render 'ms-srcset', image: section.settings.image, fallback: section.settings.image_fallback, width: 2400, sizes: '100vw' %}
      alt="{{ section.settings.image.alt | default: heading | escape }}" width="2400" height="1350" fetchpriority="high"
      style="object-position: {{ section.settings.focus }};">""",
     """    <picture>
      {%- if ph_set != '' -%}<source media="(max-width: 760px)" {{ ph_set }}>{%- endif -%}
      <img class="ms-bn__media" src="{% render 'ms-img', image: section.settings.image, fallback: section.settings.image_fallback, width: 2400 %}" {% render 'ms-srcset', image: section.settings.image, fallback: section.settings.image_fallback, width: 2400, sizes: bn_sizes %}
        alt="{{ section.settings.image.alt | default: heading | escape }}" width="2400" height="1350" fetchpriority="high"
        style="object-position: {{ section.settings.focus }};">
    </picture>"""),
    ('  .ms-bn__media { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }',
     '  .ms-bn__media { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }\n  .ms-bn picture { display: contents; }'),
    ("""    { "type": "text", "id": "image_fallback", "label": "Photograph address", "info": "Used when no photograph is picked: a full address, or a file in the theme's assets." },
""", """    { "type": "text", "id": "image_fallback", "label": "Photograph address", "info": "Used when no photograph is picked: a full address, or a file in the theme's assets." },
""" + _PHONE_SCHEMA),
])
_r28_sub(THEME + '/sections/ms-hp-chapter.liquid', [
    ("""<section class="ms-ch ms-ch--{{ s.layout }}""", _PHONE_CAP.replace('PFX', 's') + """<section class="ms-ch ms-ch--{{ s.layout }}"""),
    ("""        <img src="{% render 'ms-img', image: s.image, fallback: s.image_fallback, width: 2000 %}" {% render 'ms-srcset', image: s.image, fallback: s.image_fallback, width: 2000, sizes: '100vw' %} alt=""",
     """        <picture>{%- if ph_set != '' -%}<source media="(max-width: 760px)" {{ ph_set }}>{%- endif -%}<img src="{% render 'ms-img', image: s.image, fallback: s.image_fallback, width: 2000 %}" {% if s.layout == 'full' %}{% render 'ms-srcset', image: s.image, fallback: s.image_fallback, width: 2400, sizes: '(max-width: 760px) 180vh, 100vw' %}{% else %}{% render 'ms-srcset', image: s.image, fallback: s.image_fallback, width: 2000, sizes: '100vw' %}{% endif %} alt="""),
    ("""{% if s.shape == 'landscape' %}1500{% else %}2500{% endif %}" loading="lazy">
      </div>""", """{% if s.shape == 'landscape' %}1500{% else %}2500{% endif %}" loading="lazy"></picture>
      </div>"""),
    ('  .ms-ch__media img { width: 100%; height: 100%; object-fit: cover; display: block; }',
     '  .ms-ch__media img { width: 100%; height: 100%; object-fit: cover; display: block; }\n  .ms-ch__media picture { display: contents; }'),
    ("""    { "type": "text", "id": "image_fallback", "label": "Photograph address", "info": "Used when no photograph is picked." },
""", """    { "type": "text", "id": "image_fallback", "label": "Photograph address", "info": "Used when no photograph is picked." },
""" + _PHONE_SCHEMA),
])
# a collection's opening on a phone: its wide photograph at the width it is shown
_t = open(THEME + '/sections/ms-collection-hero.liquid', encoding='utf-8').read()
_u = re.sub(r"(\{% render 'ms-srcset', [^%]*?width: (?:2400|1920), )sizes: '100vw' %\}", r"\1sizes: '(max-width: 760px) 150vh, 100vw' %}", _t)
if _u != _t:
    open(THEME + '/sections/ms-collection-hero.liquid', 'w', encoding='utf-8').write(_u)
    _r28_n += 1
assert not re.search(r"width: (?:2400|1920), sizes: '100vw'", _u), 'collection hero sizes'
# the upright photographs where the openings have them
for _name, _sec, _f in (('index.json', None, 'ms-photo-drapes-fireplace-m.jpg'),
                        ('page.loro-piana-interiors.json', 's01', 'ms-photo-lp-paisley-room-m.jpg'),
                        ('collection.ms-loro.json', 's01', 'ms-photo-lp-paisley-room-m.jpg'),
                        ('page.sleep-culture.json', None, 'ms-graded-horse-m.jpg'),
                        ('collection.ms-sleep-culture.json', None, 'ms-graded-horse-m.jpg')):
    _h, _d = tpl_load(_name)
    _src = _f.replace('-m.jpg', '.jpg')
    _hit = 0
    for _k, _s in _d.get('sections', {}).items():
        if (_sec and _k != _sec) or _s.get('type') not in ('ms-banner', 'ms-hp-chapter'):
            continue
        _st = _s.get('settings', {})
        if _st.get('image_fallback') == _src and (_s['type'] == 'ms-banner' or _st.get('layout') == 'full'):
            _hit += 1
            if _st.get('image_fallback_mobile') != _f:
                _st['image_fallback_mobile'] = _f
                tpl_save(_name, _h, _d)
                _r28_n += 1
    assert _hit == 1, (_name, _hit)

# ── Loro Piana, Dressed for both seasons, on a phone: one frame and the season chosen above it (or with
#    a swipe), the two cloths crossing over, instead of two stacked pictures that only changed height
_r28_sub(THEME + '/sections/ms-lp-seasons.liquid', [
    ("""  @media (max-width: 760px) {
    .ms-lps__head { grid-template-columns: minmax(0, 1fr); gap: 18px; }
    .ms-lps__faces { flex-direction: column; height: auto; }
    .ms-lps__face { flex: none; height: 230px; transition: height .8s cubic-bezier(.22, 1, .36, 1); }
    .ms-lps__face.is-on { height: 340px; }
    .ms-lps__note { opacity: 1; transform: none; }
  }""", """  /* Round 28: on a phone, one frame; the season chosen just above it, or with a swipe */
  @media (max-width: 760px) {
    .ms-lps__head { grid-template-columns: minmax(0, 1fr); gap: 18px; }
    .ms-lps__switch { display: flex; width: 100%; margin-top: 30px; padding: 0; border: 0; border-bottom: 1px solid rgba(23, 20, 15, .16); border-radius: 0; }
    .ms-lps__sb { flex: 1 1 0; justify-content: center; position: relative; padding: 14px 6px; border-radius: 0; }
    .ms-lps__sb.is-on { background: none; color: #17140F; }
    .ms-lps__sb::after { content: ''; position: absolute; left: 0; right: 0; bottom: -1px; height: 1px; background: #17140F; transform: scaleX(0); transition: transform .5s cubic-bezier(.22, 1, .36, 1); }
    .ms-lps__sb.is-on::after { transform: none; }
    .ms-lps__faces { display: grid; height: auto; margin-top: 16px; aspect-ratio: 4 / 5; touch-action: pan-y; }
    .ms-lps__face { grid-area: 1 / 1; flex: none; opacity: 0; visibility: hidden; transition: opacity .7s, visibility 0s .7s; }
    .ms-lps__face.is-on { z-index: 1; opacity: 1; visibility: visible; transition: opacity .7s; }
    .ms-lps__note { opacity: 1; transform: none; }
  }"""),
    ("""      root.querySelectorAll('[data-lps]').forEach(function (b) { b.addEventListener('click', function () { show(b.getAttribute('data-lps')); }); });
""", """      root.querySelectorAll('[data-lps]').forEach(function (b) { b.addEventListener('click', function () { show(b.getAttribute('data-lps')); }); });
      // a swipe across the frame turns to the other season
      var fc = root.querySelector('.ms-lps__faces'), sx = null, sy = 0;
      fc.addEventListener('touchstart', function (e) { sx = e.touches[0].clientX; sy = e.touches[0].clientY; }, { passive: true });
      fc.addEventListener('touchend', function (e) {
        var t = e.changedTouches[0], dx = sx === null ? 0 : t.clientX - sx;
        if (Math.abs(dx) > 40 && Math.abs(dx) > Math.abs(t.clientY - sy)) show(dx < 0 ? 'summer' : 'winter');
        sx = null;
      }, { passive: true });
"""),
])

# ── Beds with headboards, side by side, on a phone: one row to swipe along, still to one scale, instead
#    of two columns seven rows deep
_r28_sub(THEME + '/sections/ms-bed-lineup.liquid', [
    ("""  .ms-bl__cat .ms-bl__h { letter-spacing: .08em; text-transform: none; font-size: 11.5px; line-height: 1.5; }
</style>""", """  .ms-bl__cat .ms-bl__h { letter-spacing: .08em; text-transform: none; font-size: 11.5px; line-height: 1.5; }
  /* Round 28: on a phone, one row along which to swipe, the next bed showing at the edge */
  @media (max-width: 760px) {
    .ms-bl { padding-left: 0; padding-right: 0; }
    .ms-bl__head { padding: 0 18px; }
    .ms-bl__row { grid-template-columns: none; grid-auto-flow: column; grid-auto-columns: 40vw; gap: 0 14px; overflow-x: auto; overscroll-behavior-x: contain; scroll-snap-type: x proximity; scroll-padding-inline: 18px; padding: 0 18px 12px; scrollbar-width: none; -webkit-overflow-scrolling: touch; }
    .ms-bl__row::-webkit-scrollbar { display: none; }
    .ms-bl__bed, .ms-bl__cat { scroll-snap-align: start; }
    .ms-bl__name { font-size: 16px; }
  }
</style>"""),
])

# ── Icons opens on two of the house's campaign photographs side by side, Top in the gallery of the Paris
#    Opera and Flora at a palace's ironwork windows (scripts/icons_photo_r28.py); on a phone, Top alone,
#    upright. The title back at the left. The abbey photograph leaves the theme.
_r28_sub(THEME + '/sections/ms-collection-hero.liquid', [
    ("  assign tier_side = 'left'\n  case tier\n", "  assign tier_side = 'left'\n  assign tier_m = ''\n  case tier\n"),
    ("""    when 'icons', 'icon'
      assign tier_name = 'ms-photo-icons-abbey.jpg'
      assign tier_photo = tier_name | asset_url
      assign tier_pos = '24% 84%'
      assign tier_side = 'right'
""", """    when 'icons', 'icon'
      assign tier_name = 'ms-photo-icons-pair.jpg'
      assign tier_photo = tier_name | asset_url
      assign tier_pos = 'center'
      assign tier_m = 'ms-photo-icons-pair-m.jpg'
"""),
    ("""<img alt="{%- render 'ms-coll-name', c: collection -%}" width="1920" height="1280" src="{{ tier_photo }}" {% render 'ms-srcset', fallback: tier_name, width: 1920, sizes: '(max-width: 760px) 150vh, 100vw' %} style="width: 100%; height: min(66vh, 640px); object-fit: cover; object-position: {{ tier_pos }}; display: block;" fetchpriority="high">""",
     """<picture style="display: block;">{%- if tier_m != '' -%}<source media="(max-width: 760px)" {% render 'ms-srcset', fallback: tier_m, width: 1000, sizes: '100vw' %}>{%- endif -%}<img alt="{%- render 'ms-coll-name', c: collection -%}" width="1920" height="1280" src="{{ tier_photo }}" {% render 'ms-srcset', fallback: tier_name, width: 2400, sizes: '(max-width: 760px) 150vh, 100vw' %} style="width: 100%; height: min(66vh, 640px); object-fit: cover; object-position: {{ tier_pos }}; display: block;" fetchpriority="high"></picture>"""),
])
# the two beds stand low in their photographs: Icons' name at the top, over the ceilings, not over a bed
_r28_sub(THEME + '/sections/ms-collection-hero.liquid', [
    ("  assign tier_m = ''\n  case tier\n", "  assign tier_m = ''\n  assign tier_v = ''\n  case tier\n"),
    ("      assign tier_m = 'ms-photo-icons-pair-m.jpg'\n", "      assign tier_m = 'ms-photo-icons-pair-m.jpg'\n      assign tier_v = 'top'\n"),
    ("radial-gradient(ellipse 52% 62% at {% if tier_side == 'right' %}100%{% else %}0%{% endif %} 100%, rgba(10, 8, 6, 0.42), rgba(10, 8, 6, 0) 72%), linear-gradient(180deg, rgba(10, 8, 6, 0.34) 0%, rgba(10, 8, 6, 0) 24%,",
     "radial-gradient(ellipse 52% 62% at {% if tier_side == 'right' %}100%{% else %}0%{% endif %} {% if tier_v == 'top' %}0%{% else %}100%{% endif %}, rgba(10, 8, 6, 0.42), rgba(10, 8, 6, 0) 72%), linear-gradient(180deg, rgba(10, 8, 6, {% if tier_v == 'top' %}0.46{% else %}0.34{% endif %}) 0%, rgba(10, 8, 6, 0) {% if tier_v == 'top' %}40%{% else %}24%{% endif %},"),
    ("display: flex; flex-direction: column; justify-content: flex-end; padding: clamp(26px, 5vw, 88px); color: rgb(251, 249, 245);{% if tier_side",
     "display: flex; flex-direction: column; justify-content: {% if tier_v == 'top' %}flex-start{% else %}flex-end{% endif %}; padding: clamp(26px, 5vw, 88px); color: rgb(251, 249, 245);{% if tier_side"),
])
for _t in glob.glob(THEME + '/*/*'):
    if os.path.isfile(_t) and 'ms-photo-icons-abbey' in open(_t, encoding='utf-8', errors='ignore').read() and not _t.endswith('ms-photo-icons-abbey.jpg'):
        raise AssertionError(('abbey', _t))
if os.path.exists(THEME + '/assets/ms-photo-icons-abbey.jpg'):
    os.remove(THEME + '/assets/ms-photo-icons-abbey.jpg')
    _r28_n += 1

# ── the phone menu, refined (bin/r28/menu.js, menu.css): the page behind inert, focus in and back, the
#    back gesture and a swipe to the right a level up or closed, the current page marked, the safe
#    areas of the screen kept, the next pages fetched ahead
for _f, _m in (('ms-site.js', 'menu.js'), ('ms-site.css', 'menu.css')):
    _p = THEME + '/assets/' + _f
    _t = open(_p, encoding='utf-8').read()
    _add = open(SP + '/bin/r28/' + _m, encoding='utf-8').read()
    if 'Round 28: the phone menu, refined' not in _t:
        open(_p, 'w', encoding='utf-8').write(_t.rstrip('\n') + '\n' + _add)
        _r28_n += 1
    else:
        assert _add.strip() in _t, ('menu', _f)

print('round 28: %d files changed' % _r28_n)
