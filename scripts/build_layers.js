// The agents map's close-up detail: what a printed atlas shows of a region, from Natural Earth 1:10m
// (public domain): the sea's depth contours, the towns' built-up areas, motorways and main roads,
// railways, regional boundaries, rivers, and the names of the mountain ranges. Only around the
// places (Europe, the American east coast, Hong Kong); loaded once the visitor zooms into a region.
// usage: NODE_PATH=../geo/node_modules node build_layers.js ../dl/ne10b ../vendor/ms-world-layers.json
const fs = require('fs'), path = require('path');
const { topology } = require('topojson-server');
const { presimplify, simplify, sphericalTriangleArea } = require('topojson-simplify');
const { quantize } = require('topojson-client');
const d3 = require('d3-geo');
const [DIR, OUT] = process.argv.slice(2);
const read = n => JSON.parse(fs.readFileSync(path.join(DIR, n + '.geojson'))).features.filter(f => f.geometry);

const REGIONS = [[-12, 34, 44, 63], [-86, 22.5, -62, 50.5], [110, 19, 118.5, 26]];
const inR = ([x, y]) => REGIONS.some(([a, b, c, d]) => x >= a && x <= c && y >= b && y <= d);
// close around the places themselves, where the finest layers (main roads, railways, regions) are kept
const TIGHT = [[5, 36, 19.5, 48], [-6.5, 49.5, 2.5, 55.5], [14, 49, 25, 55], [33, 53.5, 42, 58], [-83, 24.3, -78.5, 29.7], [-75.8, 44.3, -71.3, 46.8], [113, 21.6, 115.2, 23]];

// a line cut to the regions: the pieces inside each rectangle (Liang–Barsky, segment by segment)
function clipSeg(p, q, [x0, y0, x1, y1]) {
  let t0 = 0, t1 = 1;
  const dx = q[0] - p[0], dy = q[1] - p[1];
  const P = [-dx, dx, -dy, dy], Q = [p[0] - x0, x1 - p[0], p[1] - y0, y1 - p[1]];
  for (let i = 0; i < 4; i++) {
    if (P[i] === 0) { if (Q[i] < 0) return null; continue; }
    const r = Q[i] / P[i];
    if (P[i] < 0) { if (r > t1) return null; if (r > t0) t0 = r; } else { if (r < t0) return null; if (r < t1) t1 = r; }
  }
  return [[p[0] + t0 * dx, p[1] + t0 * dy], [p[0] + t1 * dx, p[1] + t1 * dy]];
}
function clipLine(coords, rects) {
  const out = [];
  (rects || REGIONS).forEach(rect => {
    let cur = null;
    for (let i = 1; i < coords.length; i++) {
      const s = clipSeg(coords[i - 1], coords[i], rect);
      if (!s) { if (cur && cur.length > 1) out.push(cur); cur = null; continue; }
      if (cur && Math.abs(cur[cur.length - 1][0] - s[0][0]) < 1e-9 && Math.abs(cur[cur.length - 1][1] - s[0][1]) < 1e-9) cur.push(s[1]);
      else { if (cur && cur.length > 1) out.push(cur); cur = [s[0], s[1]]; }
    }
    if (cur && cur.length > 1) out.push(cur);
  });
  return out;
}
function lines(geom) {
  const g = geom.type;
  if (g === 'LineString') return [geom.coordinates];
  if (g === 'MultiLineString') return geom.coordinates;
  if (g === 'Polygon') return geom.coordinates;
  if (g === 'MultiPolygon') return geom.coordinates.flat();
  return [];
}
function asLines(features, keep, props, rects) {
  const out = [];
  features.forEach(f => {
    if (keep && !keep(f.properties)) return;
    const parts = lines(f.geometry).flatMap(l => clipLine(l, rects));
    if (parts.length) out.push({ type: 'Feature', properties: props ? props(f.properties) : {}, geometry: { type: 'MultiLineString', coordinates: parts } });
  });
  return { type: 'FeatureCollection', features: out };
}
const anyIn = geom => lines(geom).some(l => l.some(inR));

// the sea floor: contours at 200, 1,000, 2,000 and 3,000 metres
const depth = {};
[['K_200', 'd200'], ['J_1000', 'd1000'], ['I_2000', 'd2000'], ['H_3000', 'd3000']].forEach(([n, k]) => { depth[k] = asLines(read('ne_10m_bathymetry_' + n)); });

// built-up areas: the towns' own shapes
const urban = { type: 'FeatureCollection', features: read('ne_10m_urban_areas').filter(f => anyIn(f.geometry)).map(f => ({ type: 'Feature', properties: {}, geometry: f.geometry })) };

// roads: motorways and ring roads, then the main roads
const roadsAll = read('ne_10m_roads');
const major = asLines(roadsAll, p => p.type === 'Major Highway' || p.type === 'Beltway' || (p.expressway === 1 && p.type !== 'Ferry Route'));
const minor = asLines(roadsAll, p => (p.type === 'Secondary Highway' || p.type === 'Road') && p.expressway !== 1 && p.scalerank <= 8, null, TIGHT);
const rail = asLines(read('ne_10m_railroads'), p => p.scalerank <= 7, null, TIGHT);
const states = asLines(read('ne_10m_admin_1_states_provinces_lines'), null, null, TIGHT);

// rivers: the main ones a little stronger
const rv = read('ne_10m_rivers_lake_centerlines_scale_rank').concat(read('ne_10m_rivers_europe'), read('ne_10m_rivers_north_america'))
  .filter(f => !/Lake Centerline/.test(f.properties.featurecla || ''));
const rivers1 = asLines(rv, p => (p.scalerank || 10) <= 6);
const rivers2 = asLines(rv, p => (p.scalerank || 10) > 6 && (p.scalerank || 10) <= 10);

// mountain ranges, named in italic where there is room
const ranges = read('ne_10m_geography_regions_polys').filter(f => f.properties.FEATURECLA === 'Range/mtn').map(f => {
  const c = d3.geoCentroid(f);
  return [f.properties.NAME_EN || f.properties.NAME, +c[0].toFixed(3), +c[1].toFixed(3), f.properties.SCALERANK || 6];
}).filter(r => inR([r[1], r[2]]) && r[0]);

// simplified on the sphere to what the closest view (zoom 10) can show, then quantised
let topo = topology({ urban, major, minor, rail, states, rivers1, rivers2, ...depth });
topo = presimplify(topo, sphericalTriangleArea);
const MIN = +(process.env.MIN || 4e-10);
topo = simplify(topo, MIN);
topo.arcs = topo.arcs.map(a => a.map(p => [p[0], p[1]]));
topo = quantize(topo, +(process.env.Q || 4e5));
topo.ranges = ranges.sort((a, b) => a[3] - b[3]);
fs.writeFileSync(OUT, JSON.stringify(topo));
const count = k => topo.objects[k].geometries.length;
console.log('layers', (fs.statSync(OUT).size / 1024).toFixed(0) + 'KB', Object.keys(topo.objects).map(k => k + ' ' + count(k)).join(', '), 'ranges', ranges.length,
  'points', topo.arcs.reduce((n, a) => n + a.length, 0));
