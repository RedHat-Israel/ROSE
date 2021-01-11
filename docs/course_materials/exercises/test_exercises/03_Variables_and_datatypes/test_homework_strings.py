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


@pytest.mark.strings
def test_names(helpers):
    helpers.student_file = helpers.home_dir + 'names.py'
    helpers.expected_pycode = [
        # Create a string variable with your name, call it my_name
        r'''\bmy_name\s*=\s*['"]\w+["']''',
        # Create a string variable with your family name,
        # call it my_family_name
        r'''\bmy_family_name\s*=\s*['"]\w+["']''',
        # Create a string variable called my_full_name which is composed from
        # the 2 variables my_name and my_family_name.
        r'''\bmy_full_name\s*=.*\bmy_name\b.*\bmy_family_name\b''',
        # Create a variable with your city name: call it my_city_name
        r'''\bmy_city_name\s*=\s*['"]\w+['"]''',
        # Create a variable msg with "My name is X and I’m from Y" using
        # the variables you created above
        r'''\bmsg\s*=.*[f'My name is {]my_(full_)?name''' +
        r'''[} and I'm from {my_city_name}]'''
    ]

    helpers.test_assignment()


@pytest.mark.strings
def test_times(helpers):
    helpers.student_file = helpers.home_dir + 'times.py'
    expected_msg = ('You have to spend {} minutes this week to ' +
                    'complete ROSE homework')
    helpers.input = [['2', '3'], ['11', '6'], ['10', '2']]
    helpers.expected_stdout = [
        [expected_msg.format(6)],
        [expected_msg.format(66)],
        [expected_msg.format(20)],
    ]

    helpers.test_assignment()


@pytest.mark.strings
def test_letter(helpers):
    helpers.student_file = helpers.home_dir + 'letter.py'
    helpers.expected_pycode = [
        r'''\b(print\(f'{date}\\n\\tFor\\n\\t{name}).*''',
    ]
    expected_msg = ('{}\n\tFor\n\t{}\n\t{}\n' +
                    '\nDear Mr./Mrs. {}\n' +
                    'Please visit our office as soon as possible to arrange ' +
                    'your payments.\n' +
                    'We can\'t wait until it’s all done ...\n\n' +
                    'Sincerely\n\tKoogle Inc.\n\t{}')
    helpers.input = [
        ['3.3.20', 'Anna', 'Rasbery, US', 'Hotel california, US'],
        ['5.4.21', 'Yael', 'Herzel 5, Haifa', 'Yam 1, Tel Aviv']
    ]
    helpers.expected_stdout = [
        [r'.*' + expected_msg.format(helpers.input[0][0],
                                     helpers.input[0][1],
                                     helpers.input[0][2],
                                     helpers.input[0][1],
                                     helpers.input[0][3])],
        [r'.*' + expected_msg.format(helpers.input[1][0],
                                     helpers.input[1][1],
                                     helpers.input[1][2],
                                     helpers.input[1][1],
                                     helpers.input[1][3])]
    ]

    helpers.test_assignment()


@pytest.mark.strings
def test_manipulations(helpers):
    helpers.student_file = helpers.home_dir + 'manipulations.py'
    helpers.expected_pycode = [
        # declare the varible s: "...very long line..."
        r'''\b[s]\s*=\s*[\'\'\'].*''',
        r'''.*[\'\'\']'''
    ]

    helpers.test_assignment()
