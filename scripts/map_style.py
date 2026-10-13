"""The agents map's style: OpenFreeMap's Positron (vendor/ofm-positron.json, from the OpenMapTiles
schema), in the house's colours: paper land, a quiet sea, warm roads and soft labels. No sprite (no
icons: road shields and airport marks go); every name is "@name", which the page sets to the
visitor's language. Written to snippets/ms-map-style.liquid as JSON, by bin/build_more.py."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
PAPER, SEA, SEA_LINE = '#F3EEE5', '#D2DCDE', '#C3D1D5'
INK, INK_SOFT, HALO = '#5F5446', '#857865', '#F6F2EA'
ROAD, ROAD_CASE = '#FFFFFF', '#E3D7C6'

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
            pa['text-halo-width'] = 1.4
            pa.pop('text-halo-blur', None)
        if i == 'background':
            pa['background-color'] = PAPER
        elif i == 'park':
            pa['fill-color'] = '#E5E7D6'; pa['fill-opacity'] = .7
        elif i == 'water':
            pa['fill-color'] = SEA
        elif i == 'waterway':
            pa['line-color'] = SEA_LINE
        elif i == 'landcover_wood':
            pa['fill-color'] = '#E3E6D3'; pa['fill-opacity'] = .55
        elif i in ('landcover_glacier', 'landcover_ice_shelf'):
            pa['fill-color'] = '#F8F7F2'
        elif i == 'landuse_residential':
            pa['fill-color'] = '#EEE6DA'
        elif i == 'building':
            pa['fill-color'] = '#E7DED0'; pa['fill-outline-color'] = '#D9CDBC'
        elif i.endswith('_casing') and i.startswith(('highway', 'tunnel')):
            pa['line-color'] = ROAD_CASE
        elif i.endswith('_inner') and i.startswith(('highway', 'tunnel')):
            if i == 'highway_motorway_inner':
                pa['line-color'] = ['interpolate', ['linear'], ['zoom'], 5.8, 'rgba(214,201,182,0.6)', 6, ROAD]
            else:
                pa['line-color'] = ROAD
        elif i.endswith('_subtle'):
            pa['line-color'] = 'rgba(205,190,170,0.55)'
        elif i == 'highway_minor':
            pa['line-color'] = ROAD
        elif i == 'highway_path':
            pa['line-color'] = '#E6DCCD'
        elif i.startswith('railway'):
            pa['line-color'] = '#D8CEC0' if 'dash' not in i else PAPER
        elif i.startswith('aeroway'):
            pa['line-color' if L['type'] == 'line' else 'fill-color'] = '#EAE3D8'
        elif i in ('boundary_2', 'boundary_disputed'):
            pa['line-color'] = '#BCAE98'
        elif i == 'boundary_3':
            pa['line-color'] = '#D3C8B7'
        if i.startswith(('water_name', 'waterway_line_label')):
            pa['text-color'] = '#7A9197'
        if i.startswith('label_country'):
            pa['text-color'] = INK_SOFT
            lay['text-transform'] = 'uppercase'
            lay['text-letter-spacing'] = .18
            lay['text-font'] = ['Noto Sans Regular']
        if i.startswith('label_city') or i == 'label_town':
            pa['text-color'] = '#3E352C'
        if i.startswith('highway-name'):
            pa['text-color'] = INK_SOFT
        out.append(L)
    st['layers'] = out
    st['name'] = 'Midsummer Milano'
    return st

if __name__ == '__main__':
    s = json.dumps(style(), separators=(',', ':'))
    print(len(s), 'bytes')
