from game.obstacles import (
    NONE,
    CRACK,
    TRASH,
    PENGUIN,
    BIKE,
    WATER,
    BARRIER,
    ALL,
    get_random_obstacle,
)


def test_constants():
    assert NONE == ""
    assert CRACK == "crack"
    assert TRASH == "trash"
    assert PENGUIN == "penguin"
    assert BIKE == "bike"
    assert WATER == "water"
    assert BARRIER == "barrier"


def test_all_constant():
    assert ALL == (NONE, CRACK, TRASH, PENGUIN, BIKE, WATER, BARRIER)


def test_get_random_obstacle():
    # This test checks if the function returns a valid obstacle
    obstacle = get_random_obstacle()
    assert obstacle in ALL
