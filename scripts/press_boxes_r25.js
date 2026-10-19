// Round 25: each press mark (SVG) drawn large on a clear ground, so that scripts/press_trim_r25.py
// can find the ink and trim the mark's viewBox to it.
// usage: NODE_PATH=/opt/node22/lib/node_modules node tools/press_boxes_r25.js <dir of svgs> <out dir>
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
(async () => {
  const [src, out] = process.argv.slice(2);
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 2200, height: 1600 } });
  for (const f of fs.readdirSync(src).filter(f => f.endsWith('.svg')).sort()) {
    const data = 'data:image/svg+xml;base64,' + fs.readFileSync(path.join(src, f)).toString('base64');
    await p.setContent(`<body style="margin:0;background:transparent"><img id="i" src="${data}" style="display:block;width:2000px;height:auto"></body>`);
    await p.waitForFunction(() => document.getElementById('i').complete);
    const box = await p.evaluate(() => { const r = document.getElementById('i').getBoundingClientRect(); return [r.width, r.height]; });
    await p.locator('#i').screenshot({ path: path.join(out, f.replace(/\.svg$/, '.png')), omitBackground: true });
    console.log(f, box.map(Math.round).join('x'));
  }
  await b.close();
})();
