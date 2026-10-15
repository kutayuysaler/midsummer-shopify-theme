# Round 20, run at the end of bin/build_more.py in its scope (THEME, SP, tpl_load, tpl_save...), after
# Round 18. Every step is guarded, so a second build changes nothing.
import re as _re

# ── Sizes: every bed is made to measure, so the sizes are examples, all written the same way (width ×
#    length, in cm, narrowest first), and "Your size" draws any width and length, or a round bed, and asks
#    for it. The names (Single, Queen, King …) are gone: they read as a menu of fixed sizes.
_p = THEME + '/sections/ms-product-reasons.liquid'
_s = open(_p, encoding='utf-8').read()
if 'data-ms-szo' not in _s:
    _s = _s.replace('<section data-dc-tpl="764" ', '''{%- liquid
  # the round beds (Giotto) are drawn and asked for by their diameter alone, from the 2026 catalogue:
  # Giotto Round, Ø 225 and 245; the Giotto mattress, Ø 225; the Giotto bed, Ø 255
  assign ms_round = ''
  assign ms_ph = product.handle | default: ''
  if ms_ph contains 'giotto'
    if ms_ph contains 'round'
      assign ms_round = '225,245'
    elsif ms_ph == 'giotto-1' or ms_ph contains 'mattress'
      assign ms_round = '225'
    else
      assign ms_round = '255'
    endif
  endif
-%}
<section data-dc-tpl="764" data-ms-round="{{ ms_round }}" data-ms-title="{{ product.title | escape }}" ''', 1)
    _a = _s.index('<div data-ms="sizes"')
    _b = _s.index('<div class="ms-sz" data-ms-sz>')
    _s = _s[:_a] + """<div class="ms-szp">
<span class="ms-szp__k">{{ section.settings.sizes_label }}</span>
<div data-ms="sizes" class="ms-szp__row">
{%- if ms_round != '' -%}
  {%- assign ms_ds = ms_round | split: ',' -%}
  {%- for d in ms_ds -%}<button type="button" class="ms-szp__c" data-ms-size data-w="{{ d }}" data-l="{{ d }}" aria-pressed="false">Ø {{ d }}</button>{%- endfor -%}
{%- else -%}
{%- for i in (1..6) -%}
  {%- assign kw = 's' | append: i | append: '_w' -%}{%- assign kl = 's' | append: i | append: '_l' -%}
  {%- if section.settings[kw] != blank and section.settings[kl] != blank -%}<button type="button" class="ms-szp__c" data-ms-size data-w="{{ section.settings[kw] | escape }}" data-l="{{ section.settings[kl] | escape }}" aria-pressed="false">{{ section.settings[kw] }} × {{ section.settings[kl] }}</button>{%- endif -%}
{%- endfor -%}
{%- endif -%}
<button type="button" class="ms-szp__c ms-szp__own" data-ms-size-own aria-pressed="false" aria-controls="ms-szo-{{ section.id }}" aria-expanded="false">{{ section.settings.own_label }}</button>
</div>
</div>
""" + _s[_b:]
    # the custom size: width and length (or the diameter of a round bed), drawn as typed, then asked for
    _c = _s.index('<div class="ms-sz__txt">')
    _c = _s.index('</div>', _s.index('</div>', _c) + 6) + 6
    _s = _s[:_c] + """
<div class="ms-szo" id="ms-szo-{{ section.id }}" data-ms-szo hidden>
  {%- if ms_round != '' -%}
  <label class="ms-szo__f"><span>{{ section.settings.own_d }}</span><b><input type="number" inputmode="numeric" min="150" max="320" step="1" value="{{ ms_round | split: ',' | first }}" data-szo-w><i>cm</i></b></label>
  {%- else -%}
  <label class="ms-szo__f"><span>{{ section.settings.own_w }}</span><b><input type="number" inputmode="numeric" min="70" max="320" step="1" value="170" data-szo-w><i>cm</i></b></label>
  <label class="ms-szo__f"><span>{{ section.settings.own_l }}</span><b><input type="number" inputmode="numeric" min="150" max="320" step="1" value="210" data-szo-l><i>cm</i></b></label>
  {%- endif -%}
  <a class="ms-szo__cta" href="{% render 'ms-link', to: 'enquire', q: 'enquiry=proposal' %}#enquire" data-ms-enquire data-ms-enquiry="proposal" data-szo-cta>{{ section.settings.own_cta }}<span aria-hidden="true"> →</span></a>
</div>""" + _s[_c:]
    # the old fixed list of six, and its script, give way
    _s = _re.sub(r'<script type="application/json" data-ms-sizes-data>.*?</script>\n', '', _s, count=1, flags=_re.S)
    _a = _s.index('<script>\n(function () {\n  var root = document.currentScript.previousElementSibling.previousElementSibling;')
    _b = _s.index('</script>', _a) + len('</script>')
    _s = _s[:_a] + r"""<script>
(function () {
  var root = document.currentScript.previousElementSibling;
  var sz = root && root.querySelector && root.querySelector('[data-ms-sz]');
  if (!sz) return;
  var row = root.querySelector('[data-ms="sizes"]'), ownBtn = root.querySelector('[data-ms-size-own]'), form = root.querySelector('[data-ms-szo]');
  var title = root.getAttribute('data-ms-title') || '', ROUND = !!root.getAttribute('data-ms-round');
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  function fmt(w, l) { return ROUND ? 'Ø ' + Math.round(w) : Math.round(w) + ' × ' + Math.round(l); }
  // the sizes this product's own description lists, when it lists them: all written the same way
  var own = window.MS_SIZES;
  if (!ROUND && own && own.length > 1 && row) {
    own = own.slice().sort(function (a, b) { return a.w - b.w || a.l - b.l; });
    Array.prototype.slice.call(row.querySelectorAll('[data-ms-size]')).forEach(function (c) { c.parentNode.removeChild(c); });
    own.forEach(function (o) {
      var b = document.createElement('button');
      b.type = 'button'; b.className = 'ms-szp__c'; b.setAttribute('data-ms-size', ''); b.setAttribute('aria-pressed', 'false');
      b.setAttribute('data-w', o.w); b.setAttribute('data-l', o.l); if (o.note) b.setAttribute('data-note', o.note);
      b.textContent = fmt(o.w, o.l);
      row.insertBefore(b, ownBtn);
    });
    // said here, so not again among the facts at the top
    var dd = document.querySelector('[data-ms-dims]');
    var drow = dd && dd.closest('dl > div');
    if (drow && drow.parentNode) drow.parentNode.removeChild(drow);
  }
  var chips = Array.prototype.slice.call(row.querySelectorAll('[data-ms-size]'));
  var dims = chips.map(function (c) { return [+c.getAttribute('data-w') || 160, +c.getAttribute('data-l') || 200, c.getAttribute('data-note') || '']; });
  var big = dims.reduce(function (m, d) { return [Math.max(m[0], d[0]), Math.max(m[1], d[1])]; }, [0, 0]);
  if (!big[0]) big = [200, 200];
  var CX = 110, TOP = 14, cur = null, raf = 0;
  function q(sel) { return sz.querySelector(sel); }
  function box(el, x, y, w, h, r) { el.setAttribute('x', x.toFixed(1)); el.setAttribute('y', y.toFixed(1)); el.setAttribute('width', Math.max(0, w).toFixed(1)); el.setAttribute('height', Math.max(0, h).toFixed(1)); if (r !== undefined) { el.setAttribute('rx', r.toFixed(1)); el.setAttribute('ry', r.toFixed(1)); } }
  // c = [width, length, roundness 0..1]; the scale follows, so a large bed of your own still fits
  function paint(c) {
    var w = c[0], l = c[1], rd = c[2];
    var S = Math.min(150 / Math.max(big[0], w), 136 / Math.max(big[1], l));
    box(q('[data-sz-ref]'), CX - big[0] * S / 2, TOP, big[0] * S, big[1] * S, ROUND ? big[0] * S / 2 : 0);
    var W = w * S, L = l * S, x = CX - W / 2, y = TOP;
    box(q('[data-sz-rect]'), x, y, W, L, 2 + rd * (Math.min(W, L) / 2 - 2));
    q('[data-sz-turn]').setAttribute('d', rd > .5 ? '' : 'M' + (x + 3).toFixed(1) + ' ' + (y + L * .3).toFixed(1) + 'H' + (x + W - 3).toFixed(1));
    var two = w >= 120, inset = 6 + rd * W * .14, top = y + 6 + rd * L * .1;
    var pw = two ? (W - 2 * inset - 4) / 2 : W - 2 * inset, ph = Math.min(18, L * .12);
    box(q('[data-sz-p1]'), x + inset, top, pw, ph);
    box(q('[data-sz-p2]'), two ? x + W - inset - pw : x, top, two ? pw : 0, two ? ph : 0);
    var yb = y + L + 12, xr = x + W + 12;
    q('[data-sz-dw]').setAttribute('d', 'M' + x.toFixed(1) + ' ' + (yb - 4) + 'v8M' + x.toFixed(1) + ' ' + yb + 'H' + (x + W).toFixed(1) + 'M' + (x + W).toFixed(1) + ' ' + (yb - 4) + 'v8');
    q('[data-sz-dl]').setAttribute('d', rd > .5 ? '' : 'M' + (xr - 4).toFixed(1) + ' ' + y + 'h8M' + xr.toFixed(1) + ' ' + y + 'V' + (y + L).toFixed(1) + 'M' + (xr - 4).toFixed(1) + ' ' + (y + L).toFixed(1) + 'h8');
    var tw = q('[data-sz-tw]'), tl = q('[data-sz-tl]');
    tw.setAttribute('x', CX); tw.setAttribute('y', yb + 14); tw.textContent = (rd > .5 ? 'Ø ' : '') + Math.round(w);
    tl.setAttribute('x', xr + 13); tl.setAttribute('y', y + L / 2 + 4); tl.textContent = rd > .5 ? '' : Math.round(l);
  }
  function draw(to) {
    if (!cur || reduce) { cur = to; paint(to); return; }
    var from = cur.slice(), t0 = null; cancelAnimationFrame(raf);
    (function step(ts) {
      if (t0 === null) t0 = ts;
      var k = Math.min(1, (ts - t0) / 460), e = 1 - Math.pow(1 - k, 3);
      cur = [0, 1, 2].map(function (j) { return from[j] + (to[j] - from[j]) * e; });
      paint(cur);
      if (k < 1) raf = requestAnimationFrame(step); else cur = to;
    })(performance.now());
  }
  function say(name, fig) {
    var nm = root.querySelector('[data-ms-size-name]'); if (nm) nm.textContent = name;
    var fg = root.querySelector('[data-ms-size-figure]'); if (fg) { fg.textContent = fig; fg.hidden = !fig; }
  }
  function press(el) {
    chips.concat(ownBtn ? [ownBtn] : []).forEach(function (c) { c.setAttribute('aria-pressed', c === el ? 'true' : 'false'); });
  }
  function pick(i) {
    press(chips[i]);
    if (form) { form.hidden = true; if (ownBtn) ownBtn.setAttribute('aria-expanded', 'false'); }
    var d = dims[i] || [160, 200, ''];
    draw([d[0], d[1], ROUND ? 1 : 0]);
    say(fmt(d[0], d[1]) + ' cm', d[2]);
  }
  chips.forEach(function (c, k) { c.addEventListener('click', function () { pick(k); }); });
  // your size: as typed, kept within what can be drawn; a round bed has one measure, its diameter
  if (ownBtn && form) {
    var iw = form.querySelector('[data-szo-w]'), il = form.querySelector('[data-szo-l]'), cta = form.querySelector('[data-szo-cta]');
    var note = root.getAttribute('data-ms-own-note') || '';
    function clamp(v, a, b, dflt) { v = Math.round(+v); return isNaN(v) || !v ? dflt : Math.max(a, Math.min(b, v)); }
    function mine() {
      var w = clamp(iw.value, ROUND ? 150 : 70, 320, +iw.defaultValue), l = ROUND || !il ? w : clamp(il.value, 150, 320, 210);
      draw([w, l, ROUND ? 1 : 0]);
      var said = fmt(w, l) + ' cm';
      say(said, note);
      if (cta) cta.setAttribute('data-ms-note', (title ? title + ', ' : '') + said);
    }
    ownBtn.addEventListener('click', function () {
      press(ownBtn); form.hidden = false; ownBtn.setAttribute('aria-expanded', 'true'); mine();
      if (window.matchMedia('(hover: hover)').matches) iw.focus({ preventScroll: true });
    });
    [iw, il].filter(Boolean).forEach(function (el) { el.addEventListener('input', mine); el.addEventListener('change', mine); });
    [iw, il].filter(Boolean).forEach(function (el) { el.addEventListener('blur', function () { if (el.value !== '') el.value = clamp(el.value, +el.min, +el.max, +el.defaultValue); mine(); }); });
  }
  var start = 0;
  if (!ROUND) dims.forEach(function (d, k) { if (!start && d[0] >= 160 && d[0] <= 180) start = k; });
  if (chips.length) pick(start);
})();
</script>""" + _s[_b:]
    _s = _s.replace("<section data-dc-tpl=\"764\" data-ms-title=\"{{ product.title | escape }}\" ",
                    "<section data-dc-tpl=\"764\" data-ms-title=\"{{ product.title | escape }}\" data-ms-own-note=\"{{ section.settings.own_note | escape }}\" ", 1)
    _s = _s.replace("""      .ms-sz__fig { font-size: 12px; letter-spacing: .1em; font-variant-numeric: tabular-nums; color: #6E675C; }""",
                    """      .ms-sz__fig { font-size: 12px; letter-spacing: .1em; font-variant-numeric: tabular-nums; color: #6E675C; }
      .ms-szp { margin-top: 24px; }
      .ms-szp__k { display: block; font-size: 10px; letter-spacing: .24em; text-transform: uppercase; color: #6E675C; }
      .ms-szp__row { display: flex; flex-wrap: wrap; align-items: center; gap: 4px 18px; margin-top: 6px; }
      .ms-site .ms-szp__c { background: none; border: 0; border-bottom: 1px solid transparent; padding: 12px 0 6px; cursor: pointer; font-family: Newsreader, Georgia, serif; font-size: clamp(14px, 1.4vw, 17px); line-height: 1.3; white-space: nowrap; color: #6E675C; font-variant-numeric: tabular-nums; transition: color .2s, border-color .2s; }
      .ms-site .ms-szp__c:hover { color: #17140F; }
      .ms-site .ms-szp__c[aria-pressed="true"] { color: #17140F; border-bottom-color: #17140F; }
      .ms-site .ms-szp__own { font-style: italic; color: #7E623B; border-bottom: 1px dashed rgba(126, 98, 59, .55); }
      .ms-site .ms-szp__own::before { content: '+ '; font-style: normal; }
      .ms-site .ms-szp__own[aria-pressed="true"] { color: #17140F; border-bottom: 1px solid #17140F; }
      .ms-szo { display: flex; flex-wrap: wrap; align-items: flex-end; gap: 12px 18px; margin-top: 16px; padding-top: 14px; border-top: 1px solid rgba(23, 20, 15, .12); }
      .ms-szo[hidden], .ms-szo [hidden] { display: none; }
      .ms-szo__f { display: grid; gap: 4px; font-size: 10px; letter-spacing: .2em; text-transform: uppercase; color: #6E675C; }
      .ms-szo__f input { width: 64px; padding: 6px 0 4px; border: 0; border-bottom: 1px solid #17140F; background: transparent; font-family: Newsreader, Georgia, serif; font-size: 20px; letter-spacing: 0; color: #17140F; font-variant-numeric: tabular-nums; -moz-appearance: textfield; }
      .ms-szo__f input::-webkit-outer-spin-button, .ms-szo__f input::-webkit-inner-spin-button { -webkit-appearance: none; margin: 0; }
      .ms-szo__f input:focus-visible { outline: 1px solid #7E623B; outline-offset: 4px; }
      .ms-szo__f b { display: inline-flex; align-items: baseline; gap: 6px; font-weight: 400; }
      .ms-szo__f i { font-style: normal; font-size: 12px; letter-spacing: .06em; text-transform: none; color: #6E675C; }
      .ms-site a.ms-szo__cta { display: inline-flex; align-items: center; min-height: 40px; font-size: 10.5px; letter-spacing: .22em; text-transform: uppercase; color: #17140F; border-bottom: 1px solid #17140F; }
      .ms-szo__cta span { margin-left: 8px; }""", 1)
    # the settings: six names out (the sizes now say themselves), the words for "Your size" in
    _j0 = _s.index('{% schema %}') + len('{% schema %}')
    _j1 = _s.index('{% endschema %}')
    _d = json.loads(_s[_j0:_j1])
    _d['settings'] = [x for x in _d['settings'] if x.get('id') not in ('t4', 't5', 't6', 't7', 't8', 't9')]
    _at = next(i for i, x in enumerate(_d['settings']) if x.get('id') == 's1_w')
    _d['settings'][_at:_at] = [
        {'type': 'header', 'content': 'Sizes'},
        {'type': 'paragraph', 'content': 'Every bed is made to measure: the sizes below are examples, shown as width × length in cm. A product that lists its own sizes in its description shows those instead.'},
        {'type': 'text', 'id': 'sizes_label', 'label': 'Above the sizes', 'default': 'For example, in cm'},
        {'type': 'text', 'id': 'own_label', 'label': 'Your own size', 'default': 'Your size'},
        {'type': 'text', 'id': 'own_w', 'label': 'Your size: width', 'default': 'Width'},
        {'type': 'text', 'id': 'own_l', 'label': 'Your size: length', 'default': 'Length'},
        {'type': 'text', 'id': 'own_d', 'label': 'Your size: diameter (Giotto)', 'default': 'Diameter'},
        {'type': 'text', 'id': 'own_note', 'label': 'Your size: said under it', 'default': 'Made to your measure'},
        {'type': 'text', 'id': 'own_cta', 'label': 'Your size: ask for it', 'default': 'Ask for this size'},
    ]
    _s = _s[:_j0] + '\n' + json.dumps(_d, indent=2, ensure_ascii=False) + '\n' + _s[_j1:]
    open(_p, 'w', encoding='utf-8').write(_s)
# the templates kept no values for the six names; any that did would point at settings that are gone
for _f in glob.glob(THEME + '/templates/product*.json'):
    _h, _d = tpl_load(os.path.basename(_f))
    _ch = False
    for _v in _d.get('sections', {}).values():
        if _v.get('type') == 'ms-product-reasons':
            for _k in ('t4', 't5', 't6', 't7', 't8', 't9'):
                if _k in _v.get('settings', {}):
                    del _v['settings'][_k]; _ch = True
    if _ch:
        tpl_save(os.path.basename(_f), _h, _d)
print('sizes: examples in cm, and your own size, drawn')

# the sizes guide (Questions page): any size, made to measure; the usual ones only for reference
for _f in ('page.faq.json', 'collection.ms-faq.json'):
    if not os.path.exists(THEME + '/templates/' + _f):
        continue
    _h, _d = tpl_load(_f)
    _ch = False
    for _v in _d.get('sections', {}).values():
        _st = _v.get('settings', {})
        if _v.get('type') == 'ms-guide' and _st.get('heading') == 'Standard sizes, and every other.':
            _st['heading'] = 'Any size, made to measure.'
            _st['text'] = 'For reference, the usual bed sizes and their names, in centimetres and inches. Any width, length or shape, round included, is made to order.'
            _ch = True
    if _ch:
        tpl_save(_f, _h, _d)

# ── Instagram: no stand-in photographs. The row is the account's latest posts (a feed, or an Instagram
#    app's block), or nothing; the templates keep no photographs for it
for _f in glob.glob(THEME + '/templates/*.json'):
    _h, _d = tpl_load(os.path.basename(_f))
    _ch = False
    for _v in _d.get('sections', {}).values():
        if _v.get('type') == 'ms-follow':
            for _k in ['image_%d' % i for i in range(1, 6)]:
                if _k in _v.get('settings', {}):
                    del _v['settings'][_k]; _ch = True
    if _ch:
        tpl_save(os.path.basename(_f), _h, _d)
for _f in glob.glob(THEME + '/sections/*-group.json'):
    _t = open(_f, encoding='utf-8').read()
    if '"ms-follow"' in _t and '"image_1"' in _t:
        print('note: a section group keeps Instagram photographs:', os.path.basename(_f))
print('instagram: live posts or nothing')
