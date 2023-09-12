import pytest
from game.track import Track


def test_track_initialization():
    t = Track()
    assert t.max_x == 0
    assert t.max_y == 0

    t2 = Track([["a", "b"], ["c", "d"]])
    assert t2.max_x == 2
    assert t2.max_y == 2


def test_track_get():
    t = Track([["a", "b"], ["c", "d"]])
    assert t.get(0, 0) == "a"
    assert t.get(1, 0) == "b"
    assert t.get(0, 1) == "c"
    assert t.get(1, 1) == "d"


def test_track_get_out_of_bounds():
    t = Track([["a", "b"], ["c", "d"]])

    with pytest.raises(IndexError, match="x out of range: 0-1"):
        t.get(2, 0)

    with pytest.raises(IndexError, match="y out of range: 0-1"):
        t.get(0, 2)


def test_track_validate_pos():
    t = Track([["a", "b"], ["c", "d"]])

    # These should not raise any errors
    t._validate_pos(0, 0)
    t._validate_pos(1, 0)
    t._validate_pos(0, 1)
    t._validate_pos(1, 1)

    with pytest.raises(IndexError, match="x out of range: 0-1"):
        t._validate_pos(2, 0)

    with pytest.raises(IndexError, match="y out of range: 0-1"):
        t._validate_pos(0, 2)
