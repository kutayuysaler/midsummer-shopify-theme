# Round 25, run at the end of bin/build_more.py in its scope (THEME, tpl_load, tpl_save ...), after
# Round 24. Every step is an exact replacement or a guarded write, so a second build changes nothing.
#  · Photographs: the summer face of the seasons in a real linen, Roma at the atelier in two sharper
#    frames, Wish in its two photographed colours, the atelier's rooms and beds made up for the night.
#  · The press: every publication's mark, one still line at a time, turned by hand; the PNG marks
#    redrawn in one ink, the SVG marks trimmed to their ink.
#  · The collection photographs, graded in their files, no longer toned a second time.
#  · Natural materials: a photograph chosen in the editor is toned like the bundled plates.
#  · Hospitality: 15 + 15 is for private homes, not for hotel orders; yachts and private jets.
#  · Sleep Culture: a night, hour by hour, and rooms kept for rest. The atelier: its rooms.

_r25_n = 0


def _r25_sub(path, pairs):
    global _r25_n
    _t = open(path, encoding='utf-8').read()
    _u = _t
    for _a, _b in pairs:
        if _a in _u:
            _u = _u.replace(_a, _b)
        else:
            assert _b in _u, (path, _a[:80])
    if _u != _t:
        open(path, 'w', encoding='utf-8').write(_u)
        _r25_n += 1


def _r25_copy(src, dst):
    global _r25_n
    if not os.path.exists(dst) or open(src, 'rb').read() != open(dst, 'rb').read():
        shutil.copy(src, dst)
        _r25_n += 1


# ── the photographs and marks of this round (vendor/r25; the press marks redrawn by scripts/press_ink_r25.py)
for _f in sorted(glob.glob(SP + '/vendor/r25/*.jpg')):
    _r25_copy(_f, THEME + '/assets/' + os.path.basename(_f))
for _f in sorted(glob.glob(SP + '/vendor/r25/press/ms-press-*.png')):
    _r25_copy(_f, THEME + '/assets/' + os.path.basename(_f))

# ── the summer face: the atelier's own photograph of a linen weave, not a drawn colour
for _name in ('page.loro-piana-interiors.json', 'collection.ms-loro.json'):
    if os.path.exists(THEME + '/templates/' + _name):
        _h, _d = tpl_load(_name)
        _ss = _d['sections'].get('seasons', {}).get('settings', {})
        if _ss.get('summer_fallback') != 'ms-lp-linen-summer.jpg':
            _ss['summer_fallback'] = 'ms-lp-linen-summer.jpg'
            tpl_save(_name, _h, _d)
            _r25_n += 1

# ── a photograph graded in its own file (ms-graded-…) is not toned again by the site's gentle tone
_r25_sub(THEME + '/snippets/ms-photo-tone.liquid', [
    ('body img:not([src*=".svg"]):not([src*="ms-press-"])', 'body img:not([src*=".svg"]):not([src*="graded"]):not([src*="ms-press-"])')])

# ── Natural materials: a photograph chosen in the editor, toned as one with the bundled plates
_OWN = ' style="filter: grayscale(1) sepia(.42) contrast(1.05) brightness(1.03) !important;"'
_r25_sub(THEME + '/sections/ms-fibre-atlas.liquid', [
    ('<img class="ms-fa__photo" src="{{ photo }}"', '<img class="ms-fa__photo" src="{{ photo }}"{% if bs.image != blank %}' + _OWN + '{% endif %}')])
_r25_sub(THEME + '/sections/ms-fibre-gallery.liquid', [
    ('<img src="{{ src_sm }}" srcset="{{ src_sm }} 720w, {{ src }} 1400w"', '<img src="{{ src_sm }}"{% if bs.image != blank %}' + _OWN + '{% endif %} srcset="{{ src_sm }} 720w, {{ src }} 1400w"')])

# ── the press: every publication's mark, one still line at a time beneath the piece shown, those
#    with a piece first; the arrows beneath turn to the next line and nothing moves on its own. A mark
#    with a piece behind it brings it forward; the marks are drawn at one optical weight, and the SVG
#    marks are trimmed to their ink (scripts/press_trim_r25.py) so that each is measured alike. The
#    line is kept out of the site's scroll reveal (data-ms="pressrow"), which faded each mark up to
#    full ink before it settled back to its quiet tone.
for _f in sorted(glob.glob(SP + '/vendor/r25/press/ms-press-*.svg')):
    _r25_copy(_f, THEME + '/assets/' + os.path.basename(_f))
_PR_PREV = '<svg viewBox="0 0 16 16" aria-hidden="true" focusable="false"><path d="M10 3.5 5.5 8l4.5 4.5" fill="none" stroke="currentColor" stroke-width="1.1"/></svg>'
_PR_NEXT = '<svg viewBox="0 0 16 16" aria-hidden="true" focusable="false"><path d="M6 3.5 10.5 8 6 12.5" fill="none" stroke="currentColor" stroke-width="1.1"/></svg>'
_r25_sub(THEME + '/sections/ms-hp-proof.liquid', [
    ("""  link to read it. The award opens the sequence. Beneath, the marks of the most recent
  publications run in one slow line; hover or tap a mark to bring its piece forward. A
  publication with nothing to read (an empty press blog, no headline) is not shown.""",
     """  link to read it. The award opens the sequence. Beneath, every publication's mark, one still
  line at a time: those with a piece first (hover or tap one to bring its piece forward), then
  the others. The arrows beneath turn to the next line; nothing moves on its own."""),
    ("  assign recs = ''\n", "  assign recs = ''\n  assign rest = ''\n"),
    ("""    if line == blank
      continue
    endif
    if block.settings.logo != blank
      assign src = block.settings.logo | image_url: width: 300
    elsif block.settings.logo_file != blank
      assign src = block.settings.logo_file | asset_url
    else
      assign src = ''
    endif
""", """    if block.settings.logo != blank
      assign src = block.settings.logo | image_url: width: 300
    elsif block.settings.logo_file != blank
      assign src = block.settings.logo_file | asset_url
    else
      assign src = ''
    endif
    if line == blank
      # nothing to read: the mark is still shown, among the others on the line
      if src != blank
        assign rest = rest | append: src | append: '¤' | append: block.settings.name | append: '¦'
      endif
      continue
    endif
"""),
    ("""      assign n = n | plus: 1
    endfor
  endcapture
  capture press_url""", """      assign n = n | plus: 1
    endfor
    # the rest of the press: the pieces beyond those shown, then every other publication
    for r in recs offset: max
      assign f = r | split: '¤'
      if f[4] != blank
        assign ename = f[5] | escape
        echo '<li class="ms-pr__logo is-plain"><span class="ms-pr__pm"><img src="' | append: f[4] | append: '" alt="' | append: ename | append: '" width="150" height="40" loading="lazy"></span></li>'
      endif
    endfor
    assign rl = rest | split: '¦'
    for r in rl
      assign f = r | split: '¤'
      assign ename = f[1] | escape
      echo '<li class="ms-pr__logo is-plain"><span class="ms-pr__pm"><img src="' | append: f[0] | append: '" alt="' | append: ename | append: '" width="150" height="40" loading="lazy"></span></li>'
    endfor
  endcapture
  capture press_url"""),
    ("""        <ul class="ms-pr__run" role="list">{{ strip }}</ul>
      </div>
""", """        <ul class="ms-pr__run" role="list" data-ms="pressrow">{{ strip }}</ul>
      </div>
      <div class="ms-pr__pager" data-ms-pr-pager hidden>
        <button type="button" class="ms-pr__turn" data-ms-pr-turn="-1" aria-label="{% capture ms_t_out %}{% render 'ms-t', v: 'Previous' %}{% endcapture %}{{ ms_t_out | escape }}">""" + _PR_PREV + """</button>
        <span class="ms-pr__pages" data-ms-pr-pages role="group" aria-label="{% capture ms_t_out %}{% render 'ms-t', v: s.press_label %}{% endcapture %}{{ ms_t_out | escape }}"></span>
        <button type="button" class="ms-pr__turn" data-ms-pr-turn="1" aria-label="{% capture ms_t_out %}{% render 'ms-t', v: 'Next' %}{% endcapture %}{{ ms_t_out | escape }}">""" + _PR_NEXT + """</button>
      </div>
"""),
    ("""  .ms-pr__run > li:nth-child(n+9) { display: none; }
  @media (max-width: 760px) { .ms-pr__run { flex-wrap: wrap; } .ms-pr__run > li:nth-child(n+7) { display: none; } .ms-pr__logo > * { height: 42px; } }""",
     """  /* Round 25: every publication's mark, one still line at a time, those with a piece first; the
     arrows beneath turn to the next line, and nothing moves on its own */
  .ms-pr__rail { margin-top: 16px; }
  .ms-site .ms-pr .ms-pr__run { width: 100%; max-width: 1160px; margin: 0 auto; flex-wrap: nowrap; justify-content: center; overflow: hidden; transition: opacity .26s ease; }
  .ms-pr__run.is-turning { opacity: 0; }
  .ms-pr__run > li { display: flex; flex: 0 1 158px; min-width: 0; justify-content: center; }
  .ms-pr__run > li:nth-child(n+9) { display: none; }
  .ms-pr.is-paged .ms-pr__run > li { display: flex; }
  .ms-pr.is-paged .ms-pr__run > li[hidden] { display: none; }
  .ms-pr__logo > * { width: 100%; height: 64px; padding: 0 10px; }
  .ms-site .ms-pr .ms-pr__logo img { height: 24px; width: auto; max-width: 100%; max-height: 34px; opacity: .58; }
  .ms-site .ms-pr .ms-pr__logo > button:hover img, .ms-site .ms-pr .ms-pr__logo > button:focus-visible img, .ms-site .ms-pr .ms-pr__logo.is-on img { opacity: 1; }
  .ms-pr__logo.is-plain > * { cursor: default; }
  .ms-pr__pager { display: flex; align-items: center; justify-content: center; gap: 4px; margin-top: 6px; }
  .ms-pr__pager[hidden] { display: none; }
  .ms-pr__turn { width: 34px; height: 34px; display: flex; align-items: center; justify-content: center; padding: 0; background: none; border: 0; border-radius: 50%; color: #8A8276; cursor: pointer; transition: color .3s ease, background-color .3s ease; }
  .ms-pr__turn:hover, .ms-pr__turn:focus-visible { color: #17140F; background: #F1ECE2; }
  .ms-pr__turn svg { width: 15px; height: 15px; }
  .ms-pr__pages { display: flex; gap: 4px; margin: 0 6px; }
  .ms-pr__pages button { width: 24px; height: 24px; padding: 0; background: none; border: 0; cursor: pointer; display: flex; align-items: center; }
  .ms-pr__pages button span { display: block; width: 100%; height: 1px; background: #DDD6C9; transition: background-color .3s ease; }
  .ms-pr__pages button:hover span { background: #A89F90; }
  .ms-pr__pages button[aria-current="true"] span { background: #17140F; }
  @media (max-width: 760px) {
    .ms-site .ms-pr .ms-pr__run { flex-wrap: wrap; }
    .ms-pr__run > li { flex: 0 0 33.333%; }
    .ms-pr__run > li:nth-child(n+7) { display: none; }
    .ms-pr__logo > * { height: 56px; padding: 0 6px; }
    .ms-site .ms-pr .ms-pr__logo img { height: 20px; max-height: 28px; }
    .ms-pr__pages button { width: 18px; }
  }
  @media (max-width: 520px) {
    .ms-pr__run > li { flex-basis: 50%; }
    .ms-pr__run > li:nth-child(n+5) { display: none; }
  }
  @media (prefers-reduced-motion: reduce) { .ms-pr__run { transition: none; } }"""),
    ("""    } else { schedule(); }
  })();
</script>""", """    } else { schedule(); }

    // Round 25: every publication's mark, one still line at a time; the arrows turn to the next line
    var run = root.querySelector('.ms-pr__run'), pager = root.querySelector('[data-ms-pr-pager]');
    if (!run) return;
    var marks = [].slice.call(run.children), pages = [], page = 0, turning = null, x0 = null;
    var wide = window.matchMedia('(min-width: 1101px)'), narrow = window.matchMedia('(max-width: 760px)'), small = window.matchMedia('(max-width: 520px)');
    function weigh(img) {
      // one optical weight for marks of every shape: a long wordmark is drawn lower than a compact one
      var ar = img.naturalWidth / img.naturalHeight;
      if (!ar || !isFinite(ar)) return;
      var k = narrow.matches ? .8 : 1, wmax = small.matches ? 128 : narrow.matches ? 110 : 136;
      var h = Math.max(12, Math.min(30, 24 * Math.pow(4 / ar, .42))) * k;
      if (h * ar > wmax) h = Math.max(9, wmax / ar);
      img.style.height = h.toFixed(1) + 'px'; img.style.width = 'auto'; img.style.maxHeight = 'none';
    }
    function weighAll() {
      marks.forEach(function (m) {
        var i = m.querySelector('img');
        if (!i) return;
        if (i.complete && i.naturalWidth) weigh(i); else i.addEventListener('load', function () { weigh(i); }, { once: true });
      });
    }
    function turn(i, now) {
      if (!pages.length) return;
      page = (i + pages.length) % pages.length;
      function go() {
        marks.forEach(function (m) { m.hidden = pages[page].indexOf(m) < 0; });
        if (pager) pager.querySelectorAll('[data-ms-pr-page]').forEach(function (d, k) { d.setAttribute('aria-current', k === page ? 'true' : 'false'); });
        run.classList.remove('is-turning');
      }
      clearTimeout(turning);
      if (now || reduce) go(); else { run.classList.add('is-turning'); turning = setTimeout(go, 260); }
    }
    function cut() {
      // lines of as even a length as the marks allow: 27 marks on a wide screen are 7, 7, 7 and 6
      var max = wide.matches ? 8 : small.matches ? 4 : 6, n = marks.length, p = Math.max(1, Math.ceil(n / max)), q = Math.floor(n / p), r = n % p, k = 0, i;
      pages = [];
      for (i = 0; i < p; i++) { var c = q + (i < r ? 1 : 0); pages.push(marks.slice(k, k + c)); k += c; }
      root.classList.toggle('is-paged', p > 1);
      if (pager) {
        pager.hidden = p < 2;
        var dots = pager.querySelector('[data-ms-pr-pages]');
        dots.innerHTML = '';
        for (i = 0; i < p; i++) {
          var d = document.createElement('button');
          d.type = 'button'; d.setAttribute('data-ms-pr-page', i); d.setAttribute('aria-label', (i + 1) + ' / ' + p);
          d.appendChild(document.createElement('span')); dots.appendChild(d);
        }
      }
      turn(Math.min(page, p - 1), true);
      weighAll();
    }
    if (pager) pager.addEventListener('click', function (e) {
      var t = e.target.closest('[data-ms-pr-turn]'), d = e.target.closest('[data-ms-pr-page]');
      if (t) turn(page + +t.getAttribute('data-ms-pr-turn'));
      else if (d) turn(+d.getAttribute('data-ms-pr-page'));
    });
    run.addEventListener('touchstart', function (e) { x0 = e.touches[0].clientX; }, { passive: true });
    run.addEventListener('touchend', function (e) {
      if (x0 === null || pages.length < 2) return;
      var dx = e.changedTouches[0].clientX - x0; x0 = null;
      if (Math.abs(dx) > 40) turn(page + (dx < 0 ? 1 : -1));
    }, { passive: true });
    [wide, narrow, small].forEach(function (mq) { if (mq.addEventListener) mq.addEventListener('change', cut); else if (mq.addListener) mq.addListener(cut); });
    // the marks of the other lines are fetched as the section nears, so that a turn shows them at once
    if ('IntersectionObserver' in window) {
      var near = new IntersectionObserver(function (es) {
        if (!es[0].isIntersecting) return;
        near.disconnect();
        marks.forEach(function (m) { var i = m.querySelector('img'); if (i) i.loading = 'eager'; });
      }, { rootMargin: '600px 0px' });
      near.observe(root);
    }
    cut();
  })();
</script>"""),
    ('"info": "Only those with a piece to read, most recent first. The rest are on the press page."',
     '"info": "Those with a piece to read, most recent first; every other publication\'s mark follows on the line."'),
])

# ── yachts and private jets: the house has made beds for both
_JETS = [('Handmade beds for hotels, residences and yachts: specified to the room, delivered in phases, installed by our own team.',
          'Handmade beds for hotels, residences, yachts and private jets: specified to the room, delivered in phases, installed by our own team.'),
         ('Midsummer supplies hotels, branded residences and yachts with the same hand-built natural-fibre systems',
          'Midsummer supplies hotels, branded residences, yachts and private jets with the same hand-built natural-fibre systems')]
_r25_sub(THEME + '/sections/ms-hosp-01.liquid', _JETS[:1])
_r25_sub(THEME + '/sections/ms-hosp-02.liquid', _JETS[1:])
for _name in ('page.faq.json', 'collection.ms-faq.json', 'page.json'):
    if os.path.exists(THEME + '/templates/' + _name):
        _r25_sub(THEME + '/templates/' + _name, [('We supply hotels, branded residences and yachts with', 'We supply hotels, branded residences, yachts and private jets with')])
# the general FAQ still promised 15 + 15 to hotels: it is for private homes only
_r25_sub(THEME + '/templates/page.json', [(', housekeeping protocols per system, and the 15 + 15 service written into the agreement.</p>', ', and housekeeping protocols per system.</p>')])
for _name in ('page.facts.json', 'collection.ms-facts.json'):
    if os.path.exists(THEME + '/templates/' + _name):
        _r25_sub(THEME + '/templates/' + _name, [('Private homes, architects and interior designers, hotels, villas and yachts.', 'Private homes, architects and interior designers, hotels, villas, yachts and private jets.')])
_r25_sub(THEME + '/templates/index.llms.liquid', [('Clients include private homes, architects and interior designers, hotels, villas and yachts.',
                                                   'Clients include private homes, architects and interior designers, hotels, villas, yachts and private jets.')])
_r25_sub(THEME + '/snippets/meta-tags.liquid', [
    (": handmade beds for homes, hotels, villas and yachts, specified", ": handmade beds for homes, hotels, villas, yachts and private jets, specified"),
    ("'Handmade beds and mattresses for hotels, villas, yachts and residences, specified", "'Handmade beds and mattresses for hotels, villas, yachts, private jets and residences, specified")])
_sdp = THEME + '/config/settings_data.json'
_r25_sub(_sdp, [
    ('"description": "Handmade luxury beds, mattresses and toppers, built one by one, by hand, in Italy from natural fibres and Loro Piana Interiors fabrics."',
     '"description": "Handmade luxury beds, mattresses and toppers, built one by one, by hand, in Italy from natural fibres and Loro Piana Interiors fabrics, for private homes, hotels, yachts and private jets."'),
    ('Italian furniture craftsmanship, sleep systems"', 'Italian furniture craftsmanship, sleep systems, hotel beds, yacht beds, private jet beds"')])
_r25_sub(THEME + '/sections/ms-seo.liquid', [
    ('in Italy from natural fibres and Loro Piana Interiors fabrics. Atelier at Via Andegari 4, Milan, open by appointment."',
     'in Italy from natural fibres and Loro Piana Interiors fabrics, for private homes, hotels, yachts and private jets. Atelier at Via Andegari 4, Milan, open by appointment."'),
    ('Italian furniture craftsmanship, sleep systems"\n', 'Italian furniture craftsmanship, sleep systems, hotel beds, yacht beds, private jet beds"\n')])

# ── hospitality: two questions more. 15 + 15 is for beds in private homes; the house makes for yachts
#    and private jets too
_R25_QA = [('r25_q15', 'Does the 15 + 15 programme apply to hotel orders?',
            '<p>No. 15 + 15 is our programme for beds in private homes. Hotel, residence and other contract orders are specified, delivered and looked after under the agreement drawn up for each project.</p>'),
           ('r25_jets', 'Do you make beds for yachts and private jets?',
            '<p>Yes. We have made beds for yachts and for private jets: drawn to the cabin, made to its exact sizes and by hand in Italy, like every Midsummer bed.</p>')]
for _name in ('page.hospitality.json', 'collection.ms-hospitality.json'):
    if not os.path.exists(THEME + '/templates/' + _name):
        continue
    _h, _d = tpl_load(_name)
    _qa = _d['sections'].get('qa')
    if _qa is None:
        continue
    _chg = False
    for _id, _q, _a in _R25_QA:
        if _id not in _qa.setdefault('blocks', {}):
            _qa['blocks'][_id] = {'type': 'qa', 'settings': {'q': _q, 'a': _a}}
            _qa.setdefault('block_order', []).insert(1 if _id == 'r25_q15' else len(_qa['block_order']), _id)
            _chg = True
    if _chg:
        tpl_save(_name, _h, _d)
        _r25_n += 1

# ── Sleep Culture: a night, hour by hour, after the opening statement; rooms kept for rest, after the
#    three things the house designs for
_R25_NIGHT = {'type': 'ms-night', 'settings': {
    'eyebrow': 'From lying down to waking', 'heading': 'A night, as the bed lives it.',
    'text': 'Eight hours, give or take, in one place. Choose an hour to see what the bed is doing while you sleep.',
    'link_label': 'The fibres, one by one'},
    'blocks': {
        'h1': {'type': 'hour', 'settings': {'time': '23:00', 'name': 'Lying down', 'text': 'The body lets go of the day and gives off its warmth. Natural fibres take it in and let it pass, so the bed feels neither cold nor close.'}},
        'h2': {'type': 'hour', 'settings': {'time': '01:00', 'name': 'Deep sleep', 'text': 'The body is at its heaviest and stillest. A bed made by hand follows its line, so that the shoulders and the hips rest without pressing.'}},
        'h3': {'type': 'hour', 'settings': {'time': '03:00', 'name': 'The coolest hour', 'text': 'In the small hours the body runs at its coolest. Wool keeps the warmth close in winter; in summer, linen and silk let it go.'}},
        'h4': {'type': 'hour', 'settings': {'time': '05:00', 'name': 'Lighter sleep', 'text': 'Sleep grows lighter and you turn more often. The bed answers each turn quietly, and settles again.'}},
        'h5': {'type': 'hour', 'settings': {'time': '07:00', 'name': 'Waking', 'text': 'Leave the covers turned back for a while: the fibres give up the night’s moisture to the air, and the bed is fresh again by evening.'}}},
    'block_order': ['h1', 'h2', 'h3', 'h4', 'h5']}


def _r25_gallery(eyebrow, heading, photos):
    bl = {}
    for _i, (_f, _c) in enumerate(photos, 1):
        bl['p%02d' % _i] = {'type': 'photo', 'settings': {'image_fallback': _f, 'caption': _c}}
    return {'type': 'ms-gallery', 'settings': {'eyebrow': eyebrow, 'heading': heading}, 'blocks': bl, 'block_order': sorted(bl)}


_R25_ROOMS = _r25_gallery('The bedroom', 'Rooms kept for rest.', [
    ('ms-photo-sleep-tulip.jpg', 'Tulip, in blue velvet, made up for the night.'),
    ('ms-photo-sleep-pillows.jpg', 'Pillows against a padded headboard.'),
    ('ms-photo-sleep-turned-down.jpg', 'Turned down for the night.'),
    ('ms-photo-sleep-throw.jpg', 'A throw folded back at the foot of the bed.'),
    ('ms-photo-sleep-made-up.jpg', 'A bed made up in the blue-and-gold room.')])
_R25_ATELIER = _r25_gallery('The rooms', 'Inside Via Andegari.', [
    ('ms-photo-atelier-leopard.jpg', 'The leopard room, a bed made up for the night.'),
    ('ms-photo-atelier-teal.jpg', 'Teal bedding, printed with flowers and birds.'),
    ('ms-photo-atelier-parrot-room.jpg', 'The parrot room.'),
    ('ms-photo-atelier-blue-gold-made.jpg', 'The blue-and-gold room, the bed made up.'),
    ('ms-photo-atelier-lacquer.jpg', 'Walnut and orange lacquer.'),
    ('ms-photo-atelier-red-wall.jpg', 'A golden branch on a red wall.'),
    ('ms-photo-atelier-edge.jpg', 'The edge of a mattress, piped and stitched by hand.'),
    ('ms-photo-atelier-linen.jpg', 'Linen, folded and ready for the bed.')])


def _r25_place(name, key, sec, after):
    global _r25_n
    if not os.path.exists(THEME + '/templates/' + name):
        return
    _h, _d = tpl_load(name)
    if key in _d['sections']:
        return
    _d['sections'][key] = json.loads(json.dumps(sec))
    _o = _d['order']
    _o.insert(_o.index(after) + 1 if after in _o else len(_o), key)
    tpl_save(name, _h, _d)
    _r25_n += 1


for _name in ('page.sleep-culture.json', 'collection.ms-sleep-culture.json'):
    _r25_place(_name, 'night', _R25_NIGHT, 's02')
    _r25_place(_name, 'rooms', _R25_ROOMS, 's03')
for _name in ('page.atelier.json', 'collection.ms-atelier.json'):
    _r25_place(_name, 'rooms', _R25_ATELIER, 's04')

print('round 25: %d files changed' % _r25_n)
