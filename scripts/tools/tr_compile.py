"""The locale tables: bin/tr/it.json and bin/tr/ru.json (English string → translation) from the units
translated in bin/tr/src/*.txt and the glossary. Each unit there is three lines:
    @<id>          (tools/tr_batch.py prints the ids)
    <Italian>      (= keeps the English; \\n is a line break)
    <Russian>
Checks every unit keeps the English's placeholders ([name], {fibres}, {1}…{/1}), line breaks and list
separators. usage: python3 tools/tr_compile.py"""
import collections, glob, json, os, re, sys
SP = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(SP, 'bin', 'tr'))
import units as U, glossary as G  # noqa: E402

src = {}
for f in sorted(glob.glob(os.path.join(SP, 'bin', 'tr', 'src', '*.txt'))):
    lines = [l.rstrip('\n') for l in open(f, encoding='utf-8')]
    i = 0
    while i < len(lines):
        m = re.match(r'^@([0-9a-f]{7})\s*$', lines[i])
        if not m:
            if lines[i].strip():
                print('%s:%d: stray line: %s' % (os.path.basename(f), i + 1, lines[i][:80]))
            i += 1
            continue
        if i + 2 >= len(lines) + 0 and i + 2 > len(lines) - 1 and i + 2 != len(lines) - 1:
            pass
        it, ru = (lines[i + 1] if i + 1 < len(lines) else ''), (lines[i + 2] if i + 2 < len(lines) else '')
        if m.group(1) in src and src[m.group(1)] != (it, ru):
            print('%s: %s given twice (the later one is kept)' % (os.path.basename(f), m.group(1)))
        src[m.group(1)] = (it, ru)
        i += 3

ALL = json.load(open(os.path.join(SP, 'bin', 'tr', 'strings.json'), encoding='utf-8'))
USED = {x['en'] for x in json.load(open(os.path.join(SP, 'bin', 'tr', 'strings_used.json'), encoding='utf-8'))}
PH = re.compile(r'\[[a-z_]+\]|\{[^{}\s]*\}')
errors = []


def check(en, tr, lang, uid):
    def bag(rx, s):  # a verb for several or for one ({keep/keeps}) is translated, so only its place is kept
        return collections.Counter('{many/one}' if re.fullmatch(r'\{[^{}/\s]+/[^{}/\s]+\}', x) else x for x in rx.findall(s))
    if not tr.strip():
        errors.append('%s %s: empty' % (uid, lang)); return False
    if bag(PH, en) != bag(PH, tr):
        errors.append('%s %s: placeholders %s → %s :: %s' % (uid, lang, sorted(bag(PH, en)), sorted(bag(PH, tr)), tr[:70])); return False
    for ch in ('\n', '|', '~'):
        if en.count(ch) != tr.count(ch):
            errors.append('%s %s: %r count %d → %d :: %s' % (uid, lang, ch, en.count(ch), tr.count(ch), tr[:70])); return False
    if re.fullmatch(r'[^,\n]+(,[^ ,][^,\n]*)+', en) and en.count(',') != tr.count(','):
        errors.append('%s %s: list of %d → %d :: %s' % (uid, lang, en.count(',') + 1, tr.count(',') + 1, tr[:70])); return False
    if '"' in tr and '"' not in en:
        errors.append('%s %s: straight double quote (breaks an attribute; use “ ” or « ») :: %s' % (uid, lang, tr[:70])); return False
    if re.search(r'<[a-zA-Z/]', tr) and not re.search(r'<[a-zA-Z/]', en):
        errors.append('%s %s: markup added :: %s' % (uid, lang, tr[:70])); return False
    return True


tables = {'it': {}, 'ru': {}}
unit_en = {}
for x in ALL:
    for u in U.units(x['en']):
        unit_en[U.uid(u)] = u
for k, (it, ru) in src.items():
    en = unit_en.get(k)
    if en is None:
        continue  # a unit no longer in the theme
    for lang, tr in (('it', it), ('ru', ru)):
        tr = en if tr.strip() == '=' else tr.replace('\\n', '\n')
        if check(en, tr, lang, k):
            tables[lang][en] = tr

missing = collections.Counter()
for lang, li in (('it', 0), ('ru', 1)):
    out = {}
    for x in ALL:
        en = x['en']
        a = U.auto(en, G, li)
        if a is not None:
            out[en] = a
            continue
        r = U.rebuild(en, tables[lang])
        if r is not None:
            out[en] = r
        elif en in USED:
            missing[lang] += 1
    json.dump(out, open(os.path.join(SP, 'bin', 'tr', lang + '.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0, sort_keys=True)
    print('%s: %d strings translated, %d used strings still missing' % (lang, len(out), missing[lang]))
for e in errors:
    print('  !', e)
print(len(src), 'units written,', len(errors), 'problems')
