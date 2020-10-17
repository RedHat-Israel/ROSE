from pathlib import Path
import check_helper

exercise_commands = ['cp', 'mv', 'head', 'tail', 'diff', 'clear', 'man',
                    'mkdir folder1 folder2 folder3', 'welcome.txt ~/hw1/other', 'welcome.txt ~/hw1/docs/backup.txt'
                    ]

exercise_paths = ['/hw1/other/folder1',
                '/hw1/other/folder2',
                '/hw1/other/folder3',
                '/hw1/other/welcome.txt',
                '/hw1/docs/backup.txt'
                ]

exercise_deleted_paths = [
                        ]

def main():
    '''
    Running the tests and prompting the student according to his work.
    '''
    check_helper.test_exercise(exercise_commands, exercise_paths, exercise_deleted_paths)