import asyncio
import logging
import random
import aiohttp

from common import config

from game import score, net
from game.player import Player
from game.track import Track

log = logging.getLogger("logic")


async def initialize_game(state):
    """Reset game settings and return re-initialized track and players."""
    state["reset"] = None
    state["running"] = 0
    state["timeleft"] = config.game_duration
    track = initialize_track(state["track_type"] != "same")
    players = await initialize_players(state["drivers"])
    return track, players


def initialize_track(is_track_random):
    """
    Initialize and return a new track.

    Args:
        is_track_random (bool): If False, the track will have the same obstacles for both players.
                                If True, obstacles will be randomized.

    Returns:
        Track: An initialized track object.
    """
    track = Track(is_track_random)
    track.reset()
    return track


async def initialize_players(drivers):
    """
    Asynchronously initialize players from a list of driver URLs.

    Args:
        drivers (list): List of driver URLs to initialize players from.
        players (list): List of Player objects.
    """

    # Init players
    players = []

    if not drivers:
        return players

    base_color = random.randint(0, 3)

    async with aiohttp.ClientSession() as session:
        for index, driver in enumerate(drivers):
            try:
                async with session.get(driver) as info:
                    info_data = await info.json()
                    player_name = info_data.get("info", {}).get("name")
                    player_car = (base_color + index) % 3
                    player_lane = index
                    player = Player(player_name, player_car, player_lane)
                    player.reset()
                    player.URL = driver
                    players.append(player)
            except Exception as e:
                log.error(f"error: {e}")

    return players


async def game_loop(state, active_websockets):
    """
    Asynchronously execute the game loop, using provided state and active websockets.

    Args:
        state (dict): Dictionary containing game state data (rate, running status, time left, etc.).
        active_websockets (set): A set of active websocket connections for communication.

    Returns:
        None
    """

    # Initialize or reset the game, set up track and players
    track, players = await initialize_game(state)

    # Begin the main game loop
    while True:
        # Check if the game needs a reset (based on state)
        if state["reset"] == 1:
            track, players = await initialize_game(state)

        # Stop game if timeleft is zero
        if state["timeleft"] < 1:
            state["running"] = 0

        # Check if the game is currently running and there's time left to play
        if state["running"] == 1:
            # Start executing a step in the game
            task = asyncio.create_task(
                game_step(state, players, track, active_websockets)
            )

            # Pause the game loop for a specified duration, based on the rate defined in the state
            await asyncio.sleep(1 / state["rate"])

            # If for some reason the game step hasn't finished executing, cancel it
            if not task.done():
                task.cancel()

        # If the game is not running (e.g., paused or finished)
        else:
            # Update all connected clients (via websockets) with the current game state
            await net.update_websockets(False, state, players, track, active_websockets)

            await asyncio.sleep(1)


async def game_step(state, players, track, active_websockets):
    """
    Execute a game step: Update the track, fetch drivers' actions, process actions, and update websockets.

    Args:
        state (dict): Dictionary containing game state data (rate, running status, etc.).
        players (list): List of Player objects.
        track (Track): the game track.
        active_websockets (Any): Active websockets for communication (assuming a suitable data structure).
    """

    try:
        # Fetch players actions using an asynchronous HTTP session
        await net.fetch_drivers_actions(players, track.matrix())

        # Update track
        track.update()

        # Process the actions of the players
        score.process(players, track)

        # Send data to all WebSocket connections
        await net.update_websockets(True, state, players, track, active_websockets)

        # Progress the game's timer
        state["timeleft"] -= 1

    except asyncio.CancelledError:
        log.info("Game step was canceled!")
        raise
