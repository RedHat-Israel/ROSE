from pathlib import Path
import check_helper

exercise_commands = {
    'cp': 'coping a file to a new file',
    'mv': 'moving directories or files',
    'head': 'printing the first part of files',
    'tail': 'printing the last part of files',
    'diff': 'compare files line by line',
    'clear': 'clearing the screen',
    'man': 'opening manual',
    'mkdir folder1 folder2 folder3': 'creating multiple folders',
    'welcome.txt ~/hw1/other': 'moving welcome file (partial command)', 
    'welcome.txt ~/hw1/docs/backup.txt': 'copying welcome file to backup.txt (partial command)'
    } 

exercise_paths = [check_helper.HOME + '/hw1/other/folder1',
                check_helper.HOME + '/hw1/other/folder2',
                check_helper.HOME + '/hw1/other/folder3',
                check_helper.HOME + '/hw1/other/welcome.txt',
                check_helper.HOME + '/hw1/docs/backup.txt'
                ]

exercise_deleted_paths = [
                        ]

def main():
    '''
    Running the tests and prompting the student according to his work.
    '''
    check_helper.test_exercise(exercise_commands, exercise_paths, exercise_deleted_paths)