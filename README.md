# Midsummer Milano: Shopify theme

The approved Atelier preview (`Midsummer Atelier - Preview.html`), built as a Shopify
theme on the store's Atelier 4.1.5 export.

- `midsummer-milano-atelier.zip`: upload this file as it is, under Online Store → Themes → Add theme → Upload zip file.
- `theme/`: the same theme as source files.
- `INSTALL.md`: page templates, and the store data the design reads.
- `store-images/`: photographs to upload in the admin (product media, article and collection images); see INSTALL.md §46 (and §47–§54 for what is still to do).
- `store-translations/`: the store's own words in Italian and Russian, for *Settings → Languages → Import*; see INSTALL.md §46 (and §47–§54 for what is still to do).

## How it's built

- **Templates:** `index`, `collection`, `list-collections`, `product`, `blog`, `article`,
  `search`, `404`, `page` and the `page.*` templates. Each one lists `ms-*` sections,
  one per band of the preview, and renders in `layout/ms.liquid`. The store's own
  template names (`page.loro-piana-interiors`, `page.download-the-dream`,
  `page.salone-2026`, `page.sleep-assesment`, `article.*`, `blog.collaborations` and the
  24 `product.*` templates) are kept, so every page and product switches over on its own.
- **Links:** `snippets/ms-link.liquid` finds each destination by the store's real
  handles and never leads to a 404. Menus use it in strict mode, so a missing page is left
  out rather than sent to another title's page. Overrides are under Theme settings →
  Midsummer · Where links go.
- **Enquiries:** `sections/ms-enquire.liquid` (the enquiry page, on the Contact page) and
  `sections/ms-enquiry-drawer.liquid` (the sheet); `assets/ms-site.js` rewrites both
  forms for the seven enquiries.
- **Agents & resellers:** `sections/ms-stockists.liquid`, with d3 in
  `assets/ms-atlas-vendor.js` and the world in `assets/ms-world-110m.json` (fine detail,
  `ms-world-50m.json`, loads on zoom).
- **Header, footer and enquiry sheet:** `sections/ms-header.liquid` (the bar, five
  panels and the phone menu), `sections/ms-footer.liquid` and
  `sections/ms-enquiry-drawer.liquid`.
- **Site-wide rules and behaviour:** `assets/ms-site.css` and `assets/ms-site.js`.
- **Fonts:** Newsreader and Red Hat Text, in `snippets/ms-fonts.liquid` and `assets/ms-*.woff2`.
- **Languages:** every text the theme writes passes through `snippets/ms-t.liquid`, which
  finds its Italian or Russian under `ms_tx` in `locales/it.json` and `ru.json` (written by
  `scripts/build_r23.py` from `scripts/tr/src/*.txt`; product and cloth names stay as they are).
- **Stock Atelier:** everything else, used by the cart, password and gift card pages.
