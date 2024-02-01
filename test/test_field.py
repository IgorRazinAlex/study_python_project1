from src.field import FieldTranslator


def test_field_translator():
    translator = FieldTranslator()

    assert len(translator.field) == 0

    translator.read_file('1.csv')

    assert translator.get_objects() == translator.field
    assert len(translator.field) == 160
    assert translator.field[0] == {'type': 'hum', 'x': 25 * 20, 'y': 25 * 3}
    assert translator.field[1] == {'type': 'bs_t', 'x': 25 * 20, 'y': 25 * 5}
    assert translator.field[5] == {'type': 'bs_r', 'x': 25 * 18, 'y': 25 * 3}
    assert translator.field[48] == {'type': 'bc_tl', 'x': 25 * 12, 'y': 25 * 10}
