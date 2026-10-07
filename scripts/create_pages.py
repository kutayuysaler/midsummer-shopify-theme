#!/usr/bin/env python3
"""Give every page that has a design in the Midsummer Milano theme its template, and create
the ones the store doesn't have yet.

For each designed place, the store's existing page is used if it has one (under any of the
addresses the theme knows, e.g. italian-craftsmen-luxury-mattresses for Handmade in Italy),
and switched to the theme's template; its text is left as it is. Only a place with no page
at all gets a new one, with its text. Nothing is ever deleted.

Needs an Admin API token with the read_content and write_content scopes (Shopify admin →
Settings → Apps and sales channels → Develop apps → Create an app → Admin API scopes →
Install → copy the Admin API access token). Publish the theme first, then:

    SHOPIFY_STORE=your-store.myshopify.com SHOPIFY_ADMIN_TOKEN=shpat_... python3 scripts/create_pages.py

Python 3 only, no packages to install. Add --dry-run to see what would happen first.
"""
import json, os, sys, urllib.request, urllib.error

API = '2025-01'

# (template, handles the theme recognises — same order as snippets/ms-link.liquid, the
#  first is used when the page is created —, title and text for a new page)
PLACES = [
    ('professionals', ['professionals', 'architects-and-interior-designers', 'architects-interior-designers', 'for-architects', 'trade'],
     'Architects & Interior Designers', '<p>For architects and interior designers, Midsummer Milano is a material and a method rather than a catalogue. We work from your drawing: dimensions, heights and radii, including fully round beds, with no tooling charge.</p><p>We send drawings, sections and material schedules for your set, fabric references from Loro Piana Interiors, and samples of the natural fibres. One person at the atelier follows the project from specification to installation.</p>'),
    ('hospitality', ['hospitality', 'hospitality-and-contract', 'contract', 'hotels'],
     'Hospitality', '<p>A guest remembers the bed. It is the one piece of furniture they spend eight hours inside.</p><p>For hotels and private residences we make volume programmes to the room, handmade in Milano by the same two artisans for every bed, with handover dates planned with you, and regeneration in contract at fifteen years so the beds your guests remember stay the beds they remember.</p>'),
    ('handmade-in-italy', ['italian-craftsmen-luxury-mattresses', 'handmade-in-italy', 'handmade', 'made-in-italy', 'italian-craftsmen'],
     'Handmade in Italy', '<p>Every piece is built by hand, from start to finish, by the same two Italian artisans: two or three full days of work for each mattress. It is not a marketing promise; it is a method.</p><p>Because one pair of hands follows the bed through every stage, nothing goes inside it that its makers did not choose and place themselves. And because they know it from the inside, the bed can come back to them at fifteen years to be opened, renewed and made ready for fifteen more.</p>'),
    ('sleep-culture', ['sleep-culture', 'the-culture-of-sleep', 'culture-of-sleep'],
     'Sleep Culture', '<p>Midsummer Milano began with a question its founder, an architect, kept asking: why is the bed treated as a technical product from a catalogue, when every other piece of a room is chosen with care?</p><p>Sleep Culture is where we follow that question: how material, temperature, proportion and ritual shape the night, and what making beds by hand, and listening to the people who sleep in them, has taught us.</p>'),
    ('agents-and-resellers', ['agents-and-resellers', 'agents-resellers', 'store-locator', 'stockists', 'where-to-find-us'],
     'Agents & Resellers', '<p>The beds are made in Milano and can be lain on there. Elsewhere, a showroom, an agent or a reseller will receive you, by appointment.</p>'),
    ('contact', ['contact', 'contact-us', 'contacts', 'contatti'],
     'Contact', '<p>The atelier on Via Andegari 4, Milano, by appointment, Monday to Friday. Write to us, and the person who answers will follow your enquiry from the first message to the day the bed is made up in your room.</p>'),
    ('atelier', ['atelier', 'the-atelier', 'milano-atelier', 'the-milano-atelier', 'showroom', 'visit-the-atelier'],
     'The Atelier', '<p>The atelier is at Via Andegari 4, Milano, by appointment, Monday to Friday, 09:00–12:00 and 13:00–18:00. Come and lie down on the systems, choose the fibres and the cloth against the bed itself, or meet us by video, wherever you are.</p>'),
    ('compare', ['sleep-collections', 'compare-the-collections', 'compare-collections'],
     'Compare the collections', '<p>Essentials, Signature and Icons, side by side. Every system, in every collection, is made by hand in Italy by the same two artisans, from natural fibres only; the collections differ in the cloth, the rarity of the fibres and how far the bespoke goes.</p>'),
    ('facts', ['midsummer-milano-at-a-glance', 'at-a-glance', 'facts', 'key-facts'],
     'Midsummer Milano at a glance', '<p>The essentials about the house, in plain words, for clients, journalists and partners.</p>'),
    # pages the store already has: their template is set, and they are made only if missing
    ('story', ['about-midsummer-milano', 'our-story', 'about-us', 'about', 'chi-siamo'],
     'Our Story', '<p>Midsummer Milano was founded in Milan by an architect, around one question: why is the bed, where we spend a third of our lives, treated as a technical product from a catalogue, when every other piece of a room is designed with care?</p>'),
    ('natural-materials', ['natural-luxury-materials', 'natural-materials', 'materials'],
     'Natural Materials', '<p>Baby alpaca, Cheviot wool, horsehair, vegetable horsehair, yak hair, mohair, cashmere, silk, linen, organic cotton and Orange Fiber: the natural fibres inside every Midsummer bed, and what each one does.</p>'),
    ('regeneration', ['midsummer-milanos-regeneration-service', 'regeneration-service', '15-15-refurbishment', 'regeneration', '15-15'],
     'Made to last · 15 + 15', '<p>At year fifteen the mattress returns to the Italian artisans who made it, and its comfort, integrity and life are restored for the fifteen years ahead, rather than the system being replaced.</p>'),
    ('faq', ['sleep-wise-faq', 'faq', 'questions', 'frequently-asked-questions'],
     'Sleep Wise · Questions', '<p>Direct answers about the beds, ordering, sleep and comfort, care and regeneration.</p>'),
    ('loro-piana-interiors', ['loro-piana-interiors', 'loro-piana'],
     'Loro Piana Interiors', '<p>Midsummer systems are upholstered in Loro Piana Interiors fabrics, chosen from the fabric book against the bed itself at the atelier, or by post, with samples sent ahead of a video consultation.</p>'),
    ('find-your-midsummer', ['find-your-midsummer', 'sleep-assessment', 'sleep-assesment', 'sleep-style-quiz', 'sleep-quiz'],
     'Find your Midsummer', '<p>Five questions about how you sleep suggest a system to try; at the atelier, you choose by lying down.</p>'),
    # set when the store has it, never created
    ('download-the-dream', ['download-dream-art-of-rest', 'download-the-dream', 'the-dream'], None, None),
]

# the description search engines show for a page this script creates (an existing page keeps its own)
DESCRIPTIONS = {
    'professionals': 'Handmade natural-fibre beds specified to your drawing: dimensions, radii, fibres and Loro Piana Interiors fabrics, with no tooling charge.',
    'hospitality': 'Handmade beds for hotels and residences: volume programmes made to the room in Italy, with regeneration in contract at fifteen years.',
    'handmade-in-italy': 'How a Midsummer Milano bed is made: by hand in Italy, by the same two artisans, start to finish, from natural fibres only.',
    'sleep-culture': 'Temperature, support and the seasons: what making natural-fibre beds by hand in Milan has taught us about sleep.',
    'agents-and-resellers': 'Where to see and try Midsummer Milano beds: the Milan atelier, and showrooms, agents and resellers worldwide.',
    'contact': 'Write to the Midsummer Milano atelier, request a proposal or book a private appointment in Milan or by video.',
    'atelier': 'Visit the Midsummer Milano atelier, Via Andegari 4, Milano: lie on the beds and choose fibres and cloth, by appointment.',
    'compare': 'Essentials, Signature and Icons compared: fibres, fabrics and bespoke options of the Midsummer Milano collections.',
    'facts': 'Midsummer Milano at a glance: handmade luxury beds and mattresses from Milan, natural fibres, Loro Piana Interiors, 15 + 15 regeneration.',
    'story': 'The story of Midsummer Milano, a Milan house making luxury beds and mattresses by hand from natural fibres.',
    'natural-materials': 'The natural fibres inside Midsummer Milano beds: alpaca, Cheviot wool, horsehair, yak, mohair, cashmere, silk, linen and more.',
    'regeneration': 'The 15 + 15 service: at fifteen years a Midsummer Milano mattress returns to its artisans and is regenerated for fifteen more.',
    'faq': 'Questions about Midsummer Milano beds: materials, sizes, comfort, ordering, delivery, care and the 15 + 15 regeneration.',
    'loro-piana-interiors': 'Midsummer Milano beds upholstered in Loro Piana Interiors fabrics, chosen from the fabric book against the bed itself.',
    'find-your-midsummer': 'Five questions about how you sleep, and the Midsummer Milano system to try first.',
}


def call(method, path, store, token, body=None):
    req = urllib.request.Request('https://%s/admin/api/%s/%s' % (store, API, path), method=method,
                                 data=json.dumps(body).encode() if body is not None else None,
                                 headers={'X-Shopify-Access-Token': token, 'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode() or '{}')


def main():
    store = os.environ.get('SHOPIFY_STORE', '').replace('https://', '').replace('http://', '').strip('/')
    token = os.environ.get('SHOPIFY_ADMIN_TOKEN', '')
    dry = '--dry-run' in sys.argv
    if not store or not token:
        sys.exit(__doc__)
    try:
        call('GET', 'pages.json?limit=1&fields=id', store, token)
    except urllib.error.HTTPError as e:
        sys.exit('The store refused the token (%s). Check the address and that the app has read_content and write_content.' % e.code)
    except urllib.error.URLError as e:
        sys.exit('Could not reach %s: %s' % (store, e.reason))
    for tpl, handles, title, body in PLACES:
        try:
            page = None
            for h in handles:
                found = call('GET', 'pages.json?handle=%s&fields=id,handle,template_suffix,published_at' % h, store, token).get('pages', [])
                if found:
                    page = found[0]
                    break
            if page:
                if page.get('template_suffix') == tpl:
                    print('ok          %-40s already on page.%s' % (page['handle'], tpl))
                elif dry:
                    print('would set   %-40s page.%s (now: %s)' % (page['handle'], tpl, page.get('template_suffix') or 'default'))
                else:
                    call('PUT', 'pages/%d.json' % page['id'], store, token, {'page': {'id': page['id'], 'template_suffix': tpl}})
                    print('set         %-40s page.%s' % (page['handle'], tpl))
                if not page.get('published_at'):
                    print('            %-40s is hidden: publish it in Online Store → Pages so visitors can open it' % page['handle'])
            elif title is None:
                print('skipped     %-40s the store has no such page' % handles[0])
            elif dry:
                print('would make  %-40s page.%s' % (handles[0], tpl))
            else:
                new = {'title': title, 'handle': handles[0], 'body_html': body, 'template_suffix': tpl, 'published': True}
                if tpl in DESCRIPTIONS:
                    new['metafields_global_description_tag'] = DESCRIPTIONS[tpl]
                made = call('POST', 'pages.json', store, token, {'page': new})['page']
                print('created     %-40s https://%s/pages/%s' % (made['handle'], store, made['handle']))
        except urllib.error.HTTPError as e:
            print('failed      %-40s %s %s' % (handles[0], e.code, e.read().decode()[:300]))


if __name__ == '__main__':
    main()
