""" Score logic """

from rtp.common import actions, config, obstacles

def process(players, track):
    """
    Evaluate players actions and update player state and track

    players: dict of player.Player objects
    track: track.Track object
    """
    # Process first the leading drivers, preferring those with faster
    # response time.
    sorted_players = sorted(players.itervalues(),
                     key=lambda p: (p.y , p.response_time))
    positions = set()

    for player in sorted_players:

        # First move playe, keeping inside the track

        if player.action == actions.LEFT:
            if player.x > 0:
                player.x -= 1
        elif player.action == actions.RIGHT:
            if player.x < config.matrix_width - 1:
                player.x += 1

        # Now check if player hit any obstacle

        obstacle = track.get(player.x, player.y)
        if obstacle == obstacles.CRACK:
            if player.action != actions.JUMP:
                track.clear(player.x, player.y)
                player.y += 1
        elif obstacle in (obstacles.TRASH,
                          obstacles.BIKE,
                          obstacles.BARRIER):
            track.clear(player.x, player.y)
            player.y += 1
        elif obstacle == obstacles.WATER:
            if player.action != actions.BRAKE:
                track.clear(player.x, player.y)
                player.y += 1
        elif obstacle == obstacles.PENGUIN:
            if player.action == actions.PICKUP:
                track.clear(player.x, player.y)
                player.y -= 1
                player.life += 1

        # Here we can end the game when player gets out of
        # the track bounds. For now, just keep the player at the same
        # location.
        player.y = min(config.matrix_height - 1, max(0, player.y))

        # Finally forget action
        player.action = actions.NONE

        # Fix up collisions

        if (player.x, player.y) in positions:
            print 'fix up collisions for player', player.name
            if player.y < config.matrix_height - 1:
                player.y += 1
            elif player.x > 0:
                player.x -= 1
            elif player.x < config.matrix_width - 1:
                player.x += 1

        print 'process_actions: name=%s car=%s pos=%d,%d response_time=%0.6f life=%d' % (
                player.name, player.car, player.x, player.y,
                player.response_time, player.life)
        positions.add((player.x, player.y))
