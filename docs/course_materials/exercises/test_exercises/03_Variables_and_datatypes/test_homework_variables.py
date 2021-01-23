"""
Automatically check student's homework
----------------------------------------
The tests will check:
 1. The content of the exercise file
 2. The execution and output of the exercise file
 3. The output with different inputs

Guidelines:
- You have to specify the dir Student's exercise files should be placed
in the same dir as this test.
- Test names are in the form: test_<exercise>.py
- Before each test should be the appropriate fixture: @pytest.mark.<topic>
"""
import pytest


@pytest.mark.variables
def test_variables_1(helpers):
    helpers.student_file = helpers.home_dir + 'variables_1.py'
    helpers.expected_pycode = [
        [r'^.*x *= *9.*', 'x variable is not defined'],
        [r'^.*y *= *7.*', 'y variable is not defined'],
        [r'^.*z *= *x *\+ *y.*', 'z variable is not defined'],
        [r'^.*print\(.*z.*\).*', 'print message is missing'],
    ]
    helpers.expected_stdout = [[r'.*16', 'The expected output is 16']]

    helpers.test_assignment()


@pytest.mark.variables
def test_variables_2(helpers):
    helpers.student_file = helpers.home_dir + 'variables_2.py'
    helpers.expected_pycode = [
        [r'^.*\*.*', '* sign is missing'],
        [r'^.*-.*', '- sign is missing'],
        [r'^.*/.*', '/ sign is missing'],
        [r'^.*%.*', '%' + 'sign is missing'],
    ]
    helpers.exact_answer = True
    helpers.input = [['10', '3'], ['5', '6']]
    helpers.expected_stdout = [[r'.*30\s*.*7\s*.*' + str(10/3) +
                                r'\s*.*1\s*.*',
                               f'For input: {helpers.input[0]}, ' +
                                f'expected output is: {30}, {7}, {10/3}, {1}'],
                               [r'.*30\s*.*-1\s*.*' + str(5/6) +
                                r'\s*.*5',
                               f'For input: {helpers.input[1]}, ' +
                                f'expected output is: {30}, {-1}, {5/6}, {5}']]

    helpers.test_assignment()


@pytest.mark.variables
def test_calculations(helpers):
    helpers.student_file = helpers.home_dir + 'calculations.txt'
    helpers.expected_pycode = [
        # What is the result of 10 ** 3?
        ['1000', 'For 10 ** 3 the expected result is 1000'],
        # Given (x = 1), what will be the value of after we run (x += 2)?
        ['3', 'for x=1; x+=2 the expected result is 3'],
        # What is the result of float(1)?
        [r'1\.0', 'For float(1) the expected result is 1.0'],
        # What is the result of 10 == “10”?
        ['False', 'For 10 == "10" the expected result is False'],
        # Print the result of the following variable:
        # Number = ((((13 * 8 - 4) * 2 + 50) * 4 ) % 127 ) *5
        ['555', 'For Number = ((((13 * 8 - 4) * 2 + 50) * 4 ) % 127 ) *5 \n' +
                'the expected result is 555'],
    ]

    helpers.test_assignment()
