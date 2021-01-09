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
import pytest


@pytest.mark.variables
def test_variables_1(helpers):
    helpers.student_file = helpers.home_dir + 'variables_1.py'
    helpers.expected_pycode = [
        r'^.*x *= *9.*',
        r'^.*y *= *7.*',
        r'^.*z *= *x *\+ *y.*',
        r'^.*print\(.*z.*\).*',
    ]
    helpers.expected_stdout = [r'.*16']

    helpers.test_assignment()


@pytest.mark.variables
def test_variables_2(helpers):
    helpers.student_file = helpers.home_dir + 'variables_2.py'
    helpers.expected_pycode = [
        r'^.*\*.*',
        r'^.*-.*',
        r'^.*/.*',
        r'^.*%.*',
    ]
    helpers.input = [['10', '3'], ['5', '6']]
    helpers.expected_stdout = [[r'.*30', r'.*7', r'.*' + str(10/3), r'.*1'],
                               [r'.*30', r'.*-1', r'.*' + str(5/6), r'.*5']]

    helpers.test_assignment()


@pytest.mark.variables
def test_calculations(helpers):
    helpers.student_file = helpers.home_dir + 'calculations.txt'
    helpers.expected_pycode = [
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

    helpers.test_assignment()
