# Round 26, run at the end of bin/build_more.py in its scope (THEME, tpl_load, tpl_save ...), after
# Round 25. Every step is an exact replacement or a guarded write, so a second build changes nothing.
#  · The theme editor: a section that lives on some pages alone shows a slim editor-only note
#    elsewhere, instead of showing itself where the store never does (the Tangram on every collection).

_r26_n = 0


def _r26_sub(path, pairs):
    global _r26_n
    _t = open(path, encoding='utf-8').read()
    _u = _t
    for _a, _b in pairs:
        if _a in _u:
            _u = _u.replace(_a, _b)
        else:
            assert _b in _u, (path, _a[:80])
    if _u != _t:
        open(path, 'w', encoding='utf-8').write(_u)
        _r26_n += 1


def _r26_copy(src, dst):
    global _r26_n
    if not os.path.exists(dst) or open(src, 'rb').read() != open(dst, 'rb').read():
        shutil.copy(src, dst)
        _r26_n += 1


# ── the theme editor: where a section is not shown, a note says where it is
_r26_copy(SP + '/bin/r26/ms-ednote.liquid', THEME + '/snippets/ms-ednote.liquid')
_r26_sub(THEME + '/sections/ms-tangram.liquid', [
    ("""  if request.design_mode
    assign show = true
  endif
-%}""", """  # in the theme editor, elsewhere: a note in its place (snippets/ms-ednote), not the section itself
-%}"""),
    ("""  document.addEventListener('shopify:section:load', function (e) { init(e.target.querySelector('[data-ms-tg]')); });
})();
</script>
{%- endif -%}""", """  document.addEventListener('shopify:section:load', function (e) { init(e.target.querySelector('[data-ms-tg]')); });
})();
</script>
{%- else -%}
{%- render 'ms-ednote', kind: 'tangram' -%}
{%- endif -%}"""),
])
_r26_sub(THEME + '/sections/ms-craft.liquid', [
    ("    elsif mkp[0] != 'system' and request.design_mode != true\n", "    elsif mkp[0] != 'system'\n"),
    ("""      draw.addEventListener('pointerleave', function () { svg.style.setProperty('--px', 0); svg.style.setProperty('--py', 0); });
    }
  });
})();
</script>
{%- endif -%}

{% schema %}""", """      draw.addEventListener('pointerleave', function () { svg.style.setProperty('--px', 0); svg.style.setProperty('--py', 0); });
    }
  });
})();
</script>
{%- else -%}
{%- render 'ms-ednote', kind: 'craft' -%}
{%- endif -%}

{% schema %}"""),
])
# ── the collection photographs in their own colours: the opening photograph had a dark veil over all of
#    it (and the house tone on top: the "double filter"); now only a soft shade where the title and the
#    header sit, and no tone. The product photographs of a collection are shown untoned too; a softened
#    photograph (the Thin Topper) keeps only its softening there, without the tone.
_r26_sub(THEME + '/sections/ms-collection-hero.liquid', [
    ('<section style="position: relative; overflow: hidden; background: rgb(23, 20, 15);">',
     '<section class="ms-colhero" style="position: relative; overflow: hidden; background: rgb(23, 20, 15);">\n<style>.ms-site .ms-colhero img, body .ms-colhero img { filter: none !important; } .ms-colhero h1, .ms-colhero h1 ~ *, .ms-colhero [style*="letter-spacing: 0.3em"] { text-shadow: 0 1px 24px rgba(10, 8, 6, .5), 0 0 2px rgba(10, 8, 6, .3); } .ms-colhero [style*="letter-spacing: 0.3em"] { opacity: 1 !important; }</style>'),
    ('<div style="position: absolute; inset: 0px; background: linear-gradient(rgba(10, 8, 6, 0.3), rgba(10, 8, 6, 0.55));"></div>',
     '<div style="position: absolute; inset: 0px; background: radial-gradient(ellipse 52% 62% at {% if tier_side == \'right\' %}100%{% else %}0%{% endif %} 100%, rgba(10, 8, 6, 0.42), rgba(10, 8, 6, 0) 72%), linear-gradient(180deg, rgba(10, 8, 6, 0.34) 0%, rgba(10, 8, 6, 0) 24%, rgba(10, 8, 6, 0) 50%, rgba(10, 8, 6, 0.36) 100%);"></div>'),
])
_r26_sub(THEME + '/sections/ms-systems.liquid', [
    ("  .ms-sy__kinds { display: flex; flex-wrap: wrap; gap: 8px; margin-top: clamp(24px, 3vw, 40px); }\n",
     "  /* Round 26: a collection's photographs in their own colours, without the house tone */\n  .ms-site .ms-sy img, body .ms-sy img { filter: none !important; }\n  .ms-sy__kinds { display: flex; flex-wrap: wrap; gap: 8px; margin-top: clamp(24px, 3vw, 40px); }\n"),
])
_r26_sub(THEME + '/snippets/ms-photo-soften.liquid', [
    ("""  {%- if sel != '' -%}
  <style>{{ sel }} body img.ms-photo-soften { filter: sepia({{ sep }}) saturate({{ sat }}) contrast({{ con }}) brightness({{ bri }}) !important; }</style>""",
     """  {%- if sel != '' -%}
  {%- assign sel_c = sel | replace: 'body img[', '.ms-site .ms-sy img[' -%}
  {%- assign bri_c = keep | round: 3 -%}
  <style>{{ sel }} body img.ms-photo-soften { filter: sepia({{ sep }}) saturate({{ sat }}) contrast({{ con }}) brightness({{ bri }}) !important; }
  {{ sel_c }} .ms-site .ms-sy img.ms-photo-soften { filter: saturate(0.96) brightness({{ bri_c }}) !important; }</style>"""),
])

# ── Icons opens on the Giotto Round in the abbey of San Galgano, the bed at the left: the title moves to
#    the right, over the stone. The collection's own image in the admin (Bellagio) is left as it is.
for _f in sorted(glob.glob(SP + '/vendor/r26/*.jpg')):
    _r26_copy(_f, THEME + '/assets/' + os.path.basename(_f))
# (Rounds 28 and 29 open Icons on other photographs, and leave this step behind them)
_h26 = open(THEME + '/sections/ms-collection-hero.liquid', encoding='utf-8').read()
if 'ms-photo-icons-pair.jpg' not in _h26 and 'ms-photo-icons-opera.jpg' not in _h26:
  _r26_sub(THEME + '/sections/ms-collection-hero.liquid', [
    ("  assign tier_pos = 'center'\n", "  assign tier_pos = 'center'\n  assign tier_side = 'left'\n"),
    ("""    when 'icons', 'icon'
      assign tier_name = 'ms-graded-arches.jpg'
      assign tier_photo = tier_name | asset_url
      assign tier_pos = 'center 64%'""", """    when 'icons', 'icon'
      assign tier_name = 'ms-photo-icons-abbey.jpg'
      assign tier_photo = tier_name | asset_url
      assign tier_pos = '24% 84%'
      assign tier_side = 'right'"""),
    ('<div style="position: absolute; inset: 0px; display: flex; flex-direction: column; justify-content: flex-end; padding: clamp(26px, 5vw, 88px); color: rgb(251, 249, 245);">',
     '<div style="position: absolute; inset: 0px; display: flex; flex-direction: column; justify-content: flex-end; padding: clamp(26px, 5vw, 88px); color: rgb(251, 249, 245);{% if tier_side == \'right\' %} align-items: flex-end; text-align: right;{% endif %}">'),
])

# ── Professionals: the bar under the header kept the header's height from the moment the page loaded;
#    when the header's real height came out a few pixels different (its fonts, its logo), a strip of the
#    page showed between the two while scrolling. Now it follows the header's bottom edge as it changes,
#    sits a hair under it rather than a hair below, and while it is held under the header a cream skirt
#    behind it covers any gap.
_r26_sub(THEME + '/sections/ms-pro-nav.liquid', [
    ("  .ms-pn { background: #FBF9F5; border-bottom: 1px solid rgba(23, 20, 15, .1); }",
     "  .ms-pn { position: relative; background: #FBF9F5; border-bottom: 1px solid rgba(23, 20, 15, .1); }\n"
     "  .ms-pn.is-stuck::before { content: ''; position: absolute; left: 0; right: 0; bottom: 100%; height: 48px; background: #FBF9F5; pointer-events: none; }"),
    ("""    function set() {
      var h = !w || w.classList.contains('is-hidden') ? 0 : w.getBoundingClientRect().height;
      document.documentElement.style.setProperty('--ms-pn-top', Math.round(h) + 'px');
    }
    set();
    if (w && window.MutationObserver) new MutationObserver(set).observe(w, { attributes: true, attributeFilter: ['class'] });
    window.addEventListener('resize', set);""",
     """    var hd = w && (w.querySelector('[data-ms-header]') || w), top = 0;
    function set() {
      // the header's own bottom edge, where its colour ends; a pixel under it, never a pixel below
      var h = !w || w.classList.contains('is-hidden') ? 0 : Math.max(hd.getBoundingClientRect().bottom - w.getBoundingClientRect().top, 0);
      top = h ? Math.max(Math.floor(h) - 1, 0) : 0;
      document.documentElement.style.setProperty('--ms-pn-top', top + 'px');
      stuck();
    }
    function stuck() {
      Array.prototype.forEach.call(document.querySelectorAll('.ms-pn'), function (n) { n.classList.toggle('is-stuck', n.getBoundingClientRect().top <= top + 2); });
    }
    set();
    if (w && window.MutationObserver) new MutationObserver(set).observe(w, { attributes: true, attributeFilter: ['class'] });
    if (w && window.ResizeObserver) new ResizeObserver(set).observe(hd);
    window.addEventListener('resize', set);
    window.addEventListener('load', set);
    window.addEventListener('scroll', stuck, { passive: true });
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(set);"""),
])

# ── the galleries composed (sections/ms-gallery, from bin/extra): Sleep Culture's rooms all from the
#    shoot at Via Andegari, the older Tulip pictures retired; the atelier's rooms in an order that makes
#    even rows; each theme photograph's proportion read from its own file.
from PIL import Image as _R26Image
_R26_SLEEP = [
    ('ms-photo-sleep-made-up.jpg', 'A bed made up in the blue-and-gold room.'),
    ('ms-photo-sleep-turned-down.jpg', 'Turned down for the night.'),
    ('ms-photo-sleep-pillows.jpg', 'Pillows against a padded headboard.'),
    ('ms-photo-sleep-blanket.jpg', 'A grey blanket over white sheets.'),
    ('ms-photo-sleep-bedside.jpg', 'The bedside, in the parrot room.'),
    ('ms-photo-sleep-armchair.jpg', 'A throw left on the armchair.')]
_R26_ATELIER_ORDER = ['ms-photo-atelier-blue-gold-made.jpg', 'ms-photo-atelier-leopard.jpg', 'ms-photo-atelier-teal.jpg',
                      'ms-photo-atelier-parrot-room.jpg', 'ms-photo-atelier-lacquer.jpg', 'ms-photo-atelier-edge.jpg',
                      'ms-photo-atelier-red-wall.jpg', 'ms-photo-atelier-linen.jpg']
for _f in ('ms-photo-sleep-tulip.jpg', 'ms-photo-sleep-throw.jpg'):
    if os.path.exists(THEME + '/assets/' + _f):
        os.remove(THEME + '/assets/' + _f)
        _r26_n += 1


def _r26_ratio(_fn):
    _p = THEME + '/assets/' + _fn
    if not _fn or not os.path.exists(_p):
        return ''
    _w, _h = _R26Image.open(_p).size
    return '%.3f' % (_w / _h)


for _name in sorted(os.listdir(THEME + '/templates')):
    if not _name.endswith('.json'):
        continue
    _h, _d = tpl_load(_name)
    _ch = False
    for _k, _sec in _d.get('sections', {}).items():
        if _sec.get('type') != 'ms-gallery':
            continue
        if _k == 'rooms' and 'sleep-culture' in _name:
            _bl = {'p%02d' % _i: {'type': 'photo', 'settings': {'image_fallback': _f, 'caption': _c}} for _i, (_f, _c) in enumerate(_R26_SLEEP, 1)}
            if _sec.get('blocks') != _bl:
                _sec['blocks'], _sec['block_order'], _ch = _bl, sorted(_bl), True
        if _k == 'rooms' and 'atelier' in _name:
            _by = {_b['settings'].get('image_fallback'): _bid for _bid, _b in _sec['blocks'].items()}
            _order = [_by[_f] for _f in _R26_ATELIER_ORDER if _f in _by] + [_b for _b in _sec['block_order'] if _b not in [_by.get(_f) for _f in _R26_ATELIER_ORDER]]
            if _order != _sec['block_order']:
                _sec['block_order'], _ch = _order, True
        for _b in _sec.get('blocks', {}).values():
            _r = _r26_ratio(_b.get('settings', {}).get('image_fallback', ''))
            if _r and _b['settings'].get('ratio') != _r:
                _b['settings']['ratio'], _ch = _r, True
    if _ch:
        tpl_save(_name, _h, _d)
        _r26_n += 1

# ── the press: one endless line of every publication's mark, seamless. It drifts slowly (off where the
#    visitor asks for less motion, or in the editor), stops under the cursor and is held and moved by
#    hand, with a round cursor that says so; a mark with a piece still brings it forward. The lines of
#    Round 25 and their arrows give way to it.
_PRP = THEME + '/sections/ms-hp-proof.liquid'
_t = open(_PRP, encoding='utf-8').read()
_u = re.sub(r'      <div class="ms-pr__pager" data-ms-pr-pager hidden>.*?\n      </div>\n', '', _t, flags=re.S)
_u = _u.replace('<div class="ms-pr__rail" data-ms-pr-rail>', '<div class="ms-pr__rail" data-ms-pr-rail data-drift="{% if s.drift == false %}0{% else %}1{% endif %}">')
_u = _u.replace('<ul class="ms-pr__run" role="list" data-ms="pressrow">{{ strip }}</ul>\n',
                '<ul class="ms-pr__run" role="list" data-ms="pressrow">{{ strip }}</ul>\n'
                '        <span class="ms-pr__cursor" aria-hidden="true"><span><svg viewBox="0 0 10 10"><path d="M6.5 2 3.5 5l3 3" fill="none" stroke="currentColor" stroke-width="1"/></svg>{% render \'ms-t\', v: \'Drag\' %}<svg viewBox="0 0 10 10"><path d="m3.5 2 3 3-3 3" fill="none" stroke="currentColor" stroke-width="1"/></svg></span></span>\n')
_CSS26 = """  /* Round 26: one endless line of every publication's mark, drifting slowly, held and moved by hand */
  .ms-pr__rail { position: relative; display: block; margin: 14px 0 0; overflow: hidden; touch-action: pan-y; -webkit-mask-image: none; mask-image: none; user-select: none; -webkit-user-select: none; }
  .ms-pr__rail::before, .ms-pr__rail::after { content: ''; position: absolute; top: 0; bottom: 0; z-index: 1; width: clamp(40px, 9vw, 160px); pointer-events: none; }
  .ms-pr__rail::before { left: 0; background: linear-gradient(90deg, #FBF9F5, rgba(251, 249, 245, 0)); }
  .ms-pr__rail::after { right: 0; background: linear-gradient(270deg, #FBF9F5, rgba(251, 249, 245, 0)); }
  .ms-site .ms-pr .ms-pr__run { display: flex; flex-wrap: nowrap; justify-content: flex-start; width: max-content; max-width: none; margin: 0; overflow: visible; animation: none; will-change: transform; }
  .ms-pr__run > li, .ms-pr__run > li:nth-child(n) { display: flex; flex: 0 0 auto; }
  .ms-pr__logo > * { width: clamp(136px, 12vw, 176px); height: 76px; padding: 0 clamp(14px, 1.6vw, 26px); }
  .ms-site .ms-pr .ms-pr__logo img { height: 24px; width: auto; max-width: 100%; max-height: 30px; opacity: .58; pointer-events: none; -webkit-user-drag: none; transition: opacity .35s ease; }
  .ms-site .ms-pr .ms-pr__logo > button:hover img, .ms-site .ms-pr .ms-pr__logo > button:focus-visible img, .ms-site .ms-pr .ms-pr__logo.is-on img { opacity: 1; }
  .ms-pr__logo.is-plain > * { cursor: inherit; }
  .ms-pr__rail.is-dragging .ms-pr__logo > * { cursor: inherit; }
  .ms-pr__cursor { position: absolute; left: 0; top: 0; z-index: 2; width: 0; height: 0; pointer-events: none; }
  .ms-pr__cursor > span { position: absolute; left: -42px; top: -42px; width: 84px; height: 84px; border-radius: 50%; display: flex; align-items: center; justify-content: center; gap: 3px; background: rgba(23, 20, 15, .9); color: #FBF9F5; font-size: 9px; letter-spacing: .16em; text-transform: uppercase; opacity: 0; transform: scale(.4); transition: opacity .3s ease, transform .45s cubic-bezier(.2, .7, .2, 1); }
  .ms-pr__cursor svg { width: 7px; height: 7px; flex: 0 0 auto; }
  .ms-pr__cursor.is-tight svg { display: none; }
  .ms-pr__rail.is-cursor .ms-pr__cursor > span { opacity: 1; transform: scale(1); }
  .ms-pr__rail.is-cursor.is-dragging .ms-pr__cursor > span { transform: scale(.82); }
  @media (hover: hover) and (pointer: fine) { .ms-pr__rail, .ms-pr__rail * { cursor: none !important; } }
  @media (hover: none), (pointer: coarse) { .ms-pr__cursor { display: none; } }
  @media (max-width: 760px) {
    .ms-pr__logo > * { width: 124px; height: 64px; padding: 0 12px; }
    .ms-site .ms-pr .ms-pr__logo img { height: 20px; max-height: 26px; }
  }
  @media (prefers-reduced-motion: reduce) { .ms-pr__rail { overflow: hidden; } }"""
_u = re.sub(r"  /\* Round 25: every publication's mark, one still line at a time, those with a piece first; the\n.*?  @media \(prefers-reduced-motion: reduce\) \{ \.ms-pr__run \{ transition: none; \} \}", lambda _m: _CSS26, _u, flags=re.S)
_JS26 = r"""    // Round 26: one endless line of every mark: it drifts slowly, stops under the cursor, and is moved by hand
    var rail = root.querySelector('[data-ms-pr-rail]'), run = root.querySelector('.ms-pr__run'), cur = root.querySelector('.ms-pr__cursor');
    if (!rail || !run) return;
    var marks = [].slice.call(run.children), narrow = window.matchMedia('(max-width: 760px)'), fine = window.matchMedia('(hover: hover) and (pointer: fine)');
    var setW = 0, x = 0, v = 0, drag = null, held = false, focus = false, moved = 0, rest = 0, t0 = 0, raf = 0, seen = true, quiet = 0;
    var drift = rail.getAttribute('data-drift') !== '0' && !reduce;
    function weigh(img) {
      // one optical weight for marks of every shape: a long wordmark is drawn lower than a compact one
      var ar = img.naturalWidth / img.naturalHeight;
      if (!ar || !isFinite(ar)) return;
      var k = narrow.matches ? .84 : 1, wmax = narrow.matches ? 100 : 136;
      var h = Math.max(12, Math.min(30, 24 * Math.pow(4 / ar, .42))) * k;
      if (h * ar > wmax) h = Math.max(9, wmax / ar);
      img.style.height = h.toFixed(1) + 'px'; img.style.width = 'auto'; img.style.maxHeight = 'none';
    }
    function weighAll() {
      run.querySelectorAll('img').forEach(function (i) {
        if (i.complete && i.naturalWidth) weigh(i); else i.addEventListener('load', function () { weigh(i); }, { once: true });
      });
    }
    function build() {
      // as many copies of the line as fill the width twice over, so that it never shows an end
      run.querySelectorAll('[data-ms-pr-copy]').forEach(function (c) { c.remove(); });
      setW = marks.reduce(function (s, m) { return s + m.offsetWidth; }, 0);
      if (!setW) return;
      var copies = Math.max(1, Math.ceil(rail.clientWidth * 2 / setW));
      for (var k = 0; k < copies; k++) marks.forEach(function (m) {
        var c = m.cloneNode(true);
        c.setAttribute('data-ms-pr-copy', ''); c.setAttribute('aria-hidden', 'true'); c.removeAttribute('data-shopify-editor-block');
        c.querySelectorAll('button, a').forEach(function (b) { b.tabIndex = -1; });
        c.querySelectorAll('img').forEach(function (i) { i.loading = 'eager'; });
        run.appendChild(c);
      });
      weighAll();
    }
    function paint() {
      if (setW) x = ((x % setW) + setW) % setW;
      run.style.transform = 'translate3d(' + (-x).toFixed(2) + 'px, 0, 0)';
    }
    function tick(t) {
      var dt = t0 ? Math.min(t - t0, 64) : 16; t0 = t;
      if (!drag) {
        if (Math.abs(v) > 0.01) { x += v * dt; v *= Math.pow(0.92, dt / 16); }
        else if (drift && !held && !focus && t > rest) { v = 0; x += 0.024 * dt; }
      }
      // while it is moved or still gliding, the marks passing under the hand do not each bring their piece forward
      if (drag || Math.abs(v) > 0.01) quiet = t + 320;
      root.classList.toggle('is-pr-dragging', t < quiet);
      paint();
      raf = seen ? requestAnimationFrame(tick) : 0;
    }
    function go() { if (!raf) { t0 = 0; raf = requestAnimationFrame(tick); } }
    rail.addEventListener('pointerdown', function (e) {
      if (e.pointerType === 'mouse' && e.button !== 0) return;
      drag = { x: e.clientX, y: e.clientY, lx: e.clientX, t: performance.now(), id: e.pointerId, lock: null };
      moved = 0; v = 0; held = true;
      root.classList.add('is-pr-dragging'); quiet = performance.now() + 320;
    });
    window.addEventListener('pointermove', function (e) {
      if (cur && fine.matches && rail.classList.contains('is-cursor')) {
        var r = rail.getBoundingClientRect();
        cur.style.transform = 'translate3d(' + (e.clientX - r.left).toFixed(1) + 'px, ' + (e.clientY - r.top).toFixed(1) + 'px, 0)';
      }
      if (!drag || e.pointerId !== drag.id) return;
      var dx = e.clientX - drag.x, dy = e.clientY - drag.y;
      if (drag.lock === null && (Math.abs(dx) > 6 || Math.abs(dy) > 6)) {
        drag.lock = Math.abs(dx) > Math.abs(dy) ? 'x' : 'y';
        if (drag.lock === 'x') { try { rail.setPointerCapture(e.pointerId); } catch (err) {} rail.classList.add('is-dragging'); root.classList.add('is-pr-dragging'); quiet = performance.now() + 320; }
      }
      if (drag.lock === 'y') { drag = null; held = rail.classList.contains('is-cursor'); return; }
      if (drag.lock !== 'x') return;
      var now = performance.now(), step = e.clientX - drag.lx;
      x -= step; v = Math.max(-1.4, Math.min(1.4, v * .7 - step / Math.max(now - drag.t, 8) * .3)); drag.t = now; drag.lx = e.clientX; moved = Math.max(moved, Math.abs(dx));
      paint();
    });
    function end() {
      if (!drag) return;
      if (performance.now() - drag.t > 90) v = 0;
      drag = null; rail.classList.remove('is-dragging');
      held = rail.classList.contains('is-cursor'); rest = performance.now() + 1600;
    }
    window.addEventListener('pointerup', end); window.addEventListener('pointercancel', end);
    // a drag is not a click
    rail.addEventListener('click', function (e) { if (moved > 6) { e.preventDefault(); e.stopPropagation(); } moved = 0; }, true);
    rail.addEventListener('wheel', function (e) {
      if (Math.abs(e.deltaX) <= Math.abs(e.deltaY)) return;
      e.preventDefault(); x += e.deltaX; v = 0; rest = performance.now() + 1600; paint();
    }, { passive: false });
    if (cur) {
      rail.addEventListener('pointerenter', function (e) { if (e.pointerType === 'mouse' && fine.matches) { rail.classList.add('is-cursor'); held = true; var r = rail.getBoundingClientRect(); cur.style.transform = 'translate3d(' + (e.clientX - r.left).toFixed(1) + 'px, ' + (e.clientY - r.top).toFixed(1) + 'px, 0)'; } });
      rail.addEventListener('pointerleave', function () { rail.classList.remove('is-cursor'); if (!drag) held = false; });
    }
    // a mark reached from the keyboard comes into view, and the line waits for it
    rail.addEventListener('focusin', function (e) {
      var li = e.target.closest('li'); if (!li) return;
      try { if (!e.target.matches(':focus-visible')) return; } catch (err) {}
      focus = true; v = 0; x = li.offsetLeft - (rail.clientWidth - li.offsetWidth) / 2; paint();
    });
    rail.addEventListener('focusout', function () { focus = false; rest = performance.now() + 1600; });
    var rw = rail.clientWidth;
    window.addEventListener('resize', function () { if (Math.abs(rail.clientWidth - rw) > 40) { rw = rail.clientWidth; build(); } });
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (es) { seen = es[0].isIntersecting; if (seen) go(); }, { rootMargin: '200px 0px' }).observe(rail);
    }
    // a longer word for "drag" (in another language) keeps the disc round: the little arrows give way
    if (cur && cur.firstElementChild && document.createRange) {
      var cs = cur.firstElementChild, rg = document.createRange(), m = getComputedStyle(cs).transform, sc = 1;
      if (m && m.indexOf('matrix(') === 0) sc = parseFloat(m.slice(7)) || 1;
      rg.selectNodeContents(cs);
      if (rg.getBoundingClientRect().width / sc > cs.offsetWidth - 12) cur.classList.add('is-tight');
    }
    build(); paint(); go();
"""
_u = re.sub(r"    // Round 25: every publication's mark, one still line at a time; the arrows turn to the next line\n.*?    cut\(\);\n", lambda _m: _JS26, _u, flags=re.S)
_u = _u.replace(
    '{ "type": "range", "id": "max_logos", "label": "Publications shown",',
    '{ "type": "checkbox", "id": "drift", "label": "Let the line of marks drift slowly", "info": "It stops under the cursor, and can always be moved by hand.", "default": true },\n    { "type": "range", "id": "max_logos", "label": "Publications shown",')
# while the line is dragged, the marks passing under the hand do not each bring their piece forward
_u = _u.replace("      if (b && +b.getAttribute('data-ms-pr-to') !== at) show(+b.getAttribute('data-ms-pr-to'));",
                "      if (b && !root.classList.contains('is-pr-dragging') && +b.getAttribute('data-ms-pr-to') !== at) show(+b.getAttribute('data-ms-pr-to'));")
assert '// Round 26: one endless line' in _u and 'Round 26: one endless line of every publication' in _u and 'ms-pr__cursor' in _u and 'data-ms-pr-pager' not in _u, 'press r26'
if _u != _t:
    open(_PRP, 'w', encoding='utf-8').write(_u)
    _r26_n += 1

# ── Top: the Green Product Award, as a seal on the drawing of Inside Top. Its ring (Green Product Award ·
#    Berlin · 2025) turns slowly round the award's own mark, and it leads to the award's page. Only on the
#    Top system, found as the product page finds it (Top Dream is another bed).
_SEAL = """      <figure class="ms-cr__draw">
        {%- liquid
          assign cr_award = false
          if pname != ''
            assign ms_tt = product.title | downcase | strip
            assign ms_aw = product.metafields.custom.award.value | append: ''
            if ms_key == 'top-2' or product.handle == 'top' or product.handle == 'top-2' or ms_tt == 'top' or ms_tt contains 'top sleeping system' or ms_tt contains 'top bed system' or ms_tt contains 'top system' or ms_tt contains 'sistema top' or ms_tt contains 'sistema letto top' or ms_aw contains 'Green Product Award'
              unless ms_tt contains 'dream'
                assign cr_award = true
              endunless
            endif
          endif
        -%}
        {%- if cr_award -%}
          <a class="ms-cr__seal" href="https://www.gp-award.com/en/produkte/top-bed-system" target="_blank" rel="noopener" aria-label="{% capture ms_t_out %}{% render 'ms-t', v: 'Green Product Award 2025' %}{% endcapture %}{{ ms_t_out | strip | escape }}">
            <svg class="ms-cr__seal-ring" viewBox="0 0 120 120" aria-hidden="true" focusable="false">
              <defs><path id="crs-{{ section.id }}" d="M60 60m-46.5 0a46.5 46.5 0 1 1 93 0a46.5 46.5 0 1 1-93 0"/></defs>
              <circle cx="60" cy="60" r="59" fill="#FBF9F5" stroke="#B4996B" stroke-width=".7"/>
              <circle cx="60" cy="60" r="55.6" fill="none" stroke="#D9CBB2" stroke-width=".5"/>
              <circle cx="60" cy="60" r="37.5" fill="none" stroke="#B4996B" stroke-width=".6"/>
              <text textLength="290" lengthAdjust="spacing"><textPath href="#crs-{{ section.id }}">{% render 'ms-t', v: 'Green Product Award · Berlin · 2025' %} ·</textPath></text>
            </svg>
            <span class="ms-cr__seal-in" aria-hidden="true">
              <img src="{{ 'ms-press-green-product-award.svg' | asset_url }}" alt="" width="28" height="28">
              <strong>2025</strong>
            </span>
          </a>
        {%- endif -%}
"""
_SEAL_CSS = """  .ms-cr__draw { margin: 0; }
  /* Round 26: the Green Product Award's seal on Inside Top */
  .ms-cr__draw { position: relative; }
  .ms-site a.ms-cr__seal { position: absolute; top: clamp(-44px, -3vw, -8px); left: clamp(-16px, -1vw, 0px); z-index: 3; width: clamp(96px, 8.6vw, 128px); aspect-ratio: 1; display: block; color: #7E623B; border-radius: 50%; filter: drop-shadow(0 10px 22px rgba(60, 40, 20, .12)); transition: transform .5s cubic-bezier(.2, .7, .2, 1); }
  .ms-site a.ms-cr__seal:hover, .ms-site a.ms-cr__seal:focus-visible { transform: scale(1.05); }
  .ms-cr__seal-ring { position: absolute; inset: 0; width: 100%; height: 100%; animation: msCrSeal 48s linear infinite; }
  .ms-cr__seal:hover .ms-cr__seal-ring { animation-play-state: paused; }
  .ms-cr__seal-ring text { font-size: 8px; font-weight: 500; letter-spacing: .12em; text-transform: uppercase; fill: #5E4A2E; font-family: inherit; }
  .ms-cr__seal-in { position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 2px; }
  .ms-site .ms-cr__seal-in img { width: 26%; height: auto; aspect-ratio: 1; object-fit: cover; object-position: 0 50%; filter: none !important; }
  .ms-cr__seal-in strong { font-family: Newsreader, Georgia, serif; font-weight: 300; font-size: clamp(17px, 1.5vw, 22px); letter-spacing: .02em; color: #17140F; line-height: 1; }
  @keyframes msCrSeal { to { transform: rotate(360deg); } }
  @media (prefers-reduced-motion: reduce) { .ms-cr__seal-ring { animation: none; } }
  @media (max-width: 760px) { .ms-site a.ms-cr__seal { top: -22px; left: 0; width: 78px; } .ms-cr__seal-in strong { font-size: 15px; } .ms-cr__seal-ring text { font-size: 8.6px; } }"""
_r26_sub(THEME + '/sections/ms-craft.liquid', [
    ('      <figure class="ms-cr__draw">\n', _SEAL),
    ('  .ms-cr__draw { margin: 0; }', _SEAL_CSS),
])

print('round 26: %d files changed' % _r26_n)
