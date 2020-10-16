from pathlib import Path
import check_helper

exercise_commands = {
    'pwd': 'printing current directory name',
    'mkdir': 'creating directories',
    'cd': 'changing between directories',
    'ls': 'listing directory contents',
    'tree': 'viewing the directory tree',
    'rm': 'removing a file or directory',
    'touch': 'creating new files',
    'cat': 'printing the contents of a file',
    'vim': 'for editing a file',
    'website.txt': 'writing your favorite song (partial command)', 
    'docs': 'a folder in hw1 (partial command)'
    } 

exercise_paths = [check_helper.HOME + '/hw1',
                check_helper.HOME + '/hw1/web',
                check_helper.HOME + '/hw1/other',
                ]

exercise_deleted_paths = [check_helper.HOME + '/hw1/docs',
                        check_helper.HOME + '/hw1/web/website.txt',
                        ]

def main():
    '''
    Running the tests and prompting the student according to his work.
    '''
    check_helper.test_exercise(exercise_commands, exercise_paths, exercise_deleted_paths)