# Midsummer Milano: installing the theme

`midsummer-milano-atelier.zip` is the approved preview built as a Shopify theme. Every
band of every screen is its own section. The fonts, the logotype, the graded
photographs, the press logos and the map ship inside the theme.

## 1. Upload

**Online Store → Themes → Add theme → Upload zip file** → `midsummer-milano-atelier.zip`,
then **Preview**.

## 2. What happens on its own

- **Every link finds its page.** Header, footer and page links look up the store's real
  pages, collections and blog by handle (for example `about-midsummer-milano` or
  `about-us`, `sleep-wise-faq` or `faq`, and `news` or `journal`). If a page has another
  handle, point the link at it under **Theme settings → Midsummer · Where links go**.
- **No two menu titles lead to the same page.** A menu entry whose page, collection or
  journal subject doesn't exist yet is left out of the menus until it does, instead of
  sending you to a page another title already leads to. This applies to Handmade in
  Italy, Sleep Culture, Architects & Interior Designers, Hospitality, the Mattresses,
  Toppers, Bases, Headboards and Bedding collections, and the Journal's Sleep, Materials
  and Design subjects. Other duplicates are fixed too:
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
  `page.agents-and-resellers` as a copy). It shows all 16 places from your current store
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

These have no page in the store yet, so they stay out of the menus until you create them.
Create each page in **Online Store → Pages** with exactly this handle; the design and
its menu entries appear on their own:

| Page | Handle |
| --- | --- |
| Architects & Interior Designers | `professionals` |
| Hospitality | `hospitality` |
| Handmade in Italy (optional) | `handmade-in-italy` |
| Sleep Culture (optional) | `sleep-culture` |

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

Then comes **The build, in section**, a dark band that draws the seven layers with the
texture of each material; you can step through them. Depths are never given in figures.
The drawing is marked "Indicative, not to scale", and each layer carries a word instead
of a measurement (Fine, Light, Generous, Deep, Foundation). The cm values in the editor
only choose which word and drawing height a layer gets, and they never reach the page.

After it, **The fibres** shows that system's natural fibres. Their drawings arrive on a
white ground, so the theme blends the white away and only the ink line shows on the
page.

The other systems in the collection come last. The line under the name is the metafield
`custom.subtitle`; without it, the preview's line for that system is used.

**Products keep their own templates.** The old theme gave 24 products a template of their
own (`amalfi`, `bellagio`, `bellini`, `brera`, `capri`, `dreamy-2`, `dreamy-springs`,
`essenziale`, `first-dream`, `flora`, `giotto`, `monteverdi`, `my-dream`, `paisley`,
`perfumes`, `raffaello`, `roma`, `storage`, `top-2`, `topper-roma`, `ultra-dry`,
`vicuna`, `vivaldi-2`, `vivaldi-plus`). This theme has a template under each of those
names, so every product picks up the new design with nothing to reassign.

- Each template carries the **Product · Fibres** band, with that system's natural fibres (for
  example Cashmere, Silk, Cheviot Wool, Horsehair) taken from the old theme's icons.
- Every product page runs in this order: the system, dimensions and fabric, the build,
  the fibres, then the other systems.
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

**The enquiry page** is your Contact page (`/pages/contact`, template `page.contact`),
redesigned as a full landing page:

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
- Under Request brochure it offers the PDF to download straight away.

Both send through Shopify's contact form. The chosen enquiry arrives as "Enquiry mode",
so each message says what it is.
