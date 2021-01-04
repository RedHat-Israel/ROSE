""" Helper functions for automatically checking student's exercises

The tests will check:
 1. The content of the exercise file, needs expected answers and file to test.
 2. The output of the exercise file to the cmd.
 3. If the student answer file exists.


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
import pytest
from subprocess import PIPE, STDOUT, Popen, TimeoutExpired
from rose_check import HOME


@pytest.fixture
def home_folder():
    return HOME


class Helpers:
    @staticmethod
    def run_cmd(cmd_list, input_list=[], **kwargs):
        '''
        Simulates a cmd action to check output
        '''
        input_data = ('\n'.join(input_list).encode('utf-8') if input_list
                      else None)

        p = Popen(cmd_list, stdout=PIPE, stdin=PIPE, stderr=STDOUT)
        try:
            stdout, stderr = p.communicate(input=input_data, timeout=20, 
                                           **kwargs)
        except TimeoutExpired:
            p.kill()
            stdout, stderr = p.communicate()
        assert p.returncode == 0

        return stdout.decode('utf-8')

    def check_answers_from_file(self, expected_answers_list, answer_file,
                                word_pattern=False):
        '''
        1. Reads a list of answers from a student file
        2. Calls the check function
        '''
        with open(answer_file, 'r') as f:
            text = f.read()
        self.check_list_of_answers(expected_answers_list, text, word_pattern)

    @staticmethod
    def check_list_of_answers(expected_answers_list, text, word_pattern=False):
        '''
        Compares students answers with expected ones.
        '''
        for line in text.splitlines():
            # print(f'line: |{line}|')
            for answer in expected_answers_list.copy():
                pattern = f'\\b{answer}\\b' if word_pattern else answer
                # print(f'pattern: {pattern}')
                if re.match(pattern, line):
                    # print("MATCHED")
                    expected_answers_list.remove(answer)

        assert len(expected_answers_list) == 0, ("Some expected answers were "
                                                 + "not found.")

    @staticmethod
    def does_student_file_exist(filename):
        '''
        Checks if the student file exists
        '''
        assert os.path.exists(filename), ('Student homework file not ' +
                                          f'found: {filename}')


@pytest.fixture
def helpers():
    return Helpers
