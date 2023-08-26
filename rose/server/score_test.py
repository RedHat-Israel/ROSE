from rose.common import actions, config, obstacles
from . import track
from . import player
from . import score
import pytest


FORWARD_ACTIONS = [a for a in actions.ALL
                   if a not in (actions.RIGHT, actions.LEFT)]


class SinglePlayerTest(object):

    # Must be defined in subclass
    obstacle = None

    def setup_method(self, m):
        self.track = track.Track()
        self.player = player.Player("A", car=0, lane=0)
        self.x = self.player.x
        self.y = self.player.y
        self.score = self.player.score
        self.track.set(self.x, self.y, self.obstacle)

    def process(self):
        score.process({self.player.name: self.player}, self.track)

    def assert_score(self, score):
        assert self.player.x == self.x
        assert self.player.y == self.y
        assert self.player.score == score + config.score_move_forward

    def assert_move_right(self):
        assert self.player.x == self.x + 1
        assert self.player.y == self.y
        assert self.player.score == self.score + config.score_move_forward

    def assert_move_left(self):
        assert self.player.x == self.x - 1
        assert self.player.y == self.y
        assert self.player.score == self.score + config.score_move_forward

    def assert_move_back(self):
        assert self.player.x == self.x
        assert self.player.y == self.y + 1
        assert self.player.score == self.score - config.score_move_forward

    def assert_move_back_no_punish(self):
        assert self.player.x == self.x
        assert self.player.y == self.y + 1
        assert self.player.score == self.score - config.score_move_forward

    def assert_keep_obstacle(self):
        assert self.track.get(self.x, self.y) == self.obstacle

    def assert_remove_obstacle(self):
        assert self.track.get(self.x, self.y) == obstacles.NONE


class TestNoObstacle(SinglePlayerTest):

    obstacle = obstacles.NONE

    def test_right(self):
        self.player.action = actions.RIGHT
        self.process()
        self.assert_move_right()
        self.assert_keep_obstacle()

    def test_left(self):
        self.player.action = actions.LEFT
        self.process()
        self.assert_move_left()
        self.assert_keep_obstacle()

    @pytest.mark.parametrize("action", FORWARD_ACTIONS)
    def test_forward(self, action):
        self.player.action = action
        self.process()
        self.assert_score(self.score)
        self.assert_keep_obstacle()


class TestPenguin(SinglePlayerTest):
    """
    Handling penguins

    If player pick the penguin, it move forward and get more score. Otherwise
    the penguin is skipped and can be picked by other players.
    """

    obstacle = obstacles.PENGUIN

    def test_pickup(self):
        self.player.action = actions.PICKUP
        self.process()
        # Player move up and get more score
        assert self.player.x == self.x
        assert self.player.y == self.y
        assert self.player.score == self.score + config.score_move_forward * 2
        self.assert_remove_obstacle()

    def test_right(self):
        self.player.action = actions.RIGHT
        self.process()
        self.assert_move_right()
        self.assert_keep_obstacle()

    def test_left(self):
        self.player.action = actions.LEFT
        self.process()
        self.assert_move_left()
        self.assert_keep_obstacle()

    @pytest.mark.parametrize(
        "action", [a for a in FORWARD_ACTIONS if a != actions.PICKUP])
    def test_other(self, action):
        self.player.action = action
        self.process()
        self.assert_score(self.score)
        self.assert_keep_obstacle()


class MagicActionTest(SinglePlayerTest):
    """
    Handling obstacles with magic action

    If player choose the magic action the obstale is skipped. If player does
    not turn right or left, it moves back and the obstacle is consumed.
    """

    # Must be defined in subclass
    action = None
    magic_score = None

    @pytest.mark.parametrize("action", FORWARD_ACTIONS)
    def test_forward(self, action):
        self.player.action = action
        self.process()
        if action == self.action:
            self.assert_score(self.score + self.magic_score)
            self.assert_keep_obstacle()
        else:
            self.assert_move_back()
            self.assert_remove_obstacle()

    def test_right(self):
        self.player.action = actions.RIGHT
        self.process()
        self.assert_move_right()
        self.assert_keep_obstacle()

    def test_left(self):
        self.player.action = actions.LEFT
        self.process()
        self.assert_move_left()
        self.assert_keep_obstacle()


class TestCrack(MagicActionTest):
    magic_score = config.score_jump
    obstacle = obstacles.CRACK
    action = actions.JUMP


class TestWater(MagicActionTest):
    magic_score = config.score_brake
    obstacle = obstacles.WATER
    action = actions.BRAKE


class TurnTest(SinglePlayerTest):
    """
    Handling obstacles that have no magic action

    Player must turn right or left, or it will move back.
    """

    def test_right(self):
        self.player.action = actions.RIGHT
        self.process()
        self.assert_move_right()
        self.assert_keep_obstacle()

    def test_left(self):
        self.player.action = actions.LEFT
        self.process()
        self.assert_move_left()
        self.assert_keep_obstacle()

    @pytest.mark.parametrize("action", FORWARD_ACTIONS)
    def test_other(self, action):
        self.player.action = action
        self.process()
        # TODO: decrease points on redundant action?
        self.assert_move_back_no_punish()
        self.assert_remove_obstacle()


class TestTrash(TurnTest):
    obstacle = obstacles.TRASH


class TestBike(TurnTest):
    obstacle = obstacles.BIKE


class TestBarrier(TurnTest):
    obstacle = obstacles.BARRIER


class TestLimits(SinglePlayerTest):
    """
    Handling movement out of the track
    """
    obstacle = obstacles.NONE

    def test_left(self):
        # TODO: decrease score? move back?
        self.x = self.player.x = 0
        self.player.action = actions.LEFT
        self.process()
        self.assert_score(self.score)
        self.assert_keep_obstacle()

    def test_right(self):
        # TODO: decrease score? move back?
        self.x = self.player.x = config.matrix_width - 1
        self.player.action = actions.RIGHT
        self.process()
        self.assert_score(self.score)
        self.assert_keep_obstacle()

    def test_forward(self):
        self.y = self.player.y = 0
        self.player.action = actions.PICKUP
        self.obstacle = obstacles.PENGUIN
        self.track.set(self.x, self.y, self.obstacle)
        self.process()
        # Player keep position but get more score
        assert self.player.x == self.x
        assert self.player.y == self.y + 2
        assert self.player.score == self.score + config.score_move_forward * 2
        self.assert_remove_obstacle()

    def test_back(self):
        # TODO: always decrease score
        self.y = self.player.y = config.matrix_height - 1
        self.player.action = actions.NONE
        self.player.score = 0
        self.obstacle = obstacles.TRASH
        self.track.set(self.x, self.y, self.obstacle)
        self.process()
        self.assert_score(config.score_move_backward * 2)
        self.assert_remove_obstacle()


class TestCollisions(object):
    """
    Handling case where two players try to move to the same cell.

    Current behavior is to prefer the players with smaller y value and smaller
    response_time.

    TODO: change behavior to prefer the player in its lane, so driving in other
    player lane is more risky.
    """

    def setup_method(self, m):
        self.track = track.Track()
        self.player1 = player.Player("A", car=0, lane=0)
        self.player2 = player.Player("B", car=0, lane=1)

    def process(self):
        players = {self.player1.name: self.player1,
                   self.player2.name: self.player2}
        score.process(players, self.track)

    def test_player_in_lane_wins(self):
        self.track.set(1, 6, obstacles.PENGUIN)
        # Player 1 in its lane at 1,5, missed the penguin.
        self.player1.x = 1
        self.player1.y = 5
        self.player1.score = 0
        self.player1.action = actions.NONE
        # Player 2 is not in its lane, trying to pick up the penguin.
        self.player2.x = 1
        self.player2.y = 6
        self.player2.score = 0
        self.player2.action = actions.PICKUP
        self.process()
        # Player got the normal score for this step.
        assert self.player1.x == 1
        assert self.player1.y == 5
        assert self.player1.score == config.score_move_forward
        # Player 2 picked up the penging, got extra score.
        assert self.player2.x == 1
        assert self.player2.y == 6
        assert self.player2.score == config.score_move_forward * 2

    def test_after_turn_to_not_in_lane(self):
        # Player 1 in its lane at 2,5
        self.player1.x = 2
        self.player1.y = 5
        self.player1.score = 0
        self.player1.action = actions.NONE
        # Player 2 in its lane, but after turning left will not be in his lane.
        self.player2.x = 3
        self.player2.y = 5
        self.player2.score = 0
        self.player2.action = actions.LEFT
        self.process()
        # Player 1 win because it is in lane
        assert self.player1.x == 2
        assert self.player1.y == 5
        assert self.player1.score == self.player1.score
        # Player 2 got more score but move back
        assert self.player2.x == 2
        assert self.player2.y == 6
        # TODO - decrease score when out of lane?
        assert self.player2.score == 0

    def test_move_left_out_of_world(self):
        # Player 1 in its lane at 1,8
        self.player1.x = 1
        self.player1.y = 8
        self.player1.score = 0
        self.player1.action = actions.NONE
        # Player 2 trying to move to 1,8
        self.player2.x = 0
        self.player2.y = 8
        self.player2.score = 0
        self.player2.action = actions.RIGHT
        self.process()
        # Player 1 win because it is in own lane
        assert self.player1.x == 1
        assert self.player1.y == 8
        assert self.player1.score == 0 + config.score_move_forward
        # Player 2 moved left, first free cell
        assert self.player2.x == 0
        assert self.player2.y == 8
        # TODO: decrease score?
        assert self.player2.score == 0

    def test_move_right_out_of_world(self):
        # Player 1 in its lane at 0,8
        self.player1.x = 0
        self.player1.y = 8
        self.player1.score = 0
        self.player1.action = actions.NONE
        # Player 2 move from 1,8 to 0,8
        self.player2.x = 1
        self.player2.y = 8
        self.player2.score = 0
        self.player2.action = actions.LEFT
        self.process()
        # Player 1 win because it is in own lane
        assert self.player1.x == 0
        assert self.player1.y == 8
        assert self.player1.score == 0 + config.score_move_forward
        # Player 2 moved right, no other possible cell
        assert self.player2.x == 1
        assert self.player2.y == 8
        # TODO: decrease score?
        assert self.player2.score == 0
