from src.blocks import *


def test_block_creation():
    block1 = Block((10, 20), 'b')
    assert (block1.x == 10) and (block1.y == 20)


def test_spike_creation():
    spike1 = Spike((3, 16), 's_b')
    assert (spike1.x == 3) and (spike1.y == 16)


def test_orb_creation():
    orb1 = Orb((21, 14))
    assert (orb1.x == 21) and (orb1.y == 14)


def test_portal_creation():
    portal1 = EndPortal((100, 13))
    assert (portal1.x == 100) and (portal1.y == 13)
