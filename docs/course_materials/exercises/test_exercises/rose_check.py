#!/usr/bin/env python3

import argparse
import importlib
import logging
import os.path
from pathlib import Path
import sys
from configparser import ConfigParser
import pytest
import linux_tester

HOME = ''


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
                exercise_list.append(os.path.join(currentpath,
                                                  file).replace('\\', '/'))
    return exercise_list


'''
Calling the corresponding check_exercise file.
'''
logging.basicConfig(level=logging.INFO)
parser = argparse.ArgumentParser(description='ROSE Exercise')
# getting exercise list fir linux exercises
exercise_list = get_exe_list()

# getting mark list for running pytest to check other exercises
config = ConfigParser()
config.read('pytest.ini')
# read values from a pytest section
markers = config.get('pytest', 'markers').split('\n')
select_markers = [x.split(':')[0] for x in markers if len(x) > 0]

parser = argparse.ArgumentParser(description='details',
                                 usage='use "%(prog)s --help" for more '
                                       'information',
                                 formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('--exercise_file', '-e', dest='exercise_file',
                    help='The path to the check_exercise file.\n'
                         'The available exercises are:\n' +
                         '--------------------------------------------------'
                         '\n'.join(exercise_list))
parser.add_argument('--set_home', '-s', dest='home_directory',
                    default=(str(Path.home())+'/'),
                    help='Custom definition of HOME directory, '
                         'for example: /home/student/.\n'
                         'If not specified, '
                         'standard HOME folder will be used.')
parser.add_argument('--test_exercise', '-t', dest='test_exercise',
                    default='', choices=select_markers,
                    help='The available exercise tests '
                         '(If not specified, the test will not execute):'
                         '\n--------------------------------------------------'
                         + '\n'.join(markers))

args = parser.parse_args()

if args.home_directory[-1] != '/':
    args.home_directory += '/'

if args.test_exercise:
    HOME = args.home_directory
    result = pytest.main(['-m ' + args.test_exercise])
    if result == 0:
        print('Great work! You finished your exercise.')
    else:
        print('Great effort! Try to correct the failed assignments.')
else:
    linux_tester.HOME = args.home_directory
    print(args.exercise_file)
    print(exercise_list)
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
