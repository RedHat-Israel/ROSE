# Adding test files for Python

## Setting up

To add a test file:

1. You should name it according to the `exercise/homework` theme.
2. For every test function, add an appropriate decorator (aka `mark` in pytest). Use the same `mark('@pytest.mark.<topic>')` for tests you would like to run together. For example: `@pytest.mark.variables` for variables homework check.
3. In order for `pytest` to recognize the new marks, you need to add them to the `pytest.ini` file.
4. Each function in the test file should be named: `test_exercise_#` and should invoke `helpers` as input. For example: `def test_variables_1(helpers)`
5. The `helpers` is defined by `pytest fixture` and creates a `Helpers class` that stores our check values and the functions for the testing.

## Variables in the test files

Each test needs the following variables:

1. **helpers.student_file**(string):  
   Stores the path for student file for testing.
   `set_student_file` function appends automatically the HOME directory or the directory we supplied to the name of the student file according to the homework instructions.

2. **helpers.expected_pycode** (boolean):
   Initiated as True, if there is no code to check should be changed to False.

3. **helpers.expected_stdout**(boolean):
   Initiated as True, if there is no stdout to check should be changed to False.

4. **helpers.tests_list**(list):
   Should include code/text we expect in the student answer file/stdout and the error message to be displayed.
   The expected values should be supplied as string or in regex format.  
   An example for the check:

   ```Python
   helpers.tests_list = [[r'^.*x *= *9.*', 'x should equal 9'], 
                              [r'^.*print\(.*z.*\).*',
                                 'please use the print function']]
   ```

   You can also add a check for 'working but not optimal' solution by using the following:  

 ```Python
   helpers.tests_list = [[r"f'best \{solution\}",
                               [r"other correct solution",
                                'explanation for better solution',
                                'error message']]]
   ```

5. **helpers.input**(list):
   Should include all the inputs we want to check.  
   For example: `helpers.input = [['10', '3'], ['5', '6']]`, will check 2 pairs of input.

## Under the hood (using pytest)

- rose_check.py calls pytest when `-t <mark>` is invoked
- pytest.ini sets the parameters for the pytest run:
  - addopts: runs pytest using cmdline arguments
    - --tb=no to hide long trace output
    - -v for verbose, shows PASSED/FAILED
    - --no-header, --no-summary - hides those parts of outputs
  - markers - all our marks(decorators) should be registered here for pytest to recognize them.
  - log_cle - specify which log to show on live log. Use `LOGGER.error(message)` to show output to the user (also available `LOGGER.info/warning`).
