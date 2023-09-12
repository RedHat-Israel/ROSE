import json
import os

import aiohttp
import websockets
from aiohttp import web

from common import config
from game import logic

# Global active_websockets
# IMPORTANT - shared with game loop in game.py
active_websockets = set()

# Global state
# IMPORTANT - shared with game loop in game.py
state = {"rate": None, "running": None, "reset": None, "drivers": [], "timeleft": None}


async def admin_handler(request):
    """
    Handle admin requests to set the game rate.

    Args:
        request (aiohttp.web.Request): The request object.

    Returns:
        aiohttp.web.Response: A response indicating the new game rate or an error message.
    """
    global state

    rate = request.rel_url.query.get("rate")
    if rate:
        try:
            state["rate"] = float(rate)
        except ValueError:
            return web.Response(text="Invalid rate provided", status=400)

    running = request.rel_url.query.get("running")
    if running:
        try:
            state["running"] = int(running)
        except ValueError:
            return web.Response(text="Invalid running provided", status=400)

    reset = request.rel_url.query.get("reset")
    if reset:
        try:
            state["reset"] = int(reset)
        except ValueError:
            return web.Response(text="Invalid reset provided", status=400)

    # This expects the drivers to be passed as a comma-separated list in the query param
    # e.g., ?drivers=http://localhost:8081/drv2,http://driver.com:8090/
    drivers = request.rel_url.query.get("drivers")
    if drivers:
        drivers_list = drivers.split(",")
        state["drivers"] = drivers_list
        state["running"] = 0
        state["reset"] = 1

    return web.Response(text=json.dumps(state))


async def websocket_handler(websocket, path):
    """
    Handle websocket connections, sending a greeting to the client.

    Args:
        websocket (websockets.WebSocketServerProtocol): The websocket protocol instance.
        path (str): The path the client connected to.
    """
    active_websockets.add(websocket)
    try:
        async for message in websocket:
            # Handle or respond to the message if necessary
            await websocket.send(f"Received: {message}")
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        active_websockets.remove(websocket)


async def run(
    http_port,
    ws_port,
    listen_address,
    initial_rate,
    initial_running,
    initial_drivers,
    public,
    theme,
    track_type,
):
    """
    Start the servers (HTTP and Websocket) and the game loop.

    Args:
        http_port (int): The port to listen on for the HTTP server.
        ws_port (int): The port to listen on for the Websocket server.
        listen_address (str): The address for both servers to bind to.
        initial_rate (float): The initial game rate in seconds.
        running (bollean): The initial starting state of the game.
        drivers (list of strings): list of driver URLs to use.
        public (str): Path to the static files directory.
        theme (str): Path to the static them resources directory.
        track_type (str): Type of track can be "random" or "same".
    """
    global state

    state["rate"] = initial_rate
    state["running"] = 1 if initial_running else 0
    state["drivers"] = initial_drivers
    state["timeleft"] = config.game_duration
    state["track_type"] = track_type

    app = web.Application()

    # Add static files server using the 'public' arg
    async def index_handler(request):
        return web.FileResponse(os.path.join(public, "index.html"))

    app.router.add_get("/", index_handler)
    app.router.add_post("/admin", admin_handler)

    app.router.add_static("/res/", path=theme, name="theme")
    app.router.add_static("/", path=public, name="static")

    runner = aiohttp.web.AppRunner(app)
    await runner.setup()
    site = aiohttp.web.TCPSite(runner, listen_address, http_port)

    # Start HTTP server
    await site.start()

    # Start websocket server
    await websockets.serve(websocket_handler, listen_address, ws_port)

    print(f"Theme         {theme}")
    print(f"Track         {track_type}")
    print(f"Drivers       {initial_drivers}")
    print(f"Listen        {listen_address}:{http_port}")
    print(f"Server URL    http://127.0.0.1:{http_port}")

    # Start game loop
    # IMPORTANT: state and active_websockets are references, changes in this file will affect the game loop.
    await logic.game_loop(state, active_websockets)
