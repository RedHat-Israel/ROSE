""" Automatically check student's homework

The tests will check:
 1. The content of the exercise file
 2. The execution and output of the exercise file
 3. The output with different inputs

Guidelines:
- Student's exercise files should be placed in the same dir as this test.
- Test names are in the form: test_<topic>_<num of ex>.py

Usage:

    # List all tests
    pytest -o addopts="" --collect-only

    # Run all tests:
    pytest -o addopts=""

    # Test a specific topic
    pytest -o addopts="" -k test_variables
"""
from pathlib import Path
import pytest


@pytest.mark.variables
def test_variables_1(helpers, home_folder):
    answer_file = str(home_folder) + 'variables.py'
    print(answer_file)
    expected_pycode = [
        r'^.*x *= *9.*',
        r'^.*y *= *7.*',
        r'^.*z *= *x *\+ *y.*',
        r'^.*print.*z.*',
    ]
    expected_stdout = '16'

    helpers.does_student_file_exist(answer_file)

    helpers.check_answers_from_file(helpers, expected_pycode, answer_file)

    stdout = helpers.run_cmd(['python', answer_file])
    helpers.check_list_of_answers([expected_stdout], stdout.strip(),
                                  word_pattern=True)


@pytest.mark.variables
def test_variables_2(helpers):
    answer_file = 'calculations.txt'
    expected_answers = [
        # What is the result of 10 ** 3?
        '1000',
        # Given (x = 1), what will be the value of after we run (x += 2)?
        '3',
        # What is the result of float(1)?
        r'1\.0',
        # What is the result of 10 == “10”?
        'False',
        # Print the result of the following variable:
        # Number = ((((13 * 8 - 4) * 2 + 50) * 4 ) % 127 ) *5
        '555',
    ]
    helpers.check_answers_from_file(helpers, expected_answers, answer_file,
                                    word_pattern=True)


@pytest.mark.variables
def test_variables_3(helpers):
    # ??? TODO: ASK SHIRA file names
    # Accept two numbers from the user (using input) and calculate:
    # 1. multiplication (*)
    # 2. Subtract (-)
    # 3. Divide (/)
    # 4. Modulus (%)
    pass
