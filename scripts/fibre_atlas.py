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

def F(fibre, name, group, mark, q, ql, lead, figs=(), origin='', species='', photo='none', alt=''):
    st = {'fibre': fibre, 'name': name, 'group': group, 'mark': mark, 'qualities': q, 'quality_label': ql, 'lead': lead, 'photo': photo}
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
      [('100–200 g', 'Of fine fibre from one goat, in a year.'), ('Mongolia', 'The only place our cashmere comes from.')],
      origin='Mongolia', species='Capra hircus', photo='cashmere', alt='A herd of goats coming down a mountain valley.'),
    F('camel', 'Camel hair', 'animal', 'Camel Hair', 'temperature', 'Warmth · Temperature',
      'It shields the camel from the extremes of the desert, cold and heat, and does the same in a bed. Fine and soft, it holds a great deal of air, '
      'and it is more hygroscopic than sheep’s wool: a dry, pleasant warmth.',
      [('700 g', 'At most, combed from one young camel in a year.')],
      origin='Asia', species='Camelus bactrianus'),
    F('yak', 'Yak', 'animal', 'Yak Hair', 'temperature softness', 'Warmth · Softness',
      'A fine, very warm and particularly robust hair, soft and fluffy, with the look of cashmere. The yak is neither shorn nor combed: '
      'in May its winter undercoat falls, and the nomads gather it.',
      [('May', 'When the undercoat falls, and is gathered.'), ('Never', 'Shorn or combed: collected once it is shed.')],
      species='Bos grunniens', photo='yak', alt='A yak on a misty mountainside.'),
    F('alpaca', 'Baby alpaca', 'animal', 'Baby Alpaca', 'temperature hypoallergenic', 'Temperature · Hypoallergenic',
      'From an animal of the high South American ranges, with an abundant fleece, soft and almost silky. The fibre sits between wool and cashmere, '
      'nearer to cashmere; alpaca cloth was once kept for the Inca emperors.',
      [('No lanolin', 'And so naturally hypoallergenic.')],
      origin='The South American highlands', species='Vicugna pacos'),
    F('mohair', 'Mohair', 'animal', 'Mohair', 'temperature', 'Warmth without weight',
      'On the winter side of a bed, with cashmere, silk and wool: warmth without weight.'),
    F('silk', 'Silk', 'animal', 'Silk', 'softness temperature', 'Temperature · Softness',
      'The only animal fibre spun by a silkworm, fed on mulberry leaves. A continuous filament, fine and lustrous: light, insulating, '
      'elastic and flexible, held to be the finest and softest of the natural fibres.',
      [('800–1,000 m', 'Of filament from a single cocoon.')],
      species='Bombyx mori', photo='silk', alt='Silk satin, falling in soft folds.'),
    F('wool', 'Wool', 'animal', 'Wool', 'support temperature', 'Support · Temperature',
      'The most hygroscopic of the natural fibres. It keeps the body cool when it is warm and warm when it is cold, holds no static and resists mould. '
      'Ours comes from small farms: Cheviot, from Scotland, with the longest fibres, and Falkland.',
      [('⅓', 'Of its own weight in vapour, taken up without feeling wet.'), ('Small farms', 'Never merino from extensive Australian farms.')],
      species='Ovis aries', photo='wool', alt='Sheep in full fleece, close together.'),
    F('horsehair', 'Horsehair', 'animal', 'Horsehair', 'support breathability', 'Support · Breathability',
      'Used in upholstery for centuries because it is elastic and flexible, and curling makes it more so. Like wool, it takes up the moisture '
      'of the night and gives it back to the air by day, keeping the bed fresh.',
      [('Argentina', 'Where the horses live free.'), ('Horses only', 'Never the hair of other animals.')],
      origin='Argentina', species='Equus caballus', photo='horsehair', alt='The long, pale mane of a horse, close up.'),
    F('linen', 'Linen', 'plant', 'Linen', 'breathability', 'Breathability · Freshness',
      'From the stem of the flax plant, grown in the cool regions of northern Europe. A good conductor of heat, it feels cool against the skin: '
      'the fibre of the summer side.',
      [('20%', 'Of its own weight in moisture, absorbed.')],
      origin='Northern Europe', species='Linum usitatissimum'),
    F('cotton', 'Organic cotton', 'plant', 'Cotton', 'breathability', 'Breathability',
      'Only from organic farms that keep to fair working conditions, since ordinary cotton crops use huge amounts of chemicals. '
      'Fresh and very breathable, for the warm months.',
      [('Organic', 'Farms only, with fair working conditions.')],
      species='Gossypium', photo='cotton', alt='Cotton bolls opening on the plant.'),
    F('vegetable', 'Vegetable horsehair', 'plant', 'Vegetable Horsehair', 'support breathability', 'Support · Breathability',
      'Fibres from the leaves of palms, mainly the dwarf palm of southern Italy and Sicily, known as St Peter’s palm. The leaves are dried, '
      'curled and braided into ropes, like horsehair: soft, resilient and practically indestructible.',
      [('Sicily', 'And southern Italy, where the palm grows.')],
      origin='Southern Italy and Sicily', species='Chamaerops humilis'),
    F('ingeo', 'Ingeo', 'plant', 'Ingeo', 'breathability', 'Breathability · Freshness',
      'A sustainable fibre derived from maize. With wool, linen and cotton, it is on the summer side: fresh and breathable.',
      [('Maize', 'The plant it is drawn from.')]),
    F('orange', 'Orange Fiber', 'plant', 'Orange Fiber', 'breathability', 'Freshness · Breathability',
      'An innovative, sustainable material made from Sicilian orange peels: light, breathable and naturally fresh.',
      [('Orange peel', 'From Sicily’s oranges.')]),
]
