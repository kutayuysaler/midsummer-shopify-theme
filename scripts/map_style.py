"""The agents map's style: OpenFreeMap's Positron (vendor/ofm-positron.json, from the OpenMapTiles
schema), made light and current: pale stone land, clear water, fresh parks, white streets on soft
casings, charcoal labels on white halos, and only the main roads warm, in the house's gold. No sprite (no
icons: road shields and airport marks go); every name is "@name", which the page sets to the
visitor's language. Written to snippets/ms-map-style.liquid as JSON, by bin/build_more.py."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
PAPER, SEA, SEA_LINE = '#F2F1ED', '#C4D9E4', '#B2CCDA'
INK, INK_SOFT, HALO = '#36332E', '#6F6A62', '#FFFFFF'
ROAD, ROAD_CASE = '#FFFFFF', '#DCD8CF'
MAJOR, MAJOR_CASE = '#FFFFFF', '#CFC9BD'
MOTOR, MOTOR_CASE = '#F6E9CF', '#DCC79E'

def style():
    st = json.load(open(os.path.join(HERE, '..', 'vendor', 'ofm-positron.json')))
    st['sources'] = {'openmaptiles': st['sources']['openmaptiles']}
    st.pop('sprite', None)
    out = []
    for L in st['layers']:
        i = L['id']
        if i.startswith('highway-shield') or i in ('road_shield_us', 'airport', 'map-custom-content-anchor'):
            continue
        lay, pa = L.setdefault('layout', {}), L.setdefault('paint', {})
        for k in [k for k in lay if k.startswith('icon-')]:
            del lay[k]
        if 'text-field' in lay:
            lay['text-field'] = '@name'
            if lay.get('text-anchor') == 'bottom' and i.startswith('label_'):
                lay['text-anchor'] = 'center'
                lay.pop('text-offset', None)
            pa['text-color'] = INK
            pa['text-halo-color'] = HALO
            pa['text-halo-width'] = 1.6
            pa.pop('text-halo-blur', None)
        if i == 'background':
            pa['background-color'] = PAPER
        elif i == 'park':
            pa['fill-color'] = '#D7E5CC'; pa['fill-opacity'] = .9
        elif i == 'water':
            pa['fill-color'] = SEA
        elif i == 'waterway':
            pa['line-color'] = SEA_LINE
        elif i == 'landcover_wood':
            pa['fill-color'] = '#D2E0C4'; pa['fill-opacity'] = .6
        elif i in ('landcover_glacier', 'landcover_ice_shelf'):
            pa['fill-color'] = '#FAFAF8'
        elif i == 'landuse_residential':
            pa['fill-color'] = '#EEEDE8'
        elif i == 'building':
            pa['fill-color'] = '#E4E1DA'; pa['fill-outline-color'] = '#D3CFC6'
        elif i.endswith('_casing') and i.startswith(('highway', 'tunnel')):
            pa['line-color'] = MOTOR_CASE if 'motorway' in i else MAJOR_CASE if 'major' in i else ROAD_CASE
        elif i.endswith('_inner') and i.startswith(('highway', 'tunnel')):
            if 'motorway' in i:
                pa['line-color'] = ['interpolate', ['linear'], ['zoom'], 5.8, 'rgba(220,199,158,0.6)', 6, MOTOR]
            else:
                pa['line-color'] = MAJOR if 'major' in i else ROAD
        elif i.endswith('_subtle'):
            pa['line-color'] = 'rgba(200,192,178,0.55)'
        elif i == 'highway_minor':
            pa['line-color'] = ROAD
        elif i == 'highway_path':
            pa['line-color'] = '#E2DED6'
        elif i.startswith('railway'):
            pa['line-color'] = '#CFCBC3' if 'dash' not in i else PAPER
        elif i.startswith('aeroway'):
            pa['line-color' if L['type'] == 'line' else 'fill-color'] = '#E8E6E1'
        elif i in ('boundary_2', 'boundary_disputed'):
            pa['line-color'] = '#B4ADA2'
        elif i == 'boundary_3':
            pa['line-color'] = '#D2CDC4'
        if i.startswith(('water_name', 'waterway_line_label')):
            pa['text-color'] = '#4F7487'
        if i.startswith('label_country'):
            pa['text-color'] = INK_SOFT
            lay['text-transform'] = 'uppercase'
            lay['text-letter-spacing'] = .18
            lay['text-font'] = ['Noto Sans Regular']
        if i.startswith('label_city') or i == 'label_town':
            pa['text-color'] = '#26231F'
        if i.startswith('highway-name'):
            pa['text-color'] = INK_SOFT
        out.append(L)
    st['layers'] = out
    st['name'] = 'Midsummer Milano'
    return st

if __name__ == '__main__':
    s = json.dumps(style(), separators=(',', ':'))
    print(len(s), 'bytes')
