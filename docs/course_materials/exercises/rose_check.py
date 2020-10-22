#!/usr/bin/env python3

import argparse
import importlib
import logging
import os.path
from pathlib import Path
import sys
from linux_tester import LinuxTester
from python_tester import PythonTester


def load_file(file_path):
    """
    Load the file as module

    Arguments:
        file_path (str): The path to the file

    Returns:
        File as module

    Raises:
        FileNotFoundError if the file cannot be loaded
    """
    module_name = os.path.split(os.path.splitext(file_path)[0])[1]
    module_spec = importlib.util.spec_from_file_location(module_name, file_path)
    if module_spec is None:
        print('Module: {} not found'.format(module_name))
        return None
    else:
        try:
            module = importlib.util.module_from_spec(module_spec)
            module_spec.loader.exec_module(module)
            return module
        except FileNotFoundError as e:
            print("Error loading the file %r: %s" % (file_path, e.strerror))
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
parser = argparse.ArgumentParser(description="ROSE Exercise")
exercise_list = get_exe_list()
parser.add_argument("exercise_file",
                    help="The path to the check_exercise file. "
                         "The available exercises are: " + " ".join(exercise_list))
parser.add_argument("--set_home", "-s", dest="home_directory",
                        default=(str(Path.home())+"/"),
                        help="Custom definition of 'home' directory, "
                             "for example: /home/student/. "
                             "If not specified, home folder will be used.")

args = parser.parse_args()

if args.home_directory[-1] != '/':
    args.home_directory += '/'

exercise_mod = load_file(args.exercise_file)
if exercise_mod.exercise_type == "Linux":
    tester = LinuxTester(args.home_directory, exercise_mod)
elif exercise_mod.exercise_type == "Python":
    tester = PythonTester(args.home_directory, exercise_mod)
else:
    print("Invalid exercise type")

flag = tester.test()
if flag:
    print('Great work! You finished your exercise.')
else:
    print('Great effort! Try to complete the missing assignments.')
