# Round 29, run at the end of bin/build_more.py in its scope (THEME, SP), after Round 28. Every step is
# an exact replacement or a guarded write, so a second build changes nothing.
#  · A language switcher, not in the way: in the header the code of the language in use (EN), which
#    opens English, Italiano, Русский; in the phone menu and the footer the three side by side.
#    Shopify's own localization form (snippets/ms-lang.liquid).

_r29_n = 0


def _r29_sub(path, pairs):
    """an exact replacement; one that holds what it replaces is made once"""
    global _r29_n
    _t = open(path, encoding='utf-8').read()
    _u = _t
    for _a, _b in pairs:
        if _a in _b and _b in _u:
            continue
        if _a in _u:
            _u = _u.replace(_a, _b)
        else:
            assert _b in _u, (path, _a[:80])
    if _u != _t:
        open(path, 'w', encoding='utf-8').write(_u)
        _r29_n += 1


_src = SP + '/bin/r29/ms-lang.liquid'
_dst = THEME + '/snippets/ms-lang.liquid'
if not os.path.exists(_dst) or open(_src, 'rb').read() != open(_dst, 'rb').read():
    shutil.copy(_src, _dst)
    _r29_n += 1

# the header: before the appointment button, after Showrooms and Enquiries
_r29_sub(THEME + '/sections/ms-header.liquid', [
    ("""<a data-ms-enquire="" href="{% render 'ms-link', to: 'contact' %}" style="display: inline-flex; align-items: center; min-height: 42px; padding: 0px 18px; border: 1px solid currentcolor;""",
     """{% render 'ms-lang', place: 'head' %}<a data-ms-enquire="" href="{% render 'ms-link', to: 'contact' %}" style="display: inline-flex; align-items: center; min-height: 42px; padding: 0px 18px; border: 1px solid currentcolor;"""),
    # the phone menu: under its small links, at the end of the first level
    ('</div><div data-ms-msub="beds" hidden="">', """{% render 'ms-lang', place: 'menu' %}</div><div data-ms-msub="beds" hidden="">"""),
])
# the footer: in its last line, between the company and the legal links
_r29_sub(THEME + '/sections/ms-footer.liquid', [
    ("<span>{{ section.settings.t25 }}</span>",
     "<span>{{ section.settings.t25 }}</span>{% render 'ms-lang', place: 'foot' %}"),
    # the word "English" the preview wrote at the end of the legal links, never a choice: the switcher says it now
    ('<span>{{ section.settings.t29 }}</span>', ''),
])
_p = THEME + '/assets/ms-site.css'
_t = open(_p, encoding='utf-8').read()
_add = open(SP + '/bin/r29/lang.css', encoding='utf-8').read()
# the block is the stylesheet's last: written once, or brought up to date where an earlier one stands
_i = _t.find('/* Round 29: the languages, quietly')
_u = (_t if _i < 0 else _t[:_i]).rstrip('\n') + '\n' + _add
if _u != _t:
    open(_p, 'w', encoding='utf-8').write(_u)
    _r29_n += 1
for _f, _n in (('sections/ms-header.liquid', 2), ('sections/ms-footer.liquid', 1)):
    assert open(THEME + '/' + _f, encoding='utf-8').read().count("{% render 'ms-lang'") == _n, _f
assert 'section.settings.t29 }}' not in open(THEME + '/sections/ms-footer.liquid', encoding='utf-8').read(), 'footer English'

# ── Icons on one photograph: Top in the gallery of the Paris Opera at the right, the collection's name
#    beside it on the dark ground, at its foot like the other collections' (scripts/icons_photo_r29.py).
#    On a phone, the photograph upright, the name at its foot as on Essentials and Signature (it was at the
#    top, over the ceiling, until the house asked for it at the foot). The two side by side are gone.
_HERO = THEME + '/sections/ms-collection-hero.liquid'
_h = open(_HERO, encoding='utf-8').read()
_h2 = _h.replace("      assign tier_m = 'ms-photo-icons-opera-m.jpg'\n      assign tier_v = 'top'\n", "      assign tier_m = 'ms-photo-icons-opera-m.jpg'\n      assign tier_v = ''\n")
if _h2 != _h:
    open(_HERO, 'w', encoding='utf-8').write(_h2)
    _r29_n += 1
_r29_sub(_HERO, [
    ("  assign tier_v = ''\n  case tier\n", "  assign tier_v = ''\n  assign tier_plate = false\n  assign tier_sizes = '(max-width: 760px) 150vh, 100vw'\n  case tier\n"),
    ("""      assign tier_name = 'ms-photo-icons-pair.jpg'
      assign tier_photo = tier_name | asset_url
      assign tier_pos = 'center'
      assign tier_m = 'ms-photo-icons-pair-m.jpg'
      assign tier_v = 'top'
""", """      assign tier_name = 'ms-photo-icons-opera.jpg'
      assign tier_photo = tier_name | asset_url
      assign tier_pos = 'center 80%'
      assign tier_m = 'ms-photo-icons-opera-m.jpg'
      assign tier_v = ''
      assign tier_plate = true
      assign tier_sizes = '(max-width: 760px) 100vw, 46vw'
"""),
    ('<section class="ms-colhero" style="position: relative;', '<section class="ms-colhero{% if tier_plate %} ms-colhero--plate{% endif %}" style="position: relative;'),
    ("{% render 'ms-srcset', fallback: tier_name, width: 2400, sizes: '(max-width: 760px) 150vh, 100vw' %}", "{% render 'ms-srcset', fallback: tier_name, width: 2400, sizes: tier_sizes %}"),
    ('<div style="position: absolute; inset: 0px; background: radial-gradient(', '<div class="ms-colhero__veil" style="position: absolute; inset: 0px; background: radial-gradient('),
    ('<div style="position: absolute; inset: 0px; display: flex; flex-direction: column; justify-content:', '<div class="ms-colhero__copy" style="position: absolute; inset: 0px; display: flex; flex-direction: column; justify-content:'),
    (""".ms-colhero [style*="letter-spacing: 0.3em"] { opacity: 1 !important; }</style>""",
     """.ms-colhero [style*="letter-spacing: 0.3em"] { opacity: 1 !important; } @media (min-width: 761px) { .ms-colhero--plate picture img { width: 46% !important; margin-left: auto; } .ms-colhero--plate .ms-colhero__veil { left: auto !important; width: 46%; background: linear-gradient(180deg, rgba(10, 8, 6, .4), rgba(10, 8, 6, 0) 28%) !important; } .ms-colhero--plate .ms-colhero__copy { right: 46% !important; justify-content: flex-end !important; } }</style>"""),
    # the header's words stay clear over the chandeliers
    ("background: linear-gradient(180deg, rgba(10, 8, 6, .4), rgba(10, 8, 6, 0) 28%) !important;", "background: linear-gradient(180deg, rgba(10, 8, 6, .64), rgba(10, 8, 6, .2) 20%, rgba(10, 8, 6, 0) 34%) !important;"),
])
_u = open(_HERO, encoding='utf-8').read()
assert 'icons-pair' not in _u and _u.count('ms-colhero--plate') >= 4, 'icons plate'
for _f in ('ms-photo-icons-pair.jpg', 'ms-photo-icons-pair-m.jpg'):
    if os.path.exists(THEME + '/assets/' + _f):
        os.remove(THEME + '/assets/' + _f)
        _r29_n += 1

# ── one way to enquire on each screen: on a wide one the appointment button in the header (its
#    Enquiries link is off unless named, bin/build_chrome.py); on a phone, where the header has no
#    buttons, the small Enquire in the corner
_SS = THEME + '/config/settings_schema.json'
_t = open(_SS, encoding='utf-8').read()
_ss = json.loads(_t)
for _grp in _ss:
    for _x in _grp.get('settings', []):
        if _x.get('id') == 'ms_enquiry_bubble':
            _x['label'] = 'Show the enquiry button on phones'
            _x['info'] = 'A small button in the corner of a phone that opens the enquiry form, once the visitor has scrolled.'
_u = json.dumps(_ss, indent=2, ensure_ascii=False) + '\n'
if _u != _t:
    open(_SS, 'w', encoding='utf-8').write(_u)
    _r29_n += 1

# ── the enquiry sheet on a phone: it rose all at once (its animation was switched off there, and with it
#    the drag that should move it). Now it rises softly, and closes by going back down; see lang.css too
_r29_sub(THEME + '/assets/ms-site.css', [
    ("    animation: none !important; transform: none !important;\n",
     "    animation: msSheetUp .5s cubic-bezier(.32, .72, 0, 1) backwards !important;\n"),
])
_r29_sub(THEME + '/assets/ms-site.js', [
    ("""  function openDrawer(source) {
    if (!drawer) return false;
""", """  var closing = null;
  function openDrawer(source) {
    if (!drawer) return false;
    if (closing) { closing.forEach(function (a) { try { a.cancel(); } catch (err) {} }); closing = null; }
"""),
    ("""  function closeDrawer() {
    if (!drawer || drawer.hidden) return;
    drawer.hidden = true;
    body.classList.remove('ms-lock');
    if (lastFocus && lastFocus.focus) lastFocus.focus({ preventScroll: true });
  }""", """  function closeDrawer() {
    if (!drawer || drawer.hidden || closing) return;
    var sheet = drawer.querySelector('[data-ms="sheet"]'), veil = drawer.querySelector('[data-ms-drawer] > [data-ms-drawer-close]');
    closing = [];
    function done() {
      if (!closing) return;
      closing.forEach(function (a) { try { a.cancel(); } catch (err) {} });
      closing = null;
      drawer.hidden = true;
      if (sheet) { sheet.style.transform = ''; sheet.style.transition = ''; }
      if (veil) veil.style.opacity = '';
      body.classList.remove('ms-lock');
      if (lastFocus && lastFocus.focus) lastFocus.focus({ preventScroll: true });
    }
    // Round 29: the sheet goes back the way it came, from wherever a finger left it, the room brightening
    if (reduce || !sheet || !sheet.animate) { done(); return; }
    var phone = window.matchMedia('(max-width: 760px)').matches, from = getComputedStyle(sheet).transform;
    var a = sheet.animate([{ transform: from && from !== 'none' ? from : 'translate3d(0, 0, 0)' }, { transform: phone ? 'translate3d(0, 100%, 0)' : 'translate3d(100%, 0, 0)' }],
      { duration: phone ? 340 : 400, easing: 'cubic-bezier(.32, 0, .67, 0)', fill: 'forwards' });
    closing.push(a);
    if (veil) closing.push(veil.animate([{ opacity: getComputedStyle(veil).opacity }, { opacity: 0 }], { duration: phone ? 340 : 400, easing: 'ease-in', fill: 'forwards' }));
    a.onfinish = done;
    setTimeout(done, 700);
  }"""),
    ("""    var y0 = e.clientY;
    function move(ev) { var dy = Math.max(0, ev.clientY - y0); sheet.style.transform = 'translateY(' + dy + 'px)'; sheet.style.transition = 'none'; }
    function up(ev) {
      window.removeEventListener('pointermove', move); window.removeEventListener('pointerup', up);
      var dy = Math.max(0, ev.clientY - y0);
      if (dy > 110) { closeDrawer(); return; }
      sheet.style.transition = 'transform .28s cubic-bezier(.22,1,.36,1)';
      sheet.style.transform = 'translateY(0)';
    }""", """    var y0 = e.clientY, t0 = Date.now(), veil = sheet.parentNode.querySelector(':scope > [data-ms-drawer-close]');
    function move(ev) { var dy = Math.max(0, ev.clientY - y0); sheet.style.transform = 'translateY(' + dy + 'px)'; sheet.style.transition = 'none'; if (veil) veil.style.opacity = String(Math.max(.25, 1 - dy / 520)); }
    function up(ev) {
      window.removeEventListener('pointermove', move); window.removeEventListener('pointerup', up);
      var dy = Math.max(0, ev.clientY - y0);
      // far enough, or a quick flick: it goes; otherwise it settles back
      if (dy > 110 || (dy > 36 && Date.now() - t0 < 260)) { closeDrawer(); return; }
      sheet.style.transition = 'transform .32s cubic-bezier(.22,1,.36,1)';
      sheet.style.transform = 'translateY(0)';
      if (veil) veil.style.opacity = '';
    }"""),
])

# ── the phone menu, calmer (the look is in lang.css). Its foot was fixed under the list: the appointment,
#    a line and the socials took a fifth of a phone, under the browser's own bar, and repeated the
#    Contact level's appointment there. They now follow the first level's list, the languages between
#    them; the deeper levels end with their own links
_H = THEME + '/sections/ms-header.liquid'
_h = open(_H, encoding='utf-8').read()
_FOOT = '<div style="flex: 0 0 auto; padding: 14px 18px 16px; border-top: 1px solid rgb(221, 214, 201); background: rgb(251, 249, 245);">'
_SOC = """<div style="margin-top: 18px; display: flex; justify-content: center;">{% render 'ms-social' %}</div>\n</div>"""
_LANG = """{% render 'ms-lang', place: 'menu' %}</div><div data-ms-msub="beds" hidden="">"""
if _FOOT in _h:
    _i = _h.index(_FOOT)
    _j = _h.index(_SOC, _i)
    _cta = _h[_i + len(_FOOT):_j].strip('\n')
    assert _h.count(_LANG) == 1 and 'data-ms-landing' in _cta, 'menu foot'
    _h = _h[:_i] + _h[_j + len(_SOC):]
    _h = _h.replace(_LANG, '<div class="ms-mcta">' + _cta + "</div>{% render 'ms-lang', place: 'menu' %}"
                    + """<div class="ms-msoc">{% render 'ms-social' %}</div></div><div data-ms-msub="beds" hidden="">""")
else:
    assert 'class="ms-mcta"' in _h and 'class="ms-msoc"' in _h, 'menu foot'
# the menu's small photographs ask for a small picture, not one for six tenths of the screen
_h, _k = re.subn(r"""(<img width="(?:88|64)" height="(?:110|80)"[^>]*?sizes: ')\(max-width: 760px\) 60vw, 24vw'""", r"\g<1>64px'", _h)
assert _k >= 1 or "sizes: '64px'" in _h, 'menu thumbs'
if _h != open(_H, encoding='utf-8').read():
    open(_H, 'w', encoding='utf-8').write(_h)
    _r29_n += 1
# the menu's photographs fetched as it opens, and the hairline under its head: a block of its own after
# Round 28's (bin/r29/menu.js), written once, or brought up to date where an earlier one stands
_p = THEME + '/assets/ms-site.js'
_t = open(_p, encoding='utf-8').read()
_add = open(SP + '/bin/r29/menu.js', encoding='utf-8').read()
_i = _t.find("/* Round 29: the phone menu's few photographs")
_u = (_t if _i < 0 else _t[:_i]).rstrip('\n') + '\n' + _add
if _u != _t:
    open(_p, 'w', encoding='utf-8').write(_u)
    _r29_n += 1

# ── Find your Midsummer: each question's own photograph. The img's srcset held the first photograph in
#    place whatever its src said, so the five questions showed one picture. Now each comes with its own
#    widths and fades in; an answer brings the next question into view. The phone layout is in lang.css
# the snippet is patched in place from build to build: an earlier copy of this block (one or more) goes
# first, so the one below is always the only one, word for word
_QZ = THEME + '/snippets/ms-quiz.liquid'
_q = open(_QZ, encoding='utf-8').read()
_q2 = re.sub(r"  // Round 29: (?:a question|the photograph of each question).*?(?=  function render\(\) \{\n)", '', _q, flags=re.S)
if _q2 != _q:
    open(_QZ, 'w', encoding='utf-8').write(_q2)
_r29_sub(THEME + '/snippets/ms-quiz.liquid', [
    ("""  function render() {
    var done = qi >= QUESTIONS.length;
""", """  // Round 29: the photograph of each question, at the widths it is shown, faded in (no apostrophes in
  // these comments: build_r23.py reads the strings of this script by its quotes)
  function widths(u) {
    return [540, 900, 1400].map(function (w) {
      return (/\\/assets\\//.test(u) ? u.replace(/(\\.(?:jpe?g|png))(\\?|$)/i, '_' + w + 'x$1$2') : u.replace(/([?&]width=)\\d+/, '$1' + w)) + ' ' + w + 'w';
    }).join(', ');
  }
  function photo(u) {
    var im = $('[data-ms-quiz-img]');
    if ((im.getAttribute('data-ms-now') || im.getAttribute("src")) === u) { im.setAttribute('data-ms-now', u); return; }
    im.setAttribute('data-ms-now', u);
    im.style.opacity = '0';
    im.onload = im.onerror = function () { im.style.opacity = ''; };
    im.srcset = widths(u);
    im.src = u;
  }
  // and the next question in view, from wherever the answer was tapped
  function toTop() {
    var dlg = root.closest('.ms-quizdlg'), r = root.getBoundingClientRect();
    if (dlg) { if (dlg.scrollTop > 0) dlg.scrollTo({ top: 0, behavior: "smooth" }); }
    else if (r.top < 0) window.scrollTo({ top: window.pageYOffset + r.top - 90, behavior: "smooth" });
  }
  function render() {
    var done = qi >= QUESTIONS.length;
"""),
    ("    $('[data-ms-quiz-img]').src = done ? DONE_IMG : QUESTIONS[qi].img;\n",
     "    photo(done ? DONE_IMG : QUESTIONS[qi].img);\n"),
    ("b.addEventListener('click', function () { answers = answers.slice(0, qi).concat([o[0]]); qi++; render(); });",
     "b.addEventListener('click', function () { answers = answers.slice(0, qi).concat([o[0]]); qi++; render(); toTop(); });"),
])

# the kinds of enquiry, on a phone a strip that scrolls sideways: the chosen one is brought fully into it
_r29_sub(THEME + '/assets/ms-site.js', [
    ("""  function setTab(form, t) {
    var copy = TABS[t];
""", """  // Round 29: on a phone the kinds of enquiry are a strip that scrolls sideways; the chosen one comes fully into it
  function keepInView(b) {
    var l = b.parentNode;
    if (!l || l.scrollWidth <= l.clientWidth + 1) return;
    var lr = l.getBoundingClientRect(), br = b.getBoundingClientRect();
    if (br.left >= lr.left + 4 && br.right <= lr.right - 4) return;
    l.scrollBy({ left: br.left - lr.left - (lr.width - br.width) / 2, behavior: reduce ? 'auto' : 'smooth' });
  }
  function setTab(form, t) {
    var copy = TABS[t];
"""),
    ("""      b.setAttribute('aria-pressed', on ? 'true' : 'false');
      var dot = b.querySelector('[data-ms-dot]');
""", """      b.setAttribute('aria-pressed', on ? 'true' : 'false');
      if (on) keepInView(b);
      var dot = b.querySelector('[data-ms-dot]');
"""),
])

# ── the Milano atelier without the blue-and-gold room (scripts/atelier_photos_r29.py; the opening, steps
#    and pair in bin/build_extra.py). In The rooms, the first and the sixth photographs give way to the
#    teal room and a wool blanket, the order kept; their proportions are read from the files
for _f in sorted(glob.glob(SP + '/vendor/r29/ms-photo-atelier-*.jpg')):
    _d = THEME + '/assets/' + os.path.basename(_f)
    if not os.path.exists(_d) or open(_f, 'rb').read() != open(_d, 'rb').read():
        shutil.copy(_f, _d)
        _r29_n += 1
_ROOMS29 = {'ms-photo-atelier-blue-gold-made.jpg': ('ms-photo-atelier-teal-room.jpg', 'The teal room, the bed made up.'),
            'ms-photo-atelier-edge.jpg': ('ms-photo-atelier-blanket.jpg', 'A wool blanket at the foot of the bed.')}
_ORDER29 = ['ms-photo-atelier-teal-room.jpg', 'ms-photo-atelier-leopard.jpg', 'ms-photo-atelier-teal.jpg', 'ms-photo-atelier-parrot-room.jpg',
            'ms-photo-atelier-lacquer.jpg', 'ms-photo-atelier-blanket.jpg', 'ms-photo-atelier-red-wall.jpg', 'ms-photo-atelier-linen.jpg']
for _name in ('page.atelier.json', 'collection.ms-atelier.json'):
    if not os.path.exists(THEME + '/templates/' + _name):
        continue
    _h, _d = tpl_load(_name)
    _sec = _d['sections']['rooms']
    _ch = False
    for _b in _sec['blocks'].values():
        _st = _b['settings']
        if _st.get('image_fallback') in _ROOMS29:
            _st['image_fallback'], _st['caption'] = _ROOMS29[_st['image_fallback']]
            _ch = True
        _r = _r26_ratio(_st.get('image_fallback', ''))
        if _r and _st.get('ratio') != _r:
            _st['ratio'], _ch = _r, True
    _by = {_b['settings'].get('image_fallback'): _bid for _bid, _b in _sec['blocks'].items()}
    _order = [_by[_f] for _f in _ORDER29 if _f in _by] + [_b for _b in _sec['block_order'] if _b not in [_by.get(_f) for _f in _ORDER29]]
    if _order != _sec['block_order']:
        _sec['block_order'], _ch = _order, True
    if _ch:
        tpl_save(_name, _h, _d)
        _r29_n += 1
    assert not re.search(r'blue-gold|orange-bed|atelier-sun|atelier-pure|atelier-edge', json.dumps(_d)), ('atelier photos', _name)
# the two that only the atelier's rooms showed leave the theme
for _f in _ROOMS29:
    _p = THEME + '/assets/' + _f
    if os.path.exists(_p) and not any(_f in open(_x, encoding='utf-8', errors='ignore').read() for _x in glob.glob(THEME + '/*/*.liquid') + glob.glob(THEME + '/templates/*.json')):
        os.remove(_p)
        _r29_n += 1

# the VK mark (Russian site) was a solid block among outline marks, plain to see once the menu's socials
# lost their circles: its letters now sit in a rounded square drawn like Instagram's and LinkedIn's
_S = THEME + '/snippets/ms-social.liquid'
_s = open(_S, encoding='utf-8').read()
_VK0 = '<path d="M15.684 0H8.316C1.592 0 0 1.592 0 8.316'
if _VK0 in _s:
    _i = _s.index(_VK0)
    _j = _s.index('/>', _i) + 2
    _d = _s[_i + 9:_j - 3]
    _k = _d.index('zm3.692 17.123')
    _s = (_s[:_i] + '<rect x="3.5" y="3.5" width="17" height="17" rx="5" fill="none" stroke="currentColor" stroke-width="1.35" stroke-linejoin="round"/>'
          + '<path transform="translate(12 12) scale(.62) translate(-12 -12.7)" d="M19.376 17.123' + _d[_k + 14:] + '"/>' + _s[_j:])
    open(_S, 'w', encoding='utf-8').write(_s)
    _r29_n += 1
else:
    assert 'translate(-12 -12.7)' in _s, 'vk mark'

# ── Top: the award's label lay over the topper (and its name) once the topper was opened and lifted, and
#    under the drawing it crowded the caption: Inside Top shows the bed alone. The award stays under the
#    product's name at the top of the page (.ms-pm__award)
_CR = THEME + '/sections/ms-craft.liquid'
_c = open(_CR, encoding='utf-8').read()
_t = _c
if 'class="ms-cr__award"' in _c:
    _i = _c.index('        {%- liquid\n          assign cr_award = false')
    _j = _c.index('        {%- endif -%}\n', _c.index('class="ms-cr__award"', _i)) + len('        {%- endif -%}\n')
    _c = _c[:_i] + _c[_j:]
_c = re.sub(r'(?m)^  (?:/\* Round 27: the Green Product Award[^\n]*\*/|\.ms-site a\.ms-cr__award[^\n]*|\.ms-cr__award-[^\n]*|\.ms-site \.ms-cr__award-[^\n]*|@media \(max-width: \d+px\) \{ \.ms-site a\.ms-cr__award[^\n]*)\n', '', _c)
if _c != _t:
    open(_CR, 'w', encoding='utf-8').write(_c)
    _r29_n += 1
assert 'ms-cr__award' not in _c and 'cr_award' not in _c, 'no award in Inside Top'

# ── the product's photographs whole and sharp: every one was cut to a tall 4:5 frame (and shorter still
#    under the screen's height), so a wide studio photograph lost its ends and a room's photograph its
#    floor, and both were enlarged past their resolution. The frame now takes the first photograph's own
#    proportions (between 3:4 and 3:2), sized to the screen; a photograph of other proportions is shown
#    whole within it. Fetched up to 2800 px wide for large, dense screens
_PM = THEME + '/sections/ms-product-main.liquid'
_r29_sub(_PM, [
    # (a first draft of this step set the proportions on the photograph's column, not beside its thumbnails)
    ('      {%- liquid\n        assign ms_ar = images.first.preview_image.aspect_ratio | default: images.first.aspect_ratio | default: 0.8\n'
     '        if ms_ar < 0.75\n          assign ms_ar = 0.75\n        elsif ms_ar > 1.5\n          assign ms_ar = 1.5\n        endif\n      -%}\n'
     '      <div class="ms-pm__main" style="--ms-ar: {{ ms_ar }}">\n', '      <div class="ms-pm__main">\n'),
    ('  .ms-pm__main { width: min(100%, calc(min(100vh - 190px, 980px) * var(--ms-ar, .8))); }\n', ''),
    ('    .ms-pm__main { width: 100%; }\n', ''),
    ('    <div class="ms-pm__gallery{% if n_images < 2 %} is-single{% endif %}" data-ms-pm-gallery aria-roledescription',
     '    {%- liquid\n'
     '      assign ms_ar = images.first.preview_image.aspect_ratio | default: images.first.aspect_ratio | default: 0.8\n'
     '      if ms_ar < 0.75\n'
     '        assign ms_ar = 0.75\n'
     '      elsif ms_ar > 1.5\n'
     '        assign ms_ar = 1.5\n'
     '      endif\n'
     '    -%}\n'
     '    <div class="ms-pm__gallery{% if n_images < 2 %} is-single{% endif %}" data-ms-pm-gallery style="--ms-ar: {{ ms_ar }}" aria-roledescription'),
    ('              <div class="ms-pm__slide{% if forloop.first %} is-on{% endif %}" data-ms-pm-slide="{{ forloop.index0 }}">\n',
     '              {%- assign m_ar = media.preview_image.aspect_ratio | default: media.aspect_ratio | default: ms_ar -%}\n'
     '              {%- assign m_off = m_ar | divided_by: ms_ar | minus: 1 | abs -%}\n'
     '              <div class="ms-pm__slide{% if forloop.first %} is-on{% endif %}{% if m_off > 0.06 %} is-fit{% endif %}" data-ms-pm-slide="{{ forloop.index0 }}">\n'),
    (" {{ media | image_url: width: 2200 }} 2200w\"", " {{ media | image_url: width: 2200 }} 2200w, {{ media | image_url: width: 2800 }} 2800w\""),
    # the frame as wide as the first photograph's proportions allow under the screen's height, beside its
    # thumbnails, the two centred in their column; the white of a studio photograph laid into the paper
    # (the slide's own ground: it inherited a transparent one, so the multiply of ms-on-white had nothing under it)
    ('  .ms-pm__gallery.is-single { grid-template-columns: minmax(0, 1fr); }',
     '  .ms-pm__gallery.is-single { grid-template-columns: minmax(0, 1fr); }\n'
     '  .ms-pm__gallery { --ms-fw: min(100%, calc(min(100vh - 190px, 980px) * var(--ms-ar, .8))); grid-template-columns: 68px min(calc(100% - 84px), calc(min(100vh - 190px, 980px) * var(--ms-ar, .8))); justify-content: center; }\n'
     '  .ms-pm__gallery.is-single { grid-template-columns: var(--ms-fw); }'),
    ('  .ms-pm__track { position: relative; width: 100%; aspect-ratio: 4 / 5; max-height: min(calc(100vh - 190px), 980px); outline: none; }',
     '  .ms-pm__track { position: relative; width: 100%; aspect-ratio: var(--ms-ar, 4 / 5); outline: none; }\n'
     '  .ms-pm__slide.is-fit img { object-fit: contain; }'),
    ('    .ms-pm__slide { position: relative; inset: auto; flex: 0 0 100%; opacity: 1; scroll-snap-align: start; scroll-snap-stop: always; aspect-ratio: 4 / 5; max-height: 78vh; }',
     '    .ms-pm__slide { position: relative; inset: auto; flex: 0 0 100%; opacity: 1; scroll-snap-align: start; scroll-snap-stop: always; aspect-ratio: var(--ms-ar, 4 / 5); max-height: 78vh; }'),
    # on a phone a photograph nearly of the frame's proportions fills it; one far from them is shown whole
    ('{% if m_off > 0.06 %} is-fit{% endif %}" data-ms-pm-slide', '{% if m_off > 0.06 %} is-fit{% endif %}{% if m_off > 0.15 %} is-far{% endif %}" data-ms-pm-slide'),
    ('    .ms-pm__slide { position: relative; inset: auto; flex: 0 0 100%; opacity: 1; scroll-snap-align: start; scroll-snap-stop: always; aspect-ratio: var(--ms-ar, 4 / 5); max-height: 78vh; }\n',
     '    .ms-pm__slide { position: relative; inset: auto; flex: 0 0 100%; opacity: 1; scroll-snap-align: start; scroll-snap-stop: always; aspect-ratio: var(--ms-ar, 4 / 5); max-height: 78vh; }\n'
     '    .ms-pm__slide.is-fit:not(.is-far) img { object-fit: cover; }\n'),
])
_r29_sub(THEME + '/snippets/ms-on-white.liquid', [('  .ms-pm__slide { background: inherit; }', '  .ms-pm__slide { background: #F1ECE3; }')])
_c = open(_PM, encoding='utf-8').read()
assert _c.count('--ms-ar: {{ ms_ar }}') == 1 and _c.count('assign ms_ar = 0.75') == 1 and _c.count(' is-fit{% endif %}{% if m_off > 0.15 %} is-far{% endif %}') == 1 and _c.count('.is-fit:not(.is-far)') == 1 and '2800w' in _c, 'product photographs whole'

print('round 29: %d files changed' % _r29_n)
