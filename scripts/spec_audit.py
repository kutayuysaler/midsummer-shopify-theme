# the site's fibres per system (lp_data.FIBRES) and per part (lp_data.CRAFT) against the 2026 catalogue
import sys, os
SP = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, SP + '/bin'); sys.path.insert(0, SP + '/scripts')
from lp_data import FIBRES, CRAFT
from catalogue_2026 import CAT
bad = 0
for k, parts in CAT.items():
    whole = set().union(*parts.values())
    have = set(FIBRES.get(k, []))
    if have != whole:
        bad += 1; print('%-14s fibres: site has %s; catalogue has %s' % (k, sorted(have - whole) or '-', sorted(whole - have) or '-'))
    c = CRAFT.get(k, {})
    for part, fs in parts.items():
        if part not in c: 
            if fs: print('%-14s %s: not on the site' % (k, part)); bad += 1
            continue
        sf = set(c[part][2])
        # Capri and Giotto: base and mattress are one piece on the site, told as the mattress
        one_piece = part == 'base' and not sf and set(c.get('mattress', ('', '', []))[2]) == fs
        if sf != fs and not (part == 'base' and not fs) and not one_piece:
            bad += 1; print('%-14s %-8s site %s | catalogue %s' % (k, part, sorted(sf), sorted(fs)))
print(bad, 'differences')
