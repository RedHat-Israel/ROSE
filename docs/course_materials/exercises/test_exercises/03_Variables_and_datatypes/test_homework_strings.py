"""
Automatically check student's homework
----------------------------------------
The tests will check:
 1. The content of the exercise file
 2. The execution and output of the exercise file
 3. The output with different inputs

Guidelines:
- Student's work should be placed at the HOME directory.
If another directory was chosen use the appropriate command
when running the test.
- Test names are in the form: test_<exercise>.py
- Before each test should be the appropriate fixture: @pytest.mark.<topic>
"""
import pytest


@pytest.mark.strings
def test_names(helpers):
    helpers.set_student_file('names.py')
    helpers.expected_stdout = False
    helpers.tests_list = [
        # Create a string variable with your name, call it my_name
        [r'''\bmy_name\s*=\s*['"]\w+(\s\w+)*["']''',
         'check my_name variable definition'],
        # Create a string variable with your family name,
        # call it my_family_name
        [r'''\bmy_family_name\s*=\s*['"]\w+(\s\w+)*["']''',
         'check my_family_name variable definition'],
        # Create a string variable called my_full_name which is composed from
        # the 2 variables my_name and my_family_name.
        [r'''\bmy_full_name\s*=.*\bmy_name\b.*\bmy_family_name\b''',
         'expected my_full_name to be defined by the previous variables'],
        # Create a variable with your city name: call it my_city_name
        [r'''\bmy_city_name\s*=\s*['"]\w+(\s\w+)*['"]''',
         'check my_city_name variable definition'],
        # Create a variable msg with "My name is X and I’m from Y" using
        # the variables you created above
        [r'''\bmy_message\s*=.*my_(full_)?name.*my_city_name.*''',
         'check my_message variable definition'],
        [r'''.*f["']My name is \{my_(full_)?name''' +
         r'''\} and I'm from \{my_city_name\}''',
         [r'''(.*['"]My name is\s*['"]\s*[+]\s*my_(full_)?name''' +
          r'''\s*[+]\s*['"]\s*and I'm from\s*['"]\s*[+]\s*''' +
          r'''my_city_name)|(.*['"]My name is \%s and I'm from \%s''' +
          r'''['"]\s*\%\s*\(my_(full_)?name,\s*my_city_name\))''',
          'a better definition for my_message should use f"string"',
          'expected the use of f"string" for my_message variable, ' +
          'make sure to include the previous variables']]
    ]

    helpers.test_assignment()


@pytest.mark.strings
def test_times(helpers):
    helpers.set_student_file('times.py')
    helpers.expected_pycode = False
    expected_msg = ('You have to spend {} minutes this week to ' +
                    'complete ROSE homework')
    helpers.input = [['2', '3'], ['11', '6'], ['10', '2']]
    helpers.tests_list = [
        [expected_msg.format(6),
         f'for input: {helpers.input[0]} expected output: 6'],
        [expected_msg.format(66),
         f'for input: {helpers.input[1]} expected output: 66'],
        [expected_msg.format(20),
         f'for input: {helpers.input[2]} expected output: 20'],
    ]

    helpers.test_assignment()


@pytest.mark.strings
def test_letter(helpers):
    helpers.set_student_file('letter.py')
    helpers.input = [
        ['3.3.20', 'Anna', 'Rasbery, US', 'Hotel california, US'],
    ]

    helpers.tests_list = [
        [r'''\bprint\(f['|"]\{.*[date].*\}\\n\\tFor\\n\\t\{.*[name].*\}.*''',
         [r'.*\\n.*\\t.*',
          'For best solution, make sure to enter all the text',
          'make sure to use \\t, \\n and f\' in your print statement.']],
    ]

    helpers.test_assignment()


@pytest.mark.strings
def test_manipulations(helpers):
    helpers.set_student_file('manipulations.py')
    helpers.expected_stdout = False
    helpers.tests_list = [
        # declare the variable s: "...very long line..."
        [r'''\b[s]\s*=\s*[\'\'\'].*''',
         'missing \'\'\''],
        [r'''.*[\'\'\']''',
         'expected several lines that end with \'\'\'']
    ]

    helpers.test_assignment()
