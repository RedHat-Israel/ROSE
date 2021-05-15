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


@pytest.mark.dictionaries
def test_countries(helpers):
    helpers.set_student_file('countries.py')
    helpers.expected_stdout = False
    dictionary_message = str('make sure to set all the values in the ' +
                             'dictionary: {"Italy":2, "Spain":3, "Israel":1}')
    helpers.tests_list = [
        # Create a new dictionary with Udi’s flights number to each country:
        # "Italy":2 "Spain":3 "Israel":1
        [r'''^.*\s*=\s*\{\s*''',
         dictionary_message],
        [r'''.*\bItaly\b.*\:\s?2\s?,.*''',
         dictionary_message],
        [r'''.*\bSpain\b.*\:\s?3\s?,.*''',
         dictionary_message],
        [r'''.*\bIsrael\b.*\:\s?1\s?.*\}?''',
         dictionary_message],
        # Insert a new element : "Belgium":1
        [r'''^.*\[(('Belgium')|("Belgium"))\]\s*=\s*1''',
         'for adding a key-value pair expected: `dict["key"] = value`'],
        # Delete “Italy” record from the dictionary
        [r'''^del\s*.*\[(('Italy')|("Italy"))\]$''',
         'for deleting a key-value pair expected: `del dict["key"]'],
        # Print how many times Udi was in Spain
        [r'''print\(.*\[(('Spain')|("Spain"))\]\)''',
         'for printing a value expected: `print(dict["key"])`'],
    ]

    helpers.test_assignment()


@pytest.mark.dictionaries
def test_family(helpers):
    helpers.set_student_file('family_members_average_age.py')
    helpers.tests_list = [
        # Define a dictionary called ages, ages should be empty in it this time
        [r'''^ages\s*=\s*\{\}$''',
         'Expected to see a dictionary definition using `ages = {}`'],
        # Add your family members names to the dictionary with their ages.
        # for example: “Samira”:8
        [r'''(ages\.update\({)|(ages\[.*\]=\d*)''',
         'Expected the use of dict.update() or dict(key)=value for updating'],
        # Print the dictionary
        [r'''^print\(.*\bages\b.*\)''',
         'Expected the use of print(dict) for printing.'],
        [r'''(\'\w*\':\s\d*)|(r'^[^{].*\b\d*\b')''',
         'please print the dictionary `ages`'],
        # Calculate the average age in your family using the dictionary
        # and print it.
        [r'''(for.*in ages\.values\(\):)|(sum\(ages\.values\(\)\))|''' +
         r'''(ages\[.*\]\s*\+\s*ages\[.*\])''',
         'Expected the use of: sum(dict.values() or ' +
         'for loop on dict.values or by adding dict[key]'],
        [r'''(\/\s*len\(ages\))''',
         [r'''(\/\s*\d)''',
          'A better way to calculate average is using len(dict)',
          'to calculate average you can divide by using len(dict)']],
    ]

    helpers.test_assignment()
