"""The units to translate (bin/tr/units.py), from bin/tr/strings_used.json, in page order, each once:
writes bin/tr/units.json [{id, en, where, n}]; strings the glossary composes are left out.
usage: python3 tools/tr_units.py"""
import json, os, sys
SP = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(SP, 'bin', 'tr'))
import units as U, glossary as G  # noqa: E402
L = json.load(open(os.path.join(SP, 'bin', 'tr', 'strings_used.json'), encoding='utf-8'))
seen = {}
order = []
auto = 0
for x in L:
    if U.auto(x['en'], G, 0) is not None:
        auto += 1
        continue
    for u in U.units(x['en']):
        if u not in seen:
            seen[u] = {'id': U.uid(u), 'en': u, 'where': x['where'][0], 'n': 0}
            order.append(u)
        seen[u]['n'] += 1
out = [seen[u] for u in order]
ids = {}
for o in out:
    assert o['id'] not in ids, ('id clash', o['en'], ids.get(o['id']))
    ids[o['id']] = o['en']
json.dump(out, open(os.path.join(SP, 'bin', 'tr', 'units.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(out), 'units,', sum(len(o['en']) for o in out), 'characters;', auto, 'strings composed from the glossary')
