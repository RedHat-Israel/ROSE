import os

# Networking

game_port = 8888
web_port = 8880

# Server

game_rate = 1.0
game_duration = 60

# Client

frame_rate = 30
number_of_cars = 4
car_jitter = 10

# Matrix

matrix_height = 9
matrix_width = 6
row_height = 65
cell_width = 130
left_margin = 95
top_margin = 10
dashboard_height = 150

# Window

background_color = 0, 0, 0
window_caption = "ROSE Project"
windows_width = cell_width*(matrix_width+1)
windows_height = (row_height * matrix_height)+dashboard_height
window_size = windows_width, windows_height

player_name_and_score_pos = 35
player_score_pos = 70

# Files

install_dir = os.path.dirname(__file__)
obstacles_glob = os.path.join(install_dir, '../res/obstacles/obstacle*.png')
road_glob = os.path.join(install_dir, '../res/bg/bg*.png')
cars_dir = os.path.join(install_dir, '../res/cars')
dashboard_png = os.path.join(install_dir, '../res/dashboard/dashboard.png')
splash_png = os.path.join(install_dir, '../res/splash/splash_screen.png')
end_line_png = os.path.join(install_dir, '../res/end/final_flag.png')

# Player

max_players = 2
