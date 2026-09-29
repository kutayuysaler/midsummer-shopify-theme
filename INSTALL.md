# Midsummer Milano: installing the theme

`midsummer-milano-atelier.zip` is built page by page from the approved preview
(`Midsummer Atelier - Preview.html`). Every band of every screen is its own section,
with the preview's exact markup, type, colour and spacing. The fonts and the graded
photographs ship inside the theme, so nothing needs uploading to Files first.

## What changed from the last upload

- **The homepage no longer shows the 404.** The earlier homepage used about 20 stock
  Atelier sections with 175 blocks, and one invalid value was enough for Shopify to drop
  the whole file. The new templates list only Midsummer sections, with no stock settings
  to get wrong.
- **The pages render in their own layout, `layout/ms.liquid`,** so Atelier's styles can't
  change the design. The cart and other stock pages keep Atelier's layout, with the
  Midsummer header and footer.
- **Nothing loads from outside the store.** The fonts, the logotype, the graded
  photographs, the map library and the world map are theme assets. The other
  photographs are the store's own files on its CDN, exactly as the preview uses them.

## 1. Upload

**Online Store → Themes → Add theme → Upload zip file** → `midsummer-milano-atelier.zip`,
then **Preview**. If Shopify lists errors against the theme after the upload, send me
that list.

## 2. Pages and their templates

In each page, set **Theme template**. Create the pages that don't exist yet.

| Page | Handle | Template |
| --- | --- | --- |
| Architects & Interior Designers | `professionals` | `page.professionals` |
| Hospitality | `hospitality` | `page.hospitality` |
| Find Your Midsummer | `find-your-midsummer` | `page.find-your-midsummer` |
| Natural Materials | `natural-luxury-materials` | `page.natural-materials` |
| 15 + 15 | `midsummer-milanos-regeneration-service` | `page.regeneration` |
| Questions | `sleep-wise-faq` | `page.faq` |
| Agents & Resellers | `agents-and-resellers` | `page.agents-resellers` |
| Sustainability | `our-eco-friendly-approach` | `page.sustainability` |
| Contact | `contact` | `page.contact` |
| Our Story, Handmade in Italy, Sleep Culture, Terms, Privacy | as they are | `page` (the default) |

Home, Our Beds (`/collections`), each collection, each product, the Journal
(`/blogs/news`), each journal note, search and 404 need nothing: those templates are
the defaults.

## 3. Data the design reads

- **Collections** `essentials`, `signature` and `icons`. Their opening photograph,
  numeral and introduction come from the preview until you give a collection an image
  and a description.
- **Products** show their first photograph, their collection, their title and the line
  under it. That line is the metafield `custom.subtitle`; until it exists, the
  preview's line for that system is used. The second and third photographs fill the
  two plates further down the page.
- **Journal**: the first article is the large feature. Each article's first tag is its
  label ("Materials", "Craft"). The subject links read the tags Sleep, Materials and Design.
- **The enquiry sheet** opens from every "Book an appointment" or "Request a proposal"
  link. It submits through Shopify's contact form, so enquiries arrive at the store's
  email, with the chosen intention ("Book appointment", "Request brochure" and so on)
  in the message.

## 4. Editing

Every word, photograph and link in a section is a setting in the theme editor. Some
sections carry more text than fits in 40 settings, so their later lines are fixed in the
code. That applies to the header's panels and the phone menu. The FAQ
answers, the press strip and the map markets are blocks, so you can add, remove and
reorder them.

**Before publishing, check two things:**
- The 22 markets on the Agents & Resellers map are the preview's structure, not a
  confirmed partner list.
- The press strip shows each publication's name until you pick its logo.
