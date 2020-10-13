import os.path
from pathlib import Path
import check_helper

home = str(Path.home())
exercise_commands = {'mkdir': 'creating directories', 'tree': 'viewing the directory tree'}
exercise_paths = [home + '/test/tmp']

def main():
    '''
    Running the tests and prompting the student according to his work.
    '''
    test_result = ''
    student_commands = check_helper.get_student_commands()
    unused_commands = check_helper.find_unused_commands(student_commands, exercise_commands)
    if len(unused_commands) > 0:
        test_result += "It seems you missed some commands. Make sure you have used the following commands:\n"
        for command in unused_commands:
            test_result += "'" + command + "' for " + exercise_commands[command] + '.\n'
    missing_paths = check_helper.created_directories(exercise_paths)
    if len(missing_paths) > 0:
        test_result += ("It seems that not all directories were created in the right place. "
                    "Make sure you create the following:\n")
        for cur_path in missing_paths:
            test_result += cur_path + "\n"
    if len(test_result) == 0:
        test_result = 'Great work! You finished your exercise.'
    print(test_result)