"""Every template setting as the theme was built, for Italian and Russian.

Translate & Adapt can save a translation for any text setting of a template. Its machine translation
replaces the theme's own Italian and Russian (Book became «Libro», Press «Premere») and does not stop
at words: a photograph's file, a blog's address, a map position or a publication's name come back
changed, and the page shows a broken picture, a Liquid error, a link to nothing or a wrong pin.

So each setting a template holds is written into the theme under its place (section/block/setting,
per template):
  - snippets/ms-en-map.liquid: the settings that are not language (PROTECT: files, addresses,
    positions, handles, names never translated), as built. snippets/ms-en.liquid uses them outside
    the shop's main language, whatever Translate & Adapt holds (a file of the theme's own chosen
    later in the editor is kept);
  - snippets/ms-tx-map.liquid: every other text, by the fingerprint of the English it was built with.
    When the value ms-t.liquid is handed has no translation of its own (Translate & Adapt replaced
    it), ms-t shows the theme's translation of the built English instead. A text the theme leaves
    as it is (a name, an address) is given a translation equal to itself (locales ms_tx), so a
    machine translation cannot replace it either.
English is never affected, and a page whose values are the built ones never reads the maps for text.

The script also checks that no template text that holds a file, an address, a number or a key is
left unprotected. usage: python3 -I scripts/en_guard.py [THEME_DIR]"""
import glob, hashlib, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
THEME = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), 'theme')
TEXT_TYPES = {'text', 'textarea', 'richtext', 'inline_richtext', 'html'}

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
    ('ms-home-01', None, 'video_url'): 'v',
    ('ms-hp-chapter', None, 'link_query'): 'v',
    ('ms-product-main', 'fibre', 'name'): 'v',
    ('ms-fibre-atlas', 'fibre', 'mark'): 'v',
    ('ms-lp-fabrics', 'fabric', 'code'): 'v',
}
HARMLESS = {
    ('ms-stockists', 'place', 'city'), ('ms-stockists', 'place', 'country'), ('ms-stockists', 'place', 'address'),
    ('ms-fibre-atlas', 'fibre', 'name'), ('ms-sizes', 'system', 'height'),
}
strip = lambda s: re.sub(r'\A\s*/\*.*?\*/', '', s, flags=re.S)
md5 = lambda s: hashlib.md5(s.encode('utf-8')).hexdigest()


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
    m = re.search(r'{%-?\s*schema\s*-?%}(.*?){%-?\s*endschema', open(f, encoding='utf-8').read(), re.S)
    if not m:
        continue
    sch = json.loads(m.group(1))
    n = os.path.basename(f)[:-7]
    types[(n, None)] = {x['id']: x['type'] for x in sch.get('settings', []) if 'id' in x}
    for b in sch.get('blocks', []):
        types[(n, b.get('type'))] = {x['id']: x['type'] for x in b.get('settings', []) if 'id' in x}

prot, txt, loose, texts = {}, {}, [], set()


def take(tk, key, bid, stype, btype, settings):
    for sid, v in (settings or {}).items():
        t = types.get((stype, btype), {}).get(sid)
        p = PROTECT.get((stype, btype, sid))
        if not isinstance(v, str) or v == '' or (t not in TEXT_TYPES and not p):
            continue
        slot = '%s/%s/%s' % (key, bid or '-', sid)
        if p:
            assert '¦' not in v and '{{' not in v and '{%' not in v and '\n' not in v, (tk, slot, v[:60])
            prot.setdefault(tk, []).append('%s=%s' % (slot, v))
        else:
            if kind(v) and (stype, btype, sid) not in HARMLESS and t in ('text', 'textarea'):
                loose.append((tk, stype, btype, sid, v))
            txt.setdefault(tk, []).append('%s=k%s' % (slot, md5(v)[:16]))
            texts.add(v)


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
if loose:
    for x in loose[:40]:
        print('UNGUARDED', x)
    sys.exit('%d template values hold a file, an address, a number or a key and are not protected' % len(loose))


def pieces(s, size=1000):
    """a translation longer than one locale value, cut between paragraphs where it can be"""
    out = []
    while len(s) > size:
        cut = s.rfind('</p>', 0, size - 4)
        cut = cut + 4 if cut > size // 3 else s.rfind(' ', 0, size)
        cut = cut if cut > 0 else size
        out.append(s[:cut]); s = s[cut:]
    out.append(s)
    assert len(out) <= 9
    return out


new_strings = {}
ns = os.path.join(HERE, 'r36_new_strings.json')
if os.path.exists(ns):
    new_strings = json.load(open(ns, encoding='utf-8'))
report = {}
for li, loc in enumerate(('it', 'ru')):
    path = os.path.join(THEME, 'locales', loc + '.json')
    d = json.load(open(path, encoding='utf-8'))
    tx = d['ms_tx']
    added = 0
    for en, tr in new_strings.items():
        base = 'k' + md5(en)[:16]
        for k in [k for k in tx if k == base + '_html' or re.fullmatch(re.escape(base) + r'_\d_html', k)]:
            del tx[k]
        for i, p in enumerate(pieces(tr[li]), 1):
            tx[base + ('_html' if i == 1 else '_%d_html' % i)] = p
    for v in sorted(texts):
        base = 'k' + md5(v)[:16]
        if base + '_html' not in tx:
            # left as it is in every language (a name, an address, a figure): its translation is itself
            for i, p in enumerate(pieces(v), 1):
                tx[base + ('_html' if i == 1 else '_%d_html' % i)] = p
            added += 1
    d.pop('ms_sl', None)
    raw = json.dumps(d, ensure_ascii=False, indent=2) + '\n'
    open(path, 'w', encoding='utf-8').write(raw)
    report[loc] = (added, len(raw))

assets = sorted(os.listdir(os.path.join(THEME, 'assets')))
assert all('¦' not in a for a in assets)


def write_map(name, maps, extra, what):
    out = ['{%- comment -%}',
           '  Written by scripts/en_guard.py: ' + what + ', per template (¦section/block/setting=…¦).',
           '{%- endcomment -%}',
           '{%- case tk -%}']
    groups = {}
    for tk in sorted(maps):
        groups.setdefault('¦' + '¦'.join(maps[tk]) + '¦', []).append(tk)
    for body, tks in sorted(groups.items(), key=lambda x: x[1][0]):
        out.append('{%- when ' + ', '.join("'%s'" % t for t in tks) + ' -%}' + body)
    out += extra + ['{%- endcase -%}']
    p = os.path.join(THEME, 'snippets', name)
    open(p, 'w', encoding='utf-8').write('\n'.join(out) + '\n')
    return os.path.getsize(p), max(len(b) for b in groups) if groups else 0


a = write_map('ms-en-map.liquid', prot, ["{%- when 'assets' -%}¦" + '¦'.join(assets) + '¦'],
              'the settings that are not language, as built; and the theme\'s own files')
b = write_map('ms-tx-map.liquid', txt, [], 'the fingerprint of the English each text setting was built with')
print('ms-en-map: %d values in %d templates (%d bytes, largest %d); ms-tx-map: %d texts in %d templates (%d bytes, largest %d);'
      ' identity translations added it %d, ru %d'
      % (sum(len(v) for v in prot.values()), len(prot), a[0], a[1], sum(len(v) for v in txt.values()), len(txt), b[0], b[1], report['it'][0], report['ru'][0]))
json.dump(sorted([[x, y or '', z] for (x, y, z) in PROTECT]), open(os.path.join(HERE, 'en_guard_protect.json'), 'w'))
