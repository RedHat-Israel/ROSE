from game.actions import NONE, RIGHT, LEFT, PICKUP, JUMP, BRAKE, ALL


def test_constants():
    assert NONE == "none"
    assert RIGHT == "right"
    assert LEFT == "left"
    assert PICKUP == "pickup"
    assert JUMP == "jump"
    assert BRAKE == "brake"


def test_all_constant():
    assert ALL == (NONE, RIGHT, LEFT, PICKUP, JUMP, BRAKE)
