# Midsummer Milano: Shopify theme

The approved Atelier preview (`Midsummer Atelier - Preview.html`), built as a Shopify
theme on the store's Atelier 4.1.5 export.

- `midsummer-milano-atelier.zip`: upload this file as it is, under Online Store → Themes → Add theme → Upload zip file.
- `theme/`: the same theme as source files.
- `INSTALL.md`: page templates, and the store data the design reads.

## How it's built

- **Templates:** `index`, `collection`, `list-collections`, `product`, `blog`, `article`,
  `search`, `404`, `page` and the `page.*` templates. Each one lists `ms-*` sections,
  one per band of the preview, and renders in `layout/ms.liquid`. The store's own
  template names (`page.loro-piana-interiors`, `page.download-the-dream`,
  `page.salone-2026`, `page.sleep-assesment`, `article.*`, `blog.collaborations` and the
  24 `product.*` templates) are kept, so every page and product switches over on its own.
- **Links:** `snippets/ms-link.liquid` finds each destination by the store's real
  handles and never leads to a 404.
- **Header, footer and enquiry sheet:** `sections/ms-header.liquid` (the bar, five
  panels and the phone menu), `sections/ms-footer.liquid` and
  `sections/ms-enquiry-drawer.liquid`.
- **Site-wide rules and behaviour:** `assets/ms-site.css` and `assets/ms-site.js`.
- **Fonts:** Newsreader and Red Hat Text, in `snippets/ms-fonts.liquid` and `assets/ms-*.woff2`.
- **Stock Atelier:** everything else, used by the cart, password and gift card pages.
