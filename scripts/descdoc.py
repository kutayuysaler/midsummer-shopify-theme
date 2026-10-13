# DESCRIPTIONS.md for the owner: what in each product's admin description the theme hides (the build),
# and what else to correct there. From dl/products_aug2025.json (the store's export of 14 Aug 2025).
import json, re, html, sys
d = json.load(open(sys.argv[1]))
CON = re.compile(r"\b(layers?|strat[oi]|springs?|micro-?springs?|microsprings?|mini-?molle|molle|sommier|knots?|nodi|coils?|pocket(ed)?|insacchettat\w*|hourglass|clessidra|core|nucleo)\b", re.I)
SKIP = re.compile(r"dreamy springs|box-?springs?|spring\s*(/|and|e)\s*summer|\b(in|of|the|this|every|early|late)\s+spring\b", re.I)
def lines(b):
    b = re.sub(r'<!--.*?-->', '', b, flags=re.S)
    b = re.sub(r'<(br|/p|/div|/li|/h\d)[^>]*>', '\n', b, flags=re.I)
    b = html.unescape(re.sub(r'<[^>]+>', ' ', b)).replace('\xa0', ' ')
    return [re.sub(r'\s+', ' ', l).strip() for l in b.split('\n') if l.strip()]
rows = []
for h, x in sorted(d.items(), key=lambda kv: kv[1]['title']):
    hits = [s for l in lines(x['body_html']) for s in re.split(r'(?<=[.!?])\s+', l) if CON.search(SKIP.sub('', s))]
    other = []
    if 'Midsummer-Milano' in x['body_html']:
        other.append('it writes "Midsummer-Milano"; the site shows "Midsummer Milano"')
    if re.search(r'click here', x['body_html'], re.I):
        other.append('a "Click here" link; the site shows it as "More at" and the address')
    if re.search(r'polyurethane', x['body_html'], re.I):
        other.append('it names polyurethane. The site no longer says "natural fibres only" or "nothing synthetic"; confirm what is inside')
    if h in ('test-product', 'langify_image_container'):
        other.append('a placeholder product: keep it unpublished, or delete it')
    if hits or other:
        rows.append((x['title'], h, hits, other))
out = ['# Product descriptions: what to edit in admin', '',
       "These notes come from the store's product descriptions as exported on 14 August 2025. Edit them in **Products → [product] → Description**. The theme can only show the text it is given; it cannot correct it.", '',
       "On the product page, the theme hides any sentence that names springs, layers, the core or the inside of the bed. It also hides any list under a heading of that kind. The setting is **Keep the build private in descriptions** and is on by default. The hidden words are still in the page source, in the search-engine description and in the store's product feed, so please remove them in admin as well.", '',
       'Each bullet below is a sentence the page now hides. Lines that begin with "Also" are other things to correct.', '']
for t, h, hits, other in rows:
    out += ['## %s (`%s`)' % (t, h), '']
    out += ['- %s' % s[:300] for s in hits[:14]]
    if len(hits) > 14:
        out.append('- … and %d more lines of the same kind.' % (len(hits) - 14))
    out += ['- Also: %s.' % o for o in other]
    out.append('')
open(sys.argv[2], 'w').write('\n'.join(out))
print(len(rows), 'products')
