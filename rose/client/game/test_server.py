import pytest
import requests
import threading
from game.server import MyTCPServer, MyHTTPRequestHandler


def drive(world):
    return ""


# Start the server in a separate thread for testing
@pytest.fixture(scope="module")
def start_server():
    server_address = ("", 8081)
    MyHTTPRequestHandler.drive = drive
    httpd = MyTCPServer(server_address, MyHTTPRequestHandler)
    thread = threading.Thread(target=httpd.serve_forever)
    thread.start()
    yield
    httpd.shutdown()
    thread.join()


def test_get_driver_name(start_server):
    response = requests.get("http://localhost:8081/")
    data = response.json()
    assert data["info"]["name"] == "Unknown"  # Default driver name


def test_post_valid_data(start_server):
    payload = {
        "info": {"car": {"x": 3, "y": 8}},
        "track": [
            ["", "", "bike"],
            ["", "", ""],
            ["", "", ""],
            ["", "", ""],
            ["", "", ""],
            ["", "", ""],
            ["", "", ""],
            ["", "", ""],
        ],
    }
    response = requests.post("http://localhost:8081/", json=payload)
    data = response.json()
    assert "action" in data["info"]


def test_post_invalid_json(start_server):
    response = requests.post("http://localhost:8081/", data="not a valid json")
    assert response.status_code == 400


def test_post_unexpected_data_structure(start_server):
    payload = {"unexpected": "data"}
    response = requests.post("http://localhost:8081/", json=payload)
    assert response.status_code == 500
