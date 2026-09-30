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
  `about-us`, `sleep-wise-faq` or `faq`, and `news` or `journal`). A missing destination
  falls back to a sensible page instead of a 404.
- **Existing pages take their design without a template.** The default page template
  carries each designed page and shows it only on its own page. That covers Questions,
  Natural Materials, 15 + 15, Sustainability, Professionals, Hospitality and Find your
  Midsummer. Every other page (About Us, Terms and so on) gets a centred editorial
  layout.
- **The quiz.** Your live page that uses the `sleep-assesment` template shows the new
  Find your Midsummer quiz. If the store has no quiz page at all, every "Find your
  Midsummer" link opens the quiz as an overlay, on any page.
- **Agents & Resellers** keeps its template (`page.agents-resellers`) and shows the
  stockists from your current store locator: the Milano atelier, COSE & COSE (San Marino),
  bredaquaranta (Milan), Maison Territo (Montreal), In Made (Hong Kong) and Villa
  Arredamenti (Monza and Brianza). Each has its address, telephone, email and website.
  Edit them in the editor; each stockist is a block.
- **Contact** keeps its template (`page.contact`).

## 3. Pages to create

These have no page in the store yet, so their links fall back until you create them.
Create each page in **Online Store → Pages** with exactly this handle; the design
appears on its own:

| Page | Handle |
| --- | --- |
| Architects & Interior Designers | `professionals` |
| Hospitality | `hospitality` |
| Handmade in Italy (optional) | `handmade-in-italy` |
| Sleep Culture (optional) | `sleep-culture` |

The collections `essentials`, `signature` and `icons` are used by the Our Beds panel and
the collection pages. If one doesn't exist, its links go to `/collections`.

## 4. Product pages

All of a product's photographs sit together on the left, and a click opens them full
screen. On the right are the name, the line under it, price on request and the two
enquiry buttons. **The build, in section** follows as a dark band. It draws the seven
layers to depth with the texture of each material, and you can step through them.

Next come dimensions and fabric, in the store's six sizes:

- Single 100 × 200
- Queen 153 × 203
- Small Double 160 × 200
- Double 180 × 200
- King 193 × 203
- Double Extra 200 × 200

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

## 6. The enquiry sheet

"Book an appointment", "Request a proposal" and "Request brochure" open the same sheet.
Under "Request brochure" it also offers the PDF brochure to download straight away.
