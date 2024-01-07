import asyncio
import aiohttp
import json
import time
import logging


log = logging.getLogger("net")


async def fetch_drivers_actions(players, track_matrix):
    """
    Asynchronously fetch actions for each player.

    Args:
        players (list): List of Player objects.
        track_matrix (list of list): The matrix representation a 2D array of the track.

    Returns:
        list: List of player actions fetched.
    """
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(
            *(fetch_driver_action(session, player, track_matrix) for player in players),
            return_exceptions=True,
        )


async def fetch_driver_action(session, player, track_matrix):
    """
    Asynchronously fetch content from a URL using a POST request and return the parsed JSON
    along with the time it took to get the response.

    Args:
        session (aiohttp.ClientSession): An active ClientSession for making the request.
        player (Player): The player object containing name, URL, and position.
        track_matrix (list of list): The matrix representation a 2D array of the track.

    Returns:
        tuple: A tuple containing:
            - dict or None: The JSON-decoded response from the server or None if an error occurred.
            - float: The time taken (in seconds) to get the response.
            - str or None: The error message, if any. None if no error occurred.
    """
    start_time = time.time()

    try:
        response_data = await send_post_request(session, player, track_matrix)
        return process_driver_response(player, response_data, start_time)

    except Exception as e:
        elapsed_time = time.time() - start_time
        player.response_time = elapsed_time
        error_msg = f"Error during POST request {e}"
        log.error(error_msg)

        player.action = None
        player.httperror = "Error POST to driver"

        return None, elapsed_time


async def send_post_request(session, player, track_matrix):
    data = {"info": {"car": {"x": player.x, "y": player.y}}, "track": track_matrix}

    async with session.post(player.URL, data=json.dumps(data).encode()) as response:
        return await response.json()


def process_driver_response(player, response_data, start_time):
    elapsed_time = time.time() - start_time
    player.response_time = elapsed_time

    try:
        player.name = response_data.get("info").get("name")
        player.action = response_data.get("info").get("action")
        player.httperror = None
        return response_data, elapsed_time

    except Exception as e:
        error_msg = f"Post to driver error {e}"
        log.error(error_msg)

        player.action = None
        player.httperror = error_msg

        return None, elapsed_time


async def update_websockets(started, state, players, track, active_websockets):
    """Generate game state data and send it to all active websockets."""
    data = {
        "action": "update",
        "payload": {
            "started": started,
            "rate": state["rate"],
            "timeleft": state["timeleft"],
            "players": [player.state() for player in players],
            "track": track.state(),
        },
    }

    await send_to_all_websockets(data, active_websockets)


async def send_to_all_websockets(data, active_websockets):
    """Send the given data to all active websocket connections."""
    json_encoded_data = json.dumps(data)
    for ws in active_websockets:
        try:
            await ws.send_str(json_encoded_data)
        except Exception as e:
            log.error("Fail ws send", e)
