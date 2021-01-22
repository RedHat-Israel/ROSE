# Checking Exercises

## Running the checks

First, make sure you are using python 3.7 or later.  

        `pipenv --python /usr/local/bin/python3.7 shell`

Second, change directory to `ROSE/docs/course_materials/exercises/test_exercises` before running the tests.

For checking an exercise, you should use `-t` or `--test_exercise` in combination  
with the test name. For example:  

        `rose_check -t <check_homework_#>`

or

        `rose_check -t <mark_of_exercise>`

If you need to run on a directory different from HOME use `-s` or `--set_dir`:  

        `rose-check -t <check_homework_#> -s <your_dir>`

For the list of all available check files use `-e` or `--exercises`:  

        `rose_check -e`
