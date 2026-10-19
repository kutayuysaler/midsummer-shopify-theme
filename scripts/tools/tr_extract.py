"""Every English text the theme shows through snippets/ms-t.liquid, with where it is used:
the text settings of the ms-* sections in the templates and section groups, and the literal texts
the build passes to ms-t in sections and snippets ({% render 'ms-t', v: '…' %}).
Writes bin/tr/strings.json: [{"en": …, "where": [...]}], in order of first appearance.
usage: python3 tools/tr_extract.py"""
import glob, json, os, re, sys
SP = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
THEME = os.path.join(SP, 'v5')
sys.path.insert(0, os.path.join(SP, 'bin'))
TEXT = {'text', 'textarea', 'richtext', 'inline_richtext', 'html'}
TECH = re.compile(r'(handle|_url$|^url$|link$|tag$|_tag$|email|phone|lat$|lng$|lon$|^id$|_id$|blog$|code|instagram|feed|width|height|ratio|anchor|hash|key$|query|(^|_)(image|img|video|logo)(_\d+)?$|file$|^src$|icon$|pdf$|color$|colour$|qualities$|needs$|^kind$|slug|^mark$|soften$)')


def named_text(sid, typ, default):
    """as bin/build_r23.py: an id that reads like an address (band_link) with words for its default is a text"""
    if typ in TEXT and re.search(r'link$', sid) and isinstance(default, str) and re.search(r'[A-Za-z]{3,}', default) \
            and not re.match(r'\s*(/|https?:|shopify:|#|mailto:|tel:)', default) and not re.fullmatch(r'[a-z0-9_.-]+', default.strip()):
        return 'text!'
    return typ


def is_text(sid, typ):
    return typ == 'text!' or (typ in TEXT and not TECH.search(sid))


def load(p):
    s = open(p, encoding='utf-8').read()
    s = re.sub(r'^\s*/\*.*?\*/', '', s, flags=re.S)
    return json.loads(s)


schema = {}
DEFAULTS = []
for f in glob.glob(os.path.join(THEME, 'sections', 'ms-*.liquid')):
    t = open(f, encoding='utf-8').read()
    m = re.search(r'{%-?\s*schema\s*-?%}(.*?){%-?\s*endschema', t, re.S)
    if not m:
        continue
    sc = json.loads(m.group(1))
    st = {s['id']: named_text(s['id'], s.get('type'), s.get('default')) for s in sc.get('settings', []) if 'id' in s}
    bt = {}
    for b in sc.get('blocks', []):
        bt[b.get('type')] = {s['id']: named_text(s['id'], s.get('type'), s.get('default')) for s in b.get('settings', []) if 'id' in s}
    schema[os.path.basename(f)[:-7]] = (st, bt)
    # a section placed with no value of its own shows its schema default
    for x in sc.get('settings', []) + [y for blk in sc.get('blocks', []) for y in blk.get('settings', [])]:
        if 'id' in x and is_text(x['id'], named_text(x['id'], x.get('type'), x.get('default'))) and isinstance(x.get('default'), str):
            DEFAULTS.append((x['default'], os.path.basename(f) + ':default.' + x['id']))

seen = {}


def add(s, where):
    if not isinstance(s, str) or not s.strip():
        return
    if not re.search(r'[A-Za-z]{2}', re.sub(r'<[^>]+>', '', s)):
        return  # no words: numbers, marks, an address in figures
    if re.match(r'^\s*(https?:|shopify:|/|#[0-9A-Fa-f]{3,6}\s*$)', s) or re.match(r'^[\w.-]+\.(jpe?g|png|svg|webp|gif|mp4|pdf)$', s.strip()):
        return  # an address, a file, a colour
    seen.setdefault(s, []).append(where)


for f in sorted(glob.glob(os.path.join(THEME, 'templates', '*.json')) + glob.glob(os.path.join(THEME, 'sections', '*.json'))):
    d = load(f)
    fn = os.path.basename(f)
    for sid, sec in d.get('sections', {}).items():
        ty = sec.get('type', '')
        if ty not in schema:
            continue
        st, bt = schema[ty]
        for k, v in (sec.get('settings') or {}).items():
            if is_text(k, st.get(k)):
                add(v, '%s:%s.%s' % (fn, sid, k))
        for bid, b in (sec.get('blocks') or {}).items():
            bts = bt.get(b.get('type'), {})
            for k, v in (b.get('settings') or {}).items():
                if is_text(k, bts.get(k)):
                    add(v, '%s:%s.%s.%s' % (fn, sid, bid, k))

for d_, w_ in DEFAULTS:
    add(d_, w_)

# the theme's own text settings (Theme settings → Midsummer), their values and defaults
_ss = json.load(open(os.path.join(THEME, 'config', 'settings_schema.json'), encoding='utf-8'))
_sd = load(os.path.join(THEME, 'config', 'settings_data.json'))
_cur = _sd.get('current', {}) if isinstance(_sd.get('current'), dict) else {}
for grp in _ss:
    for x in grp.get('settings', []):
        if x.get('type') in TEXT and 'id' in x and (x['id'].startswith('ms_') and not TECH.search(x['id']) and not x['id'].startswith('ms_link') and ('whatsapp' not in x['id'] or x['id'] == 'ms_whatsapp_label')):
            add(x.get('default'), 'settings_schema:' + x['id'])
            add(_cur.get(x['id']), 'settings_data:' + x['id'])

# literal texts handed to ms-t by the build (generated snippets, hand-written sections)
LIT = re.compile(r"render 'ms-t', v: (?:'([^']*)'|\"([^\"]*)\")")
for f in sorted(glob.glob(os.path.join(THEME, 'sections', '*.liquid')) + glob.glob(os.path.join(THEME, 'snippets', '*.liquid')) + glob.glob(os.path.join(THEME, 'layout', '*.liquid'))):
    for m in LIT.finditer(open(f, encoding='utf-8').read()):
        add(m.group(1) if m.group(1) is not None else m.group(2), os.path.basename(f))

out = [{'en': k, 'where': v} for k, v in seen.items()]
os.makedirs(os.path.join(SP, 'bin', 'tr'), exist_ok=True)
json.dump(out, open(os.path.join(SP, 'bin', 'tr', 'strings.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(out), 'strings,', sum(len(x['en']) for x in out), 'characters')
