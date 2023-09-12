from game.car import Car
from game.track import Track


def create(game_data):
    """
    Creates a world object based on the provided game data.

    World allows read-only access to game data.

    Arguments:
      game_data: A dictionary containing information about the car and track.

    Returns:
      An instance of the World class.
    """

    # Extract car and track details from game data
    car_data = game_data.get("info", {}).get("car", {})
    track_data = game_data.get("track", [])

    # Instantiate Car and Track objects
    car = Car(car_data)
    track = Track(track_data)

    class World(object):
        @property
        def car(self):
            """Return my car"""
            return car

        def get(self, pos):
            """
            Return the obsticale at position pos

            Arguments:
              pos: 2-tuple (x, y) using game logical units

            Accessing a position out of the world bounds will raise IndexError
            exception.
            """
            return track.get(pos[0], pos[1])

    return World()
