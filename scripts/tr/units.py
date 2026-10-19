"""Translation units: the theme's English strings cut where their markup cuts them, so a translation never
touches the markup. A string with block markup (<p>, <span>, <br> …) gives one unit per run of words
between the blocks; inline markup inside a run (<a>, <em>, <strong> …) is shown as {1}…{/1} and put
back from the string's own tags. A string without markup is one unit. Words that come from the
glossary (fibre lists, fibre~need data) are composed, not written by hand.

Used by tools/tr_units.py (the list to translate) and tools/tr_compile.py (the locale tables)."""
import hashlib, re

BLOCK = re.compile(r'(<\s*/?\s*(?:p|span|div|li|ul|ol|h[1-6]|br|summary|details|button|label|figure|figcaption|blockquote|section|header|footer|small|table|tr|td|th|dl|dt|dd)\b[^>]*>)', re.I)
INLINE = re.compile(r'<\s*(/?)\s*(a|em|strong|b|i|u|sup|sub|abbr|mark|s|cite|q)\b[^>]*>', re.I)


def uid(text):
    return hashlib.md5(text.encode('utf-8')).hexdigest()[:7]


def words(t):
    return bool(re.search(r'[A-Za-z]{2}', re.sub(r'<[^>]+>|&[a-z]+;|&#\d+;', '', t)))


def inline_out(core):
    """'see <a href="x">the award</a>' → ('see {1}the award{/1}', ['<a href="x">', '</a>'] by number)"""
    tags = {}
    stack = []
    n = [0]

    def rep(m):
        if m.group(1):  # closing
            k = stack.pop() if stack else 0
            tags.setdefault('/%d' % k, m.group(0))
            return '{/%d}' % k
        n[0] += 1
        stack.append(n[0])
        tags[str(n[0])] = m.group(0)
        return '{%d}' % n[0]
    return INLINE.sub(rep, core), tags


def inline_in(text, tags):
    return re.sub(r'\{(/?\d+)\}', lambda m: tags.get(m.group(1), m.group(0)), text)


def segments(s):
    """[(raw, None)] for markup and spacing kept as it is, [(unit_text, tags)] for words to translate"""
    out = []
    if not BLOCK.search(s):
        if words(s):
            lead = s[:len(s) - len(s.lstrip())]
            trail = s[len(s.rstrip()):]
            core = s.strip()
            u, tags = inline_out(core)
            if lead:
                out.append((lead, None))
            out.append((u, tags))
            if trail:
                out.append((trail, None))
        else:
            out.append((s, None))
        return out
    for part in BLOCK.split(s):
        if not part:
            continue
        if BLOCK.fullmatch(part) or not words(part):
            out.append((part, None))
            continue
        lead = part[:len(part) - len(part.lstrip())]
        trail = part[len(part.rstrip()):]
        u, tags = inline_out(part.strip())
        if lead:
            out.append((lead, None))
        out.append((u, tags))
        if trail:
            out.append((trail, None))
    return out


def units(s):
    return [u for u, tags in segments(s) if tags is not None]


def rebuild(s, table):
    """the string with every unit replaced from table (unit text → translation); None if one is missing"""
    out = []
    for u, tags in segments(s):
        if tags is None:
            out.append(u)
            continue
        t = table.get(u)
        if t is None:
            return None
        out.append(inline_in(t, tags))
    return ''.join(out)


# ── composed from the glossary
def auto(en, glossary, li):
    """a translation built from the glossary alone (li 0: Italian, 1: Russian), or None"""
    F, N, LOW = glossary.FIBRES, glossary.NEEDS, glossary.LOWER
    fl = {k.lower(): v for k, v in F.items()}

    def fib(x):
        x2 = x.strip()
        v = fl.get(x2.lower())
        if v is None:
            return None
        return x[:len(x) - len(x.lstrip())] + v[li] + x[len(x.rstrip()):]
    s = en
    if s in LOW:
        return LOW[s][li]
    # name~Need · Need|name~Need …
    if '~' in s and '|' in s or re.fullmatch(r'[^~|]+~[^~|]+', s):
        out = []
        for item in s.split('|'):
            if '~' not in item:
                return None
            a, b = item.split('~', 1)
            fa = fib(a)
            if fa is None:
                return None
            needs = []
            for nd in b.split(' · '):
                nv = N.get(nd.strip())
                if nv is None:
                    return None
                needs.append(nv[li])
            out.append(fa + '~' + ' · '.join(needs))
        return '|'.join(out)
    # a list of fibres: "Silk, Cheviot Wool, Linen" or "Silk,Cheviot Wool"
    for sep in (', ', ','):
        items = s.split(sep)
        if len(items) >= 1 and all(fib(x) is not None for x in items) and (len(items) > 1 or s.strip().lower() in fl):
            return sep.join(fib(x) for x in items)
    if s in LOW:
        return LOW[s][li]
    if s in N:
        return N[s][li]
    return None
