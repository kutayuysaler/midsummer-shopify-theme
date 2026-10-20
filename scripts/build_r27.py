# Round 27, run at the end of bin/build_more.py in its scope (THEME, tpl_load, tpl_save, and Round 26's
# _SEAL, _SEAL_CSS ...), after Round 26. Every step is an exact replacement or a guarded write, so a second
# build changes nothing.
#  · Top: the Green Product Award no longer a turning seal, but a quiet label above the drawing: the
#    award's own mark, its name, Berlin · 2025, and the way to the award's page.
#  · Sleep Culture: the rooms kept for rest, each photograph a different room or moment.

_r27_n = 0


def _r27_sub(path, pairs):
    global _r27_n
    _t = open(path, encoding='utf-8').read()
    _u = _t
    for _a, _b in pairs:
        if _a in _u:
            _u = _u.replace(_a, _b)
        else:
            assert _b in _u, (path, _a[:80])
    if _u != _t:
        open(path, 'w', encoding='utf-8').write(_u)
        _r27_n += 1


def _r27_copy(src, dst):
    global _r27_n
    if not os.path.exists(dst) or open(src, 'rb').read() != open(dst, 'rb').read():
        shutil.copy(src, dst)
        _r27_n += 1


# ── Top: the award as a label above the drawing, in the house's own type; nothing turns
_SEAL_A = _SEAL[_SEAL.index('        {%- if cr_award -%}'):]
_LABEL = """        {%- if cr_award -%}
          <a class="ms-cr__award" href="https://www.gp-award.com/en/produkte/top-bed-system" target="_blank" rel="noopener" aria-label="{% capture ms_t_out %}{% render 'ms-t', v: 'Green Product Award 2025' %}{% endcapture %}{{ ms_t_out | strip | escape }}">
            <span class="ms-cr__award-mk" aria-hidden="true"><img src="{{ 'ms-press-green-product-award.svg' | asset_url }}" alt="" width="137" height="32" loading="lazy"></span>
            <span class="ms-cr__award-t" aria-hidden="true"><span class="ms-cr__award-n">Green Product Award</span><span class="ms-cr__award-y">{% render 'ms-t', v: 'Berlin · 2025' %}</span></span>
            <span class="ms-cr__award-go" aria-hidden="true">↗</span>
          </a>
        {%- endif -%}
"""
_SEAL_C = _SEAL_CSS[_SEAL_CSS.index("  /* Round 26: the Green Product Award's seal on Inside Top */"):]
_LABEL_CSS = """  /* Round 27: the Green Product Award, a quiet label above the drawing of Inside Top */
  .ms-cr__draw { position: relative; }
  .ms-site a.ms-cr__award { position: relative; z-index: 1; display: flex; width: max-content; max-width: 100%; align-items: center; gap: 14px; margin: 0 0 -4% 6%; padding: 10px 16px 10px 12px; color: #17140F; text-decoration: none; background: rgba(251, 249, 245, .42); border: 1px solid rgba(126, 98, 59, .24); transition: border-color .4s, background-color .4s; }
  .ms-site a.ms-cr__award:hover, .ms-site a.ms-cr__award:focus-visible { border-color: rgba(126, 98, 59, .58); background: rgba(251, 249, 245, .72); }
  .ms-cr__award-mk { width: 32px; height: 32px; overflow: hidden; flex: 0 0 auto; }
  .ms-site .ms-cr__award-mk img { width: auto; height: 32px; max-width: none; display: block; filter: none !important; }
  .ms-cr__award-t { display: grid; gap: 5px; padding-left: 14px; border-left: 1px solid rgba(126, 98, 59, .28); line-height: 1; }
  .ms-cr__award-n { font-family: Newsreader, Georgia, serif; font-weight: 300; font-size: 17px; letter-spacing: .005em; }
  .ms-cr__award-y { font-size: 9.5px; letter-spacing: .24em; text-transform: uppercase; color: #7E623B; }
  .ms-cr__award-go { align-self: flex-start; margin-left: 4px; font-size: 11px; line-height: 1; color: #7E623B; opacity: .55; transition: opacity .4s, transform .4s; }
  .ms-site a.ms-cr__award:hover .ms-cr__award-go, .ms-site a.ms-cr__award:focus-visible .ms-cr__award-go { opacity: 1; transform: translate(2px, -2px); }
  @media (max-width: 760px) { .ms-site a.ms-cr__award { gap: 12px; padding: 9px 14px 9px 10px; } .ms-cr__award-t { padding-left: 12px; } .ms-cr__award-n { font-size: 16px; } }"""
_r27_sub(THEME + '/sections/ms-craft.liquid', [
    (_SEAL_A, _LABEL),
    (_SEAL_C, _LABEL_CSS),
])
_u = open(THEME + '/sections/ms-craft.liquid', encoding='utf-8').read()
assert 'ms-cr__seal' not in _u and 'msCrSeal' not in _u and _u.count('class="ms-cr__award"') == 1, 'award label'

# ── Sleep Culture: the rooms kept for rest, from the house's palazzo shoot (scripts/gallery_photos_r27.py),
#    a different room or moment in each and none shown elsewhere; the Via Andegari pictures stay on the
#    atelier's page alone. Two even rows: the wide bed by the glass leads, the late light opens the second.
for _f in sorted(glob.glob(SP + '/vendor/r27/*.jpg')):
    _r27_copy(_f, THEME + '/assets/' + os.path.basename(_f))
_R27_SLEEP = [
    ('ms-photo-sleep-glass.jpg', 'Morning by the glass, beside a lemon tree.'),
    ('ms-photo-sleep-tea.jpg', 'Tea and a book on the windowsill.'),
    ('ms-photo-sleep-throws.jpg', 'Throws folded by the window.'),
    ('ms-photo-sleep-late-light.jpg', 'Late light across the pillows.'),
    ('ms-photo-sleep-tulips.jpg', 'Two low tables and a few tulips.'),
    ('ms-photo-sleep-woven-throw.jpg', 'A woven throw at the foot of the bed.')]
for _name in sorted(os.listdir(THEME + '/templates')):
    if not _name.endswith('.json') or 'sleep-culture' not in _name:
        continue
    _h, _d = tpl_load(_name)
    _sec = _d.get('sections', {}).get('rooms')
    if not _sec or _sec.get('type') != 'ms-gallery':
        continue
    _bl = {'p%02d' % _i: {'type': 'photo', 'settings': {'image_fallback': _f, 'caption': _c, 'ratio': _r26_ratio(_f)}}
           for _i, (_f, _c) in enumerate(_R27_SLEEP, 1)}
    if _sec.get('blocks') != _bl or _sec.get('block_order') != sorted(_bl):
        _sec['blocks'], _sec['block_order'] = _bl, sorted(_bl)
        tpl_save(_name, _h, _d)
        _r27_n += 1
# the Round 25 and 26 rooms, now shown nowhere: out of the theme (their sources stay in vendor/)
for _f in ('ms-photo-sleep-made-up.jpg', 'ms-photo-sleep-turned-down.jpg', 'ms-photo-sleep-pillows.jpg',
           'ms-photo-sleep-blanket.jpg', 'ms-photo-sleep-bedside.jpg', 'ms-photo-sleep-armchair.jpg'):
    for _t in glob.glob(THEME + '/*/*'):
        if os.path.isfile(_t) and not _t.endswith('/' + _f) and _f in open(_t, encoding='utf-8', errors='ignore').read():
            raise AssertionError((_f, _t))
    if os.path.exists(THEME + '/assets/' + _f):
        os.remove(THEME + '/assets/' + _f)
        _r27_n += 1

print('round 27: %d files changed' % _r27_n)
