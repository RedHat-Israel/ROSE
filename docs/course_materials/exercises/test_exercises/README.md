# Checking Exercises

## Running the checks

First, make sure you are using python 3.7 or later.  

        `pipenv --python /usr/local/bin/python3.7 shell`

For checking a linux exercise, you should use the following:  

        `rose_check <lesson>/<check_homework_#>`

For checking other exercises, you should use the following:  

        `rose_check -t <mark_of_exercise>`

If you need to run on a directory different from HOME use:  

        `rose-check <lesson>/<check_homework_#> -s <your_home_dir>`

or  

        `rose_check -t <mark_of_exercise> -s <your_home_dir>`

For the list of all available check files use:  

        `rose_check --help`


## Adding check_exercise files(linux lesson):

To add a check file use the convention `check_` followed by `homework` or `class_exercise`, and exercise number.

## Linux check_exercise files:

The check_exercise file uses 3 lists for tests:
1. **exercise_commands**:  
   Should include all the commands the student is expected to use.  
   It can be a built in command like `cat` or a partial command that makes sure the student used some functionality.  
   You can also check for file/folders that were deleted later in the exercise, like `file.txt`.

2. **exercise_paths**:  
   Should include all the paths we expect to have at the end of the exercise, all relative paths to home directory.
   For example: `hw1/other` or `hw1/file.txt`.
   
3. **exercise_deleted_paths**:  
   Should include all the paths we expect to be absent, since we want the student to delete or change them during the exercise.  
   All paths are relative to home directory.
   For example: `hw1/other` or `hw1/file.txt`.

## Adding test files(not linux lesson):

To add a test file:
1. You should name it according to the `exercise/homework` theme.
2. For every test function, add an appropriate decorator (aka `mark` in pytest). Use the same `mark('@pytest.mark.<topic>')` for tests you would like to run together. For example: `@pytest.mark.variables` for variables homework check.
3. In order for `pytest` to recognize the new marks, you need to add them to the `pytest.ini` file.
4. Each function in the test file should be named: `test_exercise_#` and should invoke `helpers` as input. For example: `def test_variables_1(helpers)`
5. The `helpers` is defined by `pytest fixture` and creates a `Helpers class` that stores our check values and the functions for the testing.

## Variables in the files:

The tests uses 3 lists for tests:
helpers.student_file = helpers.home_dir + 'variables_1.py'
     
    helpers.expected_stdout
1. **helpers.student_file**:  
   Stores the path for student file for testing.
   Includes the HOME directory or the directory we supplied and the name of the student file according to the homework instructions.

2. **helpers.expected_pycode**:  
   Should include code/text we expect in the student answer file.  All values shold be supplied as string or in regex format.  
   For example: `helpers.expected_pycode = [r'^.*x *= *9.*', r'^.*print\(.*z.*\).*']` for checking code.
   
3. **helpers.input**
   Should include all the inputs we want to check.  
   For example: `helpers.input = [['10', '3'], ['5', '6']]`, will check 2 pairs of input.

4. **helpers.expected_stdout**:  
   Should include the output we expect to get.  
   For example: `helpers.expected_stdout = [[r'.*30', r'.*7', r'.*' + str(10/3), r'.*1']]` for 4 printouts tht can be prefixed with text.

## Under the hood (using pytest):

- rose_check.py calls pytest when `-t <mark>` is invoked
- pytest.ini sets the parameters for the pytest run:
  - addopts: runs pytest using cmdline arguments
    - --tb=no to hide long trace output
    - -v for verbose, shows PASSED/FAILED
    - --no-header, --no-summary - hides those parts of outputs
  - markers - all our marks(decorators) should be registered here for pytest to recognize them.
  - log_cle - specify which log to show on live log. Use `LOGGER.error(message)` to show output to the user (also available `LOGGER.info/warning`). 