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
    helpers.expected_pycode = [
        # comment for Create a list exercise
        [r'''^[#]+.*((C|c)reate|1)''',
         'comment for exercise number 1 is missing'],
        # Create two empty lists list1 and list2 in different ways
        [r'''^list.*\s*=\s*\[\]''', 'use [] to set a list'],
        [r'''^list.*\s*=\s*list\(\)''',
         'use list() to set a list'],
        # Create a list l1 with the numbers: 2,3,4,5,6.
        [r'''^l1\s*=\s*\[2,\s*3,\s*4,\s*5,\s*6\]''',
         'set list l1 with the values [2, 3, 4, 5, 6]'],
        # Print the index of the number 6
        [r'''l1\.index\(6\)''',
         'to find an index please use list.index() function'],
        # Append the numbers 7 and 8 to the end of l1
        [r'''l1\.(extend|append)\(\[?7.*''',
         'you can use list.extend([]) or list.append() to add values'],
        # Print the length of the l1
        [r'''len\(l1\)''',
         'use len(list) to check the length of the list'],
        # Add the number 1 to the l1 at index 0
        [r'''l1\.insert\(0, 1\)''',
         'for inserting at an index use list.insert(index, value)'],
        # comment for Slicing a list exercise
        [r'''^[#]+.*((S|s)licing|2)''',
         'comment for exercise number 2 is missing'],
        # Print first 4 numbers of l1
        [r'''(print\()?l1\[0?:4\]\)?''',
         'use range for printing a sequence - [:4]'],
        # Print 4 last numbers of l1
        [r'''(print\()?l1\[-4:\]\)?''',
         'use range for printing a sequence - [-4:]'],
        # Print the two numbers in the middle
        [r'''(print\()?l1\[((3:5)|(\(len\(l1\)\/2\-1\):''' +
         r'''\(len\(l1\)\/2\+1\)))\]\)''',
         'make sure to choose the middle, you can use len(list)/2'],
        # Print l1[20], which error did you get?
        # What does this error say? (write your answer in a comment #)
        [r'''^[#].*IndexError: list index out of range''',
         'did you get the `IndexError: list index out of range`?'],
        # comment for Update a list exercise
        [r'''^[#]+.*((U|u)pdate|3)''',
         'comment for exercise number 3 is missing'],
        # Remove the items 4 and 5 from the l1 and print l1
        [r'''(del l1\[3:5\])|(l1.remove\(4\))''',
         'for deleting you can use `del list[:]` or list.remove(i)'],
        # Create a new list l2, with the items: -1, -2 ,-3 and print l2
        [r'''^l2\s*=\s*\[\-1,\s*\-2,\s*\-3\]''',
         'set list l2 with the values [-1, -2, -3]'],
        # Create a new list l3, with the items of l1 and l2, print l3
        [r'''(l3\s*\=\s*l1\s*\+\s*l2)|(l3\.extend\(l1\))''',
         'for adding lists use `c = a + b` or c.extend(a)...'],
        # Sort l3 and print the sorted list
        [r'''(print\()?l3\.sort\(\)''',
         'use list.sort() for sorting a list'],
        # Print the length of l1, l2, and l3
        [r'''(print\()?.*\blen\(l1\).*\)?''',
         'did you print all the lists length?'],
    ]

    helpers.expected_stdout = [
        [r'\b4\b[^\]]$',
         'Index of 6 should be 4'],
        [r'\b7\b[^\]]$',
         'length of l1 should be 7'],
        [r'\[1, 2, 3, 4\]',
         'first 4 numbers should be [1, 2, 3, 4]'],
        [r'\[5, 6, 7, 8\]',
         'last 4 numbers should be [5, 6, 7, 8]'],
        [r'\[4, 5\]',
         '2 middle numbers should be [4, 5]'],
        [r'\[1, 2, 3, 6, 7, 8\]',
         'l1 list should be [1, 2, 3, 6, 7, 8]'],
        [r'\[\-1, \-2, \-3\]',
         'l2 list should be [-1, -2, -3]'],
        [r'\[1, 2, 3, 6, 7, 8, \-1, \-2, \-3\]',
         'l3 list should be [1, 2, 3, 6, 7, 8, -1, -2, -3]'],
        [r'\[\-3, \-2, \-1, 1, 2, 3, 6, 7, 8\]',
         'sorted l3 should be [-3, -2, -1, 1, 2, 3, 6, 7, 8]'],
        [r'\b6\b[^\]]$',
         'len of l1 should be 6'],
        [r'\b3\b[^\]]$',
         'len of l2 should be 3'],
        [r'\b9\b[^\]]$',
         'len of l3 should be 9'],
    ]

    helpers.test_assignment()
