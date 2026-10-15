"""The fibres of the Natural materials page (sections/ms-fibre-atlas), in the house's own words.

Every line comes from the 2026 catalogue's chapter "Materials to dream of" (lp/catalogo_2026.txt,
pages 116-129), its systems' compositions, or the site's own fibre texts; every figure is the
catalogue's. Nothing here says how a bed is built."""

# slug -> the names the systems' fibre lists use (bin/lp_data.py FIBRES)
SLUG_NAMES = {
    'vicuna': ['Vicuña'], 'cashmere': ['Cashmere', 'Mongolian Cashmere'], 'camel': ['Camel Hair'],
    'yak': ['Yak Hair'], 'alpaca': ['Baby Alpaca', 'Alpaca'], 'mohair': ['Mohair'], 'silk': ['Silk'],
    'wool': ['Wool', 'Cheviot Wool', 'Falkland Wool'], 'horsehair': ['Horsehair'], 'linen': ['Linen'],
    'cotton': ['Cotton', 'Organic Cotton'], 'vegetable': ['Vegetable Horsehair'], 'ingeo': ['Ingeo'],
    'orange': ['Orange Fiber'],
}

# what the glass shows of each fibre, and what that means in a bed: general fibre science, kept to
# what the drawing shows (bin/fibre_draw.py draws every fibre to scale, beside a human hair of 70 µm)
GLASS = {
    'vicuna': 'The finest of the animal hairs, a sixth of a human hair, with small, smooth scales. The finer a fibre, the more readily it bends: against the skin, that is softness.',
    'cashmere': 'Thin, smooth-edged scales, set far apart, on a fine fibre: little for the skin to catch on. Between the softly waved fibres, still air gathers, warm and weightless.',
    'camel': 'A fine down with shallow, smooth scales and a soft, irregular wave: the wave keeps the fibres apart, and that is where the air is held.',
    'yak': 'Smooth, regular scales and a soft wave: the wave holds the fibres a little apart, and the still air caught between them is what keeps you warm.',
    'alpaca': 'Low, flat scales make it smooth to the touch; some fibres carry a core of air along their length, which makes alpaca warm for its weight.',
    'mohair': 'Thin, flat scales, few and far apart: light glances off them, which is mohair’s lustre. Thicker than cashmere, it is resilient and keeps its loft.',
    'silk': 'Two filaments side by side, as the silkworm spins them, with no scales at all: nothing for the skin to catch on, so silk glides.',
    'wool': 'Bold, overlapping scales and a deep wave, the crimp. The crimp keeps the fibres apart and full of air: wool stays lofty, breathes, and returns to its shape.',
    'horsehair': 'Up to three times as thick as a human hair, with a core along its length: thick enough to hold its shape under weight, with open space for the air between the hairs.',
    'linen': 'Straight fibres marked by small nodes, with a fine channel at the centre. Smooth and straight, they touch the skin closely: that close contact is what carries warmth away.',
    'cotton': 'A flat ribbon that twists on itself: the twists let the fibres hold one another in a soft, even yarn, and the fibre takes up moisture readily.',
    'vegetable': 'Coarse, ridged fibres of the palm leaf, far thicker than a human hair: stiff enough to hold their shape, with open paths for the air between them.',
    'ingeo': 'Made, not grown: smooth, round filaments, all of one size, with none of the scales, nodes or twists of the natural fibres.',
    'orange': 'Fine, even filaments of cellulose, the substance of every plant, here drawn from orange peel: even and silky to the hand.',
}
# across one fibre, in µm, as drawn: the catalogue's for vicuña and cashmere, the usual ranges for the rest;
# the made fibres (and the palm, a bundle rather than a fibre) have none
MICRONS = {
    'vicuna': '12', 'cashmere': '15', 'yak': '17', 'camel': '19', 'alpaca': '21', 'mohair': '25–35', 'wool': '25–33',
    'silk': '10–13', 'horsehair': '100–200', 'linen': '15–20', 'cotton': '12–20',
}
# where it comes from, for the map: latitude,longitude; several separated by ;
POINTS = {
    'vicuna': '-15.5,-70.5', 'cashmere': '46.9,103.8', 'camel': '43.5,104.5', 'alpaca': '-14.5,-71.5',
    'wool': '55.4,-2.2;-51.7,-59.2', 'horsehair': '-36.5,-62', 'linen': '50.4,3.2',
    'vegetable': '38.6,16.1', 'orange': '37.4,14.4',
}

def F(fibre, name, group, mark, q, ql, lead, figs=(), origin='', species='', photo='none', alt=''):
    st = {'fibre': fibre, 'name': name, 'group': group, 'mark': mark, 'qualities': q, 'quality_label': ql, 'lead': lead, 'photo': photo}
    if GLASS.get(fibre):
        st['glass_note'] = GLASS[fibre]
    if MICRONS.get(fibre):
        st['microns'] = MICRONS[fibre]
    if POINTS.get(fibre):
        st['points'] = POINTS[fibre]
    for i, (v, cap) in enumerate(figs, 1):
        st['f%d' % i] = v
        st['f%d_cap' % i] = cap
    if origin:
        st['origin'] = origin
    if species:
        st['species'] = species
    if alt:
        st['alt'] = alt
    return st

ATLAS = [
    F('vicuna', 'Vicuña', 'animal', 'Vicuña', 'softness temperature', 'Softness · Warmth',
      'It comes from a small camelid that lives wild in the high Andes; the Inca wove it for their kings, for its lightness and warmth. '
      'Its coat is twofold: a fine down that regulates warmth, and longer, silky fibres that protect.',
      [('12 µm', 'Across one fibre: finer than the best cashmere, at 15 µm.'), ('150 g', 'From one animal, every two years.'),
       ('14', 'Animals shorn for the vicuña of one mattress.')],
      origin='Wild, in the high Andes', species='Vicugna vicugna', photo='vicuna', alt='Four vicuñas on a ridge at dusk.'),
    F('cashmere', 'Cashmere', 'animal', 'Cashmere', 'temperature softness', 'Warmth without weight',
      'The fine undercoat of a goat, combed by hand as the goat moults, never shorn. Soft, silky and velvety, it gives warmth with lightness; '
      'even a little cashmere changes a mattress.',
      [('100–200 g', 'Of fine fibre from one goat, in a year.')],
      origin='Mongolia', species='Capra hircus', photo='cashmere', alt='A herd of goats coming down a mountain valley.'),
    F('camel', 'Camel hair', 'animal', 'Camel Hair', 'temperature', 'Warmth · Temperature',
      'It shields the camel from the extremes of the desert, cold and heat, and does the same in a bed. Fine and soft, it holds a great deal of air, '
      'and it is more hygroscopic than sheep’s wool: a dry, pleasant warmth.',
      [('700 g', 'At most, combed from one young camel in a year.')],
      origin='Asia', species='Camelus bactrianus', photo='camel', alt='A Bactrian camel crossing the snow.'),
    F('yak', 'Yak', 'animal', 'Yak Hair', 'temperature softness', 'Warmth · Softness',
      'A fine, very warm and particularly robust hair, soft and fluffy, with the look of cashmere. The yak is neither shorn nor combed: '
      'in May its winter undercoat falls, and the nomads gather it.',
      species='Bos grunniens', photo='yak', alt='A yak on a misty mountainside.'),
    F('alpaca', 'Baby alpaca', 'animal', 'Baby Alpaca', 'temperature hypoallergenic', 'Temperature · Hypoallergenic',
      'From an animal of the high South American ranges, with an abundant fleece, soft and almost silky. The fibre sits between wool and cashmere, '
      'nearer to cashmere; alpaca cloth was once kept for the Inca emperors.',
      [('No lanolin', 'And so naturally hypoallergenic.')],
      origin='The South American highlands', species='Vicugna pacos', photo='alpaca', alt='An alpaca in its long fleece, standing in a field of dry grass.'),
    F('mohair', 'Mohair', 'animal', 'Mohair', 'temperature', 'Warmth without weight',
      'On the winter side of a bed, with cashmere, silk and wool: warmth without weight.', photo='mohair', alt='Mohair close up: the long, lustrous, wavy hair of the Angora goat.'),
    F('silk', 'Silk', 'animal', 'Silk', 'softness temperature', 'Temperature · Softness',
      'The only animal fibre spun by a silkworm, fed on mulberry leaves. A continuous filament, fine and lustrous: light, insulating, '
      'elastic and flexible, held to be the finest and softest of the natural fibres.',
      [('800–1,000 m', 'Of filament from a single cocoon.')],
      species='Bombyx mori', photo='silk', alt='Silk satin, falling in soft folds.'),
    F('wool', 'Wool', 'animal', 'Wool', 'support temperature', 'Support · Temperature',
      'The most hygroscopic of the natural fibres. It keeps the body cool when it is warm and warm when it is cold, holds no static and resists mould. '
      'Ours comes from small farms: Cheviot, from Scotland, with the longest fibres, and Falkland.',
      [('⅓', 'Of its own weight in vapour, taken up without feeling wet.'), ('Never merino', 'From the extensive farms of Australia.')],
      origin='Scotland and the Falkland Islands', species='Ovis aries', photo='wool', alt='Sheep in full fleece, close together.'),
    F('horsehair', 'Horsehair', 'animal', 'Horsehair', 'support breathability', 'Support · Breathability',
      'Used in upholstery for centuries because it is elastic and flexible, and curling makes it more so. Like wool, it takes up the moisture '
      'of the night and gives it back to the air by day, keeping the bed fresh.',
      [('Horses only', 'Never the hair of other animals.')],
      origin='Argentina', species='Equus caballus', photo='horsehair', alt='The long, pale mane of a horse, close up.'),
    F('linen', 'Linen', 'plant', 'Linen', 'breathability', 'Breathability · Freshness',
      'From the stem of the flax plant, grown in the cool regions of northern Europe. A good conductor of heat, it feels cool against the skin: '
      'the fibre of the summer side.',
      [('20%', 'Of its own weight in moisture, absorbed.')],
      origin='Northern Europe', species='Linum usitatissimum', photo='linen', alt='Linen cloth, its weave close up.'),
    F('cotton', 'Organic cotton', 'plant', 'Cotton', 'breathability', 'Breathability',
      'Only from organic farms that keep to fair working conditions, since ordinary cotton crops use huge amounts of chemicals. '
      'Fresh and very breathable, for the warm months.',
      species='Gossypium', photo='cotton', alt='Cotton bolls opening on the plant.'),
    F('vegetable', 'Vegetable horsehair', 'plant', 'Vegetable Horsehair', 'support breathability', 'Support · Breathability',
      'Fibres from the leaves of palms, mainly the dwarf palm of southern Italy and Sicily, known as St Peter’s palm. The leaves are dried, '
      'curled and braided into ropes, like horsehair: soft, resilient and practically indestructible.',
      origin='Southern Italy and Sicily', species='Chamaerops humilis', photo='vegetable', alt='The fan-shaped leaves of a palm against the sky.'),
    F('ingeo', 'Ingeo', 'plant', 'Ingeo', 'breathability', 'Breathability · Freshness',
      'A sustainable fibre derived from maize. With wool, linen and cotton, it is on the summer side: fresh and breathable.',
      photo='ingeo', alt='Maize fibre, soft and white, close up.'),
    F('orange', 'Orange Fiber', 'plant', 'Orange Fiber', 'breathability', 'Freshness · Breathability',
      'An innovative, sustainable material made from Sicilian orange peels: light, breathable and naturally fresh.',
      origin='Sicily', photo='orange', alt='An orange cut across: the fruit whose peel becomes Orange Fiber.'),
]
