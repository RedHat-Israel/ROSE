"""
Helper functions for automatically checking student's exercises

The tests will check:
 1. The content of the exercise file, needs expected answers and file to test.
 2. The output of the exercise file to the cmd.
 3. If the student answer file exists.
"""
import os
import re
import pytest
from subprocess import PIPE, Popen, TimeoutExpired
import logging
from rose_check import HOME

LOGGER = logging.getLogger()
# Allow next row for debug output.
# LOGGER.setLevel('DEBUG')


@pytest.fixture
def home_folder():
    return HOME


class Test_helpers:
    def __init__(self):
        self.student_file = ''
        self.expected_pycode = True
        self.expected_stdout = True
        self.tests_list = []
        self.input = []
        self.exact_answer = False

    def test_assignment(self):
        '''
        Runs all checks on a assignment
        1. If student answer file exists
        2. If the written code corresponds to the requirements
        3. If the output corresponds to the requirements
        '''
        LOGGER.info(f'Started testing {self.student_file}:')
        self.test_file_exist()

        student_work = ''

        # Runs the code and gets stdout
        if self.expected_stdout:
            LOGGER.info('Running the code...')
            if self.input:
                for data in self.input:
                    student_work += self.run_cmd(data)
            else:
                student_work += self.run_cmd()
                LOGGER.debug(f'run CMD, {student_work}')

        # Reads code file
        if self.expected_pycode:
            student_work += self.get_student_code()

        # Tests the code
        LOGGER.info('Testing the code...')
        LOGGER.debug(student_work)
        test_code, message = self.test_answers(self.tests_list, student_work)
        LOGGER.debug(message)
        assert test_code, LOGGER.info('Good job, but needs ' +
                                      f'some improvements:\n{message[:-1]}')
        if message != '':
            LOGGER.info(f'Better code can be achieved by:\n{message}')

    def test_file_exist(self):
        '''
        Checks if the student file exists
        '''
        assert os.path.exists(self.student_file), LOGGER.warning(
                                                  'Student homework file ' +
                                                  'not found: ' +
                                                  self.student_file)

    def get_student_code(self):
        '''
        Returns the student code/text as an array by lines
        '''
        with open(self.student_file, 'r') as f:
            student_code = f.read()
        return student_code

    def run_cmd(self, data=[], **kwargs):
        '''
        Simulates a cmd action to check output
        '''
        input_data = ('\n'.join(data).encode('utf-8') if data
                      else None)

        p = Popen(['python', self.student_file], stdout=PIPE, stdin=PIPE,
                  stderr=PIPE)
        try:
            stdout, stderr = p.communicate(input=input_data, timeout=20,
                                           **kwargs)
        except TimeoutExpired:
            p.kill()
            stdout, stderr = p.communicate()
        if p.returncode != 0:
            LOGGER.error('Failed while running' +
                         f' the code. The error is:\n{stderr.decode()}')

        return stdout.decode('utf-8')

    @staticmethod
    def test_answers(expected_list, answer_list, word_pattern=False):
        '''
        Compares students answers with expected ones.
        '''
        better_code_only = True
        message = ''
        LOGGER.debug(f'expected: {expected_list}')
        for answer in expected_list:
            pattern = f'\\b{answer[0]}\\b' if word_pattern else answer[0]
            LOGGER.debug(f'pattern: {pattern}')
            answers = answer_list if word_pattern else answer_list.splitlines()
            LOGGER.debug(f'answers: {answers}')
            matched = Test_helpers.test_answer_match(pattern, answers)
            if not matched:
                if isinstance(answer[1], list):
                    test, better_message = Test_helpers.test_lesser_answers(
                                                        answer[1],
                                                        answers)
                    message += better_message
                    if not test:
                        better_code_only = False
                else:
                    message += answer[1] + '\n'
                    better_code_only = False
        return better_code_only, message

    def set_student_file(self, file):
        self.student_file = os.path.join(str(HOME), file)

    @staticmethod
    def test_answer_match(pattern, answers):
        matched = False
        for line in answers:
            LOGGER.debug(f'line: |{line}|')
            if re.search(pattern, line, re.MULTILINE):
                LOGGER.debug("MATCHED")
                matched = True
                break
        return matched

    @staticmethod
    def test_lesser_answers(expected_answer, answers):
        LOGGER.debug("Checking lesser answers")
        matched = Test_helpers.test_answer_match(expected_answer[0], answers)
        if not matched:
            return False, expected_answer[2]+'\n'
        return True, expected_answer[1]+'\n'


@pytest.fixture
def helpers():
    return Test_helpers()
