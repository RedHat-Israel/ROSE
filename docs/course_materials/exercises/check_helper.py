import os
from pathlib import Path
import datetime as dt

HOME = str(Path.home())

def get_student_commands():
    '''
    Checks stutent history file for key commands in the past 10 days.
    '''
    shell_type = os.path.basename(os.environ["SHELL"])
    past_date = str((dt.datetime.today() - dt.timedelta(days=10)).timestamp())  # used to get the epoch for 10 days back
    hist_path = HOME + '/.' + shell_type + '_history'

    my_commands = []
    with open(hist_path, 'r') as rf:
        for line in rf:
            if line[2:12] >= past_date:
                my_commands.append(line[:-1])
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

def test_commands(exercise_commands):
    student_commands = get_student_commands()
    unused_commands = find_unused_commands(student_commands, exercise_commands)
    test_result = ''
    if len(unused_commands) > 0:
        test_result += "It seems you missed some commands. Make sure you have used the following commands:\n"
        for command in unused_commands:
            test_result += "'" + command + "' for " + exercise_commands[command] + '.\n'
    return test_result

def test_paths(exercise_paths):
    missing_paths = created_directories(exercise_paths)
    test_result = ''
    if len(missing_paths) > 0:
        test_result += ("It seems that not all directories were created in the right place. "
                    "Make sure you create the following:\n")
        for cur_path in missing_paths:
            test_result += cur_path + "\n"
    return test_result


def test_exercise(exercise_commands, exercise_paths):
    test_result = test_commands(exercise_commands)
    test_result += test_paths(exercise_paths)
    if len(test_result) == 0:
        test_result = 'Great work! You finished your exercise.'
    print(test_result)
