# Changes from the Claude Design export

## Round 2 — after the first upload showed a 404 with no header

**What most likely happened.** Shopify validates section schemas on upload more strictly than
Theme Check does, and would reject two custom sections:

- `ms-dimensions`: a `url` setting defaulted to `/pages/contact`. Shopify only
  allows `/collections` or `/collections/all` as a url default.
- `ms-seo`: a `text` setting had an empty-string default.

Every JSON file that references a rejected section is rejected too. `ms-seo` sat in the
header group, so the whole header group was dropped, which is why the preview had no
header. Templates that use only Atelier's own sections, such as the 404, uploaded and
rendered. The grey illustration in that preview is Shopify's placeholder for
`ms-graded-dune.jpg`, which appears once the Files upload (INSTALL step 1) is done.

**What changed, following how the live Dawn theme is built:**

- Both defaults are fixed. Every custom schema has also been checked against
  Shopify's server-side rules: url defaults, empty defaults, labels, ids, lengths, and
  Liquid parsed with the real Liquid gem in strict mode.
- The header and footer groups now contain only Atelier's own sections. The enquiry
  panel, structured data, photographic grade and tracking are static sections rendered
  from `layout/theme.liquid`, exactly as the live theme renders `enquire-panel`. A
  problem in custom code can no longer remove the header or footer.
- Integrations from the live theme that the export had dropped are ported:
  - Google Tag Manager (head and noscript), HubSpot, iubenda (`iub-cookie-banner`)
    and Avada SEO (its snippets, included the way the live theme includes them).
  - `robots.txt.liquid` and `search.avada-seo.liquid`.
  - In `snippets/meta-tags.liquid`: the audit's SEO fixes (policy canonicals,
    noindex for utility pages and `/collections/all`, brand-suffixed titles, meta
    description fallbacks, the article `og:image`). `og:price` is now withheld while
    prices are hidden.
- The 11 app embeds (8 enabled) from the live `settings_data.json` are kept, so
  publishing doesn't switch any app off.
- `page.agents-and-resellers` is renamed `page.agents-resellers`, the template the
  live page is already assigned, so the map appears without reassigning it.

## Round 1

Source: `export/midsummer-atelier-theme.zip` (Atelier 4.1.5 plus the Midsummer build),
which is byte-identical to the Drive folder `midsummer-atelier-theme/`. Stock Atelier
code was left alone except where noted. All Midsummer code lives in the `ms-*` and
`_ms-*` files, the templates, the section groups and `config/`.

## Validation

- **Shopify Theme Check** (CLI 4.8, full rule set): 0 errors. The 6 warnings left are
  in untouched stock Atelier files (`header.liquid` has 42 settings, and
  `divider.liquid` has doc params).
- **Schema validation of every setting value** in all 18 templates, both section groups
  and `settings_data.json`, checked the way Shopify validates on upload: select
  options, range bounds and steps, block types and nesting, and section and block
  limits. It found **227 invalid values** in the export, and all are fixed. Theme
  Check doesn't catch these; Shopify rejects the file on upload.
- **Rendered and run in Chromium** with the real template data: the quiz end to end,
  the enquiry panel (open, tabs, required fields, Escape), all five dataLayer events,
  the stockists map (177 countries, 22 markets, select-to-zoom), and every JSON-LD graph
  parsed.

## Fixes that would have blocked the upload

| File | Problem | Fix |
| --- | --- | --- |
| `blocks/ms-materials.liquid` | A theme block declared local child blocks with settings, which Shopify rejects (and `block.blocks` doesn't exist in theme blocks) | Children are now `blocks/_ms-material.liquid`, rendered with `content_for 'blocks'`, and `product.json` is retyped to match |
| `config/settings_data.json` | Type sizes 15/96/38/22/11 px, `icon_stroke: "1"`, `card_title_case: "none"` and `variant_button_width: "fit"` aren't valid options | Added 11, 15, 22, 38 and 96 px as type-size options in `settings_schema.json`, so the approved scale is kept exactly, and mapped the others to their equivalents (thin, default, default-width) |
| 10 section schemas | Templates use 120–160 px section padding; the schema maximum is 100 | `padding-block-*` is widened to 0–200 in steps of 2 (Shopify caps a range at 101 steps) in `section`, `main-page`, `main-404`, `main-blog`, `main-collection`, `main-collection-list`, `featured-blog-posts`, `product-list`, `product-recommendations` and `search-results` |
| `blocks/icon.liquid`, `snippets/icon.liquid` | Icons `bed`, `gem`, `hand` and `wrench` don't exist | Drawn in Atelier's 20 × 20 line style and added as options |
| `sections/hero.liquid` | `gradient_direction: "to right"` isn't an option | Added *Right* and *Left*; the overlay already passes the value to `linear-gradient()` |
| Templates | `type_preset: "paragraph-small"` on 16 caption and descriptor blocks | Captions are now italic Newsreader at 1rem (as in the approved preview), and descriptors Red Hat Text at 0.875rem |
| Templates | `border: "top"` on two groups, 11px menu type, a 5:6 menu image ratio, 78cqw/64px/"medium" card values, a "link" button style, and unknown `alignment`/`padding` keys on icon blocks | Group top rules are now real `_divider` blocks, and the other values are mapped to the nearest valid option or removed |

## Bugs fixed

- **The Find Your Midsummer quiz never worked.** Four of the five questions have three
  answers, and the Liquid wrote a trailing comma after the last one (`},]`), so
  `JSON.parse` failed and the quiz rendered an empty question. The comma is now tracked
  with a separator variable.
- **`ms_quiz_complete` never fired.** The tracking listened for `ms:quiz-complete`,
  which the quiz never dispatched. The quiz now dispatches it with the recommendation.
- **`ms_enquiry_open` missed most opens.** Opens from ordinary links to
  `/pages/contact`, which is most CTAs, were logged only as `ms_cta_click`. The panel
  now announces every visitor-triggered open.
- **The enquiry panel popped open over the Contact page.** After someone submitted the
  page's own form, the panel opened on `contact_posted=true` too. The panel form now
  has its own id (`#ms-enquiry-form`) and reopens only for its own submissions, or for
  submissions made away from the Contact page.
- **Prices leaked on a price-on-request site.** They appeared in the predictive-search
  dropdown, mega-menu product cards and the cart page, and in Google's data through
  Atelier's native Product JSON-LD, which also duplicated the Midsummer Product graph. A
  new theme setting, *Enquiry-led commerce → Show prices* (off), gates
  `snippets/price.liquid`. `ms-seo` is now the single Product graph and reads the same
  switch.
- **Missing translation keys.** `accessibility.zoom_in`, `zoom_out`, `reset` and
  `attribute` rendered as "translation missing" in screen-reader labels. They're now
  added to all 34 storefront locale files.
- **The map broke on a decimal comma.** Market coordinates are free text, so
  `45,4642` produced invalid JSON and an empty map. Both `.` and `,` are now accepted.
- **FAQ structured data was emitted on three pages.** It's now emitted only on the FAQ
  page, following Google's guidance to mark up repeated FAQ content once.
- **Two stock Unsplash photos were still in use.** One was captioned "Via Andegari 4,
  Milano." They're replaced with `Paisleydettaglio.jpg` (Contact, as in the approved
  preview) and `ms-graded-ochre-room.jpg` (Hospitality).
- **Links now use the live handles** that the original notes say must be kept:
  `/pages/natural-luxury-materials`, `/pages/midsummer-milanos-regeneration-service` and
  `/blogs/news`.

## Performance and privacy

- **Stockists map**: the page loaded all of d3 (~280 KB) and topojson from unpkg as
  render-blocking scripts and fetched the world geometry from jsdelivr at runtime.
  These are replaced by `assets/ms-atlas-vendor.js`, a 72 KB bundle (25 KB gzipped)
  of only the d3 modules the map uses (licences included), loaded with `defer`, and
  `assets/ms-world-110m.json` with the unused land layer stripped. The page now makes
  **zero third-party requests**, so visitor IPs no longer go to US CDNs.
- **Quiz**: the first question's photograph is rendered server-side, with width and
  height, instead of an empty `<img>` that JavaScript filled in later.
- **Precious materials**: the empty-icon squares now show only in the theme editor, not
  to visitors.
- `layout/theme.liquid`: the `ms-motion.js` include is tidied and commented; it's still
  deferred.
