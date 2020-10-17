#!/usr/bin/env python3

import argparse
import importlib
from importlib.abc import Finder 
import logging
import os.path
from pathlib import Path
import sys
import check_helper

 
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
            
            
'''
Calling the corresponding check_exercise file.
'''
logging.basicConfig(level=logging.INFO)
parser = argparse.ArgumentParser(description="ROSE Exercise")
parser.add_argument("exercise_file",
                    help="The path to the check_exercise file. "
                         "For example: '01_Linux/check_class_exercise_1.py'")
parser.add_argument("--set_home", "-s", dest="home_directory",
                        default=str(Path.home()),
                        help="Custom definition of 'home' directory."
                             "If not specified, home folder will be used.")

args = parser.parse_args()
'''
If a custom folder is entered, will update the HOME value.
'''
if args.home_directory != str(Path.home()):
    check_helper.HOME = args.home_directory

cur_dir = os.path.dirname(os.path.abspath(__file__))
helper = load_file(cur_dir + '/check_helper.py')
exercise_mod = load_file(args.exercise_file)

exercise_mod.main()