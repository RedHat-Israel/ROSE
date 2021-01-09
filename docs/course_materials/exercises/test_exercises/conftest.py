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
from subprocess import PIPE, STDOUT, Popen, TimeoutExpired
from rose_check import HOME


@pytest.fixture
def home_folder():
    return HOME


class Test_helpers:
    def __init__(self):
        self.home_dir = str(HOME)
        self.student_file = ''
        self.expected_pycode = []
        self.expected_stdout = []
        self.input = []
        self.exact_answer = False

    def test_assignment(self):
        '''
        Runs all checks on a assignment
        1. If student answer file exists
        2. If the writen code corresponds to the requirments
        3. If the output corresponds to the requirments
        '''
        self.test_file_exist()

        # testing the code
        if len(self.expected_pycode) > 0:
            student_code = self.get_student_code()
            self.test_answers(self.expected_pycode, student_code,
                              message='Check your code, it\'s incomplete.')

        # Testing the output
        if len(self.expected_stdout) > 0:
            if self.input:
                for data, expected_stdout in zip(self.input,
                                                 self.expected_stdout):
                    student_stdout = self.run_cmd(data)
                    self.test_answers(expected_stdout, student_stdout.strip(),
                                      message=(f'For input: {data}, ' +
                                               'the expected output is: ' +
                                               f'{expected_stdout} but ' +
                                               f'got {student_stdout}'),
                                      word_pattern=self.exact_answer)
            else:
                student_stdout = self.run_cmd()
                self.test_answers(self.expected_stdout, student_stdout.strip(),
                                  message='Your code output not match the ' +
                                  'expected output.',
                                  word_pattern=self.exact_answer)

    def test_file_exist(self):
        '''
        Checks if the student file exists
        '''
        assert os.path.exists(self.student_file), ('Student homework file ' +
                                                   'not found: ' +
                                                   self.student_file)

    def get_student_code(self):
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
                  stderr=STDOUT)
        try:
            stdout, stderr = p.communicate(input=input_data, timeout=20,
                                           **kwargs)
        except TimeoutExpired:
            p.kill()
            stdout, stderr = p.communicate()
        assert p.returncode == 0, stderr

        return stdout.decode('utf-8')

    @staticmethod
    def test_answers(expected_list, answer_list, message, word_pattern=False):
        '''
        Compares students answers with expected ones.
        '''
        for line in answer_list.splitlines():
            # print(f'line: |{line}|')
            for answer in expected_list:
                pattern = f'\\b{answer}\\b' if word_pattern else answer
                # print(f'pattern: {pattern}')
                if re.match(pattern, line):
                    # print("MATCHED")
                    expected_list.remove(answer)

        assert len(expected_list) == 0, message


@pytest.fixture
def helpers():
    return Test_helpers()
