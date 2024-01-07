from common import actions, config
from game import player


def test_player_initialization():
    player1 = player.Player("John", 1, 1)

    assert player1.name == "John"
    assert player1.car == 1
    assert player1.lane == 1
    # player.Player x value should be middle of it's lane
    assert player1.x == player1.lane * config.cells_per_player + 1
    assert player1.y == config.matrix_height // 3 * 2
    assert player1.action == actions.NONE
    assert player1.response_time is None
    assert player1.score == 0


def test_player_reset():
    player1 = player.Player("John", 1, 1)

    player1.score = 50  # Modify player to make sure reset works
    player1.reset()
    assert player1.x == player1.lane * config.cells_per_player + 1
    assert player1.y == config.matrix_height // 3 * 2
    assert player1.action == actions.NONE
    assert player1.response_time is None
    assert player1.score == 0


def test_player_in_lane():
    player1 = player.Player("John", 1, 1)

    lane_start = player1.lane * config.cells_per_player

    for offset in range(config.cells_per_player):
        player1.x = lane_start + offset
        assert player1.in_lane()


def test_player_not_in_lane():
    player1 = player.Player("John", 1, 1)

    # Modify player's position to be out of their lane
    other_lane = (player1.lane + 1) % config.max_players
    other_lane_start = other_lane * config.cells_per_player

    for offset in range(config.cells_per_player):
        player1.x = other_lane_start + offset
        assert not player1.in_lane()


def test_player_comparison():
    player1 = player.Player("John", 1, 1)
    player2 = player.Player("Doe", 2, 2)

    # Initial scores are the same
    assert not player1 < player2
    assert not player2 < player1

    # Modify scores
    player1.score = 10
    player2.score = 20

    assert player1 < player2


def test_player_state():
    player1 = player.Player("John", 2, 1)

    expected_state = {
        "name": "John",
        "car": 2,
        "x": 4,  # 1 * config.cells_per_player + 1
        "y": config.matrix_height // 3 * 2,
        "action": actions.NONE,
        "response_time": None,
        "error": None,
        "lane": 1,
        "score": 0,
        "pickups": 0,
        "misses": 0,
        "hits": 0,
        "breaks": 0,
        "jumps": 0,
        "collisions": 0,
    }

    assert player1.state() == expected_state
