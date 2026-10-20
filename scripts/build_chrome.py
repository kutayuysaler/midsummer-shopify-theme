"""Header (bar, five panels, phone menu) and footer, from the preview DOM."""
import re, sys
sys.path.insert(0, '/tmp/claude-0/-home-user-atelier-operations-suite/706be317-7628-51f6-9f00-9c341b36daf7/scratchpad/bin')
from conv import *

def soup(path):
    return BeautifulSoup(open(path).read(), 'html.parser')

home = soup(PV + '/p1440/00-home.html')
header = home.find('header')
headrow = header.find(attrs={'data-ms': 'headrow'})

# ── bar ──
for b, key in zip(headrow.find(attrs={'data-ms': 'nav'}).find_all('button'), ['beds', 'heritage', 'pro', 'journal', 'contact']):
    b['data-ms-mega'] = key
    b['aria-expanded'] = 'false'
    b['type'] = 'button'
    b.attrs.pop('data-go', None)
logo_img = headrow.find(attrs={'data-ms': 'logo'}).find('img')
logo_img['style'] = 'display: block; height: clamp(19px, 1.75vw, 28px); width: auto;'
logo_img['data-ms-logo'] = ''
menubtn = headrow.find(attrs={'data-ms': 'menubtn'})
menubtn.attrs.pop('data-go', None)
menubtn['data-ms-menu-open'] = ''
menubtn['type'] = 'button'
menubtn['aria-expanded'] = 'false'

# ── panels ──
panels = []
for key in ['beds', 'heritage', 'pro', 'journal', 'contact']:
    s = soup(f'{PV}/p1440/mega-{key}.html')
    p = s.find('header').find_all(recursive=False)[1]
    p['data-ms-panel'] = key
    p['hidden'] = ''
    st = p.get('style', '')
    p['style'] = re.sub(r'animation:[^;]*;?', '', st).strip()
    panels.append(p)

# ── phone menu ──
menu = soup(PV + '/p390/menu.html').find(attrs={'role': 'dialog'})
menu['data-ms-menu'] = ''
menu['hidden'] = ''
close = menu.find('button', attrs={'aria-label': 'Close menu'})
close.attrs.pop('data-go', None); close['data-ms-menu-close'] = ''; close['type'] = 'button'
mbody = menu.find(attrs={'data-ms': 'mbody'})
root = BeautifulSoup('<div data-ms-mroot=""></div>', 'html.parser').div
for c in list(mbody.children):
    root.append(c.extract())
mbody.append(root)
for b, key in zip(root.find('nav').find_all('button'), ['beds', 'heritage', 'pro', 'journal', 'contact']):
    b.attrs.pop('data-go', None)
    if key == 'journal':
        b.name = 'a'
        b['data-go'] = 'journal'
        b['style'] = b['style']
    else:
        b['data-ms-msub-open'] = key
        b['type'] = 'button'
topbar = menu.find_all(recursive=False)[0]
topbar_logo = topbar.find('a')
topbar_logo['data-ms-mroot-only'] = ''
back = BeautifulSoup('<button type="button" data-ms-msub-back="" hidden style="display: flex; align-items: center; gap: 12px; min-height: 44px; background: none; border: 0px; padding: 0px; cursor: pointer; color: inherit; font-size: 11px; letter-spacing: 0.26em; text-transform: uppercase;"><svg viewBox="0 0 16 16" width="14" height="14" aria-hidden="true" style="display: block;"><path d="M10 3 5 8l5 5" fill="none" stroke="currentColor" stroke-width="1.1"></path></svg>Menu</button>', 'html.parser').button
topbar_logo.insert_after(back)

M_NAV = {
    'beds': ('01', 'Our Beds', 'Twenty-four systems in three collections, each one built to order.', [
        ('Essentials', 'Five systems', 'collection:essentials', 'ms-graded-bougainvillea.jpg'),
        ('Signature', 'Seven systems', 'collection:signature', 'ms-graded-ochre-room.jpg'),
        ('Icons', 'Twelve systems', 'collection:icons', 'ms-graded-arches.jpg'),
        ('Compare the collections', 'The three side by side', 'collections', None),
        ('Find your Midsummer', 'Five questions to your bed', 'quiz', None)]),
    'heritage': ('02', 'Heritage & Craft', 'How a Midsummer bed is made, and what it is made of.', [
        ('Our story', 'A house of beds in Milan', 'story', None),
        ('Handmade in Italy', 'Two artisans, one bed', 'handmade', None),
        ('Sleep culture', 'The art of sleeping well', 'sleep-culture', None),
        ('Natural materials', 'Wool, horsehair, silk and linen', 'materials', None),
        ('Loro Piana Interiors', 'The fabrics we upholster in', 'loro', None),
        ('Made to last · 15 + 15', 'Regenerated at fifteen years', 'regen', None)]),
    'pro': ('03', 'Professionals', 'For architects, interior designers, hotels and residences.', [
        ('Architects & Interior Designers', 'Specification support', 'architects', None),
        ('Hospitality & Contract', 'Hotels and residences', 'hospitality', None),
        ('Become a partner', 'Represent Midsummer', 'partner', None)]),
    'contact': ('05', 'Contact', 'Visit the atelier on Via Andegari, or write to us.', [
        ('Book an appointment', 'At the atelier or by video call', 'drawer', None),
        ('Agents & Resellers', 'Showrooms worldwide, on the map', 'agents', None),
        ('Questions & customer care', 'Answers before you ask', 'faq', None)]),
}
MEGA_SETTINGS = [{'type': 'header', 'content': 'Menu panels'}] + [
    {'type': t, 'id': i, 'label': l, **({'default': d} if d is not None else {})} for (t, i, l, d) in [
    ('text', 'mg_address', 'Address', 'Via Andegari 4, 20121 Milano'),
    ('text', 'mg_hours', 'Hours', 'By appointment, Monday to Friday'),
    ('text', 'mg_book', 'Appointment link', 'Book an appointment'),
    ('textarea', 'mg_beds_lede', 'Our beds: line', 'Twenty-four systems in three collections, each built to order by two artisans in Milan.'),
    ('text', 'mg_compare', 'Our beds: compare', 'Compare the collections'),
    ('text', 'mg_quiz', 'Our beds: quiz', 'Find your Midsummer'),
    ('text', 'mg_proposal', 'Our beds: proposal', 'Request a proposal'),
    ('image_picker', 'mg_img_essentials', 'Essentials photograph', None),
    ('text', 'mg_essentials', 'Essentials line', 'The entry into the Midsummer world: natural fibres, artisan construction, clean lines.'),
    ('image_picker', 'mg_img_signature', 'Signature photograph', None),
    ('text', 'mg_signature', 'Signature line', 'Loro Piana Interiors fabrics over spring architectures designed for the highest comfort.'),
    ('image_picker', 'mg_img_icons', 'Icons photograph', None),
    ('text', 'mg_icons', 'Icons line', 'The most important pieces we make. Completely bespoke, with no equivalent.'),
    ('textarea', 'mg_heritage_lede', 'Heritage: line', 'How a Midsummer bed is made, what it is made of, and why it lasts thirty years.'),
    ('image_picker', 'mg_img_heritage', 'Heritage photograph (first)', None),
    ('text', 'mg_h1', 'Heritage 1', 'Our story'), ('text', 'mg_h1_note', 'Heritage 1 line', 'A house of beds in Milan'),
    ('text', 'mg_h2', 'Heritage 2', 'Handmade in Italy'), ('text', 'mg_h2_note', 'Heritage 2 line', 'Two artisans, one bed'),
    ('text', 'mg_h3', 'Heritage 3', 'Sleep culture'), ('text', 'mg_h3_note', 'Heritage 3 line', 'The art of sleeping well'),
    ('text', 'mg_h4', 'Heritage 4', 'Natural materials'), ('text', 'mg_h4_note', 'Heritage 4 line', 'Wool, horsehair, silk, cashmere'),
    ('text', 'mg_h5', 'Heritage 5', 'Loro Piana Interiors'), ('text', 'mg_h5_note', 'Heritage 5 line', 'The fabrics we upholster in'),
    ('text', 'mg_h6', 'Heritage 6', 'Made to last · 15 + 15'), ('text', 'mg_h6_note', 'Heritage 6 line', 'Regenerated at fifteen years'),
    ('textarea', 'mg_pro_lede', 'Professionals: line', 'For architects, interior designers, hotels and residences: drawings, samples and a single contact from brief to installation.'),
    ('image_picker', 'mg_img_pro', 'Professionals photograph (first)', None),
    ('text', 'mg_p1', 'Professionals 1', 'Architects & Interior Designers'), ('text', 'mg_p1_note', 'Professionals 1 line', 'Specification support'),
    ('text', 'mg_p2', 'Professionals 2', 'Hospitality & Contract'), ('text', 'mg_p2_note', 'Professionals 2 line', 'Hotels and residences'),
    ('text', 'mg_p3', 'Professionals 3', 'Portfolio'), ('text', 'mg_p3_note', 'Professionals 3 line', 'Houses, hotels and yachts'),
    ('text', 'mg_p4', 'Professionals 4', 'Become a partner'), ('text', 'mg_p4_note', 'Professionals 4 line', 'Represent Midsummer'),
    ('text', 'mg_p5', 'Professionals 5', 'Trade enquiry'), ('text', 'mg_p5_note', 'Professionals 5 line', 'Samples, drawings, pricing'),
    ('text', 'mg_pro_cta1', 'Professionals: button', 'Agents & Resellers'),
    ('text', 'mg_contact_cta1', 'Contact: button', 'Enquire'),
    ('text', 'mg_contact_cta2', 'Contact: link', 'Agents & Resellers'),
    ('textarea', 'mg_journal_lede', 'Journal: line', 'Notes from the atelier on sleep, natural fibres and the houses our beds go to.'),
    ('text', 'mg_all_notes', 'Journal: all notes', 'All notes'),
    ('text', 'mg_press', 'Journal: press', 'Press'),
    ('text', 'mg_collab', 'Journal: collaborations', 'Collaborations'),
    ('text', 'mg_note_label', 'Journal: note label', 'From the Journal'),
    ('textarea', 'mg_contact_lede', 'Contact: line', 'Come and lie down at the atelier in Milan, or speak to us by video. One person answers every enquiry.'),
    ('text', 'mg_c1', 'Contact 1', 'Book an appointment'), ('text', 'mg_c1_note', 'Contact 1 line', 'At the atelier or by video'),
    ('text', 'mg_c2', 'Contact 2', 'Agents & Resellers'), ('text', 'mg_c2_note', 'Contact 2 line', 'Showrooms worldwide, on the map'),
    ('text', 'mg_c3', 'Contact 3', 'Direct contact'), ('text', 'mg_c3_note', 'Contact 3 line', 'Telephone and email'),
    ('text', 'mg_c4_note', 'WhatsApp line', 'Write to the atelier'),
    ('text', 'mg_c5', 'Contact 5', 'The Milano atelier'), ('text', 'mg_c5_note', 'Contact 5 line', 'Via Andegari 4'),
    ('text', 'mg_c6', 'Contact 6', 'Questions & customer care'), ('text', 'mg_c6_note', 'Contact 6 line', 'Answers before you ask'),
]]
ARROW = '<svg viewBox="0 0 16 16" width="14" height="14" aria-hidden="true" style="display: block; justify-self: end;"><path d="M6 3l5 5-5 5" fill="none" stroke="currentColor" stroke-width="1.1"></path></svg>'
for key, (n, label, intro, items) in M_NAV.items():
    h = [f'<div data-ms-msub="{key}" hidden><div style="padding: 22px 0px 20px;">'
         f'<div style="font-size: 11px; letter-spacing: 0.26em; text-transform: uppercase; color: rgb(126, 98, 59);">{n}</div>'
         f'<div style="font-family: Newsreader, Georgia, serif; font-size: 38px; line-height: 1.05; letter-spacing: -0.025em; font-weight: 200; margin-top: 10px;">{label.replace("&", "&amp;")}</div>'
         f'<p style="font-size: 13.5px; line-height: 1.7; color: rgb(74, 68, 59); margin-top: 12px; max-width: 34ch;">{intro}</p></div>']
    for (il, note, go, img) in items:
        cols = '64px minmax(0px, 1fr) 16px' if img else 'minmax(0px, 1fr) 16px'
        im = f'<img src="@asset:{img}" alt="" style="display: block; width: 64px; aspect-ratio: 4 / 5; object-fit: cover;">' if img else ''
        h.append(f'<a href="#" data-go="{go}" style="display: grid; grid-template-columns: {cols}; gap: 16px; align-items: center; min-height: 64px; padding: 12px 0px; border-top: 1px solid rgb(221, 214, 201); color: rgb(23, 20, 15);">{im}'
                 f'<span style="display: flex; flex-direction: column; gap: 4px; min-width: 0px;"><span style="font-family: Newsreader, Georgia, serif; font-size: 22px; line-height: 1.2;">{il.replace("&", "&amp;")}</span>'
                 f'<span style="font-size: 12.5px; line-height: 1.5; color: rgb(110, 103, 92);">{note}</span></span>{ARROW}</a>')
    h.append('</div>')
    mbody.append(BeautifulSoup(''.join(h), 'html.parser'))

# assemble
bar = BeautifulSoup('<header data-ms-header=""></header>', 'html.parser').header
bar.append(headrow)
# the five panels are drawn by snippets/ms-mega.liquid (and ms-mega-panel)
bar.append(BeautifulSoup('<div data-ms-mega-panels=""></div>', 'html.parser').div)
wrap = BeautifulSoup('<div data-ms-headerroot=""></div>', 'html.parser').div
wrap.append(bar)
wrap.append(menu)

c = Conv()
c.walk(wrap)
out = c.render(wrap)
out = re.sub(r'src="@asset:([^"]+)"', lambda m: 'src="{{ \'%s\' | asset_url }}"' % m.group(1), out)
# every menu title leads to its own place (bin/links.py)
import links
out = links.contact_social(links.phone_enquiry(links.enquiry_card(links.card_labels(links.latest_article(links.relink(out, keep_enquire=('t6 }}',)))))))
out = re.sub(r'<div data-ms-mega-panels="">\s*</div>', "{% render 'ms-mega', ss: section.settings %}", out)
assert "render 'ms-mega'" in out
c.settings += MEGA_SETTINGS
# the phone menu's links say where they go
for st in c.settings:
    if st.get('default') == 'Store locator':
        st['default'] = st['label'] = 'Agents & Resellers'
    if st.get('default') == 'Visit the atelier':
        st['default'] = st['label'] = 'The Milano atelier'
        pat = re.compile(r'<a data-ms-enquire="" href="\{% render \'ms-link\', to: \'contact\' %\}"([^>]*>\{\{ section\.settings\.' + st['id'] + r' \}\})')
        out = pat.sub(lambda m: '<a href="{%% render \'ms-link\', to: \'atelier\' %%}"'.replace('%%', '%') + m.group(1), out)
# the agents' map one click away, beside the appointment button (the enquiry page too, when named)
HEAD_LINKS = ('<a class="ms-hlink" href="{% render \'ms-link\', to: \'agents\' %}">{{ section.settings.hl_agents }}</a>'
              '{% if section.settings.hl_enquire != blank %}<a class="ms-hlink" href="{% render \'ms-link\', to: \'enquire\' %}#enquire" data-ms-landing>{{ section.settings.hl_enquire }}</a>{% endif %}')
out = out.replace('<div data-ms="headaction" style="display: flex; align-items: center; flex: 0 0 auto; order: 3; gap: clamp(14px, 2vw, 28px);">\n',
                  '<div data-ms="headaction" style="display: flex; align-items: center; flex: 0 0 auto; order: 3; gap: clamp(14px, 2vw, 28px);">\n' + HEAD_LINKS + '\n', 1)
assert 'ms-hlink' in out
c.settings += [{'type': 'text', 'id': 'hl_agents', 'label': 'Header link: agents map', 'default': 'Showrooms'},
               {'type': 'text', 'id': 'hl_enquire', 'label': 'Header link: enquiry page (optional)', 'info': 'Empty: no link, as the appointment button already opens the enquiry (Round 29).'}]
# the logo: an uploaded file overrides the preview's logotype everywhere it appears
open(THEME + '/sections/ms-header.liquid', 'w').write(out + '\n' + schema('MS · Header', c.settings, {'tag': 'div', 'class': 'ms-header-section'}))
print('header settings', len(c.settings))

# ── footer ──
footer = home.find('footer')
footer['data-ms-footer'] = ''
c = Conv()
c.walk(footer)
open(THEME + '/sections/ms-footer.liquid', 'w').write(links.footer_social(links.relink(c.render(footer))) + '\n' + schema('MS · Footer', c.settings, {'tag': 'div'}))
print('footer settings', len(c.settings))
copy_assets()
print(USED_ASSETS.keys())
