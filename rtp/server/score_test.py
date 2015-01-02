from rtp.common import actions, config, obstacles
import track
import player
import score

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
        self.life = self.player.life
        self.track.set(self.x, self.y, self.obstacle)

    def process(self):
        score.process({self.player.name: self.player}, self.track)

    def assert_keep_player(self):
        assert self.player.x == self.x
        assert self.player.y == self.y
        assert self.player.life == self.life

    def assert_move_right(self):
        assert self.player.x == self.x + 1
        assert self.player.y == self.y
        assert self.player.life == self.life

    def assert_move_left(self):
        assert self.player.x == self.x - 1
        assert self.player.y == self.y
        assert self.player.life == self.life

    def assert_move_back(self):
        assert self.player.x == self.x
        assert self.player.y == self.y + 1
        assert self.player.life == self.life

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

    def test_forward(self):
        for action in FORWARD_ACTIONS:
            self.player.action = action
            self.process()
            self.assert_keep_player()
            self.assert_keep_obstacle()


class TestPenguin(SinglePlayerTest):
    """
    Handling penguins

    If player pick the penguin, it move forward and get more life. Otherwise
    the penguin is skipped and can be picked by other players.
    """

    obstacle = obstacles.PENGUIN

    def test_pickup(self):
        self.player.action = actions.PICKUP
        self.process()
        # Player move up and get more life
        assert self.player.x == self.x
        assert self.player.y == self.y - 1
        assert self.player.life == self.life + 1
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

    def test_other(self):
        for action in [a for a in FORWARD_ACTIONS if a != actions.PICKUP]:
            self.player.action = action
            self.process()
            self.assert_keep_player()
            self.assert_keep_obstacle()


class MagicActionTest(SinglePlayerTest):
    """
    Handling obstacles with magic action

    If player choose the magic action the obstale is skipped. If player does
    not turn right or left, it moves back and the obstacle is consumed.
    """

    # Must be defined in subclass
    action = None

    def test_magic_action(self):
        self.player.action = self.action
        self.process()
        self.assert_keep_player()
        self.assert_keep_obstacle()

    def test_other_action(self):
        for action in [a for a in FORWARD_ACTIONS if a != self.action]:
            self.player.action = action
            self.process()
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
    obstacle = obstacles.CRACK
    action = actions.JUMP


class TestWater(MagicActionTest):
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

    def test_other(self):
        for action in FORWARD_ACTIONS:
            self.player.action = action
            self.process()
            self.assert_move_back()
            self.assert_remove_obstacle()


class TestTrash(TurnTest):
    obstacle = obstacles.TRASH


class TestBike(TurnTest):
    obstacle = obstacles.BIKE


class TestBarrier(TurnTest):
    obstacle = obstacles.BARRIER


class TestLimits(SinglePlayerTest):
    """
    Handling movment out of the track
    """
    obstacle = obstacles.NONE

    def test_left(self):
        # TODO: decrease life? move back?
        self.x = self.player.x = 0
        self.player.action = actions.LEFT
        self.process()
        self.assert_keep_player()
        self.assert_keep_obstacle()

    def test_right(self):
        # TODO: decrease life? move back?
        self.x = self.player.x = config.matrix_width - 1
        self.player.action = actions.RIGHT
        self.process()
        self.assert_keep_player()
        self.assert_keep_obstacle()

    def test_forward(self):
        self.y = self.player.y = 0
        self.player.action = actions.PICKUP
        self.obstacle = obstacles.PENGUIN
        self.track.set(self.x, self.y, self.obstacle)
        self.process()
        # Player keep position but get more life
        assert self.player.x == self.x
        assert self.player.y == self.y
        assert self.player.life == self.life + 1
        self.assert_remove_obstacle()

    def test_back(self):
        # TODO: always decrease life
        self.y = self.player.y = config.matrix_height - 1
        self.player.action = actions.NONE
        self.obstacle = obstacles.TRASH
        self.track.set(self.x, self.y, self.obstacle)
        self.process()
        self.assert_keep_player()
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
        players = {self.player1.name: self.player1, self.player2.name: self.player2}
        score.process(players, self.track)

    def test_player_in_lane_wins(self):
        # Player 1 in its lane at 1,5
        self.player1.x = 1
        self.player1.y = 5
        self.player1.life = 0
        self.player1.action = actions.NONE
        # Player 2 is not in its lane, trying to pick penguin at 1,6
        self.track.set(1, 6, obstacles.PENGUIN)
        self.player2.x = 1
        self.player2.y = 6
        self.player2.life = 0
        self.player2.action = actions.PICKUP
        self.process()
        # Player 1 win because it is in lane
        assert self.player1.x == 1
        assert self.player1.y == 5
        assert self.player1.life == 0
        # Player 2 got more life but move back
        assert self.player2.x == 1
        assert self.player2.y == 6
        assert self.player2.life == 1

    def test_move_left(self):
        # Player 1 in its lane at 1,8
        self.player1.x = 1
        self.player1.y = 8
        self.player1.life = 0
        self.player1.action = actions.NONE
        # Player 2 trying to move to 1,8
        self.player2.x = 0
        self.player2.y = 8
        self.player2.life = 0
        self.player2.action = actions.RIGHT
        self.process()
        # Player 1 win because it is in own lane
        assert self.player1.x == 1
        assert self.player1.y == 8
        assert self.player1.life == 0
        # Player 2 moved left, first free cell
        assert self.player2.x == 0
        assert self.player2.y == 8
        # TODO: decrease life?
        assert self.player2.life == 0

    def test_move_right(self):
        # Player 1 in its lane at 0,8
        self.player1.x = 0
        self.player1.y = 8
        self.player1.life = 0
        self.player1.action = actions.NONE
        # Player 2 move from 1,8 to 0,8
        self.player2.x = 1
        self.player2.y = 8
        self.player2.life = 0
        self.player2.action = actions.LEFT
        self.process()
        # Player 1 win because it is in own lane
        assert self.player1.x == 0
        assert self.player1.y == 8
        assert self.player1.life == 0
        # Player 2 moved right, no other possible cell
        assert self.player2.x == 1
        assert self.player2.y == 8
        # TODO: decrease life?
        assert self.player2.life == 0
