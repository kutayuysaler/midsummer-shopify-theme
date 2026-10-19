"""The house's words in Italian and Russian, one source for the build (bin/build_r23.py: the fibre
marks and atlas links that must still recognise a translated fibre name) and for the translation
tables (tools/tr_compile.py: fibre lists and data strings composed from these words).

FIBRES: the fibre names as the data writes them (Title Case), with their Italian and Russian names.
LOWER: the same names as they sit inside a sentence ("{fibres} carry the warmth").
NEEDS: the qualities a fibre answers, as the data writes them after a fibre (Silk~Temperature · Softness).
"""

FIBRES = {
    'Silk': ('Seta', 'Шёлк'),
    'Wool': ('Lana', 'Шерсть'),
    'Cheviot Wool': ('Lana Cheviot', 'Шерсть чевиот'),
    'Falkland Wool': ('Lana Falkland', 'Фолклендская шерсть'),
    'Falkland': ('Lana Falkland', 'Фолклендская шерсть'),
    'Horsehair': ('Crine di cavallo', 'Конский волос'),
    'Vegetable Horsehair': ('Crine vegetale', 'Растительный волос'),
    'Linen': ('Lino', 'Лён'),
    'Cotton': ('Cotone', 'Хлопок'),
    'Organic Cotton': ('Cotone biologico', 'Органический хлопок'),
    'Cashmere': ('Cashmere', 'Кашемир'),
    'Mongolian Cashmere': ('Cashmere della Mongolia', 'Монгольский кашемир'),
    'Vicuña': ('Vigogna', 'Викунья'),
    'Camel Hair': ('Pelo di cammello', 'Верблюжья шерсть'),
    'Yak Hair': ('Pelo di yak', 'Шерсть яка'),
    'Yak': ('Yak', 'Як'),
    'Baby Alpaca': ('Baby alpaca', 'Бэби-альпака'),
    'Alpaca': ('Alpaca', 'Альпака'),
    'Alpaca Wool': ('Lana d’alpaca', 'Шерсть альпаки'),
    'Mohair': ('Mohair', 'Мохер'),
    'Ingeo': ('Ingeo', 'Ingeo'),
    'Orange Fiber': ('Orange Fiber', 'Orange Fiber'),
    'Hemp': ('Canapa', 'Конопля'),
}

LOWER = {
    'baby alpaca': ('baby alpaca', 'бэби-альпака'),
    'alpaca': ('alpaca', 'альпака'),
    'wool': ('lana', 'шерсть'),
    'Cheviot wool': ('lana Cheviot', 'шерсть чевиот'),
    'Falkland wool': ('lana Falkland', 'фолклендская шерсть'),
    'horsehair': ('crine di cavallo', 'конский волос'),
    'vegetable horsehair': ('crine vegetale', 'растительный волос'),
    'yak hair': ('pelo di yak', 'шерсть яка'),
    'vicuña': ('vigogna', 'викунья'),
    'cashmere': ('cashmere', 'кашемир'),
    'mohair': ('mohair', 'мохер'),
    'camel hair': ('pelo di cammello', 'верблюжья шерсть'),
    'linen': ('lino', 'лён'),
    'silk': ('seta', 'шёлк'),
    'cotton': ('cotone', 'хлопок'),
    'Ingeo': ('Ingeo', 'Ingeo'),
    'Orange Fiber': ('Orange Fiber', 'Orange Fiber'),
}

NEEDS = {
    'Temperature': ('Temperatura', 'Терморегуляция'),
    'Softness': ('Morbidezza', 'Мягкость'),
    'Support': ('Sostegno', 'Поддержка'),
    'Breathability': ('Traspirabilità', 'Воздухопроницаемость'),
    'Freshness': ('Freschezza', 'Свежесть'),
    'Hypoallergenic': ('Ipoallergenico', 'Гипоаллергенность'),
    'Resilience': ('Elasticità', 'Упругость'),
    'Warmth': ('Calore', 'Тепло'),
    'Structure': ('Struttura', 'Структура'),
    'Durability': ('Durata', 'Долговечность'),
    'Lightness': ('Leggerezza', 'Лёгкость'),
    'Moisture': ('Umidità', 'Влагоотведение'),
    'Warmth without weight': ('Calore senza peso', 'Тепло без тяжести'),
}


def mark_aliases():
    """every Italian and Russian fibre name (lower case) with the English one the marks know"""
    out = {}
    for en, (it, ru) in list(FIBRES.items()) + [(k, v) for k, v in LOWER.items()]:
        for x in (it, ru):
            x = x.lower()
            if x != en.lower():
                out.setdefault(x, en.lower())
        if 'ё' in ru.lower():
            out.setdefault(ru.lower().replace('ё', 'е'), en.lower())
    return out
