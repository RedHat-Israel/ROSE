"""
This driver does not do any action.
"""
from rtp.common import obstacles, actions

server_address = "localhost"
driver_name = "No Driver"

def drive(world):
    return actions.NONE
