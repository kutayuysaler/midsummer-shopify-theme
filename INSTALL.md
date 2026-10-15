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
  number, award and map, under *Structured data* in the header. The Avada SEO and SEOon
  Blog embeds come switched off (section 25), so no page carries its data twice.
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

## 25. Ready for launch

**SEO-ROLLOUT.md §3** is the launch checklist: what the theme already does, and the steps
left in Shopify, in order.

- **Prices stay on request**, as the house asked MOHD on 21 September. *Theme settings → Show
  a starting price while prices are hidden* adds "From €…" under "On request" (on product
  pages and collection cards) and gives search engines that starting price. It is off.
- **App embeds come preset**, as on the live theme. Turned on: Tipo Appointment, Appointo and
  Mailchimp. Turned off: Avada SEO Suite and SEOon Blog, whose structured data repeated the
  theme's.
- **Fibres**: every system's fibres now come from the house's catalogue (section 26).

## 26. Loro Piana Interiors, cloth by cloth, and every system's fibres

The sources are the 2026 catalogue (composition and fittings of every system), the price lists
of August 2026 (the cloth of every system), the Essenziale and First Dream sheets, Loro Piana
Interiors' 2026 trade list (article and composition) and the Loro Piana Interiors cards kept at
the atelier. Everything shown can also be edited in the theme editor.

- **The Loro Piana Interiors page** now shows the cloths our systems are actually made in, one
  after the other: Mystic River, Connemara, Altai, Wish, Cardi, Ely’s Harbour, Bangor and Shadan.
  Each one shows its article and composition, the systems it dresses, and its colours by name,
  with their numbers as on the cards:
  - Mystic River: 12 colours, photographed.
  - Connemara: 9 colours, from the card at the atelier.
  - Altai: 13 plain colours and 3 mélange, from the card at the atelier.

  Choose a colour and the large sample follows; *Ask about this colour* opens the enquiry with
  the cloth and the colour already written. The old palette, 39 unnamed cloths, is gone.
- **Wish, Cardi, Ely’s Harbour and Bangor** have no colour card in Drive or Dropbox, so they show
  *Colours at the atelier*. To add their colours, edit the page (*Loro Piana cloths* section):
  add **Colour** blocks right after the cloth, each with its name and number as on the card
  ("4 Zen"), its colour and, ideally, a photograph.
- **Every product page** says what that system is dressed in. Systems made in Loro Piana
  Interiors name the cloth, show its own colours and link to it on the Loro Piana Interiors
  page:
  - Capri, Dreamy, Roma, Topper Roma and Storage: Mystic River.
  - Brera: Connemara, edged in Altai.
  - Top: Connemara, Ely’s Harbour and Bangor.
  - Giotto Round: Connemara and Bangor.
  - Flora: Cardi (Loro Piana Interiors' Fiore di Cardo, A702050RS, 90% virgin wool, 10%
    cashmere) and Wish.
  - Bellini: Wish.
  - Paisley: Shadan and Katai silk.
  - Dreamy Springs and Vicuña: offered in it on request.

  The other systems name their natural cloth (cotton, linen and cotton, raw linen and cotton,
  viscose for My Dream) and say nothing about Loro Piana Interiors. This applies to the
  Upholstery line, the line under the name, *Before you order*, the cloth column and *Inside
  the bed*.
- **Fibres** follow the catalogue on every system. The biggest corrections:
  - **Monteverdi** is the house's fully plant-based mattress (vegetable horsehair, linen and
    Ingeo), not cashmere and camel hair.
  - **Topper Roma** is cashmere, mohair, silk, Falkland wool, linen and Ingeo, not yak.
  - **Vivaldi Plus** is cashmere and silk, without camel hair.
  - **Flora**'s cashmere is in its cloth; its padding is yak, horsehair, Cheviot wool, silk,
    linen and Orange Fiber.
- **Collections**: Signature and Icons are no longer described as "fully upholstered in Loro
  Piana Interiors". Several of their systems are covered in natural linen and cotton.

## 27. Calmer colours, each bed's own inside, the cloths at a glance, a quieter map

- **Inside the bed** sits on a muted clay-rose (from the house's salmon, quieter), with the
  small labels a shade deeper so they stay readable.
- **On every product page, Inside the bed now describes that system**:
  - The intro says whether it is a complete system, a mattress or a topper.
  - The topper, the mattress and the base each give their own fibres for winter and summer,
    their cloth, and what can be seen (ribbons, hand stitching, drawers, leather legs).
  - A mattress sold on its own shows the topper and the boxspring as what completes it.
  - Nothing of the build is named: no springs, no layers.

  All of it comes from the 2026 catalogue and the Models & Layers sheets, and can be edited
  per product template in the theme editor.
- **Collection pages**:
  - Vicuña's name shows correctly.
  - *What matters most to you?* now reads each system by its three defining fibres, so
    the filters tell the systems apart again.
  - The fibres shown are the catalogue's; the Models & Layers sheets (Raffaello, Vivaldi,
    Vivaldi Plus, Bellagio, Flora, Top, Vicuña) agree with it.
- **Loro Piana Interiors** shows one cloth at a time, so the eight cloths fit on one screen.
  A row of names on top chooses the cloth, and *Next* moves along. Links from product pages
  (`#mystic-river`, `#connemara` …) open the right cloth directly. Without script, every cloth
  shows, one after the other.
- **The map, zoomed in**, now uses CARTO's light *Positron* map (from OpenStreetMap) laid in
  grey on the house's cream, sharp on retina screens. The drawn map gives way entirely once
  the detailed one has arrived, so the two never blur together. CARTO's maps are free with
  the credit shown, up to 75,000 map views a month; another address can be set under
  *Agents & Resellers → Detailed map tiles*.


## 28. Site audit

Every template was rendered and checked at desktop (1440px) and phone (390px) widths for:
script errors, missing files, sideways scrolling, one H1 per page, images without text,
links and buttons without a name, structured data that does not parse, duplicate IDs,
in-page links to nothing, and Liquid or template text showing through. All 78 pages pass.
The theme check reports 0 errors, the strict Liquid parse 0 errors across 116 files, and the
111 interaction tests all pass.

The audit also read every page's words. What it changed:

- **No springs or layers in the words.** The FAQ, Story and home page said *the same two hands
  that open the spring core sew the final seam*; they now say *the same two hands that begin
  the bed sew its final seam*. *The depth of the spring architecture* (Collections) and *Every
  layer is reachable* (Regeneration, Sustainability) are gone. So are the Finder's Raffaello
  answer (*over a hand-sewn spring core*) and two defaults (an unused comparison table, the
  craft section's fallback text). *Dreamy Springs* stays: it is the product's name.
- **Signature is not all Loro Piana Interiors.** The menu's Signature line, the home page's
  Signature collection and the FAQ said Signature is made *in Loro Piana Interiors fabrics*.
  Several Signature systems are made in natural linen and cotton, so these now say *precious
  natural fibres, in natural linen or Loro Piana Interiors*, as the collection page already did.

Four templates cannot be rendered outside Shopify: the cart and the appointment product page
use Shopify's `content_for` tag, and `llms.txt` and `robots.txt` are text files. They are
Atelier's own and were not changed. Page titles and descriptions come from the layout, which
is checked through the theme check and the SEO tests rather than these renders.


## 29. Fibres up close, projects on a map, 15 + 15 to play with

### The world map, zoomed in
- The map is drawn by the theme itself; no outside map service is needed. The *Detailed map
  tiles* setting is optional and empty by default.
- The detail now comes from Natural Earth's 10m countries (world-atlas):
  - France and Norway were missing from the previous source, and showed as sea when zoomed in.
    They are back.
  - Coastlines and borders are ten times finer, with no more stepped edges.
- Lakes come from Natural Earth's 10m lakes: Como, Maggiore, Lugano, Garda, Iseo, Geneva and
  the rest.

### Natural materials: fibres up close
- The Natural materials page (and the materials collection template) has a new band,
  *Before it is a bed, it is this.* It holds photographs of the raw fibres from the Drive:
  - vicuña (twice),
  - yak, cashmere, wool and silk,
  - horsehair and cotton.
- Clicking a photograph opens it larger. A closing card notes, with the animals drawn, that
  none of them could make the photo shoot.
- The photographs ship with the theme (`ms-fibre-photo-*.jpg`, each in two sizes).
- Each card is a block. It can use a bundled photograph or any picture from Files, with its own
  name, place and line.
- Only close-ups of single fibres are used. Photographs that showed fibres side by side in a
  cross-section were left out on purpose.

### Projects, as postcards on a map
- The projects blog now shows as postcards on a drawn map of Italy, with one pin per place.
  - Hovering a postcard lights its pin; clicking a pin brings its postcard into view.
  - Three projects in Milano share one pin, marked 3.
- Which blogs show this way is set under *Theme settings → Midsummer · Where links go →
  Blogs shown as projects* (default: `projects, hotels, progetti, portfolio`). Every other
  blog shows the Journal as before.
- A project finds its place from its title or handle (Lucca, Brianza, Lierna, Meina, Milano …).
  - The map knows about fifty places in Italy.
  - For a place the title does not name, add a tag such as `place:Lucca`.
  - A project with no place still gets its postcard, without a pin.

### 15 + 15, to play with
- The regeneration page (and Sustainability) has *Thirty years, in one line*: a slider from
  year 0 to year 30.
  - The mattress drawing stays as it is, which is the point.
  - At year fifteen it leaves for Italy and sends a postcard home.
  - A tally counts one Midsummer against the industrial mattresses thrown away in the same time.
- The industrial lifespan defaults to 9 years. The page itself says eight to ten.
- The stages are blocks, each with its own year, title and text.

### At a glance, in figures
The facts page opens with six figures, all taken from the facts below them:

| Figure | What it counts |
| --- | --- |
| 2014 | the year the house was founded |
| 2 | artisans per bed |
| 12 | natural fibres |
| 15 + 15 | years |
| 8 | countries |
| 0 | tooling charges, not even for a round bed |

Each figure is a block. Plain numbers count up as they appear; the year stays still.

### Beds with headboards and Tangram
- The eight beds with headboards each show a drawing of that bed on their product page:
  Cashmere Couture, Silk Flowers, Soft to the Touch, Beating of Wings, Jungle Dreams, Tulip,
  Pure and Giotto.
- Their collection page lines the beds up side by side.
- The Tangram product page has a composer for its seats. The outdoor collection page shows it too.
- Each product's kind decides what its page shows. A kind is one of:
  - a system, a mattress, a topper or a boxspring,
  - a bed with headboard,
  - outdoor,
  - linen.

  The kind is read from the product's handle and type, so each page shows only what applies
  to that product.

### Collections
- The collections page lists every collection the store has, on two shelves:
  - beds by kind,
  - what completes the bedroom.
- A card appears only when its collection exists and holds products.
- The recommended structure in the admin is one collection per kind, plus the three lines:
  - **Beds:** Bed systems (`designer-beds`), Beds with headboards (`beds-with-headboards`),
    Mattresses (`mattresses`), Toppers (`mattress-toppers`), Outdoor (`outdoor-1`).
  - **The bedroom:** Duvets and sheets (`duvets`), Blankets and throws
    (`gallery-blankets-and-throws`), Cushions and screens (`cushions-and-screens`), Furniture
    (`gallery-furniture`), Lamps (`gallery-lamps`), Wallcoverings (`wallcovering-and-fabrics`),
    Treasures (`midsummer-treasures`).
  - **Lines:** Essentials, Signature and Icons, as before.

  Each product sits in one kind and one line.

### Journal
- Every note finds its subject by itself:
  - Sleep, Materials, Craft, The bedroom, Italian living, Sustainability, Projects, or
    News & press.
  - The note's title, tags and opening lines are read, and the strongest subject wins. Notes
    written in future are filed the same way.
  - Tested against the store's 279 notes.
- A tag always decides when added: `cat:sleep`, `cat:materials` and so on, or the subject's name.
- On a note's page:
  - Paragraphs are evenly spaced, even where the editor left empty lines or stray breaks.
  - Reading time is counted from the text.
  - The share row has an icon beside each name, and *Copy link* keeps its icon after copying.

### Instagram, latest posts
The Follow section can show the account's latest posts in either of two ways.

**With a token**
1. In Meta for Developers, create an app with *Instagram API with Instagram Login*.
2. Generate a long-lived token for the Midsummer account.
3. Paste it under *Theme settings → Midsummer · Social and WhatsApp → Instagram access token*.

The theme asks Instagram to extend the token about once a week when the page is visited. If
the posts ever stop appearing, paste a fresh token.

**Security note:** the token is visible in the page's source to anyone who looks. It is
read-only: it can show the account's public posts, and cannot post or change anything. If
that is not acceptable, use an app instead.

**With an app**
1. Install an Instagram feed app.
2. Add its app block to the Follow section.

Without either, the section shows the photographs chosen in it, as before.

### Made by hand in Italy, not in Milan
- The artisans do not work in Milan. Every place that said the beds are made, or built, in Milan
  or at the Milan atelier now says *made by hand in Italy*.
- This covers sections, templates, the share and search descriptions, and the translation
  files.
- The atelier on Via Andegari is where the beds are shown, tried and specified, and the copy
  says so.

### Smaller things
- **Product size drawing:** it no longer jumps between sizes. The bed eases from one size to
  the next in a fixed frame.
- **Inside the bed:** each system's drawing is its own (23 systems), from the catalogue. Nothing
  of the build is shown.
- **Fibre marks and icons:** they draw at full size everywhere, with nothing clipped.

### Checks

| Check | Result |
| --- | --- |
| Theme check | 0 errors, 0 warnings |
| Strict Liquid parse | 0 errors, 130 files |
| Page audit | all 78 pages pass |
| Interaction tests | 120 pass, 9 of them new |

The page audit covers script errors, missing files, sideways scrolling and one H1 per page.
The new interaction tests cover the fibre photographs, the projects map, the 15 + 15 slider and
the figures. The parser now accepts `{% render block %}`, Shopify's own tag for app blocks.

## 30. A map that works again, clearer collections, quieter charts, sharper drawings and icons

### Agents and resellers: the map works again
- **Cause:** the map redrew its full detailed outline (about 1.6 MB of paths) on every zoom and
  resize. On most machines this froze the page.
- **Fix:** it now draws only what is in view, simplified for the current zoom. It uses three
  levels of detail:
  - The world at a glance.
  - A middle level from `ms-world-mid.json`, which is new and ships with the theme.
  - The fine level (`ms-world-detail.json`), loaded only when zoomed close.
- While zooming, the last drawing is scaled. It is redrawn crisply once the zoom settles.
- The map bundle (`ms-atlas-vendor.js`) was rebuilt. It now includes the bounds function the
  view clipping needs.

### Journal notes read properly
- Notes pasted from other editors arrive wrapped in extra boxes, bold blocks and line breaks.
  The theme now unwraps them when the note is shown, without touching the note itself.
- Lines that begin with a bold word, such as *Tuesday* or *The sheets*, become a tidy list with
  the word set apart.
- Headings get room above them.
- The sign-off is set in italics and to the right.
- A link that stands alone at the end becomes an invitation link, not a bare line.

### Collections: what each piece is, at a glance
- Every card says what the product is: *Bed system*, *Mattress*, *Topper*, *Boxspring*,
  *Headboard* or *Outdoor*. Each has its own small drawn mark.
- Bed systems also say what they include, for example *Topper, mattress and boxspring*. On the
  *All* page they also show their tier.
- Cards are larger: three to a row on desktop, two on tablets and phones.
- When a collection holds more than one kind, a row of filters (*All*, *Bed systems*,
  *Mattresses*, …) sits above the grid. It works together with the existing *needs* filter.
- The labels can be changed in the section settings.

### Natural materials: the fibres, as specimens
- The photo band is replaced by a specimen viewer:
  - On the left is an index of the seven fibres, each with its Latin name.
  - On the right is one large square plate, with its caption.
  - Hovering, clicking or using the arrow keys moves through the fibres.
  - On phones, the index scrolls sideways above the plate.
- The seven photographs are recropped square around the fibre itself: vicuña, yak, cashmere,
  wool, silk, horsehair and cotton.
- Each fibre is a block (photograph, name, Latin name, origin, line). Any picture from Files
  can replace a bundled one.
- The closing card with the animals is gone.

### Thirty years, instead of 15 + 15
- The slider is replaced by a calm, drawn chart on one line of thirty years:
  - An industrial mattress, replaced every few years. The section setting defaults to nine, so
    that is four mattresses.
  - One Midsummer mattress, marked at year fifteen: *renewed by hand in Italy*.
- The bars draw themselves once, as the chart comes into view. With reduced motion they are
  simply there.
- The note under the chart says it is an illustration, not a forecast.
- The Hospitality page has the same chart, written for hotels.

### Inside the bed: refined drawings
- The drawings are redrawn with soft shading, rounded edges and finer cloth patterns. Giotto,
  Paisley and the round systems especially are much improved.
- **Giotto:** drawn round, with its gold ribbon and linen base.
- **Paisley:** ivory with its red ribbon over a red paisley base.
- The section background takes a faint tint from each system's own colour. The tint is never
  stronger than a shade of the usual ivory.
- The cards use the product's own photographs when the section has none chosen.
- Nothing of the build is shown.

### Icons
- **Fibre marks:** redrawn as filled silhouettes on one grid. They cover sheep, goat, camelid,
  camel, yak, horse, silkworm cocoon, flax, cotton, palm, corn, orange, hemp and thread.
- **Social icons:** Instagram, Pinterest, LinkedIn, WhatsApp and Telegram are redrawn as fine
  lines.
- **Sustainability icons:** redrawn, including the needle and the seam.
- **Collection kinds:** each kind has a new mark.

### Architects, Hospitality and the Milan atelier
- **Architects & Interior Designers:**
  - A specification drawing shows plan and elevation, with tabs for rectangular, round and
    split bases, and the facts beside it.
  - *A project, step by step* sets five steps from the drawing to the dressed bed on one line.
- **Hospitality & Contract:**
  - The specification drawing, written for hotels.
  - The *Thirty years* chart.
- **The Milan atelier:**
  - An hours plate shows the address, and whether the atelier is open now in Milan time.
  - It has links to book a visit and for directions.
  - A week timetable sets today in italics and marks the hour.
- **Wording:** pages that said the atelier makes or rebuilds the beds now say the beds are made
  and renewed by our artisans in Italy. The atelier is where they are seen, specified and lain
  on.

### Checks

| Check | Result |
| --- | --- |
| Theme check | 0 errors, 0 warnings |
| Strict Liquid parse | 0 errors, 136 files |
| Page audit | all 78 pages pass |
| Interaction tests | 124 pass |

New and updated tests cover:
- the fibre viewer;
- the thirty-year chart;
- collection kinds and the kind filter;
- the size of the map drawing;
- journal unwrapping;
- the specification drawing and steps;
- the atelier hours.

## 31. Two upload failures fixed: the bed drawing and the agents page

Both problems came from Shopify refusing a file when the theme was uploaded. A refused file is
simply missing from the store afterwards.

- **Inside the bed showed "Could not find asset snippets/ms-craft-svg.liquid".**
  - **Cause:** Shopify refuses any Liquid file over 256 KB. The drawings of all 24 systems,
    kept in one file, came to 275 KB.
  - **Fix:** each system now has its own small file (`ms-craft-svg-<system>.liquid`, about
    12 KB each). `ms-craft-svg.liquid` only picks the right one.
- **Agents & Resellers opened the 404 page.**
  - **Cause:** the map section had a text setting (*Detailed map tiles*) with an empty
    default, and Shopify refused the section for it.
  - When Shopify refuses a section, it also refuses every template that uses that section.
    All three of the agents page's templates did, so the page was left with no template at
    all, and Shopify showed the 404 page.
  - The default page template also holds the map, so it was refused too. Any page relying
    on it would also have opened the 404 page.
  - **Fix:** the setting has no default now. It is still optional and empty.
- **Hidden pages:** the agents link (and every other link to a page) now skips a page that
  is hidden in admin. The address of a hidden page is a 404 for visitors, so the link opens
  the designed page instead.
- **Headboard lineup:** a drawing call passed a filtered value straight into `render`, which
  Shopify's parser rejects. The value is now prepared first.

### Checks added to `tools/validate.py`, so this cannot happen again
- **File sizes:** Liquid files 256 KB, JSON templates 512 KB, settings and locales 1.5 MB.
- **Empty defaults:** none on text settings.
- **Missing files:** every `render`, `include` and `section` points to a file that exists,
  and every `asset_url` points to a file in `assets/`.

Run against the previous zip, the validator now reports both problems. Against this one, it
reports none.

### Checks

| Check | Result |
| --- | --- |
| Theme check | 0 errors (63 advisory warnings: remote images, settings counts) |
| Strict Liquid parse | 0 errors, 442 files |
| Page audit | all 78 pages pass |
| Interaction tests | 124 pass |

After uploading, check the list Shopify shows when the upload finishes. It should name no
files.

## 32. Natural materials: new photographs

The design of the fibre section stays the same. The phone close-ups are replaced by licensed
photographs from the company's own library, one for each fibre at its source:

| Plate | Photograph | Source |
| --- | --- | --- |
| 01 Vicuña | Four vicuñas on a ridge at dusk | Shutterstock 109093589 |
| 02 Yak | A yak on a misty mountainside | Unsplash, Toomas Tartes |
| 03 Cashmere | A herd of goats coming down a mountain valley | Shutterstock 535793413 |
| 04 Wool | Sheep in full fleece, close together | Shutterstock 104115377 |
| 05 Silk | Silk satin, falling in soft folds | Shutterstock (texture "seta") |
| 06 Horsehair | The long, pale mane of a horse | Shutterstock 356083304 |
| 07 Cotton | Cotton bolls opening on the plant | Shutterstock 127061399 |

- **Where the photographs came from:**
  - The Shutterstock images are from the brand's own *SHUTTERSTOCK* folder, which was
    already used for catalogues.
  - The yak is from the *materiale per newsletter* folder.
- **How they are prepared:**
  - Each is cropped square around its subject.
  - All seven are toned alike, in a warm monochrome taken from the site's ivory and walnut, so
    they read as one series of plates.
  - Each comes in two sizes, 1400 and 720 px.
  - The script is `scripts/fibre_plates.py`.
- **Section text:** the heading is now *Where each fibre begins.* and each plate has its own
  alt text.
- **Silk:** no photograph of silk cocoons was found in the Drive or Dropbox, so the silk plate
  shows the cloth. Any picture can replace it from the section's *Silk* block, using *Or a picture from the store*.

## 33. One navigation for the beds, the toppers told apart, a fibre atlas, finer bed drawings, a real atlas when the map zooms in

### Collection navigation

- **The same navigation on every collection page.** Every collection page now carries one bar,
  just under its opening photograph, in two rows:
  - *By kind:* Bed systems, With headboards, Mattresses, Toppers, Outdoor.
  - *By collection:* Essentials I, Signature II, Icons III.
- **How it behaves:**
  - The page you are on is underlined, so from Toppers you can go straight on to Mattresses or to
    Signature.
  - A kind the store has no collection for is left out.
  - On a phone each row scrolls sideways. The current item is brought into view, and a row that
    continues fades at its edge.
  - The section is *Collection · Navigation*, and every label in it is editable.
- **The mega menu ("Our beds")** follows the same structure, in three groups: *By kind*, *For the
  bedroom* and *Choosing* (compare the collections, Find your Midsummer, request a proposal).
- **The Outdoor page** no longer shows a lone small card. With one piece in a collection, that
  piece is shown large, photograph beside its words. A collection without a description no
  longer leaves an empty column beside its figures.

### Specifications and materials, checked against the 2026 catalogue

`scripts/spec_audit.py` compares every system's fibres with the catalogue's composition pages. It
now reports **0 differences**. Corrections made this round:

- **Bellini, Vicuña and Roma:** Ingeo added where the catalogue lists it.
- **The toppers:** the store gives the *Medium & High Topper* and the *Thin Topper* the Roma
  topper's template, so all three showed Roma's fibres ("Cashmere, Mohair, Silk, Falkland Wool,
  Linen, Ingeo"). Each now shows its own data, taken from the catalogue's toppers page:

  | Product | Fibres | Specification |
  | --- | --- | --- |
  | Medium & High Topper | Silk, wool, linen, Ingeo; the high one also in vicuña, the medium one also in wool and horsehair | High 9–10 cm, soft; medium 5 cm, soft. Can be upholstered in Loro Piana Interiors linen and cotton, or cashmere |
  | Thin Topper | Silk and Ingeo, or wool and Ingeo | 3 cm, medium to firm |
  | Roma Topper | Winter: cashmere, silk, mohair, Falkland wool. Summer: silk, linen, Ingeo, Falkland wool | Sizes as before; the wrong "Headboard height 110 cm" line is removed |

  - **How it works:** the theme recognises the two by name (thin, high or medium; also sottile,
    alto, medio). Their product page, Inside the bed, questions and compare table then use their
    own data, even on the Roma template.
  - **Optional:** two templates now exist, `product.topper-high` and `product.topper-thin`. You
    can assign them in admin (Products → the topper → Theme template). Nothing breaks if you don't.
- **The lines under the topper names** were also corrected. The Thin Topper no longer says
  "wool and cotton".

### Natural materials: one atlas

The photograph gallery and the cards below it (which the reader could not connect) are replaced
by one section, *Fibres · Atlas*.

- **On the left:** the fourteen fibres in our beds, *From animals* and *From plants*, each with its
  qualities.
  - *What matters most to you?* (Temperature, Support, Softness, Breathability, Hypoallergenic)
    keeps the fibres that answer it lit.
- **Choosing a fibre opens it beside the list:**
  - Its plate: the photograph at its source where we have one (seven of them). Every fibre also
    has its own drawing *under the glass*: wool's crimp, linen's nodes, cotton's twist, silk's
    paired filament, the scales of the animal hairs. A small lens on the photograph switches
    between the two.
  - What it does, in the catalogue's own words (*Materials to dream of*).
  - Its figures, all from the catalogue: vicuña 12 µm against cashmere's 15 µm, 150 g every two
    years, 14 animals for one mattress; 800–1,000 m of silk from one cocoon; linen takes up 20 %
    of its weight; and so on.
  - Its origin and species, set small and upright.
  - *In our beds:* the store's own products made with it, as links. These are found
    automatically from each product's template.
- **On a phone** the list opens in place.
- **Links:** `#fibre-cashmere` (or any fibre) in a link opens that fibre. The fibre names on every
  product page now link to their own entry.
- **The Latin names** are no longer in large italics; they sit in the detail, small.

### Inside the bed

- **The drawing:** each system's drawing is now drawn as a fine technical illustration. The cloth
  colours are softer washes, the edges are hairlines, and the pulsing dots are gone.
- **Labels:** each part has a leader line to its numeral and name.
- **Animation:**
  - The bed is shown whole until the section comes into view, then opens gently into its three
    parts. The base settles first, then the mattress, then the topper, and the labels draw in.
  - Each part casts a soft shadow on the one below.
  - Hovering a part lifts it a little while the others step back.
  - The parts move very slightly with the cursor, at their own depths.
- Nothing of the inside or the build is drawn.

### The agents map, close up

Zoomed in, the map used to be a flat field covered in tiny village names. It now draws what a
printed atlas shows of a region, from Natural Earth 1:10m (public domain, no third-party map
service):

- the sea's depth contours
- built-up areas
- motorways, as a white line with a fine edge, and main roads
- railways
- regional boundaries
- rivers and lakes
- the mountain ranges, named in spaced italics

Other changes:

- **Labels:** far fewer names, set larger. The big cities are named first, a few towns only when
  you are close, and never the villages.
- **Colours:** ivory land on a cool, quiet sea.
- **Zoom:** the closest zoom now stops where this detail still holds. Places in the same street
  are listed when you click their number.
- **Loading:** the detail lives in `assets/ms-world-layers.json` (3.6 MB, about 1.1 MB as sent).
  It loads only when a visitor zooms into a region.

## 34. A full review: every page checked on a desktop and a phone, and refined

Every template (43 pages) was reviewed at desktop width (1440 px) and phone width (390 px). These
are the changes that came out of the review.

### Words and photographs

- **The Loro Piana Interiors page:** the second photograph of the pair is now the red Paisley bed.
  Its caption reads "Paisley: Katai, a pure silk, on the base and the border of the mattress."
  The old caption described a headboard the photograph did not show.
- **The Salone 2026 page:** the first photograph is now the Paisley bed that its caption
  ("Paisley, in Loro Piana Interiors Shadan.") describes. Before, the caption sat under a general
  view of the atelier.
- **Every list of fibres now names all 14:** baby alpaca, camel hair, Cheviot and Falkland wool,
  horsehair, vegetable horsehair, yak hair, mohair, cashmere, silk, linen, organic cotton, Ingeo
  and Orange Fiber, with vicuña in the Icons collection. Camel hair, Falkland wool and Ingeo were
  missing before. The lists appear on the Facts, FAQ and Sustainability pages. The Facts figure
  changed from 12 to 14, to match the fibre atlas.
- **The opening line on a product page:**
  - When a product's description has paragraphs or line breaks, the opening line no longer runs
    words together (as in "silk.The").
  - The same fix applies to the search-engine description and the product's structured data.
  - A headboard with no subtitle now opens on its own line from the bed data, for example "A
    headboard of padded folds, parted by a band of pure silk.", instead of the start of its
    description.

### The materials page on the default template

If the Natural materials page uses the store's default page template rather than
`page.natural-materials`, it now shows the fibre atlas too, in place of the old gallery. The atlas
appears only on the materials page, so other pages on the default template are unchanged.

### Layout

- **The journal band** (articles at the foot of a page):
  - Three equal columns on a desktop, two on a tablet and one on a phone.
  - When there is only one article, it is shown large, with the photograph beside its words,
    instead of a lone small card.
- **The collections index:** a collection with no image of its own now shows a house photograph
  that fits its kind, so no card is left blank. Bed systems show the atelier, headboards the
  fresco bed, mattresses a mattress detail, toppers the tufting, bedding the linen sheets, and so
  on.
- **The headboard line-up:** on a wide screen, up to ten headboards now sit in one row instead of
  wrapping to a second row with one or two left over.
- **The process steps:** the steps not yet reached are easier to read, at 72% strength instead of
  55%.
- **The contact block:** the email address stays on one line and scales with the screen instead
  of breaking.
- **Page text:** headings inside a page's body text have space below them, as well as above.

### On a phone

- **The craft drawing:** on a phone the parts' names give way to their numerals, and the drawing
  now widens to fill the room they leave instead of sitting small in the middle.
- **The footer:** the social icons are a little smaller (35 px) and closer together, so they stay
  on one row.

### Checks

- **Theme Check:** 0 errors.
- **Strict Liquid parse:** 449 files, 0 errors.
- **Render audit:** 78 pages, 0 render errors, 0 missing assets.
- **Interaction tests:** 133 passed, 0 failed.


## 35. Round 14: Inside the bed as each bed is made, the materials under the glass, a street map, the journal by subject, the audits

**About the preview.** The preview link (`…shopifypreview.com`) could not be opened from the
environment this work runs in, because its network policy blocks that host. Every check below
was therefore made on local renders of this theme. Those renders used the store's own product
texts (the export of 14 August 2025), its 279 journal notes and its press blogs. The street
map's tiles (OpenFreeMap) and Instagram could not be reached either, so test both on the store
once the theme is published (see the checklist at the end).

### Inside the bed

- **A topper, a mattress or a boxspring page shows that part alone.**
  - The parts it does not include are drawn in outline and marked *Not included*.
  - Each of those parts leads onward: first to its own companions on the store (the Roma topper
    to the Roma mattress, a boxspring to its mattress), then to the collection of that kind
    (*All toppers*, *All mattresses*, *All boxsprings*).
  - A badge says which part this product is.
  - Each part shows its winter face and its summer face side by side.
  - A caption under the drawing names the product.
- **The boxspring is called the boxspring everywhere,** in the drawing, the buttons, the panels
  and the captions. The word "base" is gone from what a visitor reads.
- **The systems are drawn as the 2026 catalogue makes them:**
  - **Capri and Giotto Round** come in two parts: the topper, and one piece that is the mattress
    and the boxspring together. They are drawn as one block with a single seam, with the topper
    lifting off it, and the heading reads "Two parts, made as one."
  - **Brera** also comes in two parts: one slim piece that is mattress and topper at once, on its
    17 cm boxspring with leather legs.
  - **Storage and Amalfi** take a topper only if you wish. Their topper is drawn in outline,
    marked *Optional*, and leads to the toppers.
  - The other systems are unchanged: a topper, a mattress and a boxspring.
- **Wording you asked for:**
  - The topper no longer says "A removable covering in Loro Piana Interiors, embroidered on
    request."
  - The boxspring is "upholstered for your room in Loro Piana Interiors or in other natural
    fabrics, and made to carry your mattress and topper for many years."
  - "Without tooling charges" is gone.
  - The line about storage, slim and round boxsprings now names the systems and links to them:
    "with drawers beneath, as in Storage; slim, on leather legs, as in Brera; or round, as in
    Giotto Round."
- **New photographs on the home page cards:** the mattress card shows Flora's mattress from the
  side, and the boxspring card shows Flora's Wish bouclé boxspring. The boxspring card used to
  show a throw.
- **New settings in the section:**
  - *Heading on a system in two parts*
  - *Part III, when mattress and boxspring are one piece*
  - *Part II, when mattress and topper are one piece*
  - *An optional part*, and its badge
  - The captions for a two-part system and for a system with an optional topper

### Natural materials

- **Under the glass now works.** Each fibre's plate has three views:
  - the photograph;
  - **Under the glass**, the fibre as a microscope shows it, with a dark eyepiece around it;
  - **Its origin**, a pin on a dotted world map.

  Click or tap the glass to look closer. It zooms in 2.4 times, at the point you chose. Each
  fibre has a short line on what to look for, such as the scales on wool or the hollow core of
  camel hair.
- **The drawings are lit as under a microscope.** The strands behind are softly out of focus,
  and the light falls along each fibre. Each fibre has its own colour.
- **In our beds** lists the beds made with each fibre, as cards with a photograph, a name and
  what each one is (system, mattress or topper).
- **Two origins corrected:** wool now reads "Scotland and the Falkland Islands", and Orange
  Fiber reads "Sicily".

### The Loro Piana Interiors page

- **The header** is now Flora: the Cardi topper over the Wish bouclé boxspring. It used to be a
  paisley throw.
- **Cardi and Wish** now each show a close-up of Flora, captioned "On the Flora topper" and
  "On the Flora boxspring". Shadan's photograph is captioned "On the Paisley topper". These
  captions come from a new block setting, *Photograph caption*.
- **The cloths and colours** were checked against the cards: Mystic River 12, Connemara 9 and
  Altai 16, with the systems each cloth dresses.

### The stockists map

- **A real street map** (MapLibre, with OpenFreeMap's tiles) now shows each store at street
  level:
  - zoom it with the buttons, the wheel or a pinch;
  - choose a store in the list and the map flies to it;
  - stores close together gather into a numbered cluster that opens when clicked.
- **Its colours** come from the house palette: paper land, a pale sea, and white roads with a
  warm edge. Place names follow the visitor's language.
- **If the tiles cannot load,** the drawn map from before takes over by itself within a few
  seconds.
- **The setting** is *Street map* (on by default). The map is credited to OpenFreeMap,
  OpenMapTiles and OpenStreetMap, as their licences require.

### The journal, by subject

- **Each subject has its own page:** Sleep, Materials, Craft, The bedroom, Italian living,
  Sustainability, Projects, and News & press.
  - Every note is sorted into a subject automatically, from its title and words.
  - A subject page lists every note of that subject across the journal, with a heading and a
    count.
- **The addresses** are `/blogs/<journal>?view=sleep`, `?view=materials` and so on. The theme's
  menus and notes use them, and old `?cat=` links still lead to the right page.
- **Each subject page has its own title and description** for search engines.

### Product pages

- **A way back at the top:** it leads to the collection the visitor came from, or else to that
  kind of product (Mattresses, Toppers, Boxsprings, Headboards, Outdoor).
- **Every description is put in order,** whatever shape it has in admin:
  - an opening quotation becomes an epigraph with its author;
  - the first paragraph becomes a lead;
  - headings stay headings;
  - sizes, heights, composition and finishings move into the list of facts at the top of the
    page;
  - the delivery small print becomes a short "Made to order" note.
- **Tidy wording:** sizes read "160 × 220" and "4 cm", and "Midsummer-Milano" reads "Midsummer
  Milano". A "Click here" link reads "More at" and its address, for example "More at
  michelanicoli.com".
- **Keep the build private in descriptions** (a new setting, on by default). Any sentence that
  names springs, layers or the core is left out of the description shown. So is any list under
  a heading of that kind. The words are still in the page source and the product feed, so
  **DESCRIPTIONS.md** lists, product by product, what to edit in admin.
- **The line under the name:**
  - When a product has no subtitle, the line is the first sentence of its description, and the
    description below no longer repeats it.
  - The boxsprings have lines of their own: Top Dream, Dreamy Springs, My Dream, First Dream and
    Storage.
  - A plaid that shares a system's name (the mohair "Capri" and "Roma") no longer takes that
    system's line.
- **Sizes** are translated in Italian and Russian.
- **A product shown without a price** is described to search engines as a thing, not as a
  product with an offer. The theme setting *Search engines, while prices are on request*
  (under Enquiry-led commerce) lets you change this.

### Across the site

- **A gentle tone on the photographs:** a little warmth and a little less saturation, so that
  photographs from different shoots sit together. The tone does not touch logos, drawings,
  swatches or the map. Its settings are under **Midsummer · Photographs** (on, strength 40).
- **On a phone:**
  - the Tangram section shows only on the outdoor collection;
  - the fibre marks on collection pages are smaller.
- **The artisan on the home page** is now a Midsummer artisan working fibre by hand, from the
  *Foto artigiani* folder. The stock photograph of a seamstress is gone from the home page, the
  menu and the Handmade in Italy page.
- **The questions page** has the topics as an index beside the answers. The index follows you
  down the page, and *Not here?* sits beneath it. The opening no longer talks about search
  engines.
- **Care of the cloth:** "Loro Piana Interiors upholstery is removable: clean it as its care
  label directs, and ask the atelier whenever in doubt."
- **The architects and hotels pages** have a new table, *Systems, measured*: each system's
  collection, overall height, standard sizes and cloth, from the 2026 catalogue, with a link to
  each system's page.
- **The Instagram row** shows house photographs that link to the profile: the artisan, Flora,
  the fresco bed, the parrots room and the shepherd. The latest posts appear only with a token
  or an app (see the checklist).

### The two website audits, theme side

- **Literal claims, softened.** Each of these now says something that is plainly true:
  - "two hands" and "two artisans" now read "by hand in Italy";
  - "24 systems" now reads "three collections";
  - "no tooling charge" is gone everywhere, round beds included;
  - "the base, for thirty years" now reads "for many years";
  - "natural fibres only" now reads "natural fibres";
  - "nothing synthetic" now reads "Made to order, by hand in Italy";
  - "no tooling to amortise" now reads "no production line".
- **The press strip:**
  - it shows only publications with a piece to read, most recent first, eight at most;
  - "L'Officiel", "Festival dell'Etica" and "Lust & Leben" are spelt as those publications spell
    them;
  - "Midsummer-Milano" in a press title reads "Midsummer Milano";
  - the year shown is the one the piece's title names (Kommersant 2025), or otherwise the year
    it was published;
  - the Green Product Award leads the strip.
- **Titles and descriptions:**
  - each press blog, the projects blog and the journal has its own description;
  - "&amp;" no longer shows double-encoded;
  - the contact page no longer reads "Please proceed with your enquiry";
  - the brand is one name, Midsummer Milano, in titles, share cards and structured data;
  - the Icons collection is named "Icons".
- **Alt text:** photographs that had none now describe what they show.

### Checks

- **Theme Check:** 0 errors.
- **Strict Liquid parse:** 461 files, 0 errors.
- **Render audit:** 78 pages, no issues. The cart, the appointment product page, `llms.txt` and
  `robots.txt` cannot be rendered outside Shopify.
- **Interaction tests:** 149 passed, 0 failed. New tests cover:
  - the description structure, and the build kept private;
  - the two-part and optional-topper systems;
  - the questions index;
  - the materials views;
  - the street map;
  - the journal subjects.
- **The natural materials of every product** were compared with the 2026 catalogue, system by
  system and part by part, with 0 differences.

### Owner checklist (admin, not the theme)

1. **Prices.**
   - The Essenziale prices are broken, and some products carry placeholder prices of €12,200.
     Correct them, or set them to 0 for "on request".
   - Shopify publishes variant prices in `/products.json` and in each product's `.js` address,
     whatever the theme does. A price that must stay private should not be entered.
2. **Product descriptions:** see **DESCRIPTIONS.md**.
   - It lists the sentences that name the build (37 products), as hidden by the theme.
   - It also lists "Midsummer-Milano" spellings, a "Click here" link and two placeholder
     products (`test-product`, `langify_image_container`).
   - Amalfi's description says eight colours; the catalogue says four.
   - My Dream boxspring and Caravaggio name polyurethane. Please confirm what is inside.
3. **Product types:** use one list across the catalogue: Bed system, Mattress, Topper,
   Boxspring, Bed with headboard, Outdoor, Throw, Bed linen, Furniture, Perfume.
4. **Handles.** Rename these with a redirect (Online Store → Navigation → URL redirects):
   - `icon` to `icons`;
   - `camelia` (the product is spelt "Camelie" elsewhere);
   - `silk-fowers` to `silk-flowers`;
   - `outdoor-1` to `outdoor`.

   The handle `roma` was the Roma mohair plaid in August 2025; the Roma bed is `mystic-river`.
   The theme tells the two apart.
5. **Pages that 404:** Paisley and Tangram Air. Publish the products, or remove the links that
   lead to them.
6. **Press blogs:**
   - Robb Report has no article: add one, or the strip simply leaves it out.
   - The Elle Decor blog also holds Elle Decoration pieces; rename it or split it if you want
     them told apart.
   - AD Magazine and Architectural Digest are two blogs, so they show as two marks.
   - Kommersant's article is dated 2026 for a 2025 piece. The strip shows 2025; correct the
     date in admin.
7. **Italian and Russian:** in Translate & Adapt, translate the product titles, the SEO titles
   and descriptions, and the subtitle metafield.
8. **At launch:**
   - Check Settings → Customer events for the pixel that returns 404.
   - Remove the password page, so the store is no longer noindex.
9. **Instagram:** the row can show the latest posts in either of two ways:
   - paste a token from the Instagram API with Instagram Login in Theme settings →
     Midsummer · Social and WhatsApp;
   - or add an Instagram feed app's block to the section.
10. **The street map:** once the theme is live, open the stockists page and zoom in.
    - If the tiles do not appear, turn off *Street map* in the section; the drawn map returns.
    - The tiles and fonts come from `tiles.openfreemap.org`.
11. **The softened claims (see the audits above):** if any of the original figures can be
    sourced, it can be restored in the editor.

## 36. Round 15 (urgent): the homepage and product pages

**What happened:** on the Round 14 theme, the homepage and every product page showed the
theme's own 404 page ("This page is no longer here."). Shopify shows that page when it has no
template for the address. So `templates/index.json` and the product templates were missing from
the uploaded theme.

**The likely cause:** the one section all of those templates share is *Inside the bed*
(`sections/ms-craft.liquid`).
- In Round 14 it grew from 40 settings to 72.
- Shopify's own checker gives 40 as the maximum for a section.
- When Shopify refuses a section, every template that uses it is refused with it.

**The fix:**
- *Inside the bed* is back to the 40 settings of the last version that uploaded.
- The new wording (the headings for a mattress, a topper or a boxspring alone, the captions,
  *Optional*, *Not included*, *All toppers* …) now sits in the section's code.
- The fibres for each face come from `snippets/ms-sys-data`.
- The page looks exactly as before. Both versions were rendered with Shopify's own Liquid engine
  and compared: the output is the same.

**Checks run on this build:**
- Shopify's Liquid engine (Ruby, with `strict2` parsing): every section, snippet and layout file
  parses.
- That engine renders the homepage and every product template, with and without a product,
  including toppers, mattresses and boxsprings, with no errors.
- Theme Check: 0 errors.

**After uploading, please check:**
1. When the upload finishes, Shopify lists any files it could not take. It should list none.
2. In *Edit code*, `templates/index.json` and `templates/product.json` should both be there.
3. If the homepage still shows the 404 page, open *Customize*. The editor names the template
   or section it cannot load. Send me that message.

**Also in this build:**
- **Product cards:** one photograph per product. The second photograph on hover is gone,
  including on the store's own cards (Theme settings, *Show second image on hover*: off).
- **The homepage film on a phone:** the whole frame is shown under the header, with the words
  and the appointment button beneath it. The tall crop that showed only a blur is gone.

## 37. Round 15: the rest of the requests

### Natural materials: every fibre has its plate

The seven fibres that showed only their drawing now have a photograph at the source, toned like
the first seven (`scripts/fibre_plates.py`). All come from the brand's Drive:

| Fibre | Photograph | Source |
| --- | --- | --- |
| Camel hair | A Bactrian camel crossing the snow | Shutterstock 390845494 |
| Baby alpaca | The fleece, close up | the brand's ALPACA_BEIGE photograph |
| Mohair | Tufts of mohair on a sample card | *MOhair colors* |
| Linen | Linen cloth in soft folds | Shutterstock, *lino* (_TEXTURE folder) |
| Vegetable horsehair | The fan-shaped leaves of a palm | Unsplash, Nika Akin (_VEGETAZIONE folder) |
| Ingeo | A tuft of maize fibre with cotton | the brand's fibre close-up *cotone + fibra mais* |
| Orange Fiber | Oranges under a Top mattress | the brand's *Top_arance* |

Vegetable horsehair comes from palm leaves, so the plate shows a palm. The coconut-fibre
close-up in the Drive is a different fibre and is not used.

### Loro Piana Interiors

- **Wish:** the Flora boxspring corner is replaced by the official Wish bouclé swatch, in ivory,
  from the Drive (1200 px).
- **Each colour now looks like cloth:**
  - Altai and Connemara are shown on a photographed weave: an atelier photograph of a linen
    plain weave for Connemara, and a fine wool and cashmere nap for Altai.
  - Each is tinted with the colour measured on the Loro Piana card and lit softly.
  - The chips are 240 px and the large view 1000 px. The script is `scripts/cloth_render.py`.
  - The footnote says so.
- **Ely's Harbour and Bangor:** their large view shows the cloth's weave in a natural ground,
  still captioned *Colours at the atelier*.
- **The chips:** clean small cuts with a soft shadow; the chosen one has a fine ring. The pinked
  edges are gone.
- **Altai's three mélange colours** are named as such: *1 Biancore mélange*, and so on.

### Professionals

- **One bar on each professional page:** the Architects, Hospitality and Agents & Resellers
  pages share the same bar.
  - It holds *Architects & Designers · Hospitality & Contract · Portfolio · Agents &
    Resellers*, and *Open a project file* on the right.
  - The page you are on is underlined.
  - It is a section (*Professionals bar*), so it can be moved or removed in the editor.
- **The menu's Professionals panel** lists the same places in the same order, with *Open a
  project file* as its button.
  - *Become a partner* is on the Agents & Resellers page.
  - The phone menu matches.
- **The project desk** (bottom of the Architects page) is recomposed:
  - The three steps of a project sit beside the frescoed loft photograph, with the mattress
    label as a detail.
  - The lifestyle photograph with the red throw is gone.

### Enquiries reach info@ clearly

The enquiry page and the enquiry drawer post to Shopify's contact form. Shopify emails each one
to the store's contact email.
- **In admin:** Settings → Store details (Store contact email) must be
  **info@midsummer-milano.com**. Replying to the email answers the visitor.
- **Each email now starts with:**
  - the enquiry type (*Book appointment*, *Trade enquiry*, …);
  - the visitor's title and name, in Shopify's own name field, so the sender line shows it;
  - the page it was sent from, with its address.
- **The other fields are named by the tab:** *Preferred date*, *Subject*, *Company*,
  *Project*, *Message* …
- **Check:** send one test enquiry from the live site. If it does not arrive, look in spam.
  Shopify sends from its own mailer, so mark it as a trusted sender.

### The world map

The agents page opens on the drawn map again. It has been checked in every round, with regions,
clusters and a legend.
- The street map (OpenFreeMap tiles) stays in the section as *Street map (test before turning
  on)*, off by default.
- Its tiles cannot be reached from where the theme is built, so it was never seen with real
  tiles. Turn it on only after looking at it on the store.

### Collection pages: one line of products

The products of a collection run in one horizontal line:
- Each card snaps into place, and the next one shows at the edge.
- Draw the line along with the mouse, or swipe on a phone.
- Arrows and a fine progress line with *01 / 12* sit beneath it.
- The kind and need filters work as before.
- A collection of one product keeps its large single layout.

### Checks on this build

| Check | Result |
| --- | --- |
| Shopify's Liquid engine (Ruby, `strict` and `strict2` parsing) | 462 files, 0 errors |
| The same engine rendering the homepage, product pages (system, topper, mattress, boxspring), Professionals, Loro Piana, collection and agents pages | no errors |
| Theme Check | 0 errors (67 warnings, as before) |
| Template values against section schemas | no new issues |
| Page audit (78 templates, computer and phone) | no sideways overflow, no missing images, no script errors |
| Interaction tests | 152 pass (new: the collection line and its arrow) |

After uploading, check the list Shopify shows when the upload finishes. It should name no files.

## 38. Round 16: ready for launch

### Home

- **Chapter I, *By hand. One bed at a time*:** a wide photograph of the artisan working the
  fibre, with a second, smaller photograph of hands smoothing wool along the edge of a bed. It
  carries the caption *Wool, smoothed by hand along the edge of the bed*.
  - The section (*Home chapter*) has a new *Shape* setting (upright or wide) and an optional
    second photograph with its caption.
  - On a phone the second photograph is smaller and its caption is hidden.
- **Chapter III, Loro Piana Interiors:** the teal throw is replaced by a real Loro Piana bed:
  Paisley, in Shadan and Katai.

### Inside the bed (home and product pages)

- **Each part card shows its own product.**
  - Flora, Paisley, Roma, the Dreamy line and the First Dream line each show their own topper,
    mattress and boxspring, cut from the house's photographs.
  - Every other bed shows the house's photographs of a topper, a mattress and a boxspring.
  - The topper card always shows a topper.
  - None of the photographs shows the inside of a bed.
- **The drawings are redrawn:**
  - Each part is dressed in its own cloth, taken from photographs of the real cloths: Shadan
    paisley, Katai silk, the Cardi damask, Wish bouclé, the Mystic River weave and linen.
  - Each has piping, hand tufts, a stitched border and brass vents.
  - Integrated systems show the mattress inside.
  - Nothing describes layers or construction.
- **Paisley, corrected from the photographs:** the paisley linen (Shadan) is on the topper and
  the border of the mattress. The boxspring is Katai silk, in deep red. The old drawing put the
  paisley on the boxspring. The card texts and the Loro Piana page say the same now.
  **Please confirm this is right.**
- The three part cards now line up at the top. They had sat about 10px apart when one card had
  more text.

### Loro Piana Interiors page

- **The page opens on Paisley in its room** (the real Loro Piana photograph).
- **The colour chips have their pinked edges back**, with a dot on the chosen colour.
- **Two plain sections are replaced by three new ones:**
  - **Seasons.** The winter face (wool and cashmere) and the summer face (linen) sit side by
    side. Choosing one opens it wide.
  - **Paisley.** The bed beside its two cloths, each cut with pinked edges and labelled:
    - Shadan, AL2075RS, 100% linen: on the topper and the mattress border.
    - Katai, AS1005, pure silk: on the boxspring.

    A close-up of the bed's edge and a link to Paisley follow.
  - **Roma.** The Roma topper and mattress in Mystic River, as they stand at the atelier.
- **Other Loro Piana cards** (the menu's Heritage panel, the Professionals page and the *next
  read* card at the foot of pages) now show the Paisley bed, not a throw.

### Natural materials

Under each fibre, *In our beds* now lists every bed. After the sixth, a *Show N more* button
opens the rest in place, and *Show fewer* closes them. It no longer leads to the compare page.

### Collection pages: a register instead of the horizontal line

The horizontal line of products is gone. Products are laid out like a printed register:
- **Gallery**, in a set rhythm:
  - one wide photograph and one upright beside it;
  - then three smaller ones;
  - then the pair reversed.

  Each entry is numbered (01, 02 …). Each sleep product carries a small pinked cut of its own
  cloth. Filtering keeps the rhythm and renumbers from 01.
- **Index:** every product on one line each, with what it is, its cloth and its fibres. On a
  computer, the product's photograph follows the cursor.
- **Compare**, as before.

On a phone the gallery is two columns.

### Agents & resellers: down to the street

- **The map goes from the drawn world down to the street.**
  - Zooming in fades in a street map (OpenStreetMap, credited in the corner).
  - Choosing a place in the list, or a pin, flies to its street.
  - The drawn city names step back once the street map is in.
- **The tiles come from OpenStreetMap by default.** The section setting is *Map tiles to the
  street (address)*.
  - OpenStreetMap allows modest use with the credit shown. If the site's traffic grows, put a
    keyed provider's address (MapTiler, Stadia, CARTO …) in that setting.
  - Leaving the setting empty keeps the drawn map alone, down to city level.
- **If the tiles cannot be reached,** the map goes back to the drawn map by itself, zoomed to
  city level, with every pin.
- **Testing:** OpenStreetMap cannot be reached from where the theme is built. The map was tested
  with stand-in tiles:
  - The atelier, Via Andegari 4, landed on the right street tile (zoom 16).
  - The fallback was tested with tiles that fail.

  **Look at it once on the store:** zoom into Milan and check that the streets appear.

### Navigation

- **The Professionals bar:**
  - It appears only on the Architects and Hospitality pages.
  - It holds *Architects & Designers · Hospitality & Contract · Portfolio*, and *Open a
    project file* on the right.
  - Agents & resellers is filed under Contact in the menu, so the bar no longer appears there.
- **The menu's Professionals panel:** *Become a partner* (the partner enquiry) replaces Agents &
  resellers. The phone menu matches.
- **The footer follows the menu:**

  | Column | Links |
  | --- | --- |
  | Professionals | Architects & interior designers, Hospitality, Portfolio (shown when the store has the page) |
  | Speak to the atelier | Enquire, Agents & resellers, Care and maintenance |
  | Heritage & Craft | its existing links, plus Journal |

  The *Speak to the atelier* heading now lines up with the other column headings.

### Package

- Five photographs nothing uses any more are left out (the teal and paisley throws, two old Flora
  views, a ceiling fresco).
- Zip: 32.5 MB, 1,019 files. The largest Liquid file is 161 KB.

### Checks on this build

| Check | Result |
| --- | --- |
| Shopify's Liquid engine (Ruby, `strict` and `strict2` parsing) | 466 files, 0 errors |
| The same engine rendering the homepage and every product handle (30, systems, mattresses, toppers, boxsprings) | no errors; each product's own part photographs |
| Theme Check | 0 errors (69 warnings, of the same kinds as before) |
| Template values against section schemas | no new issues |
| Page audit (78 templates, computer and phone) | no script errors, no missing files, one H1 each |
| Interaction tests | 159 pass (new: register gallery and index, Professionals bar, agents under Contact, footer, street map and its fallback) |

### To check on the store after uploading

1. Agents & resellers: zoom into Milan and choose the atelier in the list. The street map
   should appear, with the pin on Via Andegari.
2. Paisley: confirm the wording (Shadan linen on the topper and mattress border; Katai silk on
   the boxspring).
3. Send one test enquiry and check it reaches info@midsummer-milano.com.
4. After the upload finishes, Shopify's list of rejected files should be empty.

## 39. Round 17: before release

### Product pages

- **The foot of the page: *More from the collection*.** This replaces the thin *Also in Icon*
  row.
  - Four pieces from the product's own collection (Essentials, Signature or Icons), with pieces
    of the same kind first: another bed system after a bed system, another mattress after a
    mattress.
  - Each card is drawn as on the collection page: photograph, what it is, name, one line and its
    fibres.
  - On the right, a link to the whole collection (*All of Icons →*).
  - The section is *Product · Also in*. Its settings hold the label, the link text and the name
    of each kind.
- **Sizes are said once.** Some descriptions list every size, which used to show up again in the
  specifications and again under the drawing. Now, when a description lists the sizes (Jungle
  Dreams, for example):
  - The specifications say them in one line (*6 sizes: 100 × 200 · …*) with a link, *See each
    size, drawn ↓*.
  - The size drawing switches to the piece's own sizes, smallest first, each with its note (for
    example, the headboard).

  This only happens when the list is clearly a list of sizes: more than one size, and at least
  four lines in five read as sizes. Every other product keeps its usual drawing.
- **Inside the bed: three different photographs.** Topper, mattress and boxspring each show
  their own photograph, never the same one twice. This covers Paisley, Flora, Roma, Dreamy and
  First Dream. None of the photographs shows the inside of a bed.
- **Top: the Green Product Award.**
  - Under the name: the award's mark, *Green Product Award 2025*, and *Awarded in Berlin for its
    plant-based materials and seasonal construction*.
  - It links to the award's page for Top (gp-award.com).
  - It is also in the product's structured data for search engines.
  - Another product can carry an award through the product section's *Award* setting.

### Collection pages

The register is gone. Products now sit in an even grid:
- three columns on a computer, two on a tablet and a phone;
- every photograph the same size, the names lined up;
- no numbers and no cloth cut on the cards;
- views reduced to *Gallery* and *Compare*, and shown only when a collection has more than one
  bed system.

### Handmade in Italy

*Slow, by method* has two new photographs:
- an artisan cutting the cloth by hand;
- a finished Roma corner, captioned *Every tuft tied by hand, every border stitched by hand*.

### The Professionals bar

- **It no longer disappears.** It stays in view while the page scrolls, just under the header,
  and moves up when the header hides on a phone.
- **It now also appears on the Portfolio** (the journal called *projects* or *portfolio*), with
  Portfolio marked.
- **On a phone** the row of links scrolls sideways. It opens on the page you are on, and fades
  at the edge where more links follow.

### Agents & resellers map

- **The map opens on the whole world**, with every place on it and *World* marked. Each region
  is one tap away.
- **The kind filter** (*All · Showrooms · Boutiques · Agents*, each with its count) is one quiet
  row of tabs, the chosen one underlined.
  - Every name is shown whole at every width from 320 px up.
  - Before this, *Agents* was cut off.

### Natural materials

Five fibre photographs are replaced:

| Fibre | New photograph |
| --- | --- |
| Alpaca | the animal in its long fleece |
| Mohair | a mohair throw falling to its fringe |
| Linen | the close weave of linen cloth |
| Ingeo | the maize fibre itself, on a dark ground |
| Orange Fiber | an orange cut across |

The orange keeps a little more of its colour than the other plates; in monochrome alone it read
as eggs. The photographs come from the house's library. The stock sites could not be reached
from where the theme is built, so there was no flax field, maize plant or Angora goat to choose
from.

### Package

- Zip: 32.0 MB, 1,016 files. The largest Liquid file is 161 KB.
- Part photographs nothing uses any more are left out, and so is the cloth-cut snippet the old
  register used.

### Checks on this build

| Check | Result |
| --- | --- |
| Shopify's Liquid engine (Ruby, `strict` and `strict2` parsing) | 465 files, 0 errors |
| Theme Check | 0 errors (69 warnings, of the same kinds as before) |
| Template values against section schemas | no new issues |
| Page audit (every template, computer and phone) | no script errors, no missing files |
| Interaction tests | 171 pass (new: Top's award, the product foot, sizes said once, the bar staying in view and on the Portfolio, the map on the world, its kinds whole at 1440, 390 and 320 px, the new photographs) |

### To check on the store after uploading

1. **The "Loro Piana patch".** I took this to mean the small pinked cloth cut on each collection
   card, and removed it. The pinked colour chips on the Loro Piana page are unchanged. If you
   meant those, say so.
2. **Top:** the award shows under the name, and its link opens the Green Product Award page.
3. **A product whose description lists its sizes** (Jungle Dreams): the specifications should say
   the sizes once, and the drawing should step through them.
4. **Still open from Round 16:**
   - Agents & resellers: zoom into Milan and check that the street map appears.
   - Paisley: confirm the wording.
   - Send one test enquiry.

## 40. Round 18: a full optimisation pass

Every page was measured before and after, on a phone and on a computer, with:
- Lighthouse (speed, accessibility, best practices, SEO);
- axe-core (accessibility, WCAG 2.1 AA);
- a sweep of all 78 templates at 360, 768 and 1440 px.

### Speed: pictures at the width they are seen

**The problem.** A photograph used to be sent at one size, usually 1,600 to 2,600 px wide, whatever the screen. This applied both to photos chosen in the editor and to the theme's own photographs. A phone downloaded the picture a large screen needs.

**The fix.**
- **Several widths per picture.** Fifty pictures in 31 sections now offer widths from 360 to 2,400 px. The browser takes the one that fits.
  - Shopify's CDN makes each width.
  - Where the browser accepts it, the CDN sends WebP, which is lighter than JPEG.
- **Real display widths.** Each picture states how wide it is actually shown, measured at 390, 900 and 1440 px. For example, the Professionals pairs are 44% of the screen on a computer and 90% on a phone.
- **One shared snippet,** `ms-srcset`, writes these widths for every section.
- **Also covered:**
  - the collection header's own photograph (Essentials, Icons);
  - the home film's still, now 1,600 px; it shows only until the film plays.
- **Below the fold:** the press marks and the footer logo now load only when the visitor nears them.

Lighthouse, phone profile, with the CDN's resizing simulated locally:

| Page | Score before → after | Largest paint | Page weight |
| --- | --- | --- | --- |
| Home | 61 → 82 | 10.8 s → 4.5 s | 2.5 MB → 1.2 MB |
| Natural materials | 72 → 77 | 8.4 s → 5.4 s | 1.4 MB → 0.8 MB |
| Collection (Icons) | 79 → 82 | 5.3 s → 4.6 s | 801 → 617 KB |

- **Product pages:** their pictures come from the store and already offered several widths. They are unchanged.
- **On the store:** the real numbers depend on Shopify's CDN. Check them with PageSpeed Insights once the theme is published.
- **Re-encoding:** the photographs themselves were already well compressed (about quality 82). Re-encoding them would have saved only 2%, so it was not done.

### Accessibility (WCAG 2.1 AA)

axe-core went from nine kinds of issue to none on content. The only flags left are the decorative index numerals (01, 02 …), which screen readers already skip and the standard exempts.

- **Small text that was too light now reads clearly.**
  - Labels, captions and figures in light grey or gold were darkened just enough to meet 4.5:1, in the same hue. This covers the fibre atlas, the collection labels, the opening hours, the size tables and the questions index.
  - It holds on the ivory and on the beige cards alike.
- **The process steps** (Atelier, Handmade in Italy) no longer fade the steps that are not in view.
  - The step in view has its title in ink; the others are in the muted grey.
  - Every word stays readable.
- **Page structure:**
  - The WhatsApp button now sits inside a landmark.
  - Product pages have their headings in order: the name, then each section.
  - The header's navigation and the collection pages' page links are named.
- **Compare:** the yes and no marks are named images. The column heads hold their links. The last row's head says what it is.
- **Loro Piana Interiors:** each cloth's panel is a proper tab panel.
- **The *Why Midsummer* table's** empty corner cell now says what its columns are.
- **Rows that scroll sideways on a phone** can be reached and scrolled from the keyboard, and are named for screen readers.
- **Collection cards** no longer read the product's name twice (once for the photo, once for the name).

### Fixed

*At a glance:* on a 360 px phone the "15 + 15" figure was 2 px wider than the screen. It now scales down there.

### Checks on this build

| Check | Result |
| --- | --- |
| Shopify's Liquid engine (`strict` and `strict2`) | 466 files, 0 errors |
| Theme Check | 0 errors, 69 warnings (unchanged) |
| Template values against section schemas | no new issues |
| Page audit (78 templates) | no script errors, no missing files, one H1 each |
| Overflow sweep (78 templates × 360, 768, 1440 px) | nothing wider than the screen |
| axe-core (78 templates × phone, computer) | no issues on content |
| Interaction tests | 178 pass (new: pictures at their width, steps readable, WhatsApp landmark, heading order, *At a glance* at 360 px, compare roles, card names) |
| Package | 32.0 MB, 1,017 files; the largest Liquid file is 157 KB |

### To check on the store after uploading

1. Open a page on a phone (Atelier or Natural materials). The photographs should look as sharp as before.
2. Run PageSpeed Insights on the home page and a product page, and keep the numbers as the baseline for later changes.
3. The items still open from Rounds 16 and 17 (section 39) stand.

## 41. Round 19: Instagram, the street map, each fact once, iubenda, and the fibres under the glass

### Instagram: the latest posts, live

The *Follow us* section on the home page can now show the account's latest posts, each tile leading to its own post. Without a feed it shows the house's photographs, leading to the account, as before.

Instagram does not let a page read an account's posts without a key, and a key must never sit in a page's code. A feed service holds the key and gives the theme a plain address instead. The theme reads [Behold](https://behold.so)'s feeds (the free plan covers one account) and any feed that uses Instagram's own fields.

1. Sign in at behold.so, connect the *midsummermilano* Instagram account and create a feed (JSON).
2. Copy the feed's address (it looks like `https://feeds.behold.so/…`).
3. In the theme editor: **Theme settings → Midsummer · Social and WhatsApp → Instagram feed address (latest posts)**. Paste it and save.

How it behaves:
- The posts load only when the section comes near the screen, and are kept for an hour in the visitor's browser.
- Films and albums carry a small mark. Each post's first line is the picture's description.
- If the feed is missing or does not answer, the house's photographs stay.
- No access token appears anywhere in the theme.

### Agents and showrooms: a street map that stays sharp

Zooming into a city now draws the streets themselves (OpenFreeMap vector data) in the house's colours, sharp at any size and on any screen. It replaces the blurred, too-bright street tiles.

- The map library is a theme asset (`ms-maplibre.js`). It loads only when someone zooms in.
- The streets draw only once their data has arrived. If OpenFreeMap cannot be reached, the drawn map (or the older tiles) stays, never an empty frame.
- The credit (OpenFreeMap © OpenMapTiles, data from OpenStreetMap) shows while the streets are on.
- **Setting:** *Agents and resellers* section → **Street map, sharp at any size** (on by default). Off: the older tiles.

### Product pages: each fact said once, in its best place

- **The facts list at the top** no longer repeats what the sections below show better:
  - the sizes (drawn, with each headboard, in the sizes band);
  - the cloth;
  - the service.
  - **Setting:** *Product* section → **Sizes, cloth and service only in their sections** (on by default). Off: the list shows them too.
- ***Specified, not selected:*** the dimensions row is gone when the page already shows the sizes.
- ***Inside the bed* (headboard beds):**
  - the *Height* and *Sizes* rows are gone (the sizes band shows them);
  - the quote is hidden when the product description already opens with it.
- **Questions:** 52 answers on product pages that repeated the reasons or the specifications are left out.

### iubenda, and Avada evicted

The theme has no cookie banner of its own. It works with iubenda, or with any banner that reports through Shopify's Customer Privacy API.

**To switch iubenda on:**
1. Install iubenda's Shopify app and set up the cookie banner there.
2. **Online Store → Themes → Customize → App embeds:** turn on iubenda's embed.
3. **Settings → Customer privacy:** turn off Shopify's own cookie banner, so visitors see one banner, not two.
4. **Theme settings → Midsummer · Where links go:** paste your iubenda **Privacy policy** and **Cookie policy** addresses. Empty: the store's own policy page.

**What the theme then does:**
- The footer's *Cookies* link opens iubenda's preferences. With no banner it opens the cookie policy.
- The theme's own measurement (the AI-referral note) keeps nothing beyond the page until the visitor allows analytics.

**Avada SEO Suite.** Its app embeds are removed from the theme's settings. The theme's own titles, descriptions, structured data and sitemaps cover what Avada did.

To finish in the admin:
1. **Settings → Apps and sales channels:** uninstall *Avada SEO Suite* (and *SEOon Blog*, if installed).
2. The URL redirects Avada created stay in **Online Store → Navigation → URL redirects**. Keep them: they protect old links.
3. Search Console, Bing and Pinterest verification codes now have their own fields: **Theme settings → Midsummer · Cookies and search**. Paste the code or the whole meta tag. If Avada was what verified the site, paste the codes there before uninstalling it.

### Natural materials

**Mohair.** The plate now shows mohair close up, from the house's own photograph of a mohair cover: the long, lustrous, wavy hair of the Angora goat. It replaces the generic tuft. The library has no photograph of an Angora goat. Send one and the plate script will process it like the others.

**Under the glass, redrawn to scale.**
- **Real proportions.** Every fibre is drawn at its real width (2 px per micron, a field 0.4 mm across). Behind each one lies a pale human hair, about 70 µm, at the same scale. A 100 µm bar sits at the head of the field.
- **What a customer sees:**
  - vicuña at a sixth of a hair;
  - wool's bold scales and crimp;
  - silk's paired filament, with no scales;
  - linen's nodes;
  - cotton's twisted ribbon;
  - horsehair dwarfing the hair behind it.
- **What each fibre's surface is drawn with:**
  - smooth, flat, faint, wavy or jagged scale edges;
  - the air-filled core of alpaca and horsehair;
  - the fine central channel of linen;
  - the ridges of the palm.
- **The caption on the plate** says how fine the fibre is, for example "25–33 µm across. The pale band is a human hair, about 70 µm." The number is left out where a figure beside it already gives it (vicuña's 12 µm).
- **Beside each fibre,** a short *Under the glass* note says what the glass shows and what it means in a bed. Examples:
  - the finer a fibre, the more readily it bends, which the skin feels as softness;
  - the crimp keeps wool full of air.
  
  The notes are general fibre science, kept to what the drawing shows, and do not repeat the fibre's own text.
- **Where the numbers come from.** Vicuña's and cashmere's widths are the catalogue's. The others are the usual ranges for each fibre. The made fibres (Ingeo, Orange Fiber) and the palm fibre have no number.
- **Editing:** each fibre block has **Across one fibre, in µm** and **Under the glass, said**.
- **Figures that repeated the text beside them** were removed, for example *Mongolia* next to "Origin: Mongolia", and the yak's *May*. The map view names the place once.
- **On a phone,** the three view buttons now hold their words.

### Fixed

Two of the build's own patches were adding the same lines again on every build. They now apply once, and two builds in a row give identical files. Neither changed what a visitor saw.
- The *Cookies* link's script had five extra copies of one check.
- The Professionals menu had 45 extra copies of one line.

### Checks on this build

| Check | Result |
| --- | --- |
| Shopify's Liquid engine (`strict` and `strict2`) | 469 files, 0 errors |
| Theme Check | 0 errors, 69 warnings (unchanged) |
| Template values against section schemas | no new issues |
| Page audit (78 templates) | no script errors, no missing files, one H1 each |
| Overflow sweep (78 templates × 360, 768, 1440 px) | nothing wider than the screen |
| axe-core (78 templates × phone, computer) | no issues on content (only the decorative numerals) |
| Interaction tests | 194 pass. New: Instagram live, film and album marks, a failing feed, no token; the street map, aligned, and its fallback; the fibres to scale with their notes and captions; figures that do not repeat; the view buttons on a phone; the quote said once; facts said once; iubenda's preferences from the *Cookies* link; consent before anything is kept |

### To check on the store after uploading

1. **Instagram:** paste the Behold feed address (above), then open the home page. The latest posts should replace the photographs.
2. **Agents and resellers:** zoom into Milan. The streets should draw sharp. OpenFreeMap could not be reached from the test environment, so the streets were tested with generated map data.
3. **iubenda:** with the app embed on and Shopify's banner off, check that only one banner appears and that the footer's *Cookies* link opens its preferences.
4. **Avada:** uninstall it, after moving any verification codes (above).
5. **A headboard bed's page,** for example Cashmere Couture: the sizes are said once, in the sizes band.
6. **Natural materials:** open *Under the glass* for wool and for vicuña.

## 42. Round 20: sizes made to measure, Instagram without stand-ins, Soft to the Touch redrawn, a fresher map

### Sizes: any size, shown as such

Every bed is made to measure, so the product pages no longer read as a menu of fixed sizes.

- **The "Standard sizes" row at the top of product pages is gone,** on every product. It listed names (Single, Queen, Small Double …) that the sizes section below already shows, and it suggested the sizes were fixed. It is also out of the product's structured data.
- **The sizes section** (*Specified, not selected.*):
  - Every size is written the same way: width × length in centimetres, narrowest first, under the label "For example, in cm". No more mixed "100 × 200 … Queen, King".
  - A product whose description lists its own sizes (for example Jungle Dreams, Soft to the Touch) shows those, still in centimetres. The headboard measure stays under the drawing, for example "headboard 208 × 216 × 103 h".
  - **New: + Your size.** The customer types a width and a length, or ticks **Round** and types a diameter, and the drawing redraws to that size. **Ask for this size** opens the enquiry form, already filled with the product and the measure (for example "Jungle Dreams, 172 × 213 cm" or "Ø 240 cm, round").
  - **Settings:** *Product · Three reasons* section → **Sizes** (the label above the sizes, and the words for *Your size*). The six old size-name settings were removed.
- **The size guide on the Questions page** now opens "Any size, made to measure." and presents the usual sizes as reference only.

### Instagram: the latest posts, or nothing

The *Follow the atelier* section no longer shows stand-in photographs.

- **With a feed** (Theme settings → Midsummer · Social and WhatsApp → *Instagram feed address*, see section 41), or **with an Instagram feed app's block** added to the section, the row shows the account's real latest posts.
- **Without either,** the section shows the account name, its link and the social icons, and no pictures.
- If the feed is set but cannot answer, the row stays hidden rather than showing old photographs.

To show the posts, either of these is enough:
1. **Behold (free, one account):** connect *midsummermilano* at behold.so, create a JSON feed, and paste its address into the setting.
2. **An Instagram feed app:** install one from the Shopify App Store that offers a theme app block (for example Instafeed). Then, in the theme editor, select the home page's *Follow the atelier* section, choose **Add block**, and pick the app's block.

### Soft to the Touch: redrawn from the bed itself

The *Soft to the touch, part by part* drawing was redrawn from the house's own front photograph of the bed:
- two soft cushions curled over a slim upholstered headboard, resting on a thin inlay of Canaletto walnut;
- a padded frame on walnut-stained legs;
- a piped mattress, two pillows and a throw laid across the foot.

The old drawing showed bare iron posts and a wide walnut band, which the real bed does not have. Height stays at the catalogue's 107 cm, and the part-by-part interaction (headboard, mattress, boxspring) is unchanged.

**The other headboard beds** (Cashmere Couture, Silk Flowers, Beating of Wings, Jungle Dreams, Tulip, Pure, Giotto) keep their headboards. Their bedding is now drawn the same way: real pillows and a throw draped across the foot, in place of the small square in one corner, with tapered wooden legs and a soft shadow under the bed.

### The agents map: lighter and current

- **The street map** has a clean, current palette:
  - pale stone land, clear blue water, fresh green parks;
  - white streets on soft grey edges, the main roads in a light warm tone;
  - charcoal place names on white halos.
- **The world view** before zooming uses matching tones, so zooming from the world into the streets has no jump in colour.
- **The pins, the legend and the controls** are unchanged.

### Checks on this build

| Check | Result |
| --- | --- |
| Shopify's Liquid engine (`strict` and `strict2`) | 469 files, 0 errors |
| Theme Check | 0 errors, 68 warnings (one fewer than before) |
| Template values against section schemas | no new issues |
| Page audit (78 templates) | no script errors, no missing files, one H1 each |
| Two builds in a row | identical files |
| Interaction tests | 203 pass. New: sizes in cm and narrowest first; no sizes at the top; *Your size*, straight and round, and its enquiry note; Instagram with no feed (no pictures) and with a failing feed (no row); Soft to the Touch drawn as photographed |

### To check on the store after uploading

1. **A product page,** for example Jungle Dreams: the top list has no sizes. The sizes section shows centimetres only, and *+ Your size* draws and asks for any size.
2. **The home page:** *Follow the atelier* shows the account only, until a feed or an app block is added (above).
3. **Soft to the Touch:** the drawing in *part by part*.
4. **Agents and resellers:** zoom into Milan and check the new map colours with the real street data. OpenFreeMap could not be reached from the test environment, so the colours were checked on generated streets.

## 43. Round 21: true Loro Piana colours, new photographs, one tone everywhere, and the owner's corrections

### Loro Piana Interiors colours, true to the cards

Connemara and Altai were measured again from the cards in the atelier's swatch folder (Drive), and redrawn.
- **Measured against the paper beside each swatch.** The photograph of each card is lit unevenly, so the far swatches had come out dull.
- **Averaged as the eye sees it.** Each colour is now the average in linear light; the old average ran a little dark.
- **Drawn with the card's own cloth.** Connemara now shows its open linen weave and Altai its milled wool, taken from the large swatch on each card. Before, a fine line texture stood in for both.
- **Shown without the house tone.** The site's photo tone had been warming and greying the cloth pictures. A colour chosen on screen is now the colour of the card.

Mystic River keeps its photographed colours. Wish, Cardi, Ely's Harbour, Bangor and Shadan keep their pictures.

The swatch folder also holds Papeete, Dingle, Tiepolo, Alchemy, Sherpas and Palmier. No Midsummer product uses them, so they are not on the site.

The official Loro Piana Interiors website could not be reached from the build environment, so it was not used.

### One tone over every photograph

- **Product photographs.** Some product photographs had escaped the house tone. The tone skipped any picture whose file name contained the word "logo", so photographs exported as "… no logo.jpg" were left out. Logos are now recognised by their markup instead: SVG files, the press marks, and the header and footer logo.
- **The cart page.** It uses the base theme's layout and now carries the tone too.
- **Exceptions.** Only the logos, the drawings and the Loro Piana cloths are left untoned.

### "What matters most to you?"

On collection pages, the line under the needs now names only fibres of the beds listed.
- **What it names.** Each bed is chosen for a need by its three most telling fibres, as the Natural materials page describes each fibre. The line names those fibres, for the beds shown at that moment.
- **Hidden needs.** A need that no listed bed answers is not offered.
- **Classifications checked.** Toppers are no longer listed under *Support*: a topper is the surface of a bed, not its support.
- **Warmth.** Wool and silk also temper a bed, but they are in nearly every system. Warmth is therefore credited to cashmere, camel hair, yak, alpaca, mohair and vicuña; otherwise *Temperature* would list 23 of the 25 systems.
- **Editing the lines.** In the theme editor, *{fibres}* in a line becomes the list, and *{carry/carries}* picks the verb for several fibres or for one.

### Cloth names read as fabrics

- **The rule.** Wherever a product is described, a Loro Piana Interiors cloth is named as a fabric: *Mystic River fabric*, *Mystic River and Connemara fabrics*.
- **Where a material already follows.** The name stays as it is: *Connemara linen*, *Katai silk*, *Wish bouclé*.
- **Italian and Russian.** The product lines say *tessuto* and *ткань*.
- **The Loro Piana Interiors page.** There each name is the title of a cloth, so it stays bare.

### Photographs

- **Inside the bed.** Products photographed on their own (Roma, Flora, Paisley, First Dream, Dreamy) keep their own photographs. Every other product now shows three current studio photographs:
  - a Top system in neutral beige, for the topper;
  - a cream mattress with rust piping, for the mattress;
  - a sand boxspring on legs, for the boxspring.
  
  Dreamy's mattress card shows its whole corner. None of these photographs shows the inside of a bed.
- **Handmade in Italy.** The opening photograph is now an artisan opening fibre by hand over the wool, in black and white so it differs from the home page. The previous photograph showed a panel being upholstered.
- ***The cloth* step.** It now shows Paisley dressed in Loro Piana Interiors (Shadan and Katai) instead of a terrace on the coast.
- **Natural materials.** Silk is now shown as raw floss, the raw material, instead of a satin cloth.

### Copy

- **Home page, delivery.** "Then a check-up when year fifteen arrives." (no longer "free").
- **15 + 15.** One quiet sentence: "The regeneration is offered by the house; the transport, there and back, is at your charge."
- **Our story, in figures.**
  - 24: *Products across three collections*.
  - Under *Made to order*: "Down to the fibres: the warmest for winter, the freshest for summer."
  - The first figure is now *2–3 · Full days of handwork in every mattress*, in place of a count of artisans.
- **Handmade in Italy.**
  - The subtitle reads "Italian artisans. Two or three full days. One bed."
  - "One pair of hands follows the bed" became "the bed is made by hand at every stage".
- **Compare the collections.** *Regenerated at fifteen years* became *Support, set to how you sleep*.

### The Green Product Award on Top

The award box on the Top product page used to appear in only two cases: when the product used the Top template, or when its handle was exactly *top*. A Top product renamed in admin, or set to the default template, lost it. It now appears for the Top system however the store names it:
- by its system (template or handle);
- by its title: *Top*, *Top Sleeping System*, *Top bed system*, *Sistema Top*;
- or from a product metafield, **custom.award** (single-line text), which can show any award on any product.

*Top Dream* is a different bed and does not show it.

### Also in this round

- **Agents and resellers.** The open place's shading keeps clear of its dot, with no box drawn round it.
- **Round sizes.** Only Giotto shows round sizes, by diameter: Giotto Round Ø 225 and 245, the Giotto mattress Ø 225, the Giotto bed Ø 255. The round option is gone from every other product.
- **Product facts.** *Comfort* and the other facts sit on one line with their labels.
- **The street map.**
  - Its Round 19 colours are back.
  - If the detailed map is slow to load, the plain map stands in, in grey, until it arrives.

### Checks on this build

| Check | Result |
| --- | --- |
| Shopify's Liquid engine (`strict` and `strict2`) | 469 files, 0 errors |
| Theme Check | 0 errors, 68 warnings (unchanged) |
| Template values against section schemas | no new issues |
| Page audit (78 templates) | no script errors, no missing files, one H1 each |
| axe-core (78 templates × phone, computer) | no issues on content (only the decorative numerals) |
| Layout sweep (360, 768, 1440 px) | no sideways scroll, no script errors |
| Two builds in a row | identical files |
| Interaction tests | 222 pass. New: each need line names only fibres of the beds shown; product photographs toned, including one named "… no logo"; logos and Loro Piana cloths untoned; the house photographs on Top; Handmade in Italy opening and cloth step; the support row on Compare; the check-up and the 15 + 15 note; Our story figures; raw silk; cloth names as fabrics; the award on Top, under another name and template, and not on Top Dream |

### To check on the store after uploading

1. **A collection page.** Choose each need under *What matters most to you?*: the line should name only fibres of the beds listed.
2. **Top:** the *Green Product Award 2025* box under the title.
3. **A product page without its own photographs** (for example Top). The three *Inside the bed* cards should show the new house photographs. On any product page, check that all photographs share the same warm tone, and that the Loro Piana cloth swatches are untoned.
4. **Loro Piana Interiors.** Compare Connemara and Altai on screen with the physical cards. The colours now follow the cards, but every screen differs a little.
5. **Handmade in Italy, Our story, 15 + 15, Compare the collections.** Check the new photograph and the new lines.
6. **Giotto.** The 2026 catalogue gives the Giotto bed Ø 255 cm. If the store's own text still says 235, correct it in the product description.

## 44. Round 22: atelier photographs, named sizes, every colour of each cloth, needs from the catalogue, phones checked, drawings checked against the catalogue

### Inside the bed: one session at the atelier

The three studio photographs from Round 21 did not belong to the house. Every product without its own photographs now shows three pictures from one session at the atelier:

- **The topper.** The topper on its mattress, with the ochre bed behind it.
- **The mattress.** The mattress on its boxspring, with the Midsummer label.
- **The boxspring.** The ochre boxspring on its walnut legs, on the herringbone floor.

The three photographs share one light, one wallpaper in gold and blue, and one floor. None shows the inside of a bed. Roma, Flora, Paisley, First Dream and Dreamy keep their own photographs.

### Sizes named again

Each size on a product page now has a name above its measure:

| Width | Name (EN) | IT | RU |
|---|---|---|---|
| under 110 cm | Single | Singolo | Односпальная |
| 120 cm | Small double | Una piazza e mezza | Полуторная |
| 140 cm | Double | Francese | Двуспальная |
| 160 cm | Queen | Queen | Queen |
| 180 cm | King | King | King |
| 190 cm and wider | Super King | Super King | Super King |
| 153 × 203 (American) | US Queen | Queen americano | Queen (США) |
| 193 × 203 (American) | US King | King americano | King (США) |

- **One rule for every product.** The name comes from the width. The two American sizes (length 203 cm) keep their American names, so no two sizes on a page share a name.
- **The chosen size.** It is said with its name, for example *Queen · 160 × 200 cm*.
- **Unnamed sizes.** *Your size* stays a plain measure, and Giotto Round keeps its diameters.
- **Translations.** The names are in the theme's languages: *Online Store → Themes → Edit default theme content*, under *ms.product.size_…*.

### Every colour of each cloth

Under *The cloth*, a product dressed in more than one Loro Piana Interiors cloth now shows every palette, each linking to its cloth on the Loro Piana Interiors page:

- **Capri and Dreamy.** Mystic River and Connemara (nine colours).
- **Brera.** Connemara and Altai (sixteen colours).

Before, only the first cloth was shown, and no palette went past twelve colours.

### *What matters most to you*: from the catalogue

A bed still qualifies for a need through its first three fibres. Where the 2026 catalogue says more of a product in its own words, that now counts too:

- **Top.** Linen and horsehair for breathability; horsehair and Cheviot wool for support.
- **Paisley.** Linen for breathability.
- **Vivaldi and Vivaldi Plus.** Cotton for breathability.
- **Raffaello.** Baby alpaca for softness.
- **Roma.** Its cashmere winter topper for warmth.
- **Monteverdi.** Vegetable horsehair and linen for temperature.

Toppers are still never offered for support.

### Phones: nothing cut, nothing covered

- **The way back to the collection.** On a phone, the product photographs were drawn up over "← Icons" and cut it in half. The photographs now start below it.
- **The bar at the foot of a product page.** On a small phone the name was cut short ("Dreamy Spri…"). It now takes two lines when it needs them. On the narrowest phones the name and the button are set a little tighter, so *Dreamy Springs Boxspring* reads in full.
- **The WhatsApp button.** It now rises above the bar by the bar's own height, so it never sits on it.
- **The check.** Every page was opened at 320, 360, 390 and 430 px wide, looking for text that another element covers or that a box cuts. Nothing else was found. The rows that scroll sideways (collection filters, the Loro Piana cloths, the journal's next articles) show part of the next item on purpose, as a sign that the row moves.

### Product photographs on a white ground

A product photographed on a white studio ground showed as a white sheet on the house's paper. Each product photograph is now looked at as it loads:

- **White all round its edge.** The photograph is laid into the ground it sits on (as a print is on paper). Its white takes the page's colour; the product keeps its own.
- **Taken in a room.** The photograph is left as it is.

This covers the gallery and its thumbnails, the collection cards, *From the same collection*, the comparison, the shop's own product cards, the cart and the search. It needs the photographs to be served from the shop's own address (*/cdn/shop/…*), as Shopify does by default.

If a photograph still looks too white, send me its product and position in the gallery.

### Inside the bed: every drawing checked against the 2026 catalogue

Each drawing was compared with the finishes listed for its product in the 2026 catalogue (rows of side stitching, air vents, handles with the Midsummer logo, ribbon). Corrected:

| Product | Before | Now, as the catalogue says |
|---|---|---|
| Raffaello | three rows | two rows |
| Flora | three rows | two rows |
| Vivaldi Plus | four rows | three rows |
| My Dream | two rows | three rows |
| Monteverdi | two rows, no handles | three rows, handles |
| Amalfi, Ultra Dry | no handles | handles |
| Brera | no handles, no vents | handles and air vents |
| Vicuña | handles | no handles (the catalogue lists hand tufting instead) |

Also:

- **Long part names.** "Mattress and boxspring, in one" (Capri, Giotto) ran past the drawing's edge. It is now set in short lines, broken after a comma, in any language.
- **The topper's shadow.** The shadow on the mattress beneath it is lighter; on a white mattress it read as a smudge.

### Not done in this round

- **Ingeo's photograph.** It is unchanged. No photograph of corn (Ingeo's source) was found in the Drive or the Dropbox, and image libraries are blocked from this workspace. Upload a licensed photograph to the Drive and it will replace the plate.

### Checks

| Check | Result |
|---|---|
| Build twice | identical |
| Liquid strict (two parsers) | 470 files, 0 errors |
| Theme Check | 0 errors; 68 warnings (unchanged) |
| Interaction tests | 237 pass. New: sizes named (Queen · 160 × 200 cm; US Queen and US King; no name twice); every palette of a product's cloths; Top's catalogue needs; the way back whole at 320, 390 and 430 px; the bar at the foot with a long name, WhatsApp clear; white grounds laid into the paper, room photographs untouched; part names inside the drawing |
| Every page at four phone widths | nothing covered or cut |
| Audit of 78 pages | clean |
| Accessibility (axe) | only the decorative numerals, as before |
| Sideways overflow | none |

### After installing, check

1. **A product page on a phone.** "← Icons" (or the collection's name) sits whole above the photographs. Scroll down: the bar at the foot shows the whole name, with the WhatsApp button above it.
2. **The sizes.** For example Top: *Single, US Queen, Queen, King, US King, Super King*, each with its measure beneath.
3. **Brera and Capri, under *The cloth*.** Every colour of each cloth.
4. **A product photographed on white**, if the shop has one. It should sit on the page without a white box.

## 45. Round 22, continued: Ingeo at its source

- **The Ingeo plate.** Natural materials now shows Ingeo at its source: an ear of maize, ripe in the field, in the same warm monochrome as the other plates. The previous plate was a close-up of the white wadding. The photograph is a Shutterstock image from the house's own catalogue folder (*foto catalogo*); please confirm its licence covers the website, as for the other Shutterstock plates.
- **Ingeo's entry.** It now gives the plant's name, *Zea mays*, like linen, cotton and the palm.
- **Giotto Round sizes.** Checked against the 2026 catalogue: Ø 225 and Ø 245, as on the site. The store's *Giotto* product (with its headboard) gives 235 cm overall for a 225 cm mattress; that is a different product, and its description is unchanged.
- **The six other cloths in the swatch folder** (Papeete, Dingle, Tiepolo, Alchemy, Sherpa, Palmier). They are not added. They appear in Loro Piana's trade list but in no Midsummer bed or catalogue page, and the Loro Piana Interiors page shows the cloths of our beds. If the atelier offers them on request, say so and they can be shown as such.
- **Checks.** Build twice identical; Liquid strict 0 errors; Theme Check 0 errors; 238 interaction tests pass (new: the Ingeo plate shows the maize, named *Zea mays*).
