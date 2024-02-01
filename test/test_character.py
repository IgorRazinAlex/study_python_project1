from src.characters import *


def test_movement():
    human = Human((0, 0))

    assert (human.x == 0) and (human.y == 0)

    blocks = []  # fake empty level

    human.move_by_x(blocks, ['right'])

    assert human.x == 2.75

    human.move_by_y(blocks, ['jump'])

    assert human.y == 0
    assert human.in_air
    assert human.y_speed == 60
