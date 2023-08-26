""" Score logic """
import logging

from rose.common import actions, config, obstacles

log = logging.getLogger('score')


def process(players, track):
    """
    Evaluate players actions and update player state and track

    players: dict of player.Player objects
    track: track.Track object
    """

    # First handle right and left actions, since they may change in_lane
    # status, used for resolving collisions.

    for player in players.values():
        if player.action == actions.LEFT:
            if player.x > 0:
                player.x -= 1
        elif player.action == actions.RIGHT:
            if player.x < config.matrix_width - 1:
                player.x += 1

    # Proccess the players by order, first the ones in lane and then
    # the ones out of lane, this ensure the car in lane will have
    # priority when picking pinguins and in case of collisions.

    sorted_players = sorted(players.values(),
                            key=lambda p: 0 if p.in_lane() else 1)
    positions = set()

    # Now handle obstacles, preferring players in their own lane.

    for player in sorted_players:
        obstacle = track.get(player.x, player.y)

        if obstacle == obstacles.NONE:
            # Move forward, leaving the obstacle on the track.
            player.score += config.score_move_forward

        elif obstacle in (obstacles.TRASH,
                          obstacles.BIKE,
                          obstacles.BARRIER):
            # Move back consuming the obstacle.
            track.clear(player.x, player.y)
            player.y += 1
            player.score += config.score_move_backward

        elif obstacle == obstacles.CRACK:
            if player.action == actions.JUMP:
                # Move forward leaving the obstacle on the track
                player.score += config.score_move_forward + config.score_jump
            else:
                # Move back consuming the obstacle.
                track.clear(player.x, player.y)
                player.y += 1
                player.score += config.score_move_backward

        elif obstacle == obstacles.WATER:
            if player.action == actions.BRAKE:
                # Move forward leaving the obstacle on the track
                player.score += config.score_move_forward + config.score_brake
            else:
                # Move back consuming the obstacle.
                track.clear(player.x, player.y)
                player.y += 1
                player.score += config.score_move_backward

        elif obstacle == obstacles.PENGUIN:
            if player.action == actions.PICKUP:
                # Move forward and collect an aquatic bird
                track.clear(player.x, player.y)
                player.score += config.score_move_forward + config.score_pickup
            else:
                # Move forward leaving the obstacle on the track
                player.score += config.score_move_forward

        # Here we can end the game when player gets out of
        # the track bounds. For now, just keep the player at the same
        # location.
        player.y = min(config.matrix_height - 1, max(2, player.y))

        # Fix up collisions

        if (player.x, player.y) in positions:
            log.info('player %s collision at %d,%d',
                     player.name, player.x, player.y)
            player.score += config.score_move_backward
            if player.y < config.matrix_height - 1:
                player.y += 1
            elif player.x > 0:
                player.x -= 1
            elif player.x < config.matrix_width - 1:
                player.x += 1

        # Finally forget action
        player.action = actions.NONE

        positions.add((player.x, player.y))

        log.info('process_actions: name=%s lane=%d pos=%d,%d score=%d '
                 'response_time=%0.6f',
                 player.name, player.lane, player.x, player.y, player.score,
                 player.response_time)
