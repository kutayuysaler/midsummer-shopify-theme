"""The store's own special pages and per-product templates, rebuilt in the Midsummer design.
Template names match the ones the live store already assigns, so those pages switch by themselves."""
import json, os, re, shutil, sys, glob
sys.path.insert(0, os.path.dirname(__file__))
from conv import SP, THEME
from layers import LAYERS, PADDING, blocks_for

HEAD = '/*\n * Midsummer Milano: %s\n */\n'
EXTRA = SP + '/bin/extra'
for f in glob.glob(EXTRA + '/*.liquid'):
    shutil.copy(f, THEME + '/sections/' + os.path.basename(f))
# the map's code and world outline as snippets, so the locator renders them inline
for src_name, snip in (('ms-atlas-vendor.js', 'ms-atlas-vendor'), ('ms-world-110m.json', 'ms-world-110m')):
    body = open(SP + '/vendor/' + src_name).read() if os.path.exists(SP + '/vendor/' + src_name) else open(THEME + '/assets/' + src_name).read()
    assert '{% endraw' not in body
    open(THEME + '/snippets/%s.liquid' % snip, 'w').write('{% raw %}' + body.strip() + '{% endraw %}')

CDN = 'https://midsummer-milano.com/cdn/shop/files/'
LIVE = 'https://midsummer-milano.com'
DROPBOX = 'https://www.dropbox.com/scl/fo/y4pley49zghabv8gl14d5/AHqqaDI-dUed5LFO2lluPYs?rlkey=sv0gr78ax2c4oyb01p76vne16&st=r5604kll&dl=0'


def write(name, note, sections, layout='ms'):
    data = {'layout': layout, 'sections': {}, 'order': []}
    for i, (typ, settings, blocks) in enumerate(sections):
        key = 's%02d' % (i + 1)
        entry = {'type': typ, 'settings': settings}
        if blocks:
            entry['blocks'] = {}
            entry['block_order'] = []
            for j, (btype, bset) in enumerate(blocks):
                bid = '%s_%02d' % (btype, j + 1)
                entry['blocks'][bid] = {'type': btype, 'settings': bset}
                entry['block_order'].append(bid)
        data['sections'][key] = entry
        data['order'].append(key)
    open('%s/templates/%s.json' % (THEME, name), 'w').write(HEAD % note + json.dumps(data, indent=2, ensure_ascii=False) + '\n')


# ── Loro Piana Interiors ───────────────────────────────────────────
# the cloths our systems are made in, with their colours by name (bin/lp_data.py: the house's
# catalogue and price lists, Loro Piana Interiors' own list, the cards kept at the atelier)
from lp_data import FABRICS, ANCHOR, CLOTH, FIBRES as SYSTEM_FIBRES, NOTES as SYSTEM_NOTES
LP_BLOCKS = []
for f in FABRICS:
    plain = {'linen': '#E2DACE', 'wool': '#C9B8A6', 'boucle': '#CDBEAA'}[f['texture']]
    fb = {'name': f['name'], 'anchor': ANCHOR[f['key']], 'code': f['code'], 'composition': f['comp'],
          'systems': f['systems'], 'text': f['text'], 'texture': f['texture'], 'color': plain}
    if f.get('image'):
        fb['image_fallback'] = f['image']
        fb['image_caption'] = f.get('caption', '')
    LP_BLOCKS.append(('fabric', {k: v for k, v in fb.items() if v}))
    for (n, h, small, large) in f['colours']:
        cb = {'name': n, 'color': h, 'image_fallback': small}
        if large:
            cb['large_fallback'] = large
        LP_BLOCKS.append(('colour', cb))
assert len(LP_BLOCKS) <= 50, len(LP_BLOCKS)
write('page.loro-piana-interiors', 'Loro Piana Interiors, the cloths the systems are made in.', [
    ('ms-banner', {'image_fallback': 'ms-photo-flora-wide.jpg', 'eyebrow': 'Upholstery', 'use_page_title': False,
                   'heading': 'Loro Piana Interiors', 'height': 'tall',
                   'text': 'The cloths our systems are made in, colour by colour.'}, None),
    ('ms-statement', {'eyebrow': 'Loro Piana Interiors', 'use_content': False,
                      'heading': 'Where a system calls for it, we make it in Loro Piana Interiors: linen for summer, wool and cashmere for winter.',
                      'text': '<p>Mystic River, Connemara, Altai, Wish, Cardi, Ely’s Harbour, Bangor and Shadan: each chosen for the system it dresses, each in its own colours. The others are covered in natural linen and cotton.</p>'}, None),
    ('ms-lp-fabrics', {'eyebrow': 'The cloths', 'heading': 'The cloths our systems are made in.',
                       'text': '<p>Every cloth here is on one of our systems, with the colours we make it in. Choose a colour to see it larger, and ask for it: the atelier on Via Andegari holds the cards, and sends samples by post.</p>',
                       'footnote': 'Colours on screen are indicative: the Mystic River colours are photographed; the others are drawn from the Loro Piana Interiors cards at the atelier, on a photographed weave. Other Loro Piana Interiors cloths, and your own, on request.'},
     LP_BLOCKS),
    ('ms-statement', {'tone': 'stone', 'eyebrow': 'Seasonal upholstery',
                      'heading': 'Dressed for both seasons.',
                      'text': '<p>On Flora and Top, wool and cashmere dress the winter face and linen the summer face, so the bed is turned when the season changes, not replaced.</p>'}, None),
    ('ms-image-pair', {'eyebrow': 'Paisley', 'heading': 'Shadan linen and Katai silk.',
                       'image_1': 'shopify://shop_images/Paisleydettaglio.jpg', 'fallback_1': CDN + 'Paisleydettaglio.jpg?v=1788246821&width=1400',
                       'caption_1': 'Shadan, a paisley linen by Loro Piana Interiors, on the topper of Paisley.',
                       'fallback_2': 'ms-graded-paisley-red.jpg',
                       'caption_2': 'Paisley: Shadan on the topper and the border of the mattress; Katai, a pure silk, on the boxspring.'}, None),
    ('ms-collection-cards', {'eyebrow': 'Where you will find it', 'heading': 'Across the three collections', 'link_label': 'Compare the collections →'},
     [('collection', {'handle': 'essentials', 'title': 'Essentials', 'numeral': 'I', 'image_fallback': 'ms-photo-glass-house.jpg',
                      'text': 'Capri, in Mystic River, or two-tone with Connemara.'}),
      ('collection', {'handle': 'signature', 'title': 'Signature', 'numeral': 'II', 'image_fallback': 'ms-graded-ochre-room.jpg',
                      'text': 'Dreamy in Mystic River; Brera in Connemara, edged in Altai.'}),
      ('collection', {'handle': 'icons', 'title': 'Icons', 'numeral': 'III', 'image_fallback': 'ms-graded-arches.jpg',
                      'text': 'Roma, Storage, Flora, Bellini, Top, Giotto Round and Paisley, each in its own cloth.'})]),
    ('ms-cta-band', {'eyebrow': 'The atelier', 'heading': 'See the cloths in Milano.',
                     'text': '<p>The Loro Piana Interiors cards are at the atelier on Via Andegari. Choose against the bed, or ask us for samples by post.</p>',
                     'button': 'Book a private appointment', 'button_enquire': True,
                     'link_label': 'Request the brochure', 'link_enquire': True}, None),
])

# ── Download the Dream ─────────────────────────────────────────────
WORKS = [
    ('Tolouse_Lautrec.png', 'Henri de Toulouse-Lautrec', 'Whispers in Yellow', 'Two figures rest on a Midsummer mattress, elevating Lautrec’s intimate Paris settings with refined upholstery and artisan details.'),
    ('Frida_Kahlo.png', 'Frida Kahlo', 'The Sacred Room', 'Amid roses and symbolism, our bed becomes part of Kahlo’s inner world — a sanctuary for identity, beauty, and restorative sleep.'),
    ('Casorati.png', 'Felice Casorati', 'Reading in Silence', 'Architectural stillness meets soft elegance; the bed serves as a pedestal for focused calm.'),
    ('Henry_Rousseau.png', 'Henri Rousseau', 'Where Tigers Sleep', 'A surreal landscape where even the wild find peace — showing how natural materials bring elemental comfort.'),
    ('William_Morris.png', 'William Morris', 'The Botanical Reverie', 'A fox naps amid ornate flora, proving luxury can speak nature’s language.'),
    ('Renoir.png', 'Pierre-Auguste Renoir', 'Impression at Rest', 'Blooming greens, soft light, and effortless romance surround a bed built for generations.'),
    ('Magritte.png', 'René Magritte', 'The Weight of Dreams', 'Dreams feel weightless yet meaningful — mirroring the balanced support of natural fibre mattresses.'),
    ('David_Hockney.png', 'David Hockney', 'Lines of Lightness', 'Vivid geometry meets calming comfort; proof that modern art and heritage craft can coexist.'),
]
write('page.download-the-dream', 'Download the Dream: the Art of Rest.', [
    ('ms-banner', {'image': 'shopify://shop_images/Henry_Rousseau.png', 'eyebrow': 'The Art of Rest', 'heading': 'Download the Dream',
                   'height': 'tall', 'text': 'Art inspired beds by Midsummer-Milano — where luxury Italian design meets timeless sleep.',
                   'button': 'Download the series', 'link': DROPBOX, 'new_tab': True}, None),
    ('ms-statement', {'eyebrow': 'Why we made it', 'heading': 'A bed is more than furniture; it is a cultural object.',
                      'text': '<p>A bed lives in the intimacy of your home. In <strong>“The Art of Rest”</strong> we place our designer beds inside re-imagined masterpieces, linking bedroom art to daily wellbeing. Each downloadable image shows how comfort, beauty, and storytelling unite in a single piece of sustainable craftsmanship.</p><p><em>Free high-resolution downloads: use them as mood-board inspiration, wallpapers, or a gentle reminder that rest itself can be a work of art.</em></p>'}, None),
    ('ms-art-gallery', {'eyebrow': 'Eight masterpieces, re-imagined', 'heading': 'The series',
                        'link_label': 'Download all, in high resolution ↗', 'link': DROPBOX},
     [('work', {'image': 'shopify://shop_images/' + f, 'artist': a, 'title': t, 'text': '<p>%s</p>' % x}) for f, a, t, x in WORKS]),
    ('ms-cta-band', {'tone': 'stone', 'eyebrow': 'Free to download', 'heading': 'The whole series, in high resolution.',
                     'text': '<p>Download the entire bedroom art series and learn how our luxury Italian beds are handcrafted for longevity, sustainability, and heirloom value.</p>',
                     'button': 'Download the images', 'button_link': DROPBOX, 'button_enquire': False, 'new_tab': True}, None),
    ('ms-cta-band', {'tone': 'ink', 'eyebrow': 'Your own', 'heading': 'Ready to turn your bedroom into a masterpiece?',
                     'text': '<p>Talk to our artisans about a bespoke Midsummer bed, made by hand in Italy to your dimensions.</p>',
                     'button': 'Book a private appointment', 'button_enquire': True,
                     'link_label': 'Our beds', 'link_place': 'collections'}, None),
])

# ── Salone del Mobile 2026 ─────────────────────────────────────────
write('page.salone-2026', 'Salone del Mobile 2026: this year, the answer is Paisley.', [
    ('ms-banner', {'image_fallback': 'ms-graded-paisley-red.jpg', 'eyebrow': 'Salone del Mobile 2026 · Via Andegari 4, Milan · 21–26 April',
                   'heading': 'This year, the answer is Paisley.', 'height': 'full',
                   'text': 'Every year, we ask ourselves the same question: what can we make better?',
                   'button': 'Discover Paisley', 'product_handle': 'paisley', 'link': 'shopify://collections/all'}, None),
    ('ms-statement', {'eyebrow': 'Salone del Mobile 2026', 'use_content': False,
                      'heading': 'Every year, we ask ourselves the same question: what can we make better?',
                      'text': '<p>This year, the answer is Paisley: Loro Piana Interiors Shadan in silk and linen, over baby alpaca, wool and linen. Warm in winter, breathable in summer.</p><p>Presented at the atelier, Via Andegari 4, Milan, from 21 to 26 April.</p>',
                      'link_label': 'Book a private appointment', 'enquire': True}, None),
    ('ms-image-pair', {'eyebrow': 'Paisley', 'heading': 'An extraordinary fabric, met by a precise design vision.',
                       'fallback_1': 'ms-graded-paisley-red.jpg', 'caption_1': 'Paisley, in Loro Piana Interiors Shadan.',
                       'image_2': 'shopify://shop_images/Paisleydettaglio.jpg', 'fallback_2': CDN + 'Paisleydettaglio.jpg?v=1788246821&width=1400', 'caption_2': 'Silk and linen, sewn by hand.'}, None),
    ('ms-video-band', {'video': 'shopify://files/videos/Salone Del Mobile Page Video.mp4', 'caption': 'Salone del Mobile, at the atelier on Via Andegari.'}, None),
    ('ms-cta-band', {'tone': 'ink', 'eyebrow': 'The atelier', 'heading': 'Via Andegari 4, Milano.',
                     'text': '<p>Come and lie down on Paisley at the atelier, by appointment, Monday to Friday.</p>',
                     'button': 'Book a private appointment', 'button_enquire': True,
                     'link_label': 'Salone 2025 in the Journal', 'link': LIVE + '/blogs/press/midsummer-milano-at-salone-del-mobile-2025-a-journey-through-design-nature-and-well-being'}, None),
])

# ── Journal articles and the collaborations blog ───────────────────
write('article.salonedelmobile', 'A journal note with its film.', [
    ('ms-article', {}, None),
    ('ms-video-band', {'video': 'shopify://files/videos/Salone Del Mobile Page Video.mp4', 'caption': 'Salone del Mobile, at the atelier on Via Andegari.'}, None),
])
write('article.greenproductaward', 'A journal note with its photographs.', [
    ('ms-article', {}, None),
    ('ms-gallery', {'eyebrow': 'Green Product Award', 'heading': 'The Top System'},
     [('photo', {'image': 'shopify://shop_images/1829-%d-top-bed-system.jpg' % n}) for n in (2, 0, 5, 6, 4)]),
])
write('article.sleep-assessment', 'A journal note with Find your Midsummer.', [
    ('ms-article', {}, None),
    ('ms-quiz', {}, None),
])
JOURNAL_LIST = json.loads(re.sub(r'^\s*/\*.*?\*/', '', open(THEME + '/templates/blog.json').read(), flags=re.S))
write('blog.collaborations', 'Collaborations: the Midsummer journal, opened by the current collaboration.', [
    ('ms-banner', {'image': 'shopify://shop_images/DSC05117.jpg', 'eyebrow': 'Collaboration', 'height': 'tall',
                   'heading': 'Midsummer-Milano & Strega del Castello',
                   'text': 'Introducing our new bed perfumes, Lavanda Barocca and Agrumi di Sicilia.',
                   'button': 'Discover the perfumes', 'product_handle': 'midsummer-milano-x-la-strega-del-castello',
                   'link': 'shopify://collections/all'}, None),
    ('ms-journal-list', {}, None),
])

# ── Per-product templates: every product keeps its own fibres ──────
old = json.load(open(SP + '/pv3/product_templates.json'))
NAME = {'Cheviot': 'Cheviot Wool', 'Camelhair': 'Camel Hair', 'Yak': 'Yak Hair'}
NOTE = {'Baby Alpaca': 'Temperature · Hypoallergenic', 'Cheviot Wool': 'Support · Temperature', 'Horsehair': 'Support · Breathability',
        'Yak Hair': 'Warmth · Softness', 'Vicuña': 'Softness · Warmth', 'Cashmere': 'Warmth without weight',
        'Mongolian Cashmere': 'Warmth without weight', 'Mohair': 'Warmth without weight'}
NOTE.update({'Silk': 'Temperature · Softness', 'Linen': 'Breathability · Freshness', 'Cotton': 'Breathability', 'Ingeo': 'Breathability · Freshness',
             'Wool': 'Support · Temperature', 'Falkland Wool': 'Support · Temperature', 'Alpaca': 'Temperature · Hypoallergenic',
             'Camel Hair': 'Warmth · Temperature', 'Vegetable Horsehair': 'Support · Breathability', 'Orange Fiber': 'Freshness · Breathability'})
FIBRE_NOTE = NOTE
base_product = json.loads(re.sub(r'^\s*/\*.*?\*/', '', open(THEME + '/templates/product.json').read(), flags=re.S))
product_types = [base_product['sections'][k]['type'] for k in base_product['order'] if base_product['sections'][k]['type'] not in ('ms-product-fibres', 'ms-qa')]
# what each product is, where the name alone does not say (the rest: sleep system, or topper by name)
KIND = {'capri': 'boxspring_mattress', 'bellini': 'boxspring', 'storage': 'storage', 'giotto': 'round'}
AWARD = {'top-2': 'Green Product Award 2025'}
PROPER = {'Cheviot', 'Mongolian', 'Falkland', 'Ingeo', 'Orange', 'Fiber'}
def fibre_phrase(names):
    words = []
    for n in names:
        n = ' '.join(w if w in PROPER else w.lower() for w in n.split())
        words.append('Falkland wool' if n == 'Falkland' else n)
    return words[0] if len(words) == 1 else ', '.join(words[:-1]) + ' and ' + words[-1]
# the questions asked before an order, on every bed's page; [product] becomes the product's name
from lp_data import CRAFT, CRAFT_SHARED_KIND, CRAFT_INTRO, CRAFT_PARTS, CRAFT_OPT, CRAFT_TEXT, part_seasons
def craft_settings(suffix):
    """Inside the bed, told for this system: each part's own fibres and cloth (bin/lp_data.py); the
    parts a mattress, a topper or a boxspring does not include, told from its side; each part's
    fibres by face where its sentence names them."""
    st = {'link_label': 'The fibres inside', 'link_place': 'materials'}
    c = CRAFT.get(suffix)
    if not c:
        return st
    st['text'] = CRAFT_TEXT.get(suffix) or CRAFT_INTRO[c['kind']]
    st['fibres_label'] = 'Its fibres'
    for i, part in enumerate(('topper', 'mattress', 'base'), 1):
        lead, points, fibres = c.get(part) or CRAFT_SHARED_KIND[c['kind']][part]
        st['part%d_lead' % i] = lead
        st['part%d_text' % i] = lead
        st['part%d_points' % i] = '\n'.join(points)
        st['part%d_fibres' % i] = ', '.join(fibres)
        ss = part_seasons(lead, points)
        st['part%d_winter' % i] = ', '.join(ss[0]) if ss else ''
        st['part%d_summer' % i] = ', '.join(ss[1]) if ss else ''
    return st
def product_qa(fibre_names, cloth=''):
    qa = []
    if fibre_names:
        qa.append(('qa', {'q': 'What is [product] made of?', 'a': '<p>[product] is made by hand in Italy from natural fibres: %s. %sIt is made to order by two artisans, start to finish.</p>' % (fibre_phrase(fibre_names), cloth + ' ' if cloth else '')}))
    qa += [
        ('qa', {'q': 'Can [product] be made to my dimensions?', 'a': '<p>Yes. Dimensions, heights, fibres, fabric and comfort level are specification decisions rather than exceptions. Non-standard widths, heights and radii, including round, carry no tooling charge.</p>'}),
        ('qa', {'q': 'How is the comfort chosen?', 'a': '<p>It depends on how you sleep. On your side, hips and shoulders need to sink a little; on your back, the lumbar curve needs support; on your front, a flatter, firmer surface keeps the neck neutral. The five questions of Find your Midsummer suggest a system, and at the atelier you choose by lying down.</p>'}),
        ('qa', {'q': 'Can I try [product] before ordering?', 'a': '<p>Yes. Come and lie down at the atelier, Via Andegari 4, Milano, Monday to Friday, 09:00–12:00 and 13:00–18:00. We can also meet by video. Appointments are confirmed by email within one working day.</p>'}),
        ('qa', {'q': 'How long does it take to make?', 'a': '<p>Production and delivery windows are confirmed on enquiry, because each system is made to order. Delivery is white-glove: the bed is brought into the room, assembled and dressed by our own team.</p>'}),
        ('qa', {'q': 'Why is the price on request?', 'when_hidden': True, 'a': '<p>Because every system is made to order, and the price follows the specification: dimensions, height, fibres, fabric and comfort level. We quote after the consultation.</p>'}),
        ('qa', {'q': 'What is the 15 + 15 service?', 'a': '<p>Our regeneration service. At year fifteen the mattress returns to the Italian artisans who made it, and its comfort, integrity and life are restored for the fifteen years ahead, rather than the system being replaced.</p>'}),
    ]
    return ('ms-qa', {'anchor': 'questions', 'eyebrow': 'Questions', 'heading': 'Before you order.', 'link_label': 'All questions', 'link_place': 'faq'}, qa)
SPECS = {'topper-roma': '<p><strong>Single</strong> 100 × 200 × 10 cm</p><p><strong>Queen</strong> 153 × 203 × 10 cm</p><p><strong>Small Double</strong> 160 × 200 × 10 cm</p><p><strong>Double</strong> 180 × 200 × 10 cm</p><p><strong>King</strong> 193 × 203 × 10 cm</p><p><strong>Double Extra</strong> 200 × 200 × 10 cm</p>',
         # the 2026 catalogue's toppers page: two products on the store, the Medium & High and the Thin
         'topper-high': '<p><strong>High</strong> 9–10 cm, soft</p><p><strong>Medium</strong> 5 cm, soft</p>',
         'topper-thin': '<p><strong>Thin</strong> 3 cm, medium to firm</p>'}
# every system's fibres come from the 2026 catalogue and price lists (bin/lp_data.py)
SOURCED = SYSTEM_FIBRES
made = []
# the toppers the store sells as their own products (their templates exist so the store can give
# them; until it does, snippets/ms-sys-data tells them apart on the Roma topper's template)
for k in ('topper-high', 'topper-thin'):
    old.setdefault(k, {'mats': [], 'tabs': [], 'texts': [], 'other': []})
PRODUCT_TPLS = dict(old)
SYS_DATA = {}
for suffix, info in old.items():
    if suffix in ('', 'appointment'):
        continue
    if suffix == 'perfumes':
        write('product.perfumes', 'Bed perfumes, with Strega del Castello.', [
            ('ms-banner', {'image': 'shopify://shop_images/DSC05117.jpg', 'eyebrow': 'Scented bed perfumes', 'height': 'medium',
                           'heading': 'Midsummer-Milano & Strega del Castello', 'text': 'Lavanda Barocca & Agrumi di Sicilia'}, None),
            ('ms-product-main', {'kind': 'perfume', 'cover_value': '', 'comfort_value': '', 'f1_label': 'Made', 'f1_value': 'Handcrafted in Italy through sustainable and artisanal production methods',
                                 'f2_label': 'Ingredients', 'f2_value': 'Natural, plant-based ingredients for a pure and gentle scent',
                                 'f3_label': 'Use', 'f3_value': 'Safe for linens; made for pillows and sheets',
                                 'price_text': 'On request, from the atelier.'}, None),
            ('ms-product-related', {}, None),
        ])
        made.append(suffix)
        continue
    fibres = []
    for n in SYSTEM_FIBRES.get(suffix) or [NAME.get(m, m) for (m, img) in info['mats']]:
        n2 = NAME.get(n, n)
        b = {'name': n2}   # the drawing comes from the house's own marks (snippets/ms-fibre-mark)
        if NOTE.get(n2):
            b['note'] = NOTE[n2]
        fibres.append(('fibre', b))
    if not fibres and suffix in SOURCED:
        fibres = [('fibre', dict({'name': n}, **({'note': NOTE[n]} if NOTE.get(n) else {}))) for n in SOURCED[suffix]]
    secs = []
    for t in product_types:
        if t == 'ms-product-main':
            ms = {'specs': SPECS[suffix]} if suffix in SPECS else {}
            if suffix in CLOTH:
                ms['cover_value'] = CLOTH[suffix]['cover']
            if suffix in KIND:
                ms['kind'] = KIND[suffix]
            if suffix in AWARD:
                ms['award'] = AWARD[suffix]
            secs.append((t, ms, fibres))
        elif t == 'ms-product-related':
            secs.append(product_qa([b['name'] for _, b in fibres], CLOTH.get(suffix, {}).get('cloth', '')))
            secs.append((t, {}, None))
        elif t == 'ms-product-build':
            # the faces' fibres are read from snippets/ms-sys-data, not kept as settings
            secs.append(('ms-craft', {k: v for k, v in craft_settings(suffix).items() if not k.endswith(('_winter', '_summer'))}, None))
        else:
            secs.append((t, {}, None))
    write('product.' + suffix, 'the product, with its own fibres and its own layers.', secs)
    made.append(suffix)
    SYS_DATA[suffix] = dict(fibres=[(b['name'], b.get('note', '')) for _, b in fibres], specs=SPECS.get(suffix, ''),
                            cover=CLOTH.get(suffix, {}).get('cover', ''), craft=craft_settings(suffix),
                            made=product_qa([b['name'] for _, b in fibres], CLOTH.get(suffix, {}).get('cloth', ''))[2][0][1]['a'] if fibres else '')
# each system's data by key, for a product on another system's template or on the default one
# (snippets/ms-sys-data, read by ms-product-main, ms-craft and ms-qa when ms-kind's key differs)
def lq(s):
    assert '{%' not in s and '{{' not in s, s
    return s
# the house's boxsprings: the base alone, the rest in outline (ms-craft finds them by handle)
for k in CRAFT:
    if k == 'base' or k.startswith('base-'):
        SYS_DATA[k] = dict(fibres=[], specs='', cover='', craft=craft_settings(k), made='')
sd = ["{%- comment -%} A system's own data by key: part 'fibres' (name~note|…), 'specs', 'cover', 'made', 'text', 'kind' (system, mattress, topper or base), or 'p1'–'p3' with f 'lead', 'points', 'fibres', 'winter' or 'summer'. Generated by bin/build_extra.py from bin/lp_data.py. {%- endcomment -%}",
      "{%- case key -%}"]
for k, d in sorted(SYS_DATA.items()):
    c = d['craft']
    sd.append("{%%- when '%s' -%%}{%%- case part -%%}" % k)
    sd.append("{%%- when 'fibres' -%%}%s" % lq('|'.join('%s~%s' % (n, note) for n, note in d['fibres'])))
    sd.append("{%%- when 'specs' -%%}%s" % lq(d['specs']))
    sd.append("{%%- when 'cover' -%%}%s" % lq(d['cover']))
    sd.append("{%%- when 'made' -%%}%s" % lq(d['made']))
    sd.append("{%%- when 'text' -%%}%s" % lq(c.get('text', '')))
    sd.append("{%%- when 'kind' -%%}%s" % CRAFT.get(k, {}).get('kind', ''))
    sd.append("{%%- when 'parts' -%%}%s{%%- when 'opt' -%%}%s" % (CRAFT_PARTS.get(k, ''), CRAFT_OPT.get(k, '')))
    for i in (1, 2, 3):
        sd.append("{%%- when 'p%d' -%%}{%%- case f -%%}{%%- when 'lead' -%%}%s{%%- when 'points' -%%}%s{%%- when 'fibres' -%%}%s{%%- when 'winter' -%%}%s{%%- when 'summer' -%%}%s{%%- endcase -%%}"
                  % (i, lq(c.get('part%d_lead' % i, '')), lq(c.get('part%d_points' % i, '')), lq(c.get('part%d_fibres' % i, '')),
                     lq(c.get('part%d_winter' % i, '')), lq(c.get('part%d_summer' % i, ''))))
    sd.append("{%- endcase -%}")
sd.append("{%- endcase -%}")
open(THEME + '/snippets/ms-sys-data.liquid', 'w').write('\n'.join(sd) + '\n')
print('system data:', len(SYS_DATA), 'systems')
# the default product template: fibres and layers are filled per product, so both start empty (hidden)
gen = []
for t in product_types:
    if t == 'ms-product-related':
        gen.append(product_qa([]))
    gen.append(('ms-craft' if t == 'ms-product-build' else t, {}, None))
write('product', 'the product page.', gen)
print('products without layers:', sorted(set(made) - set(LAYERS) - {'perfumes'}))

# the booking product keeps Atelier's own product page, with its booking and cart
shutil.copy(SP + '/base/templates/product.json', THEME + '/templates/product.appointment.json')
print('product templates:', len(made), made)

# ── The enquiry page: the store's Contact page, as the full-page enquiry ──────────
write('page.contact', 'the enquiry page. Every enquiry in the menus leads here; ?enquiry=appointment, proposal, brochure, callback, message, trade or partner opens that form.', [
    ('ms-enquire', {}, None),
])

# sections no template uses any more
used = set()
for t in glob.glob(THEME + '/templates/*.json'):
    used |= set(re.findall(r'"type":\s*"(ms-[a-z0-9-]+)"', open(t).read()))
for g in glob.glob(THEME + '/sections/*-group.json'):
    used |= set(re.findall(r'"type":\s*"(ms-[a-z0-9-]+)"', open(g).read()))
for name in ('ms-contact-01', 'ms-contact-02'):
    if name not in used and os.path.exists(THEME + '/sections/%s.liquid' % name):
        os.remove(THEME + '/sections/%s.liquid' % name)
        print('removed unused', name)

# ── Agents & resellers: every place the live store locator shows ─────────────────
# The old section showed 13 built-in places (English list) plus the editor's blocks,
# merged where they are the same business (same email, website or name); the block wins.
src = open(SP + '/old/sections/store-locator-map.liquid').read()
blobs = re.findall(r'<script type="application/json" id="msm-builtin-\{\{ sid \}\}">(\[.*?\])</script>', src, re.S)
builtins = json.loads(blobs[2])          # the third list is the English one (it, ru, then the default)
assert builtins[8]['title'] == 'WWTS London', builtins[8]['title']
old_tpl = json.loads(open(SP + '/old/templates/page.agents-resellers.json').read())
loc = old_tpl['sections']['store_locator_map_87qx4Q']
blocks = [loc['blocks'][b]['settings'] for b in loc['block_order']]


def host(u):
    return re.sub(r'^(https?://)?(www\.)?', '', (u or '').lower()).strip('/').split('/')[0]


places = [dict(b) for b in builtins]
for b in blocks:
    hit = None
    for p in places:
        if (b.get('email') and b['email'].lower() == (p.get('email') or '').lower()) or \
           (b.get('website') and host(b['website']) == host(p.get('website'))) or \
           (b['title'].lower().startswith(p['title'].lower()) or p['title'].lower().startswith(b['title'].lower())):
            hit = p
            break
    rec = {'title': b['title'], 'contact': b.get('contact', ''), 'country': b['country'], 'city': b['city'],
           'address': b.get('address', ''), 'phone': b.get('phone', ''), 'email': b.get('email', ''),
           'website': b.get('website', ''), 'lat': b['lat'], 'lng': b['lng'], 'category': b['category']}
    if hit:
        for k, v in rec.items():
            if v not in ('', None):
                hit[k] = v
    else:
        places.append(rec)

REGION = {'Italy': 'Europe', 'San Marino': 'Europe', 'United Kingdom': 'Europe', 'Poland': 'Europe', 'Russia': 'Europe',
          'Canada': 'Americas', 'United States': 'Americas', 'Hong Kong': 'Asia Pacific'}
# small corrections, so each place is drawn where it is
FIX = {
    'Villa Arredamenti Interior Solutions': {'city': 'Colnago, Monza and Brianza', 'address': 'Via Manzoni, 47\n20872 Colnago (MB)'},
    'Maison Territo': {'city': 'Montreal (Mont-Royal)'},
    'In Made Ltd, a Desidery Company': {'city': 'Central, Hong Kong'},
    'Berenice — Cannigione': {'lat': 41.1066, 'lng': 9.4392, 'city': 'Cannigione, Sardinia', 'address': 'Via Lungomare A. Doria, snc\n07021 Cannigione (SS)'},
    'Berenice — Porto Cervo': {'city': 'Porto Cervo, Sardinia', 'address': 'Castel Cervo, Liscia di Vacca\n07021 Porto Cervo (SS)'},
    'Passerini Design — Boutique': {'address': '117 N County Rd\nPalm Beach, FL 33480', 'contact': ''},
    'Passerini Design — Showroom': {'address': '820 W Indiantown Rd, Suite 101–102\nJupiter, FL 33458', 'contact': ''},
    'Bergomi Milano': {'address': 'Via Palestro, 6\n20121 Milano (MI)'},
    'Bergomi Monza': {'address': 'Via Zucchi, 46\n20900 Monza (MB)'},
    'Vago Arredamenti': {'city': 'Barlassina, Monza and Brianza', 'address': 'Corso Guglielmo Marconi, 52\n20825 Barlassina (MB)'},
    'bredaquaranta': {'address': 'Via Fatebenefratelli, 10\n20121 Milano (MI)'},
    'COSE & COSE': {'address': 'Via Oreste Brizi, 8\n47891 Dogana'},
    'WWTS London': {'address': '60 Fulham Road\nLondon SW3 6HH'},
    'WWTS Moscow': {'address': "1-y Magistral'nyy Tupik, 11/9\n123290 Moscow"},
    'HH Solutions': {'city': 'Warsaw', 'address': 'ul. Duchnicka 3\n01-796 Warszawa'},
}
NOTE = {'Passerini Design — Showroom': 'Showroom and headquarters, with an interior designer on hand.',
        'Passerini Design — Boutique': 'Palm Beach boutique, with an interior designer on hand.'}
out = [{'name': 'Midsummer Milano — the atelier', 'kind': 'atelier', 'city': 'Milan', 'country': 'Italy', 'region': 'Europe',
        'address': 'Via Andegari, 4\n20121 Milano (MI)', 'email': 'info@midsummer-milano.com', 'lat': '45.468492', 'lon': '9.189679',
        'note': 'Where every system is made, and can be lain on. By appointment, Monday to Friday.'}]
for p in places:
    p.update(FIX.get(p['title'], {}))
    rec = {'name': p['title'], 'kind': p['category'], 'city': p['city'], 'country': p['country'],
           'region': REGION.get(p['country'], 'Europe'), 'contact': p.get('contact', ''), 'address': p.get('address', ''),
           'phone': p.get('phone', ''), 'email': p.get('email', ''), 'website': p.get('website', ''),
           'lat': str(p['lat']), 'lon': str(p['lng']), 'note': NOTE.get(p['title'], '')}
    out.append({k: v for k, v in rec.items() if v not in ('', None)})
RORD = ['Europe', 'Middle East', 'Americas', 'Asia Pacific']
COUNTRY_ORD = ['Italy', 'San Marino']
out.sort(key=lambda r: (RORD.index(r['region']), (COUNTRY_ORD + [r['country']]).index(r['country']) if r['country'] in COUNTRY_ORD else 9, r['country'], r['kind'] != 'atelier', r['city'].lower(), r['name'].lower()))
write('page.agents-resellers', 'Agents & resellers: every showroom, boutique and agent, each a block of the section.', [
    ('ms-stockists', {}, [('place', r) for r in out]),
])
shutil.copy(THEME + '/templates/page.agents-resellers.json', THEME + '/templates/page.agents-and-resellers.json')
print('places:', len(out), [r['name'] for r in out])

# ── Press: each publication is a blog (press-elle-decor …) on the template blog.press ──
press = json.load(open(SP + '/pv3/press.json'))
write('blog.press', 'a publication that wrote about Midsummer Milano: its mark, its pieces, and every other publication.', [
    ('ms-press-blog', {}, [('publication', {'name': n, 'link': href, 'logo_file': fn}) for (row, n, href, fn) in press]),
])

# ── Handmade in Italy and Sleep Culture: designed pages, assigned by bin/../scripts/create-pages.sh ──
HANDS = 'Untitled_Project_5_b49a7740-07fa-45f1-8b4f-464d951b0772.jpg'
write('page.handmade-in-italy', 'Handmade in Italy: how a Midsummer bed is made, by two artisans, start to finish.', [
    ('ms-banner', {'image': 'shopify://shop_images/' + HANDS, 'image_fallback': CDN + HANDS + '?width=2400', 'eyebrow': 'Heritage & craft',
                   'use_page_title': False, 'heading': 'Handmade in Italy', 'height': 'tall', 'focus': 'center',
                   'text': 'Two Italian artisans. Two or three full days. One bed.'}, None),
    ('ms-statement', {'eyebrow': 'The method', 'use_content': False,
                      'heading': 'A Midsummer bed is not assembled. It is made, by the same two pairs of hands, from the first spring to the last stitch.',
                      'text': '<p>Every piece is built by hand, from start to finish, by the same two Italian artisans: two or three full days of work for each mattress. It is not a marketing promise; it is a method.</p><p>Because one pair of hands follows the bed through every stage, nothing goes inside it that its makers did not choose and place themselves. And because they know it from the inside, the bed can come back to them at fifteen years to be opened, renewed and made ready for fifteen more.</p>'}, None),
    ('ms-process', {'eyebrow': 'The making', 'heading': 'Five stages, every one by hand.',
                    'text': '<p>The order in which a Midsummer bed comes together, from the springs up. Nothing is glued; everything can be reached again.</p>', 'ground': '#FBF9F5'}, [
        ('step', {'image_fallback': 'ms-graded-ochre-room.jpg', 'title': 'The springs', 'text': '<p>The core is built by hand, so that the bed answers to the body that lies on it, at every point and in every position.</p>'}),
        ('step', {'image': 'shopify://shop_images/Paisleydettaglio.jpg', 'image_fallback': CDN + 'Paisleydettaglio.jpg?width=1400', 'title': 'The natural fibres', 'text': '<p>Wool, silk, cashmere, horsehair, linen and Ingeo, chosen because they perform better, age better and breathe better, are opened and laid by hand, each where it does its work.</p>'}),
        ('step', {'image_fallback': 'ms-photo-mattress-detail.jpg', 'title': 'The tufting', 'text': '<p>The mattress is tufted by hand. The dimples you see are what keep every fibre in its place, year after year.</p>'}),
        ('step', {'image_fallback': 'ms-photo-silk-detail.jpg', 'title': 'The border', 'text': '<p>The sides are stitched by hand, row by row. It gives the edge its line, and the strength to hold you right to the border of the bed.</p>'}),
        ('step', {'image_fallback': 'ms-graded-bougainvillea.jpg', 'title': 'The cloth', 'text': '<p>Last, the upholstery: Loro Piana Interiors fabrics, chosen for your room. Two or three days after it was begun, the bed is finished by the same two people who started it.</p>'}),
    ]),
    ('ms-image-pair', {'eyebrow': 'In the atelier', 'heading': 'Slow, by method.',
                       'fallback_1': 'ms-photo-seamstress.jpg', 'caption_1': 'The cloth, cut by hand at the atelier.',
                       'fallback_2': 'ms-photo-tufting.jpg', 'caption_2': 'Tufted by hand through the whole depth, so every fibre stays where it was laid.'}, None),
    ('ms-cta-band', {'tone': 'ink', 'eyebrow': 'Via Andegari 4, Milano', 'heading': 'Come and see the hands at work.',
                     'text': '<p>The atelier receives by appointment, Monday to Friday. Lie on the systems, and see the fibres before they are laid.</p>',
                     'button': 'Book a private appointment', 'button_enquire': True, 'link_label': 'Natural materials', 'link_place': 'materials'}, None),
])
write('page.sleep-culture', 'Sleep Culture: rest, designed with the same rigour as the room around it.', [
    ('ms-banner', {'image_fallback': 'ms-graded-horse.jpg', 'eyebrow': 'Heritage & craft', 'use_page_title': False, 'heading': 'Sleep Culture',
                   'height': 'tall', 'text': 'Rest, designed with the same rigour as the room around it.'}, None),
    ('ms-statement', {'eyebrow': 'An architect\'s question', 'use_content': False,
                      'heading': 'A sofa gets specified. A kitchen gets designed. The bed, where we spend a third of our lives, deserves the same care.',
                      'text': '<p>Midsummer Milano began with a question its founder, an architect, kept asking: why is the bed treated as a technical product from a catalogue, when every other piece of a room is chosen with care?</p><p>Sleep Culture is where we follow that question: how material, temperature, proportion and ritual shape the night, and what making beds by hand, and listening to the people who sleep in them, has taught us.</p>'}, None),
    ('ms-process', {'eyebrow': 'What a good night is made of', 'heading': 'Three things we design for.', 'ground': '#F4EFE5'}, [
        ('step', {'image_fallback': 'ms-photo-linen-sheets.jpg', 'title': 'Temperature', 'text': '<p>Natural fibres breathe. Wool and horsehair carry warmth and moisture away from the body, so the bed stays even through the night, in August as in January.</p>'}),
        ('step', {'image_fallback': 'ms-photo-my-dream-sleep.jpg', 'title': 'Support', 'text': '<p>Springs that work one by one follow the body instead of pushing back against it, at every point and in every position you sleep in.</p>'}),
        ('step', {'image_fallback': 'ms-photo-cream-blanket.jpg', 'title': 'The seasons', 'text': '<p>Rest has a rhythm. Our toppers turn with the year: linen and silk to face the summer, wool and cashmere for the winter, in the same bed.</p>'}),
    ]),
    ('ms-article-rail', {'tag': 'sleep', 'eyebrow': 'From the Journal', 'heading': 'Notes on sleep.', 'link_label': 'All notes'}, None),
    ('ms-cta-band', {'tone': 'ink', 'eyebrow': 'Five questions', 'heading': 'Find the bed that suits the way you sleep.',
                     'button': 'Find your Midsummer', 'button_enquire': False, 'button_place': 'quiz', 'link_label': 'Book a private appointment', 'link_enquire': True}, None),
])
# ── the home page's figures count up as they come into view (assets/ms-site.js) ──
p = THEME + '/sections/ms-home-06.liquid'
s = open(p).read()
FIG = '<div style="display: flex; align-items: baseline; gap: 4px; font-family: Newsreader'
if 'data-ms-count' not in s:
    s = s.replace(FIG, '<div data-ms-count style="display: flex; align-items: baseline; gap: 4px; font-family: Newsreader')
    open(p, 'w').write(s)
print('figures that count:', s.count('data-ms-count'))

# ── the default page template also carries the locator and the enquiry page, each shown only
#    on its own page, so they appear whichever template those pages were given ──
def gate(liquid, key):
    checks = ''.join("    capture ms_here\n      render 'ms-link', to: '%s'\n    endcapture\n    if ms_here == page.url\n      assign ms_show = true\n    endif\n" % k for k in key.split(','))
    head = ("{%%- liquid\n  assign ms_show = true\n  if template.suffix == blank and page\n    assign ms_show = false\n%s"
            "  endif\n-%%}\n{%%- if ms_show -%%}\n") % checks
    i = liquid.index('{% schema %}')
    return head + liquid[:i].rstrip() + '\n{%- endif -%}\n' + liquid[i:]


for name, key in (('ms-stockists', 'agents'), ('ms-enquire', 'enquire')):
    p = THEME + '/sections/%s.liquid' % name
    s = open(p).read()
    if 'assign ms_show' not in s:
        open(p, 'w').write(gate(s, key))

def load(name):
    return json.loads(re.sub(r'^\s*/\*.*?\*/', '', open('%s/templates/%s.json' % (THEME, name)).read(), flags=re.S))

pj = load('page')
agents = load('page.agents-resellers')['sections']['s01']
pj['sections']['agents'] = agents
pj['sections']['enquire'] = {'type': 'ms-enquire', 'settings': {}}
pj['order'] = [k for k in pj['order'] if k not in ('agents', 'enquire')] + ['agents', 'enquire']
assert len(pj['order']) <= 25, len(pj['order'])
open(THEME + '/templates/page.json', 'w').write(HEAD % 'every page. Pages with a design of their own (Questions, Professionals, Hospitality, Natural Materials, Made to last, Find your Midsummer, Agents & resellers, the enquiry page) show it here too, each only on its own page.' + json.dumps(pj, indent=2, ensure_ascii=False) + '\n')
print('page.json sections:', len(pj['order']))

# ── the home page, in chapters: the film; one sentence; the three collections; then four
#    chapters (made by hand, what is inside, what it is made of and dressed in, made to last)
#    with the comparison between them; the proof; the journal; the accounts; the invitation.
#    One idea per screen, the same space around each.
CDN_ = 'https://midsummer-milano.com/cdn/shop/files/'
WHY = [('Who makes it', 'Two artisans, start to finish, in our Milan atelier.', 'A production line, with many hands and no one answerable for the whole.'),
       ('What is inside', 'Only natural fibres: wool, horsehair, silk, cashmere and linen, laid by hand over pocket springs.', 'Foams, latex and synthetic fillings, glued in layers.'),
       ('Through the year', 'A winter side and a summer side, turned with the season.', 'One side, all year.'),
       ('Size and shape', 'Any size, round included, with no tooling charge.', 'A catalogue of standard sizes.'),
       ('What it is dressed in', 'Natural linen and cotton, or Loro Piana Interiors, chosen for the room.', 'The house ticking.'),
       ('After fifteen years', 'Opened, cleaned and rebuilt by the artisans who made it, for fifteen more.', 'Replaced, and sent to landfill.')]
home = load('index')
by_type = {v['type']: k for k, v in home['sections'].items()}
S = home['sections']
S['words'] = {'type': 'ms-hp-statement', 'settings': {}}
S['ch1'] = {'type': 'ms-hp-chapter', 'settings': {
    'layout': 'split', 'side': 'left', 'tone': 'light', 'image_fallback': 'ms-photo-seamstress-portrait.jpg',
    'numeral': '01', 'eyebrow': 'Handmade in Milan', 'heading': 'Two artisans. One bed.',
    'text': 'No production line. The same two hands open the spring core and sew the final seam, in our atelier on Via Andegari. That is why a change of size, height or fabric is a decision, never an exception.',
    'stat1_value': '2', 'stat1_label': 'Artisans build each system, start to finish',
    'stat2_value': '24', 'stat2_label': 'Systems across three collections',
    'stat3_value': '100%', 'stat3_label': 'Natural fibres, nothing synthetic',
    'link_label': 'Handmade in Italy', 'link_place': 'handmade'}}
S['build'] = {'type': 'ms-craft', 'settings': {'eyebrow': '02 · Inside a Midsummer bed'}}
S['ch3'] = {'type': 'ms-hp-chapter', 'settings': {
    'layout': 'split', 'side': 'right', 'tone': 'sand', 'image_fallback': 'ms-photo-teal-throw.jpg',
    'numeral': '03', 'eyebrow': 'Natural fibres · Loro Piana Interiors', 'heading': 'Only what nature makes. Dressed in Loro Piana Interiors.',
    'text': 'Wool, cashmere, silk, horsehair, linen and Ingeo, chosen because they breathe, last and age well, are laid by hand where each does its work. Many systems are then made in Loro Piana Interiors cloths, chosen for the room; the others in natural linen and cotton.',
    'link_label': 'Natural materials', 'link_place': 'materials'}}
S['why'] = {'type': 'ms-why', 'settings': {'eyebrow': '04 · Why Midsummer'}, 'blocks': {}, 'block_order': []}
for i, (l, o, t) in enumerate(WHY):
    bid = 'row_%02d' % (i + 1)
    S['why']['blocks'][bid] = {'type': 'row', 'settings': {'label': l, 'ours': o, 'theirs': t}}
    S['why']['block_order'].append(bid)
S['ch5'] = {'type': 'ms-hp-chapter', 'settings': {
    'layout': 'full', 'tone': 'dark', 'image_fallback': 'ms-photo-drapes-fireplace.jpg',
    'numeral': '05', 'eyebrow': 'Made to last · 15 + 15', 'heading': 'Fifteen years. Then fifteen more.',
    'text': 'At fifteen years your mattress comes back to the artisans who made it. They open it, wash and re-card the fibres, check every spring and close it again, for fifteen more.',
    'link_label': 'The 15 + 15 service', 'link_place': 'regen'}}
press = home['sections'][by_type['ms-home-15']]
LINES = {'Il Sole 24 Ore': ('Arredo Design 24 on the elegance of good sleep, with Midsummer Milano.', '2025'),
         'Kommersant': ('Midsummer Milano in Style Interiors, the Russian design magazine.', ''),
         'Salone del Mobile': ('Salone del Mobile 2026: the atelier on Via Andegari opens its doors.', '2026')}
pblocks = json.loads(json.dumps(press.get('blocks', {})))
for b in pblocks.values():
    l = LINES.get(b['settings'].get('name'))
    if l:
        b['settings']['line'], b['settings']['when'] = l
S['proof'] = {'type': 'ms-hp-proof', 'settings': {'award_logo': 'ms-press-green-product-award.svg'}, 'blocks': pblocks, 'block_order': press.get('block_order', [])}
S['follow'] = {'type': 'ms-follow', 'settings': {}}
S['visit'] = {'type': 'ms-hp-chapter', 'settings': {
    'layout': 'split', 'side': 'left', 'tone': 'dark', 'image_fallback': 'ms-photo-atelier-blue-gold.jpg',
    'numeral': '', 'eyebrow': 'The atelier · Via Andegari 4, Milano', 'heading': 'Come and lie down.',
    'text': 'Lie on the systems, touch the fibres and the cloths, and leave with a proposal drawn for your room. By appointment, Monday to Friday, 09:00–12:00 and 13:00–18:00, or by video call wherever you are.',
    'link_label': 'Book a private appointment', 'link_place': 'enquire', 'link_query': 'enquiry=appointment'}}
S['voices'] = {'type': 'ms-voices', 'settings': {}}
S['letters'] = {'type': 'ms-letters', 'settings': {}}
HOME_FLOW = [by_type['ms-home-01'], 'words', by_type['ms-home-03'], 'ch1', 'build', 'ch3', 'why', 'ch5', 'proof', 'voices',
             by_type['ms-home-14'], 'follow', 'letters', 'visit']
home['order'] = HOME_FLOW
for k in list(S):
    if k not in home['order']:
        del S[k]
open(THEME + '/templates/index.json', 'w').write(HEAD % 'the home page, in chapters: the film, one sentence, the collections; made by hand, what is inside, what it is made of, why it is different, made to last; the proof; the journal; the invitation.' + json.dumps(home, indent=2, ensure_ascii=False) + '\n')
print('home bands:', len(home['order']))

# ── every designed place, always reachable: /collections/all?view=ms-<place> renders
#    templates/collection.ms-<place>.json, so a menu entry never leads nowhere even before
#    its page is created in admin (snippets/ms-link.liquid falls back to it).
VIEWS = {'handmade': 'page.handmade-in-italy', 'sleep-culture': 'page.sleep-culture', 'materials': 'page.natural-materials',
         'regen': 'page.regeneration', 'quiz': 'page.find-your-midsummer', 'professionals': 'page.professionals',
         'hospitality': 'page.hospitality', 'agents': 'page.agents-resellers', 'faq': 'page.faq', 'contact': 'page.contact',
         'loro': 'page.loro-piana-interiors', 'dream': 'page.download-the-dream'}
for v, src in VIEWS.items():
    d = load(src)
    d['layout'] = 'ms'
    open('%s/templates/collection.ms-%s.json' % (THEME, v), 'w').write(HEAD % ('the %s page, reachable before its page exists in admin (?view=ms-%s).' % (v, v)) + json.dumps(d, indent=2, ensure_ascii=False) + '\n')
# Our story has no page design of its own: it is told with the home page's house, craft and service bands
write('collection.ms-story', 'Our story, reachable before the About page exists in admin (?view=ms-story).', [
    ('ms-banner', {'image_fallback': 'ms-photo-loft.jpg', 'eyebrow': 'Midsummer Milano', 'heading': 'Our story', 'height': 'tall',
                   'text': 'A house of beds, made by hand in Milan.'}, None),
    ('ms-home-02', {}, None), ('ms-home-05', {}, None), ('ms-home-06', {}, None), ('ms-home-09', {}, None),
    ('ms-home-08', {}, None), ('ms-home-17', {}, None)])
# the collections, compared: the page every "Compare" and "Our beds" link opens
CMP_ROWS = [
    ('For', 'Natural fibres and honest construction, done properly.', 'Fabric chosen for the room, comfort chosen for you.', 'Without limit. No detail overlooked.', False),
    ('Fibres', 'Natural fibres throughout', 'Precious blends: yak, camel hair, silk, cashmere', 'The rarest, vicuña and cashmere among them', False),
    ('Cloth', 'Cotton, or linen and cotton; Capri in Loro Piana Interiors Mystic River', 'Raw linen and cotton; Dreamy and Brera in Loro Piana Interiors', 'Loro Piana Interiors on most systems', False),
    ('Made to measure', 'Made to your size', 'Your size and your cloth', 'Everything, to your drawing, round beds included', False),
    ('Systems', 'Five', 'Seven', 'Twelve', False),
    ('Handmade in Italy, by two artisans', 'yes', 'yes', 'yes', True),
    ('Only natural fibres', 'yes', 'yes', 'yes', True),
    # Round 21: support in place of the regeneration (which every page about 15 + 15 already tells): the
    # firmness is set with each sleeper, in every collection
    ('Support, set to how you sleep', 'yes', 'yes', 'yes', True),
    ('Price', 'On request', 'On request', 'On request', True)]
CMP_QA = [
    ('Which collection is right for me?', '<p>It depends on how you sleep and how far you want the bespoke to go. Essentials is natural comfort, done properly; Signature adds precious fibres, and Loro Piana Interiors on Dreamy and Brera; Icons is the house without limits. The five questions of Find your Midsummer suggest a system, and at the atelier in Milan you can lie on all three.</p>'),
    ('Are Essentials made differently from Icons?', '<p>No. Every system, in every collection, is made by hand in Italy by the same two artisans, from natural fibres only. The collections differ in the cloth, the rarity of the fibres and how far each system is made to measure.</p>'),
    ('Can I have a size that is not listed?', '<p>Yes. Every system is made to order: dimensions and heights are worked to your drawing, round beds included, without tooling charges.</p>'),
    ('Why are prices on request?', '<p>Because nothing is made before it is specified. Size, firmness, fibres and cloth are chosen with you, at the atelier or by video, and the system is quoted from that specification.</p>'),
    ('How long does a Midsummer bed last?', '<p>It is made to last and to be renewed: at fifteen years the atelier opens, cleans and rebuilds the mattress, by hand, for fifteen more.</p>')]
CMP = [
    ('ms-compare', {}, [('row', {'label': l, 'v1': a, 'v2': b, 'v3': c, 'shared': sh}) for (l, a, b, c, sh) in CMP_ROWS]),
    ('ms-qa', {'tone': 'sand', 'eyebrow': 'Choosing', 'heading': 'Questions before choosing.', 'link_label': 'Ask the atelier', 'link_place': 'enquire'},
     [('qa', {'q': q, 'a': a}) for (q, a) in CMP_QA])]
write('page.compare', 'the three collections compared (the store page sleep-collections opens in it with ?view=compare).', CMP)
write('collection.ms-compare', 'the three collections compared, reachable before its page exists (?view=ms-compare).', CMP)
# the three collections, always reachable: the store's collection, or the systems the house lists under it
TIERS = {'essentials': ('Collection I', 'Essentials', 'The entry into the Midsummer world: natural fibres, the same hand-built construction, clean lines.', 'ms-graded-bougainvillea.jpg'),
         'signature': ('Collection II', 'Signature', 'Exclusive blends of precious natural fibres, designed for the highest comfort, in natural linen or Loro Piana Interiors.', 'ms-graded-ochre-room.jpg'),
         'icons': ('Collection III', 'Icons', 'The most important pieces we make: completely bespoke, most of them made in Loro Piana Interiors, with no detail overlooked.', 'ms-graded-arches.jpg')}
for key, (eyebrow, title, text, img) in TIERS.items():
    write('collection.ms-' + key, 'the %s collection, reachable whatever the store calls it (?view=ms-%s).' % (title, key), [
        ('ms-banner', {'image_fallback': img, 'eyebrow': eyebrow, 'use_page_title': False, 'heading': title, 'height': 'tall', 'text': text}, None),
        ('ms-curated', {'tier': key, 'eyebrow': 'The systems', 'heading': 'Every one made to order.',
                        'text': 'Each system is specified with you, at the atelier or by video: dimensions, firmness, fibres and cloth. Prices on request.'}, None)])
# the same story as a page template, so the store's About page opens in it (?view=story)
STORY = load('collection.ms-story')
open('%s/templates/page.story.json' % THEME, 'w').write(HEAD % 'Our story: the About page (about-midsummer-milano), in the house\'s own design.' + json.dumps(STORY, indent=2, ensure_ascii=False) + '\n')
print('views:', len(VIEWS) + 1)

# ── designed sections on the default page template: shown on their own page, decided by the
#    page's handle (snippets/ms-page-key.liquid), and always inside the theme's own designed
#    templates (reached as ?view=<template> or assigned in admin) ──
OURS = sorted(os.path.basename(f)[5:-5] for f in glob.glob(THEME + '/templates/page.*.json'))
GATE_HEAD = re.compile(r"\A(\{%- comment -%\}.*?\{%- endcomment -%\}\n)?\{%- liquid\n  assign ms_show = true\n.*?-%\}\n", re.S)
regated = 0
for f in glob.glob(THEME + '/sections/ms-*.liquid'):
    s = open(f).read()
    m = GATE_HEAD.match(s)
    if not m:
        continue
    name = os.path.basename(f)[:-7]
    if name == 'ms-page':
        head = ("{%- liquid\n  assign ms_show = true\n  if template.name == 'page'\n    capture ms_key\n      render 'ms-page-key'\n    endcapture\n"
                "    if ms_key != blank\n      assign ms_show = false\n    endif\n  endif\n-%}\n")
    else:
        keys = sorted({{'sustain': 'regen', 'enquire': 'contact'}.get(k, k) for k in re.findall(r"to: '([a-z-]+)'", m.group(0))})
        head = ("{%%- liquid\n  assign ms_show = true\n  if template.name == 'page'\n    assign ms_show = false\n"
                "    assign ms_ours = '%s' | split: ','\n    if ms_ours contains template.suffix\n      assign ms_show = true\n    else\n"
                "      capture ms_key\n        render 'ms-page-key'\n      endcapture\n      assign ms_want = '%s' | split: ','\n"
                "      if ms_want contains ms_key\n        assign ms_show = true\n      endif\n    endif\n  endif\n-%%}\n") % (','.join(OURS), ','.join(keys))
    open(f, 'w').write((m.group(1) or '') + head + s[m.end():])
    regated += 1
print('gated sections:', regated)

# ── photographs from the house's own library (Drive): the professional and hotel pages open on them
for name, old_new, alt in (('ms-hosp-01', 'ms-photo-glass-house.jpg', 'A Midsummer bed in a glass house among the trees'),
                           ('ms-pro-01', 'ms-photo-fresco-bed.jpg', 'A Midsummer bed against a frescoed wall, with a paisley throw')):
    p = THEME + '/sections/%s.liquid' % name
    t = open(p).read()
    t = re.sub(r"\{\{ 'ms-graded-[a-z-]+\.jpg' \| asset_url \}\}", "{{ '%s' | asset_url }}" % old_new, t, count=1)
    t = re.sub(r'<img alt="[^"]*" src="(\{% if section\.settings\.img1)', '<img alt="%s" width="1122" height="1402" src="\\1' % alt, t, count=1)
    t = t.replace('aspect-ratio: 1122 / 1402; object-fit: contain;', 'aspect-ratio: 1122 / 1402; object-fit: cover;', 1)
    open(p, 'w').write(t)

# ── every picture states its size, so the page does not shift while it loads (CLS)
IMG = re.compile(r'<img\b(?:[^>"]|"[^"]*")*>')
def sized(m):
    tag = m.group(0)
    if re.search(r'\swidth=', tag):
        return tag
    if 'midsummer-logotype' in tag or 'alt="Midsummer Milano"' in tag:
        return tag.replace('<img ', '<img width="577" height="136" ', 1)
    w = re.search(r'width:\s*(\d+)px;\s*aspect-ratio:\s*(\d+)\s*/\s*(\d+)', tag)
    if w:
        W = int(w.group(1)); H = round(W * int(w.group(3)) / int(w.group(2)))
        return tag.replace('<img ', '<img width="%d" height="%d" ' % (W, H), 1)
    a = re.search(r'aspect-ratio:\s*(\d+)\s*/\s*(\d+)', tag)
    if a:
        return tag.replace('<img ', '<img width="1200" height="%d" ' % round(1200 * int(a.group(2)) / int(a.group(1))), 1)
    if 'object-fit' in tag:
        return tag.replace('<img ', '<img width="1600" height="1000" ', 1)
    return tag
unsized = 0
for f in glob.glob(THEME + '/sections/*.liquid') + glob.glob(THEME + '/snippets/ms-*.liquid'):
    s = open(f).read()
    t = IMG.sub(sized, s)
    if t != s:
        open(f, 'w').write(t)
print('pictures sized')

# ── "Heritage & craft" on the story leads to how a bed is made, not to regeneration
p = THEME + '/sections/ms-home-05.liquid'
t = open(p).read().replace("data-ms=\"cta\" href=\"{% render 'ms-link', to: 'regen' %}\"", "data-ms=\"cta\" href=\"{% render 'ms-link', to: 'handmade' %}\"")
open(p, 'w').write(t)

# ── Natural materials opens like the other story pages: a photograph and its name, then the words
for tpl in ('page.natural-materials', 'collection.ms-materials'):
    p = THEME + '/templates/%s.json' % tpl
    raw = open(p).read()
    m = re.match(r'\A(\s*/\*.*?\*/\s*)?', raw, re.S)
    head, body = m.group(1) or '', raw[m.end():]
    data = json.loads(body)
    if 'opening' not in data['sections']:
        data['sections'] = dict([('opening', {'type': 'ms-banner', 'settings': {
            'image_fallback': 'ms-photo-cashmere-throw.jpg', 'eyebrow': 'Heritage & craft', 'use_page_title': False,
            'heading': 'Natural materials', 'height': 'tall',
            'text': 'Vicuña, cashmere, alpaca, horsehair and wool, each laid by hand where it does its work.'}})] + list(data['sections'].items()))
        data['order'].insert(0, 'opening')
    open(p, 'w').write(head + json.dumps(data, indent=2, ensure_ascii=False) + '\n')
p = THEME + '/sections/ms-materials-01.liquid'
t = open(p).read()
t = re.sub(r'<h1 (style="font-family: Newsreader[^"]*">\{\{ section\.settings\.t2 \}\})</h1>', r'<h2 \1</h2>', t)
open(p, 'w').write(t)

# ── the trade and hotel pages open with a line and the two things a professional comes to do
LEADS = {'ms-pro-01': ('Specification support, the full Loro Piana Interiors palette and systems made to your drawing, with one person at the atelier from the first sketch to delivery.', 'Open a project file'),
         'ms-hosp-01': ('Handmade beds for hotels, residences and yachts: specified to the room, delivered in phases, with regeneration written into the contract.', 'Start a hotel project')}
for name, (lead, cta) in LEADS.items():
    p = THEME + '/sections/%s.liquid' % name
    t = open(p).read()
    if 'ms-hero-lead' not in t:
        t = re.sub(r'(<h1 [^>]*>\{\{ section\.settings\.t\d \}\}</h1>)',
                   lambda m: m.group(1) + '\n{%- if section.settings.lead != blank -%}<p class="ms-hero-lead">{{ section.settings.lead }}</p>{%- endif -%}'
                   '<div class="ms-hero-ctas"><a class="ms-hero-cta" href="{% render \'ms-link\', to: \'enquire\', q: \'enquiry=trade\' %}#enquire" data-ms-landing>{{ section.settings.cta }}</a>'
                   '<a class="ms-hero-link" href="{% render \'ms-link\', to: \'agents\' %}">{{ section.settings.cta2 }}</a></div>', t, count=1)
        t = t.replace('"settings": [\n', '"settings": [\n    { "type": "textarea", "id": "lead", "label": "Opening line", "default": %s },\n    { "type": "text", "id": "cta", "label": "Button", "default": %s },\n    { "type": "text", "id": "cta2", "label": "Second link", "default": "Agents & Resellers" },\n' % (json.dumps(lead), json.dumps(cta)), 1)
        assert 'ms-hero-lead' in t, name
        open(p, 'w').write(t)

# ── every journal note ends with more notes from the same journal
for f in glob.glob(THEME + '/templates/article*.json'):
    raw = open(f).read()
    m = re.match(r'\A(\s*/\*.*?\*/\s*)?', raw, re.S)
    data = json.loads(raw[m.end():])
    if 'more' not in data['sections']:
        data['sections']['more'] = {'type': 'ms-article-rail', 'settings': {'eyebrow': 'From the Journal', 'heading': 'More notes.', 'link_label': 'All notes'}}
        data['order'].append('more')
    open(f, 'w').write((m.group(1) or '') + json.dumps(data, indent=2, ensure_ascii=False) + '\n')

# ── the gold of the small labels, deep enough to read on every light ground (WCAG AA, ≥ 4.5:1)
for f in glob.glob(THEME + '/sections/*.liquid') + glob.glob(THEME + '/snippets/ms-*.liquid') + [THEME + '/assets/ms-site.css', THEME + '/assets/ms-site.js', THEME + '/layout/ms.liquid']:
    t = open(f).read()
    u = re.sub(r'#8C8579', '#6E675C', re.sub(r'#9A7B4F', '#7E623B', t, flags=re.I), flags=re.I).replace('rgb(154, 123, 79)', 'rgb(126, 98, 59)')
    if u != t:
        open(f, 'w').write(u)

# ── on a phone, the rest of the collection is a row to swipe, not four full-height pictures
p = THEME + '/sections/ms-product-related.liquid'
t = open(p).read()
if 'ms-rel' not in t:
    t = t.replace('<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: clamp(16px, 2.4vw, 36px);">',
                  '<div class="ms-rel" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: clamp(16px, 2.4vw, 36px);">', 1)
    t = t.replace('{%- endif -%}\n{% schema %}', '{%- endif -%}\n<style>@media (max-width: 700px) { .ms-site .ms-rel { display: flex !important; overflow-x: auto; scroll-snap-type: x mandatory; scrollbar-width: none; margin-right: calc(-1 * clamp(18px, 5vw, 80px)); padding-right: clamp(18px, 5vw, 80px); } .ms-rel::-webkit-scrollbar { display: none; } .ms-rel > a { flex: 0 0 72%; scroll-snap-align: start; } }</style>\n{% schema %}', 1)
    assert 'ms-rel' in t and 'scroll-snap' in t
    open(p, 'w').write(t)

# ── no picture below the house's standard: the store's low-resolution files are replaced by the library's
LOWRES = {'Top_deserto_mobile5.jpg': 'ms-photo-atelier-pure.jpg', 'Paisley_IMG_5161_low.jpg': 'ms-photo-atelier-pure.jpg',
          'Paisley_IMG_4918_low_70960abc-6877-49b2-abc8-0bd379994114.jpg': 'ms-photo-fabric-weave.jpg'}
for f in glob.glob(THEME + '/sections/*.liquid'):
    t = open(f).read(); u = t
    for low, good in LOWRES.items():
        u = re.sub(r"assign (\w+) = 'https://midsummer-milano\.com/cdn/shop/files/" + re.escape(low) + r"[^']*'", lambda m: "assign %s = '%s' | asset_url" % (m.group(1), good), u)
        u = re.sub(r"https://midsummer-milano\.com/cdn/shop/files/" + re.escape(low) + r"[^\"'{ ]*", "{{ '%s' | asset_url }}" % good, u)
    if u != t:
        open(f, 'w').write(u)

# ── discretion: the site shows how beautifully the beds are made, never how they are built
if not any('"ms-product-build"' in open(f).read() for f in glob.glob(THEME + '/templates/*.json')):
    if os.path.exists(THEME + '/sections/ms-product-build.liquid'):
        os.remove(THEME + '/sections/ms-product-build.liquid')
QUIET = [
    (r',\s*six layers of springs,', ','),
    (r'Six layers of springs, vicu(ñ|n)a', r'Vicu\1a'),
    (r'over six layers of springs\. The fabric leads; the springwork does the rest\.', 'over a core built by hand. The fabric leads; the craft does the rest.'),
    (r'over six layers of springs', 'over a core built by hand'),
    (r'(Five|Six|Four|Three|Two) layers of (micro |pocket |cover )?springs[^."<]*\.?', 'Built by hand, inside and out.'),
    (r'with cover springs (above and below|at the faces)', 'built by hand'),
    (r'\bcover springs\b', 'springs'),
    (r'\bmicro springs\b', 'springs'),
    (r'Layers of springs in an Icons syst(em|…)', 'Natural fibres, nothing synthetic'),
    (r'Micro springs', 'Springs'),
    (r'over a micro spring layer of ', 'over '),
    (r', laid by hand over pocket springs', ', laid by hand'),
    (r'with pocket springs, wool', 'with wool'),
    (r'Pocket springs, hand-sewn natural fibres', 'Hand-built, natural fibres only'),
    (r'Pocket springs, hand-sewn natural …', 'Hand-built, natural fibres only'),
    (r'Six spring layers over the Vivaldi core\.', 'The Vivaldi, taken further.'),
    # nothing that tells how the core is built, or in what order a bed is put together
    (r'Pocket by pocket\. The integrity of the spring core, the resilience of each individual coil and the condition of the wool felt that protects them\.',
     'Piece by piece. The integrity of the core, its resilience, and the condition of every natural fibre.'),
    (r'Pocket by pocket\. The integrity of…', 'Piece by piece. The integrity of…'),
    (r'Check the springs\.', 'Inspect the core.'),
    (r'Springs checked, wool recarded, plate replaced only if spoiled\.', 'The core inspected, the wool re-carded, a part renewed only where it needs it.'),
    (r'check every spring and close it again', 'renew what the years have worn and close it again'),
    (r'Springs that work one by one follow the body', 'A core built by hand follows the body'),
    (r'The order in which a Midsummer bed comes together, from the springs up\.', 'How a Midsummer bed comes together, stage by stage.'),
    (r'from the first spring to the last stitch', 'from the core to the last stitch'),
    (r'"title": "The springs"', '"title": "The core"'),
    # audit: no springs or layers in the words, and Signature is not all Loro Piana (bin/lp_data.py)
    (r'the same two hands that open the spring core sew the final seam', 'the same two hands that begin the bed sew its final seam'),
    (r'The same two hands that open the spring core sew the final seam', 'The same two hands that begin the bed sew its final seam'),
    (r'The same two hands open the spring core and sew the final seam', 'The same two hands begin the bed and sew its final seam'),
    (r'seven systems in Loro Piana Interiors fabrics over spring architectures built for the highest comfort',
     'seven systems in precious natural fibres, in natural linen or Loro Piana Interiors, built for the highest comfort'),
    (r'Loro Piana Interiors fabrics over spring architectures (designed|built) for the highest comfort',
     r'Precious natural fibres, in natural linen or Loro Piana Interiors, \1 for the highest comfort'),
    (r'The heart of the collection\. Loro …', 'The heart of the collection. Precious…'),
    (r'the fabric, the depth of the spring architecture and how far the bespoke goes', 'the cloth, the fibres and how far the bespoke goes'),
    (r'Spring architectures for the highe…', 'Precious fibres for the highest c…'),
    (r'Spring architectures for the highest comfort', 'Precious fibres for the highest comfort'),
    (r'A spring core built by hand\.', 'Built by hand, inside and out.'),
    (r'Every layer is reachable\.', 'Every part can be reached.'),
    (r'Baby alpaca over a hand-sewn spring core\.', 'Baby alpaca, sewn by hand.'),
]
for f in glob.glob(THEME + '/sections/*.liquid') + glob.glob(THEME + '/templates/*.json') + glob.glob(THEME + '/snippets/ms-*.liquid'):
    t = open(f).read(); u = t
    for a, b in QUIET:
        u = re.sub(a, b, u)
    if f.endswith('ms-home-06.liquid'):
        u = u.replace('"label": "6",\n      "default": "6"', '"label": "Figure 3",\n      "default": "100%"')
    if u != t:
        open(f, 'w').write(u)

# ── the natural materials page carries the same fibre marks as the product pages
p = THEME + '/sections/ms-materials-02.liquid'
t = open(p).read()
t2 = re.sub(r'<svg aria-hidden="true" height="22"[^>]*>.*?</svg>(\s*<(h2|h3|div|span)[^>]*>)\{\{ section\.settings\.(t\d+) \}\}',
            lambda m: '<span style="color: #7E623B; display: block; flex: 0 0 auto;">{%% render \'ms-fibre-mark\', name: section.settings.%s, size: 46 %%}</span>%s{{ section.settings.%s }}' % (m.group(3), m.group(1), m.group(3)), t, flags=re.S)
print('materials marks:', len(re.findall('ms-fibre-mark', t2)))
open(p, 'w').write(t2)

# ── Journal: one list of subjects everywhere; the heading keeps only its words
p = THEME + '/sections/ms-journal-head.liquid'
t = open(p).read()
t = re.sub(r'\n<div style="[^"]*">\n<a href="\{\{ blog\.url \}\}".*?\{%- endfor -%\}\n</div>', '', t, flags=re.S)
open(p, 'w').write(t)

# ── a note reads like a page of a book: back to the Journal, its subject, a calm measure, sharing
p = THEME + '/sections/ms-article.liquid'
t = open(p).read()
if 'ms-art-back' not in t:
    t = t.replace("{%- assign kicker = article.tags | first | default: blog.title -%}",
                  "{%- capture cat -%}{% render 'ms-note-cat', a: article %}{%- endcapture -%}{%- capture kicker -%}{% render 'ms-note-cat', label: cat %}{%- endcapture -%}{%- if kicker == blank -%}{%- assign kicker = blog.title -%}{%- endif -%}", 1)
    t = t.replace('<span>{{ kicker }}</span></div>', '<span>{% if cat != blank %}<a href="{{ blog.url }}?view={{ cat }}" style="color: inherit;">{{ kicker }}</a>{% else %}{{ kicker }}{% endif %}</span></div>', 1)
    t = re.sub(r'(<section style="padding: clamp\(60px, 9vw, 140px\) clamp\(18px, 5vw, 80px\) 0px; max-width: 820px; margin: 0px auto;">\n)',
               r'\1<a class="ms-art-back" href="{{ blog.url }}"><span aria-hidden="true">←</span> {{ section.settings.all }}</a>\n', t, count=1)
    share = """<div class="ms-art-share" aria-label="Share">
<span>{{ section.settings.share | default: 'Share' }}</span>
<a href="https://wa.me/?text={{ article.title | url_encode }}%20{{ shop.url | append: article.url | url_encode }}" target="_blank" rel="noopener">WhatsApp</a>
<a href="https://www.linkedin.com/sharing/share-offsite/?url={{ shop.url | append: article.url | url_encode }}" target="_blank" rel="noopener">LinkedIn</a>
<a href="https://pinterest.com/pin/create/button/?url={{ shop.url | append: article.url | url_encode }}{% if article.image %}&media={{ article.image | image_url: width: 1600 | prepend: 'https:' | url_encode }}{% endif %}&description={{ article.title | url_encode }}" target="_blank" rel="noopener">Pinterest</a>
<a href="mailto:?subject={{ article.title | url_encode }}&body={{ shop.url | append: article.url | url_encode }}">Email</a>
<button type="button" data-ms-copy="{{ shop.url | append: article.url }}">{{ section.settings.copy | default: 'Copy link' }}</button>
</div>
"""
    t = t.replace('{{ article.content }}\n', '{{ article.content }}\n' + share, 1)
    css = """
  /* reading: a book's measure, a lede, quiet headings, pictures to the edge of the text */
  .ms-site a.ms-art-back { display: inline-flex; gap: 10px; align-items: center; font-size: 10.5px; letter-spacing: .24em; text-transform: uppercase; color: #6E675C; margin-bottom: clamp(26px, 3vw, 40px); }
  .ms-site a.ms-art-back:hover { color: #17140F; }
  .ms-site .ms-article-body { font-size: 17px !important; line-height: 1.9 !important; color: #2F2B25 !important; max-width: 760px !important; }
  .ms-site .ms-article-body > p:first-of-type { font-family: Newsreader, Georgia, serif; font-weight: 300; font-size: clamp(21px, 2vw, 25px); line-height: 1.55; color: #17140F; }
  .ms-site .ms-article-body h2, .ms-site .ms-article-body h3 { font-family: Newsreader, Georgia, serif; font-weight: 300; letter-spacing: -0.015em; color: #17140F; margin-top: 18px; }
  .ms-site .ms-article-body h2 { font-size: clamp(26px, 2.6vw, 34px); line-height: 1.2; }
  .ms-site .ms-article-body h3 { font-size: clamp(21px, 2vw, 25px); line-height: 1.3; }
  .ms-site .ms-article-body a { color: #17140F; text-decoration: underline; text-decoration-thickness: 1px; text-underline-offset: 4px; }
  .ms-site .ms-article-body blockquote { margin: 12px 0; padding: 4px 0 4px 26px; border-left: 1px solid #7E623B; font-family: Newsreader, Georgia, serif; font-style: italic; font-size: clamp(21px, 2vw, 26px); line-height: 1.5; color: #17140F; }
  .ms-site .ms-article-body img { width: 100%; height: auto; margin: 10px 0; }
  .ms-site .ms-article-body ul, .ms-site .ms-article-body ol { padding-left: 1.2em; display: grid; gap: 8px; }
  .ms-art-share { display: flex; flex-wrap: wrap; align-items: center; gap: 12px 22px; margin-top: 18px; padding-top: 22px; border-top: 1px solid #DDD6C9; font-size: 10.5px; letter-spacing: .22em; text-transform: uppercase; }
  .ms-art-share span { color: #7E623B; }
  .ms-site .ms-art-share a, .ms-site .ms-art-share button { color: #4A443B; background: none; border: 0; padding: 6px 0; font: inherit; letter-spacing: inherit; text-transform: inherit; cursor: pointer; text-decoration: none !important; }
  .ms-site .ms-art-share a:hover, .ms-site .ms-art-share button:hover { color: #17140F; }
"""
    t = t.replace('<style>\n', '<style>\n' + css, 1)
    t = t.replace("    update();\n  })();", "    update();\n    document.querySelectorAll('[data-ms-copy]').forEach(function (b) { b.addEventListener('click', function () { var t = b.textContent; (navigator.clipboard ? navigator.clipboard.writeText(b.getAttribute('data-ms-copy')) : Promise.reject()).then(function () { b.textContent = '✓'; setTimeout(function () { b.textContent = t; }, 1600); }, function () {}); }); });\n  })();", 1)
    t = t.replace('"settings": [\n', '"settings": [\n    { "type": "text", "id": "share", "label": "Share label", "default": "Share" },\n    { "type": "text", "id": "copy", "label": "Copy link label", "default": "Copy link" },\n', 1)
    assert 'ms-art-back' in t and 'ms-art-share' in t
    open(p, 'w').write(t)

# ── the end of a note: the share line, a sign-off from the atelier, and the notes either side, with their pictures
p = THEME + '/sections/ms-article.liquid'
t = open(p).read()
if 'ms-art-end' not in t:
    old_end = re.search(r'<div style="border-top: 1px solid rgb\(221, 214, 201\); padding-top: 24px; margin-top: 12px;[^\n]*\n<a data-ms="cta" href="\{\{ blog.url \}\}"[^\n]*\n<a data-ms="cta" data-ms-enquire[^\n]*\n</div>\n', t)
    assert old_end, 'article end not found'
    t = t[:old_end.start()] + t[old_end.end():]
    old_nav = re.search(r'\{%- assign older = blog.next_article -%\}.*?</nav>\n\{%- endif -%\}\n', t, re.S)
    assert old_nav, 'article nav not found'
    END = """<aside class="ms-art-end" aria-label="{{ section.settings.end_label | escape }}">
  <div class="ms-art-end__in">
    <svg aria-hidden="true" width="28" height="28" viewBox="0 0 24 24" class="ms-art-end__leaf"><path d="M4 20 C4 11 11 4 20 4 C20 13 13 20 4 20 Z" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.1"/><path d="M4 20 L16 8" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.1"/></svg>
    <div class="ms-art-end__eyebrow">{{ section.settings.end_label }}</div>
    <p class="ms-art-end__h">{{ section.settings.end_heading }}</p>
    {%- if section.settings.end_text != blank -%}<p class="ms-art-end__t">{{ section.settings.end_text }}</p>{%- endif -%}
    <div class="ms-art-end__links">
      <a class="ms-art-end__btn" data-ms-enquire data-ms-cta="article-end" href="{% render 'ms-link', to: 'enquire' %}">{{ section.settings.cta }}</a>
      <a class="ms-art-end__all" href="{{ blog.url }}"><span aria-hidden="true">←</span> {{ section.settings.all }}</a>
      {%- if cat != blank -%}<a class="ms-art-end__all" href="{{ blog.url }}?view={{ cat }}">{{ section.settings.same }} {{ kicker }}</a>{%- endif -%}
    </div>
  </div>
</aside>
{%- liquid
  assign newer = nil
  assign older = nil
  assign found = false
  assign last = nil
  for a in blog.articles limit: 50
    if found
      assign older = a
      break
    endif
    if a.url == article.url
      assign found = true
      assign newer = last
    endif
    assign last = a
  endfor
-%}
{%- if older or newer -%}
<nav class="ms-art-nav{% unless older and newer %} is-solo{% endunless %}" aria-label="{{ section.settings.more | escape }}">
  {%- for side in (1..2) -%}
    {%- if side == 1 -%}{%- assign n = older -%}{%- assign lab = section.settings.older -%}{%- else -%}{%- assign n = newer -%}{%- assign lab = section.settings.newer -%}{%- endif -%}
    {%- if n -%}
      {%- capture ncat -%}{% render 'ms-note-cat', a: n %}{%- endcapture -%}{%- capture nkick -%}{% render 'ms-note-cat', label: ncat %}{%- endcapture -%}
      <a class="ms-art-nav__a{% if side == 2 %} is-next{% endif %}" href="{{ n.url }}">
        <span class="ms-art-nav__img">{%- if n.image -%}<img src="{{ n.image | image_url: width: 640 }}" alt="" width="640" height="480" loading="lazy">{%- else -%}<svg aria-hidden="true" width="34" height="34" viewBox="0 0 24 24"><path d="M4 20 C4 11 11 4 20 4 C20 13 13 20 4 20 Z" fill="none" stroke="#7E623B" stroke-width="1"/><path d="M4 20 L16 8" fill="none" stroke="#7E623B" stroke-width="1"/></svg>{%- endif -%}</span>
        <span class="ms-art-nav__txt">
          <span class="ms-art-nav__lab">{{ lab }}</span>
          <em>{{ n.title }}</em>
          <span class="ms-art-nav__meta">{% if nkick != blank %}{{ nkick }} · {% endif %}{{ n.published_at | date: '%-d %B %Y' }}</span>
        </span>
      </a>
    {%- endif -%}
  {%- endfor -%}
</nav>
{%- endif -%}
"""
    t = t[:old_nav.start()] + END + t[old_nav.end():]
    # the old nav styles give way to the new ending
    t = re.sub(r"  \.ms-art-nav \{.*?\n  @media \(max-width: 600px\) \{ \.ms-art-nav[^\n]*\n", "", t, flags=re.S)
    CSS = """
  .ms-site .ms-art-share a, .ms-site .ms-art-share button { border-bottom: 0 !important; }
  .ms-art-end { background: #F4EFE5; padding: clamp(64px, 8vw, 120px) clamp(16px, 5vw, 80px); }
  .ms-art-end__in { max-width: 760px; margin: 0 auto; text-align: center; display: flex; flex-direction: column; align-items: center; }
  .ms-art-end__leaf { color: #7E623B; }
  .ms-art-end__eyebrow { font-size: 11px; letter-spacing: .28em; text-transform: uppercase; color: #6E675C; margin-top: 18px; }
  .ms-site .ms-art-end__h { font-family: Newsreader, Georgia, serif; font-weight: 200; font-size: clamp(28px, 3.4vw, 46px); line-height: 1.1; letter-spacing: -0.025em; color: #17140F; margin-top: 16px; max-width: 22ch; }
  .ms-site .ms-art-end__t { font-size: 15px; line-height: 1.9; color: #4A443B; margin-top: 18px; max-width: 54ch; }
  .ms-art-end__links { display: flex; flex-wrap: wrap; justify-content: center; align-items: center; gap: 16px 30px; margin-top: clamp(26px, 3vw, 36px); }
  .ms-site a.ms-art-end__btn { display: inline-flex; align-items: center; min-height: 52px; padding: 0 28px; background: #17140F; color: #FBF9F5; font-size: 10.5px; letter-spacing: .22em; text-transform: uppercase; text-decoration: none; }
  .ms-site a.ms-art-end__btn:hover { background: #2F2A22; }
  .ms-site a.ms-art-end__all { display: inline-flex; gap: 10px; font-size: 10.5px; letter-spacing: .22em; text-transform: uppercase; color: #4A443B; text-decoration: none; border-bottom: 1px solid rgba(23, 20, 15, .3); padding-bottom: 5px; }
  .ms-site a.ms-art-end__all:hover { color: #17140F; border-color: #17140F; }
  .ms-art-nav { max-width: 1120px; margin: 0 auto; padding: clamp(48px, 6vw, 88px) clamp(16px, 5vw, 80px) 0; display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: clamp(16px, 2vw, 28px); }
  .ms-art-nav.is-solo { grid-template-columns: minmax(0, 1fr); max-width: 760px; }
  .ms-site a.ms-art-nav__a { display: grid; grid-template-columns: 38% 1fr; align-items: stretch; border: 1px solid #DDD6C9; color: #17140F; text-decoration: none; transition: border-color .3s ease, background .3s ease; overflow: hidden; }
  .ms-site a.ms-art-nav__a:hover { border-color: #17140F; background: #F4EFE5; }
  .ms-site a.ms-art-nav__a.is-next { grid-template-columns: 1fr 38%; text-align: right; }
  .ms-art-nav__a.is-next .ms-art-nav__img { order: 2; }
  .ms-art-nav__img { display: flex; align-items: center; justify-content: center; background: #EDE6D9; min-height: 150px; overflow: hidden; }
  .ms-art-nav__img img { width: 100%; height: 100%; object-fit: cover; display: block; transition: transform 1s cubic-bezier(.2, .7, .2, 1); }
  .ms-art-nav__a:hover .ms-art-nav__img img { transform: scale(1.04); }
  .ms-art-nav__txt { display: flex; flex-direction: column; justify-content: center; gap: 10px; padding: clamp(18px, 2.4vw, 30px); }
  .ms-art-nav__lab { font-size: 10.5px; letter-spacing: .26em; text-transform: uppercase; color: #7E623B; }
  .ms-art-nav__a em { font-family: Newsreader, Georgia, serif; font-style: normal; font-size: clamp(19px, 1.8vw, 24px); line-height: 1.3; }
  .ms-art-nav__meta { font-size: 12px; letter-spacing: .06em; color: #6E675C; }
  @media (max-width: 700px) {
    .ms-art-nav { grid-template-columns: minmax(0, 1fr); }
    .ms-site a.ms-art-nav__a, .ms-site a.ms-art-nav__a.is-next { grid-template-columns: 34% 1fr; text-align: left; }
    .ms-art-nav__a.is-next .ms-art-nav__img { order: 0; }
    .ms-art-nav__img { min-height: 120px; }
  }
"""
    t = t.replace('  .ms-read { position: fixed;', CSS + '  .ms-read { position: fixed;', 1)
    t = t.replace('padding: clamp(40px, 6vw, 72px) clamp(18px, 5vw, 80px) clamp(60px, 9vw, 140px); max-width: 820px;', 'padding: clamp(40px, 6vw, 72px) clamp(18px, 5vw, 80px) clamp(48px, 6vw, 88px); max-width: 820px;', 1)
    t = t.replace('    { "type": "text", "id": "more", "label": "More notes label", "default": "More notes" },',
                  '    { "type": "text", "id": "more", "label": "More notes label", "default": "More notes" },\n'
                  '    { "type": "text", "id": "same", "label": "More on the subject", "default": "More on" },\n'
                  '    { "type": "text", "id": "end_label", "label": "Sign-off label", "default": "From the atelier" },\n'
                  '    { "type": "text", "id": "end_heading", "label": "Sign-off heading", "default": "Continue the conversation in Milano." },\n'
                  '    { "type": "textarea", "id": "end_text", "label": "Sign-off text", "default": "Every note is written at the atelier on Via Andegari, where the beds can be lain on and the fibres held. Visit by appointment, or meet us by video." },', 1)
    assert 'ms-art-end' in t and 'blog.next_article' not in t
    open(p, 'w').write(t)

# ── The Milano atelier: its own page, the place every "visit" leads
ATELIER = [
    # (Round 29) the house's own rooms, never the blue-and-gold one: scripts/atelier_photos_r29.py
    ('ms-banner', {'image_fallback': 'ms-photo-atelier-parrot-front.jpg', 'focus': 'bottom', 'eyebrow': 'Via Andegari 4, Milano', 'use_page_title': False,
                   'heading': 'The Milano atelier', 'height': 'tall',
                   'text': 'Where the beds can be lain on. By appointment, Monday to Friday.'}, None),
    ('ms-statement', {'eyebrow': 'Visiting', 'use_content': False,
                      'heading': 'Lie on the systems, touch the fibres, and leave with a proposal drawn for your room.',
                      'text': '<p>The atelier is at Via Andegari 4, 20121 Milano, a few steps from La Scala. It opens by appointment, Monday to Friday, 09:00–12:00 and 13:00–18:00, and every appointment is confirmed by email within one working day.</p><p>Wherever you are, the same conversation can happen by video: we send the fibres and the cloths ahead, and specify the system with you on screen.</p>'}, None),
    ('ms-process', {'eyebrow': 'Your visit', 'heading': 'Four steps, at your pace.', 'ground': '#F4EFE5'}, [
        ('step', {'image_fallback': 'ms-photo-atelier-screen.jpg', 'title': 'Book', 'text': '<p>Choose a morning or an afternoon, at the atelier or by video. A person replies within one working day.</p>'}),
        ('step', {'image_fallback': 'ms-photo-atelier-leopard-side.jpg', 'title': 'Lie down', 'text': '<p>Essentials, Signature and Icons, made up as they would be at home. Take your time on each.</p>'}),
        ('step', {'image_fallback': 'ms-photo-fabric-weave.jpg', 'title': 'Touch', 'text': '<p>The natural fibres before they are laid, and the Loro Piana Interiors cloths against the bed.</p>'}),
        ('step', {'image_fallback': 'ms-photo-atelier-wool-edge.jpg', 'title': 'Specify', 'text': '<p>Size, firmness, fibres and cloth, written down with you. The proposal follows, drawn for your room.</p>'})]),
    ('ms-image-pair', {'eyebrow': 'In the rooms', 'heading': 'Every bed made up, as it would be at home.',
                       'fallback_1': 'ms-photo-atelier-parrots.jpg', 'caption_1': 'The parrot room, with a Signature system.',
                       'fallback_2': 'ms-photo-atelier-leopard-above.jpg', 'caption_2': 'The leopard room, Via Andegari.'}, None),
    ('ms-qa', {'eyebrow': 'Before you come', 'heading': 'Visiting the atelier.', 'link_label': 'Book a private appointment', 'link_place': 'enquire'}, [
        ('qa', {'q': 'Do I need an appointment?', 'a': '<p>Yes. The atelier receives by appointment, Monday to Friday, 09:00–12:00 and 13:00–18:00, so that each visit has the rooms, and our attention, to itself.</p>'}),
        ('qa', {'q': 'Can we meet by video instead?', 'a': '<p>Yes. We send the fibres and cloth samples ahead and specify the system with you on screen, wherever you are.</p>'}),
        ('qa', {'q': 'What should I bring?', 'a': '<p>The measurements of the room and of the bed you have in mind, a few photographs, and any fabric or colour references. Architects are welcome to bring drawings.</p>'}),
        ('qa', {'q': 'Can I see the Loro Piana Interiors fabrics?', 'a': '<p>Yes. The range is at the atelier, to be chosen against the bed itself.</p>'}),
        ('qa', {'q': 'Is there somewhere nearer to me?', 'a': '<p>Midsummer beds can also be seen at showrooms, agents and resellers in Europe, the Americas and Asia. See Agents &amp; Resellers for the map.</p>'})]),
    ('ms-cta-band', {'tone': 'ink', 'eyebrow': 'Via Andegari 4, Milano', 'heading': 'Come and lie down.',
                     'text': '<p>Monday to Friday, by appointment. Or by video, wherever you are.</p>',
                     'button': 'Book a private appointment', 'button_enquire': True, 'link_label': 'Agents & Resellers', 'link_place': 'agents'}, None)]
write('page.atelier', 'the Milano atelier (a store page with the handle atelier opens in it, or ?view=atelier).', ATELIER)
write('collection.ms-atelier', 'the Milano atelier, reachable before its page exists (?view=ms-atelier).', ATELIER)

def add_sections(tpl, extra):
    p = THEME + '/templates/%s.json' % tpl
    if not os.path.exists(p):
        return
    raw = open(p).read()
    m = re.match(r'\A(\s*/\*.*?\*/\s*)?', raw, re.S)
    data = json.loads(raw[m.end():])
    for key, typ, settings, blocks in extra:
        if key in data['sections']:
            continue
        sec = {'type': typ, 'settings': settings}
        if blocks:
            sec['blocks'] = {}
            sec['block_order'] = []
            for j, (bt, bs) in enumerate(blocks):
                bid = '%s_%02d' % (bt, j + 1)
                sec['blocks'][bid] = {'type': bt, 'settings': bs}
                sec['block_order'].append(bid)
        data['sections'][key] = sec
        data['order'].append(key)
    open(p, 'w').write((m.group(1) or '') + json.dumps(data, indent=2, ensure_ascii=False) + '\n')

# ── Heritage & Craft read as one book: every chapter ends with the next one
for cur, tpls in (('story', ['page.story', 'collection.ms-story']), ('handmade', ['page.handmade-in-italy', 'collection.ms-handmade']),
                  ('sleep-culture', ['page.sleep-culture', 'collection.ms-sleep-culture']), ('materials', ['page.natural-materials', 'collection.ms-materials']),
                  ('loro', ['page.loro-piana-interiors', 'collection.ms-loro']), ('regen', ['page.regeneration', 'collection.ms-regen', 'page.sustainability'])):
    for t in tpls:
        add_sections(t, [('next', 'ms-next-read', {'current': cur}, None)])

# ── the trade and hotel pages: what they need next, recent projects, and their questions
PRO_CARDS = [('card', {'place': 'collections', 'title': 'The three collections', 'text': 'Essentials, Signature and Icons side by side, to specify from.', 'image_fallback': 'ms-graded-ochre-room.jpg'}),
             ('card', {'place': 'loro', 'title': 'Loro Piana Interiors', 'text': 'The full palette, and your own cloth on request.', 'image_fallback': 'ms-photo-teal-throw.jpg'}),
             ('card', {'place': 'materials', 'title': 'Natural materials', 'text': 'What each fibre does, for your specification notes.', 'image_fallback': 'ms-photo-cashmere-throw.jpg'}),
             ('card', {'place': 'regen', 'title': 'Made to last · 15 + 15', 'text': 'Regeneration at fifteen years, for the life of the project.', 'image_fallback': 'ms-photo-drapes-fireplace.jpg'})]
PRO_QA = [('qa', {'q': 'Do you work from our drawings?', 'a': '<p>Yes. Dimensions, heights and radii, round beds included, are worked to your drawing, with no tooling charge.</p>'}),
          ('qa', {'q': 'Can we specify our own fabric?', 'a': '<p>Yes. The full Loro Piana Interiors palette is available, and your own cloth (COM) on request.</p>'}),
          ('qa', {'q': 'What do you send for a specification?', 'a': '<p>Drawings, sections and material schedules for your set, fabric references from Loro Piana Interiors and samples of the natural fibres.</p>'}),
          ('qa', {'q': 'Who follows the project?', 'a': '<p>One person at the atelier, from the first specification to delivery and installation.</p>'}),
          ('qa', {'q': 'Where can our clients see the beds?', 'a': '<p>At the atelier in Milan, by appointment, or at our agents and resellers in Europe, the Americas and Asia.</p>'})]
HOSP_CARDS = [('card', {'place': 'regen', 'title': 'Regeneration in contract', 'text': 'Fifteen years, then fifteen more, written into the agreement.', 'image_fallback': 'ms-photo-drapes-fireplace.jpg'}),
              ('card', {'place': 'collections', 'title': 'The three collections', 'text': 'One build for every room, from Essentials to Icons.', 'image_fallback': 'ms-graded-arches.jpg'}),
              ('card', {'place': 'handmade', 'title': 'Handmade in Italy', 'text': 'The same two artisans for every bed in the programme.', 'image_fallback': 'ms-photo-seamstress-portrait.jpg'}),
              ('card', {'place': 'agents', 'title': 'Agents & Resellers', 'text': 'Our partners near your project, wherever it is.', 'image_fallback': 'ms-photo-atelier-pure.jpg'})]
HOSP_QA = [('qa', {'q': 'Can you make beds for a whole hotel?', 'a': '<p>Yes. We make volume programmes to the room, by hand in Italy, with phased production aligned to your floor handovers and the same fibres across every key.</p>'}),
           ('qa', {'q': 'Are the beds suitable for contract use?', 'a': '<p>Fire-retardancy and contract certification are prepared for each market and documented for your file.</p>'}),
           ('qa', {'q': 'How are the beds maintained?', 'a': '<p>Each system comes with its housekeeping protocol, and we offer on-site rotation and care training for your team.</p>'}),
           ('qa', {'q': 'What happens at fifteen years?', 'a': '<p>The 15 + 15 service can be written into the agreement: the beds return to the atelier to be opened, cleaned and rebuilt, rather than replaced.</p>'})]
for t in ('page.professionals', 'collection.ms-professionals'):
    add_sections(t, [('places', 'ms-link-cards', {'eyebrow': 'For your specification', 'heading': 'Everything you will need, in one house.', 'text': 'The pages architects and interior designers use most when they specify a Midsummer system.'}, PRO_CARDS),
                     ('projects', 'ms-article-rail', {'blog_handle': 'projects', 'eyebrow': 'Projects', 'heading': 'Where our beds went.', 'link_label': 'All projects', 'limit': 4}, None),
                     ('qa', 'ms-qa', {'tone': 'sand', 'eyebrow': 'Trade questions', 'heading': 'Before you specify.', 'link_label': 'Open a project file', 'link_place': 'enquire'}, PRO_QA)])
for t in ('page.hospitality', 'collection.ms-hospitality'):
    add_sections(t, [('places', 'ms-link-cards', {'eyebrow': 'For your programme', 'heading': 'A bed your guests remember, for thirty years.', 'text': 'What a hotel or residence project draws on.'}, HOSP_CARDS),
                     ('projects', 'ms-article-rail', {'blog_handle': 'projects', 'eyebrow': 'Projects', 'heading': 'Hotels and residences.', 'link_label': 'All projects', 'limit': 4}, None),
                     ('qa', 'ms-qa', {'tone': 'sand', 'eyebrow': 'Contract questions', 'heading': 'Before you open.', 'link_label': 'Start a hotel project', 'link_place': 'enquire'}, HOSP_QA)])

# ── Questions & customer care: topics, a menu of them, more answers, one FAQPage
p = THEME + '/sections/ms-faq-02.liquid'
t = open(p).read()
if 'ms-faq-topics' not in t:
    t = t.replace("""<div>
{%- for block in section.blocks -%}
<details {{ block.shopify_attributes }}{% if forloop.first %} open{% endif %} style="border-top: 1px solid rgb(221, 214, 201);{% if forloop.last %} border-bottom: 1px solid rgb(221, 214, 201);{% endif %}">""",
"""<div>
{%- assign topics = section.blocks | where: 'type', 'topic' -%}
{%- if topics.size > 1 -%}
<nav class="ms-faq-topics" aria-label="Topics">{%- for tb in topics -%}<a href="#{{ tb.settings.title | handleize }}">{{ tb.settings.title }}</a>{%- endfor -%}</nav>
{%- endif -%}
{%- assign opened = false -%}
{%- for block in section.blocks -%}
{%- if block.type == 'topic' -%}
<h2 class="ms-faq-topic" id="{{ block.settings.title | handleize }}" {{ block.shopify_attributes }}>{{ block.settings.title }}</h2>
{%- continue -%}
{%- endif -%}
<details {{ block.shopify_attributes }}{% unless opened %} open{% endunless %} style="border-top: 1px solid rgb(221, 214, 201);{% if forloop.last %} border-bottom: 1px solid rgb(221, 214, 201);{% endif %}">{%- assign opened = true -%}""", 1)
    t = t.replace("""{%- for block in section.blocks -%}
{"@type": "Question", "name": {{ block.settings.question | json }}, "acceptedAnswer": {"@type": "Answer", "text": {{ block.settings.answer | strip_html | json }}}}{% unless forloop.last %},{% endunless %}
{%- endfor -%}""", """{%- assign qs = section.blocks | where: 'type', 'question' -%}
{%- for block in qs -%}
{"@type": "Question", "name": {{ block.settings.question | json }}, "acceptedAnswer": {"@type": "Answer", "text": {{ block.settings.answer | strip_html | json }}}}{% unless forloop.last %},{% endunless %}
{%- endfor -%}""", 1)
    t = t.replace("""  #shopify-section-{{ section.id }} details > div p { margin: 0; }""", """  #shopify-section-{{ section.id }} details > div p { margin: 0; }
  #shopify-section-{{ section.id }} details > div p + p { margin-top: 12px; }
  #shopify-section-{{ section.id }} details > div a { color: #17140F; text-decoration: underline; text-underline-offset: 3px; }
  .ms-faq-topics { display: flex; flex-wrap: wrap; gap: 8px 22px; padding-bottom: 22px; margin-bottom: 8px; }
  .ms-site .ms-faq-topics a { font-size: 10.5px; letter-spacing: .22em; text-transform: uppercase; color: #6E675C; padding: 8px 0; border-bottom: 1px solid #DDD6C9; }
  .ms-site .ms-faq-topics a:hover { color: #17140F; border-bottom-color: #17140F; }
  .ms-faq-topic { font-family: Newsreader, Georgia, serif; font-weight: 300; font-size: clamp(24px, 2.4vw, 32px); letter-spacing: -0.02em; margin: clamp(36px, 4vw, 56px) 0 14px; scroll-margin-top: 110px; }
  .ms-faq-topic:first-of-type { margin-top: 12px; }""", 1)
    t = t.replace('"max_blocks": 30,', '"max_blocks": 50,')
    t = t.replace('"blocks": [\n', '"blocks": [\n    { "type": "topic", "name": "Topic", "settings": [ { "type": "text", "id": "title", "label": "Topic" } ] },\n', 1)
    assert 'ms-faq-topics' in t and '"type": "topic"' in t
    open(p, 'w').write(t)

def L(place, label):
    return '<a href="{{ %s }}">%s</a>' % (place, label)
FAQ = [
  ('topic', 'The beds'),
  ('Where are Midsummer beds made?', None),
  ('Which natural materials do you use?', None),
  ('How do the three collections differ?', None),
  ('Who founded Midsummer Milano?', '<p>Midsummer Milano was founded in Milan by Chiara Mennini, an architect, around a question she kept asking: why is the bed, where we spend a third of our lives, treated as a technical product from a catalogue, when every other piece of a room is designed with care?</p>'),
  ('Has Midsummer Milano won any awards?', '<p>Yes. The Top System was awarded the Green Product Award 2025 in Berlin, for its plant-based materials and seasonal construction. The house has also been featured by publications including Il Sole 24 Ore and Kommersant, and at the Salone del Mobile in Milan.</p>'),
  ('topic', 'Ordering'),
  ('How do I order a Midsummer bed?', '<p>Book an appointment at the atelier in Milan or by video, or write to us from the enquiry page. The system is specified with you (size, height, firmness, fibres and cloth) and you receive a written proposal. The bed is made to order once the proposal is confirmed.</p>'),
  ('Can a bed be made to my dimensions?', None),
  ('Why are prices not shown?', None),
  ('Can I try a bed before ordering?', None),
  ('Can I see the fibres and fabrics first?', '<p>Yes: at the atelier, where the Loro Piana Interiors range can be chosen against the bed itself, or by post, with fibre and fabric samples sent ahead of a video consultation.</p>'),
  ('How long does delivery take?', None),
  ('Do you deliver outside Italy?', '<p>Yes, worldwide. Where there is no showroom near you, the atelier handles the enquiry directly: specification by video, fabric samples by post, and white-glove delivery by our own team.</p>'),
  ('Where can I see Midsummer beds outside Milan?', '<p>At our showrooms, agents and resellers in Italy, San Marino, the United Kingdom, Poland, Russia, Canada, the United States and Hong Kong. The map on Agents &amp; Resellers shows each of them.</p>'),
  ('topic', 'Sleep & comfort'),
  ('Which firmness is right for me?', '<p>It depends on how you sleep. On your side, hips and shoulders need to sink a little; on your back, the lumbar curve needs support; on your front, a flatter, firmer surface keeps the neck neutral. The five questions of Find your Midsummer suggest a system, and at the atelier you choose by lying down.</p>'),
  ('Will a natural-fibre bed sleep too warm?', '<p>No. Natural fibres breathe: wool and horsehair carry warmth and moisture away from the body, so the bed stays even through the night, in August as in January.</p>'),
  ('Does the bed have a winter and a summer side?', '<p>Yes, where the system is padded for the seasons: wool and cashmere face the winter, linen and silk the summer. Turn it when the season changes.</p>'),
  ('Are the materials suitable for people with allergies?', '<p>Several of the fibres we use are naturally hypoallergenic: alpaca, for example, contains no lanolin. If you have a specific allergy, tell us at the consultation and the specification is adapted.</p>'),
  ('topic', 'Care & regeneration'),
  ('How should I care for the system?', None),
  ('What is the 15 + 15 service?', None),
  ('How do I arrange a regeneration?', '<p>Write to us from the enquiry page with the name of your system and the year it was made. The atelier will tell you how and when the mattress returns to the artisans who made it, and when it comes home.</p>'),
  ('topic', 'For professionals'),
  ('Do you work with architects and interior designers?', None),
  ('Do you supply hotels and contract projects?', None),
]
def faq_blocks(existing):
    blocks, order = {}, []
    for i, item in enumerate(FAQ):
        if item[0] == 'topic':
            bid = 'topic_%02d' % i
            blocks[bid] = {'type': 'topic', 'settings': {'title': item[1]}}
        else:
            q, a = item
            if a is None:
                a = existing[q]
            bid = 'question_%02d' % i
            blocks[bid] = {'type': 'question', 'settings': {'question': q, 'answer': a}}
        order.append(bid)
    return blocks, order
for tpl in ('page.faq', 'collection.ms-faq'):
    p = THEME + '/templates/%s.json' % tpl
    raw = open(p).read()
    m = re.match(r'\A(\s*/\*.*?\*/\s*)?', raw, re.S)
    data = json.loads(raw[m.end():])
    for k, v in data['sections'].items():
        if v['type'] == 'ms-faq-02':
            existing = {b['settings']['question']: b['settings']['answer'] for b in v['blocks'].values() if b['type'] == 'question'}
            v['blocks'], v['block_order'] = faq_blocks(existing)
    open(p, 'w').write((m.group(1) or '') + json.dumps(data, indent=2, ensure_ascii=False) + '\n')
CARE = [('point', {'title': 'Turn it', 'text': 'Head to foot every three months in the first year, then twice a year.'}),
        ('point', {'title': 'With the season', 'text': 'Where the system has a winter and a summer side, turn it when the season changes.'}),
        ('point', {'title': 'Let it breathe', 'text': 'Air the bed whenever you change the linen. Natural fibres give back what they take in.'}),
        ('point', {'title': 'The cloth', 'text': 'Loro Piana Interiors upholstery is dry-cleaned by a specialist only; the atelier can arrange it.'})]
SIZES = [('point', {'title': n, 'w': w, 'l': l}) for (n, w, l) in (('Single', '100', '200'), ('Queen', '153', '203'), ('Small Double', '160', '200'),
                                                                  ('Double', '180', '200'), ('King', '193', '203'), ('Double Extra', '200', '200'))]
FAQ_PLACES = [('card', {'place': 'regen', 'title': 'Made to last · 15 + 15', 'text': 'What happens at fifteen years.', 'image_fallback': 'ms-photo-drapes-fireplace.jpg'}),
              ('card', {'place': 'collections', 'title': 'Compare the collections', 'text': 'Essentials, Signature and Icons side by side.', 'image_fallback': 'ms-graded-ochre-room.jpg'}),
              ('card', {'place': 'atelier', 'title': 'The Milano atelier', 'text': 'Come and lie down, by appointment.', 'image_fallback': 'ms-photo-atelier-sun.jpg'}),
              ('card', {'place': 'agents', 'title': 'Agents & Resellers', 'text': 'Where to see the beds near you.', 'image_fallback': 'ms-photo-atelier-pure.jpg'})]
for t in ('page.faq', 'collection.ms-faq'):
    add_sections(t, [('care', 'ms-guide', {'anchor': 'looking-after', 'tone': 'sand', 'eyebrow': 'Care', 'heading': 'Looking after a natural bed.',
                                           'text': 'A Midsummer system is made to last thirty years. A few habits keep it as it was made.', 'note': 'At fifteen years, the artisans who made it take it back for fifteen more.'}, CARE),
                     ('sizes', 'ms-guide', {'anchor': 'sizes', 'eyebrow': 'Sizes', 'heading': 'Standard sizes, and every other.',
                                            'text': 'The sizes most often specified. Any width, length or shape, round included, is made to order without tooling charges.'}, SIZES),
                     ('places', 'ms-link-cards', {'tone': 'sand', 'eyebrow': 'Read on', 'heading': 'Where to go from here.'}, FAQ_PLACES)])
for f in glob.glob(THEME + '/sections/ms-faq-01.liquid') + [THEME + '/templates/page.faq.json', THEME + '/templates/collection.ms-faq.json']:
    t = open(f).read()
    u = t.replace('Eleven answers on how the beds are made', 'Answers on how the beds are made')
    if u != t:
        open(f, 'w').write(u)
p = THEME + '/sections/ms-faq-02.liquid'
t = open(p).read()
t = t.replace('<div data-dc-tpl="1137" style="max-width: 40ch;">', '<div data-dc-tpl="1137" class="ms-faq-side" style="max-width: 40ch;">', 1)
t = t.replace('<style>', '<style>\n  @media (min-width: 1000px) { .ms-faq-side { position: sticky; top: 120px; } }\n  @media (max-width: 999px) { .ms-faq-wrap { grid-template-columns: minmax(0, 1fr) !important; } .ms-faq-side { max-width: 60ch !important; } }', 1)
t = t.replace('<section style="padding: 0px clamp(18px, 5vw, 80px) clamp(70px, 10vw, 150px); max-width: 1560px; margin: 0px auto; display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));', '<section class="ms-faq-wrap" style="padding: 0px clamp(18px, 5vw, 80px) clamp(70px, 10vw, 150px); max-width: 1560px; margin: 0px auto; display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));', 1)
open(p, 'w').write(t)

add_sections('blog', [('letters', 'ms-letters', {'heading': 'The Journal, by letter.', 'text': 'Our newsletter, sent regularly: new notes, new systems, and the dates the atelier opens.'}, None)])

# the product's cloth: on each system's page, the Loro Piana Interiors cloth it is made in, with that
# cloth's own colours, or the natural cloth it is covered in; nothing about Loro Piana Interiors on a
# system that is not made in it (snippets/ms-product-cloth, generated from bin/lp_data.py)
p = THEME + '/sections/ms-product-reasons.liquid'
t = open(p).read()
m = re.search(r'<h3 style="([^"]*)">\{\{ section\.settings\.t12 \}\}</h3>\n<p style="([^"]*)">\{\{ section\.settings\.t13 \}\}</p>\n<div style="display: flex; flex-wrap: wrap; gap: 9px; margin-top: 24px;">\n(<span style="display: block; width: 26px;[^\n]*\n){7}</div>', t)
assert m, 'reasons: cloth column not found'
H3, P = m.group(1), m.group(2)
t = t[:m.start()] + ('{%- capture ms_cloth -%}{%- if template.name == \'product\' -%}{% render \'ms-product-cloth\', key: template.suffix, handle: product.handle, part: \'reason\' %}{%- endif -%}{%- endcapture -%}\n'
                     '{%- if ms_cloth != blank -%}{{ ms_cloth }}{%- else -%}\n'
                     '<h3 style="' + H3 + '">{{ section.settings.t12 }}</h3>\n<p style="' + P + '">{{ section.settings.t13 }}</p>\n{%- endif -%}') + t[m.end():]
t = t.replace('"label": "Upholstered in Loro Piana Interior…",\n      "default": "Upholstered in Loro Piana Interiors."', '"label": "Cloth heading (systems without their own)",\n      "default": "Dressed for your room."')
t = t.replace('"label": "The palette line",\n      "default": "Thirty-nine cloths in the book, from plain cashmere to textured weaves. Your own cloth, at consultation."', '"label": "Cloth line (systems without their own)",\n      "default": "Natural cloths, chosen with you at the atelier, against the bed."')
assert 'Loro Piana' not in t, 'reasons still names Loro Piana'
open(p, 'w').write(t)

FAB = {f['key']: f for f in FABRICS}
def human(names):
    return names[0] if len(names) == 1 else ', '.join(names[:-1]) + ' and ' + names[-1]
REASON = {  # where the cloth needs more than its own description
    'capri': 'Or two-tone: natural linen and cotton, with Connemara or Mystic River.',
    'dreamy-2': 'Or two-tone: natural linen and cotton, with Connemara or Mystic River.',
    'brera': 'Connemara linen, with the winter side of the mattress edged in Altai wool and cashmere.',
    'top-2': 'Connemara linen on the base and the summer side, Ely’s Harbour linen and cashmere for winter, Bangor linen on the topper.',
    'giotto': 'Connemara linen on the base and the mattress, Bangor linen on the topper.',
    'flora': 'Cardi on the winter face of the topper, Wish bouclé on the base: both wool and cashmere, with linen for summer.',
    'bellini': 'Wish, a bouclé of wool and cashmere, soft and deep, on the whole bed.',
    'paisley': 'Shadan, a paisley linen, on the topper and the border of the mattress; Katai, a pure silk, on the boxspring.',
    'dreamy-springs': 'In natural linen and cotton, or in Mystic River, a linen and cotton in twelve colours.',
    'vicuna': 'In raw linen and cotton, or in a Loro Piana Interiors cloth chosen with you.',
    'topper-high': 'The toppers can be upholstered in Loro Piana Interiors linen and cotton, or in cashmere, in a splendid range of colours.',
}
HEADING = {'topper-high': 'In Loro Piana Interiors linen or cashmere.'}
def chip_html(f):
    out = ''
    for (n, h, small, large) in f['colours']:  # every colour of the cloth (Altai has sixteen)
        out += ('<span style="display: block; width: 30px; height: 30px; border-radius: 50%%; background: %s url({{ \'%s\' | asset_url }}) center / cover; box-shadow: rgba(23, 20, 15, 0.14) 0px 0px 0px 1px inset;" title="%s"></span>\n'
                % (h, small, n.split(' ', 1)[1] if n[0].isdigit() else n))
    return out
LINK = ('<a href="{%% render \'ms-link\', to: \'%s\' %%}%s" style="display: flex; flex-wrap: wrap; align-items: center; gap: 8px; margin-top: 24px; color: inherit; text-decoration: none;">\n'
        '%s<span style="font-size: 11px; letter-spacing: .22em; text-transform: uppercase; margin-left: %s; border-bottom: 1px solid currentColor; padding-bottom: 4px;">%s →</span>\n</a>')
cases = []
for key, c in CLOTH.items():
    lp = [k for k in c['lp'] if k in FAB]
    names = [FAB[k]['name'] for k in lp]
    if c['lp']:
        pal = FAB.get(c.get('palette', ''))
        heading = HEADING.get(key) or ('In Loro Piana Interiors %s.' % human(names) if names else 'In linen and cotton, or Loro Piana Interiors.')
        text = REASON.get(key) or pal['text']
        if pal and pal['colours']:
            link = LINK % ('loro', '#' + ANCHOR[pal['key']], chip_html(pal), '8px', 'The %s colours' % pal['name'])
            # Round 21: every colour of every cloth the system is made in (Capri and Dreamy two-tone
            # with Connemara, Brera edged in Altai), each palette in full, after the main one
            for _k2 in lp:
                if _k2 != pal['key'] and FAB[_k2]['colours']:
                    link += '\n' + LINK % ('loro', '#' + ANCHOR[_k2], chip_html(FAB[_k2]), '8px', 'The %s colours' % FAB[_k2]['name'])
        elif pal:
            link = LINK % ('loro', '#' + ANCHOR[lp[0]], '', '0', 'See %s' % human(names))
        else:
            link = LINK % ('loro', '#fabrics', '', '0', 'The Loro Piana Interiors cloths')
        lp_names = ', '.join(names) or 'Loro Piana Interiors'
        anchor = ANCHOR[pal['key']] if pal else 'fabrics'
    else:
        heading = 'Dressed in natural cloth.'
        text = c['cloth'] + ' Another cloth on request, chosen with you at the atelier.'
        link = LINK % ('materials', '', '', '0', 'The fibres inside')
        lp_names = ''
        anchor = ''
    reason = '<h3 style="%s">%s</h3>\n<p style="%s">%s</p>\n%s' % (H3, heading, P, text, link)
    keys = sorted({key, re.sub(r'-\d+$', '', key)})
    cases.append((keys, lp_names, anchor, reason))
snip = """{%- comment -%}
  What a system is dressed in, for its own page: part 'lp' gives the Loro Piana Interiors cloths it is
  made in (empty when it is made in none), 'anchor' the cloth's place on the Loro Piana Interiors
  page, 'reason' the cloth column of the product page. Found by the product's template, then by its
  handle. Generated from bin/lp_data.py (the house's catalogue and price lists).
{%- endcomment -%}
{%- liquid
  assign k = key | default: handle
  assign keys = '""" + '|'.join(','.join(c[0]) for c in cases) + """' | split: '|'
  assign hit = ''
  for group in keys
    assign ks = group | split: ','
    if ks contains k
      assign hit = ks.first
    endif
  endfor
  if hit == ''
    for group in keys
      assign ks = group | split: ','
      if ks contains handle
        assign hit = ks.first
      endif
    endfor
  endif
-%}
{%- case hit -%}
"""
for keys, lp_names, anchor, reason in cases:
    snip += "{%%- when '%s' -%%}{%%- case part -%%}{%%- when 'lp' -%%}%s{%%- when 'anchor' -%%}%s{%%- when 'reason' -%%}\n%s\n{%%- endcase -%%}\n" % (keys[0], lp_names, anchor, reason)
snip += "{%- endcase -%}\n"
open(THEME + '/snippets/ms-product-cloth.liquid', 'w').write(snip)

# the line under each system's name, from the house's documents
from lp_data import NOTES_I18N
def _note_case(notes):
    return "{%- case title -%}\n" + ''.join("  {%%- when '%s' -%%}%s\n" % (k.replace("'", "\\'"), v) for k, v in notes.items()) + "{%- endcase -%}\n"
note = ("""{%- comment -%} The one-line description of each system, from the house's 2026 catalogue and price lists, in the visitor's language. Used when a product has no custom.subtitle metafield. {%- endcomment -%}
{%- assign nl = request.locale.iso_code | slice: 0, 2 -%}
{%- if nl == 'it' -%}
""" + _note_case(dict(SYSTEM_NOTES, **{k: v for k, v in NOTES_I18N['it'].items() if k in SYSTEM_NOTES}))
        + "{%- elsif nl == 'ru' -%}\n" + _note_case(dict(SYSTEM_NOTES, **{k: v for k, v in NOTES_I18N['ru'].items() if k in SYSTEM_NOTES}))
        + "{%- else -%}\n" + _note_case(SYSTEM_NOTES) + "{%- endif -%}\n")
open(THEME + '/snippets/ms-product-note.liquid', 'w').write(note)
print('product cloth:', len(cases), 'systems,', sum(1 for c in cases if c[1]), 'in Loro Piana Interiors')

# search: two results to a row on a phone
p = THEME + '/sections/ms-search.liquid'
t = open(p).read()
if 'ms-sr-grid' not in t:
    t = t.replace('<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: clamp(24px, 4vw, 48px);">',
                  '<div class="ms-sr-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: clamp(24px, 4vw, 48px);">', 1)
    t = t.replace('{% schema %}', '<style>@media (max-width: 600px) { .ms-sr-grid { grid-template-columns: repeat(2, minmax(0, 1fr)) !important; gap: 24px 14px !important; } }</style>\n{% schema %}', 1)
    assert 'ms-sr-grid' in t
    open(p, 'w').write(t)

# the hero's words keep their contrast over a bright photograph; the WhatsApp button keeps clear of the footer's last row
p = THEME + '/sections/ms-home-01.liquid'
t = open(p).read()
if 'ms-hero-words' not in t:
    t = t.replace('<p style="font-family: Newsreader, Georgia, serif; font-style: italic; font-size: clamp(16px, 1.8vw, 21px); line-height: 1.55; opacity: 0.95;">{{ section.settings.t2 }}</p>',
                  '<p class="ms-hero-words" style="font-family: Newsreader, Georgia, serif; font-style: italic; font-size: clamp(16px, 1.8vw, 21px); line-height: 1.55; opacity: 1; text-shadow: 0 1px 18px rgba(10, 8, 6, .55), 0 0 2px rgba(10, 8, 6, .35);">{{ section.settings.t2 }}</p>', 1)
    t = t.replace('max-width: 15ch;">{{ section.settings.t1 }}</h1>', 'max-width: 15ch; text-shadow: 0 2px 30px rgba(10, 8, 6, .35);">{{ section.settings.t1 }}</h1>', 1)
    assert 'ms-hero-words' in t
    open(p, 'w').write(t)
# the hero speaks the visitor's language: while a line still holds its English default, an
# Italian or Russian page uses the theme's own translation (locales, ms.home)
p = THEME + '/sections/ms-home-01.liquid'
t = open(p).read()
HERO = [('t1', 'Handmade luxury beds and mattresses, built one by one.', 'ms.home.h1'),
        ('t2', 'We design dreams. Every bed is made by two artisans, start to finish.', 'ms.home.lede'),
        ('t3', 'Book a private appointment', 'ms.home.cta'),
        ('t4', 'At our Milan atelier, or by video call', 'ms.home.cta_note')]
for sid, default, key in HERO:
    if '{{ section.settings.%s }}' % sid in t:
        assert t.count('{{ section.settings.%s }}' % sid) == 1, sid
        assert '"default": "%s"' % default in t, sid
        t = t.replace('{{ section.settings.%s }}' % sid, "{%% render 'ms-tr', value: section.settings.%s, default: %s, key: '%s' %%}" % (sid, json.dumps(default).replace('"', "'"), key))
open(p, 'w').write(t)
p = THEME + '/sections/ms-footer.liquid'
t = open(p).read()
if 'ms-footlegal' not in t:
    t = t.replace('<div data-ms="footlegal" style="display: flex; flex-wrap: wrap; gap: 22px;">', '<div data-ms="footlegal" class="ms-footlegal" style="display: flex; flex-wrap: wrap; gap: 22px;">', 1)
    t = t.replace('{% schema %}', '<style>.ms-footlegal { padding-right: 76px; } @media (max-width: 600px) { .ms-footlegal { padding-right: 70px; } }</style>\n{% schema %}', 1)
    assert 'ms-footlegal' in t
    open(p, 'w').write(t)

# one spelling across the house: fibre (the brand Orange Fiber keeps its own)
for f in glob.glob(THEME + '/sections/ms-*.liquid') + glob.glob(THEME + '/templates/*.json'):
    if f.endswith('ms-note-cat.liquid'):
        continue
    t = open(f).read()
    u = re.sub(r'(?<!Orange )\bfiber(s?)\b', r'fibre\1', t)
    u = re.sub(r'(?<!Orange )\bFiber(s?)\b(?! ™)', lambda m: 'Fibre' + m.group(1), u)
    if u != t:
        open(f, 'w').write(u)

# ── a note's ending (sign-off and the notes either side) as its own piece, so a note with a quiz, a film or a
#    gallery below its text ends after them, not before
p = THEME + '/sections/ms-article.liquid'
t = open(p).read()
if "render 'ms-article-end'" not in t:
    a = t.index('<aside class="ms-art-end"')
    b = t.index('</nav>\n{%- endif -%}\n', a) + len('</nav>\n{%- endif -%}\n')
    end = t[a:b]
    snip = end.replace('section.settings.', 's.').replace('blog.url', 'b.url').replace('blog.articles', 'b.articles').replace('a.url == article.url', 'a.url == art.url')
    snip = snip.replace('for a in b.articles limit: 50', 'for x in b.articles limit: 50').replace('      assign older = a\n', '      assign older = x\n').replace('    if a.url == art.url\n', '    if x.url == art.url\n').replace('    assign last = a\n', '    assign last = x\n')
    head = ("{%- comment -%} The end of a Journal note: a sign-off from the atelier, then the notes either side with their pictures.\n"
            "  Usage: {% render 'ms-article-end', s: section.settings, art: article, b: blog %} {%- endcomment -%}\n"
            "{%- capture cat -%}{% render 'ms-note-cat', a: art %}{%- endcapture -%}{%- capture kicker -%}{% render 'ms-note-cat', label: cat %}{%- endcapture -%}\n")
    assert 'article.' not in snip.replace('art.', ''), 'unrenamed article reference'
    open(THEME + '/snippets/ms-article-end.liquid', 'w').write(head + snip)
    t = t[:a] + "{%- unless section.settings.end_after -%}{% render 'ms-article-end', s: section.settings, art: article, b: blog %}{%- endunless -%}\n" + t[b:]
    t = t.replace('"settings": [\n', '"settings": [\n    { "type": "checkbox", "id": "end_after", "label": "End the note after the sections below", "info": "On when a Note ending section is added further down.", "default": false },\n', 1)
    open(p, 'w').write(t)
    # the ending as a section, carrying the same words
    sch = json.loads(t[t.index('{% schema %}') + 12:t.index('{% endschema %}')])
    keep = [x for x in sch['settings'] if x.get('id') in ('all', 'cta', 'more', 'same', 'older', 'newer', 'end_label', 'end_heading', 'end_text')]
    open(THEME + '/sections/ms-article-end.liquid', 'w').write(
        "{%- comment -%} The end of a Journal note, placed after the note's own sections. {%- endcomment -%}\n"
        "{%- if template.name == 'article' -%}{% render 'ms-article-end', s: section.settings, art: article, b: blog %}{%- endif -%}\n"
        "{% schema %}\n" + json.dumps({'name': 'Note ending', 'settings': keep, 'presets': [{'name': 'Note ending'}]}, indent=2, ensure_ascii=False) + "\n{% endschema %}\n")
for f in glob.glob(THEME + '/templates/article*.json'):
    raw = open(f).read()
    m = re.match(r'(\s*/\*.*?\*/\s*)?', raw, re.S)
    data = json.loads(raw[m.end():])
    extra = [k for k in data['order'] if data['sections'][k]['type'] not in ('ms-article', 'ms-article-rail', 'ms-article-end')]
    if not extra or 'end' in data['sections']:
        continue
    art = next(k for k in data['order'] if data['sections'][k]['type'] == 'ms-article')
    data['sections'][art].setdefault('settings', {})['end_after'] = True
    data['sections']['end'] = {'type': 'ms-article-end', 'settings': {}}
    pos = data['order'].index('more') if 'more' in data['order'] else len(data['order'])
    data['order'].insert(pos, 'end')
    open(f, 'w').write((m.group(1) or '') + json.dumps(data, indent=2, ensure_ascii=False) + '\n')
print('note endings placed')

# ── a note for search engines and AI assistants: one BlogPosting (the house's own, apps' copies switched off),
#    the date it was last revised shown beside the date it was written
p = THEME + '/sections/ms-article.liquid'
t = open(p).read()
if 'BlogPosting' not in t:
    old = "{{ article.published_at | date: '%-d %B %Y' }} · {{ minutes }} {{ section.settings.minutes }}</div>"
    assert old in t
    t = t.replace(old, "<time datetime=\"{{ article.published_at | date: '%Y-%m-%d' }}\">{{ article.published_at | date: '%-d %B %Y' }}</time>"
                       "{%- liquid\n  assign ms_pub = article.published_at | date: '%s' | plus: 0\n  assign ms_upd = article.updated_at | date: '%s' | plus: 0\n  assign ms_gap = ms_upd | minus: ms_pub\n-%}"
                       "{%- if ms_gap > 604800 %} · {{ section.settings.updated | default: 'Updated' }} <time datetime=\"{{ article.updated_at | date: '%Y-%m-%d' }}\">{{ article.updated_at | date: '%-d %B %Y' }}</time>{%- endif %}"
                       " · {{ minutes }} {{ section.settings.minutes }}</div>", 1)
    ld = """{%- liquid
  assign ld_img = article.image | default: blog.image
  assign ld_desc = article.excerpt_or_content | strip_html | strip_newlines | truncate: 300
  if article.metafields.global.description_tag != blank
    assign ld_desc = article.metafields.global.description_tag
  endif
-%}
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "@id": "{{ shop.url }}{{ article.url }}#article",
  "mainEntityOfPage": { "@type": "WebPage", "@id": "{{ shop.url }}{{ article.url }}" },
  "headline": {{ article.title | strip_html | truncate: 110 | json }},
  "description": {{ ld_desc | json }},
  {%- if ld_img %}
  "image": [{{ ld_img | image_url: width: 1600 | prepend: 'https:' | json }}],
  {%- endif %}
  "datePublished": {{ article.published_at | date: '%Y-%m-%dT%H:%M:%S%z' | json }},
  "dateModified": {{ article.updated_at | default: article.published_at | date: '%Y-%m-%dT%H:%M:%S%z' | json }},
  "inLanguage": {{ request.locale.iso_code | json }},
  {%- if article.author != blank %}
  "author": { "@type": "Person", "name": {{ article.author | json }} },
  {%- else %}
  "author": { "@id": "{{ shop.url }}/#organization" },
  {%- endif %}
  "publisher": { "@id": "{{ shop.url }}/#organization" },
  "isPartOf": { "@type": "Blog", "name": {{ blog.title | json }}, "url": "{{ shop.url }}{{ blog.url }}" },
  {%- if kicker != blank %}
  "articleSection": {{ kicker | strip | json }},
  {%- endif %}
  "keywords": {{ article.tags | join: ', ' | json }},
  "wordCount": {{ words | json }}
}
</script>
"""
    t = t.replace('<div class="ms-read" aria-hidden="true">', ld + '<div class="ms-read" aria-hidden="true">', 1)
    t = t.replace('    { "type": "text", "id": "minutes", "label": "Reading time label", "default": "minute read" },',
                  '    { "type": "text", "id": "minutes", "label": "Reading time label", "default": "minute read" },\n'
                  '    { "type": "text", "id": "updated", "label": "Updated label", "info": "Shown when a note was revised more than a week after it was published.", "default": "Updated" },', 1)
    assert 'BlogPosting' in t and '"updated"' in t
    open(p, 'w').write(t)

# tag listings and filtered journals are thin copies of the Journal: kept out of the index, links still followed
p = THEME + '/snippets/meta-tags.liquid'
t = open(p).read()
if 'current_tags != blank' not in t:
    t = t.replace("  if request.page_type == 'collection' and collection.handle == 'all'\n    assign ms_noindex = true\n  endif\n",
                  "  if request.page_type == 'collection' and collection.handle == 'all'\n    assign ms_noindex = true\n  endif\n"
                  "  if current_tags != blank\n    assign ms_noindex = true\n  endif\n", 1)
    assert 'current_tags != blank' in t
    open(p, 'w').write(t)
print('article schema')

# ── Our story carries the house's recognition: its Recognition band links the Green Product
#    Award to the award's own page (a third-party citation), and the press follows
for tpl in ():   # (press band now lives on the home page and the press page only)
    d = load(tpl)
    if not any(v['type'] == 'ms-hp-proof' for v in d['sections'].values()):
        d['sections']['proof'] = json.loads(json.dumps(S['proof']))
        d['sections']['proof']['settings']['show_award'] = False   # the page's Recognition band tells it
        d['order'].insert(d['order'].index('next') if 'next' in d['order'] else len(d['order']), 'proof')
        open('%s/templates/%s.json' % (THEME, tpl), 'w').write(HEAD % 'Our story: the About page (about-midsummer-milano), in the house\'s own design.' + json.dumps(d, indent=2, ensure_ascii=False) + '\n')

# ── Midsummer Milano at a glance: the facts, one per row, each with the page that tells it in full
#    (a page with the handle midsummer-milano-at-a-glance opens in it; until then ?view=ms-facts)
def fact(label, value, place='none', link=''):
    return ('fact', {'label': label, 'value': value, 'link_place': place, 'link_label': link})
FACTS = [
    ('ms-facts', {'text': '<p>The essentials about the house, in plain words, for clients, journalists and partners.</p>'}, [
        fact('The house', '<p>Midsummer Milano is a luxury bed and mattress house from Milan. Every piece is made to order, by hand in Italy, from natural fibres only.</p>', 'story', 'Our story'),
        fact('Founded', '<p>In Milan, in 2014, by an architect who wanted the bed designed with the same care as every other piece of a room.</p>'),
        fact('What we make', '<p>Mattresses, mattress toppers, boxsprings and beds with headboards; duvets, pillows, blankets and throws.</p>', 'collections', 'Compare the collections'),
        fact('Collections', '<p>Essentials, Signature and Icons. The same hands make all three; they differ in the cloth, the rarity of the fibres and how far the bespoke goes.</p>', 'quiz', 'Find your Midsummer'),
        fact('Made', '<p>By hand in Italy, one by one, by two artisans, start to finish. Nothing is made before it is specified.</p>', 'handmade', 'Handmade in Italy'),
        fact('Natural fibres', '<p>Baby alpaca, camel hair, Cheviot and Falkland wool, horsehair, vegetable horsehair, yak hair, mohair, cashmere, silk, linen, organic cotton, Ingeo and Orange Fiber; vicuña in the Icons collection.</p>', 'materials', 'Natural materials'),
        fact('Fabrics', '<p>Loro Piana Interiors, chosen from the fabric book against the bed itself.</p>', 'loro', 'Loro Piana Interiors'),
        fact('Made to measure', '<p>Any dimension, height or radius, round beds included, with no tooling charge. Size, firmness, fibres and cloth are chosen with you.</p>'),
        fact('Made to last', '<p>15 + 15: at fifteen years the mattress returns to the artisans who made it and is regenerated for fifteen more.</p>', 'regen', 'The 15 + 15 service'),
        fact('Prices', '<p>On request. Each system is quoted from its specification, after a consultation at the atelier or by video.</p>'),
        fact('Atelier', '<p>Via Andegari 4, 20121 Milano, Italy. By appointment, Monday to Friday, 09:00–12:00 and 13:00–18:00, or by video call.</p>', 'atelier', 'The atelier'),
        fact('Where to see the beds', '<p>Showrooms, agents and resellers in Italy, San Marino, the United Kingdom, Poland, Russia, Canada, the United States and Hong Kong.</p>', 'agents', 'Agents & Resellers'),
        fact('Delivery', '<p>Worldwide. White-glove delivery by our own team: the bed is brought into the room, assembled and dressed.</p>'),
        fact('Clients', '<p>Private homes, architects and interior designers, hotels, villas and yachts.</p>', 'professionals', 'Professionals'),
        fact('Recognition', '<p>Green Product Award 2025 for the Top system (<a href="https://www.gp-award.com/en/produkte/top-bed-system" target="_blank" rel="noopener">the award</a>). Featured by Il Sole 24 Ore, Kommersant, Elle Decor and Architectural Digest; at the Salone del Mobile, Milan.</p>', 'press', 'Press'),
        fact('Languages', '<p>Italian, English and Russian.</p>'),
    ]),
]
write('page.facts', 'Midsummer Milano at a glance (a store page with the handle midsummer-milano-at-a-glance opens in it, or ?view=facts).', FACTS)
write('collection.ms-facts', 'Midsummer Milano at a glance, reachable before its page exists (?view=ms-facts).', FACTS)

# the footer's house column ends with the house at a glance
p = THEME + '/sections/ms-footer.liquid'
t = open(p).read()
if "to: 'facts'" not in t:
    a = '{%- if ms_u1 != blank -%}<a data-ms-quiz-link="" href="{{ ms_u1 }}">{{ section.settings.t13 }}</a>{%- endif -%}'
    assert t.count(a) == 1
    t = t.replace(a, a + '<a href="{% render \'ms-link\', to: \'facts\' %}">{{ section.settings.facts_label }}</a>', 1)
    t = t.replace('  "settings": [\n', '  "settings": [\n    {\n      "type": "text",\n      "id": "facts_label",\n      "label": "At a glance link",\n      "default": "At a glance"\n    },\n', 1)
    assert 'facts_label' in t
    open(p, 'w').write(t)
print('facts and recognition')

# the Recognition band (Our story) links the award to its own page
p = THEME + '/sections/ms-home-08.liquid'
t = open(p).read()
if 'award_link' not in t:
    a = '{{ section.settings.t3 }}</figcaption>'
    assert t.count(a) == 1
    t = t.replace(a, '{{ section.settings.t3 }}{%- if section.settings.award_link != blank -%}<a href="{{ section.settings.award_link }}" target="_blank" rel="noopener" style="margin-top: 10px; width: fit-content; font-size: 10.5px; letter-spacing: 0.22em; text-transform: uppercase; color: #FBF9F5; border-bottom: 1px solid rgba(251, 249, 245, 0.6); padding-bottom: 3px;">{{ section.settings.award_link_label }} <span aria-hidden="true">→</span></a>{%- endif -%}</figcaption>', 1)
    t = t.replace('  "settings": [\n', '  "settings": [\n    {\n      "type": "text",\n      "id": "award_link",\n      "label": "Award page (address)",\n      "default": "https://www.gp-award.com/en/produkte/top-bed-system"\n    },\n    {\n      "type": "text",\n      "id": "award_link_label",\n      "label": "Award link",\n      "default": "The award"\n    },\n', 1)
    assert 'award_link_label' in t
    open(p, 'w').write(t)

# ── the store's Icons collection lives at /collections/icon: every check that names the Icons
#    collection by its handle accepts both spellings, and the collection tabs link through ms-link
for f in glob.glob(THEME + '/sections/ms-*.liquid') + glob.glob(THEME + '/snippets/ms-*.liquid'):
    t = open(f).read(); u = t
    u = re.sub(r"c\.handle == 'icons'(?! or c\.handle == 'icon')", "c.handle == 'icons' or c.handle == 'icon'", u)
    u = re.sub(r"(\n\s*)when 'icons'\n", r"\1when 'icons', 'icon'\n", u)
    if f.endswith('ms-collection-grid.liquid'):
        u = u.replace('<a href="{{ routes.collections_url }}/{{ k }}" style="{% if collection.handle == k %}',
                      '{%- assign kh = collection.handle -%}{%- if kh == \'icon\' -%}{%- assign kh = \'icons\' -%}{%- endif -%}<a href="{% render \'ms-link\', to: k %}" style="{% if kh == k %}')
        assert "render 'ms-link', to: k" in u
    if u != t:
        open(f, 'w').write(u)

# ── collection openings: Essentials and Icons open on the house's own photographs (a photograph
#    chosen in the section still wins); Signature keeps its collection image
p = THEME + '/sections/ms-collection-hero.liquid'
t = open(p).read()
if 'tier_photo' not in t:
    t = t.replace("  endcase\n-%}", """  endcase
  assign tier_photo = ''
  assign tier_pos = 'center'
  case tier
    when 'essentials'
      assign tier_photo = 'ms-photo-glass-house.jpg' | asset_url
      assign tier_pos = 'center 62%'
    when 'icons', 'icon'
      assign tier_photo = 'ms-graded-arches.jpg' | asset_url
      assign tier_pos = 'center 64%'
  endcase
-%}""", 1)
    a = '{%- elsif collection.image != blank -%}'
    assert t.count(a) == 1
    t = t.replace(a, '{%- elsif tier_photo != blank -%}\n<img alt="{{ collection.title | escape }}" width="1920" height="1280" src="{{ tier_photo }}" style="width: 100%; height: min(66vh, 640px); object-fit: cover; object-position: {{ tier_pos }}; display: block;" fetchpriority="high">\n' + a, 1)
    assert 'tier_photo' in t
    open(p, 'w').write(t)

# ── what each system is made of, for the collection pages: its fibres (from its own product
#    template) and the qualities the Natural materials page gives each fibre
# what each fibre answers; a system is judged by its three defining fibres (listed first), so the
# needs filter still tells the systems apart
# (Round 21, checked against the Natural materials page: wool and silk also temper the bed, but they are in
# nearly every system, so warmth is credited to the fibres that bring it: cashmere, camel, yak, alpaca,
# mohair and vicuña; otherwise Temperature would list 23 of the 25 systems)
QUAL = {'Baby Alpaca': 'temperature hypoallergenic', 'Alpaca': 'temperature hypoallergenic', 'Alpaca Wool': 'temperature hypoallergenic',
        'Cheviot Wool': 'support', 'Wool': 'support', 'Falkland Wool': 'support', 'Falkland': 'support',
        'Horsehair': 'support breathability', 'Vegetable Horsehair': 'support breathability', 'Yak Hair': 'temperature softness',
        'Vicuña': 'softness temperature', 'Cashmere': 'temperature softness', 'Mongolian Cashmere': 'temperature softness',
        'Mohair': 'temperature', 'Camel Hair': 'temperature', 'Linen': 'breathability', 'Silk': 'softness',
        'Cotton': 'breathability', 'Organic Cotton': 'breathability', 'Ingeo': 'breathability', 'Orange Fiber': 'breathability'}
# Round 21: what the 2026 catalogue says of a system outright is added to what its fibres say (each
# with the fibre that does it, so the line under the needs names it): Top's winter side "for warmth"
# and summer side "for breathability", with horsehair and wool; Paisley "a delicate balance of warmth
# and breathability"; Vivaldi's summer side "offers breathability" (wool and cotton), and so Vivaldi Plus;
# Raffaello's "soft baby alpaca"; Roma's winter topper "soft and warm", in cashmere; Monteverdi's
# vegetable horsehair and linen, "known for their breathability, resilience and natural thermoregulation"
NEED_SAID = {
    'top-2': [('Linen', 'breathability'), ('Horsehair', 'support breathability'), ('Cheviot Wool', 'support')],
    'paisley': [('Linen', 'breathability')],
    'vivaldi-2': [('Cotton', 'breathability')],
    'vivaldi-plus': [('Cotton', 'breathability')],
    'raffaello': [('Baby Alpaca', 'softness')],
    'roma': [('Cashmere', 'temperature')],
    'monteverdi': [('Vegetable Horsehair', 'temperature'), ('Linen', 'temperature')],
}
lines = []
for suffix, info in PRODUCT_TPLS.items():
    if suffix in ('', 'appointment', 'perfumes'):
        continue
    names = SYSTEM_FIBRES.get(suffix) or [NAME.get(n, n) for (n, img) in info['mats']]
    q = sorted({w for n in names[:3] for w in QUAL.get(n, '').split()})
    # Round 21: and which of those three fibres answers which need, so the collection page's line
    # under the needs names only the fibres of the beds it shows ("Fibre:need need|…")
    d = '|'.join('%s:%s' % (n, QUAL[n]) for n in names[:3] if QUAL.get(n))
    for _f, _n in NEED_SAID.get(suffix, []):
        q = sorted(set(q) | set(_n.split()))
        _parts = [x for x in d.split('|') if x]
        for _i, _x in enumerate(_parts):
            if _x.split(':')[0] == _f:  # the fibre is already named: its new quality joins it
                _have = _x.split(':', 1)[1].split()
                _parts[_i] = '%s:%s' % (_f, ' '.join(_have + [w for w in _n.split() if w not in _have]))
                break
        else:
            _parts.append('%s:%s' % (_f, _n))
        d = '|'.join(_parts)
    # a topper is the surface of a bed: it is chosen for softness, warmth or freshness, never for support
    if suffix.startswith('topper'):
        q = [w for w in q if w != 'support']
        d = '|'.join(e for e in ('%s:%s' % (x.split(':')[0], ' '.join(w for w in x.split(':')[1].split() if w != 'support')) for x in d.split('|') if x) if e.split(':')[1])
    keys = sorted({suffix, re.sub(r'-\d+$', '', suffix)})
    lines.append("    when %s\n      echo %s" % (', '.join("'%s'" % k for k in keys), json.dumps(','.join(names) + '~' + ' '.join(q) + '~' + d, ensure_ascii=False).replace('"', "'")))
snip = """{%- comment -%}
  What a system is made of, for the collection pages: "fibre,fibre~quality quality".
  Found by the product's template (its own fibres), then by its handle. Generated from the
  product templates: a new template's fibres appear here at the next build.
{%- endcomment -%}
{%- liquid
  assign k = key | default: handle
  case k
""" + '\n'.join(lines) + """
    else
      case handle
""" + '\n'.join('  ' + l.replace('\n', '\n  ') for l in lines) + """
      endcase
  endcase
-%}
"""
open(THEME + '/snippets/ms-system-facts.liquid', 'w').write(snip)

# the store's collection pages list their systems by what matters to the sleeper
p = THEME + '/templates/collection.json'
d = load('collection')
for k, v in d['sections'].items():
    if v['type'] == 'ms-collection-grid':
        v['type'] = 'ms-systems'
        v['settings'] = {}
open(p, 'w').write(HEAD % 'a collection: its opening, its words, and its systems chosen by what matters to the sleeper.' + json.dumps(d, indent=2, ensure_ascii=False) + '\n')
print('collection systems')

# ── a note, reimagined: the title, the summary and the photograph share the first screen; the
#    text runs in a generous column beside a quiet rail (what is in the note, sharing); numbered
#    lists become a grid of numbered cards instead of a long single file
p = THEME + '/sections/ms-article.liquid'
t = open(p).read()
if 'ms-art-hero' not in t:
    a = t.index('<section style="padding: clamp(60px, 9vw, 140px)')
    b = t.index('{%- unless section.settings.end_after -%}')
    head = r'''{%- liquid
  assign ms_pub = article.published_at | date: '%s' | plus: 0
  assign ms_upd = article.updated_at | date: '%s' | plus: 0
  assign ms_gap = ms_upd | minus: ms_pub
  assign dek = article.excerpt | strip_html | strip | truncate: 260
-%}
<section class="ms-art-hero{% unless article.image %} is-plain{% endunless %}">
  <div class="ms-art-hero__txt">
    <a class="ms-art-back" href="{{ blog.url }}"><span aria-hidden="true">←</span> {{ section.settings.all }}</a>
    <div class="ms-art-kicker"><svg aria-hidden="true" height="20" viewBox="0 0 24 24" width="20"><path d="M4 20 C4 11 11 4 20 4 C20 13 13 20 4 20 Z" fill="none" stroke="currentColor" stroke-width="1.1"></path><path d="M4 20 L14 10" fill="none" stroke="currentColor" stroke-width="1.1"></path></svg>{{ kicker }}</div>
    <h1 class="ms-art-title">{{ article.title }}</h1>
    {%- if dek != blank -%}<p class="ms-art-dek">{{ dek }}</p>{%- endif -%}
    <div class="ms-art-meta"><time datetime="{{ article.published_at | date: '%Y-%m-%d' }}">{{ article.published_at | date: '%-d %B %Y' }}</time>{%- if ms_gap > 604800 %}<span>{{ section.settings.updated | default: 'Updated' }} <time datetime="{{ article.updated_at | date: '%Y-%m-%d' }}">{{ article.updated_at | date: '%-d %B %Y' }}</time></span>{%- endif %}<span>{{ minutes }} {{ section.settings.minutes }}</span></div>
  </div>
  {%- if article.image -%}
  <figure class="ms-art-hero__img">
    <img alt="{{ article.image.alt | default: article.title | escape }}" src="{{ article.image | image_url: width: 1800 }}" srcset="{{ article.image | image_url: width: 900 }} 900w, {{ article.image | image_url: width: 1400 }} 1400w, {{ article.image | image_url: width: 2000 }} 2000w" sizes="(max-width: 1000px) 100vw, 56vw" width="1800" height="2250" fetchpriority="high">
  </figure>
  {%- endif -%}
</section>
<div class="ms-art-layout">
  <aside class="ms-art-aside">
    <div class="ms-art-aside__in">
      <nav class="ms-art-toc" data-ms-toc hidden aria-label="{{ section.settings.toc | default: 'In this note' | escape }}"><span>{{ section.settings.toc | default: 'In this note' }}</span><ol></ol></nav>
      <div class="ms-art-share" aria-label="Share">
        <span>{{ section.settings.share | default: 'Share' }}</span>
        <a href="https://wa.me/?text={{ article.title | url_encode }}%20{{ shop.url | append: article.url | url_encode }}" target="_blank" rel="noopener">WhatsApp</a>
        <a href="https://www.linkedin.com/sharing/share-offsite/?url={{ shop.url | append: article.url | url_encode }}" target="_blank" rel="noopener">LinkedIn</a>
        <a href="https://pinterest.com/pin/create/button/?url={{ shop.url | append: article.url | url_encode }}{% if article.image %}&media={{ article.image | image_url: width: 1600 | prepend: 'https:' | url_encode }}{% endif %}&description={{ article.title | url_encode }}" target="_blank" rel="noopener">Pinterest</a>
        <a href="mailto:?subject={{ article.title | url_encode }}&body={{ shop.url | append: article.url | url_encode }}">Email</a>
        <button type="button" data-ms-copy="{{ shop.url | append: article.url }}">{{ section.settings.copy | default: 'Copy link' }}</button>
      </div>
    </div>
  </aside>
  <div class="ms-article-body">
{{ article.content }}
  </div>
</div>
'''
    t = t[:a] + head + t[b:]
    css = r'''<style>
  /* the note, reimagined: one opening screen, a generous column, a quiet rail */
  .ms-art-hero { max-width: 1440px; margin: 0 auto; padding: clamp(104px, 10vw, 150px) clamp(18px, 5vw, 80px) 0; display: grid; grid-template-columns: minmax(0, 5fr) minmax(0, 6fr); gap: clamp(32px, 5vw, 96px); align-items: center; }
  .ms-art-hero.is-plain { grid-template-columns: minmax(0, 1fr); max-width: 980px; }
  .ms-site .ms-art-hero a.ms-art-back { margin-bottom: clamp(22px, 2.6vw, 34px); }
  .ms-art-kicker { display: flex; align-items: center; gap: 11px; font-size: 11px; letter-spacing: .28em; text-transform: uppercase; color: #7E623B; }
  .ms-site .ms-art-title { font-family: Newsreader, Georgia, serif; font-weight: 200; font-size: clamp(38px, 4.6vw, 74px); line-height: 1.02; letter-spacing: -0.035em; color: #17140F; margin-top: 18px; text-wrap: balance; }
  .ms-art-dek { font-family: Newsreader, Georgia, serif; font-style: italic; font-weight: 300; font-size: clamp(19px, 1.7vw, 23px); line-height: 1.5; color: #4A443B; margin-top: clamp(18px, 2vw, 26px); max-width: 40ch; }
  .ms-art-meta { display: flex; flex-wrap: wrap; gap: 6px 18px; margin-top: clamp(22px, 2.4vw, 32px); padding-top: 18px; border-top: 1px solid #DDD6C9; font-size: 11px; letter-spacing: .16em; text-transform: uppercase; color: #6E675C; max-width: 460px; }
  .ms-art-hero__img { margin: 0; }
  .ms-art-hero__img img { display: block; width: 100%; height: min(78vh, 820px); object-fit: cover; background: #EDE6D9; }
  .ms-art-layout { max-width: 1240px; margin: 0 auto; padding: clamp(56px, 7vw, 110px) clamp(18px, 5vw, 80px) clamp(48px, 6vw, 96px); display: grid; grid-template-columns: 200px minmax(0, 760px); gap: clamp(40px, 6vw, 110px); justify-content: center; align-items: start; }
  .ms-art-aside { position: sticky; top: 120px; }
  .ms-art-toc span { display: block; font-size: 10.5px; letter-spacing: .26em; text-transform: uppercase; color: #7E623B; padding-bottom: 12px; border-bottom: 1px solid #DDD6C9; }
  .ms-art-toc ol { list-style: none; margin: 0; padding: 0; counter-reset: t; }
  .ms-art-toc li { counter-increment: t; border-bottom: 1px solid #ECE6DB; }
  .ms-site .ms-art-toc a { display: grid; grid-template-columns: 22px 1fr; padding: 10px 0; font-size: 13px; line-height: 1.45; color: #6E675C; text-decoration: none; transition: color .3s ease; }
  .ms-art-toc a::before { content: counter(t, decimal-leading-zero); font-family: Newsreader, Georgia, serif; font-size: 12px; color: #B5AA97; }
  .ms-site .ms-art-toc a:hover, .ms-site .ms-art-toc a.is-on { color: #17140F; }
  .ms-art-aside .ms-art-share { flex-direction: column; align-items: flex-start; gap: 2px; margin-top: 30px; padding-top: 0; border-top: 0; }
  .ms-art-aside .ms-art-share span { padding-bottom: 8px; }
  .ms-site .ms-article-body { max-width: none !important; padding: 0 !important; margin: 0 !important; display: flex; flex-direction: column; gap: 22px; font-size: 18px !important; line-height: 1.85 !important; color: #2E2A24 !important; }
  .ms-site .ms-article-body > * { margin: 0; }
  .ms-site .ms-article-body h2 { font-size: clamp(28px, 2.8vw, 38px); line-height: 1.15; margin-top: 28px; padding-top: 28px; border-top: 1px solid #DDD6C9; scroll-margin-top: 110px; }
  .ms-site .ms-article-body h2:first-child { margin-top: 0; padding-top: 0; border-top: 0; }
  .ms-site .ms-article-body h3 { font-size: clamp(21px, 2vw, 25px); margin-top: 10px; scroll-margin-top: 110px; }
  .ms-site .ms-article-body img { max-height: none; width: 100% !important; margin: 8px 0 !important; }
  .ms-site .ms-article-body ul { list-style: none; padding: 0; display: grid; gap: 10px; }
  .ms-site .ms-article-body ul > li { position: relative; padding-left: 26px; }
  .ms-site .ms-article-body ul > li::before { content: ''; position: absolute; left: 0; top: .9em; width: 14px; height: 1px; background: #7E623B; }
  .ms-site .ms-article-body ol { list-style: none; padding: 0; counter-reset: n; display: grid; gap: 12px; }
  .ms-site .ms-article-body ol > li { counter-increment: n; position: relative; padding: 20px 22px 20px 64px; background: #F4EFE5; line-height: 1.7; }
  .ms-site .ms-article-body ol > li::before { content: counter(n); position: absolute; left: 22px; top: 14px; font-family: Newsreader, Georgia, serif; font-weight: 200; font-size: 32px; line-height: 1; color: #7E623B; }
  .ms-site .ms-article-body ol:has(> li:nth-child(4)) { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .ms-site .ms-article-body ol:has(> li:nth-child(4)) > li:last-child:nth-child(odd) { grid-column: 1 / -1; }
  .ms-site .ms-article-body ol > li strong:first-child, .ms-site .ms-article-body ol > li b:first-child { display: block; font-family: Newsreader, Georgia, serif; font-weight: 400; font-size: 19px; color: #17140F; margin-bottom: 4px; }
  .ms-site .ms-article-body p > strong:first-child { color: #17140F; font-weight: 500; }
  @media (max-width: 1000px) {
    .ms-art-hero { grid-template-columns: minmax(0, 1fr); padding-top: clamp(96px, 14vw, 120px); }
    .ms-art-hero__img { order: -1; margin: 0 calc(-1 * clamp(18px, 5vw, 80px)); }
    .ms-art-hero__img img { height: auto; aspect-ratio: 4 / 3; }
    .ms-art-layout { grid-template-columns: minmax(0, 1fr); padding-top: 44px; }
    .ms-art-aside { position: static; order: 2; }
    .ms-art-toc { display: none; }
    .ms-art-aside .ms-art-share { flex-direction: row; flex-wrap: wrap; gap: 8px 20px; margin-top: 0; padding-top: 22px; border-top: 1px solid #DDD6C9; }
    .ms-site .ms-article-body { font-size: 17px !important; }
  }
  @media (max-width: 640px) {
    .ms-site .ms-article-body ol:has(> li:nth-child(4)) { grid-template-columns: minmax(0, 1fr); }
    .ms-art-hero__img { order: 0; }
  }
</style>
<script>
  (function () {
    var body = document.querySelector('.ms-article-body'), nav = document.querySelector('[data-ms-toc]');
    if (!body || !nav) return;
    var hs = Array.prototype.slice.call(body.querySelectorAll('h2'));
    if (hs.length < 2) return;
    var ol = nav.querySelector('ol'), links = [];
    hs.forEach(function (h, i) {
      if (!h.id) h.id = 'part-' + (i + 1);
      var li = document.createElement('li'), a = document.createElement('a');
      a.href = '#' + h.id; a.textContent = h.textContent.trim();
      li.appendChild(a); ol.appendChild(li); links.push(a);
    });
    nav.hidden = false;
    if ('IntersectionObserver' in window) {
      var io = new IntersectionObserver(function (es) {
        es.forEach(function (e) { if (e.isIntersecting) { var i = hs.indexOf(e.target); links.forEach(function (l, k) { l.classList.toggle('is-on', k === i); }); } });
      }, { rootMargin: '-20% 0px -70% 0px' });
      hs.forEach(function (h) { io.observe(h); });
    }
  })();
</script>
{% schema %}'''
    t = t.replace('{% schema %}', css, 1)
    t = t.replace('    { "type": "text", "id": "share", "label": "Share label", "default": "Share" },',
                  '    { "type": "text", "id": "share", "label": "Share label", "default": "Share" },\n    { "type": "text", "id": "toc", "label": "Contents label", "default": "In this note" },', 1)
    assert 'ms-art-hero' in t and '"toc"' in t
    open(p, 'w').write(t)
print('note reimagined')

# ── the collections say only what the house's catalogue says: Signature and Icons systems are made
#    in Loro Piana Interiors where the system calls for it, not all of them (bin/lp_data.py)
COLL_FIX = [
    ('The heart of the collection. Loro Piana Interiors fabrics, exclusive blends of precious natural fibres: Yak, camel hair, silk, cashmere over spring architectures designed for the highest comfort.',
     'The heart of the collection. Exclusive blends of precious natural fibres: yak, camel hair, silk, cashmere, in natural linen and cotton or in Loro Piana Interiors, designed for the highest comfort.'),
    ('Vicuña, cashmere, fully upholstered in Loro Piana Interiors.', 'Vicuña, cashmere, most of them made in Loro Piana Interiors.'),
]
for f in (THEME + '/sections/ms-beds-02.liquid', THEME + '/sections/ms-collection-intro.liquid'):
    t = open(f).read()
    for a, b in COLL_FIX:
        t = t.replace(a, b)
    assert 'fully upholstered in Loro Piana' not in t, f
    open(f, 'w').write(t)
print('collections: Loro Piana Interiors where it is used')
