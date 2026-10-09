"""What each system is made of, part by part, as the 2026 catalogue gives it (lp/catalogo_2026.txt,
the page and line noted). Used by tools/spec_audit.py to check the site's data against it.
Wool felt is a material of the base's build, not a fibre the site lists."""
CAT = {
  # page 20, line 205
  'top-2': {'base': {'Cheviot Wool'}, 'mattress': {'Cashmere', 'Baby Alpaca', 'Mohair', 'Horsehair', 'Cheviot Wool', 'Linen', 'Silk'},
            'topper': {'Yak Hair', 'Cheviot Wool', 'Linen'}},
  # page 24, line 295
  'giotto': {'base': {'Linen', 'Cheviot Wool', 'Horsehair'}, 'topper': {'Silk', 'Cheviot Wool'}},
  # page 28, line 363
  'brera': {'base': {'Wool'}, 'mattress': {'Wool', 'Yak Hair', 'Cotton', 'Ingeo'}},
  # page 32, line 437
  'capri': {'base': {'Linen', 'Cheviot Wool', 'Horsehair'}, 'topper': {'Silk', 'Cheviot Wool'}},
  # page 36, line 541
  'dreamy-2': {'base': {'Silk', 'Cheviot Wool'}, 'mattress': {'Cheviot Wool', 'Camel Hair', 'Silk'}, 'topper': {'Cheviot Wool', 'Horsehair', 'Silk', 'Linen'}},
  # page 40, line 673
  'storage': {'base': {'Cheviot Wool'}, 'mattress': {'Cheviot Wool', 'Silk', 'Cashmere'}},
  # page 44, line 725
  'amalfi': {'base': set(), 'mattress': {'Silk', 'Cheviot Wool', 'Cotton', 'Ingeo'}},
  # page 48, line 819
  'bellini': {'base': {'Cheviot Wool', 'Linen'}, 'mattress': {'Silk', 'Cheviot Wool', 'Horsehair', 'Linen', 'Ingeo', 'Cotton', 'Falkland Wool'},
              'topper': {'Silk', 'Cheviot Wool', 'Orange Fiber'}},
  # page 52, line 893
  'flora': {'base': {'Linen', 'Cheviot Wool'}, 'mattress': {'Yak Hair', 'Cheviot Wool', 'Linen', 'Orange Fiber'},
            'topper': {'Cheviot Wool', 'Horsehair', 'Silk', 'Orange Fiber'}},
  # page 56, line 961
  'paisley': {'base': {'Linen', 'Cheviot Wool'}, 'mattress': {'Cheviot Wool', 'Baby Alpaca', 'Linen'}, 'topper': {'Cheviot Wool', 'Silk', 'Linen'}},
  # page 60, line 1027
  'raffaello': {'mattress': {'Wool', 'Baby Alpaca', 'Cotton', 'Ingeo'}},
  # page 64, line 1155
  'vivaldi-2': {'mattress': {'Wool', 'Silk', 'Camel Hair', 'Cotton', 'Ingeo'}},
  # page 68, line 1271
  'vivaldi-plus': {'mattress': {'Wool', 'Cashmere', 'Silk', 'Cotton', 'Ingeo'}},
  # page 72, line 1399
  'bellagio': {'mattress': {'Yak Hair', 'Cheviot Wool', 'Linen', 'Ingeo'}},
  # page 76, line 1517
  'dreamy-springs': {'mattress': {'Cashmere', 'Camel Hair', 'Cheviot Wool', 'Horsehair', 'Linen', 'Ingeo'}},
  # page 80, line 1569
  'ultra-dry': {'mattress': {'Vegetable Horsehair', 'Linen', 'Cotton', 'Ingeo', 'Cheviot Wool', 'Silk', 'Cashmere'}, 'topper': {'Cheviot Wool', 'Cashmere'}},
  # page 84, line 1691
  'my-dream': {'mattress': {'Silk', 'Alpaca', 'Cheviot Wool'}},
  # page 88, line 1803
  'vicuna': {'mattress': {'Vicuña', 'Cashmere', 'Falkland Wool', 'Horsehair', 'Linen', 'Silk', 'Ingeo'}},
  # page 92, lines 1877 and 1889
  'roma': {'mattress': {'Silk', 'Falkland Wool', 'Horsehair', 'Linen', 'Ingeo', 'Cotton'}},
  'topper-roma': {'topper': {'Cashmere', 'Silk', 'Mohair', 'Falkland Wool', 'Linen', 'Ingeo'}},
  # page 96, line 1967
  'monteverdi': {'mattress': {'Vegetable Horsehair', 'Linen', 'Ingeo'}},
  # page 110: the high and medium toppers (one product on the store), and the thin topper
  'topper-high': {'topper': {'Linen', 'Ingeo', 'Silk', 'Wool', 'Vicuña', 'Horsehair'}},
  'topper-thin': {'topper': {'Silk', 'Ingeo', 'Wool'}},
}
