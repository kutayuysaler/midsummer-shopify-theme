// a dot-matrix world for the fibre atlas's "Where it comes from": dots on land, equirectangular,
// latitudes 75N to 58S. usage: NODE_PATH=../../geo/node_modules node dotworld.js countries-110m.json out.svg
const fs = require('fs');
const { feature, merge } = require('topojson-client');
const d3 = require('d3-geo');
const [SRC, OUT] = process.argv.slice(2);
const topo = JSON.parse(fs.readFileSync(SRC));
const land = merge(topo, topo.objects.countries.geometries.filter(g => g.id !== '010'));   // no Antarctica
const N = 75, S = -58, W = 1000, H = Math.round(W * (N - S) / 360);
const step = 7.4;
let dots = '';
for (let y = step / 2; y < H; y += step) {
  for (let x = step / 2; x < W; x += step) {
    const lon = x / W * 360 - 180, lat = N - y / H * (N - S);
    if (d3.geoContains(land, [lon, lat])) dots += `M${x.toFixed(1)} ${y.toFixed(1)}h0`;
  }
}
const svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}"><path d="${dots}" stroke="#B9AA94" stroke-width="3.1" stroke-linecap="round" fill="none"/></svg>`;
fs.writeFileSync(OUT, svg);
console.log('dots', (svg.length / 1024).toFixed(0) + 'KB', W, H);
