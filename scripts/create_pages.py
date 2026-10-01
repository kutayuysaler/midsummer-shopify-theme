#!/usr/bin/env python3
"""Create the four Midsummer Milano pages the theme has designs for.

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
        'body_html': '<p>Midsummer Milano works with architects and interior designers on residences, yachts and hotels: drawings, sections and material schedules for your set, fabric references, and beds made to the measure of the room.</p>',
    },
    {
        'handle': 'hospitality', 'title': 'Hospitality', 'template_suffix': 'hospitality',
        'body_html': '<p>For hotels and residences: volume programmes, made-to-measure systems, and regeneration in contract, so the beds a guest remembers stay the beds they remember.</p>',
    },
    {
        'handle': 'handmade-in-italy', 'title': 'Handmade in Italy', 'template_suffix': 'handmade-in-italy',
        'body_html': '<p>Every Midsummer bed is made in Milano by two artisans, from the springs to the last stitch of the border. They work with natural fibres only, wool, horsehair, cashmere and silk, laid by hand where each does its work.</p><p>Because the same hands make the whole bed, the bed can return to them at fifteen years, be opened, renewed and made ready for fifteen more.</p>',
    },
    {
        'handle': 'sleep-culture', 'title': 'Sleep Culture', 'template_suffix': 'sleep-culture',
        'body_html': '<p>We think about sleep the way an architect thinks about a room: light, temperature, material, and the body at rest within them. Sleep Culture gathers what we have learned making beds by hand, and what our clients have taught us about the nights they want.</p>',
    },
]


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
    for p in PAGES:
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
