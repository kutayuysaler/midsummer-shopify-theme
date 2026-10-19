"""Text still in English on the pages rendered in another language (rt5/<locale>/*.html): every
visible text node, alt, title, aria-label, placeholder and meta description that holds English
words and did not come through the translation. With the marked dummy translation (⟪…⟫), anything
unmarked did not pass through ms-t.
usage: python3 tools/tr_leftover.py it [--marked] > report"""
import glob, html, os, re, sys, collections
from html.parser import HTMLParser
SP = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
loc = sys.argv[1]
marked = '--marked' in sys.argv
EN = re.compile(r"\b(the|and|of|with|for|your|our|by|in|to|a|is|are|from|each|every|bed|beds|mattress|topper|boxspring|more|see|all|book|enquir\w*|request|view|read|open|close|next|previous|back|made|hand|sleep|natural|fibres?|wool|silk|linen|cotton|size|sizes|collection|collections|cloth|colours?|price|order|contact|journal|showroom|atelier)\b", re.I)


class P(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.skip = 0; self.out = []; self.stack = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ('script', 'style', 'noscript', 'template', 'svg') and not (tag == 'svg'):
            self.skip += 1
        if tag == 'svg':
            self.stack.append('svg')
        for k in ('alt', 'title', 'aria-label', 'placeholder', 'data-ms-note'):
            if a.get(k):
                self.out.append(('@' + k, a[k]))
        if tag == 'meta' and a.get('name') in ('description',) or a.get('property') in ('og:title', 'og:description'):
            if a.get('content'):
                self.out.append(('@meta', a['content']))
    def handle_endtag(self, tag):
        if tag in ('script', 'style', 'noscript', 'template'):
            self.skip = max(0, self.skip - 1)
    def handle_data(self, d):
        if not self.skip and d.strip():
            self.out.append(('text', d.strip()))


agg = collections.defaultdict(set)
for f in sorted(glob.glob(os.path.join(SP, 'rt5', loc, '*.html'))):
    p = P(); p.feed(open(f, encoding='utf-8').read())
    for kind, t in p.out:
        t = re.sub(r'\s+', ' ', t)
        if marked and ('⟪' in t or '⟫' in t):
            continue
        if not EN.search(t) or len(t) < 3:
            continue
        agg[(kind, t[:140])].add(os.path.basename(f)[:-5])
for (kind, t), pages in sorted(agg.items(), key=lambda x: -len(x[1])):
    print('%3d %-12s %s   [%s]' % (len(pages), kind, t, ' '.join(sorted(pages)[:3])))
