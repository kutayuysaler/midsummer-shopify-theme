# Round 24, run at the end of bin/build_more.py in its scope (THEME, tpl_load, tpl_save ...), after
# Round 22. Every step is an exact replacement or a guarded write, so a second build changes nothing.
#  · Hotels and contract: no regeneration offered (the owner's instruction). The 15 + 15 service stays
#    for private homes only; nothing on the hotel pages promises it or a thirty-year life.
#  · Photographs that sit too bright among the others (the Thin Topper's), softened wherever they appear.
#  (The elevation drawing's boxspring, now as wide as the mattress, is in bin/extra/ms-spec.liquid.)

_r24_n = 0


def _r24_sub(path, pairs):
    global _r24_n
    _t = open(path, encoding='utf-8').read()
    _u = _t
    for _a, _b in pairs:
        if _a in _u:
            _u = _u.replace(_a, _b)
        else:
            assert _b in _u, (path, _a[:80])
    if _u != _t:
        open(path, 'w', encoding='utf-8').write(_u)
        _r24_n += 1


def _r24_write(path, text):
    global _r24_n
    if not os.path.exists(path) or open(path, encoding='utf-8').read() != text:
        open(path, 'w', encoding='utf-8').write(text)
        _r24_n += 1


# ── hotels: the section defaults the Hotels & Residences page shows
_r24_sub(THEME + '/sections/ms-hosp-01.liquid', [
    ('Handmade beds for hotels, residences and yachts: specified to the room, delivered in phases, with regeneration written into the contract.',
     'Handmade beds for hotels, residences and yachts: specified to the room, delivered in phases, installed by our own team.')])
_r24_sub(THEME + '/sections/ms-hosp-02.liquid', [
    ('specified for contract life, delivered in phases, and regenerated rather than replaced.',
     'specified for contract life and delivered in phases, room by room.')])
_r24_sub(THEME + '/sections/ms-hosp-03.liquid', [
    ('"label": "Regeneration in contract",\n      "default": "Regeneration in contract"',
     '"label": "Installation",\n      "default": "Installation"'),
    ('"label": "The 15 + 15 service written into t…",\n      "default": "The 15 + 15 service written into the agreement: refurbishment cycles without replacement capex."',
     '"label": "White-glove delivery by our own…",\n      "default": "White-glove delivery by our own team, floor by floor: each bed brought into the room, assembled and dressed."'),
])

# ── hotels: the page itself (both the page and the collection-view template)
_R24_CARD = {'place': 'loro', 'title': 'Loro Piana Interiors', 'text': 'The full palette for every room, and your own cloth on request.',
             'image_fallback': 'ms-photo-lp-paisley-side.jpg'}
_R24_QA = {'q': 'How are the beds delivered and installed?',
           'a': '<p>By our own team, in phases aligned to your floor handovers: each bed is brought into the room, assembled and dressed.</p>'}
for _name in ('page.hospitality.json', 'collection.ms-hospitality.json'):
    if not os.path.exists(THEME + '/templates/' + _name):
        continue
    _head, _d = tpl_load(_name)
    _before = json.dumps(_d, sort_keys=True)
    _secs = _d['sections']
    if 'years' in _secs:  # "Thirty years, per room": the regeneration band
        del _secs['years']
        _d['order'] = [k for k in _d['order'] if k != 'years']
    _pl = _secs.get('places')
    if _pl:
        _pl['settings']['heading'] = 'A bed your guests remember.'
        for _b in _pl.get('blocks', {}).values():
            if _b['settings'].get('place') == 'regen':
                _b['settings'] = dict(_R24_CARD)
    _qa = _secs.get('qa')
    if _qa:
        for _b in _qa.get('blocks', {}).values():
            if _b['settings'].get('q') == 'What happens at fifteen years?':
                _b['settings'] = dict(_R24_QA)
    if json.dumps(_d, sort_keys=True) != _before:
        tpl_save(_name, _head, _d)
        _r24_n += 1

# ── the questions page: hotels are supplied without the 15 + 15 service
_R24_Q26 = ('<p>Yes. We supply hotels, branded residences and yachts with phased production aligned to floor handovers, fire-retardancy and contract certification prepared per market, housekeeping protocols per system, and the 15 + 15 service written into the agreement.</p>',
            '<p>Yes. We supply hotels, branded residences and yachts with phased production aligned to floor handovers, fire-retardancy and contract certification prepared per market, and housekeeping protocols per system.</p>')
for _name in ('page.faq.json', 'collection.ms-faq.json'):
    _p = THEME + '/templates/' + _name
    if os.path.exists(_p):
        _t = open(_p, encoding='utf-8').read()
        if _R24_Q26[0] in _t:
            open(_p, 'w', encoding='utf-8').write(_t.replace(_R24_Q26[0], _R24_Q26[1]))
            _r24_n += 1

# ── professionals: the 15 + 15 card speaks of private homes, not of projects
for _name in ('page.professionals.json', 'collection.ms-professionals.json'):
    if not os.path.exists(THEME + '/templates/' + _name):
        continue
    _head, _d = tpl_load(_name)
    _ch = False
    for _b in (_d['sections'].get('places') or {}).get('blocks', {}).values():
        if _b['settings'].get('text') == 'Regeneration at fifteen years, for the life of the project.':
            _b['settings']['text'] = 'For private homes: fifteen years, then fifteen more.'
            _ch = True
    if _ch:
        tpl_save(_name, _head, _d)
        _r24_n += 1

# ── a photograph that sits too bright among the others (the Thin Topper's main photograph): softened
#    wherever it appears, found by its own file. Theme settings → Midsummer · Photographs.
_ss_p = THEME + '/config/settings_schema.json'
_ss = json.load(open(_ss_p, encoding='utf-8'))
for _g in _ss:
    if _g.get('name') == 'Midsummer · Photographs' and not any(x.get('id') == 'ms_photo_soften' for x in _g['settings']):
        _g['settings'] += [
            {"type": "text", "id": "ms_photo_soften", "label": "Soften these products' main photographs",
             "info": "Product handles, separated by commas. For a main photograph that looks too bright beside the others.", "default": "topper-basso"},
            {"type": "range", "id": "ms_photo_soften_strength", "label": "Softening", "min": 0, "max": 30, "step": 2, "unit": "%", "default": 12}]
        open(_ss_p, 'w', encoding='utf-8').write(json.dumps(_ss, indent=2, ensure_ascii=False) + '\n')
        _r24_n += 1
_r24_write(THEME + '/snippets/ms-photo-soften.liquid', '''{%- comment -%}
  A product's main photograph that looks too bright beside the others is toned down a little wherever it
  appears (the gallery, the collection cards, the menus), found by its own file. Theme settings →
  Midsummer · Photographs. Photographs laid into the paper (white studio grounds, ms-on-white) are left
  as they are. Generated by bin/build_r24.py.
{%- endcomment -%}
{%- if settings.ms_photo_soften != blank -%}
  {%- liquid
    assign k = settings.ms_photo_tone_strength | default: 40 | divided_by: 100.0
    assign sep = k | times: 0.16 | round: 3
    assign sat = k | times: 0.14 | round: 3
    assign sat = 1 | minus: sat
    assign con = k | times: 0.04 | round: 3
    assign con = 1 | minus: con
    assign bri = k | times: 0.02 | plus: 1
    unless settings.ms_photo_tone
      assign sep = 0
      assign sat = 1
      assign con = 1
      assign bri = 1
    endunless
    assign soft = settings.ms_photo_soften_strength | default: 12 | divided_by: 100.0
    assign keep = 1 | minus: soft
    assign bri = bri | times: keep | round: 3
    assign sat = sat | times: 0.96 | round: 3
    assign sel = ''
    assign handles = settings.ms_photo_soften | split: ','
    for h in handles
      assign hh = h | strip
      assign p = all_products[hh]
      if p.featured_image
        assign f = p.featured_image.src | split: '?' | first | split: '/' | last | split: '.' | first | remove: '"'
        if f.size > 5
          assign sel = sel | append: 'body img[src*="' | append: f | append: '"]:not(.ms-on-white),'
        endif
      endif
    endfor
  -%}
  {%- if sel != '' -%}
  <style>{{ sel }} body img.ms-photo-soften { filter: sepia({{ sep }}) saturate({{ sat }}) contrast({{ con }}) brightness({{ bri }}) !important; }</style>
  {%- endif -%}
{%- endif -%}
''')
for _lay in (THEME + '/layout/ms.liquid', THEME + '/layout/theme.liquid'):
    _t = open(_lay, encoding='utf-8').read()
    if "render 'ms-photo-soften'" not in _t:
        assert "{%- render 'ms-on-white' -%}" in _t, _lay
        open(_lay, 'w', encoding='utf-8').write(_t.replace("{%- render 'ms-on-white' -%}", "{%- render 'ms-on-white' -%}\n    {%- render 'ms-photo-soften' -%}", 1))
        _r24_n += 1

# ── the product gallery's name for screen readers, in the page's language
_r24_sub(THEME + '/sections/ms-product-main.liquid', [
    ('aria-label="{{ product.title | escape }}: photographs"',
     'aria-label="{{ product.title | escape }}: {% render \'ms-t\', v: \'photographs\' %}"')])

# ── handles the store has translated (Translate & Adapt: about, agents, regeneration … and two
#    collections). In Italian or Russian a page or collection may answer to its translated handle, so
#    wherever the theme recognises a place by its handle, the translated handles are recognised too.
_R24_PAGES = {'story': 'chi-siamo-midsummer-milano,o-nas-midsummer-milano',
              'handmade': 'artigiani-italiani-materassi-lusso,italyanskie-mastera-luksovye-matrasy',
              'regen': 'rigenerazione-materasso,regeneratsiya-matrasa',
              'ergonomics': 'materassi-ergonomici,ergonomichnye-matrasy',
              'agents': 'agenti-e-rivenditori,dilery-i-partnery',
              'terms': 'termini-e-condizioni,usloviya',
              'privacy': 'privacy-e-note-legali,konfidentsialnost'}
_ml = open(THEME + '/snippets/ms-link.liquid', encoding='utf-8').read()
_pairs = []
for _k, _al in _R24_PAGES.items():
    _m = re.search(r"\n    when '" + _k + r"'(?:, '[a-z-]+')*\n(?:      assign tpl = '[^']*'\n)?      assign p = '([^']*)'", _ml)
    assert _m, _k
    _pairs.append(("assign p = '%s'" % _m.group(1), "assign p = '%s,%s'" % (_m.group(1), _al)))
_pairs += [("assign c = 'beds-with-headboards,gallery-beds,headboards'", "assign c = 'beds-with-headboards,gallery-beds,headboards,letti-con-testiera,krovati-s-izgolovem'"),
           ("assign c = 'designer-beds,bed-systems,sleep-systems'", "assign c = 'designer-beds,bed-systems,sleep-systems,letti-di-design,dizajnerskie-krovati'")]
_r24_sub(THEME + '/snippets/ms-link.liquid', _pairs)
_r24_sub(THEME + '/sections/ms-collection-intro.liquid', [
    ("    when 'essentials', 'signature', 'icons', 'icon', 'designer-beds'\n",
     "    when 'essentials', 'signature', 'icons', 'icon', 'designer-beds', 'letti-di-design', 'dizajnerskie-krovati'\n"),
    ("    when 'beds-with-headboards'\n", "    when 'beds-with-headboards', 'letti-con-testiera', 'krovati-s-izgolovem'\n")])
_r24_sub(THEME + '/snippets/ms-kind.liquid', [
    ("      if c.handle == 'beds-with-headboards'\n",
     "      if c.handle == 'beds-with-headboards' or c.handle == 'letti-con-testiera' or c.handle == 'krovati-s-izgolovem'\n")])

print('round 24: %d files changed' % _r24_n)
