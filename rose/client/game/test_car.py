import pytest
from game.car import Car


def test_car_initialization():
    info = {"x": 5, "y": 10}
    car = Car(info)

    assert car.x == 5
    assert car.y == 10


def test_car_initialization_missing_key():
    info_missing_x = {"y": 10}
    info_missing_y = {"x": 5}

    with pytest.raises(KeyError):
        Car(info_missing_x)

    with pytest.raises(KeyError):
        Car(info_missing_y)
