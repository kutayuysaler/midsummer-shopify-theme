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
screen. The name, the line under it, price on request and the two enquiry buttons stay
on the right. **The build, in section** follows as a dark band: the seven layers drawn to
depth with the texture of each material. Then come dimensions and fabric, and the other
systems in the collection. The line under the name is the metafield `custom.subtitle`;
without it, the preview's line for that system is used.

## 5. Pages the old theme built from sections

`Loro Piana Interiors`, `Download the dream` and `Salone 2026` were built from Dawn
sections in the old theme. In this theme they show their page text in the editorial
layout. Tell me if they should get a design of their own.
