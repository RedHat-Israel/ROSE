import argparse
import asyncio
import os
import logging

from game import server


def main():
    script_directory = os.path.dirname(os.path.abspath(__file__))
    default_public_path = os.path.join(script_directory, "web")
    default_theme_path = os.path.join(script_directory, "res")

    parser = argparse.ArgumentParser(description="Start the game engine.")
    parser.add_argument(
        "-p", "--port", type=int, default=8880, help="Port for HTTP server"
    )
    parser.add_argument(
        "--ws-port", type=int, default=8765, help="Port for WebSocket server"
    )
    parser.add_argument(
        "--listen", default="127.0.0.1", help="Listening address for servers"
    )
    parser.add_argument(
        "--initial-rate", type=float, default=1.0, help="Initial game rate in seconds"
    )
    parser.add_argument(
        "-d",
        "--drivers",
        nargs="+",
        help="List of driver URLs for the game engine to use",
    )
    parser.add_argument(
        "--running",
        action="store_true",
        help="Whether the game engine should start running immediately",
    )
    parser.add_argument(
        "--public",
        default=default_public_path,
        help="Path to the directory with static public files. If not provided, defaults to <current_directory>/public.",
    )
    parser.add_argument(
        "-t",
        "--track",
        choices=["same", "random"],
        default="random",
        help="Choose the track type. Can be 'same' or 'random'.",
    )
    parser.add_argument(
        "--log", default="WARNING", help="Set the logging level. E.g. --log DEBUG"
    )

    args = parser.parse_args()

    logging.basicConfig(level=getattr(logging, args.log.upper()))

    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        server.run(
            args.port,
            args.ws_port,
            args.listen,
            args.initial_rate,
            args.running,
            args.drivers,
            args.public,
            default_theme_path,
            args.track,
        )
    )


if __name__ == "__main__":
    main()
