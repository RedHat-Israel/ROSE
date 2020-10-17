import os
from pathlib import Path
import datetime as dt

HOME = str(Path.home())
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
    }

'''
Setting colors for the output:
green for positive feedback
red negative feedback
yellow for commands and paths, without new line
'''
def print_green(feedback): print("\033[92m {}\033[00m" .format(feedback)) 
def print_red(feedback): print("\033[91m {}\033[00m" .format(feedback))
def print_yellow(feedback): print("\033[93m {}\033[00m" .format(feedback), end='')

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
        print_yellow("'" + command + "'")
        print_command_description(command)
        if not any(command in performed_command for performed_command in student_commands):
            print_red("Missing")
        else:
            print_green("Used")
            num_of_used_commands += 1
    print("Got {} out of {} commands.\n".format(str(num_of_used_commands), str(len(exercise_commands))))
    if num_of_used_commands == len(exercise_commands):
        return True
    return False

def created_all_paths(exercise_paths):
    num_of_created_paths = 0
    print("Checking created directories or files...")
    for cur_path in exercise_paths:
        print_yellow("'" + HOME + cur_path + "'")
        print(" ... ", end='')
        if not os.path.exists(HOME + cur_path):
            print_red("Missing")
        else:
            print_green("Created")
            num_of_created_paths += 1
    print("Got {} out of {} directories in the right spot.\n".format(str(num_of_created_paths), str(len(exercise_paths))))
    if num_of_created_paths == len(exercise_paths):
        return True
    return False

def deleted_all_paths(exercise_deleted_paths):
    num_of_deleted_paths = 0
    print("Checking deleted directories or files...")
    for cur_path in exercise_deleted_paths:
        print_yellow("'" + HOME + cur_path + "'")
        print(" ... ", end='')
        if os.path.exists(HOME + cur_path):
            print_red("Was not deleted")
        else:
            print_green("Deleted")
            num_of_deleted_paths += 1
    print("Deleted {} out of {} directories.\n".format(str(num_of_deleted_paths), str(len(exercise_deleted_paths))))
    if num_of_deleted_paths == len(exercise_deleted_paths):
        return True
    return False

def test_exercise(exercise_commands, exercise_paths, exercise_deleted_paths):
    check_commands = used_all_commands(exercise_commands)
    check_paths = created_all_paths(exercise_paths)
    if len(exercise_deleted_paths) > 0:  # run the function only if the check is needed
        check_deleted_paths = deleted_all_paths(exercise_deleted_paths)
    else:
        check_deleted_paths = True
    if check_commands and check_paths and check_deleted_paths:
        print('Great work! You finished your exercise.')
    else:
        print('Great effort! Try to complete the missing assignments.')