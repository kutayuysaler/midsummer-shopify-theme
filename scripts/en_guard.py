"""The values that are not language, kept as the theme was built: snippets/ms-en-map.liquid.

Translate & Adapt can save a translation for any text setting of a template, and its machine
translation does not stop at words: a photograph's file name, a blog's address, a map position, a
handle, a "yes" in the comparison table or a publication's name come back changed, and in Italian
or Russian the page then shows a broken picture, a Liquid error, a link to nothing or a wrong
pin. The settings listed in PROTECT are read through snippets/ms-en.liquid, which, outside the
shop's main language, uses the value written here instead of the one Translate & Adapt holds
(a file of the theme's own chosen later in the editor is kept).

For every JSON template (and section group) this writes, under the template's name,
  ¦<section key>/<block id or ->/<setting id>=<value>¦ …
and, under 'assets', the theme's own file names. It also checks that every text setting in the
templates that holds a file, an address, a number or a key is either protected or waived on
purpose, so a new one cannot slip through unguarded.

usage: python3 -I scripts/en_guard.py [THEME_DIR]   (default: theme/ next to this folder)"""
import glob, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
THEME = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), 'theme')

# (section type, block type or None, setting id): 'f' = a file of the theme (a later choice of
# another of the theme's files is kept), 'v' = always the built value.
PROTECT = {
    ('ms-lp-fabrics', 'colour', 'image_fallback'): 'f',
    ('ms-lp-fabrics', 'colour', 'large_fallback'): 'f',
    ('ms-lp-fabrics', 'colour', 'name'): 'v',
    ('ms-lp-fabrics', 'fabric', 'image_fallback'): 'f',
    ('ms-lp-fabrics', 'fabric', 'anchor'): 'v',
    ('ms-lp-fabrics', 'fabric', 'name'): 'v',
    ('ms-gallery', 'photo', 'image_fallback'): 'f',
    ('ms-gallery', 'photo', 'ratio'): 'v',
    ('ms-stockists', 'place', 'name'): 'v',
    ('ms-stockists', 'place', 'lat'): 'v',
    ('ms-stockists', 'place', 'lon'): 'v',
    ('ms-stockists', 'place', 'website'): 'v',
    ('ms-stockists', 'place', 'phone'): 'v',
    ('ms-stockists', 'place', 'email'): 'v',
    ('ms-sizes', 'system', 'handle'): 'v',
    ('ms-fibre-atlas', 'fibre', 'points'): 'v',
    ('ms-fibre-atlas', 'fibre', 'qualities'): 'v',
    ('ms-fibre-atlas', 'fibre', 'microns'): 'v',
    ('ms-fibre-atlas', 'fibre', 'f1'): 'v',
    ('ms-fibre-atlas', 'fibre', 'f2'): 'v',
    ('ms-fibre-atlas', 'fibre', 'f3'): 'v',
    ('ms-fibre-atlas', 'fibre', 'species'): 'v',
    ('ms-press-blog', 'publication', 'link'): 'v',
    ('ms-press-blog', 'publication', 'logo_file'): 'f',
    ('ms-press-blog', 'publication', 'name'): 'v',
    ('ms-hp-proof', None, 'award_logo'): 'f',
    ('ms-hp-proof', 'publication', 'logo_file'): 'f',
    ('ms-hp-proof', 'publication', 'name'): 'v',
    ('ms-hp-proof', 'publication', 'when'): 'v',
    ('ms-qa', None, 'anchor'): 'v',
    ('ms-guide', None, 'anchor'): 'v',
    ('ms-guide', 'point', 'w'): 'v',
    ('ms-guide', 'point', 'l'): 'v',
    ('ms-night', 'hour', 'time'): 'v',
    ('ms-figures', 'figure', 'number'): 'v',
    ('ms-compare', 'row', 'v1'): 'v',
    ('ms-compare', 'row', 'v2'): 'v',
    ('ms-compare', 'row', 'v3'): 'v',
    ('ms-collection-cards', 'collection', 'handle'): 'v',
    ('ms-collection-cards', 'collection', 'image_fallback'): 'f',
    ('ms-article-rail', None, 'blog_handle'): 'v',
    ('ms-article-rail', None, 'tag'): 'v',
    ('ms-banner', None, 'image_fallback'): 'f',
    ('ms-banner', None, 'image_fallback_mobile'): 'f',
    ('ms-banner', None, 'product_handle'): 'v',
    ('ms-lp-paisley', None, 'image_fallback'): 'f',
    ('ms-lp-paisley', None, 'cloth1_fallback'): 'f',
    ('ms-lp-paisley', None, 'cloth2_fallback'): 'f',
    ('ms-lp-paisley', None, 'detail_fallback'): 'f',
    ('ms-lp-paisley', None, 'product_handle'): 'v',
    ('ms-hp-chapter', None, 'image_fallback'): 'f',
    ('ms-hp-chapter', None, 'image_2_fallback'): 'f',
    ('ms-hp-chapter', None, 'image_fallback_mobile'): 'f',
    ('ms-hp-chapter', None, 'numeral'): 'v',
    ('ms-hp-chapter', None, 'stat1_value'): 'v',
    ('ms-hp-chapter', None, 'stat2_value'): 'v',
    ('ms-hp-chapter', None, 'stat3_value'): 'v',
    ('ms-lp-seasons', None, 'winter_fallback'): 'f',
    ('ms-lp-seasons', None, 'summer_fallback'): 'f',
    ('ms-link-cards', 'card', 'image_fallback'): 'f',
    ('ms-process', 'step', 'image_fallback'): 'f',
    ('ms-image-pair', None, 'fallback_1'): 'f',
    ('ms-image-pair', None, 'fallback_2'): 'f',
}
# url settings: Shopify resolves them itself (shopify://… addresses become the page's address).
WAIVE_TYPES = {'url'}

strip = lambda s: re.sub(r'\A\s*/\*.*?\*/', '', s, flags=re.S)


def kind(v):
    if not isinstance(v, str) or not v.strip():
        return None
    v = v.strip()
    if re.search(r'\.(jpe?g|png|svg|webp|gif|mp4|webm|pdf|json)$', v, re.I):
        return 'file'
    if re.match(r'^(/|https?:|shopify:|#|mailto:|tel:|//)', v):
        return 'link'
    if re.fullmatch(r'[-\d.,;:|\s/x%]+', v):
        return 'number'
    if re.fullmatch(r'[a-z0-9_\-:,.|]+', v):
        return 'key'
    return None


types = {}
for f in glob.glob(os.path.join(THEME, 'sections', '*.liquid')):
    src = open(f, encoding='utf-8').read()
    m = re.search(r'{%-?\s*schema\s*-?%}(.*?){%-?\s*endschema', src, re.S)
    if not m:
        continue
    sch = json.loads(m.group(1))
    n = os.path.basename(f)[:-7]
    types[(n, None)] = {x['id']: x['type'] for x in sch.get('settings', []) if 'id' in x}
    for b in sch.get('blocks', []):
        types[(n, b.get('type'))] = {x['id']: x['type'] for x in b.get('settings', []) if 'id' in x}

maps, loose = {}, []


def take(tk, key, bid, stype, btype, settings):
    for sid, v in (settings or {}).items():
        p = PROTECT.get((stype, btype, sid))
        t = types.get((stype, btype), {}).get(sid)
        if p and isinstance(v, str) and v != '':
            assert '¦' not in v and '{{' not in v and '{%' not in v and '\n' not in v, (tk, key, sid, v)
            maps.setdefault(tk, []).append('%s/%s/%s=%s' % (key, bid or '-', sid, v))
        elif not p and t and t not in WAIVE_TYPES and t in ('text', 'textarea') and kind(v):
            loose.append((tk, stype, btype, sid, v))


for f in sorted(glob.glob(os.path.join(THEME, 'templates', '*.json'))):
    tk = os.path.basename(f)[:-5]
    d = json.loads(strip(open(f, encoding='utf-8').read()))
    for key, sec in (d.get('sections') or {}).items():
        take(tk, key, None, sec.get('type'), None, sec.get('settings'))
        for bid, b in (sec.get('blocks') or {}).items():
            take(tk, key, bid, sec.get('type'), b.get('type'), b.get('settings'))
seen = set()
for f in sorted(glob.glob(os.path.join(THEME, 'sections', '*.json'))):
    d = json.loads(strip(open(f, encoding='utf-8').read()))
    for key, sec in (d.get('sections') or {}).items():
        assert key not in seen, ('section key used in two groups', key)
        seen.add(key)
        take('group', key, None, sec.get('type'), None, sec.get('settings'))
        for bid, b in (sec.get('blocks') or {}).items():
            take('group', key, bid, sec.get('type'), b.get('type'), b.get('settings'))

# a value that is not language but is neither protected nor known to be harmless: say so
HARMLESS = {
    ('ms-stockists', 'place', 'city'), ('ms-stockists', 'place', 'country'), ('ms-stockists', 'place', 'address'),
    ('ms-fibre-atlas', 'fibre', 'name'), ('ms-sizes', 'system', 'height'),
}
loose = [x for x in loose if (x[1], x[2], x[3]) not in HARMLESS]
if loose:
    for x in loose[:40]:
        print('UNGUARDED', x)
    sys.exit('%d template values hold a file, an address, a number or a key and are not guarded' % len(loose))

assets = sorted(os.listdir(os.path.join(THEME, 'assets')))
assert all('¦' not in a for a in assets)
out = ['{%- comment -%}',
       '  Written by scripts/en_guard.py: the value each protected setting was built with, per template',
       '  (¦section/block/setting=value¦), and the theme\'s own files. Read by snippets/ms-en.liquid.',
       '{%- endcomment -%}',
       '{%- case tk -%}']
groups = {}
for tk in sorted(maps):
    groups.setdefault('¦' + '¦'.join(maps[tk]) + '¦', []).append(tk)
for body, tks in sorted(groups.items(), key=lambda x: x[1][0]):
    out.append('{%- when ' + ', '.join("'%s'" % t for t in tks) + ' -%}' + body)
out.append("{%- when 'assets' -%}¦" + '¦'.join(assets) + '¦')
out.append('{%- endcase -%}')
dst = os.path.join(THEME, 'snippets', 'ms-en-map.liquid')
open(dst, 'w', encoding='utf-8').write('\n'.join(out) + '\n')
n = sum(len(v) for v in maps.values())
print('ms-en-map: %d values in %d templates, %d files; %d bytes' % (n, len(maps), len(assets), os.path.getsize(dst)))
json.dump([[a, b, c] for (a, b, c) in PROTECT], open(os.path.join(HERE, 'en_guard_protect.json'), 'w'))
