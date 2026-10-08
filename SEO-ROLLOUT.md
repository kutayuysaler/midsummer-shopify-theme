# Midsummer Milano: search and AI-search rollout

What the AI Search Audit (6 October 2026), the AI SEO review (*Revisione e integrazioni*) and
the Google Search Console export say, what the new theme already fixes, and what is left to
do before and after launch.

## 1. Reading the Search Console export

About 1,000 pages are indexed. The site gets roughly 1,000–1,200 impressions a day, with a
peak of 2,958 on 17 July. On 15 September, the number of not-indexed pages jumped from
2,939 to 4,643.

| Reason | Pages | What it means | Action |
| --- | ---: | --- | --- |
| Alternate page with proper canonical tag | 3,726 | Mostly the Italian and Russian copies of each page, product URLs reached through a collection, and `?view=` / filter / sort variants. Google is following the canonical, as it should. | None for most of them. Running `create_pages.py` stops the `?view=` variants, and the new theme links products by their canonical URL. Check that the canonical pages themselves are indexed. |
| Crawled – currently not indexed | 483 | Google read these and judged them not worth indexing: typically thin or untranslated language copies, tag pages, old posts, near-duplicate pages. | Translate or unpublish the language copies (§3); tag pages are now `noindex`; the per-URL export says which posts to improve or merge. |
| Discovered – currently not indexed | 168 | Known, not yet crawled. | Should fall once the thin copies are gone; submit the sitemap again after launch. |
| Page with redirect | 109 | Old URLs that redirect. | Fine, as long as menus and internal links point at the final URLs (the new theme's do). |
| Not found (404) | 37 | Broken URLs that someone links to. | Needs the per-URL list (§3, step 7). |
| Excluded by 'noindex' | 10 | Utility pages (search, quote pages, `/collections/all`, …). | Check the list is only utility pages. |
| Server error (5xx) | 5 | Usually passing Shopify hiccups. | Validate the fix in Search Console; if they repeat, they are app pages. |
| Blocked by robots.txt | 5 | Shopify's own rules (cart, checkout, internal search). | None. |
| Other 4xx | 2 | Typically password or app pages. | Check in the per-URL list. |
| Duplicate, Google chose a different canonical | 1 | One page Google merges with another. | Check which in the per-URL list. |

**The 15 September jump** is almost certainly new URLs, not pages lost: a language
published without translations, an app generating pages, or new tag or filter URLs. The
per-URL export of *Crawled – currently not indexed* answers it in a minute.

**What I need from Search Console:** in **Indexing → Pages**, open each reason, click
**Export**, and send the files. These matter most: *Not found (404)*, *Crawled – currently
not indexed*, and *Duplicate, Google chose different canonical*. With them I can write the
redirect file and say exactly which pages to fix, merge or drop.

## 2. What the new theme already does

| Audit / review item | In the new theme |
| --- | --- |
| Article author | Unchanged, as you decided: the author is whatever the article says in Shopify. |
| Duplicate Article schema | The theme outputs one `BlogPosting` per note. The second copy came from the Avada SEO and SEOon Blog apps; their app embeds are off in the theme (§3). |
| FAQPage on Sleep Wise | Done: the questions page is marked up as `FAQPage`. |
| Organization incomplete | `foundingDate` 2014, founder, `sameAs` (Instagram, Pinterest, LinkedIn, Telegram, VK), VAT number, the Green Product Award, map link, and "by appointment" in the description. All are editable in the *Structured data* section of the header. |
| LocalBusiness for the showroom | The organisation is also a `FurnitureStore`, with the Via Andegari address, coordinates and opening hours. |
| Product pages: one-word H1 | The heading now says what the product is: *Vivaldi – Natural-fibre sleep system, handmade in Italy*, or *Capri – Boxspring and mattress* (the line under the name). It can be set per template, or per product with the metafield `custom.kind`. |
| Product pages: no specifications | The facts under the buttons are now a specification sheet: made, dimensions, standard sizes (from the product's Size option), upholstery, comfort, service. Height and lead time appear when the metafields `custom.height` and `custom.lead_time` are filled in. Nothing about the inside of the bed is listed. |
| Product pages: no product FAQ | Every bed has *Before you order*: what it is made of (its own fibres), dimensions, comfort, trying it, lead time, price, 15 + 15. Each is marked up as `FAQPage`. |
| Product schema: no availability or materials | `Product` with its fibres as `material`, the specification rows, `countryOfOrigin` Italy and the award on Top. When prices are shown, it adds `offers` with the price (or the from–to range) and `MadeToOrder` availability. While prices are hidden, no offer is given, so the data never says more than the page. With *Show a starting price while prices are hidden*, the data gives the lowest price as an `AggregateOffer`. |
| Italian homepage with an English H1 | The home hero and the product page labels now have their own Italian and Russian text in the theme. Everything else is translated in Translate & Adapt (§3, step 4). |
| Article dates not visible | Every note shows its date, and "Updated …" when it was revised. |
| llms.txt | `/?view=llms` is a brand overview, built live from the store. There is also a new **Midsummer Milano at a glance** page, a plain fact sheet for people, press and AI assistants, linked from the footer. Shopify generates `/llms.txt` itself, so check whether it can be redirected (§3, step 8). |
| Green Product Award not on About | *Our story* now ends with Recognition & press: the award first, with a link to the award's own page, then the publications. |
| Loro Piana Interiors naming | Always the full name, "Loro Piana Interiors". |
| "Vegan mattresses" | The theme says nothing about vegan beds. |
| AI crawlers | `robots.txt` keeps Shopify's own rules, so GPTBot, OAI-SearchBot, ClaudeBot, PerplexityBot and Google-Extended are allowed. It points to the fact sheet and the overview. All text is in the HTML, not loaded later. |
| `/collections/x/products/y` duplicates | The theme links every product by its canonical `/products/…` address. |
| Tag pages | Journal tag listings are `noindex, follow` (a bug stopped this before; it is fixed). |
| AI referral measurement | New event `ms_ai_referral` (§4). |

## 3. Launch checklist

Already done in the theme (nothing to do):

- **Prices** stay on request (§6). *Theme settings → Show a starting price while prices are
  hidden* adds "From €…" under "On request" and gives search engines that starting price,
  if you ever want it.
- **App embeds** are preset as on the live theme. Turned on: Tipo Appointment, Appointo and
  Mailchimp. Turned off: Avada SEO Suite and SEOon Blog, whose structured data would repeat
  the theme's. If you rely on another Avada or SEOon feature, turn its embed back on and
  switch off only its structured data / JSON-LD in the app.
- **Fibres** are now listed for Amalfi (linen), Monteverdi (cashmere, camel hair) and Ultra
  Dry (vegetable horsehair), on the page, in *Before you order* and in the structured
  data. **Bellini** still has none: tell me its fibres, or add them in the theme editor
  (*Product · The system → Add Fibre*).
- **Founding year 2014** is kept, as in the audit.

In Shopify, in this order:

1. **Upload** `midsummer-milano-atelier.zip`, preview, then publish (INSTALL.md §1).
2. **App embeds:** open *Customize → App embeds* once and check that the list matches the one
   above.
3. **Pages:** run `scripts/create_pages.py` (INSTALL.md §3), or create the pages by hand
   from the table there. Every designed page then has its own address and template. Until
   a page exists, its menu entry opens a stand-in that is kept out of Google. The script
   lists what it set and what it created, and writes a search description for each page
   it creates.
4. **Translations.** In **Translate & Adapt**, translate the theme content for Italian and
   Russian: section texts, the product questions, the At a glance page. The quickest way:
   *Export* the Italian and Russian CSV files, send them to me, I fill them in, and you
   *Import* them back. A language left half in English is the most likely cause of
   *Crawled – currently not indexed*. If a language cannot be ready by launch, unpublish
   it in **Settings → Languages** rather than leave it in English.
5. **Products.** For each bed, fill the **Search engine listing** title and description in
   this form: *Vivaldi – Handmade natural-fibre mattress | Midsummer Milano*. Optional
   metafields: `custom.kind` (overrides the line under the name), `custom.height`,
   `custom.lead_time`, `custom.firmness`.
6. **Vivaldi and Bellagio:** publish them (their templates are ready). The MOHD draft says
   their pages are coming; if you would rather retire them, change that line before
   sending.
7. **Redirects.** In Search Console, open **Indexing → Pages → Not found (404)** and click
   **Export**, then send me the file. I return a CSV (*Redirect from*, *Redirect to*) to
   import under **Online Store → Navigation → URL redirects → Import**.
8. **llms.txt.** Open `https://midsummer-milano.com/llms.txt`. If it is Shopify's generic
   file, add a URL redirect from `/llms.txt` to `/?view=llms`. If Shopify keeps its own
   file, leave it: the overview and the fact sheet are linked from `robots.txt` and the
   footer anyway.
9. **Search Console, after publishing:** in **Sitemaps**, submit `sitemap.xml` again. Then
   use URL Inspection → *Request indexing* on the home page, the three collections, the
   top ten products, At a glance, Questions and Our story.
10. **Outreach** (§5): three drafts are waiting in Gmail. They are the MOHD follow-up (in
    the price thread), the Italian resellers and the international resellers (both in
    BCC). Send them once the site is live. On **1stdibs**, edit the listings yourself in
    the seller account: current names and descriptions, "Price on request", and a link to
    the official site where the form allows one.

**Doing the Shopify steps from Claude next time.** This session could not reach the store,
because the environment's network policy blocks `*.myshopify.com` and
`midsummer-milano.com`. In the Claude Code environment settings, add those hosts under
*Network access*, and add the variables `SHOPIFY_STORE` (`your-store.myshopify.com`) and
`SHOPIFY_ADMIN_TOKEN` (the token from INSTALL.md §3). In a new session, Claude can then run
the page script, import redirects and check the live pages.

## 4. Measuring it

**Search Console (weekly)**

- Indexed pages: up, steadily.
- *Crawled – currently not indexed*: down.
- Impressions and clicks for brand queries ("midsummer milano", "midsummer milano
  mattress", "midsummer materassi").
- Impressions and clicks for category queries ("handmade horsehair mattress", "materasso
  crine fatto a mano", "luxury natural mattress Milan").

**GA4 (monthly)**

The theme pushes `ms_ai_referral` once per visit that comes from ChatGPT, Perplexity,
Gemini, Claude, Copilot and similar (by referrer, or `utm_source=chatgpt.com`). It also
adds `ai_source` to the enquiry events that follow.

- In Google Tag Manager, forward the event to GA4.
- In GA4, register `ai_source` as an event-scoped custom dimension.
- Mark `ms_enquiry_submit` as a key event.

Without Tag Manager, a GA4 exploration with *Session source* matching
`chatgpt|perplexity|gemini|claude|copilot` gives the visits, but not the enquiries.

**Monthly AI test** (15 minutes)

Ask the same questions each month in ChatGPT, Perplexity, Gemini and Claude. For each
answer, note whether Midsummer is named, which site is cited (the official site, MOHD or
1stdibs), and whether the facts are right.

1. What is Midsummer Milano?
2. Who makes Midsummer Milano mattresses, and where?
3. Best handmade natural-fibre mattress in Italy?
4. Luxury horsehair mattress, handmade, Milan?
5. Materasso naturale in lana e crine fatto a mano a Milano?
6. Which mattress brands use Loro Piana Interiors fabrics?
7. What is the Midsummer Milano 15 + 15 service?
8. How much does a Midsummer Milano mattress cost?
9. Midsummer Milano Vivaldi: what is it made of?
10. Where can I try a Midsummer Milano bed in London / New York / Hong Kong?
11. Green Product Award 2025 bed system?
12. Handmade beds for luxury hotels, Italy?

## 5. Off-site: the real gap

The audit's main finding: for "Midsummer Milano mattress", MOHD and 1stdibs rank above the
official site, and MOHD lists products (Vivaldi, Bellagio) the site does not show.

- **MOHD and 1stdibs.** Ask them to use the current names, materials and descriptions, and
  to link to the official product page. Either publish Vivaldi and Bellagio on the site
  (the theme already has their templates), or ask MOHD to retire them.
- **Every agent and reseller** (the 15 on the map): the same request, with a link to the
  official site.
- **Google Business Profile** for the atelier, with exactly the name, address, hours and
  phone the site uses.
- **Design directories** (Archiproducts, Architonic and similar): a brand profile with a
  link.
- **Third-party mentions:** the Green Product Award page should link to the site;
  documented hotel projects, trade press, and Salone del Mobile coverage.
- **Optional:** a Wikidata entry for the company (founding date, founder, website,
  headquarters). AI assistants draw on it.

## 6. Decisions taken

1. **Prices stay on request.** On 21 September the house asked MOHD to replace prices with
   "Price on request", so the site does the same. The structured data then gives no
   price, so it never says more than the page. The starting-price option (§3) is there if
   you change your mind. Ask MOHD and the resellers to hide prices too (the drafts do), or
   AI assistants keep quoting theirs.
2. **Founding year 2014**, as in the audit.
3. **Vivaldi and Bellagio:** publish them on the site, rather than ask MOHD to remove
   them.
4. **Map tiles:** OpenStreetMap, with its credit (INSTALL.md §24).
5. **Still with the house:** a final read of the product questions, the fact sheet and the
   translations by someone at the house, and Bellini's fibres.
