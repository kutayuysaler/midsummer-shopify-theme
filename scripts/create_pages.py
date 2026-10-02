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
    # pages the store already has: only their template is set, they are never created
    ('story', ['about-midsummer-milano', 'our-story', 'about-us', 'about', 'chi-siamo'], None, None),
    ('natural-materials', ['natural-luxury-materials', 'natural-materials', 'materials'], None, None),
    ('regeneration', ['midsummer-milanos-regeneration-service', 'regeneration-service', '15-15-refurbishment', 'regeneration', '15-15'], None, None),
    ('faq', ['sleep-wise-faq', 'faq', 'questions', 'frequently-asked-questions'], None, None),
    ('download-the-dream', ['download-dream-art-of-rest', 'download-the-dream', 'the-dream'], None, None),
    ('loro-piana-interiors', ['loro-piana-interiors', 'loro-piana'], None, None),
    ('find-your-midsummer', ['find-your-midsummer', 'sleep-assessment', 'sleep-assesment', 'sleep-style-quiz', 'sleep-quiz'], None, None),
]


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
                print('skipped     %-40s the store has no such page; the theme shows its design anyway' % handles[0])
            elif dry:
                print('would make  %-40s page.%s' % (handles[0], tpl))
            else:
                made = call('POST', 'pages.json', store, token, {'page': {'title': title, 'handle': handles[0], 'body_html': body,
                                                                         'template_suffix': tpl, 'published': True}})['page']
                print('created     %-40s https://%s/pages/%s' % (made['handle'], store, made['handle']))
        except urllib.error.HTTPError as e:
            print('failed      %-40s %s %s' % (handles[0], e.code, e.read().decode()[:300]))


if __name__ == '__main__':
    main()
