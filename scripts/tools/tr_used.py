"""The strings that need a translation, from bin/tr/strings.json (tools/tr_extract.py): all of them but
the names of the stockists and the press (they stay as they are written) and schema defaults no page
shows (a section placed with a value of its own). In page order: header, footer, layout, home, the rest
by file. Writes bin/tr/strings_used.json. usage: python3 tools/tr_used.py"""
import glob, html, json, os, re
SP = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
L = json.load(open(os.path.join(SP, 'bin', 'tr', 'strings.json'), encoding='utf-8'))
pages = glob.glob(SP + '/rt5/audit/*.html') + glob.glob(SP + '/rt5/*.html') + glob.glob(SP + '/rt5/sk/*.html')
blob = '\n'.join(open(p, encoding='utf-8').read() for p in pages)
blob_un = html.unescape(blob)
KEEP_NAMES = {'Midsummer Milano — the atelier'}


def seen1(e):
    return e in blob or e in blob_un or html.escape(e, quote=False) in blob


def seen(e):
    """shown as it is, or shown filled in ([name], [n]) or line by line (a textarea printed with <br>):
    then every piece of it is on a page"""
    if seen1(e):
        return True
    parts = [p.strip() for p in re.split(r'\[\[[^\]]*\]\]|\[[a-z_]+\]|\n', e) if len(p.strip()) >= 3]
    return bool(parts) and (len(parts) > 1 or parts[0] != e.strip()) and all(seen1(p) for p in parts)


keep = []
for x in L:
    w = x['where']
    if x['en'] not in KEEP_NAMES and all(re.search(r'\.(place_\d+\.(address|name|phone|email|map)|publication_\d+\.(name|title|date))$', y) for y in w):
        continue
    if all(':default.' in y for y in w) and not seen(x['en']):
        continue
    keep.append(x)
ORDER = ['header-group.json', 'footer-group.json', 'ms.liquid', 'ms-header.liquid', 'ms-footer.liquid', 'index.json']


def rank(x):
    f = x['where'][0].split(':')[0]
    return (ORDER.index(f) if f in ORDER else 10, f, x['where'][0])


keep.sort(key=rank)
json.dump(keep, open(os.path.join(SP, 'bin', 'tr', 'strings_used.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(keep), 'strings,', sum(len(x['en']) for x in keep), 'characters')
