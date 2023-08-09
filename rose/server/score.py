""" Score logic """
import logging

import pygame
import six

from rose.common import actions, config, obstacles

log = logging.getLogger('score')


# def process(players, track):
#     """
#     Evaluate players actions and update player state and track
#
#     players: dict of player.Player objects
#     track: track.Track object
#     """
#
#     # First handle right and left actions, since they may change in_lane
#     # status, used for resolving collisions.
#
#     for player in six.itervalues(players):
#         if player.action == actions.LEFT:
#             if player.x > 0:
#                 player.x -= 1
#         elif player.action == actions.RIGHT:
#             if player.x < config.matrix_width - 1:
#                 player.x += 1
#
#     # Now handle obstacles, preferring players in their own lane.
#
#     sorted_players = sorted(six.itervalues(players),
#                             key=lambda p: 0 if p.in_lane() else 1)
#     positions = set()
#
#     for player in sorted_players:
#         player.score += config.score_move_forward
#         obstacle = track.get(player.x, player.y)
#         if obstacle == obstacles.CRACK:
#             if player.action != actions.JUMP:
#                 track.clear(player.x, player.y)
#                 player.y += 1
#                 player.score += config.score_move_backward * 2
#             else:
#                 player.score += config.score_jump
#         elif obstacle in (obstacles.TRASH,
#                           obstacles.BIKE,
#                           obstacles.BARRIER):
#             if player.action not in (actions.LEFT, actions.RIGHT):
#                 track.clear(player.x, player.y)
#                 player.y += 1
#                 player.score += config.score_move_backward * 2
#         elif obstacle == obstacles.WATER:
#             if player.action != actions.BRAKE:
#                 track.clear(player.x, player.y)
#                 player.y += 1
#                 player.score += config.score_move_backward * 2
#             else:
#                 player.score += config.score_brake
#         elif obstacle == obstacles.PENGUIN:
#             if player.action == actions.PICKUP:
#                 track.clear(player.x, player.y)
#                 player.score += config.score_move_forward
#
#         # Here we can end the game when player gets out of
#         # the track bounds. For now, just keep the player at the same
#         # location.
#         player.y = min(config.matrix_height - 1, max(2, player.y))
#
#         # Finally forget action
#         player.action = actions.NONE
#
#         # Fix up collisions
#
#         if (player.x, player.y) in positions:
#             log.info('player %s collision at %d,%d',
#                      player.name, player.x, player.y)
#             player.score += config.score_move_backward
#             if player.y < config.matrix_height - 1:
#                 player.y += 1
#             elif player.x > 0:
#                 player.x -= 1
#             elif player.x < config.matrix_width - 1:
#                 player.x += 1
#
#         log.info('process_actions: name=%s lane=%d pos=%d,%d score=%d '
#                  'response_time=%0.6f',
#                  player.name, player.lane, player.x, player.y, player.score,
#                  player.response_time)
#
#         positions.add((player.x, player.y))


def process(players, track):
    """
    Evaluate players actions and update player state and track

    players: dict of player.Player objects
    track: track.Track object
    """

    # First handle right and left actions, since they may change in_lane
    # status, used for resolving collisions.

    for player in six.itervalues(players):
        if player.action == actions.LEFT:
            if player.x > 0:
                player.x -= 1
        elif player.action == actions.RIGHT:
            if player.x < config.matrix_width - 1:
                player.x += 1

    # Now handle obstacles, preferring players in their own lane.

    sorted_players = sorted(six.itervalues(players),
                            key=lambda p: 0 if p.in_lane() else 1)
    positions = set()

    for player in sorted_players:
        player.score += config.score_move_backward
        obstacle = track.get(player.x, player.y)
        if obstacle == obstacles.CRACK:
            if player.action != actions.JUMP:
                track.clear(player.x, player.y)
                player.y += 1
                player.score += config.score_move_backward_obstacle
        elif obstacle in (obstacles.TRASH,
                          obstacles.BIKE,
                          obstacles.BARRIER):
            if player.action not in (actions.LEFT, actions.RIGHT):
                track.clear(player.x, player.y)
                player.y += 1
                player.score += config.score_move_backward_obstacle
        elif obstacle == obstacles.WATER:
            if player.action != actions.BRAKE:
                track.clear(player.x, player.y)
                player.y += 1
                player.score += config.score_move_backward_obstacle
        elif obstacle == obstacles.PENGUIN:
            if player.action == actions.PICKUP:
                if player.score < 100:
                    track.clear(player.x, player.y)
                    if player.score > 90:
                        player.score += 100 - player.score
                    else:
                        player.score += config.score_move_forward

        # Here we can end the game when player gets out of
        # the track bounds. For now, just keep the player at the same
        # location.
        player.y = min(config.matrix_height - 1, max(2, player.y))

        # Finally forget action
        player.action = actions.NONE

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

        log.info('process_actions: name=%s lane=%d pos=%d,%d score=%d '
                 'response_time=%0.6f',
                 player.name, player.lane, player.x, player.y, player.score,
                 player.response_time)

        positions.add((player.x, player.y))