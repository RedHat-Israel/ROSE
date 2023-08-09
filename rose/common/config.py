import os

# Networking

game_port = 8888
web_port = 8880

# Server

game_rate = 1.0
game_duration = 60
number_of_cars = 4
is_track_random = True
track_seed = ""

# Matrix

matrix_height = 9
matrix_width = 6
row_height = 65
cell_width = 130
left_margin = 95
top_margin = 10

# Files

install_dir = os.path.dirname(__file__)

# Web interface

web_root = os.path.join(install_dir, "../web")
res_root = os.path.join(install_dir, "../res")

# Player

max_players = 2
cells_per_player = matrix_width // max_players

# Score Points

score_move_forward = 10
score_move_backward = -10
score_jump = 5
score_brake = 4

# Logging

logger_format = ("%(asctime)s %(levelname)-7s [%(name)s] %(message)s "
                 "(%(module)s:%(lineno)d)")
