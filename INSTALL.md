# Midsummer Milano: installing the theme

`midsummer-milano-atelier.zip` is the approved preview built as a Shopify theme. Every
band of every screen is its own section. The fonts, the logotype, the graded
photographs, the press logos and the map ship inside the theme.

## Start here: what you need to do

1. In **Online Store → Themes**, delete the Midsummer theme you uploaded before. Shopify
   silently refused two of its sections (the Agents & Resellers map and the enquiry
   page), so that copy can't show those pages. This version fixes it.
2. **Add theme → Upload zip file** → `midsummer-milano-atelier.zip`, then **Preview**.
   Every page opens from the menus, with nothing else to set up.

Before launch, for search engines: run the page script once (section 3). It gives your
existing pages (Contact, Agents & Resellers, About, Handmade, FAQ …) their new design at
their own address, and creates the designed pages the store doesn't have yet (Architects &
Interior Designers, Hospitality, Sleep Culture, The Atelier, Compare the collections, At a
glance …). Then see **SEO-ROLLOUT.md** for the rest of the launch list.

## 1. Upload

**Online Store → Themes → Add theme → Upload zip file** → `midsummer-milano-atelier.zip`,
then **Preview**.

## 2. What happens on its own

- **Every link finds its page.** Header, footer and page links look up the store's real
  pages, collections and blog by handle (for example `about-midsummer-milano` or
  `about-us`, `sleep-wise-faq` or `faq`, and `news` or `journal`). If a page has another
  handle, point the link at it under **Theme settings → Midsummer · Where links go**.
- **No two menu titles lead to the same page, and none leads nowhere.** A place whose
  page doesn't exist yet opens its own designed page (section 11). Only the Mattresses,
  Toppers, Bases, Headboards and Bedding collections and the Journal's subjects stay out
  of the menus until they exist. Other duplicates are fixed too:
  - "Store locator" is now called Agents & resellers everywhere.
  - "Cookies" opens Shopify's cookie preferences.
  - "Care and maintenance" opens the care question on the Questions page.
  - The Journal panel's picture shows your newest article.
- **Existing pages take their design without a template.** The default page template
  carries each designed page and shows it only on its own page. That covers Questions,
  Natural Materials, 15 + 15, Sustainability, Professionals, Hospitality and Find your
  Midsummer. Every other page (About Us, Terms and so on) gets a centred editorial
  layout.
- **The quiz.** Your live page that uses the `sleep-assesment` template shows the new
  Find your Midsummer quiz. If the store has no quiz page at all, every "Find your
  Midsummer" link opens the quiz as an overlay, on any page.
- **Agents & Resellers** keeps its template (`page.agents-resellers`, with
  `page.agents-and-resellers` as a copy), and the default page template shows it too, so
  the map appears whichever template the page has. The map's code and world outline are
  written into the page itself, so it never waits on another file. It shows all 16 places from your current store
  locator; the old section held 13 of them in its own code and the other 5 as blocks:
  - **The atelier:** Midsummer Milano, Milan.
  - **Showrooms:** bredaquaranta, Bergomi Milano, Bergomi Monza, Villa Arredamenti
    (Colnago), Vago Arredamenti (Barlassina), WWTS London, HH Solutions (Warsaw), WWTS
    Moscow, Maison Territo (Montreal) and Passerini Design (Jupiter, FL).
  - **Boutiques:** Berenice in Cannigione and Porto Cervo, and Passerini Design in Palm
    Beach.
  - **Agents:** COSE & COSE (San Marino) and In Made (Hong Kong).
  - **Corrections:** Cannigione now sits in Cannigione (its old marker was about 6 km
    east, near Porto Cervo), and Palm Beach's street reads N County Rd.
  - **Editing:** each place is a block, with its address, telephone, email, website and
    position.
- **The locator page:**
  - The list and the map sit side by side at the same height.
  - Choosing a place opens its details inside the list and flies the map to it.
    Clicking a marker opens its place in the list.
  - Places close together gather into a numbered cluster that opens as you zoom. The
    three Milan addresses on neighbouring streets are listed together when you click
    them.
  - Search by city, country or name, and filter Showrooms, Boutiques or Agents.
    World, Europe, Americas and Asia Pacific frame the map.
  - Scrolling the page never zooms the map. Zoom with Ctrl/⌘ and scroll, by pinching,
    or with the + and − buttons.
  - "Request an introduction" opens the enquiry sheet with the message already written.
  - The finer world map loads only when you zoom in.
- **Press.** Each publication on the home page links to its own press blog
  (`press-elle-decor`, `press-vanity-fair` …). Those blogs keep their template,
  `blog.press`, which now shows the publication's mark, its pieces, and every other
  publication beneath.

## 3. Pages to create

Four pages have a design in the theme but no page in the store yet. Until you create
them, their menu entries open the same design at a stand-in address (section 11); create
them so they get their own address and appear in search engines.

| Page | Handle | Template |
| --- | --- | --- |
| Architects & Interior Designers | `professionals` | `page.professionals` |
| Hospitality | `hospitality` | `page.hospitality` |
| Handmade in Italy | `handmade-in-italy` | `page.handmade-in-italy` |
| Sleep Culture | `sleep-culture` | `page.sleep-culture` |
| The Atelier | `atelier` | `page.atelier` |
| Compare the collections | `sleep-collections` | `page.compare` |
| Midsummer Milano at a glance | `midsummer-milano-at-a-glance` | `page.facts` |

**With the script** (`scripts/create_pages.py`): pages the store already has (under any
address the theme knows, such as `italian-craftsmen-luxury-mattresses` for Handmade in Italy)
are switched to their designed template and keep their text; only missing ones are created,
so nothing is duplicated:

1. In Shopify admin, go to Settings → Apps and sales channels → Develop apps → Create an
   app.
2. Under Admin API scopes, give it `write_content` and `read_content`, then install it and
   copy the Admin API access token.
3. Publish this theme first, so the templates exist. Then run:

```
SHOPIFY_STORE=your-store.myshopify.com SHOPIFY_ADMIN_TOKEN=shpat_... python3 scripts/create_pages.py
```

Add `--dry-run` to see what it would do first. Nothing is deleted. You can delete the app
afterwards.

**By hand:** in **Online Store → Pages → Add page**, enter the title, set the handle
under "Search engine listing", and choose the template on the right.

The designs:
- **Professionals and Hospitality** also appear on the default template, so you can skip
  choosing a template for those two.
- **Handmade in Italy:** the opening photograph and the page text, then *The making*: a
  photograph held in place while five stages scroll past it (core, fibres, tufting,
  border, cloth). After that, two photographs and the invitation to the atelier.
- **Sleep Culture:** the opening photograph and the page text, three things a good night
  is made of, the Journal's notes tagged *sleep*, and the quiz.

The step texts are a first draft; please check them against how the beds are really made.
Each is editable in the theme editor.

The collections `essentials`, `signature` and `icons` are used by the Our Beds panel and
the collection pages. If one doesn't exist, its links go to `/collections`. By type,
Mattresses, Toppers, Bases, Headboards and Bedding appear when a collection with that
handle exists and has products.

## 4. Product pages

The photographs sit on one large, square stage, as the great bed houses show theirs. A strip of
every picture runs beneath it. Arrows appear on hover, a counter shows where you are,
the keyboard arrows work, and a click opens the photograph full screen. On a phone the
stage runs the full width and you swipe through the pictures. The first photograph
opens the page, so put the strongest one first in the product's media. If you set a
focal point on a photograph in admin, the crop follows it.

On the right are the name, the line under it, price on request and the two enquiry
buttons.

Dimensions and fabric follow straight after, in the store's six sizes. Small Double is
chosen to begin with, and a plan of the bed (pillows, the turned-down sheet) changes
with the size:

- Single 100 × 200
- Queen 153 × 203
- Small Double 160 × 200
- Double 180 × 200
- King 193 × 203
- Double Extra 200 × 200

**About this system** (the product description) is open from the start. Below it,
**Natural fibres** lists that system's fibres one per row, in the same measure as the
facts above: the fibre's drawing, its name and what it does. Their drawings arrive on a
white ground, so the theme blends the white away and only the ink line shows. "All the
fibres" leads to the Natural materials page. In the editor they are the **Fibre** blocks
of the Product · Main section.

Then comes **The build, in section**, a dark band drawing that system's own layers, from
the top of the bed down, as the Models & Layers book sets them out. Each part of the bed
(Topper, Mattress, Boxspring, or Summer side and Winter side for Ultra Dry) is drawn as its
own piece. The heading counts the layers in words ("Twenty-nine layers, laid by hand."),
the drawing opens on the first spring layer, and you can hover, tap or step through
them; the note beside the drawing says what each layer does. Where the book gives a
seasonal padding, it is listed under the note.

Depths are never given in figures. The drawing is marked "Indicative, not to scale", and
each layer carries a word instead (Fine, Light, Generous, Deep, Foundation). In the editor
each layer is a **Layer** block: name, part of the bed, depth word, texture and note. Add,
remove or reorder them there. A product with no layers doesn't show the band at all.

- **Layers from the book:** Amalfi, Bellagio, Bellini, Brera, Capri, Dreamy 2, Dreamy
  Springs, Flora, Giotto, Monteverdi, My Dream, Raffaello, Roma, Storage, Top 2, Ultra Dry,
  Vicuña, Vivaldi 2, Vivaldi Plus.
- **Essenziale** isn't in the book. Its layers follow its own product description, so
  check them.
- **Monteverdi:** the book contradicts itself. It is drawn from its plant-based
  composition (linen and Ingeo™, vegetal horsehair, two layers of pocket springs), so check
  it.
- **Not in the book, so no build band:** Paisley, First Dream, Topper Roma, and any product
  on the default product template. Add Layer blocks to show one.

The other systems in the collection come last. The line under the name is the metafield
`custom.subtitle`; without it, the preview's line for that system is used.

**Products keep their own templates.** The old theme gave 24 products a template of their
own (`amalfi`, `bellagio`, `bellini`, `brera`, `capri`, `dreamy-2`, `dreamy-springs`,
`essenziale`, `first-dream`, `flora`, `giotto`, `monteverdi`, `my-dream`, `paisley`,
`perfumes`, `raffaello`, `roma`, `storage`, `top-2`, `topper-roma`, `ultra-dry`,
`vicuna`, `vivaldi-2`, `vivaldi-plus`). This theme has a template under each of those
names, so every product picks up the new design with nothing to reassign.

- Each template carries that system's natural fibres (for example Cashmere, Silk, Cheviot
  Wool, Horsehair), taken from the old theme's icons, and its own layers from the book.
- Every product page runs in this order: the system with its fibres, dimensions and
  fabric, the build, then the other systems.
- `topper-roma` also lists its sizes and covering.
- `perfumes` opens on a photograph.
- The `appointment` template keeps Atelier's own product page, so the booking product and
  its app go on working.

## 5. Pages with a design of their own

These pages already use these templates in the store, so each one switches to its design
by itself. Their text comes from the page itself, so what you write in admin appears in
the design.

| Page | Template | What it shows |
| --- | --- | --- |
| Loro Piana Interiors | `page.loro-piana-interiors` | The opening photograph and the page text. Then the palette of seven cloths (Paisley, Kummel, Tawny, Burnt Orange, Earthy Neutral, Verdant Green, Muted Blue), seasonal upholstery, Paisley in two photographs, Signature and Icons, and an invitation to see the cloths in Milano. |
| Download the Dream | `page.download-the-dream` | The Art of Rest: the page text, then the eight works (Toulouse-Lautrec, Frida Kahlo, Casorati, Rousseau, William Morris, Renoir, Magritte, Hockney), each opening full screen. The Dropbox link downloads the series. |
| Salone del Mobile 2026 | `page.salone-2026` | Full-screen opening "This year, the answer is Paisley.", the page text, two photographs, the Salone film and the invitation to Via Andegari 4. |

Journal posts and blog:

- `article.salonedelmobile` shows the post with its film.
- `article.greenproductaward` shows it with the five photographs of the Top bed system.
- `article.sleep-assessment` shows it with the quiz.
- `blog.collaborations` opens on La Strega del Castello.

Each band can be edited in the editor: its photographs, cloths, works and text. The same
bands (Opening photograph, Statement and text, Fabric palette, Works of art, Two
photographs, Film, Photographs, Closing band, Collections) can be added to any
other page.

## 6. Enquiries: the enquiry page and the sheet

**The enquiry page** is your Contact page (`/pages/contact`, template `page.contact`; the
default page template shows it too, and `contact-us` or `contatti` work as handles),
redesigned as a full landing page. It is reached from the Contact menu's picture card, the
phone menu's "Enquire", every enquiry link in the menus, and the footer. The brochure is
requested through the form, never downloaded directly:

- An opening, then seven enquiries side by side with one form whose labels change with
  the choice: book an appointment, request a proposal, request brochure, request a
  callback, trade enquiry, become a partner, and leave a message.
- What happens next, then direct lines (address and hours, email, WhatsApp).
- Two ways onward: Agents & resellers and Find your Midsummer.

Every enquiry in the menus and the footer leads here, each to its own form:

| Menu entry | Opens |
| --- | --- |
| Book an appointment, Book a private appointment | `?enquiry=appointment` |
| Bespoke | `?enquiry=proposal` |
| Trade enquiry | `?enquiry=trade` |
| Become a partner | `?enquiry=partner` |
| Direct contact | `#direct` |
| Enquire → (footer) | the page |

`brochure`, `callback` and `message` work the same way in a link.

**The enquiry sheet** (the side panel) stays for the **Book an appointment** button at
the top right and for the buttons inside the pages:

- The product page's Request a proposal opens it on the proposal form.
- An introduction on Agents & Resellers opens it with the message written.
- Its link "Open the full enquiry page" carries the chosen enquiry across.

Both send through Shopify's contact form. The chosen enquiry arrives as "Enquiry mode",
so each message says what it is.

## 7. Movement and finish

These apply across the site:

- **Between pages:** a short cross-fade in Chrome, Edge and Safari 18. Other browsers
  simply load the page.
- **Figures:** the home page's figures count up the first time they come into view.
- **Collection pages:** each bed card fades to the bed's second photograph on hover.
- **Journal notes:** a thin reading line runs along the top, and the previous and next
  notes are linked at the end.
- **Editorial pages (About Us …):** photographs no longer grow taller than the screen.
- **Keyboard:** focus is visible, in the house gold.
- **Anchor links:** they stop below the header.
- **Reduced motion:** visitors who ask their device for less motion get none of the
  movement.

## 8. One site, fewer and fuller pages

- **Made to last.** Sustainability and the 15 + 15 regeneration service were two pages
  saying much of the same thing. They are now one page, "Made to last", in this order:
  the 15 + 15 service and its promise, the four principles, what happens at year
  fifteen, the timeline, what we do not claim, and bringing your mattress home. Both
  addresses show it, and the menus carry one entry, "Made to last · 15 + 15". If you
  like, delete the Sustainability page and add a URL redirect (Online Store → Navigation
  → URL Redirects) from `/pages/our-eco-friendly-approach` to the 15 + 15 page.
- **Product pages:**
  - **Gallery:** a larger stage with a slim column of thumbnails and a soft cross-fade.
    Click the left or right of the photograph to move through them. A fine segmented line
    and a counter sit below, and the middle of the photograph opens it full screen. On a
    phone you swipe full width.
  - **The fibres:** now beside the photographs, under About this system.
- **Journal:** two views, remembered per visitor.
  - **Gallery:** the newest note opens the page; the rest follow in a magazine rhythm,
    each numbered like an issue.
  - **Index:** every note as a line of type, and the photograph follows the cursor.
- **Editorial pages (About Us …):** text in one centred reading column, photographs in a
  wider band, always centred, however the editor wrapped them.

## 9. Social accounts and WhatsApp

Your accounts, as small icons:
- **Where they appear:** the footer, the foot of every menu panel, the Contact panel,
  the foot of the phone menu, the enquiry page's direct lines, and the home page's new
  Follow the atelier band.
- **Accounts:** Instagram, Pinterest, LinkedIn, WhatsApp, Telegram and VK, pre-filled
  from your old theme. Facebook, YouTube and TikTok appear as soon as you add their
  links.
- **WhatsApp:** also a link among "Speak to us" in the Contact panel, and a small round
  button in the corner of every page. It appears once the visitor scrolls, opens to
  "Chat with the atelier" on hover, and steps aside when a menu or the enquiry sheet is
  open.

Change or remove any of them under **Theme settings → Midsummer · Social and WhatsApp**.
The addresses are now saved in the theme's own settings as well, so they show as soon as
the theme is installed. If they are still missing on your store, open that settings group:
an empty field there hides its icon.

## 10. The home page, in chapters

The home page is now twelve calm bands, one idea per screen, on one rhythm of space: where
two bands share a ground, the second adds no gap of its own, so no stretch of the page is
left empty:

1. **The film**, with Book a private appointment.
2. **Opening words:** one sentence, centred, signed by Chiara Mennini, and a link to Our
   story.
3. **The three collections.**
4. **I · Handmade in Milan:** a tall photograph beside *Two artisans. One bed.*, with three
   figures (2 artisans, 24 systems, 6 layers of springs).
5. **II · Inside a Midsummer bed:** the Top System's twenty-nine layers, interactive.
6. **III · Natural fibres · Loro Piana Interiors:** *Only what nature makes. Dressed in Loro
   Piana.*
7. **IV · Why Midsummer:** the six-point comparison.
8. **V · Made to last:** *Fifteen years. Then fifteen more.*, across the whole screen.
9. **Recognition & press:** one piece at a time. The award comes first, with its mark. Then each
   publication's mark and the headline of its piece, taken live from that publication's press
   blog (press-il-sole-24-ore and so on), with "Read the piece". The pieces change on their
   own, with a fine bar to step through them, and pause while you read. Beneath, every
   publication's mark runs in one slow grayscale line; hover or tap a mark to bring its piece
   forward. A publication joins the sequence as soon as its press blog has an article (or you
   write a headline in its block). The others stay in the line and link to their page.
10. **The Journal.**
11. **Follow the atelier:** @midsummermilano, your accounts and five photographs.
12. **Come and lie down:** the atelier on Via Andegari and Book a private appointment.

Each chapter is a **Home · Chapter** section: change the photograph, the words, the
figures and the link in the editor, or add another chapter anywhere. The figures, the
service steps, the quiz band, the trade band and the newsletter are off the home page now
(the quiz and the trade desk are in the menus); their sections stay in the theme.

## 11. Menus and pages that always open

**Why pages didn't open before:** to decide where a menu entry should go, the theme
searched your store's own menus by keyword. For some places that found a different
address than the one the page is published at, and then the page's design didn't
recognise it as its own page and showed nothing. The theme no longer guesses.

**Now each place goes, in this order, to:**
1. A link you set under **Theme settings → Midsummer · Where links go**.
2. Your store's real page, collection or blog, by its address. These come from your live
   site:

   | Place | Address |
   |---|---|
   | Our story | /pages/about-midsummer-milano |
   | Handmade in Italy | /pages/italian-craftsmen-luxury-mattresses |
   | Natural materials | /pages/natural-luxury-materials |
   | Agents & Resellers | /pages/agents-and-resellers |
   | Questions | /pages/sleep-wise-faq |
   | Contact and every enquiry | /pages/contact |
   | Download the dream | /pages/download-dream-art-of-rest |
   | Mattresses, Toppers, Beds with headboards, Duvets | /collections/mattresses, mattress-toppers, beds-with-headboards, duvets |
   | Journal, Press, Portfolio, Collaborations | /blogs/news, press, projects, collaborations |

3. The place's designed page, which always exists, for places your store has no page for
   yet: Sleep culture, Loro Piana Interiors, Made to last · 15 + 15, Find your Midsummer,
   Architects & Interior Designers, and Hospitality & Contract. These open at
   `/collections/all?view=ms-<place>`.

**Pages always open in their design, whatever template admin gave them.** A page with a
design of its own is linked with `?view=<template>` (for example
`/pages/sleep-wise-faq?view=faq`), so it shows its design with its own title and words.
Opened directly, from Google say, the page still recognises itself by its address and
shows its design.

**The menus, at a glance:**
- **Our beds:** Essentials, Signature, Icons; Mattresses, Toppers, Beds with headboards,
  Duvets and sheets; Compare the collections, Find your Midsummer, Request a proposal.
- **Heritage & craft:** Our story, Handmade in Italy, Sleep culture, Natural materials, Loro
  Piana Interiors, Made to last · 15 + 15.
- **Professionals:** Architects & Interior Designers, Hospitality & Contract, Portfolio,
  Become a partner, Trade enquiry.
- **Journal:** the three newest notes; All notes, the subjects, Press, Collaborations.
- **Contact:** Book an appointment, **Agents & Resellers** (the map of showrooms), The
  Milano atelier, Direct contact, WhatsApp, Questions & customer care.

No two titles lead to the same page. The footer and the phone menu use the same
addresses.

### The menu panels

Each title in the bar opens a panel that drops down while the page behind dims:
- **Layout:** the panel's number and title with a line on the left; the places as large
  titles, each with a short line; and, for Heritage, Professionals and Contact, the
  photograph of the place under the pointer on the right.
- **Our beds and Journal:** the three collections, or the three newest notes, as
  pictures.
- **Foot of every panel:** the atelier's address and hours, Book an appointment, and your
  social accounts.

All the words, lines and the collection photographs are in the **MS · Header** section
under *Menu panels*.

**Why the Icons collection didn't load:** the menu went to `/collections/icons`, but
the store's Icons collection lives under another handle. It is now found by its title.
If it still doesn't open, check in admin that the collection is published to the Online
Store and has products, or set its link under Theme settings → Midsummer · Where links go.

## 12. Photographs from your own library

I went through the photo library in your Google Drive. That covered the catalogue and location
shoots, the atelier shoots at Via Andegari (including Pure and the parrot and blue-and-gold
rooms), Lierna, Lucca, Tulip, the Mood folder and the craftsmen. Twenty-four of them are now in
the theme as web-sized assets (`assets/ms-photo-*.jpg`, about 8 MB together), so they show
without uploading anything:

| Photograph | Where it appears |
|---|---|
| Mattress with the MIDSUMMER label (atelier, DSC4500) | Home · Two artisans, one bed |
| Bed against the blue-and-gold wallpaper (Pure, DSC4320) | Home · Come and lie down |
| Orange leather bed, blue-and-gold room (Pure, DSC4401) | The Milano atelier in the Contact panel |
| Seamstress cutting cloth (SARTA) | Handmade in Italy · Slow, by method; Handmade in the menu |
| Craftsman's portrait (Frugone) | Handmade in Italy · Slow, by method |
| Asleep on My Dream (My dream 9717) | Sleep culture · Support |
| Shepherd carrying a sheep (PECORONE) | Natural materials in the menu; Follow the atelier |
| Parrot room with red bedding (DSC4636) | Follow the atelier |
| Red throw on white bed (Lucca, DSC0035) | Follow the atelier |
| Villa doorway, bed beyond (A8447393) | Book an appointment in the Contact panel |
| Loft with spiral staircase (A8447647) | Our story; Heritage panel |
| Frescoed bedroom, paisley throw (AMB_01) | Professionals page and panel; Follow |
| Draped room with fireplace (AMB_02) | Home · Fifteen years, then fifteen more; 15 + 15 in the menu |
| Window and armchair (AMB_05) | Sleep culture in the menu |
| Glass house in the forest (MODERNA_01) | Hospitality page and panel |
| Tufted mattress detail (DSC3726) | Handmade in Italy · the tufting |
| Cashmere throw (A8447515) | Home · Only what nature makes; Natural materials opening |
| Paisley throw (A8447571) | Loro Piana Interiors page and menu; Follow |
| Silk and stitching (A8447706) | Handmade in Italy · the border |
| Linen sheets, cream blanket | Sleep culture · temperature, the seasons |
| Atelier armchair, painted ceiling, Lake Como balcony | In the theme, ready for any section |

Any of them can be replaced in the theme editor by picking another photograph in that
section.

**What I left out, and why:**
- The Mood folder's stock pictures (Unsplash and Shutterstock), because they aren't yours to
  use as brand imagery.
- The Lierna villa interiors, beautiful but showing someone else's house rather than a
  Midsummer bed.
- The Tulip set, a plain catalogue of the velvet bed that suits its product page better than
  the site.

**Too large to bring across here (over 10 MB each):** the craftsmen at work (IMG_1111–1114)
and the high-resolution craftsman portrait (Frugone TIF). Upload them under Settings → Files
and pick them in Handmade in Italy. The portrait in the theme is small and looks softer.

## 13. Search engines and AI search (SEO and GEO)

Already done in the theme, with nothing to set:

- **One heading per page.** Every page has exactly one main title (h1). The quiz overlay no
  longer adds a second one.
- **Titles and descriptions.** Every page has a title and a meta description. Pages that
  have none in admin get one written for them. The stand-in pages carry their own title
  and description and are kept out of search results (`noindex`), so Google only lists the
  real pages.
- **Sharing.** Every page has a picture for WhatsApp, iMessage, LinkedIn and Facebook
  previews (the atelier, when the page has none of its own).
- **Structured data (schema.org).** The house as an Organisation and shop, with the
  atelier's address, opening hours, map position, founder (Chiara Mennini), logo, contact
  point and every social profile from Theme settings. Also the website with site search,
  breadcrumbs, each product (its fibres, its specification, made to order in Italy) and each
  Journal article. The FAQ page is marked up as questions and answers.
- **Speed and stability.** Every picture states its size, so nothing jumps while the page
  loads. Pictures below the first screen load only when reached, and the two fonts are
  preloaded.
- **AI search (GEO).** *Midsummer Milano at a glance* (`page.facts`) is a plain fact sheet,
  linked from the footer. `/?view=llms` is a plain summary of the house for ChatGPT,
  Perplexity, Gemini and Claude: who you are, the key facts, every collection and product
  with a line about it, the professional pages, and the press. It is built from the store
  live, so it never goes out of date. Add the redirect in **Start here**, step 4, so it
  also answers at the standard address `/llms.txt`. `robots.txt` keeps Shopify's own
  rules and points to it.

The step texts and figures written for the designed pages are a first draft; please check
them against how the beds are really made.

## 14. New in this round

- **Compare the collections**: a real comparison of Essentials, Signature and Icons. Every
  "Compare" and "Our beds" link opens it (your page *sleep-collections* opens in it, or a
  stand-in address).
- **Icons, Essentials and Signature** always open: the store's collection if it exists, or
  the systems listed by product handle (snippets/ms-tier.liquid).
- **The Milano atelier**: its own page (a store page with the handle *atelier* opens in it).
- **Heritage & Craft**: every chapter ends with the previous and next chapters.
- **Professionals and Hospitality**: places to go next, projects (from a blog with the handle
  *projects*, hidden if there is none) and trade questions.
- **Questions & customer care**: 22 answers in five topics, a care guide and a sizes guide.
- **Journal**: notes are filed automatically into Sleep, Materials, Craft, Longevity, Projects
  and News, by their tags, title and opening. The Journal page and the menu use the same list.
  To force a subject, tag the note with it.
- **Inside the bed** replaces the layer drawing on the home page and every product page: the
  three parts and the hand, never the build.
- **Fibre marks**: one coherent mark per fibre on product pages and the materials page.
- **Letters from the atelier**: newsletter on the home page and the Journal.
- **Clients' words**: on the home page, hidden until you add quotes in the theme editor.

## 15. New in this round: palette, the bed opened, fibres, notes

- **The whole Loro Piana Interiors palette** on the Loro Piana Interiors page: 39 cloths. That is
  32 photographed from your colour cards (Drive, *Loro Piana Interiors Color Scheme*: 20 plain
  cloths and 12 textured weaves) plus the 7 shades named in the collections. Visitors filter by
  weave and by tone, open any cloth large, and *Ask about this cloth* opens the enquiry with the
  cloth's name already written. The cards carry no names, so the photographed cloths are named
  here by tone (Blush, Camel, Bordeaux…). In the theme editor (Fabric palette → each Cloth) you
  can rename them with the atelier's references, replace a photograph, or add cloths (up to 50).
  Product pages show a row of these cloths, leading to the whole palette.
- **Inside the bed, opened**: on the home page and every product page, select the topper, the
  mattress or the base (in the drawing, the buttons or the photographs). The part lifts away and
  the words beside it open on that part: what it does, the choices it comes in (seasonal faces,
  Roma with its headboard, a removable Loro Piana Interiors covering embroidered on request;
  storage, slender or round bases; headboards to your drawing), and the fibres we tend to use,
  each with its mark. There are no layers, counts or heights, and nothing of the technique.
  Every line can be edited in the theme editor (Inside the bed → Part I, II, III; points are
  one per line, fibres are separated by commas).
- **Drawn fibre marks**: each fibre now has its own drawing in one thin line, replacing the
  letters: sheep for the wools, a goat for cashmere and mohair, a camelid for alpaca and vicuña,
  a camel, a yak, a horse for horsehair, a cocoon for silk, a flax flower for linen, a cotton
  boll, a palm for vegetable horsehair, corn for Ingeo™, an orange slice for Orange Fiber and a
  hemp leaf. An unknown fibre gets a woven thread.
- **The end of a Journal note**: the share line, then a sign-off from the atelier (book an
  appointment, all notes, more on the same subject), then the previous and next notes with their
  titles, pictures, subject and date. The empty boxes and the double underline are gone. *More
  notes* leaves out those two neighbours when the Journal has enough other notes.

## 16. Phone pass

Every page was reviewed screen by screen at phone size (390 px), as a phone shows it.

- **Questions & customer care**: the "Not here? Ask us directly" note no longer floats over the
  questions on a phone (it stays beside them on a computer).
- **Compare the collections**: on a phone the names Essentials · Signature · Icons stay pinned
  above the table while you scroll the rows.
- **Enquiry sheet**: on a phone the form gets the whole sheet (the atelier's address stays on
  the enquiry page and in the footer).
- **"Where to go from here" cards** and **search results**: two to a row on a phone instead of
  one full-screen card each.
- **Discretion**: the last mentions of spring layers ("Six spring layers over the Vivaldi core",
  "over a micro spring layer", the stages on Handmade in Italy) now speak of the result, not the
  build.

## 17. Computer pass

Every page was reviewed again screen by screen at 1440 × 900.

- **Menu**: the Contact panel's first photograph was missing; every panel now shows its pictures.
- **Product pages**: the photographs stay beside you while you read the details, sized to fit
  the window.
- **Steps** (the atelier visit, Sleep culture, Handmade in Italy): the steps you are not on are
  dimmed less, so they stay readable.
- **Home**: the opening words keep their contrast over the photograph.
- **Footer**: the WhatsApp button no longer covers the last links.
- **Spelling**: fibre throughout (Orange Fiber keeps its own name).

## 18. Tablet pass

Every page was reviewed on a tablet held upright (768 × 1024) and on its side (1024 × 768).

- **Header on an upright tablet**: the menu bar was cut off after "Professionals", so Journal
  and Contact could not be reached. Upright tablets now open the menu from its button (as
  phones do) and keep *Book an appointment* in the bar. On its side the full bar fits.
- **No lonely cards**: rows of cards no longer end with a single card alone (three collections
  as two and one, four notes as three and one). The site picks the nearest even layout by
  itself, on tablets and computers, so this also holds when you add or remove cards.
- **Questions & customer care**: on tablets the questions now use the full width, with the
  "Not here?" note above them instead of a narrow empty column beside them.

## 19. Journal and product pages, again

- **Notes with their own sections** (Salone del Mobile, Green Product Award, Sleep assessment):
  the sign-off and the previous/next notes now come after the film, the gallery or the quiz,
  so the note ends once. A new section, *Note ending*, carries it; on such a note, the
  *Journal note* section has "End the note after the sections below" ticked. To give another
  note its own sections, add them, then add *Note ending* below them and tick that box.
- **Journal**: the mosaic's last row fills the width (two notes share it, a single note takes
  the middle); the subjects keep a little space under a banner (Collaborations); "Older →"
  stays clear of the WhatsApp button.
- **Toppers**: on a product whose name contains "Topper", *Inside the bed* opens on the topper.
- **The appointment product** (product.appointment) keeps the store's own layout, because it
  is bought through the cart.

## 20. Home page, again

The home page was reviewed section by section on computer, tablet and phone; it holds
together at every size. The remaining mentions of "pocket springs" (home, product
descriptions, search results) now speak of the result: "laid by hand", "hand-built, natural
fibres only".

See AUDIT.md for the homepage audit and what competitors have that is still to add.

## 21. Search and AI search, before launch

This round follows the AI Search Audit, the AI SEO review and the Search Console export.
**SEO-ROLLOUT.md** has the full reading, the launch list, measurement and the decisions to
make. In the theme:

- **Product pages.** The heading says what the product is (*Vivaldi – Natural-fibre sleep
  system, handmade in Italy*). To change it, use *Product · The system → What it is*, or the
  product metafield `custom.kind`. The facts under the buttons are now the specification:
  made, dimensions, standard sizes (from a Size option), upholstery, comfort, height and
  lead time (metafields `custom.height`, `custom.lead_time`), service. Every bed has *Before
  you order*, seven questions marked up for search. In a question, `[product]` becomes
  the product's name. The question about price on request disappears when prices are
  shown, and a product whose sizes have different prices then shows "From €…".
- **Structured data.** Each product describes itself, with its fibres as materials. It gives
  a price only when prices are shown. The organisation now has its founding year, VAT
  number, award and map, under *Structured data* in the header. Turn off the structured
  data of Avada SEO and SEOon Blog in App embeds, or every page carries it twice.
- **Italian and Russian.** The home page's opening words and the product page's labels have
  their own translations in the theme. Everything else is translated in Translate &
  Adapt.
- **Our story** ends with Recognition & press, the Green Product Award first, linked to the
  award's page.
- **At a glance**: a new fact sheet (`page.facts`), in the footer under the house's
  pages. Every fact is a block you can edit.
- **Measurement.** *Conversion tracking* now records visits from AI assistants
  (`ms_ai_referral`) and adds `ai_source` to enquiries.
- **Journal tag pages** are now kept out of search results, as intended.
- **Discretion.** The last phrases that described the inside of the bed ("pocket by
  pocket", "each individual coil", "from the springs up") now speak of the core and the
  craft.

## 22. Feedback round: collections, map, notes, press

- **Icons collection.** The store's Icons collection lives at `/collections/icon`; the theme
  now recognises both spellings everywhere (tabs, numeral, header photograph, product pages).
- **Collection pages** open on the house's photographs (Essentials: the glass house; Icons:
  the arches; Signature keeps its own). The systems are listed under *What matters most to
  you?* (temperature, support, softness, breathability, hypoallergenic), with a line on which
  fibres answer each, and a *Compare* view that sets the systems side by side. Each system's
  fibres come from its own product template; the qualities are those of Natural materials.
- **Map**: see section 24 (the changes described here first only reached the theme there).
- **Notes** open with the title, summary and photograph on one screen; the text runs in a
  wider column beside *In this note* (made from the note's headings) and the share links.
  Numbered lists become numbered cards, two by two.
- **Press band** (home page) is still: one row of marks, the piece changing only when a mark
  is pointed at. It no longer appears on Our story.
- **Telegram and VK** show only on the Russian site (`/ru`); they stay in the structured data.
- **Newsletter**: "Letters from the atelier, in your inbox."
- **Fibre marks** have room inside the pills of *Inside the bed* and never lose a stroke.

## 23. Product pages, the bed and the sizes

- **Product pages opened the 404 page.** Shopify drops a section whose settings break its
  upload limits, and with it every template that uses it; for product pages that left no
  template at all, so Shopify showed the 404 page. The product section's new labels were
  longer than anything Shopify had accepted from this theme (up to 71 characters); they are
  now short, and `tools/validate.py` refuses any label over 55 characters from now on. If a
  product template ever comes through empty again, the layout still draws the product
  (photographs, name, description, enquiry), and in the theme editor names the template.
- **Fibre marks.** The horse, goat and yak are drawn whole, like the sheep, alpaca and camel,
  and all face the same way.
- **Inside the bed** sits on the house's salmon (#E8C7B7) instead of black: the topper
  quilted, the mattress tufted with its borders stitched and piped, the base upholstered on
  wooden feet, each piece shaded as cloth. Choosing a part still lifts it away.
- **Sizes** are drawn as made beds seen from above, to one scale: an upholstered headboard,
  soft pillows (one on a single), and a turned-down cover in the house's salmon.

## 24. The map, with real detail

- The map opens on **Europe**, around the atelier; World, Americas and Asia Pacific are one
  tap away.
- As you come closer, a **detailed map** fades in under the pins: cities, streets and place
  names from OpenStreetMap, toned to the house's sepia. Choosing a place in the list flies
  the map to street level. The drawn map stays for the world view, and stays in place if the
  detailed map cannot load.
- Sea and land are told apart, the projection never moves the pins, and a country drawn
  inside-out no longer floods the sea.
- **Map tiles.** *Agents & Resellers → Detailed map tiles* holds the tile address
  (`https://tile.openstreetmap.org/{z}/{x}/{y}.png`) and its credit. OpenStreetMap's tiles
  are free with the credit shown, for normal traffic. If the site grows busy, or you prefer
  a styled map, a provider such as MapTiler or Stadia gives an address with a key; paste it
  there and update the credit. Leave it empty to keep only the drawn map.

