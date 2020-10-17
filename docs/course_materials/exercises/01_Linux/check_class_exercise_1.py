from pathlib import Path
import check_helper

exercise_commands = ['mkdir', 'tree']
exercise_paths = ['/test', '/test/tmp']

def main():
    '''
    Running the tests and prompting the student according to his work.
    '''
    check_helper.test_exercise(exercise_commands, exercise_paths)