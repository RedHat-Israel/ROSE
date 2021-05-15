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
    helpers.set_student_file('variables_1.py')
    helpers.tests_list = [
        [r'^.*x *= *(int\()?\s?9\s?(\))?$', 'x should equal 9'],
        [r'^.*y *= *(int\()?\s?7\s?(\))?$', 'y should equal 7'],
        [r'^.*z *= *(int\()?\s?x\s?(\))? *\+ *(int\()?\s?y\s?(\))?$',
         'z should equal the sum of x and y'],
        [r'^.*print\(.*z.*\).*', 'print message is missing'],
        [r'.*16', 'The expected output is 16']
    ]

    helpers.test_assignment()


@pytest.mark.variables
def test_variables_2(helpers):
    helpers.set_student_file('variables_2.py')
    helpers.input = [['10', '3']]
    error_message = f'For input: {helpers.input[0]}, '
    helpers.tests_list = [
        [r'^.*\*.*', 'The arithmetic operator * is missing'],
        [r'^.*-.*', 'The arithmetic operator - is missing'],
        [r'^.*/.*', 'The arithmetic operator / is missing'],
        [r'^.*%.*', f'The arithmetic operator {"%"} is missing'],
        [r'\D*30\D*',
         error_message + f'the expected multiplication answer is {30}'],
        [r'\D*7\D*',
         error_message + f'the expected subtraction answer is {7}'],
        [r'\D*' + str(10/3) + r'\D*',
         error_message + f'the expected devision answer is {10/3}'],
        [r'\D*1\D*',
         error_message + f'the expected modulo answer is {1}'],
    ]

    helpers.test_assignment()


@pytest.mark.variables
def test_calculations(helpers):
    helpers.set_student_file('calculations.txt')
    helpers.expected_stdout = False
    helpers.tests_list = [
        # What is the result of 10 ** 3?
        [r'\b1000\b', 'For 10 ** 3 the expected result is 1000'],
        # Given (x = 1), what will be the value of after we run (x += 2)?
        [r'\b3\b', 'for x=1; x+=2 the expected result is 3'],
        # What is the result of float(1)?
        [r'\b1\.0\b', 'For float(1) the expected result is 1.0'],
        # What is the result of 10 == “10”?
        ['False', 'For 10 == "10" the expected result is False'],
        # Print the result of the following variable:
        # Number = ((((13 * 8 - 4) * 2 + 50) * 4 ) % 127 ) *5
        [r'\b555\b', 'For Number = ((((13 * 8 - 4) * 2 + 50) * 4 ) % 127 )' +
                     '*5\nthe expected result is 555'],
    ]

    helpers.test_assignment()
