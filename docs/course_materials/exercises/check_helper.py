import os.path
from pathlib import Path

home = str(Path.home())

def get_student_commands():
    '''
    Checks stutent history file for key commands.
    If the history is longer than 1000 commands, checks only 1000 last commands.
    '''
    my_commands = []
    hist_path = home + '/.bash_history'
    with open(hist_path, 'r') as rf:
        for line in rf:
            my_commands.append(line[:-1])
    if len(my_commands) > 1000:
        my_commands = my_commands[-1000:]
    return my_commands

def find_unused_commands(my_commands, exercise_commands):
    '''
    Checks if the student used the correct commands. 
    ''' 
    unused_commands = []
    for command in exercise_commands.keys():
        if not any(command in performed_command for performed_command in my_commands):
            unused_commands.append(command)
    return unused_commands

def created_directories(exercise_paths):
    missing_paths = []
    for cur_path in exercise_paths:
        if not os.path.exists(cur_path):
            missing_paths.append(cur_path)
    return missing_paths