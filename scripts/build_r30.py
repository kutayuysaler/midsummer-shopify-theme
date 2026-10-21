# Round 30, run at the end of bin/build_more.py in its scope (THEME, SP), after Round 29. Every step is
# an exact replacement or a guarded write, so a second build changes nothing.
#  · The site's designer and developer, Kutay Uysaler, credited where search engines and AI crawlers read
#    a site's metadata, never in the page itself: the WebSite record of the structured data (its creator),
#    a designer meta tag and a comment in the head of every page, and the theme's author in the admin

_r30_n = 0


def _r30_sub(path, pairs):
    """an exact replacement; one that holds what it replaces is made once"""
    global _r30_n
    _t = open(path, encoding='utf-8').read()
    _u = _t
    for _a, _b in pairs:
        if _a in _b and _b in _u:
            continue
        if _a in _u:
            _u = _u.replace(_a, _b)
        else:
            assert _b in _u, (path, _a[:80])
    if _u != _t:
        open(path, 'w', encoding='utf-8').write(_u)
        _r30_n += 1


_CREDIT = '    <!-- Designed and developed by Kutay Uysaler -->\n    <meta name="designer" content="Kutay Uysaler">\n'
_r30_sub(THEME + '/layout/ms.liquid', [('<html lang="{{ request.locale.iso_code }}">\n  <head>\n', '<html lang="{{ request.locale.iso_code }}">\n  <head>\n' + _CREDIT)])
_r30_sub(THEME + '/layout/theme.liquid', [('  lang="{{ request.locale.iso_code }}"\n>\n  <head>\n', '  lang="{{ request.locale.iso_code }}"\n>\n  <head>\n' + _CREDIT)])
_r30_sub(THEME + '/sections/ms-seo.liquid', [
    ('      "publisher": { "@id": "{{ shop.url }}/#organization" },\n      "potentialAction": {',
     '      "publisher": { "@id": "{{ shop.url }}/#organization" },\n'
     '      "creator": { "@type": "Person", "name": "Kutay Uysaler", "jobTitle": "Website designer and developer" },\n'
     '      "potentialAction": {'),
])
_r30_sub(THEME + '/config/settings_schema.json', [('    "theme_author": "Shopify",', '    "theme_author": "Kutay Uysaler",')])
for _f, _w in (('/layout/ms.liquid', 'Designed and developed by Kutay Uysaler'), ('/layout/theme.liquid', 'Designed and developed by Kutay Uysaler'),
               ('/sections/ms-seo.liquid', '"name": "Kutay Uysaler"'), ('/config/settings_schema.json', '"theme_author": "Kutay Uysaler"')):
    assert open(THEME + _f, encoding='utf-8').read().count(_w) == 1, ('credit', _f)

print('round 30: %d files changed' % _r30_n)
