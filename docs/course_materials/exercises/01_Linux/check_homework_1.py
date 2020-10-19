from pathlib import Path
import check_helper

exercise_commands = ['pwd', 'mkdir', 'cd', 'ls', 'tree', 'rm', 'touch', 'cat', 'vim', 'website.txt', 'docs'] 

exercise_paths = ['hw1',
                'hw1/web',
                'hw1/other',
                ]

exercise_deleted_paths = ['hw1/docs',
                        'hw1/web/website.txt',
                        ]

def main():
    '''
    Running the tests and prompting the student according to his work.
    '''
    check_helper.test_exercise(exercise_commands, exercise_paths, exercise_deleted_paths)