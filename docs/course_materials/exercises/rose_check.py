#!/usr/bin/env python3

import argparse
import importlib
import logging
import os.path
from pathlib import Path
import sys
import linux_tester


def load_file(file_path):
    '''
    Load the file as module

    Arguments:
        file_path (str): The path to the file

    Returns:
        File as module

    Raises:
        FileNotFoundError if the file cannot be loaded
    '''
    module_name = os.path.split(os.path.splitext(file_path)[0])[1]
    module_spec = importlib.util.spec_from_file_location(module_name,
                                                         file_path)
    if module_spec is None:
        print(f'Module: {module_name} not found')
        return None
    else:
        try:
            module = importlib.util.module_from_spec(module_spec)
            module_spec.loader.exec_module(module)
            return module
        except FileNotFoundError as e:
            print(f'Error loading the file {file_path}: {e.strerror}')
            sys.exit(2)


def get_exe_list():
    exercise_list = []
    for currentpath, folders, files in os.walk('.'):
        for file in files:
            if 'check_' in file and '.pyc' not in file:
                exercise_list.append(os.path.join(currentpath, file))
    return exercise_list


'''
Calling the corresponding check_exercise file.
'''
logging.basicConfig(level=logging.INFO)
parser = argparse.ArgumentParser(description='ROSE Exercise')
exercise_list = get_exe_list()
parser.add_argument('exercise_file',
                    help='The path to the check_exercise file. '
                         'The available exercises are: ' +
                         ', '.join(exercise_list))
parser.add_argument('--set_home', '-s', dest='home_directory',
                    default=(str(Path.home())+'/'),
                    help='Custom definition of HOME directory, '
                         'for example: /home/student/. '
                         'If not specified, '
                         'standard HOME folder will be used.')

args = parser.parse_args()

if args.home_directory[-1] != '/':
    args.home_directory += '/'

linux_tester.HOME = args.home_directory

if ('./' + args.exercise_file) in exercise_list:
    exercise_mod = load_file(args.exercise_file)
    linux_tester.COMMANDS = exercise_mod.exercise_commands
    linux_tester.PATHS = exercise_mod.exercise_paths
    linux_tester.DELETED_PATHS = exercise_mod.exercise_deleted_paths
    finished = linux_tester.is_exercise_done()
    if finished:
        print('Great work! You finished your exercise.')
    else:
        print('Great effort! Try to complete the missing assignments.')
else:
    print('Invalid exercise file')
