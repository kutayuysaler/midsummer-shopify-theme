"""print a batch of the units to translate (bin/tr/units.json), with their ids; those already translated
in bin/tr/src/*.txt are marked with *. usage: python3 tools/tr_batch.py <start> <count> [--todo]"""
import glob, json, os, re, sys
SP = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
L = json.load(open(os.path.join(SP, 'bin', 'tr', 'units.json'), encoding='utf-8'))
done = set()
for f in glob.glob(os.path.join(SP, 'bin', 'tr', 'src', '*.txt')):
    done |= set(re.findall(r'(?m)^@([0-9a-f]{7})\s*$', open(f, encoding='utf-8').read()))
a, n = int(sys.argv[1]), int(sys.argv[2])
todo = '--todo' in sys.argv
sys.path.insert(0, os.path.join(SP, 'bin', 'tr'))
import glossary as G, units as U  # units the glossary alone translates (fibre lists, needs) are not to do
done |= {x['id'] for x in L if U.auto(x['en'], G, 0) is not None and U.auto(x['en'], G, 1) is not None}
sel = [x for x in L if x['id'] not in done] if todo else L
for i in range(a, min(a + n, len(sel))):
    x = sel[i]
    print('%s%s\t[%s]\t%s' % ('*' if x['id'] in done else '', x['id'], x['where'][:40], x['en'].replace('\n', '\\n')))
print('# %d of %d units translated' % (len(done & {x['id'] for x in L}), len(L)), file=sys.stderr)
