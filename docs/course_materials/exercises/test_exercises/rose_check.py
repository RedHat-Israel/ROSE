#!/usr/bin/env python3

import argparse
import importlib
import logging
import os
from pathlib import Path
import sys
from configparser import ConfigParser
import pytest
import linux_tester

HOME = ""
LINUX_FOLDER = "./01_Linux/"


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
        print(f"Module: {module_name} not found")
        return None
    else:
        try:
            module = importlib.util.module_from_spec(module_spec)
            module_spec.loader.exec_module(module)
            return module
        except FileNotFoundError as e:
            print(f"Error loading the file {file_path}: {e.strerror}")
            sys.exit(2)


def get_exe_list():
    exercise_list = []
    for file in os.listdir(LINUX_FOLDER):
        if "check_" in file and ".pyc" not in file:
            exercise_list.append(file)
        exercise_list.sort()
    return exercise_list


def get_markers():
    config = ConfigParser()
    config.read("pytest.ini")
    # read values from a pytest section
    markers = config.get("pytest", "markers").split("\n")
    select_markers = [x.split(":")[0] for x in markers if len(x) > 0]
    select_markers.sort()
    return select_markers


def update_folder(folder):
    if folder == "":
        HOME = str(Path.home()) + "/"
    else:
        if folder[-1] != "/":
            folder += "/"
        HOME = folder
    return HOME


"""
Calling the corresponding test file.
"""
logging.basicConfig(level=logging.INFO)
parser = argparse.ArgumentParser(description="ROSE Exercise")
# getting exercise list fir linux exercises
exercise_list = get_exe_list()

# getting mark list for running pytest to check other exercises
select_markers = get_markers()

# Setting up the input options
parser = argparse.ArgumentParser(
    description="details",
    usage='use "%(prog)s --help" for more ' "information",
    formatter_class=argparse.RawTextHelpFormatter,
)
parser.add_argument(
    "--exercises",
    "-e",
    action="store_true",
    help="A flag for printing available exercises, "
    "stores True. If not specified, will be False.",
)
parser.add_argument(
    "--test_exercise",
    "-t",
    dest="test_exercise",
    default="",
    help="Allows to choose the exercise to be checked. "
    "(If not specified, the test will not execute)."
    "\nMake sure to use the exact exercise name.",
)
parser.add_argument(
    "--set_dir",
    "-s",
    dest="custom_dir",
    default="",
    help="Custom definition of the test directory or "
    "HOME directory in Linux, "
    "for example: /home/student/.\n"
    "You should enter the directory that contains "
    "student files to be checked. \nIf not specified, "
    "standard HOME folder will be used.",
)

args = parser.parse_args()

# Running the tests according to user input
if args.exercises:
    print(
        "Available tests for Linux are:\n\t"
        + "\n\t".join(exercise_list)
        + "\nAvailable tests for Python are:\n\t"
        + "\n\t".join(select_markers)
    )
elif args.test_exercise:
    finished = False
    HOME = update_folder(args.custom_dir)
    if ".py" in args.test_exercise:
        # Running Linux tests
        if args.test_exercise in exercise_list:
            print(os.path.join(LINUX_FOLDER, args.test_exercise))
            exercise_mod = load_file(os.path.join(LINUX_FOLDER, args.test_exercise))
            linux_tester.COMMANDS = exercise_mod.exercise_commands
            linux_tester.PATHS = exercise_mod.exercise_paths
            linux_tester.DELETED_PATHS = exercise_mod.exercise_deleted_paths
            linux_tester.HOME = HOME
            finished = linux_tester.is_exercise_done()
    else:
        # Running Python tests
        result = pytest.main(["-m " + args.test_exercise])
        finished = True if result == 0 else False
    if finished:
        print("Great work! You finished your exercise.")
    else:
        print("Great effort! Try to correct the failed assignments.")
else:
    print("Please reffer to `--help` for the available options.")
