# Midsummer Milano: the new design on Atelier

`midsummer-milano-atelier.zip` is your store's Atelier theme (the export from 29 September
2026) with the Claude Design build applied exactly, plus fixes that make every file
upload and render.

## What's different from the earlier uploads

- **No app embeds and no Dawn code.** The theme that kept refreshing carried your Dawn
  theme's 11 app embeds and the Avada SEO include. This one carries neither, exactly like
  your base Atelier theme. Switch apps on afterwards in the theme editor's **App embeds**
  panel, one at a time, checking the preview after each.
- **The header and footer are part of the design.** The five entries and their panels,
  the footer columns, and "Book an appointment" all live in the theme, so they don't
  depend on menus in admin. Edit them in the theme editor under **MS · Header** and
  **MS · Footer**.
- **Clean icons.** Claude Design had stamped a 16 KB metadata block into Atelier's 35 icon
  files; these are your originals.

## 1. Upload the photographs and logo to Files first

**Content → Files → Upload files.** Keep the names exactly as they are. They're in the
Drive folder `export/upload-to-shopify-files/`:

`midsummer-logotype.png` · `midsummer-logotype-ivory.png` · `ms-graded-bougainvillea.jpg` ·
`ms-graded-ochre-room.jpg` · `ms-graded-arches.jpg` · `ms-graded-dune.jpg` ·
`ms-graded-paisley-red.jpg` · `ms-graded-horse.jpg`

Until the logo is uploaded, the header shows a typographic MIDSUMMER / MILANO wordmark.
Until the photographs are uploaded, their slots show a grey placeholder.

## 2. Upload the theme

**Online Store → Themes → Add theme → Upload zip file** → `midsummer-milano-atelier.zip`.
When the upload finishes, look at the theme's row: if Shopify reports any errors
there, send me the list and I'll fix exactly those files.

## 3. Pages

Create the new pages and set their template (in each page, **Theme template**):

| Page | Handle | Template |
| --- | --- | --- |
| Architects & Interior Designers | `professionals` | `page.professionals` |
| Hospitality | `hospitality` | `page.hospitality` |
| Find Your Midsummer | `find-your-midsummer` | `page.find-your-midsummer` |
| Handmade in Italy | `handmade-in-italy` | `page` |
| Sleep Culture | `sleep-culture` | `page` |

Assign templates to these existing pages:

| Page | Handle | Template |
| --- | --- | --- |
| Contact | `contact` | `page.contact` |
| Sustainability | `our-eco-friendly-approach` | `page.sustainability` |
| Questions | `sleep-wise-faq` | `page.faq` |
| Agents & Resellers | `agents-and-resellers` | `page.agents-resellers` |

Collections the design links to: `essentials`, `signature`, `icons`. The Journal is the
blog `news`.

## 4. In the theme editor

- **Home → Hero:** set *Media type* to *Video* and pick the atelier film.
- **Home → As featured in:** pick each of the 27 press logos from Files. Until you do,
  each block shows the publication's name.
- **Structured data:** fill in the telephone number and social profiles.
- **MS · Footer:** fill in the Instagram, LinkedIn and Pinterest links.

## Before publishing

The Agents & Resellers map, the bed dimensions, the figures and the pull quote hold the
design's placeholder content. Replace them with the real data in the editor.
