""" Automatically check student's homework

The tests will check:
 1. The content of the exercise file
 2. The execution and output of the exercise file
 3. The output with different inputs

Guidelines:
- Student's exercise files should be placed in the same dir as this test.
- Test names are in the form: test_<topic>_<num>.py

Usage:

    # List all tests
    pytest -o addopts="" --collect-only

    # Run all tests:
    pytest -o addopts=""

    # Test a specific topic
    pytest -o addopts="" -k test_variables
"""
import os
import re
from subprocess import PIPE, STDOUT, Popen, TimeoutExpired


def test_strings_names():
    student_file = 'Names.py'
    answers = [
        # Create a string variable with your name, call it my_name
        r'''\bmy_name\s*=\s*['"]\w+["']''',
        # Create a string variable with your family name, call it my_family_name
        r'''\bmy_family_name\s*=\s*['"]\w+["']''',
        # Create a string variable called my_full_name which is composed from the 2 variables my_name and my_family_name.
        r'''\bmy_full_name\s*=.*\bmy_name\b.*\bmy_family_name\b''',
        # Create a variable with your city name: call it my_city_name
        r'''\bmy_city_name\s*=\s*['"]\w+['"]''',
        # Create a variable msg with "My name is X and I’m from Y" using the variables you created above
        r'''\bmsg\s*=.*My name is .* and I'm from .*''',
        r'''\bmsg\s*=.*\bmy_(full_)?name\b.*\bmy_city_name\b'''
    ]
    check_list_of_answers_from_file(answers, student_file)


def test_strings_times():
    student_file = 'Times.py'
    expected_msg = 'You have to spend {} minutes this week to complete ROSE homework'

    does_student_file_exist(student_file)
    for inputs, expected_output in [
        [['2', '3'], expected_msg.format(6)],
        [['11', '6'], expected_msg.format(66)],
        [['10', '2'], expected_msg.format(20)],
    ]:
        assert run_cmd(['python3', student_file], input_list=inputs) == expected_output


def run_cmd(cmd_list, input_list=[], **kwargs):
    input_data = '\n'.join(input_list).encode('utf-8') if input_list else None

    p = Popen(cmd_list, stdout=PIPE, stdin=PIPE, stderr=STDOUT)
    try:
        stdout, stderr = p.communicate(input=input_data, timeout=20, **kwargs)
    except TimeoutExpired:
        p.kill()
        stdout, stderr = p.communicate()
    assert p.returncode == 0

    return stdout.decode('utf-8')


def check_list_of_answers_from_file(expected_answers_list, answer_file, word_pattern=False):
    with open(answer_file, 'r') as f:
        text = f.read()
    check_list_of_answers(expected_answers_list, text, word_pattern)


def check_list_of_answers(expected_answers_list, text, word_pattern=False):
    for line in text.splitlines():
        # print(f'line: |{line}|')
        for answer in expected_answers_list.copy():
            pattern = f'\\b{answer}\\b' if word_pattern else answer
            # print(f'pattern: {pattern}')
            if re.match(pattern, line):
                # print("MATCHED")
                expected_answers_list.remove(answer)

    assert len(expected_answers_list) == 0, ("Some expected answers were " +
                                             "not found.")


def does_student_file_exist(filename):
    assert os.path.exists(filename), ('Student homework file not ' +
                                      f'found: {filename}')
