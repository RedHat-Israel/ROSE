#!/usr/bin/env python3

import argparse
import importlib
from importlib.abc import Finder 
import logging
import os.path
import sys

 
def load_check_file(file_path):
    """
    Load the check file as module

    Arguments:
      file_path (str): The path to the check file

    Returns:
        Check file module

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
            print("Error loading check exercise file %r: %s" % (file_path, e.strerror))
            sys.exit(2)
            
            
'''
Calling the corresponding check_exercise file.
'''
logging.basicConfig(level=logging.INFO)
parser = argparse.ArgumentParser(description="ROSE Exercise")
parser.add_argument("exercise_file",
                    help="The path to the check_exercise file."
                         " For example: '01_Linux/check_class_exercise_1.py'")

args = parser.parse_args()

exercise_mod = load_check_file(args.exercise_file)

exercise_mod.main()