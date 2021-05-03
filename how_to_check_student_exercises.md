# Checking Exercises

## Running the checks

First, make sure you are using python 3.7 or later:  

        `pipenv --python /usr/local/bin/python3.7 shell`

Install all dependencies:  

        `pipenv install --dev`

Second, change directory to test folder before running the tests:  

        `cd docs/course_materials/exercises/test_exercises`

For getting the Help use:  

        `python rose_check.py --help`

For the list of all available check files use `-e` or `--exercises`:  

        `python rose_check.py -e`

For checking an exercise, you should use `-t` or `--test_exercise` in combination  
with the test name. For example:  

        `python rose_check.py -t <exercise_name>`

If you need to run on a directory different from HOME use `-s` or `--set_dir`.  
It should include all student homework files:  

        `python rose_check.py -t <exercise_name> -s <student _homework_dir>`
