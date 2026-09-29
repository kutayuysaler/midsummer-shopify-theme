# Midsummer Milano — the new design, built into the live theme

`midsummer-milano-theme.zip` is your **live theme** (the Dawn 15.2 export
`website-audit-fixes-aug-2026`) with the new Midsummer design built into it. Everything
that already works on the live site is unchanged:

- the header, footer, menus and logo
- the enquire panel, enquire tabs, store locator and sleep-assessment quiz
- Google Tag Manager, HubSpot, iubenda, Avada SEO, `robots.txt` and the audit's SEO fixes
- every app embed (EcomSend, store locator, SEOon, Avada, Tipo, Appointo, Air Reviews, Mailchimp)
- the per-product templates (`product.paisley`, `product.vicuna`, …) and the page templates your pages are already assigned

What's new is the design: the Midsummer sections, the redesigned templates, and the
type and colour.

## 1. Upload the photographs to Files

**Content → Files → Upload files**, keeping the names exactly as they are. They're in the
Drive folder `export/upload-to-shopify-files/`:
`ms-graded-bougainvillea.jpg`, `ms-graded-ochre-room.jpg`, `ms-graded-arches.jpg`,
`ms-graded-dune.jpg`, `ms-graded-paisley-red.jpg`, `ms-graded-horse.jpg`.

The design also uses photographs that are already in your Files library:
`Paisleydettaglio.jpg`, `giotto_SANGALGANO.jpg`, `Vicuna-mattress.jpg`,
`Paisley_IMG_5161_low.jpg`, `paisley_india_low.jpg`, `Paisley.png`, `Picture4.png`,
`dreamy_spiaggia.jpg`, `Top_deserto_mobile5.jpg`,
`Paisley_IMG_4918_low_70960abc-….jpg` and the film's poster `Untitled_Project_5_….jpg`.
If one of them was renamed, its slot shows a grey placeholder; pick the picture again
in the editor.

## 2. Upload the theme

**Online Store → Themes → Add theme → Upload zip file** → `midsummer-milano-theme.zip`.
It arrives unpublished next to your live theme, so preview it before publishing.

## 3. The new pages

The existing pages (Contact, Agents & Resellers, Our Story and the rest) already have
their templates and pick up the new design on their own. Create the new ones and
choose the template in each page's **Theme template** dropdown:

| Page | Handle | Template |
| --- | --- | --- |
| Architects & Interior Designers | `professionals` | `page.professionals` |
| Hospitality | `hospitality` | `page.hospitality` |
| Find Your Midsummer | `find-your-midsummer` | `page.find-your-midsummer` |
| Sustainability (existing page) | `our-eco-friendly-approach` | `page.sustainability` |
| Questions (existing page) | `sleep-wise-faq` | `page.faq` |

Collections linked from the design: `essentials`, `signature`, `icons`.

## 4. Product pages

The default `product` template carries the new design: your live product section,
followed by the build drawing, dimensions, the three reasons, the price-on-request
invitation and two photographic plates. Products that are assigned their own template
(`product.paisley`, `product.vicuna` and so on) keep that template, so none of their
content is lost. To move a product to the new design, set its **Theme template** to
*Default product*.

## 5. What the design adds, and how to edit it

Every Midsummer section starts with **MS ·** in *Add section*, and every word, image
and link in it is editable:

- **MS · Hero**: a full-bleed photograph or film with words over it. The homepage film
  is your existing atelier film, set through *Film file URL*.
- **MS · Editorial split**: text beside a photograph, or two text columns, in Ivory, Stone
  or Ink.
- **MS · Cards**: the collections, service steps, doors, trade offers, the three
  Hospitality lines and the captioned photograph pairs.
- **Figures, Pull quote, Compare the collections, Questions and answers, The build in
  section, Dimensions, Find Your Midsummer**: the specialist sections from the design.

Any button can **open the enquire panel**: tick *Open the enquire panel* on it. The
"Book a private appointment" buttons are already set that way, and they still link to
`/pages/contact` for visitors without JavaScript.

**Photographic grade** and **Conversion tracking** sit beside the enquire panel as
site-wide sections. The tracking pushes `ms_cta_click`, `ms_enquiry_open`,
`ms_enquiry_submit` and `ms_quiz_complete` to the GTM dataLayer, each carrying an
`audience_segment`.

## 6. Look and feel

In **Theme settings**, the headings are now Newsreader and the body text Red Hat Text.
Colour scheme 1 is now ivory `#FBF9F5` with ink `#17140F` text and ink buttons, so
your existing Dawn sections match the new ones. To go back, change those two fonts and
scheme 1.
