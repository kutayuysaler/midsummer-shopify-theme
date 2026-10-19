"""Round 23: the site in Italian and Russian.

Every text the house wrote in English for its own sections (their settings in the templates, and the
texts the build writes into snippets) is shown through snippets/ms-t.liquid, which finds its
translation by a fingerprint of the English (md5) in locales/it.json and ru.json under "ms_tx".

1. snippets/ms-t.liquid is installed.
2. In every ms-* section, a text setting that is printed ({{ section.settings.x }}, with or without
   filters) or assigned to a variable is routed through ms-t. Conditions (if … != blank) are left
   as they are. snippets/ms-tr.liquid uses ms-t when a setting no longer holds its default.
3. The translations (bin/tr/it.json, bin/tr/ru.json: English → translation) are written into the
   locale files, each under ms_tx.k<md5[:16]>_html (the _html suffix keeps their markup), in
   pieces of at most 1000 characters (Shopify's limit for one value): …_html, …_2_html, ….

Run after bin/locales.py (tools/build.sh). Every step is a pure function of the build's output, so
a second build changes nothing. usage: python3 bin/build_r23.py"""
import glob, hashlib, json, os, re, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SP = os.path.dirname(HERE)
THEME = os.path.join(SP, 'v5')
TEXT = {'text', 'textarea', 'richtext', 'inline_richtext', 'html'}
changed = 0


CACHE = os.path.join(SP, '.r23')
VFS = {}
PRISTINE = {}


def read(path):
    """a theme file as the build left it before this step: when the file on disk is still this step's
    own output from the last build, its pristine version is taken from the cache, so every run
    starts from the same text and a wrong wrap never survives a later fix"""
    if path in VFS:
        return VFS[path]
    disk = open(path, encoding='utf-8').read() if os.path.exists(path) else ''
    rel = os.path.relpath(path, THEME)
    out_c, pri_c = os.path.join(CACHE, 'out', rel), os.path.join(CACHE, 'pristine', rel)
    if os.path.exists(out_c) and os.path.exists(pri_c) and open(out_c, encoding='utf-8').read() == disk:
        disk = open(pri_c, encoding='utf-8').read()
    PRISTINE[path] = disk
    VFS[path] = disk
    return disk


def write(path, text):
    if path not in VFS:
        read(path)
    VFS[path] = text


def flush():
    global changed
    for path, text in VFS.items():
        rel = os.path.relpath(path, THEME)
        for kind, body in (('pristine', PRISTINE[path]), ('out', text)):
            c = os.path.join(CACHE, kind, rel)
            os.makedirs(os.path.dirname(c), exist_ok=True)
            open(c, 'w', encoding='utf-8').write(body)
        if not os.path.exists(path) or open(path, encoding='utf-8').read() != text:
            open(path, 'w', encoding='utf-8').write(text)
            changed += 1


def key(s):
    return 'k' + hashlib.md5(s.encode('utf-8')).hexdigest()[:16]


# --restore, at the start of a build: put back the files as they were before this step, so the earlier
# steps (which patch some files in place) always find the text they expect
if '--restore' in sys.argv:
    n = 0
    for root, _, fs in os.walk(os.path.join(CACHE, 'out')):
        for fn in fs:
            out_c = os.path.join(root, fn)
            rel = os.path.relpath(out_c, os.path.join(CACHE, 'out'))
            path, pri_c = os.path.join(THEME, rel), os.path.join(CACHE, 'pristine', rel)
            if os.path.exists(path) and os.path.exists(pri_c) and open(path, encoding='utf-8').read() == open(out_c, encoding='utf-8').read():
                open(path, 'w', encoding='utf-8').write(open(pri_c, encoding='utf-8').read())
                n += 1
    print('round 23: %d files put back before the build' % n)
    sys.exit(0)

# ── 1. the lookup
write(os.path.join(THEME, 'snippets', 'ms-t.liquid'), open(os.path.join(HERE, 'tr', 'ms-t.liquid'), encoding='utf-8').read())

# ── 2. the sections
# settings that hold an address, a handle, a tag or a number, not words (never translated)
TECH = re.compile(r'(handle|_url$|^url$|link$|tag$|_tag$|email|phone|lat$|lng$|lon$|^id$|_id$|blog$|code|instagram|feed|width|height|ratio|anchor|hash|key$|query|(^|_)(image|img|video|logo)(_\d+)?$|file$|^src$|icon$|pdf$|color$|colour$|qualities$|needs$|^kind$|slug|^mark$|soften$)')


def named_text(sid, typ, default):
    """a setting's type for the wrap: 'text!' when its id reads like an address (band_link) but its
    default is words (Book a consultation)"""
    if typ in TEXT and re.search(r'link$', sid) and isinstance(default, str) and re.search(r'[A-Za-z]{3,}', default) \
            and not re.match(r'\s*(/|https?:|shopify:|#|mailto:|tel:)', default) and not re.fullmatch(r'[a-z0-9_.-]+', default.strip()):
        return 'text!'
    return typ


def schema_types(text):
    m = re.search(r'{%-?\s*schema\s*-?%}(.*?){%-?\s*endschema\s*-?%}', text, re.S)
    if not m:
        return None, {}, {}
    try:
        sc = json.loads(m.group(1))
    except ValueError:
        return None, {}, {}
    st = {s['id']: named_text(s['id'], s.get('type'), s.get('default')) for s in sc.get('settings', []) if 'id' in s}
    bt = {}
    for b in sc.get('blocks', []):
        for s in b.get('settings', []):
            if 'id' in s:
                bt[s['id']] = named_text(s['id'], s.get('type'), s.get('default'))
    return m.start(), st, bt


def is_text(scope, sid, st, bt):
    t = (st if scope == 'section' else bt).get(sid)
    return t == 'text!' or (t in TEXT and not TECH.search(sid))


n_out = n_assign = 0


def dyn_keys(body):
    """the variables that name a setting by a key built in the code (assign kt = 'step' | append: i |
    append: '_title'): each with the pattern of the setting ids it can name"""
    pats = {}
    rx = re.compile(r"assign\s+([a-z_][a-z0-9_]*)\s*=\s*('[a-z0-9_]*'|[a-z_][a-z0-9_.]*)((?:\s*\|\s*(?:append|prepend):\s*(?:'[^']*'|[a-z_][a-z0-9_.]*))+)")
    for m in rx.finditer(body):
        var, first, ops = m.groups()
        pat = re.escape(first[1:-1]) if first.startswith("'") else '.*'
        for op, arg in re.findall(r"(append|prepend):\s*('[^']*'|[a-z_][a-z0-9_.]*)", ops):
            piece = re.escape(arg[1:-1]) if arg.startswith("'") else '.*'
            pat = pat + piece if op == 'append' else piece + pat
        pats.setdefault(var, set()).add(pat)
    return pats


FWD_SKIP = {'ms-t', 'ms-tr', 'ms-link', 'ms-img', 'ms-srcset', 'ms-fibre-mark', 'ms-fibre-slug', 'ms-icon', 'ms-photo-tone',
            'ms-on-white', 'ms-sys-data', 'ms-kind', 'ms-system-facts', 'ms-fibre-beds', 'ms-note-cat'}


def rewrite(body, prefixes):
    """route the text settings printed or assigned in body through ms-t; prefixes maps each way the
    code names the settings ('section.settings', 'block.settings', or an alias such as 's' or 'ss')
    to (scope, section types, block types). A setting may be named directly (s.heading) or by a key
    the code builds (s[kt]); a key counts as text when every setting it can name is a text."""
    alt = '|'.join(re.escape(p) for p in sorted(prefixes, key=len, reverse=True))
    REF = r'((%s)(?:\.([a-z0-9_]+)|\[([a-z_][a-z0-9_]*)\]))' % alt
    out_rx = re.compile(r'\{\{(-?)\s*' + REF + r'\s*(\|[^{}]*?)?\s*(-?)\}\}')
    tag_rx = re.compile(r'\{%(-?)\s*assign\s+([a-z_][a-z0-9_]*)\s*=\s*' + REF + r'\s*(\|[^{}%]*?)?\s*(-?)%\}')
    line_rx = re.compile(r'^(\s*)assign\s+([a-z_][a-z0-9_]*)\s*=\s*' + REF + r'\s*(\|.*?)?\s*$')
    dflt_rx = re.compile(r'(default|append|prepend):\s*' + REF)
    dyn = dyn_keys(body)

    def text(pre, sid, var=None):
        scope, st, bt = prefixes[pre]
        if sid:
            return is_text(scope, sid, st, bt)
        ids = [i for i in (st if scope == 'section' else bt) if any(re.fullmatch(p, i) for p in dyn.get(var, ()))]
        return bool(ids) and all(is_text(scope, i, st, bt) for i in ids)

    n_d = [0]

    def dflt_pre(chunk):
        """the settings given as a fallback inside chunk (| default: s.heading): looked up first, by name"""
        pre = []
        def one(m):
            op, ref, p, sid, var = m.groups()
            if not text(p, sid, var):
                return m.group(0)
            n_d[0] += 1
            name = 'ms_d%d' % n_d[0]
            pre.append((name, ref))
            return op + ': ' + name
        chunk = dflt_rx.sub(one, chunk)
        # a text setting handed to a snippet that passes it on (ms-craft-svg → its drawing): looked up first
        r = re.match(r"\s*render\s+'(ms-[a-z0-9-]+)'", chunk)
        if r and r.group(1) not in FWD_SKIP:
            def prm(mm):
                name, ref, p, sid, var = mm.groups()
                if not text(p, sid, var):
                    return mm.group(0)
                n_d[0] += 1
                nm = 'ms_d%d' % n_d[0]
                pre.append((nm, ref))
                return name + ': ' + nm
            chunk = re.sub(r'\b([a-z_][a-z0-9_]*):\s*' + REF + r'(?![.\[\w])', prm, chunk)
        return chunk, pre

    def out(m):
        global n_out
        d1, ref, pre, sid, var, filt, d2 = m.groups()
        caps = []
        if filt:
            filt, caps = dflt_pre(filt)
        head = ''.join("{%% capture %s %%}{%% render 'ms-t', v: %s %%}{%% endcapture %%}" % c for c in caps)
        if not text(pre, sid, var):
            return head + ('{{%s %s %s %s}}' % (d1, ref, filt.strip(), d2) if caps else m.group(0))
        n_out += 1
        r = "{%% render 'ms-t', v: %s %%}" % ref
        if not filt:
            return r.replace('{%', '{%' + d1, 1).replace('%}', d2 + '%}') if (d1 or d2) else r
        return head + "{%% capture ms_t_out %%}%s{%% endcapture %%}{{%s ms_t_out %s %s}}" % (r, d1, filt.strip(), d2)

    def assign_tag(m):
        global n_assign
        d1, var, ref, pre, sid, kv, filt, d2 = m.groups()
        caps = []
        if filt:
            filt, caps = dflt_pre(filt)
        head = ''.join("{%% capture %s %%}{%% render 'ms-t', v: %s %%}{%% endcapture %%}" % c for c in caps)
        if not text(pre, sid, kv):
            return head + ('{%%%s assign %s = %s %s %s%%}' % (d1, var, ref, filt.strip(), d2) if caps else m.group(0))
        n_assign += 1
        r = head + "{%%%s capture %s %%}{%% render 'ms-t', v: %s %%}{%% endcapture %s%%}" % (d1, var, ref, d2)
        if filt:
            r += "{%%- assign %s = %s %s -%%}" % (var, var, filt.strip())
        return r

    def liquid_block(m):
        global n_assign
        lines = m.group(2).split('\n')
        for i, ln in enumerate(lines):
            ind = re.match(r'\s*', ln).group(0)
            ln, caps = dflt_pre(ln)
            head = []
            for c in caps:
                head += ['%scapture %s' % (ind, c[0]), "%s  render 'ms-t', v: %s" % (ind, c[1]), '%sendcapture' % ind]
            a = line_rx.match(ln)
            if a and text(a.group(4), a.group(5), a.group(6)):
                ind, var, ref, pre, sid, kv, filt = a.groups()
                rep = ['%scapture %s' % (ind, var), "%s  render 'ms-t', v: %s" % (ind, ref), '%sendcapture' % ind]
                if filt:
                    rep.append('%sassign %s = %s %s' % (ind, var, var, filt.strip()))
                ln = '\n'.join(rep)
                n_assign += 1
            lines[i] = '\n'.join(head + [ln])
        return m.group(1) + '\n'.join(lines) + m.group(3)

    body = out_rx.sub(out, body)
    body = tag_rx.sub(assign_tag, body)
    body = re.sub(r'(\{%-?\s*liquid\b)(.*?)(-?%\})', liquid_block, body, flags=re.S)

    # a text setting given as the fallback of something else ({{ s.image.alt | default: s.heading }},
    # {% assign sub = product.type | default: s.line %}): looked up first, by name
    def any_out(m):
        inner, caps = dflt_pre(m.group(2))
        if not caps:
            return m.group(0)
        return ''.join("{%% capture %s %%}{%% render 'ms-t', v: %s %%}{%% endcapture %%}" % c for c in caps) + '{{' + m.group(1) + inner + m.group(3) + '}}'

    def any_tag(m):
        if re.match(r'\s*liquid\b', m.group(2)):
            return m.group(0)
        inner, caps = dflt_pre(m.group(2))
        if not caps:
            return m.group(0)
        return ''.join("{%% capture %s %%}{%% render 'ms-t', v: %s %%}{%% endcapture %%}" % c for c in caps) + '{%' + m.group(1) + inner + m.group(3) + '%}'
    body = re.sub(r'\{\{(-?)((?:(?!\}\}).)*?)(-?)\}\}', any_out, body, flags=re.S)
    return re.sub(r'\{%(-?)((?:(?!%\}).)*?)(-?)%\}', any_tag, body, flags=re.S)


ALIAS_RX = re.compile(r'assign\s+([a-z_][a-z0-9_]*)\s*=\s*(section|block)\.settings\s*(?:-?%\}|$)', re.M)
CALL_RX = re.compile(r"render\s+'(ms-[a-z0-9-]+)'[^%]*?\b([a-z_][a-z0-9_]*):\s*(section|block)\.settings\b(?!\.)")
snippet_refs = {}
for f in sorted(glob.glob(os.path.join(THEME, 'sections', 'ms-*.liquid'))):
    src = read(f)
    cut, st, bt = schema_types(src)
    if cut is None:
        continue
    body, tail = src[:cut], src[cut:]
    prefixes = {'section.settings': ('section', st, bt), 'block.settings': ('block', st, bt)}
    for alias, scope in ALIAS_RX.findall(body):
        prefixes[alias] = (scope, st, bt)
    # a block reached by another name: for b in section.blocks … b.settings.label; assign bs = b.settings
    for v in set(re.findall(r'\b([a-z_][a-z0-9_]*)\.settings\.[a-z0-9_]', body)):
        if v not in ('section', 'block') and v + '.settings' not in prefixes:
            prefixes[v + '.settings'] = ('block', st, bt)
    for alias, src_ in re.findall(r'assign\s+([a-z_][a-z0-9_]*)\s*=\s*([a-z_][a-z0-9_]*)\.settings\s*(?:-?%\}|$)', body, re.M):
        if src_ not in ('section', 'block') and alias not in prefixes:
            prefixes[alias] = ('block', st, bt)
    # a snippet given the settings under a name of its own reads them with this section's schema
    for snip, alias, scope in CALL_RX.findall(body):
        snippet_refs.setdefault(snip, {})[alias] = (scope, st, bt)
    write(f, rewrite(body, prefixes) + tail)

for snip, prefixes in sorted(snippet_refs.items()):
    f = os.path.join(THEME, 'snippets', snip + '.liquid')
    if not os.path.exists(f) or snip in ('ms-t', 'ms-tr', 'ms-link'):
        continue
    write(f, rewrite(read(f), prefixes))

# ── 2b. the words written into the code itself (the header and its menus, the footer, drawers, labels,
#    the texts the build writes into snippets): each visible run of words, and each alt, title,
#    aria-label and placeholder made only of words, goes through ms-t. Scripts, styles, comments,
#    the schema and anything that reads as an address or code are left alone.
LIQ = re.compile(r'(\{%-?\s*(comment|raw|schema|javascript|stylesheet|style)\s*-?%\}.*?\{%-?\s*end\2\s*-?%\}|\{%-?\s*liquid\b.*?-?%\}|\{%.*?%\}|\{\{.*?\}\})', re.S)
WORDS = re.compile(r"[A-Za-z][a-z]+(?:[\s,.;:!?’'()\-–—&*…”\"»/]+|$)")
ATTR = re.compile(r'(\s(?:alt|title|aria-label|placeholder)=)"([^"{}<>]*)"')
SKIP_FILES = {'ms-t.liquid', 'ms-tr.liquid', 'ms-link.liquid', 'ms-photo-tone.liquid', 'ms-on-white.liquid', 'ms-img.liquid', 'ms-system-facts.liquid',
              'ms-product-note.liquid'}  # (ms-product-note has its own Italian and Russian)


def lit(s):
    if "'" not in s:
        return "'" + s + "'"
    if '"' not in s:
        return '"' + s + '"'
    return "'" + s.replace("'", '&#39;') + "'"


def wordy(s):
    t = s.strip()
    if len(t) < 2 or not re.search(r'[A-Za-z]{2}', t):
        return False
    if re.match(r'^[#?./@]', t) and ' ' not in t:
        return False
    if re.fullmatch(r'(center|top|bottom|left|right)(\s+(\d+%|center|top|bottom|left|right))*', t):
        return False  # a position (object-position: center 62%)
    if re.fullmatch(r'(rgba?|hsla?)\([\d.,%\s]+\)', t):
        return False  # a colour written as rgba(251, 249, 245, .78)
    if re.search(r'[{}<>=\\]|^/|https?:|\.(liquid|js|css|json|jpe?g|png|svg|webp|mp4)\b|^#[0-9a-f]{3,6}$|^[a-z0-9_,|:~-]+$', t):
        return False  # an address, a class, a key, a colour: not words
    if re.search(r'(^|[;\s])[a-z-]+\s*:\s*[^;]+;', t) and not re.search(r'[A-Z]', t) or re.search(r'#[0-9A-Fa-f]{6}\b', t):
        return False  # a style (prop: value;); prose with a semicolon or an entity (&middot;) is words
    return bool(WORDS.search(t))


def wrap_text(seg, state):
    """the HTML between two Liquid tags: wrap its text runs and plain attributes; state[0] is the open
    element the text sits in (script/style: left alone), state[1] True while inside a tag"""
    out = []
    i = 0
    while i < len(seg):
        if state[1]:
            j = seg.find('>', i)
            part = seg[i:] if j < 0 else seg[i:j + 1]
            part = ATTR.sub(lambda m: m.group(1) + '"' + ("{% render 'ms-t', v: " + lit(m.group(2)) + " %}" if wordy(m.group(2)) else m.group(2)) + '"', part)
            out.append(part)
            if j < 0:
                return ''.join(out)
            i = j + 1
            state[1] = False
            continue
        j = seg.find('<', i)
        text = seg[i:] if j < 0 else seg[i:j]
        if state[0] in ('script', 'style') or not wordy(text):
            out.append(text)
        else:
            lead = text[:len(text) - len(text.lstrip())]
            trail = text[len(text.rstrip()):]
            core = re.sub(r'\s+', ' ', text.strip())
            out.append(lead + "{% render 'ms-t', v: " + lit(core) + " %}" + trail)
        if j < 0:
            break
        m = re.match(r'<(/?)([a-zA-Z][a-zA-Z0-9-]*)', seg[j:])
        if m:
            name = m.group(2).lower()
            if m.group(1):
                if name == state[0]:
                    state[0] = None
            elif name in ('script', 'style'):
                state[0] = name
        state[1] = True
        i = j
    return ''.join(out)


n_lit = 0
targets = sorted(glob.glob(os.path.join(THEME, 'sections', 'ms-*.liquid')) + glob.glob(os.path.join(THEME, 'snippets', 'ms-*.liquid'))) + [os.path.join(THEME, 'layout', 'ms.liquid')]
for f in targets:
    if os.path.basename(f) in SKIP_FILES or os.path.basename(f).startswith('ms-craft-svg') or os.path.basename(f).startswith('ms-icon'):
        continue
    src = read(f)
    m = re.search(r'{%-?\s*schema\s*-?%}', src)
    body, tail = (src[:m.start()], src[m.start():]) if m else (src, '')
    parts = LIQ.split(body)
    # re.split with groups returns the captured tags; rebuild with the text parts wrapped
    pieces_ = []
    state = [None, False]
    k = 0
    for tok in LIQ.finditer(body):
        pieces_.append(wrap_text(body[k:tok.start()], state))
        pieces_.append(tok.group(0))
        k = tok.end()
    pieces_.append(wrap_text(body[k:], state))
    new = ''.join(pieces_)
    n_lit += new.count("render 'ms-t', v: '") + new.count('render \'ms-t\', v: "') - body.count("render 'ms-t', v: '")
    write(f, new + tail)

# ── 2c. words inside the Liquid code: texts assigned to a variable (alone or as a list split later; a
#    list keeps its separators in translation), echoed, given as a fallback (| default: '…') or
#    handed to a snippet as a label. The data strings the code parses (fibre lists) are left alone.
SQ = r"'([^'\n]*)'"
NO_LIT = SKIP_FILES | {'ms-system-facts.liquid', 'ms-sys-data.liquid'}
PARAM_SKIP = {'ms-t', 'ms-tr', 'ms-link', 'ms-img', 'ms-srcset', 'ms-fibre-mark', 'ms-fibre-slug', 'ms-icon', 'ms-photo-tone', 'ms-on-white'}
n_code = [0]


def lit_ok(t):
    return wordy(t) and '~' not in t and not re.search(r'\w:[a-z]', t)


def code_lines(text, liquid_block):
    """rewrite one {% liquid %} block's lines (liquid_block True) or one {% … %} tag's body"""
    out = []
    for ln in text.split('\n'):
        ind = re.match(r'\s*', ln).group(0)
        m = re.match(r'^(\s*)assign\s+([a-z_][a-z0-9_]*)\s*=\s*' + SQ + r'\s*(\|.*?)?\s*$', ln)
        if m and lit_ok(m.group(3)):
            ind, var, t, filt = m.groups()
            out += ['%scapture %s' % (ind, var), "%s  render 'ms-t', v: %s" % (ind, lit(t)), '%sendcapture' % ind]
            if filt:
                out.append('%sassign %s = %s %s' % (ind, var, var, filt.strip()))
            n_code[0] += 1
            continue
        m = re.match(r'^(\s*)echo\s+' + SQ + r'\s*$', ln)
        if m and lit_ok(m.group(2)):
            out.append("%srender 'ms-t', v: %s" % (m.group(1), lit(m.group(2))))
            n_code[0] += 1
            continue
        # a fallback or a snippet's label given as a literal: captured first, then used by name
        pre = []
        def dflt(mm):
            if not lit_ok(mm.group(1)):
                return mm.group(0)
            n_code[0] += 1
            var = 'ms_l%d' % n_code[0]
            pre.extend(['%scapture %s' % (ind, var), "%s  render 'ms-t', v: %s" % (ind, lit(mm.group(1))), '%sendcapture' % ind])
            return 'default: ' + var
        ln2 = re.sub(r'default:\s*' + SQ, dflt, ln)
        r = re.match(r"^\s*render\s+'([a-z0-9-]+)'", ln2)
        if r and r.group(1) not in PARAM_SKIP:
            def param(mm):
                if mm.group(1) in ('key', 'to', 'handle', 'fallback', 'image', 'width', 'sizes', 'class', 'id', 'slug', 'v', 'value', 'default'):
                    return mm.group(0)
                if not lit_ok(mm.group(2)):
                    return mm.group(0)
                n_code[0] += 1
                var = 'ms_l%d' % n_code[0]
                pre.extend(['%scapture %s' % (ind, var), "%s  render 'ms-t', v: %s" % (ind, lit(mm.group(2))), '%sendcapture' % ind])
                return '%s: %s' % (mm.group(1), var)
            ln2 = re.sub(r'\b([a-z_][a-z0-9_]*):\s*' + SQ, param, ln2)
        out += pre + [ln2]
    return '\n'.join(out)


def code_pass(body):
    def liq(m):
        return m.group(1) + code_lines(m.group(2), True) + m.group(3)
    body = re.sub(r'(\{%-?\s*liquid\b)(.*?)(-?%\})', liq, body, flags=re.S)

    # single tags: {% assign x = 'Words' | f %}, {% render 'x', label: 'Words' %}, {{ x | default: 'Words' }}
    def tag(m):
        d1, inner, d2 = m.group(1), m.group(2), m.group(3)
        if re.match(r'\s*(liquid|comment|raw|schema|when|case|if|elsif|unless|for|capture)\b', inner):
            return m.group(0)
        new = code_lines(inner.strip(), False)
        if new == inner.strip():
            return m.group(0)
        lines = new.split('\n')
        return '{%%%s liquid\n%s\n%s%%}' % (d1, '\n'.join('  ' + l.strip() for l in lines), d2)

    body = re.sub(r'\{%(-?)((?:(?!%\}).)*?)(-?)%\}', tag, body, flags=re.S)

    def outp(m):
        d1, inner, d2 = m.group(1), m.group(2), m.group(3)
        pre = []
        def dflt(mm):
            if not lit_ok(mm.group(1)):
                return mm.group(0)
            n_code[0] += 1
            var = 'ms_l%d' % n_code[0]
            pre.append("{%% capture %s %%}{%% render 'ms-t', v: %s %%}{%% endcapture %%}" % (var, lit(mm.group(1))))
            return 'default: ' + var
        inner2 = re.sub(r'default:\s*' + SQ, dflt, inner)
        return ''.join(pre) + '{{' + d1 + inner2 + d2 + '}}'
    return re.sub(r'\{\{(-?)((?:(?!\}\}).)*?)(-?)\}\}', outp, body, flags=re.S)


for f in sorted(glob.glob(os.path.join(THEME, 'sections', 'ms-*.liquid')) + glob.glob(os.path.join(THEME, 'snippets', 'ms-*.liquid'))):
    bn = os.path.basename(f)
    if bn in NO_LIT or bn.startswith('ms-craft-svg') or bn.startswith('ms-icon'):
        continue
    src = read(f)
    m = re.search(r'{%-?\s*schema\s*-?%}', src)
    body, tail = (src[:m.start()], src[m.start():]) if m else (src, '')
    write(f, code_pass(body) + tail)

# ── 2d. texts handed on to a snippet (render 'ms-mega-panel', title: ss.t2 …) are printed through ms-t
#    inside it; and the theme's own text settings (Theme settings → Midsummer: settings.ms_…)
CALLP = re.compile(r"render\s+'(ms-[a-z0-9-]+)'\s*,([^%\n]*)")
text_params = {}
alias_all = {}
for f in sorted(glob.glob(os.path.join(THEME, 'sections', 'ms-*.liquid')) + glob.glob(os.path.join(THEME, 'snippets', 'ms-*.liquid'))):
    src = read(f)
    for m in CALLP.finditer(src):
        snip = m.group(1)
        if snip in PARAM_SKIP or snip in ('ms-t', 'ms-tr'):
            continue
        for pm in re.finditer(r'\b([a-z_][a-z0-9_]*):\s*([a-z_][a-z0-9_.]*)', m.group(2)):
            name, val = pm.groups()
            if name in ('key', 'to', 'handle', 'fallback', 'image', 'width', 'sizes', 'class', 'id', 'slug', 'v', 'value', 'default', 'items', 'feature', 'foot', 'no') or name.endswith('_url') or name.endswith('_landing'):
                continue
            if re.match(r'(ss|s|section\.settings|block\.settings|settings)\.', val) or re.match(r'ms_l\d+$', val):
                text_params.setdefault(snip, set()).add(name)
for snip, names in sorted(text_params.items()):
    f = os.path.join(THEME, 'snippets', snip + '.liquid')
    if not os.path.exists(f):
        continue
    src = read(f)
    alt = '|'.join(sorted(names, key=len, reverse=True))
    def po(m):
        global n_out
        d1, ref, filt, d2 = m.groups()
        n_out += 1
        r = "{%% render 'ms-t', v: %s %%}" % ref
        return r if not filt else "{%% capture ms_t_out %%}%s{%% endcapture %%}{{%s ms_t_out %s %s}}" % (r, d1, filt.strip(), d2)
    src = re.sub(r'\{\{(-?)\s*(%s)\s*(\|[^{}]*?)?\s*(-?)\}\}' % alt, po, src)
    write(f, src)

# the theme's own text settings
try:
    _ss = json.load(open(os.path.join(THEME, 'config', 'settings_schema.json'), encoding='utf-8'))
except ValueError:
    _ss = []
GTEXT = {x['id'] for grp in _ss for x in grp.get('settings', []) if x.get('type') in TEXT and 'id' in x and not TECH.search(x['id']) and not x['id'].startswith('ms_link') and 'whatsapp' not in x['id'] or x.get('id') == 'ms_whatsapp_label'}
for f in sorted(glob.glob(os.path.join(THEME, 'sections', 'ms-*.liquid')) + glob.glob(os.path.join(THEME, 'snippets', 'ms-*.liquid')) + [os.path.join(THEME, 'layout', 'ms.liquid')]):
    src = read(f)
    def go(m):
        global n_out
        d1, ref, sid, filt, d2 = m.groups()
        if sid not in GTEXT:
            return m.group(0)
        n_out += 1
        r = "{%% render 'ms-t', v: %s %%}" % ref
        return r if not filt else "{%% capture ms_t_out %%}%s{%% endcapture %%}{{%s ms_t_out %s %s}}" % (r, d1, filt.strip(), d2)
    write(f, re.sub(r'\{\{(-?)\s*(settings\.([a-z0-9_]+))\s*(\|[^{}]*?)?\s*(-?)\}\}', go, src))

# ── 2e. fibre names: data the code reads (a fibre's mark, its atlas entry) is shown translated, so the
#    mark and the link also know a fibre by its Italian and Russian names; and the collection pages'
#    fibre names, which the code assembles from English data (snippets/ms-system-facts), are each
#    looked up as they are shown.
sys.path.insert(0, os.path.join(HERE, 'tr'))
import glossary  # noqa: E402
_al = glossary.mark_aliases()
_by = {}
for _k, _v in sorted(_al.items()):
    _by.setdefault(_v, []).append(_k)
_case = '\n'.join("    when %s\n      assign %%s = '%s'" % (', '.join("'%s'" % x.replace("'", "’") for x in ks), en) for en, ks in sorted(_by.items()))


def _sub1(path, pairs):
    t = read(path)
    for a, b in pairs:
        assert a in t or b in t, (path, a[:70])
        t = t.replace(a, b, 1) if b not in t else t
    write(path, t)


_fm = os.path.join(THEME, 'snippets', 'ms-fibre-mark.liquid')
_sub1(_fm, [("  assign n = name | downcase | strip\n",
             "  assign n = name | downcase | strip\n  case n\n" + (_case % (('n',) * len(_by))) + "\n  endcase\n")])
_fs = os.path.join(THEME, 'snippets', 'ms-fibre-slug.liquid')
_sub1(_fs, [("{%- assign fname = name | downcase | strip -%}\n",
             "{%- assign fname = name | downcase | strip -%}\n{%- liquid\n  case fname\n" + (_case % (('fname',) * len(_by))) + "\n  endcase\n-%}\n")])

_sy = os.path.join(THEME, 'sections', 'ms-systems.liquid')
_ft = ''.join('\n    <span data-f="%s">{%% render \'ms-t\', v: \'%s\' %%}</span>' % (k, k) for k in glossary.LOWER)
_sub1(_sy, [
    ("""<span data-k="and">{% capture ms_t_out %}{% render 'ms-t', v: s.and_label %}{% endcapture %}{{ ms_t_out | default: 'and' }}</span>\n""",
     """<span data-k="and">{% capture ms_t_out %}{% render 'ms-t', v: s.and_label %}{% endcapture %}{{ ms_t_out | default: 'and' }}</span>""" + _ft + "\n"),
    ("hints[n.getAttribute('data-k')] = n.textContent; });\n",
     "hints[n.getAttribute('data-k')] = n.textContent; });\n    var ft = {};\n    if (tpl) Array.prototype.forEach.call(tpl.content.querySelectorAll('[data-f]'), function (n) { ft[n.getAttribute('data-f')] = n.textContent; });\n"),
    ("      var fs = fibresFor(n);\n",
     "      var fs = fibresFor(n).map(function (f) { return ft[f] || f; });\n"),
    ("""<li title="{{ f | escape }}">{% render 'ms-fibre-mark', name: f, size: 26 %}<span class="ms-sy__vh">{{ f }}</span></li>""",
     """{%- capture ft -%}{% render 'ms-t', v: f %}{%- endcapture -%}<li title="{{ ft | escape }}">{% render 'ms-fibre-mark', name: f, size: 26 %}<span class="ms-sy__vh">{{ ft }}</span></li>"""),
    ("""<p class="ms-sy__fnames" aria-hidden="true">{{ fibres | join: ' · ' }}</p>""",
     """<p class="ms-sy__fnames" aria-hidden="true">{%- for f in fibres -%}{%- unless forloop.first %} · {% endunless -%}{% render 'ms-t', v: f %}{%- endfor -%}</p>"""),
    ("""<td class="ms-sy__tf">{{ fparts[0] | replace: ',', ', ' | default: '–' }}</td>""",
     """<td class="ms-sy__tf">{%- assign tfs = fparts[0] | split: ',' -%}{%- for f in tfs -%}{%- unless forloop.first -%}, {% endunless -%}{% render 'ms-t', v: f %}{%- else -%}–{%- endfor -%}</td>"""),
])
_rel = os.path.join(THEME, 'sections', 'ms-product-related.liquid')
_sub1(_rel, [("""<span class="ms-rel__marks" title="{{ fibres | join: ' · ' | escape }}">""",
              """{%- capture fts -%}{%- for f in fibres -%}{%- unless forloop.first %} · {% endunless -%}{% render 'ms-t', v: f %}{%- endfor -%}{%- endcapture -%}<span class="ms-rel__marks" title="{{ fts | strip | escape }}">""")])

# ── 2f. the words the site's script writes (the enquiry forms' notes, labels and hints): looked up in
#    the page as window.msT (snippets/ms-js-t, in the visitor's language only), and shown through T().
#    The names the form sends to the atelier stay in English.
_js = os.path.join(THEME, 'assets', 'ms-site.js')
_jt = read(_js)
_m = re.search(r'var TABS = \{(.*?)\n  \};', _jt, re.S)
assert _m, 'ms-site.js TABS'
_jstr = []
for _x in re.findall(r"'((?:[^'\\]|\\.)*)'", _m.group(1)):
    if re.search(r'[A-Za-z]{2}', _x) and _x not in _jstr:
        _jstr.append(_x)
_sub_js = [
    ("  var SLUG = { appointment:",
     "  var T = function (s) { var d = window.msT; return (d && d[s]) || s; };\n  var SLUG = { appointment:"),
    ("""    set('[data-ms-copy="note"]', copy.note);
    set('[data-ms-copy="five"]', copy.five);
    set('[data-ms-copy="six"]', copy.six);
    set('[data-ms-copy="notes"]', copy.notes);
    form.querySelectorAll('[data-ms-copy="sixHint"]').forEach(function (el) { el.setAttribute('placeholder', copy.sixHint); });""",
     """    set('[data-ms-copy="note"]', T(copy.note));
    set('[data-ms-copy="five"]', T(copy.five));
    set('[data-ms-copy="six"]', T(copy.six));
    set('[data-ms-copy="notes"]', T(copy.notes));
    form.querySelectorAll('[data-ms-copy="sixHint"]').forEach(function (el) { el.setAttribute('placeholder', T(copy.sixHint)); });"""),
    ("    set('[data-ms-copy=\"title\"]', copy.title || t);",
     "    set('[data-ms-copy=\"title\"]', T(copy.title || t));"),
    ("""      want = /proposal|quote|specif/.test(w) ? 'Request a proposal' : /brochure|catalogue/.test(w) ? 'Request brochure' : /call ?back/.test(w) ? 'Request callback'
        : /partner|represent/.test(w) ? 'Become a partner' : /trade/.test(w) ? 'Trade enquiry' : null;""",
     """      want = /proposal|quote|specif|propost|preventiv|предложен|смет/.test(w) ? 'Request a proposal' : /brochure|catalog|брошюр|каталог/.test(w) ? 'Request brochure' : /call ?back|richiam|перезвон|звонок/.test(w) ? 'Request callback'
        : /partner|represent|rappresent|партн|представ/.test(w) ? 'Become a partner' : /trade|professionist|профессионал/.test(w) ? 'Trade enquiry' : null;"""),
]
for _a, _b in _sub_js:
    assert _a in _jt or _b in _jt, _a[:60]
    _jt = _jt.replace(_a, _b, 1) if _b not in _jt else _jt
write(_js, _jt)
_snip = ['{%- comment -%} The words the site\'s script writes (assets/ms-site.js: the enquiry forms), in the visitor\'s',
         '  language, for its T(). Generated by bin/build_r23.py from the script itself. {%- endcomment -%}',
         "{%- assign ms_jl = request.locale.iso_code | slice: 0, 2 -%}",
         "{%- if ms_jl != 'en' -%}<script>window.msT = {"]
for _i, _x in enumerate(_jstr):
    _snip.append("{%%- capture ms_jx -%%}{%% render 'ms-t', v: %s %%}{%%- endcapture -%%}%s: {{ ms_jx | strip | json }}%s"
                 % (lit(_x), json.dumps(_x, ensure_ascii=False), ',' if _i < len(_jstr) - 1 else ''))
_snip.append('};</script>{%- endif -%}')
write(os.path.join(THEME, 'snippets', 'ms-js-t.liquid'), '\n'.join(_snip) + '\n')
for _lay in (os.path.join(THEME, 'layout', 'ms.liquid'), os.path.join(THEME, 'layout', 'theme.liquid')):
    _t = read(_lay)
    _a = """    <script src="{{ 'ms-site.js' | asset_url }}" defer="defer"></script>"""
    assert _a in _t, _lay
    if "render 'ms-js-t'" not in _t:
        _t = _t.replace(_a, "    {%- render 'ms-js-t' -%}\n" + _a, 1)
    write(_lay, _t)

# ── 2g. the sleep quiz (snippets/ms-quiz): its questions, answers and the closing sentence are written by
#    its script. They are looked up in the page (TT, in the visitor's language) and the sentence is one
#    whole template, so each language can order it in its own way.
_qz = os.path.join(THEME, 'snippets', 'ms-quiz.liquid')
_qt = read(_qz)
_why_old = """    var why = 'You sleep ' + (POSTURE[answers[0]] || 'in every position') + ', and you want a surface that feels ' + feel.toLowerCase() +
      '. We would build the ' + r[0] + ' from the ' + r[1] + ' collection at ' + firm.toLowerCase() + ' comfort, in ' + (SIZE_PHRASE[answers[3]] || 'a double') + '.';"""
_why_new = """    var FEEL = { 'Enveloping': 'enveloping', 'Balanced': 'balanced', 'Structured': 'structured' };
    var why = T('You sleep {posture}, and you want a surface that feels {feel}. We would build the {name} from the {collection} collection at {firm} comfort, in {size}.')
      .replace('{posture}', T(POSTURE[answers[0]] || 'in every position')).replace('{feel}', T(FEEL[feel] || 'balanced'))
      .replace('{name}', r[0]).replace('{collection}', r[1]).replace('{firm}', T(firm.toLowerCase())).replace('{size}', T(SIZE_PHRASE[answers[3]] || 'a double'));"""
_qsubs = [
    (_why_old, _why_new),
    ("      $('[data-ms-quiz-q]').textContent = q.q;", "      $('[data-ms-quiz-q]').textContent = T(q.q);"),
    ("        b.children[0].textContent = o[0];\n        b.children[1].textContent = o[1];",
     "        b.children[0].textContent = T(o[0]);\n        b.children[1].textContent = T(o[1]);"),
    ("    $('[data-ms-r=\"tagline\"]').textContent = r[2];", "    $('[data-ms-r=\"tagline\"]').textContent = T(r[2]);"),
    ("    $('[data-ms-r=\"firm\"]').textContent = firm;", "    $('[data-ms-r=\"firm\"]').textContent = T(firm);"),
    ("    $('[data-ms-r=\"size\"]').textContent = answers[3] === 'Made to measure' ? 'Made to measure' : (answers[3] || 'Double');",
     "    $('[data-ms-r=\"size\"]').textContent = T(answers[3] === 'Made to measure' ? 'Made to measure' : (answers[3] || 'Double'));"),
    ("    $('[data-ms-r=\"fibre\"]').textContent = fibre;", "    $('[data-ms-r=\"fibre\"]').textContent = T(fibre);"),
]
for _a, _b in _qsubs:
    assert _a in _qt or _b in _qt, _a[:60]
    _qt = _qt.replace(_a, _b, 1) if _b not in _qt else _qt
_ms = re.search(r'<script>\n\(function \(\) \{\n  var CDN = [^\n]*\n(.*?)\n</script>', _qt, re.S)
assert _ms, 'quiz script'
_qstr = []
for _x in re.findall(r"'((?:[^'\\]|\\.)*)'", _ms.group(1)):
    if (wordy(_x) or re.fullmatch(r'[a-z][a-z -]+', _x)) and not re.search(r'[=\[\]]|^ms:|^data-', _x) and _x not in _qstr \
            and _x not in ('a', 'h', 'li', 'span', 'button', 'style', 'click'):
        _qstr.append(_x)
_qstr += [x for x in ('You sleep {posture}, and you want a surface that feels {feel}. We would build the {name} from the {collection} collection at {firm} comfort, in {size}.',
                      'soft', 'firm', 'medium') if x not in _qstr]
_tt = ["  {%- capture ms_q -%}{% render 'ms-t', v: " + lit(_x) + " %}{%- endcapture -%}" + json.dumps(_x, ensure_ascii=False) + ": {{ ms_q | strip | json }}" + (',' if _i < len(_qstr) - 1 else '')
       for _i, _x in enumerate(_qstr)]
_head = "<script>\n(function () {\n  var TT = {\n" + '\n'.join(_tt) + "\n  };\n  var T = function (s) { return TT[s] || s; };\n"
if 'var TT = {' not in _qt:
    _qt = _qt.replace("<script>\n(function () {\n", _head, 1)
write(_qz, _qt)

# ms-tr: a setting that no longer holds its English default is still looked up
tr = os.path.join(THEME, 'snippets', 'ms-tr.liquid')
t = read(tr)
t2 = t.replace("  if lang != 'en' and value == default\n    echo key | t\n  else\n    echo value\n  endif",
               "  if lang != 'en' and value == default\n    echo key | t\n  else\n    render 'ms-t', v: value\n  endif")
write(tr, t2)

# ── 2h. the stockist regions: the English names are what each place's setting holds, so the list the
#    places are matched against stays English and only the names shown are translated
_sl = os.path.join(THEME, 'sections', 'ms-stockists.liquid')
_sub1(_sl, [
    ("  capture regions\n    render 'ms-t', v: 'Europe,Middle East,Americas,Asia Pacific'\n  endcapture\n  assign regions = regions | split: ','\n",
     "  capture region_names\n    render 'ms-t', v: 'Europe,Middle East,Americas,Asia Pacific'\n  endcapture\n  assign region_names = region_names | split: ','\n"
     "  assign regions = 'Europe,Middle East,Americas,Asia Pacific' | split: ','\n"),
    ('<h3 class="ms-sl__rhead">{{ region }}</h3>', '<h3 class="ms-sl__rhead">{{ region_names[forloop.index0] | default: region }}</h3>'),
    ('aria-pressed="false">{{ region }}</button>', 'aria-pressed="false">{{ region_names[forloop.index0] | default: region }}</button>'),
])

# ── 3. the translations, into the locale files
def jsonc_load(p):
    s = read(p)
    head = ''
    m = re.match(r'\s*/\*.*?\*/\s*', s, re.S)
    if m:
        head, s = m.group(0), s[m.end():]
    return head, json.loads(s)


def pieces(s, n=1000):
    """at most n characters each, broken after a closing tag or a sentence where possible"""
    out = []
    while len(s) > n:
        cut = max(s.rfind('</p>', 0, n - 4) + 4 if s.rfind('</p>', 0, n - 4) > 0 else -1,
                  s.rfind('. ', 0, n) + 2 if s.rfind('. ', 0, n) > 0 else -1)
        if cut <= 0:
            cut = s.rfind(' ', 0, n) + 1 or n
        out.append(s[:cut]); s = s[cut:]
    out.append(s)
    return out


def pieces_n(s, n, size=1000):
    """s in exactly n pieces of at most size characters (n is at least what pieces() needs), cut
    after a closing tag, a sentence or a word near each n-th of its length"""
    out = []
    for j in range(n - 1, 0, -1):
        aim = len(s) // (j + 1)
        lo, hi = max(1, len(s) - j * size), min(size, len(s) - j)
        best = -1
        for mark, w in (('</p>', 4), ('. ', 2), (' ', 1)):
            c = s.rfind(mark, lo - w, min(hi, aim + 200) - w + 1)
            if c >= 0 and lo <= c + w <= hi:
                best = c + w
                break
        if best < 0:
            best = max(lo, min(hi, aim))
        out.append(s[:best]); s = s[best:]
    out.append(s)
    return out


# Every translated text has the same keys in all three files (English holds its own text), so
# Theme Check finds the locales matching, and Translate & Adapt lists them as theme content. A key
# a language lacks would fall back to the English file, so no language has fewer pieces than another.
n_keys = {}
tables = {}
for loc in ('it', 'ru'):
    src = os.path.join(os.environ.get('TR_DIR') or os.path.join(HERE, 'tr'), loc + '.json')
    tables[loc] = json.load(open(src, encoding='utf-8')) if os.path.exists(src) else {}
txs = {'en': {}, 'it': {}, 'ru': {}}
for en in sorted(set(tables['it']) | set(tables['ru'])):
    vals = {'en': en, 'it': tables['it'].get(en) or en, 'ru': tables['ru'].get(en) or en}
    if vals['it'] == en and vals['ru'] == en:
        continue
    n = max(len(pieces(v)) for v in vals.values())
    k = key(en)
    for loc, v in vals.items():
        parts = pieces_n(v, n)
        assert len(parts) == n and all(parts) and all(len(x) <= 1000 for x in parts) and ''.join(parts) == v, (loc, en[:60])
        txs[loc][k + '_html'] = parts[0]
        for i, part in enumerate(parts[1:], 2):
            txs[loc]['%s_%d_html' % (k, i)] = part
for loc, fname in (('en', 'en.default.json'), ('it', 'it.json'), ('ru', 'ru.json')):
    p = os.path.join(THEME, 'locales', fname)
    raw = read(p)
    if loc == 'en':
        # the English file keeps its comments (// …), so its key is written into the text itself
        body = json.dumps(txs['en'], ensure_ascii=False, indent=4).replace('\n}', '\n  }')
        body = re.sub(r'(?m)^    ', '    ', body)
        raw2 = re.sub(r',\n  "ms_tx": \{.*?\n  \}\n\}\s*$', '\n}\n', raw, flags=re.S)
        raw2 = re.sub(r'\n\}\s*$', ',\n  "ms_tx": ' + body.replace('\\', '\\\\') + '\n}\n', raw2, count=1)
        write(p, raw2)
    else:
        head, d = jsonc_load(p)
        d['ms_tx'] = txs[loc]
        write(p, head + json.dumps(d, ensure_ascii=False, indent=2) + '\n')
    n_keys[loc] = len(txs[loc])

flush()
print('round 23: %d outputs, %d assignments, %d written texts and %d texts in code through ms-t; keys %s; %d files changed' % (n_out, n_assign, n_lit, n_code[0], n_keys, changed))
