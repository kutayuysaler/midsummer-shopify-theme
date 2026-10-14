# Round 17, run at the end of bin/build_more.py in its scope (THEME, SP, tpl_load, tpl_save...), after
# Round 16. Every step is guarded, so a second build changes nothing.

# the house's new photographs (vendor/r17): copied as they are
for _f in sorted(glob.glob(SP + '/vendor/r17/*.jpg')):
    shutil.copy(_f, THEME + '/assets/' + os.path.basename(_f))

# Inside the bed: a part photograph no card uses any more leaves the package
_keep = set(os.path.basename(_f) for _f in glob.glob(SP + '/vendor/r16/parts/ms-part-*.jpg'))
for _f in glob.glob(THEME + '/assets/ms-part-*.jpg'):
    if os.path.basename(_f) not in _keep:
        os.remove(_f)

# Handmade in Italy, 'Slow, by method': the artisan cutting the cloth by hand, and a finished corner,
# every tuft tied and the border stitched by hand
for _name in ('page.handmade-in-italy.json', 'collection.ms-handmade.json'):
    if not os.path.exists(THEME + '/templates/' + _name):
        continue
    _h, _d = tpl_load(_name)
    _ch = False
    for _sec in _d['sections'].values():
        _st = _sec.get('settings') or {}
        if _sec.get('type') == 'ms-image-pair' and _st.get('heading') == 'Slow, by method.' and _st.get('fallback_1') != 'ms-photo-artisan-cutting.jpg':
            _st.update({'fallback_1': 'ms-photo-artisan-cutting.jpg', 'caption_1': 'The cloth, cut by hand by our artisans.',
                        'fallback_2': 'ms-photo-lp-roma-corner.jpg', 'caption_2': 'Every tuft tied by hand, every border stitched by hand.'})
            _ch = True
    if _ch:
        tpl_save(_name, _h, _d)
print('handmade: slow, by method, in two new photographs')

# The portfolio (the journal called projects or portfolio) carries the professionals' bar, like the
# other two pages it names
_h, _d = tpl_load('blog.json')
if 'pronav' not in _d['sections']:
    _d['sections']['pronav'] = {'type': 'ms-pro-nav', 'settings': {'current': 'portfolio'}}
    _d['order'].insert(0, 'pronav')
    tpl_save('blog.json', _h, _d)
print('professionals: the bar on the portfolio too')

# The size drawing on a product page: the piece's own sizes when its description lists them (read by
# the description's script into window.MS_SIZES), each with what goes with it; the specifications then
# say the sizes in one line and point here
_p = THEME + '/sections/ms-product-reasons.liquid'
_s = open(_p, encoding='utf-8').read()
if 'MS_SIZES' not in _s:
    _a = "  var sz = root.querySelector('[data-ms-sz]'), cur = null, raf = 0;\n"
    assert _s.count(_a) == 1, 'reasons script changed'
    _s = _s.replace(_a, _a + """  var own = window.MS_SIZES;
  function esc(t) { return String(t).replace(/[&<>"]/g, function (c) { return ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[c]; }); }
  if (own && own.length > 1 && chips.length) {
    var holder = chips[0].parentNode, proto = chips[0].cloneNode(false);
    Array.prototype.forEach.call(chips, function (c) { c.parentNode.removeChild(c); });
    dims = own.map(function (o) { return [o.w, o.l, o.note]; });
    own.forEach(function (o) { var b = proto.cloneNode(false); b.textContent = o.name || (o.w + ' × ' + o.l); holder.appendChild(b); });
    chips = holder.querySelectorAll('[data-ms-size]');
    if (!root.id) root.id = 'ms-sizes';
    var dd = document.querySelector('[data-ms-dims]'), dbox = document.querySelector('[data-ms-desc]');
    if (dd) {
      var ln = (dbox && dbox.getAttribute('data-l-sizes')) || '[n] sizes', see = (dbox && dbox.getAttribute('data-l-see')) || 'See each size, drawn';
      var keep = Array.prototype.filter.call(dd.querySelectorAll('p'), function (p) { return !/\\d\\s*[×x]\\s*\\d/.test(p.textContent); }).map(function (p) { return p.outerHTML; }).join('');
      dd.innerHTML = '<p>' + esc(ln.replace('[n]', own.length)) + ': ' + own.map(function (o) { return esc(o.name || (o.w + ' × ' + o.l)); }).join(' · ') + '</p>' + keep +
        '<p class="ms-pm__tosizes"><a href="#' + root.id + '">' + esc(see) + ' ↓</a></p>';
    }
  }
""", 1)
    _b = "    var fg = root.querySelector('[data-ms-size-figure]'); if (fg) fg.textContent = d[0] + ' × ' + d[1] + ' cm';"
    assert _s.count(_b) == 1, 'reasons figure changed'
    _s = _s.replace(_b, "    var fg = root.querySelector('[data-ms-size-figure]'); if (fg) fg.textContent = d[0] + ' × ' + d[1] + ' cm' + (d[2] ? ' · ' + d[2] : '');")
    _c = "  var start = 0; chips.forEach(function (c, k) { if (c.textContent.trim() === 'Small Double') start = k; });"
    assert _s.count(_c) == 1, 'reasons start changed'
    _s = _s.replace(_c, "  var start = 0; chips.forEach(function (c, k) { if (c.textContent.trim() === 'Small Double') start = k; });\n"
                        "  if (own && own.length > 1) { start = 0; dims.forEach(function (d, k) { if (!start && +d[0] >= 160 && +d[0] <= 180) start = k; }); }")
    open(_p, 'w', encoding='utf-8').write(_s)
print('product: the sizes said once, drawn one by one')

# the collections' register is gone; its cloth cuts with it
_cs = THEME + '/snippets/ms-cloth-swatch.liquid'
if os.path.exists(_cs):
    _used = any("'ms-cloth-swatch'" in open(_f, encoding='utf-8', errors='ignore').read()
                for _f in glob.glob(THEME + '/sections/*.liquid') + glob.glob(THEME + '/snippets/*.liquid') + glob.glob(THEME + '/blocks/*.liquid'))
    if not _used:
        os.remove(_cs)
print('collections: an even grid')
