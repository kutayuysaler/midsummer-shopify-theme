#!/usr/bin/env python3
"""Create the Midsummer Milano pages the theme has designs for (and a Contact page, if the store has none).

Each page is created with its handle, its text, and the theme template that designs it.
Pages that already exist are left as they are (their template is set if it is missing).

Needs an Admin API token with the write_content scope (Shopify admin → Settings → Apps
and sales channels → Develop apps → Create an app → Admin API scopes: write_content,
read_content → Install → copy the Admin API access token). Then:

    SHOPIFY_STORE=your-store.myshopify.com SHOPIFY_ADMIN_TOKEN=shpat_... python3 scripts/create_pages.py

Python 3 only, no packages to install. Add --dry-run to see what would happen.
"""
import json, os, sys, urllib.request, urllib.error

API = '2025-01'
PAGES = [
    {
        'handle': 'professionals', 'title': 'Architects & Interior Designers', 'template_suffix': 'professionals',
        'body_html': '<p>For architects and interior designers, Midsummer Milano is a material and a method rather than a catalogue. We work from your drawing: dimensions, heights and radii, including fully round beds, with no tooling charge.</p><p>We send drawings, sections and material schedules for your set, fabric references from Loro Piana Interiors, and samples of the natural fibres. One person at the atelier follows the project from specification to installation.</p>',
    },
    {
        'handle': 'hospitality', 'title': 'Hospitality', 'template_suffix': 'hospitality',
        'body_html': '<p>A guest remembers the bed. It is the one piece of furniture they spend eight hours inside.</p><p>For hotels and private residences we make volume programmes to the room, handmade in Milano by the same two artisans for every bed, with handover dates planned with you, and regeneration in contract at fifteen years so the beds your guests remember stay the beds they remember.</p>',
    },
    {
        'handle': 'handmade-in-italy', 'title': 'Handmade in Italy', 'template_suffix': 'handmade-in-italy',
        'body_html': '<p>Every piece is built by hand, from start to finish, by the same two Italian artisans: two or three full days of work for each mattress. It is not a marketing promise; it is a method.</p><p>Because one pair of hands follows the bed through every stage, nothing goes inside it that its makers did not choose and place themselves. And because they know it from the inside, the bed can come back to them at fifteen years to be opened, renewed and made ready for fifteen more.</p>',
    },
    {
        'handle': 'sleep-culture', 'title': 'Sleep Culture', 'template_suffix': 'sleep-culture',
        'body_html': '<p>Midsummer Milano began with a question its founder, an architect, kept asking: why is the bed treated as a technical product from a catalogue, when every other piece of a room is chosen with care?</p><p>Sleep Culture is where we follow that question: how material, temperature, proportion and ritual shape the night, and what making beds by hand, and listening to the people who sleep in them, has taught us.</p>',
    },
]


# the enquiry page lives on the store's Contact page; it is created only if the store has none
CONTACT = {'handle': 'contact', 'title': 'Contact', 'template_suffix': 'contact',
           'body_html': '<p>The atelier on Via Andegari 4, Milano, by appointment, Monday to Friday. Write to us, and the person who answers will follow your enquiry from the first message to the day the bed is made up in your room.</p>'}
CONTACT_HANDLES = ('contact', 'contact-us', 'contacts', 'contatti', 'enquire', 'enquiry')


def call(method, path, store, token, body=None):
    req = urllib.request.Request('https://%s/admin/api/%s/%s' % (store, API, path), method=method,
                                 data=json.dumps(body).encode() if body is not None else None,
                                 headers={'X-Shopify-Access-Token': token, 'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode() or '{}')


def main():
    store = os.environ.get('SHOPIFY_STORE', '').replace('https://', '').strip('/')
    token = os.environ.get('SHOPIFY_ADMIN_TOKEN', '')
    dry = '--dry-run' in sys.argv
    if not store or not token:
        sys.exit(__doc__)
    pages = list(PAGES)
    try:
        if not any(call('GET', 'pages.json?handle=%s&fields=id' % h, store, token).get('pages') for h in CONTACT_HANDLES):
            pages.append(CONTACT)
    except urllib.error.HTTPError as e:
        print('could not look for a contact page:', e.code)
    for p in pages:
        try:
            found = call('GET', 'pages.json?handle=%s&fields=id,handle,template_suffix' % p['handle'], store, token).get('pages', [])
            if found:
                page = found[0]
                if not page.get('template_suffix') and not dry:
                    call('PUT', 'pages/%d.json' % page['id'], store, token, {'page': {'id': page['id'], 'template_suffix': p['template_suffix']}})
                    print('exists, template set:', p['handle'])
                else:
                    print('exists, left as it is:', p['handle'], '(template: %s)' % (page.get('template_suffix') or 'default'))
                continue
            if dry:
                print('would create:', p['handle'], '→ template page.%s' % p['template_suffix'])
                continue
            made = call('POST', 'pages.json', store, token, {'page': dict(p, published=True)})['page']
            print('created:', made['handle'], 'https://%s/pages/%s' % (store, made['handle']))
        except urllib.error.HTTPError as e:
            print('failed:', p['handle'], e.code, e.read().decode()[:300])


if __name__ == '__main__':
    main()
