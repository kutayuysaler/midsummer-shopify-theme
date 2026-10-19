"""A marked dummy translation for finding text that does not pass through ms-t: every run of words
between tags and list separators becomes ⟪…⟫. Writes bin/tr/pseudo/it.json from bin/tr/strings.json.
usage: python3 tools/tr_pseudo.py; TR_DIR=bin/tr/pseudo python3 bin/build_r23.py; tools/render_locale.sh it"""
import json, os, re
SP = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
L = json.load(open(os.path.join(SP, 'bin', 'tr', 'strings.json'), encoding='utf-8'))


def mark(s):
    out = []
    for part in re.split(r'(<[^>]+>|\[[a-z]+\]|\{[a-z/]+\})', s):
        if not part or part.startswith('<') or re.fullmatch(r'\[[a-z]+\]|\{[a-z/]+\}', part):
            out.append(part)
            continue
        out.append(re.sub(r'[^,|~;·]*[A-Za-z][^,|~;·]*', lambda m: '⟪' + m.group(0) + '⟫', part))
    return ''.join(out)


d = {x['en']: mark(x['en']) for x in L}
os.makedirs(os.path.join(SP, 'bin', 'tr', 'pseudo'), exist_ok=True)
json.dump(d, open(os.path.join(SP, 'bin', 'tr', 'pseudo', 'it.json'), 'w', encoding='utf-8'), ensure_ascii=False)
print(len(d))
