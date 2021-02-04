# Adding test files for Linux

To add a check file use the convention `check_` followed by `homework` or `class_exercise`, and exercise number.  
Make sure you save the check file in the `01_Linux` directory.

## Linux check_exercise files:

The check_exercise file needs 3 lists for tests:
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
