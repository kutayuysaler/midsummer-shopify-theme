# Midsummer Milano × Atelier — install guide

`midsummer-atelier-theme-final.zip` is the complete theme: Shopify's Atelier 4.1.5
with every Midsummer section, template and setting built in. The theme folders sit at
the top level of the zip, which is what Shopify expects. Uploading it creates a new,
**unpublished** theme and does not touch products, collections, pages, menus or blog
posts.

It passes Shopify Theme Check with no errors and every template setting validates
against its schema, so every file uploads. `CHANGES.md` lists what was fixed relative to
the Claude Design export.

Work through the steps in order. Steps 1–2 take about ten minutes; steps 3–7 are admin
data that can't travel inside a theme file.

---

## 1. Upload the photographs and logos to Files first

**Content → Files → Upload files.** Keep the filenames exactly as they are, because
the templates reference them by name. They're in the Drive folder
`export/upload-to-shopify-files/`:

| File | Used for |
| --- | --- |
| `midsummer-logotype.png` | Header logo |
| `midsummer-logotype-ivory.png` | Header logo over the homepage film (transparent header) |
| `ms-graded-bougainvillea.jpg` | Essentials card, default page band, Journal |
| `ms-graded-ochre-room.jpg` | Signature card, Professionals opening, Hospitality pair |
| `ms-graded-arches.jpg` | Icons card, Hospitality opening |
| `ms-graded-dune.jpg` | Recognition (Green Product Award), 404 |
| `ms-graded-paisley-red.jpg` | Paisley plate |
| `ms-graded-horse.jpg` | Find your Midsummer band, collection, Sustainability, Natural Materials |

The templates also use these photographs, which are **already in your Files library**
because the live site uses them. If any of them has been renamed or deleted, that
image slot shows a grey placeholder until you pick a picture in the editor:

`Paisleydettaglio.jpg` · `giotto_SANGALGANO.jpg` · `Vicuna-mattress.jpg` ·
`Paisley_IMG_5161_low.jpg` · `paisley_india_low.jpg` · `Paisley.png` · `Picture4.png` ·
`dreamy_spiaggia.jpg` · `Top_deserto_mobile5.jpg` ·
`Paisley_IMG_4918_low_70960abc-6877-49b2-abc8-0bd379994114.jpg` ·
`Untitled_Project_5_b49a7740-07fa-45f1-8b4f-464d951b0772.jpg` (the film's poster frame)

## 2. Upload the theme

**Online Store → Themes → Add theme → Upload zip file** →
`midsummer-atelier-theme-final.zip`. Don't unzip it first. Leave it unpublished until
step 8.

## 3. Pages — Online Store → Pages

The templates link to these handles. Where a page already exists on the live site,
keep its handle and just assign the template. Create the ones marked *new*.

| Page | Handle | Template |
| --- | --- | --- |
| Our Story | `about-midsummer-milano` | `page` |
| Handmade in Italy *(new)* | `handmade-in-italy` | `page` |
| Natural Materials | `natural-luxury-materials` | `page` |
| 15 + 15 Refurbishment | `midsummer-milanos-regeneration-service` | `page` |
| Sleep Culture *(new)* | `sleep-culture` | `page` |
| Sustainability | `our-eco-friendly-approach` | `page.sustainability` |
| Architects & Interior Designers *(new)* | `professionals` | `page.professionals` |
| Hospitality *(new)* | `hospitality` | `page.hospitality` |
| Find Your Midsummer *(new)* | `find-your-midsummer` | `page.find-your-midsummer` |
| Agents & Resellers | `agents-and-resellers` | `page.agents-resellers` (the template it already uses on the live site) |
| Book an appointment / Contact | `contact` | `page.contact` |
| Questions | `sleep-wise-faq` | `page.faq` |

`/pages/contact` is also the enquiry panel's page. Any link to it opens the side panel
instead of loading the page, while the page itself keeps working for direct visits,
search engines and visitors without JavaScript.

## 4. Collections, blog and product data

- **Collections** with the handles `essentials`, `signature` and `icons` (5, 7 and 12
  systems). The homepage, the comparison table and the quiz link to them. `/collections`
  is the *Our Beds* landing page (template `list-collections`).
- **Journal** is the existing blog `news`. Tag every article `sleep`, `materials` or
  `design`, so the Journal menu items filter it. The *As featured in* strip links to
  your existing `press-…` blogs.
- **Product metafields**: Settings → Custom data → Products → Add definition:

  | Namespace and key | Type | Shows as |
  | --- | --- | --- |
  | `custom.subtitle` | Single line text | Italic line under the product name |
  | `custom.specification` | Rich text | *Specification* accordion row |
  | `custom.materials` | Rich text | *Materials and fibres* row, plus structured data |

  Empty metafields render nothing. The eyebrow above each product name reads the
  product's **Type**; set it to `Essentials`, `Signature` or `Icons`.
- **Paisley**: in Products → Paisley, make `ms-graded-paisley-red.jpg` the first image.

## 5. Menus — Content → Navigation

The header reads `main-menu`. Keep *Book an appointment* out of it, because it's already the
persistent action on the right of the header.

| Top level | Children |
| --- | --- |
| Our Beds → `/collections` | Mattresses · Toppers · Bases · Headboards · Bedding (your product-type collections) · Bespoke → `/pages/contact` · Compare Beds → `/collections` · Find Your Midsummer → `/pages/find-your-midsummer` · Essentials · Signature · Icons |
| Heritage & Craft → `/pages/about-midsummer-milano` | Our Story · Handmade in Italy · Natural Materials · 15 + 15 Refurbishment · Sleep Culture · Sustainability |
| Professionals → `/pages/professionals` | Architects & Interior Designers · Hospitality · Agents & Resellers |
| Journal → `/blogs/news` | Sleep → `/blogs/news/tagged/sleep` · Materials → `…/tagged/materials` · Design → `…/tagged/design` |
| Contact → `/pages/contact` | Book an appointment · Stockists & Partners → `/pages/agents-and-resellers` · Trade enquiry → `/pages/professionals` · Questions → `/pages/sleep-wise-faq` |

The footer reads five menus by handle. Create each one, mirroring the header branch
of the same name: `footer-our-beds`, `footer-heritage-craft`, `footer-professionals`,
`footer-journal`, `footer-contact`.

## 6. Media to pick in the theme editor

The theme can't pre-select these, because they aren't in the store yet or are videos:

- **Home → Hero — atelier film**: Media type → *Video* → pick the atelier film. Until
  then the hero shows the film's poster frame.
- **Home → As featured in**: 27 publication blocks, in the live site's order and
  already linked. Pick each logo from Files. Until you do, each block shows the
  publication's name in type.
- **Find Your Midsummer**: one image per question (5). This is optional; the quiz
  works without them.
- **Product → Precious materials**: five fibre line drawings (Baby Alpaca, Cashmere,
  Horsehair, Mohair, Yak). This is optional: on the storefront the row shows the names
  only until an icon is picked, and in the editor empty icons show as outlined squares.

## 7. Settings worth knowing

- **Carried over from the live theme, so nothing changes when you publish:** Google
  Tag Manager (`GTM-T2NKS496`), HubSpot tracking, the iubenda consent API, Avada SEO,
  `robots.txt`, the policy-page canonicals, noindex rules, brand-suffixed titles and
  meta description fallbacks. The same app embeds are also switched on: EcomSend,
  store locator, SEOon, Avada SEO, Tipo and Appointo booking, Air Reviews and
  Mailchimp. Check the **App embeds** panel in the theme editor once after upload.
- **The enquiry panel, structured data, photographic grade and conversion tracking**
  are site-wide sections rendered from the layout, the same way the live theme renders
  its enquire panel. The header and footer groups hold only Atelier's own sections,
  so they can never be taken down by custom code.

- **Theme settings → Enquiry-led commerce → Show prices** is **off**. Prices are
  hidden everywhere they could appear (product cards, predictive search, menus,
  cart), and structured data describes each system as *price on request*. Turn it on
  to show prices, for example if Essentials becomes priced.
- **Structured data** (a site-wide section; in the editor it's listed with the other site-wide sections): fill in **Telephone** and **Social profiles**,
  which were left blank rather than guessed. Each graph has its own switch in case an
  SEO app already outputs it.
- **Photographic grade** (site-wide section) applies a warm, matte filter to every photograph
  except files with `graded` in the name. It has four sliders, plus an off switch.
- **Conversion tracking** (site-wide section) pushes these events to `window.dataLayer` for
  GTM/GA4: `ms_track_ready`, `ms_cta_click`, `ms_enquiry_open`, `ms_enquiry_submit`
  and `ms_quiz_complete`. Each carries `audience_segment` (private,
  architect-designer, hospitality, dealer or press), inferred from the page path.
  Override it on any element with `data-ms-segment="dealer"`. Turn on **Log events to
  the browser console** while you set up GA4.
- **Footer → Social links** are blank, so add the correct accounts.
- The scroll-reveal motion lives in `assets/ms-motion.js`. To switch it off, delete the
  one `<script>` line marked in `layout/theme.liquid`.

## 8. Before you publish, check the placeholder content

The theme's copy is written and editable, but a few things were placeholders that
only you can confirm:

1. **Agents & Resellers**: the 22 markets on the map are an illustrative structure,
   not your real partner list. Replace, rename or delete the *Market* blocks; the map
   redraws from each block's latitude and longitude (decimal degrees, and either
   `45.4642` or `45,4642` works).
2. **Dimensions**: the five sizes are European standards (Singolo 90 × 200 up to Super
   King 200 × 200). Check them against your schedule.
3. **Figures**: 2 artisans · 24 systems · 6 spring layers · 15 + 15 years. Add
   hours-per-system or systems-per-year if you publish them.
4. **Hospitality**: the lines are named Amalfi, Silver Dream and Rapallo, in block order.
   Drag the blocks to reorder them.
5. **Pull quote**: currently the Green Product Award 2025. Swap in a named press or
   client quote once one is cleared.
6. **Questions**: review the eleven FAQ answers on the FAQ page. The FAQ structured data
   is emitted there only; the homepage and Hospitality show the same questions without
   duplicating the markup.

Then preview each template (Home, a product, a collection, `/collections`, each page
above, the Journal and an article), and publish.
