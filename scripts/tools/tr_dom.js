// text still in English after the page's scripts have run (rt5/<locale>/*.html, marked dummy translation):
// visible text, aria-label, title, placeholder; anything with English words and no ⟪…⟫ mark.
// usage: LOC=it node tools/tr_dom.js > report
const { chromium } = require('playwright-core');
const http = require('http'), fs = require('fs'), path = require('path');
const ROOT = path.join(__dirname, '..'), LOC = process.env.LOC || 'it';
const types = { svg: 'image/svg+xml', jpg: 'image/jpeg', png: 'image/png', webp: 'image/webp', js: 'text/javascript', css: 'text/css', woff2: 'font/woff2', html: 'text/html', json: 'application/json' };
const srv = http.createServer((q, r) => { let u = decodeURIComponent(q.url.split('?')[0]); if (u.startsWith('/theme/')) u = '/v5/' + u.slice(7); u = u.replace(/^(\/v5\/assets\/.+)_\d+x(\.(?:jpe?g|png))$/i, '$1$2');
  fs.readFile(path.join(ROOT, u), (e, d) => { if (e) { r.writeHead(404); r.end(); return; } r.writeHead(200, { 'content-type': types[u.split('.').pop()] || 'application/octet-stream' }); r.end(d); }); }).listen(8798);
const EN = /\b(the|and|of|with|for|your|our|by|to|is|are|from|each|every|bed|beds|mattress|topper|more|see|all|book|enquir\w*|request|view|read|open|close|next|previous|back|made|hand|sleep|natural|fibres?|wool|silk|linen|cotton|size|sizes|collection|collections|cloth|colours?|price|order|contact|journal|showroom|atelier|phone|message|name|email|send|select|optional|notes?)\b/i;
const pages = (process.env.ONLY ? process.env.ONLY.split(',').map(x => x + '.html') : fs.readdirSync(path.join(ROOT, 'rt5', LOC)).filter(f => f.endsWith('.html')));
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const agg = {};
  for (const w of [1440, 390]) {
    const ctx = await b.newContext({ viewport: { width: w, height: 900 } });
    for (const f of pages) {
      const p = await ctx.newPage();
      await p.route(/^https?:\/\/(?!127\.0\.0\.1)/, r => r.abort());
      try { await p.goto('http://127.0.0.1:8798/rt5/' + LOC + '/' + f, { waitUntil: 'load', timeout: 30000 }); } catch (e) { await p.close(); continue; }
      await p.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 700) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 30)); } });
      await p.waitForTimeout(250);
      const got = await p.evaluate(() => {
        const out = [];
        const tw = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
        let n;
        while ((n = tw.nextNode())) {
          const t = n.nodeValue.replace(/\s+/g, ' ').trim();
          if (!t || t.length < 3) continue;
          const el = n.parentElement; if (!el || el.closest('script,style,noscript,template')) continue;
          const r = el.getBoundingClientRect(), s = getComputedStyle(el);
          if (!(r.width > 0 && r.height > 0) || s.visibility === 'hidden') continue;
          out.push(['text', t]);
        }
        document.querySelectorAll('[aria-label],[title],[placeholder],img[alt]').forEach(el => { for (const a of ['aria-label', 'title', 'placeholder', 'alt']) { const v = el.getAttribute(a); if (v && v.trim()) out.push(['@' + a, v.trim()]); } });
        return out;
      });
      for (const [k, t] of got) { if (/[⟪⟫]/.test(t) || !EN.test(t)) continue; const key = k + '\t' + t.slice(0, 140); (agg[key] = agg[key] || new Set()).add(f.replace('.html', '') + '@' + w); }
      await p.close();
    }
    await ctx.close();
  }
  await b.close(); srv.close();
  Object.entries(agg).sort((a, b) => b[1].size - a[1].size).forEach(([k, s]) => console.log(String(s.size).padStart(3), k, '  [' + [...s].slice(0, 3).join(' ') + ']'));
})();
