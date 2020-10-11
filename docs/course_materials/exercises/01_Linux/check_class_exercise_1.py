import argparse
import os.path
from os import path
from pathlib import Path

home = str(Path.home())
exercise_commands = ['mkdir test', 'mkdir tmp', 'tree']

def get_student_commands():
    '''
    Checks stutent history file for key commands.
    If the history is longer than 20 commands, checks only 20 last commands.
    '''
    my_commands = []
    hist_path = home + '/.bash_history'
    with open(hist_path, 'r') as rf:
        for line in rf:
            my_commands.append(line[:-1])
    if len(my_commands) > 100:
        my_commands = my_commands[-100:]
    return my_commands

def used_right_commands(my_commands):
    '''
    Checks if the student used the correct commands. 
    '''
    for command in exercise_commands:
        if command not in my_commands:
            return False
    return True

def created_directories():
    return path.exists(home + '/test/tmp')

def main():
    '''
    Running the tests and prompting the student according to his work.
    '''
    test_result = ''
    student_commands = get_student_commands()
    if not used_right_commands(student_commands):
        test_result += '''It seems you missed some commands.
    Make sure you have used 'mkdir' for creating the directories
    and 'tree' for viewing the directory tree.\n'''
    if not created_directories():
        test_result += '''It seems that not all directories were created in the right place.
    Make sure you create a 'test' directory in 'home'
    and a 'tst' directory in 'test'.'''
    if len(test_result) == 0:
        test_result = 'Great work! You finished your exercise.'
    print(test_result)