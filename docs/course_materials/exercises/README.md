# Checking Exercises

## Running the checks

For checking an exercise, you should use the following:  

        `rose-check lesson/check_homework_1`

If you need to run on a directory different from home use:

        `rose-check lesson/check_homework_1 -s your_home_dir`

## Adding tests to the Linux check_exercise file

The check_exercise file has 3 lists used for tests:
1. **exercise_commands**:  
   Should include all the commands the student is expected to use. It can be a built in command like `cat` or a partial command that makes sure the student used some functionality. You can also check if something was created that was deleted later in the exercise, like `file.txt`.

2. **exercise_paths**:  
   Should include all the paths we expect to have at the end of the exercise, all relative paths to home directory.
   For example: `hw1/other` or `hw1/file.txt`.
   
3. **exercise_deleted_paths**:  
   Should include all the paths we expect to be absent, since we want the student to delete or change during the exercise. All paths are relative to home directory.
   For example: `hw1/other` or `hw1/file.txt`.
