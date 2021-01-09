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


def test_strings_names(helpers, home_folder):
    student_file = str(home_folder) + 'Names.py'
    helpers.does_student_file_exist(student_file)
    answers = [
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
        r'''\bmsg\s*=.*My name is .* and I'm from .*''',
        r'''\bmsg\s*=.*\bmy_(full_)?name\b.*\bmy_city_name\b'''
    ]
    helpers.check_list_of_answers_from_file(answers, student_file)


def test_strings_times(helpers, home_folder):
    student_file = str(home_folder) + 'Times.py'
    expected_msg = ('You have to spend {} minutes this week to' +
                    'complete ROSE homework')

    helpers.does_student_file_exist(student_file)
    for inputs, expected_output in [
        [['2', '3'], expected_msg.format(6)],
        [['11', '6'], expected_msg.format(66)],
        [['10', '2'], expected_msg.format(20)],
    ]:
        helpers.check_output(student_file, inputs, expected_output)
