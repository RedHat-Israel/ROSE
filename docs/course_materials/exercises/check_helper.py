import os
from pathlib import Path
import datetime as dt

HOME = str(Path.home()) + "/"
command_dictionary = {
    'pwd': 'printing current directory name',
    'mkdir': 'creating directories',
    'cd': 'changing between directories',
    'ls': 'listing directory contents',
    'tree': 'viewing the directory tree',
    'rm': 'removing a file or directory',
    'touch': 'creating new files',
    'cat': 'printing the contents of a file',
    'vim': 'editing a file',
    'cp': 'coping a file to a new file',
    'mv': 'moving directories or files',
    'head': 'printing the first part of files',
    'tail': 'printing the last part of files',
    'diff': 'compare files line by line',
    'clear': 'clearing the screen',
    'man': 'opening manual',
    'wc': 'counting words in file',
    'wc -l': 'counting lines in file'
    }

'''
Setting colors for the output:
green for positive feedback
red negative feedback
yellow for commands and paths
'''
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"

'''
Helper variables for check_all_paths, used to distinguish between deleted and created paths.
'''
CREATED = ["Created", ["Created", 1, GREEN], ["Missing", 0, RED], " in the right place"]
DELETED = ["Deleted", ["Was not deleted", 0, RED], ["Deleted", 1, GREEN], ""]


def print_color(feedback, color, new_line=True):
    '''
    Used to print in color with an option for new line.
    '''
    if new_line:
        p_end = '\n'
    else:
        p_end = ''
    print("{} {}\033[00m" .format(color, feedback), end=p_end) 


def get_student_commands():
    '''
    Checks stutent history file for key commands in the past 10 days.
    '''
    shell_type = os.path.basename(os.environ["SHELL"])
    # used to get the epoch for x days back
    past_date = str((dt.datetime.today() - dt.timedelta(days=10)).timestamp())
    hist_path = HOME + '/.' + shell_type + '_history'

    my_commands = []
    with open(hist_path, 'r') as rf:
        for line in rf:
            if line[2:12] >= past_date:
                my_commands.append(line[:-1])
    return my_commands


def print_command_description(command):
    if command_dictionary.get(command) is not None:
        print(" for {} ... ".format(command_dictionary[command]), end='')
    else:
        print(" checking command structure", end='')


def used_all_commands(exercise_commands):
    student_commands = get_student_commands()
    num_of_used_commands = 0
    print("Checking used commands...")
    for command in exercise_commands:
        print_color("'" + command + "'", YELLOW, 0)
        print_command_description(command)
        
        # Print feedback about the command
        if not any(command in performed_command for performed_command in student_commands):
            print_color("Missing", RED)
        else:
            print_color("Used", GREEN)
            num_of_used_commands += 1
    
    print("Got {} out of {} commands.\n".format(str(num_of_used_commands), str(len(exercise_commands))))
    if num_of_used_commands == len(exercise_commands):
        return True
    return False


def check_all_paths(paths_to_check, path_type):
    '''
    paths_to_check will get a list of exercise paths to create or delete.
    path_type will get CREATED or DELETED.
    '''
    num_of_paths = 0
    print("Checking " + path_type[0].lower() + "deleted directories or files...")
    for cur_path in paths_to_check:
        print_color("'" + HOME + cur_path + "'", YELLOW, 0)
        print(" ... ", end='')

        # Print feedback about the path
        if os.path.exists(HOME + cur_path):
            print_color(path_type[1][0], path_type[1][2])
            num_of_paths += path_type[1][1]
        else:
            print_color(path_type[2][0], path_type[2][2])
            num_of_paths += path_type[2][1]

    print("{} {} out of {} directories{}.\n".format(path_type[0],
                                                    str(num_of_paths), str(len(paths_to_check)),
                                                    path_type[3]))
    if num_of_paths == len(paths_to_check):
        return True
    return False


def test_exercise(exercise_commands, exercise_paths, exercise_deleted_paths):
    check_commands = used_all_commands(exercise_commands)
    check_paths = check_all_paths(exercise_paths, CREATED)
    
    # run the function only if the check is needed
    if len(exercise_deleted_paths) > 0: 
        check_deleted_paths = check_all_paths(exercise_deleted_paths, DELETED)
    else:
        check_deleted_paths = True
    
    if check_commands and check_paths and check_deleted_paths:
        print('Great work! You finished your exercise.')
    else:
        print('Great effort! Try to complete the missing assignments.')