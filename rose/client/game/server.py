import http.server
import json
import logging
import socket
import socketserver

from game import world

log = logging.getLogger("driver")


class MyTCPServer(socketserver.TCPServer):
    # This ensures that the server will free-up the address and port when terminated
    allow_reuse_address = True

    def shutdown(self):
        # Explicitly shutting down the socket
        self.socket.shutdown(socket.SHUT_RDWR)
        socketserver.TCPServer.shutdown(self)


class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """
    Custom HTTP request handler to handle logic driver POST requests.

    This handler is designed to process incoming POST requests containing
    JSON data related to a car's metadata and game track. Based on this
    information, it determines an action for the car using the `driver`
    function from the driver logic module.

    Example:
        curl -X POST -H "Content-Type: application/json" -d '{
            "info": {
                "car": {
                    "x": 3,
                    "y": 8
                }
            },
            "track": [
                ["", "", "bike", "", "", ""],
                ["", "crack", "", "", "trash", ""],
                ["", "", "penguin", "", "", "water"],
                ["", "water", "", "trash", "", ""],
                ["barrier", "", "", "", "bike", ""],
                ["", "", "trash", "", "", ""],
                ["", "crack", "", "", "", "bike"],
                ["", "", "", "penguin", "water", ""],
                ["", "", "bike", "", "", ""]
            ]
        }' http://localhost:8081/ -s | jq
    """

    drive = None  # Set a default value for class attribute
    driver_name = "Unknown"  # Set a default value for class attribute

    def do_GET(self):
        """
        Handle a GET request.

        Response data format:
        {
            "info": { "name": <str> }
        }
        """
        response_data = {
            "info": {"name": MyHTTPRequestHandler.driver_name},
        }

        # Send response back
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(response_data).encode("utf-8"))

    def do_POST(self):
        """
        Handle a POST request.

        Expected POST data format:
        {
            "info": { "car": { "x": <int>, "y": <int> } },
            "track": <2D array>
        }

        Response data format:
        {
            "info": { "name": <str>, "action": <str> }
        }

        :raises json.JSONDecodeError: If the provided JSON data is not in the
                                      expected format.
        """

        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length).decode("utf-8")

        try:
            # Decode the JSON payload
            game_data = json.loads(post_data)

            # Extract metadata
            game_world = world.create(game_data)

            # Determine the next action using the driver's logic
            try:
                action = MyHTTPRequestHandler.drive(game_world)
            except Exception as e:
                log.error(f"Error executing drive method: {e}")

            # Construct the response data
            response_data = {
                "info": {"name": MyHTTPRequestHandler.driver_name, "action": action},
            }

            # Send response back
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode("utf-8"))

        except json.JSONDecodeError:
            self.send_response(400)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Invalid JSON payload")

        except Exception as e:
            self.send_response(500)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(str(e).encode("utf-8"))
