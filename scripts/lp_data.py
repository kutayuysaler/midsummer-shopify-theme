"""What each system is made of and dressed in, as the house's own documents state it.

Sources: the 2026 catalogue (MIDSUMMER_CATALOGO_digitale, composition and fittings of every
system), the price lists of August 2026 (Listini Estero / Italia 260805: the cloth of every
system), the Essenziale and First Dream sheets, and Loro Piana Interiors' 2026 trade list
(article, composition). Colours: the Loro Piana Interiors cards kept at the atelier
(Connemara, Altai) and the twelve Mystic River colours photographed for the house.
Only the fibres are named; nothing of the build.
"""
import json, os

# padding fibres, most telling first
FIBRES = {
    'essenziale': ['Wool', 'Linen', 'Ingeo'],
    'raffaello': ['Baby Alpaca', 'Wool', 'Cotton', 'Ingeo'],
    'amalfi': ['Silk', 'Cheviot Wool', 'Cotton', 'Ingeo'],
    'capri': ['Horsehair', 'Linen', 'Cheviot Wool', 'Silk'],
    'bellagio': ['Yak Hair', 'Cheviot Wool', 'Linen', 'Ingeo'],
    'vivaldi-2': ['Camel Hair', 'Silk', 'Wool', 'Cotton', 'Ingeo'],
    'monteverdi': ['Vegetable Horsehair', 'Linen', 'Ingeo'],
    'ultra-dry': ['Vegetable Horsehair', 'Linen', 'Cotton', 'Ingeo', 'Cashmere', 'Silk', 'Cheviot Wool'],
    'dreamy-2': ['Camel Hair', 'Silk', 'Cheviot Wool', 'Horsehair', 'Linen'],
    'brera': ['Yak Hair', 'Wool', 'Cotton', 'Ingeo'],
    'vivaldi-plus': ['Cashmere', 'Silk', 'Wool', 'Cotton', 'Ingeo'],
    'roma': ['Horsehair', 'Silk', 'Falkland Wool', 'Linen', 'Cotton', 'Ingeo'],
    'dreamy-springs': ['Cashmere', 'Camel Hair', 'Horsehair', 'Cheviot Wool', 'Linen', 'Ingeo'],
    'my-dream': ['Alpaca', 'Silk', 'Cheviot Wool'],
    'bellini': ['Silk', 'Horsehair', 'Cheviot Wool', 'Falkland Wool', 'Linen', 'Cotton', 'Ingeo', 'Orange Fiber'],
    'giotto': ['Horsehair', 'Cheviot Wool', 'Linen', 'Silk'],
    'vicuna': ['Vicuña', 'Cashmere', 'Falkland Wool', 'Horsehair', 'Silk', 'Linen', 'Ingeo'],
    'flora': ['Yak Hair', 'Horsehair', 'Cheviot Wool', 'Silk', 'Linen', 'Orange Fiber'],
    'top-2': ['Cashmere', 'Baby Alpaca', 'Mohair', 'Yak Hair', 'Horsehair', 'Silk', 'Linen', 'Cheviot Wool'],
    'storage': ['Cashmere', 'Silk', 'Cheviot Wool'],
    'paisley': ['Baby Alpaca', 'Cheviot Wool', 'Silk', 'Linen'],
    'topper-roma': ['Cashmere', 'Mohair', 'Silk', 'Falkland Wool', 'Linen', 'Ingeo'],
    'first-dream': ['Baby Alpaca', 'Cashmere', 'Silk', 'Linen', 'Cheviot Wool', 'Ingeo'],
    # the 2026 catalogue's toppers page (page 110): the high and medium toppers are one product on the store
    'topper-high': ['Silk', 'Wool', 'Linen', 'Ingeo', 'Horsehair', 'Vicuña'],
    'topper-thin': ['Silk', 'Wool', 'Ingeo'],
}

# the Loro Piana Interiors cloths, as the page shows them
CARDS = json.load(open(os.path.join(os.path.dirname(__file__), 'lp_cards.json')))
FABRICS = [
    {'key': 'mystic', 'name': 'Mystic River', 'code': 'AL2040', 'comp': '64% linen, 36% cotton', 'texture': 'linen',
     'text': 'A linen and cotton with a soft, nubbed hand, heavy enough to hold the line of a mattress. The cloth we use most, in twelve colours.',
     'systems': 'Roma, Topper Roma, Capri, Dreamy and Storage; Dreamy Springs on request.',
     'colours': [(n, h, f, l) for (n, h, f, l) in CARDS['mystic']]},
    {'key': 'connemara', 'name': 'Connemara', 'code': 'AL2008', 'comp': '100% linen', 'texture': 'linen',
     'text': 'A pure linen with a clear, even weave, cool to the touch and quick to breathe.',
     'systems': 'Top, Giotto Round and Brera, and the two-tone Capri and Dreamy.',
     'colours': [(n, h, f, f[:-4] + '-l.jpg') for (n, h, f) in CARDS['connemara']]},
    {'key': 'altai', 'name': 'Altai', 'code': 'A4668RS · A3668RS', 'comp': '90% virgin wool, 10% cashmere', 'texture': 'wool',
     'text': 'Wool and cashmere, dense and warm: plain, or mélange in its three last colours. It edges the winter side of Brera.',
     'systems': 'Brera; the Flora topper on request.',
     'colours': [(n, h, f, f[:-4] + '-l.jpg') for (n, h, f) in CARDS['altai']]},
    {'key': 'wish', 'name': 'Wish', 'code': 'A702384RS', 'comp': 'Bouclé of virgin wool and cashmere', 'texture': 'boucle',
     'text': 'A bouclé of wool and cashmere, soft and deep, its loops catching the light. It dresses Bellini, and the boxspring of Flora.',
     'systems': 'Bellini; the boxspring of Flora.', 'image': 'ms-lp-wish-l.jpg', 'caption': 'The bouclé, close up: wool and cashmere', 'colours': []},
    {'key': 'cardi', 'name': 'Cardi', 'code': 'Fiore di Cardo, A702050RS', 'comp': '90% virgin wool, 10% cashmere', 'texture': 'wool',
     'text': 'Loro Piana Interiors’ Fiore di Cardo: wool and cashmere woven with a thistle flower. It dresses the winter face of the Flora topper; the summer face is linen and cotton.',
     'systems': 'Flora: the topper.', 'image': 'ms-lp-cardi-l.jpg', 'caption': 'On the Flora topper', 'colours': []},
    {'key': 'elys', 'name': 'Ely’s Harbour', 'code': 'A6801RS', 'comp': '60% linen, 40% cashmere', 'texture': 'linen',
     'text': 'Linen and cashmere: the freshness of linen with the warmth of cashmere, on the winter side of Top.',
     'systems': 'Top: the winter side of the mattress and of the topper.', 'image': 'ms-lp-elys-l.jpg', 'colours': []},
    {'key': 'bangor', 'name': 'Bangor', 'code': 'AL2025', 'comp': '100% linen', 'texture': 'linen',
     'text': 'A fine pure linen for the surface you sleep on in summer.',
     'systems': 'Top and Giotto Round: the topper.', 'image': 'ms-lp-bangor-l.jpg', 'colours': []},
    {'key': 'shadan', 'name': 'Shadan', 'code': 'AL2075RS', 'comp': '100% linen', 'texture': 'linen',
     'text': 'A linen woven with a paisley, from the Paisley book. On Paisley it covers the topper, with Katai, a pure silk (AS1005), on the boxspring.',
     'systems': 'Paisley.', 'image': 'ms-lp-shadan-l.jpg', 'caption': 'On the Paisley topper', 'colours': []},
]
ANCHOR = {f['key']: f['name'].lower().replace('’', '').replace(' ', '-') for f in FABRICS}

# what each system is dressed in. lp: the Loro Piana Interiors cloths it is made in (empty: none);
# cover: the Upholstery line of its specification; cloth: the sentence for its questions;
# palette: the cloth whose colours its page shows
CLOTH = {
    'essenziale': {'lp': [], 'cover': '100% cotton', 'cloth': 'Its cover is pure cotton.'},
    'raffaello': {'lp': [], 'cover': 'Cotton', 'cloth': 'Its cover is cotton.'},
    'amalfi': {'lp': [], 'cover': 'Linen and cotton, in four colours', 'cloth': 'It is covered in linen and cotton, in four colours.'},
    'bellagio': {'lp': [], 'cover': 'Raw linen and cotton, edged in orange', 'cloth': 'It is covered in raw linen and cotton, edged in orange.'},
    'vivaldi-2': {'lp': [], 'cover': 'Linen and cotton', 'cloth': 'It is covered in linen and cotton.'},
    'vivaldi-plus': {'lp': [], 'cover': 'Linen and cotton', 'cloth': 'It is covered in linen and cotton.'},
    'monteverdi': {'lp': [], 'cover': 'Raw recycled linen and cotton', 'cloth': 'No animal fibre is used: it is covered in raw recycled linen and cotton.'},
    'ultra-dry': {'lp': [], 'cover': 'Raw linen and cotton', 'cloth': 'It is covered in raw linen and cotton.'},
    'my-dream': {'lp': [], 'cover': 'Viscose', 'cloth': 'Its cover is viscose.'},
    'first-dream': {'lp': [], 'cover': 'Edged with a caramel or pink ribbon', 'cloth': 'It is edged with a ribbon in caramel or pink.'},
    'capri': {'lp': ['mystic', 'connemara'], 'palette': 'mystic',
              'cover': 'Loro Piana Interiors Mystic River; or two-tone, natural linen and cotton with Connemara or Mystic River',
              'cloth': 'It is upholstered in Loro Piana Interiors Mystic River, or two-tone, in natural linen and cotton with Connemara or Mystic River.'},
    'dreamy-2': {'lp': ['mystic', 'connemara'], 'palette': 'mystic',
                 'cover': 'Loro Piana Interiors Mystic River; or two-tone, natural linen and cotton with Connemara or Mystic River',
                 'cloth': 'It is upholstered in Loro Piana Interiors Mystic River, or two-tone, in natural linen and cotton with Connemara or Mystic River.'},
    'brera': {'lp': ['connemara', 'altai'], 'palette': 'connemara',
              'cover': 'Loro Piana Interiors Connemara linen, the winter side edged in Altai wool and cashmere',
              'cloth': 'It is upholstered in Loro Piana Interiors Connemara linen, its winter side edged in Altai wool and cashmere.'},
    'roma': {'lp': ['mystic'], 'palette': 'mystic', 'cover': 'Loro Piana Interiors Mystic River, edged in Midsummer pink',
             'cloth': 'It is upholstered in Loro Piana Interiors Mystic River, a linen and cotton, and edged in Midsummer pink.'},
    'topper-roma': {'lp': ['mystic'], 'palette': 'mystic', 'cover': 'Loro Piana Interiors Mystic River',
                    'cloth': 'It is upholstered in Loro Piana Interiors Mystic River, a linen and cotton.'},
    'topper-high': {'lp': ['any'], 'cover': 'Loro Piana Interiors linen and cotton, or cashmere',
                    'cloth': 'It can be upholstered in Loro Piana Interiors linen and cotton, or in cashmere, in a range of colours.'},
    'storage': {'lp': ['mystic'], 'palette': 'mystic', 'cover': 'Loro Piana Interiors Mystic River, drawers included',
                'cloth': 'It is upholstered in Loro Piana Interiors Mystic River, a linen and cotton, drawers included.'},
    'dreamy-springs': {'lp': ['mystic'], 'palette': 'mystic', 'cover': 'Natural linen and cotton, or Loro Piana Interiors Mystic River',
                       'cloth': 'It is covered in natural linen and cotton, or upholstered in Loro Piana Interiors Mystic River.'},
    'bellini': {'lp': ['wish'], 'palette': 'wish', 'cover': 'Loro Piana Interiors Wish, a bouclé of wool and cashmere',
                'cloth': 'It is upholstered in Loro Piana Interiors Wish, a bouclé of wool and cashmere.'},
    'flora': {'lp': ['cardi', 'wish'], 'palette': 'wish',
              'cover': 'Loro Piana Interiors Cardi on the topper, Wish on the boxspring, both wool and cashmere',
              'cloth': 'It is upholstered in Loro Piana Interiors: Cardi on the winter face of the topper, Wish on the boxspring, both wool and cashmere.'},
    'top-2': {'lp': ['connemara', 'elys', 'bangor'], 'palette': 'connemara',
              'cover': 'Loro Piana Interiors Connemara, Ely’s Harbour and Bangor',
              'cloth': 'It is upholstered in three Loro Piana Interiors cloths: Connemara linen, Ely’s Harbour linen and cashmere, and Bangor linen.'},
    'giotto': {'lp': ['connemara', 'bangor'], 'palette': 'connemara', 'cover': 'Loro Piana Interiors Connemara and Bangor linen',
               'cloth': 'It is upholstered in Loro Piana Interiors Connemara and Bangor linen.'},
    'paisley': {'lp': ['shadan'], 'palette': 'shadan', 'cover': 'Loro Piana Interiors Shadan linen and Katai silk',
                'cloth': 'It is upholstered in Loro Piana Interiors: Shadan, a paisley linen, on the topper, and Katai silk on the boxspring.'},
    'vicuna': {'lp': ['any'], 'cover': 'Raw linen and cotton, or a Loro Piana Interiors cloth',
               'cloth': 'It is covered in raw linen and cotton, or in a Loro Piana Interiors cloth chosen with you.'},
}

# the line under each system's name, where no metafield gives one (by title)
NOTES = {
    'Essenziale': 'The first mattress. Wool, linen and Ingeo, nothing superfluous.',
    'Raffaello': 'Baby alpaca and wool, in a cotton cover.',
    'Amalfi': 'Coloured linen and cotton, in four colours.',
    'Capri': 'Boxspring and mattress in one clean line, in Mystic River.',
    'Thin Topper': 'Three centimetres of silk or wool, with Ingeo.',
    'Bellagio': 'Yak and Cheviot wool, in raw linen edged in orange.',
    'Vivaldi': 'Camel hair, silk and wool: the balanced mattress, the one we are asked for most.',
    'Monteverdi': 'Fully plant-based: vegetable horsehair, linen and Ingeo.',
    'Ultra Dry': 'Vegetable horsehair and linen, for humid climates.',
    'Dreamy': 'Capitonné comfort, in Loro Piana Interiors Mystic River.',
    'Brera': 'Slim and structured, in Loro Piana Interiors Connemara linen.',
    'Medium & High Topper': 'Silk, wool and linen, in two heights; the high one also in vicuña.',
    'Paisley': 'Loro Piana Interiors Shadan linen and Katai silk.',
    'Top': 'The most complete system of the house, in three Loro Piana Interiors cloths.',
    'Vicuña': 'The fibre of the gods, at full weight.',
    'Giotto Round': 'Round, made entirely to measure, in Connemara and Bangor linen.',
    'Bellini': 'A slender bed, dressed in Loro Piana Interiors Wish bouclé.',
    'Storage': 'Storage without a visible line, in Mystic River.',
    'Flora': 'Loro Piana Interiors Cardi and Wish, in wool and cashmere.',
    'Dreamy Springs': 'Cashmere and camel hair beneath the capitonné.',
    'My Dream': 'The hypoallergenic one: silk, alpaca and Cheviot wool.',
    'Roma': 'Loro Piana Interiors Mystic River, edged in Midsummer pink.',
    'Roma Topper': 'Two faces, for winter and summer, to finish the Roma.',
    'Vivaldi Plus': 'The Vivaldi, taken further, with cashmere and silk.',
    'First Dream': 'Baby alpaca and cashmere for winter, linen and silk for summer.',
    # the boxsprings sold on their own, from their own pages: what they are, not how they are built
    'Top Dream Boxspring': 'Our masterpiece among boxsprings, made entirely by hand.',
    'Dreamy Springs Boxspring': 'The base of the Dreamy Springs, with pure Scottish wool and coconut fibre.',
    'My Dream Boxspring': 'The boxspring for heavy use and contract projects, dressed in natural cloth.',
    'First Dream Boxspring': 'The firmer base, with pure Cheviot wool and coconut fibre, 13 or 20 cm high.',
    'Storage Boxspring': 'A boxspring with four mahogany drawers beneath.',
}

# ── Inside each system: what its topper, mattress and base are made of and dressed in, as the
#    catalogue and Models & Layers describe them. Fibres by season and the cloth only: nothing of
#    the build (no springs, no layers). kind: 'system', 'mattress' or 'topper'.
#    Each part: (lead, [points], [fibres]); None uses the shared text for that kind.
CRAFT = {
    'essenziale': {'kind': 'mattress',
        'mattress': ('Pure wool on the winter face; wool, linen and Ingeo on the summer face.',
                     ['No synthetic foam and nothing derived from petroleum: only natural fibres.', 'Covered in pure cotton, natural and breathable.', 'In soft, medium or firm.'],
                     ['Wool', 'Linen', 'Ingeo'])},
    'raffaello': {'kind': 'mattress',
        'mattress': ('Baby alpaca and wool for winter; wool, cotton and Ingeo for summer.',
                     ['Comfortable and welcoming in its simplicity.', 'Covered in cotton, edged with the Midsummer pink ribbon.', 'Its feel is chosen with you, from soft to firm.'],
                     ['Baby Alpaca', 'Wool', 'Cotton', 'Ingeo'])},
    'amalfi': {'kind': 'system',
        'topper': ('Optional: a low or medium topper, in the same colour and cloth.', ['Silk, wool and linen, with a summer and a winter face.'], ['Silk', 'Cheviot Wool', 'Linen']),
        'mattress': ('Silk and Cheviot wool for winter; Cheviot wool, cotton and Ingeo for summer.',
                     ['Covered in linen and cotton, in four colours.', 'Made with its boxspring, to the same measure.'], ['Silk', 'Cheviot Wool', 'Cotton', 'Ingeo']),
        'base': ('A soft boxspring, padded with wool felt.', ['Dressed in the same linen and cotton as the mattress.'], ['Wool'])},
    'capri': {'kind': 'system',
        'topper': ('Silk and Cheviot wool: the soft surface of the system.', ['Upholstered in the cloth of the bed.'], ['Silk', 'Cheviot Wool']),
        'mattress': ('Base and mattress are a single piece, padded with linen, Cheviot wool and horsehair.',
                     ['Our most compact system: one clean line from the floor to the topper.', 'Its feel is chosen with you, from soft to firm.'], ['Horsehair', 'Linen', 'Cheviot Wool']),
        'base': ('The mattress and the boxspring are one piece, padded with linen, Cheviot wool and horsehair.',
                 ['Our most compact system: one clean line from the floor to the topper.', 'Its feel is chosen with you, from soft to firm.',
                  'Upholstered in Loro Piana Interiors Mystic River, in any of its twelve colours, or two-tone with natural linen and cotton.',
                  'Split in two on request, for the wider sizes.'], ['Horsehair', 'Linen', 'Cheviot Wool'])},
    'bellagio': {'kind': 'mattress',
        'mattress': ('Yak and Cheviot wool for winter; Cheviot wool, linen and Ingeo for summer.',
                     ['Named after the town on Lake Como and its humid climate: it keeps the body dry and the temperature even.',
                      'Covered in unbleached linen reinforced with cotton, edged in orange, its sides sewn by hand in orange waxed thread.'],
                     ['Yak Hair', 'Cheviot Wool', 'Linen', 'Ingeo'])},
    'vivaldi-2': {'kind': 'mattress',
        'mattress': ('Camel hair, silk and wool for winter; wool, cotton and Ingeo for summer.',
                     ['An original blend of precious fibres, and the mattress we are asked for most.', 'Covered in linen and cotton.', 'Its feel is chosen with you, from soft to firm.'],
                     ['Camel Hair', 'Silk', 'Wool', 'Cotton', 'Ingeo'])},
    'vivaldi-plus': {'kind': 'mattress',
        'mattress': ('Cashmere and silk with wool for winter; wool, cotton and Ingeo for summer.',
                     ['The Vivaldi, enriched with precious cashmere.', 'Covered in linen and cotton.', 'Its feel is chosen with you, from soft to firm.'],
                     ['Cashmere', 'Silk', 'Wool', 'Cotton', 'Ingeo'])},
    'monteverdi': {'kind': 'mattress',
        'mattress': ('Fully plant-based: vegetable horsehair, linen and Ingeo, and no animal fibre.',
                     ['Vegetable horsehair gives structure and lets the air move freely; linen keeps it fresh and light.', 'Covered in raw recycled linen and cotton.'],
                     ['Vegetable Horsehair', 'Linen', 'Ingeo']),
        'base': ('Made to rest on a Midsummer boxspring.', ['Made by the same artisans, to the size of the mattress, and dressed in natural cloth.'], [])},
    'ultra-dry': {'kind': 'mattress',
        'topper': ('A winter topper in Cheviot wool and cashmere, on request.', ['Soft or medium, to warm the bed in the cold months.'], ['Cashmere', 'Cheviot Wool']),
        'mattress': ('Two mattresses, one for each climate.',
                     ['Summer: vegetable horsehair, linen, cotton and Ingeo, to stay dry in humid air.', 'Winter: Cheviot wool, silk and cashmere.', 'Covered in raw linen and cotton.'],
                     ['Vegetable Horsehair', 'Linen', 'Cotton', 'Ingeo', 'Cashmere', 'Silk', 'Cheviot Wool'])},
    'dreamy-2': {'kind': 'system',
        'topper': ('Cheviot wool and horsehair for winter; Cheviot wool, silk and linen for summer.', ['Capitonné, for an enveloping comfort.'], ['Horsehair', 'Cheviot Wool', 'Silk', 'Linen']),
        'mattress': ('Cheviot wool, camel hair and silk.', ['Its feel is chosen with you, from soft to firm.'], ['Camel Hair', 'Cheviot Wool', 'Silk']),
        'base': ('Silk and Cheviot wool, upholstered in Loro Piana Interiors Mystic River.',
                 ['All in Mystic River, or two-tone with natural linen and cotton.', 'A headboard to match, on request.'], ['Silk', 'Cheviot Wool'])},
    'brera': {'kind': 'system',
        'topper': ('Brera needs no separate topper: its slim mattress is soft enough to be one.', ['Light, and easy to turn with the seasons.'], []),
        'mattress': ('Wool and yak for winter; wool, cotton and Ingeo for summer.',
                     ['Mattress and topper in one slim piece.', 'Upholstered in Loro Piana Interiors Connemara linen.', 'Its winter side edged in Altai wool and cashmere.', 'Light, and easy to turn with the seasons.'], ['Yak Hair', 'Wool', 'Cotton', 'Ingeo']),
        'base': ('Our slimmest boxspring, padded with wool, on natural leather legs.',
                 ['A headboard on request, in Connemara linen with natural leather straps.'], ['Wool'])},
    'roma': {'kind': 'mattress',
        'topper': ('Two Roma toppers, one for each season.',
                   ['Winter: cashmere, silk, mohair and Falkland wool.', 'Summer: silk, linen, Ingeo and Falkland wool.'], ['Cashmere', 'Mohair', 'Silk', 'Falkland Wool', 'Linen', 'Ingeo']),
        'mattress': ('Silk, Falkland wool and horsehair for winter; linen, Ingeo, cotton, Falkland wool and horsehair for summer.',
                     ['Upholstered in Loro Piana Interiors Mystic River, edged with the Midsummer pink ribbon.', 'Its sides stitched by hand.'],
                     ['Horsehair', 'Silk', 'Falkland Wool', 'Linen', 'Ingeo', 'Cotton']),
        'base': ('A Midsummer boxspring in Mystic River to match.', ['With its own headboard, drawn with you, on request.'], ['Cheviot Wool'])},
    'dreamy-springs': {'kind': 'mattress',
        'mattress': ('Cashmere, camel hair, Cheviot wool and horsehair for winter; linen, Ingeo, Cheviot wool and horsehair for summer.',
                     ['Capitonné on the surface, designed to deepen sleep.', 'In natural linen and cotton, or Loro Piana Interiors Mystic River, edged in Midsummer pink.'],
                     ['Cashmere', 'Camel Hair', 'Horsehair', 'Cheviot Wool', 'Linen', 'Ingeo'])},
    'my-dream': {'kind': 'mattress',
        'mattress': ('Silk, alpaca and Cheviot wool, on both faces.', ['Designed to be hypoallergenic.', 'Covered in viscose.'], ['Alpaca', 'Silk', 'Cheviot Wool'])},
    'bellini': {'kind': 'system',
        'topper': ('Silk and Cheviot wool for winter; Cheviot wool and Orange Fiber for summer.',
                   ['Orange Fiber is made from Sicilian orange peel: light, breathable and naturally fresh.', 'Edged with a grosgrain ribbon.'], ['Silk', 'Cheviot Wool', 'Orange Fiber']),
        'mattress': ('Silk, Cheviot wool and horsehair for winter; linen, Ingeo, cotton, Falkland wool and horsehair for summer.',
                     ['Its feel is chosen with you, from soft to firm.'], ['Silk', 'Horsehair', 'Cheviot Wool', 'Falkland Wool', 'Linen', 'Cotton', 'Ingeo']),
        'base': ('Cheviot wool and linen, upholstered in Loro Piana Interiors Wish.',
                 ['Wish is a bouclé of wool and cashmere: it gives the slender base its texture and warmth.'], ['Cheviot Wool', 'Linen'])},
    'giotto': {'kind': 'system',
        'topper': ('Silk and Cheviot wool, round to the last stitch.', ['Both faces in Loro Piana Interiors Bangor linen, its side in Connemara.'], ['Silk', 'Cheviot Wool']),
        'mattress': ('Base and mattress are one piece, padded with linen, Cheviot wool and horsehair.',
                     ['Round, and made entirely to measure.'], ['Horsehair', 'Linen', 'Cheviot Wool']),
        'base': ('The mattress and the boxspring are one round piece, padded with linen, Cheviot wool and horsehair.',
                 ['Round, and made entirely to measure, in any diameter.', 'Upholstered in Loro Piana Interiors Connemara linen.'], ['Horsehair', 'Linen', 'Cheviot Wool'])},
    'vicuna': {'kind': 'mattress',
        'topper': ('A vicuña topper on request: vicuña, silk and wool.', ['To bring the same fibre to the surface of the bed.'], ['Vicuña', 'Silk', 'Wool']),
        'mattress': ('Vicuña, cashmere, Falkland wool and horsehair for winter; linen, silk, Ingeo, Falkland wool and horsehair for summer.',
                     ['Vicuña is finer than the finest cashmere, from a small wild camelid of the Andes.',
                      'Covered in raw linen and cotton, edged with a vicuña-coloured ribbon and tufted by hand; or in a Loro Piana Interiors linen.'],
                     ['Vicuña', 'Cashmere', 'Falkland Wool', 'Horsehair', 'Silk', 'Linen', 'Ingeo'])},
    'flora': {'kind': 'system',
        'topper': ('Cheviot wool and horsehair for winter; Cheviot wool, silk and Orange Fiber for summer.',
                   ['Its winter face in Loro Piana Interiors Cardi, wool and cashmere; its summer face in linen and cotton.'], ['Horsehair', 'Cheviot Wool', 'Silk', 'Orange Fiber']),
        'mattress': ('Yak and Cheviot wool for winter; Cheviot wool, linen and Orange Fiber for summer.',
                     ['Its feel is chosen with you, from soft to firm.'], ['Yak Hair', 'Cheviot Wool', 'Linen', 'Orange Fiber']),
        'base': ('Linen and Cheviot wool, upholstered in Loro Piana Interiors Wish bouclé.', ['Wool and cashmere, soft and deep.'], ['Linen', 'Cheviot Wool'])},
    'top-2': {'kind': 'system',
        'topper': ('Yak and Cheviot wool for winter; Cheviot wool and linen for summer.',
                   ['Ely’s Harbour linen and cashmere on the winter face, Bangor linen on the summer face.'], ['Yak Hair', 'Cheviot Wool', 'Linen']),
        'mattress': ('Cashmere, baby alpaca, mohair, horsehair and Cheviot wool for winter; linen, silk, Cheviot wool and horsehair for summer.',
                     ['Ely’s Harbour on the winter side, Connemara linen on the summer side.', 'Its feel is chosen with you, from soft to firm.'],
                     ['Cashmere', 'Baby Alpaca', 'Mohair', 'Horsehair', 'Silk', 'Linen', 'Cheviot Wool']),
        'base': ('Cheviot wool, fully upholstered in Connemara linen.', ['No wood or metal shows: even the legs are covered in cloth.'], ['Cheviot Wool'])},
    'storage': {'kind': 'system',
        'mattress': ('Cheviot wool, silk and cashmere.', ['Upholstered in Loro Piana Interiors Mystic River, to match its base.'], ['Cashmere', 'Silk', 'Cheviot Wool']),
        'base': ('A slender base that holds two or four upholstered drawers.', ['Cheviot wool on top; the drawers in the same Mystic River.'], ['Cheviot Wool'])},
    'paisley': {'kind': 'system',
        'topper': ('Cheviot wool and silk for winter; Cheviot wool and linen for summer.', ['Upholstered in Loro Piana Interiors Shadan, a paisley linen.'], ['Silk', 'Cheviot Wool', 'Linen']),
        'mattress': ('Cheviot wool and baby alpaca for winter; Cheviot wool and linen for summer.', ['Its border in Katai silk.'], ['Baby Alpaca', 'Cheviot Wool', 'Linen']),
        'base': ('Linen and Cheviot wool, upholstered in Loro Piana Interiors Katai silk.', ['With or without a headboard.'], ['Linen', 'Cheviot Wool'])},
    'topper-roma': {'kind': 'topper',
        'topper': ('Two faces: cashmere, silk, mohair and Falkland wool for winter; silk, linen, Ingeo and Falkland wool for summer.',
                   ['Upholstered in Loro Piana Interiors Mystic River.', 'Soft or medium, to sit on the mattress beneath it.'],
                   ['Cashmere', 'Mohair', 'Silk', 'Falkland Wool', 'Linen', 'Ingeo'])},
    # the 2026 catalogue, page 110
    'topper-high': {'kind': 'topper',
        'topper': ('High, 9 to 10 cm, or medium, 5 cm: silk, wool, linen and Ingeo; the high one also in vicuña, the medium one also in wool and horsehair.',
                   ['The body rests on the mattress, gently held by the softness of the fibres above it.',
                    'Warm for the winter, cool and breathable for the summer.',
                    'Upholstered in Loro Piana Interiors linen and cotton, or cashmere, in a range of colours.'],
                   ['Silk', 'Wool', 'Linen', 'Ingeo', 'Vicuña', 'Horsehair'])},
    'topper-thin': {'kind': 'topper',
        'topper': ('Three centimetres of silk and Ingeo, or of wool and Ingeo.',
                   ['A warm welcome and an even temperature, in a few centimetres of precious fibres.',
                    'Medium to firm.'],
                   ['Silk', 'Wool', 'Ingeo'])},
    'first-dream': {'kind': 'mattress',
        'mattress': ('Cheviot wool, cashmere and baby alpaca for winter; Cheviot wool, Ingeo, linen and silk for summer.',
                     ['The first of the Dream series, made to follow the natural curves of the spine.', 'Edged with a ribbon in caramel or pink.'],
                     ['Baby Alpaca', 'Cashmere', 'Silk', 'Linen', 'Cheviot Wool', 'Ingeo'])},
}
# the house's boxsprings, sold as their own products (bin/beds_data.py BOXSPRING_HANDLES): the base
# alone, with the mattress and topper that complete it in outline. Only what the catalogue and the
# systems' own pages say of them.
BOX_LEAD = ('A Midsummer boxspring: the foundation of the bed, and the part of it the room sees.',
            ['Made by hand in Italy, to the size of the mattress it carries.', 'Upholstered to match the bed, in natural cloth or Loro Piana Interiors.',
             'With a headboard drawn with you, if you wish.'], ['Cheviot Wool'])
CRAFT.update({
    'base-dreamy-springs': {'kind': 'base', 'base': BOX_LEAD},
    'base-my-dream': {'kind': 'base', 'base': BOX_LEAD},
    'base-first-dream': {'kind': 'base', 'base': ('A slim Midsummer boxspring: the foundation of the bed, and the part of it the room sees.', BOX_LEAD[1], BOX_LEAD[2])},
    'base-top-dream': {'kind': 'base', 'base': BOX_LEAD},
    'base-storage': {'kind': 'base', 'base': ('A boxspring with four mahogany drawers beneath.',
                     ['Pure virgin wool on top; the structure in mahogany.', 'Made by hand in Italy, to the size of the mattress it carries.'], ['Wool'])},
    'base': {'kind': 'base', 'base': BOX_LEAD},
})
# a boxspring product's handle -> its drawing and data (snippets/ms-kind tells it is a boxspring)
BOX_KEYS = {'dreamy-springs': 'base-dreamy-springs', 'my-dream-1': 'base-my-dream', 'first-dream-1': 'base-first-dream',
            'top-dream': 'base-top-dream', 'storage-boxspring': 'base-storage'}

# the parts a product does not include, told from the side of what it is: a mattress, a topper or
# a base. They are drawn in outline, marked "not included", and lead to where they can be found.
TOPPER_OUT = ('Not part of [name]: a Midsummer topper finishes the bed.',
              ['Three heights, with a summer and a winter face.', 'Made to sit on the mattress without changing its feel.'], ['Silk', 'Cheviot Wool', 'Linen'])
BASE_OUT = ('Not part of [name]: it rests on a Midsummer boxspring.',
            ['Made by hand in Italy, to the size of the mattress.', 'Dressed in natural cloth, with a headboard drawn with you if you wish.'], ['Cheviot Wool'])
CRAFT_SHARED_KIND = {
    'system': {
        'topper': ('Optional: a Midsummer topper to finish the bed.', TOPPER_OUT[1], TOPPER_OUT[2]),
        'mattress': ('The heart of the system, made with its boxspring.', ['Its feel is chosen with you, from soft to firm.'], []),
        'base': ('Made to rest on a Midsummer boxspring.', BASE_OUT[1], BASE_OUT[2]),
    },
    'mattress': {'topper': TOPPER_OUT, 'base': BASE_OUT},
    'topper': {
        'mattress': ('Not part of [name]: it sits on the mattress beneath it.', ['On a Midsummer mattress, or on any good mattress you already sleep on.'], []),
        'base': BASE_OUT,
    },
    'base': {
        'topper': TOPPER_OUT,
        'mattress': ('Not part of [name]: a Midsummer mattress rests on it.', ['Natural fibres, chosen with you.', 'Its feel is chosen with you, from soft to firm.'], []),
    },
}
CRAFT_SHARED = CRAFT_SHARED_KIND['system']
# the parts a system is made of, where they are not the usual three (the 2026 catalogue): Capri and
# Giotto Round are a topper and one piece that is mattress and boxspring; Brera one slim piece that
# is mattress and topper, on its boxspring. Storage and Amalfi take a topper only if you wish.
CRAFT_PARTS = {'capri': 'topper,base', 'giotto': 'topper,base', 'brera': 'mattress,base'}
CRAFT_OPT = {'storage': 'topper', 'amalfi': 'topper'}
CRAFT_TEXT = {
    'capri': '[name] is made in two parts: a topper, and the mattress and boxspring in one piece. By hand in Italy, and specified with you.',
    'giotto': '[name] is made in two parts: a topper, and the mattress and boxspring in one round piece. By hand in Italy, and specified with you.',
    'brera': '[name] is made in two parts: one slim piece that is mattress and topper at once, and the boxspring beneath it. By hand in Italy, and specified with you.',
    'storage': '[name] is a mattress on a boxspring with drawers beneath, made by hand in Italy and specified with you. A topper can finish it, if you wish.',
    'amalfi': '[name] is a mattress on its boxspring, in the same cloth and colour, made by hand in Italy. A low or medium topper can finish it, if you wish.',
}
CRAFT_INTRO = {
    'system': '[name] is made as one: topper, mattress and boxspring, by hand in Italy, and specified with you.',
    'mattress': '[name] is the mattress alone, the heart of the bed. A topper and a Midsummer boxspring complete it, and are shown here in outline.',
    'topper': '[name] is the topper alone, the surface of the bed. It sits on the mattress beneath it, shown here in outline.',
    'base': '[name] is a Midsummer boxspring, alone. The mattress and topper that complete it are shown here in outline.',
}

# fibres by face, read from each part's own sentence ("A and B for winter; C and D for summer"):
# the craft section shows them side by side
SEASON_NAMES = {'yak': 'Yak Hair', 'yak hair': 'Yak Hair', 'wool': 'Wool', 'pure wool': 'Wool', 'cheviot wool': 'Cheviot Wool', 'falkland wool': 'Falkland Wool',
                'camel hair': 'Camel Hair', 'baby alpaca': 'Baby Alpaca', 'alpaca': 'Alpaca', 'cotton': 'Cotton', 'orange fiber': 'Orange Fiber',
                'ingeo': 'Ingeo', 'vegetable horsehair': 'Vegetable Horsehair', 'horsehair': 'Horsehair', 'mohair': 'Mohair', 'cashmere': 'Cashmere',
                'silk': 'Silk', 'linen': 'Linen', 'vicuña': 'Vicuña'}
def seasons(lead):
    """(winter, summer) fibre names from a lead like 'Silk and wool for winter; wool, cotton and Ingeo for summer.', or None"""
    import re
    t = re.sub(r'^Two faces:\s*', '', lead.strip().rstrip('.'))
    m = re.match(r'^(.*?)\s+(?:for winter|on the winter face);\s*(.*?)\s+(?:for summer|on the summer face)$', t)
    if not m:
        return None
    out = []
    for side in m.groups():
        names = []
        for w in re.split(r',\s*|\s+and\s+|\s+with\s+', side):
            k = w.strip().lower()
            if not k:
                continue
            if k not in SEASON_NAMES:
                raise ValueError('season fibre %r in %r' % (w, lead))
            if SEASON_NAMES[k] not in names:
                names.append(SEASON_NAMES[k])
        out.append(names)
    return tuple(out)
def season_points(points):
    """(winter, summer) from points 'Winter: A, B and C.' and 'Summer: D and E, to stay dry…', or None"""
    import re
    w = next((p for p in points if p.startswith('Winter: ')), None)
    s = next((p for p in points if p.startswith('Summer: ')), None)
    if not (w and s):
        return None
    side = lambda p: re.sub(r',\s*to\s.*$', '', p.split(': ', 1)[1].rstrip('.'))
    return seasons('%s for winter; %s for summer.' % (side(w), side(s)))
def part_seasons(lead, points):
    return seasons(lead) or season_points(points)

# what completes a mattress, a topper or a boxspring: its own companions on the store, by handle,
# before the collection of that kind (snippets/ms-craft-mates)
MATES = {
    'roma': {'topper': 'topper-roma,roma-topper'},
    'topper-roma': {'mattress': 'mystic-river,roma'},
    'my-dream': {'base': 'my-dream-1'},
    'first-dream': {'base': 'first-dream-1'},
    'dreamy-springs': {'base': 'dreamy-springs'},
    'base-my-dream': {'mattress': 'my-dream'},
    'base-first-dream': {'mattress': 'first-dream-mattress'},
    'base-dreamy-springs': {'mattress': 'dreamy-springs-mattress,dreamy-springs-1'},
}
# when the store has no collection of that kind: the house's own pieces, by handle
SPARE = {'topper': 'topper-roma', 'mattress': '', 'base': 'dreamy-springs,top-dream,my-dream-1,first-dream-1,storage-boxspring'}

# the line under each system's name, in Italian and Russian (the store's other languages)
NOTES_I18N = {
    'it': {
        'Essenziale': 'Il primo materasso. Lana, lino e Ingeo, niente di superfluo.',
        'Raffaello': 'Baby alpaca e lana, in una fodera di cotone.',
        'Amalfi': 'Lino e cotone colorati, in quattro colori.',
        'Capri': 'Boxspring e materasso in un’unica linea pulita, in Mystic River.',
        'Thin Topper': 'Tre centimetri di seta o lana, con Ingeo.',
        'Bellagio': 'Yak e lana Cheviot, in lino grezzo bordato d’arancio.',
        'Vivaldi': 'Cammello, seta e lana: il materasso equilibrato, il più richiesto.',
        'Monteverdi': 'Interamente vegetale: crine vegetale, lino e Ingeo.',
        'Ultra Dry': 'Crine vegetale e lino, per i climi umidi.',
        'Dreamy': 'Il comfort del capitonné, in Loro Piana Interiors Mystic River.',
        'Brera': 'Sottile e strutturato, in lino Loro Piana Interiors Connemara.',
        'Medium & High Topper': 'Seta, lana e lino, in due altezze; quello alto anche in vigogna.',
        'Paisley': 'Lino Shadan e seta Katai di Loro Piana Interiors.',
        'Top': 'Il sistema più completo della casa, in tre tessuti Loro Piana Interiors.',
        'Vicuña': 'La fibra degli dei, a pieno peso.',
        'Giotto Round': 'Rotondo, interamente su misura, in lino Connemara e Bangor.',
        'Bellini': 'Un letto slanciato, vestito di bouclé Wish di Loro Piana Interiors.',
        'Storage': 'Un contenitore senza linee visibili, in Mystic River.',
        'Flora': 'Cardi e Wish di Loro Piana Interiors, in lana e cashmere.',
        'Dreamy Springs': 'Cashmere e cammello sotto il capitonné.',
        'My Dream': 'L’ipoallergenico: seta, alpaca e lana Cheviot.',
        'Roma': 'Loro Piana Interiors Mystic River, bordato in rosa Midsummer.',
        'Roma Topper': 'Due lati, per l’inverno e l’estate, a completare il Roma.',
        'Vivaldi Plus': 'Il Vivaldi, portato oltre, con cashmere e seta.',
        'First Dream': 'Baby alpaca e cashmere per l’inverno, lino e seta per l’estate.',
        'Top Dream Boxspring': 'Il nostro capolavoro tra i boxspring, interamente fatto a mano.',
        'Dreamy Springs Boxspring': 'La base del Dreamy Springs, con pura lana scozzese e fibra di cocco.',
        'My Dream Boxspring': 'Il boxspring per l’uso intenso e i progetti contract, vestito di tessuto naturale.',
        'First Dream Boxspring': 'La base più rigida, con pura lana Cheviot e fibra di cocco, alta 13 o 20 cm.',
        'Storage Boxspring': 'Un boxspring con quattro cassetti in mogano.',
    },
    'ru': {
        'Essenziale': 'Первый матрас. Шерсть, лён и Ingeo — ничего лишнего.',
        'Raffaello': 'Беби-альпака и шерсть, в хлопковом чехле.',
        'Amalfi': 'Цветной лён и хлопок, в четырёх цветах.',
        'Capri': 'Бокс-спринг и матрас одной чистой линией, в ткани Mystic River.',
        'Thin Topper': 'Три сантиметра шёлка или шерсти, с Ingeo.',
        'Bellagio': 'Як и шерсть шевиот, в небелёном льне с оранжевой окантовкой.',
        'Vivaldi': 'Верблюжья шерсть, шёлк и шерсть: сбалансированный матрас, который у нас просят чаще всего.',
        'Monteverdi': 'Полностью растительный: растительный конский волос, лён и Ingeo.',
        'Ultra Dry': 'Растительный конский волос и лён, для влажного климата.',
        'Dreamy': 'Комфорт капитоне, в ткани Loro Piana Interiors Mystic River.',
        'Brera': 'Тонкий и структурный, в льне Loro Piana Interiors Connemara.',
        'Medium & High Topper': 'Шёлк, шерсть и лён, в двух высотах; высокий — также из викуньи.',
        'Paisley': 'Лён Shadan и шёлк Katai от Loro Piana Interiors.',
        'Top': 'Самая полная система дома, в трёх тканях Loro Piana Interiors.',
        'Vicuña': 'Волокно богов, в полной мере.',
        'Giotto Round': 'Круглый, полностью по индивидуальным размерам, в льне Connemara и Bangor.',
        'Bellini': 'Изящная кровать в буклé Wish от Loro Piana Interiors.',
        'Storage': 'Хранение без видимых линий, в ткани Mystic River.',
        'Flora': 'Ткани Cardi и Wish от Loro Piana Interiors, из шерсти и кашемира.',
        'Dreamy Springs': 'Кашемир и верблюжья шерсть под капитоне.',
        'My Dream': 'Гипоаллергенный: шёлк, альпака и шерсть шевиот.',
        'Roma': 'Loro Piana Interiors Mystic River с окантовкой цвета Midsummer pink.',
        'Roma Topper': 'Две стороны, для зимы и лета, — завершение Roma.',
        'Vivaldi Plus': 'Vivaldi, доведённый до совершенства, с кашемиром и шёлком.',
        'First Dream': 'Беби-альпака и кашемир для зимы, лён и шёлк для лета.',
        'Top Dream Boxspring': 'Наш шедевр среди бокс-спрингов, целиком ручная работа.',
        'Dreamy Springs Boxspring': 'Основание Dreamy Springs, с чистой шотландской шерстью и кокосовым волокном.',
        'My Dream Boxspring': 'Бокс-спринг для интенсивного использования и контрактных проектов, в натуральной ткани.',
        'First Dream Boxspring': 'Более жёсткое основание, с чистой шерстью Cheviot и кокосовым волокном, высотой 13 или 20 см.',
        'Storage Boxspring': 'Бокс-спринг с четырьмя ящиками из красного дерева.',
    },
}
