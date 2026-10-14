# Round 18, run at the end of bin/build_more.py in its scope (THEME, SP, tpl_load, tpl_save...), after
# Round 17. Every step is guarded, so a second build changes nothing.
import re as _re
from PIL import Image as _Image

# Pictures at the width they are seen: a photograph chosen in the editor, or one of the theme's own, is
# offered at several widths (srcset), so a phone no longer downloads the 2,000 px picture a large
# screen needs. Shopify's CDN makes each width, and sends a lighter format where the browser takes one.
open(THEME + '/snippets/ms-srcset.liquid', 'w', encoding='utf-8').write("""{%- comment -%}
  The same picture at several widths, written as srcset (and sizes) attributes: the editor's image,
  else a photograph from the theme's assets, resized by Shopify's CDN. A full address, or a drawing,
  has no other widths, and then nothing is written.
  Usage: <img src="..." {% render 'ms-srcset', image: section.settings.image, fallback: section.settings.fallback, width: 2000, sizes: '100vw' %}>
{%- endcomment -%}
{%- liquid
  assign w = width | default: 1800 | plus: 0
  assign steps = '360,540,720,960,1200,1600,2000,2400' | split: ','
  assign out = ''
  if image != blank
    assign iw = image.width | default: w | plus: 0
    if iw < w
      assign w = iw
    endif
    for s in steps
      assign n = s | plus: 0
      if n < w
        assign u = image | image_url: width: n
        assign out = out | append: u | append: ' ' | append: n | append: 'w, '
      endif
    endfor
    assign u = image | image_url: width: w
    assign out = out | append: u | append: ' ' | append: w | append: 'w'
  elsif fallback != blank
    assign fb = fallback | downcase
    unless fb contains '/'
      if fb contains '.jpg' or fb contains '.jpeg' or fb contains '.png'
        for s in steps
          assign n = s | plus: 0
          if n < w
            assign sz = n | append: 'x'
            assign u = fallback | asset_img_url: sz
            assign out = out | append: u | append: ' ' | append: n | append: 'w, '
          endif
        endfor
        assign sz = w | append: 'x'
        assign u = fallback | asset_img_url: sz
        assign out = out | append: u | append: ' ' | append: w | append: 'w'
      endif
    endunless
  endif
  if out != blank
    echo ' srcset="' | append: out | append: '"'
    if sizes != blank
      echo ' sizes="' | append: sizes | append: '"'
    endif
  endif
-%}
""")

def _intrinsic(name):
    p = THEME + '/assets/' + name
    try:
        return _Image.open(p).size[0]
    except Exception:
        return None

def _src_value(tag):
    # the src attribute's value, read past any Liquid inside it
    i = tag.find(' src="')
    if i < 0:
        return None, None, None
    j = i + 6; k = j
    while k < len(tag):
        if tag.startswith('{{', k):
            k = tag.index('}}', k) + 2; continue
        if tag.startswith('{%', k):
            k = tag.index('%}', k) + 2; continue
        if tag[k] == '"':
            return tag[j:k], i, k + 1
        k += 1
    return None, None, None

_IMG = _re.compile(r'<img\b(?:[^>{]|\{\{.*?\}\}|\{%.*?%\})*>', _re.S)
_R_MSIMG = _re.compile(r"^\{%-?\s*render 'ms-img',\s*(.*?)\s*-?%\}$", _re.S)
_R_IFELSE = _re.compile(r"^\{%-?\s*if (\S+) != blank\s*-?%\}\{\{\s*\1\s*\|\s*image_url: width: (\d+)\s*\}\}\{%-?\s*else\s*-?%\}\{\{\s*'([^']+)'\s*\|\s*asset_url\s*\}\}\{%-?\s*endif\s*-?%\}$", _re.S)
_R_IFELSE_URL = _re.compile(r"^\{%-?\s*if (\S+) != blank\s*-?%\}\{\{\s*\1\s*\|\s*image_url: width: (\d+)\s*\}\}\{%-?\s*else\s*-?%\}[^{]*\{%-?\s*endif\s*-?%\}$", _re.S)
_R_IMGURL = _re.compile(r"^\{\{\s*([\w.\[\]']+)\s*\|\s*image_url: width: (\d+)\s*\}\}$")
_R_ASSET_LIT = _re.compile(r"^\{\{\s*'([^']+\.(?:jpe?g|png))'\s*\|\s*asset_url\s*\}\}$", _re.I)
_R_ASSET_VAR = _re.compile(r"^\{\{\s*([\w.\[\]]+)\s*\|\s*asset_url\s*\}\}$")

def _srcset_for(v):
    m = _R_MSIMG.match(v)
    if m:
        args = m.group(1)
        if 'width:' not in args:
            args += ', width: 1800'
        return "{% render 'ms-srcset', " + args + " %}"
    m = _R_IFELSE.match(v)
    if m:
        w = int(m.group(2)); iw = _intrinsic(m.group(3))
        return "{%% render 'ms-srcset', image: %s, fallback: '%s', width: %d %%}" % (m.group(1), m.group(3), w if not iw else max(360, min(w, iw)))
    m = _R_IFELSE_URL.match(v)
    if m:
        return "{%% render 'ms-srcset', image: %s, width: %s %%}" % (m.group(1), m.group(2))
    m = _R_IMGURL.match(v)
    if m and int(m.group(2)) >= 600:
        return "{%% render 'ms-srcset', image: %s, width: %s %%}" % (m.group(1), m.group(2))
    m = _R_ASSET_LIT.match(v)
    if m:
        iw = _intrinsic(m.group(1)) or 1600
        return "{%% render 'ms-srcset', fallback: '%s', width: %d %%}" % (m.group(1), min(iw, 2400))
    m = _R_ASSET_VAR.match(v)
    if m and 'logo' not in m.group(1):
        return "{%% render 'ms-srcset', fallback: %s, width: 1600 %%}" % m.group(1)
    return None

# where the picture is not the full width of the screen, the share of it, so the browser picks
# the right width: by the section file, then (optionally) a class on the img
_HALF = '(max-width: 760px) 90vw, 44vw'
_THIRD = '(max-width: 760px) 72vw, 29vw'
SIZES = {
    # measured at 390, 900 and 1440 px wide (Round 18)
    'ms-article': '(max-width: 760px) 32vw, 180px', 'ms-article-end': '(max-width: 760px) 32vw, 180px',
    'ms-article-rail': '(max-width: 760px) 72vw, (max-width: 1080px) 44vw, 31vw',
    'ms-beds-02': _HALF, 'ms-home-08': _HALF, 'ms-hosp-01': _HALF, 'ms-pro-01': _HALF, 'ms-image-pair': _HALF, 'ms-next-read': _HALF,
    'ms-collection-cards': _THIRD, 'ms-home-03': _THIRD, 'ms-home-14': _THIRD,
    'ms-collection-index': '(max-width: 760px) 90vw, (max-width: 1080px) 29vw, 17vw',
    'ms-compare': '(max-width: 760px) 30vw, 23vw',
    'ms-craft': '(max-width: 1080px) 70vw, 29vw',
    'ms-link-cards': '(max-width: 760px) 44vw, 21vw',
    'ms-lp-paisley': '(max-width: 1080px) 90vw, 46vw',
    'ms-lp-seasons': '(max-width: 760px) 95vw, 58vw',
    'ms-quiz': '(max-width: 760px) 100vw, 50vw',
    'ms-search': '(max-width: 760px) 44vw, 28vw',
    'ms-pro-04': {'ms-pd__big': '(max-width: 760px) 82vw, 39vw', 'ms-pd__inset': '(max-width: 760px) 47vw, 21vw'},
    # the menu's pictures, the journal's and Instagram's tiles, the cards drawn by snippets
    'ms-header': '(max-width: 760px) 60vw, 24vw', 'ms-mega': '(max-width: 760px) 60vw, 24vw', 'ms-mega-panel': '(max-width: 760px) 60vw, 24vw',
    'ms-follow': '(max-width: 760px) 50vw, 20vw', 'ms-cu-card': '(max-width: 760px) 50vw, 30vw',
    'ms-product-fallback': '(max-width: 760px) 100vw, 60vw',
    'ms-hp-chapter': {'s.image_2': '(max-width: 760px) 45vw, 24vw', '': '100vw'},
    'ms-footer': '(max-width: 760px) 70vw, 400px',
}
def _sizes_for(base, tag):
    sz = SIZES.get(base, '100vw')
    if isinstance(sz, dict):
        sz = next((v for k, v in sz.items() if k and k in tag), sz.get('', '100vw'))
    return sz

_r18_n = 0; _r18_files = set()
for _f in sorted(glob.glob(THEME + '/sections/ms-*.liquid') + glob.glob(THEME + '/snippets/ms-*.liquid') + glob.glob(THEME + '/blocks/*.liquid')):
    if _f.endswith('/ms-srcset.liquid') or _f.endswith('/ms-img.liquid'):
        continue
    _s = open(_f, encoding='utf-8').read()
    _base = os.path.basename(_f)[:-7]
    def _fix(m):
        global _r18_n
        tag = m.group(0)
        if "'ms-srcset'" in tag:
            # written by an earlier build: bring its sizes up to date
            sz = _sizes_for(_base, tag)
            t2 = _re.sub(r"(render 'ms-srcset',[^%]*?sizes: ')[^']*(')", lambda mm: mm.group(1) + sz + mm.group(2), tag)
            return t2
        if 'srcset' in tag:
            return tag
        v, a, b = _src_value(tag)
        if v is None:
            return tag
        ss = _srcset_for(v)
        if not ss:
            return tag
        if 'sizes=' not in tag:
            sz = _sizes_for(_base, tag)
            ss = ss[:-2].rstrip() + ", sizes: '%s' %%}" % sz
        _r18_n += 1; _r18_files.add(_base)
        return tag[:b] + ' ' + ss + tag[b:]
    _s2 = _IMG.sub(_fix, _s)
    if _s2 != _s:
        open(_f, 'w', encoding='utf-8').write(_s2)
print('pictures at their width: %d pictures in %d files' % (_r18_n, len(_r18_files)))

# The collection header's own photograph (Essentials, Icons) at its widths too
_p = THEME + '/sections/ms-collection-hero.liquid'
_s = open(_p, encoding='utf-8').read()
if 'tier_name' not in _s:
    for _n in ('ms-photo-glass-house.jpg', 'ms-graded-arches.jpg'):
        _a = "      assign tier_photo = '%s' | asset_url\n" % _n
        assert _s.count(_a) == 1, 'collection hero changed'
        _s = _s.replace(_a, "      assign tier_name = '%s'\n      assign tier_photo = tier_name | asset_url\n" % _n)
    _a = 'src="{{ tier_photo }}"'
    assert _s.count(_a) == 1, 'collection hero img changed'
    _s = _s.replace(_a, _a + " {% render 'ms-srcset', fallback: tier_name, width: 1920, sizes: '100vw' %}")
    open(_p, 'w', encoding='utf-8').write(_s)

# The home film's still, shown until the film plays: 1,600 px is enough for it
_p = THEME + '/sections/ms-home-01.liquid'
_s = open(_p, encoding='utf-8').read()
_a = "{{ section.settings.poster | image_url: width: 2400 }}"
if _a in _s:
    _s = _s.replace(_a, "{{ section.settings.poster | image_url: width: 1600 }}")
    open(_p, 'w', encoding='utf-8').write(_s)
print('collection header and home film still: lighter')

# Below the fold, the press marks and the footer's logo wait until they are near
for _n in ('ms-home-15', 'ms-footer'):
    _p = THEME + '/sections/%s.liquid' % _n
    if not os.path.exists(_p):
        continue
    _s = open(_p, encoding='utf-8').read()
    _s2 = _IMG.sub(lambda m: m.group(0) if 'loading=' in m.group(0) else m.group(0).replace('<img ', '<img loading="lazy" ', 1), _s)
    if _s2 != _s:
        open(_p, 'w', encoding='utf-8').write(_s2)
print('press marks and footer logo: lazy')

# Small text that was too light to read comfortably (WCAG AA, 4.5:1): each light grey or gold, where
# it colours words, darkened just enough, in the same hue, on the ivory and on the beige cards alike.
# Decorative numerals that screen readers skip, and the drawn marks, keep their lighter tone.
_AA = {'#9a8f7e': '#756b5c', '#8c8273': '#736b5f', '#a79c8a': '#766b59', '#b5aa97': '#776b55',
       '#a08b6c': '#7b6a50', '#8a7f6e': '#746b5d', '#9a6b4f': '#8d6248'}
_DECOR = ('.ms-art-toc a::before', '.ms-cn__n', '.ms-fa__n', '.ms-fa__mk', '.ms-sy__marks li')
_aa_n = 0
for _f in sorted(glob.glob(THEME + '/sections/ms-*.liquid') + glob.glob(THEME + '/snippets/ms-*.liquid')):
    _s = open(_f, encoding='utf-8').read()
    def _rule(m):
        global _aa_n
        sel, body = m.group(1), m.group(2)
        last = sel.strip().split('\n')[-1].strip()
        if any(d in last for d in _DECOR):
            return m.group(0)
        def _c(mm):
            global _aa_n
            _aa_n += 1
            return mm.group(1) + _AA[mm.group(2).lower()]
        body2 = _re.sub(r'(?<![-\w])(color\s*:\s*)(' + '|'.join(_AA) + r')\b', _c, body, flags=_re.I)
        return sel + '{' + body2 + '}'
    _s2 = _re.sub(r'([^{}]+)\{([^{}]*)\}', _rule, _s)
    if _s2 != _s:
        open(_f, 'w', encoding='utf-8').write(_s2)
print('small text darkened to read well: %d rules' % _aa_n)

# Accessibility (axe-core, every page on a phone and a computer)
def _patch(name, pairs, folder='sections'):
    p = THEME + '/%s/%s.liquid' % (folder, name)
    if not os.path.exists(p):
        return
    s = open(p, encoding='utf-8').read(); s0 = s
    for a, b, n in pairs:
        if b in s:
            continue  # done by an earlier build
        assert s.count(a) == n, '%s: %r found %d times' % (name, a[:60], s.count(a))
        s = s.replace(a, b)
    if s != s0:
        open(p, 'w', encoding='utf-8').write(s)

# the WhatsApp button inside a landmark, like everything else on the page
_patch('ms-whatsapp', [('<a class="ms-wa" ', '<aside class="ms-wa-wrap" aria-label="WhatsApp"><a class="ms-wa" ', 1),
                       ('  <span class="ms-wa__label">{{ settings.ms_whatsapp_label }}</span>\n</a>\n', '  <span class="ms-wa__label">{{ settings.ms_whatsapp_label }}</span>\n</a></aside>\n', 1)], 'snippets')
# product pages: the headings in order (title, then sections)
_p = THEME + '/sections/ms-product-reasons.liquid'
_s = open(_p, encoding='utf-8').read()
_s2 = _re.sub(r'<h3 (style="font-family: Newsreader[^"]*">\{\{ section\.settings\.t\d+ \}\})</h3>', r'<h2 \1</h2>', _s)
if _s2 != _s:
    open(_p, 'w', encoding='utf-8').write(_s2)
_patch('ms-product-main', [("'<h4 class=\"ms-desc__h\">' + g.head + '</h4>'", "'<h2 class=\"ms-desc__h\">' + g.head + '</h2>'", 1)])
# compare: the yes mark is an image with a name; column heads hold their links; the last row's head says what it is
_patch('ms-compare', [('<span class="ms-cmp__yes" aria-label="Yes"></span>', '<span class="ms-cmp__yes" role="img" aria-label="Yes"></span>', 1),
                      ('<span class="ms-cmp__no" aria-label="No">—</span>', '<span class="ms-cmp__no" role="img" aria-label="No">—</span>', 1),
                      ('<div class="ms-cmp__label" role="rowheader"></div>', '<div class="ms-cmp__label" role="rowheader"><span class="ms-visually-hidden">{{ s.view_label | default: s.eyebrow }}</span></div>', 1)])
_p = THEME + '/sections/ms-compare.liquid'
_s = open(_p, encoding='utf-8').read()
if '<a class="ms-cmp__col" href="{{ u }}" role="columnheader">' in _s:
    _i = _s.index('<a class="ms-cmp__col" href="{{ u }}" role="columnheader">')
    _j = _s.index('</a>', _i)
    _s = _s[:_i] + '<div class="ms-cmp__colh" role="columnheader"><a class="ms-cmp__col" href="{{ u }}">' + _s[_i + len('<a class="ms-cmp__col" href="{{ u }}" role="columnheader">'):_j] + '</a></div>' + _s[_j + 4:]
    _s = _s.replace('</style>', '  .ms-cmp__colh { display: contents; }\n</style>', 1)
    open(_p, 'w', encoding='utf-8').write(_s)
# the why table's empty corner says what its column is
_patch('ms-why', [('<span role="columnheader"></span>', '<span role="columnheader"><span class="ms-visually-hidden">{{ section.settings.us_label }} · {{ section.settings.them_label }}</span></span>', 1)])
# the Loro Piana cloth panel is a tab panel (a div; an article cannot be one)
_p = THEME + '/sections/ms-lp-fabrics.liquid'
_s = open(_p, encoding='utf-8').read()
if '<article class="ms-lf__fab' in _s:
    _s = _s.replace('<article class="ms-lf__fab', '<div class="ms-lf__fab').replace('</div></article>{%- endif -%}', '</div></div>{%- endif -%}')
    assert '<article' not in _s and '</article>' not in _s, 'lp fabrics: article left'
    open(_p, 'w', encoding='utf-8').write(_s)
# the gallery's sideways rail is a named region
_patch('ms-gallery', [('<div class="ms-gl__rail" data-ms="rail-x" tabindex="0" aria-label=', '<div class="ms-gl__rail" data-ms="rail-x" tabindex="0" role="region" aria-label=', 1)])
# each navigation named, so they can be told apart
_patch('ms-header', [('<nav data-ms="nav" style=', '<nav data-ms="nav" aria-label="{{ \'ms.product.aria_primary_nav\' | t }}" style=', 1)])
_patch('ms-systems', [('<nav class="ms-sy__pages">', '<nav class="ms-sy__pages" aria-label="{{ \'ms.product.aria_pages\' | t }}">', 1)])

# rows that scroll sideways on a phone: reachable from the keyboard, and named
_p = THEME + '/assets/ms-site.js'
_s = open(_p, encoding='utf-8').read()
if 'data-ms-kb' not in _s:
    _s += """
// rows that scroll sideways (on a phone): reachable from the keyboard, and named for screen readers
(function () {
  function mark() {
    document.querySelectorAll('[data-ms="rail"]').forEach(function (r) {
      var scrolls = r.scrollWidth > r.clientWidth + 2;
      if (scrolls && !r.hasAttribute('tabindex')) {
        r.setAttribute('tabindex', '0'); r.setAttribute('data-ms-kb', '');
        if (!r.getAttribute('role')) r.setAttribute('role', 'region');
        if (!r.getAttribute('aria-label')) { var sec = r.closest('section, .shopify-section'); var h = sec && sec.querySelector('h1, h2, h3'); r.setAttribute('aria-label', h ? h.textContent.trim().slice(0, 80) : document.title); }
      } else if (!scrolls && r.hasAttribute('data-ms-kb')) {
        r.removeAttribute('tabindex'); r.removeAttribute('data-ms-kb'); r.removeAttribute('role');
      }
    });
  }
  mark();
  window.addEventListener('resize', function () { clearTimeout(mark.t); mark.t = setTimeout(mark, 200); });
})();
"""
    open(_p, 'w', encoding='utf-8').write(_s)
print('accessibility: landmarks, headings, roles, names, keyboard rows')
