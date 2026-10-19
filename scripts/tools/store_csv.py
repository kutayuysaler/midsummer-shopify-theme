"""The store's own words in Italian and Russian, as a file for Translate & Adapt → Import.
Reads the store's export (tr/export/*.csv) and the translations written for it (r24/csv/s*.txt, the
same @id / Italian / Russian blocks as bin/tr/src), and writes only the rows it fills or corrects:
  - what was left untranslated (titles, SEO titles and descriptions, collections, the FAQ entries,
    option values, image descriptions, press blogs, the founder's letter);
  - product names, which stay as they are in every language (the Russian machine translations
    turned Dreamy Springs into «Мечтательные источники»);
  - the articles' addresses, from their translated titles (Italian words; Russian transliterated);
  - the articles' image descriptions, which repeat the article's title.
Left alone on purpose: product, page, collection and blog handles (the theme recognises places by
them), long texts already translated but marked outdated (Shopify keeps showing them), app data
and old metafields, the policies, and the Glossary page (it describes construction the house does
not disclose; see INSTALL.md).
usage: python3 tools/store_csv.py → r24/csv/Midsummer-Milano_translations_import.csv"""
import csv, glob, hashlib, os, re, sys, unicodedata, collections
SP = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = sorted(glob.glob(os.path.join(SP, 'tr', 'export', '*.csv')))[-1]
OUT = os.path.join(SP, 'r24', 'csv', 'Midsummer-Milano_translations_import.csv')
rows = list(csv.DictReader(open(SRC, encoding='utf-8-sig')))
COLS = list(rows[0].keys())

tr = {}
for f in sorted(glob.glob(os.path.join(SP, 'r24', 'csv', 's*.txt'))):
    lines = open(f, encoding='utf-8').read().split('\n')
    i = 0
    while i < len(lines):
        m = re.match(r'@([0-9a-f]{7})\s*$', lines[i])
        if m:
            assert m.group(1) not in tr, m.group(1)
            tr[m.group(1)] = (lines[i + 1], lines[i + 2])
            i += 3
        else:
            i += 1

# product names stay as they are; a few titles are words, not names
NAMES_KEEP = {'langify_image_container'}
WORDS = {
    'Blankets and throws': ('Coperte e plaid', 'Пледы и покрывала'),
    'Bed linen': ('Biancheria da letto', 'Постельное бельё'),
    'Bella Rest Chair': ('Poltrona Bella Rest', 'Кресло Bella Rest'),
    'Herons Panel': ('Pannello Aironi', 'Панно «Цапли»'),
    'Peacocks and Herons Panel': ('Pannello Pavoni e aironi', 'Панно «Павлины и цапли»'),
    'Green Cordonetto Bed Set': ('Completo letto Cordonetto verde', 'Комплект постельного белья Cordonetto, зелёный'),
    'Red Cordonetto Bed Set': ('Completo letto Cordonetto rosso', 'Комплект постельного белья Cordonetto, красный'),
    'Cavalieri Blanket - White': ('Coperta Cavalieri - Bianca', 'Плед Cavalieri — белый'),
    'Cavalieri Blanket - Grey': ('Coperta Cavalieri - Grigia', 'Плед Cavalieri — серый'),
    'Fiori Chiari Blanket': ('Coperta Fiori Chiari', 'Плед Fiori Chiari'),
    'Michela Nicoli collection': ('Collezione Michela Nicoli', 'Коллекция Michela Nicoli'),
    'Cashmere and Alpaca Duvet': ('Piumino in cashmere e alpaca', 'Одеяло из кашемира и альпаки'),
    'Capri Mohair Plaid': ('Plaid Capri in mohair', 'Плед Capri из мохера'),
    'Pure Plaid': ('Plaid Pure', 'Плед Pure'),
    'Pure Blanket': ('Coperta Pure', 'Одеяло Pure'),
    'Roma Mohair Plaid': ('Plaid Roma in mohair', 'Плед Roma из мохера'),
    'Test product': ('Prodotto di prova', 'Тестовый товар'),
    'White and Gray Incontri Bed Set': ('Completo letto Incontri bianco e grigio', 'Комплект постельного белья Incontri, бело-серый'),
    'Book a Showroom Visit': ('Prenota una visita allo showroom', 'Записаться на визит в шоурум'),
}
PANELS_RU_OK = re.compile(r'^Панно «')  # the art panels' existing Russian titles are kept

RU_LAT = dict(zip('абвгдеёжзийклмнопрстуфхцчшщъыьэюя',
                  ['a', 'b', 'v', 'g', 'd', 'e', 'e', 'zh', 'z', 'i', 'y', 'k', 'l', 'm', 'n', 'o', 'p', 'r', 's', 't', 'u', 'f',
                   'kh', 'ts', 'ch', 'sh', 'shch', '', 'y', '', 'e', 'yu', 'ya']))


def slug(s, ru=False):
    s = re.sub(r'<[^>]+>', ' ', s).lower()
    if ru:
        s = ''.join(RU_LAT.get(ch, ch) for ch in s)
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode()
    s = re.sub(r"['’`]", '-', s)
    s = re.sub(r'[^a-z0-9]+', '-', s).strip('-')
    s = re.sub(r'-{2,}', '-', s)
    if len(s) > 90:
        s = s[:90].rsplit('-', 1)[0]
    return s


key = lambda r: (r['Type'], r['Identification'], r['Field'], r['Locale'])
by = {key(r): r for r in rows}
out = collections.OrderedDict()


def put(r, value, why):
    if value is None or value == r['Translated content']:
        return
    o = dict(r)
    o['Translated content'] = value
    o['Status'] = ''
    out[key(r)] = (o, why)


def unit(text):
    return hashlib.md5(text.encode()).hexdigest()[:7]


def value_for(r):
    t = tr.get(unit(r['Default content']))
    if not t:
        return None
    v = t[0 if r['Locale'] == 'it' else 1]
    v = r['Default content'] if v.strip() == '=' else v.replace('\\n', '\n')
    return v


# 1. product names
for r in rows:
    if r['Type'] == 'PRODUCT' and r['Field'] == 'title' and r['Locale'] in ('it', 'ru'):
        en = r['Default content']
        if en in NAMES_KEEP:
            continue
        if en in WORDS:
            v = WORDS[en][0 if r['Locale'] == 'it' else 1]
        elif en.startswith(('“', '"')) and 'Panel' in en and r['Translated content'].strip() and (r['Locale'] == 'it' or PANELS_RU_OK.match(r['Translated content'])):
            continue  # the art panels: their translated titles name the work, and stay
        elif en.startswith(('“', '"')) and 'Panel' in en:
            v = r['Translated content'].replace('Панель', 'Панно') or None
        else:
            v = en  # a name
        put(r, v, 'product name')

# 2. what was left untranslated, or is short and outdated; and the descriptions that named how a
#    bed is built (springs, layers), replaced whatever their translation was
FORCE = {'1504677', '34657da', 'c252a1c', 'b4543ea', '7a06dc4', '423425b', '52a193d', '3040c20', 'b3a4f22', '8a42b9c',
         'b44883e', '7681c80', '7869216'}
SKIP_T ={'ONLINE_STORE_THEME', 'PACKING_SLIP_TEMPLATE', 'SHOP_POLICY', 'METAFIELD', 'DELIVERY_METHOD_DEFINITION', 'FILTER'}
for r in rows:
    if r['Type'] in SKIP_T or r['Field'] == 'handle' or r['Locale'] not in ('it', 'ru'):
        continue
    if r['Type'] == 'PRODUCT' and r['Field'] == 'title':
        continue
    if not r['Default content'].strip():
        continue
    if r['Translated content'].strip() and not (r['Status'] == 'outdated' and len(r['Default content']) < 400) \
            and unit(r['Default content']) not in FORCE:
        continue
    v = value_for(r)
    if v is not None:
        put(r, v, 'translated')

# 2b. names the machine translations translated: magazines keep their names, and Midsummer is the
#     house, not the season («Mezza estate», «Середина лета»). By the English text; None keeps what is there.
TITLE_FIX = {
    'A Liberty Villa on Lake Como': (None, 'Вилла в стиле либерти на озере Комо'),
    'Fashion - The Design Issue': ('Fashion - Il numero dedicato al design', 'Fashion — номер о дизайне'),
    'Real Estate': ('Real Estate', 'Real Estate'),
    'Elle Decor Middle East': ('Elle Decor Middle East', 'Elle Decor Middle East'),
    'Home': ('Home', 'Home'),
    'Crisalide Press - Design Special': ('Crisalide Press - Design Special', 'Crisalide Press — Design Special'),
    'You Trade': ('You Trade', 'You Trade'),
    'Hospitality Design USA': ('Hospitality Design USA', 'Hospitality Design USA'),
    'Bella': (None, 'Bella'),
    'Lust & Leben': ('Lust & Leben', 'Lust & Leben'),
    'Gaaf goed': ('Gaaf goed', 'Gaaf goed'),
    'Glam Deko': ('Glam Deko', 'Glam Deko'),
    'Marie Claire Maison': (None, 'Marie Claire Maison'),
    'Plaza Koti': ('Plaza Koti', 'Plaza Koti'),
    'Robb Report': ('Robb Report', 'Robb Report'),
    'Midsummer-Milano at Fuori Salone 2018. Join us.': (None, 'Midsummer-Milano на Fuori Salone 2018. Присоединяйтесь к нам.'),
    'Crafting the Best Possible Boxspring': (None, 'Как создать лучший бокс-спринг'),
    'ARCHITECTURAL DIGEST': ('ARCHITECTURAL DIGEST', 'ARCHITECTURAL DIGEST'),
    'NHTEPPEPHBIN': ('ИНТЕРЬЕРНЫЙ', 'ИНТЕРЬЕРНЫЙ'),
    'KOMMERSANT STYLE INTERIORS': ('KOMMERSANT STYLE INTERIORS', 'KOMMERSANT STYLE INTERIORS'),
    'Our Ultra Dry Mattress': (None, 'Наш матрас Ultra Dry'),
    'Elle Decor': (None, 'Elle Decor'),
    'Architectural Digest N.4': (None, 'Architectural Digest №4'),
    'Architectural Digest N.3': (None, 'Architectural Digest №3'),
    'Architectural Digest - October': (None, 'Architectural Digest — октябрь'),
    'RBC Style - October': ('RBC Style - Ottobre', 'РБК Стиль — октябрь'),
    'Michela Nicoli collection': (None, 'Коллекция Michela Nicoli'),
    'Oh Jeanne': ('Oh Jeanne', 'Oh Jeanne'),
    'The Beauty Sleep': (None, 'Сон для красоты'),
    'Midwinter or Midsummer': (None, 'Середина зимы или Midsummer'),
    'Sleep Resurrection': (None, 'Воскрешение сна'),
    'Architectural Design N.5': ('Architectural Design N.5', 'Architectural Design №5'),
    'Interior Design': ('Interior Design', 'Interior Design'),
    'Salon Interior': ('Salon Interior', 'Salon Interior'),
    'Midsummer Milano - The Symbol': ('Midsummer Milano - The Symbol', 'Midsummer Milano — The Symbol'),
    'Midsummer: sustainable models for sleeping and relaxing': ('Midsummer: modelli sostenibili per dormire e rilassarsi', 'Midsummer: экологичные модели для сна и отдыха'),
    'Midsummer: our day': ('Midsummer: il nostro giorno', 'Midsummer: наш день'),
    'Midsummer on vacation': ('Midsummer in vacanza', 'Midsummer в отпуске'),
    'Do you need a boxspring?': (None, 'Нужен ли вам бокс-спринг?'),
    "The Power Nap: What Is, What Isn't": (None, 'Короткий дневной сон: что это и чем он не является'),
    'MIDSUMMER-MILANO: Tangram collezione per esterni': ('MIDSUMMER-MILANO: Tangram, collezione per esterni', 'MIDSUMMER-MILANO: Tangram, коллекция для улицы'),
    'Midsummer-Milano on vacation': ('Midsummer-Milano in vacanza', 'Midsummer-Milano на каникулах'),
    'Vanity Fair: Tangram di Midsummer-Milano': ('Vanity Fair: Tangram di Midsummer-Milano', 'Vanity Fair: Tangram от Midsummer-Milano'),
    'Midsummer-Milano for Il Sole 24 Ore': (None, 'Midsummer-Milano для Il Sole 24 Ore'),
    "Festival dell'Etica: Honorable Mention": (None, 'Festival dell’Etica: почётное упоминание'),
    'Monteverdi: Sleeping Vegan, Doing Good': (None, 'Monteverdi: спать по-вегански, делать добро'),
    'A Scented Collaboration: Strega del Castello for Midsummer': (None, 'Ароматное сотрудничество: Strega del Castello для Midsummer'),
    'Midsummer Treasures': (None, 'Сокровища Midsummer'),
    'Under the Shade of Masters – midsummer-milano': (None, 'Под сенью мастеров – midsummer-milano'),
    'Midsummer Milano in Il Sole 24 Ore: Elegance of Good Sleep': ('Midsummer Milano su Il Sole 24 Ore: l’eleganza del buon sonno', None),
}
old_titles = {'it': {}, 'ru': {}}
for r in rows:
    if r['Field'] in ('title', 'meta_title') and r['Type'] in ('ARTICLE', 'COLLECTION') and r['Locale'] in ('it', 'ru'):
        fx = TITLE_FIX.get(r['Default content'])
        if fx and fx[0 if r['Locale'] == 'it' else 1] is not None:
            v = fx[0 if r['Locale'] == 'it' else 1]
            if r['Translated content'].strip() and r['Translated content'].strip() != v:
                old_titles[r['Locale']][r['Translated content'].strip()] = v
            put(r, v, 'name restored')
BODY_FIX = {
    'ru': [(r'[Сс]ередина лета\s*[-–—,]\s*[Мм]илан[оа]?\b', 'Midsummer-Milano'), (r'[Мм]идс[ао]м+[ае]р\s*[-–—]\s*[Мм]илан[оа]?', 'Midsummer-Milano'),
           (r'[Мм]идс[ао]м+[ае]р', 'Midsummer'), (r'«[Сс]ередина лета»', '«Midsummer»'),
           (r'(alt="[^"]*?)\s[-–—]\s[Сс]ередина лета"', r'\1 - Midsummer"'), (r'(alt|title)="[Сс]ередина лета"', r'\1="Midsummer"'),
           (r'Spotify [Сс]ередина лета', 'Spotify Midsummer')],
    'it': [(r'[Mm]ezza [Ee]state\s*[-–—]\s*[Mm]ilano', 'Midsummer-Milano'), (r'MILANO DI MEZZA ESTATE', 'MIDSUMMER-MILANO'),
           (r'Milano di mezza estate', 'Midsummer Milano'), (r'mezza estate-milano', 'midsummer-milano'),
           (r'(alt="[^"]*?)\s[-–—]\s[Mm]ezza estate"', r'\1 - Midsummer"'), (r'Spotify Mezza estate', 'Spotify Midsummer'),
           (r'(letti|letto|materassi) di [Mm]ezza [Ee]state', r'\1 Midsummer'), (r"Battito d'Ali", 'Beating of Wings'),
           (r'(Artigianato|filosofia) di mezza estate', r'\1 Midsummer')],
}
for r in rows:
    if r['Type'] in ('ARTICLE', 'PAGE', 'PRODUCT', 'COLLECTION') and r['Field'] in ('body_html', 'summary_html') and r['Locale'] in ('it', 'ru'):
        k = key(r)
        v0 = out[k][0]['Translated content'] if k in out else r['Translated content']
        if not v0.strip():
            continue
        v = v0
        for a_, b_ in BODY_FIX[r['Locale']]:
            v = re.sub(a_, b_, v)
        for a_, b_ in sorted(old_titles[r['Locale']].items(), key=lambda kv: -len(kv[0])):
            if len(a_) > 6:
                v = v.replace('>' + a_ + '<', '>' + b_ + '<').replace('> ' + a_ + '<', '> ' + b_ + '<')
        if v != v0:
            put(r, v, 'name restored in the text')

# 3. the articles' titles in each language (what the store has, with what this file adds)
title = {}
for r in rows:
    if r['Type'] == 'ARTICLE' and r['Field'] == 'title' and r['Locale'] in ('it', 'ru'):
        k = key(r)
        v = out[k][0]['Translated content'] if k in out else r['Translated content']
        title[(r['Identification'], r['Locale'])] = v.strip() or r['Default content']
en_title = {r['Identification']: r['Default content'] for r in rows if r['Type'] == 'ARTICLE' and r['Field'] == 'title' and r['Locale'] == 'it'}

# 4. article addresses from their titles; never the same as another article's
for loc in ('it', 'ru'):
    taken = {r['Default content'] for r in rows if r['Type'] == 'ARTICLE' and r['Field'] == 'handle' and r['Locale'] == loc}
    taken |= {r['Translated content'] for r in rows if r['Type'] == 'ARTICLE' and r['Field'] == 'handle' and r['Locale'] == loc and r['Translated content'].strip()}
    for r in rows:
        if r['Type'] != 'ARTICLE' or r['Field'] != 'handle' or r['Locale'] != loc or r['Translated content'].strip():
            continue
        t = title.get((r['Identification'], loc), '')
        s = slug(t, ru=(loc == 'ru'))
        if not s or s == r['Default content'] or s == slug(en_title.get(r['Identification'], '')):
            continue  # the title is a name: the English address already reads right
        base, n = s, 2
        while s in taken:
            s = '%s-%d' % (base, n); n += 1
        taken.add(s)
        put(r, s, 'article address')

# 5. article images, described by the article's title
tt = {}
for (ident, loc), v in title.items():
    tt[(en_title.get(ident, ''), loc)] = v
for r in rows:
    if r['Type'] == 'ARTICLE_IMAGE' and r['Field'] == 'alt' and r['Locale'] in ('it', 'ru') and not r['Translated content'].strip():
        m = re.match(r'(.*) - midsummer-milano$', r['Default content'])
        if m and (m.group(1), r['Locale']) in tt and tt[(m.group(1), r['Locale'])] != m.group(1):
            put(r, tt[(m.group(1), r['Locale'])] + ' - midsummer-milano', 'image description')

# checks: nothing that names how a bed is built; Liquid-unsafe straight quotes in short fields
BAD = re.compile(r'pocket|molle insacchettate|micromoll|пружин|strat[io] di molle|четыр[её]хслой|двухслой|four-layer|two-layer', re.I)
problems = [(k, o['Translated content'][:80]) for k, (o, w) in out.items() if BAD.search(o['Translated content'])]
os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, 'w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, fieldnames=COLS)
    w.writeheader()
    for k, (o, why) in out.items():
        w.writerow(o)
c = collections.Counter((k[0], k[2], why) for k, (o, why) in out.items())
for k, v in sorted(c.items()):
    print('%5d %s' % (v, ' · '.join(k)))
print(len(out), 'rows →', os.path.relpath(OUT, SP))
missing = [x for x in tr if not any(unit(o['Default content']) == x for o, _ in out.values())]
print('translations not used:', len(missing), missing[:10])
print('problems:', problems)
