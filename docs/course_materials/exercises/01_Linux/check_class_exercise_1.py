from pathlib import Path
import check_helper

exercise_commands = {'mkdir': 'creating directories', 'tree': 'viewing the directory tree'}
exercise_paths = [check_helper.HOME + '/test', check_helper.HOME + '/test/tmp']

def main():
    '''
    Running the tests and prompting the student according to his work.
    '''
    check_helper.test_exercise(exercise_commands, exercise_paths)