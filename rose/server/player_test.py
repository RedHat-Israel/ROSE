from . import player


def test_in_lane():
    p = player.Player("A", car=0, lane=0)
    for x in (0, 1, 2):
        p.x = x
        assert p.in_lane()


def test_not_in_lane():
    p = player.Player("A", car=0, lane=1)
    for x in (0, 1, 2):
        p.x = x
        assert not p.in_lane()
