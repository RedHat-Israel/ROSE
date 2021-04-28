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


@pytest.mark.lists
def test_lists(helpers):
    helpers.set_student_file('lists.py')
    helpers.tests_list = [
        # comment for Create a list exercise
        [r'''^[#]+.*((C|c)reate|1)''',
         '1. Expected a comment for exercise 1 - create a list'],
        # Create two empty lists list1 and list2 in different ways
        [r'''^list.*\s*=\s*\[\]''',
         '1.1. Expected the list to be set by using `= []`'],
        [r'''^list.*\s*=\s*list\(\)''',
         '1.1. Expected the list to be set by using list()'],
        # Create a list l1 with the numbers: 2,3,4,5,6.
        [r'''^l1\s*=\s*\[2,\s*3,\s*4,\s*5,\s*6\]''',
         '1.2. List l1 is not defined properly'],
        # Print the index of the number 6
        [r'''l1\.index\(6\)''',
         '1.3. Expected the use of list.index()'],
        [r'.*?\b4\b(.*[^\]])?$',
         '1.3. Index of number 6 is incorrect'],
        # Append the numbers 7 and 8 to the end of l1
        [r'''l1\.(extend|append)\(\[?7.*''',
         '1.4. Expected list.extend([]) or list.append() to add values'],
        # Print the length of the l1
        [r'''len\(l1\)''',
         '1.5. Expected len(list) for getting the length of the list'],
        [r'.*?\b7\b(.*[^\]])?$',
         '1.5. Make sure to print out the length of l1'],
        # Add the number 1 to the l1 at index 0
        [r'''l1\.insert\(0,\s*1\)''',
         '1.6. Expected the use of list.insert(index, value)'],
        # comment for Slicing a list exercise
        [r'''^[#]+.*((S|s)licing|2)''',
         '2. Expected a comment for exercise 2 - Slicing a list'],
        # Print first 4 numbers of l1
        [r'''(print\()?l1\[0?:4\]\)?''',
         [r'for.*in range\(.*?4\)\:',
          '2.1 A better solution is using slicing - list[:4]',
          '2.1. Expected the use of slicing for printing a sequence']],
        [r'\[1, 2, 3, 4\]',
         [r'.*?\b1\b(.*[^\]])?$',
          '2.1. Expected a one line print of the first 4 numbers',
          '2.1. Expected the print of the first 4 numbers: 1,2,3,4']],
        # Print 4 last numbers of l1
        [r'''(print\()?l1\[-4:\]\)?''',
         [r'for.*in range\(4,\s?8\)\:',
          '2.2 A better solution is using slicing list[-4:]',
          '2.2. Expected the use of slicing a list ' +
          'with negative values for printing a sequence']],
        [r'\[5, 6, 7, 8\]',
         [r'.*?\b5\b(.*[^\]])?$',
          '2.2. Expected a one line print of the last 4 numbers',
          '2.2. Expected the print of the last 4 numbers: 5,6,7,8']],
        # Print the two numbers in the middle
        [r'''(print\()?l1\[((3:5)|(\(len\(l1\)\/2\-1\):''' +
         r'''\(len\(l1\)\/2\+1\)))\]\)''',
         '2.3. Expected the use of len(list) in retrieving the middle values'],
        [r'\[4, 5\]',
         '2.3. Expected the print of the 2 middle numbers'],
        # Print l1[20], which error did you get?
        # What does this error say? (write your answer in a comment #)
        [r'''^[#].*IndexError: list index out of range''',
         '2.4. Expected the `IndexError: ...`'],
        # comment for Update a list exercise
        [r'''^[#]+.*((U|u)pdate|3)''',
         '3. Expected a comment for exercise 3 - Update the list'],
        # Remove the items 4 and 5 from the l1 and print l1
        [r'''(del l1\[3:5\])|(l1.remove\(4\))''',
         '3.1. Expected the use of `del list[:]` or list.remove(i)'],
        [r'\[1, 2, 3, 6, 7, 8\]',
         '3.1. Expected a print of l1 list after removing the middle numbers'],
        # Create a new list l2, with the items: -1, -2 ,-3 and print l2
        [r'''^l2\s*=\s*\[\-1,\s*\-2,\s*\-3\]''',
         '3.2. Expected the definition of l2 as a list of numbers'],
        [r'print\(.*l2.*\)',
         '3.2. Expected a print out of l2 list'],
        # Create a new list l3, with the items of l1 and l2, print l3
        [r'''(l3\s*\=\s*l1\s*\+\s*l2)|(l3\.extend\(l1\))''',
         '3.3. Expected l3 to be defined by l1 and l2'],
        [r'\[1, 2, 3, 6, 7, 8, \-1, \-2, \-3\]',
         '3.3. Expected the print of l3 list that contains l1 and l2'],
        # Sort l3 and print the sorted list
        [r'''(print\()?l3\.sort\(\)''',
         '3.4. Expected the use of list.sort() for sorting a list'],
        [r'\[\-3, \-2, \-1, 1, 2, 3, 6, 7, 8\]',
         '3.4. Expected a print of the sorted l3 list'],
        # Print the length of l1, l2, and l3
        [r'''(print\()?.*\blen\(l1\).*\)?''',
         '3.5. Expected the use of len(list)'],
        [r'.*?\b6\b(.*[^\]])?$',
         '3.5. len of l1 should be 6'],
        [r'.*?\b3\b(.*[^\]])?$',
         '3.5. len of l2 should be 3'],
        [r'.*?\b9\b(.*[^\]])?$',
         '3.5. len of l3 should be 9'],
    ]

    helpers.test_assignment()
