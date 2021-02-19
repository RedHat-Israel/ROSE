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


@pytest.mark.dictionary
def test_countries(helpers):
    helpers.set_student_file('countries.py')
    helpers.expected_pycode = [
        # Create a new dictionary with Udi’s flights number to each country:
        # "Italy":2 "Spain":3 "Israel":1
        [r'''^.*\s*=\s*\{.*\bItaly\b.*\:\s?2\s?,.*\bSpain\b.*\:\s?3\s?,''' +
         r'''.*\bIsrael\b.*\:\s?1\s?\}''',
         'set the dictionary using: {"Italy":2 "Spain":3 "Israel":1}'],
        # Insert a new element : "Belgium":1
        [r'''^.*\[(('Belgium')|("Belgium"))\]\s*=\s*1''',
         'to add a key-value pair use: `dict["key"] = value`'],
        # Delete “Italy” record from the dictionary
        [r'''^del\s*.*\[(('Italy')|("Italy"))\]$''',
         'to delete a key-value pair use: `del dict["key"]'],
        # Print how many times Udi was in Spain
        [r'''print\(.*\[(('Spain')|("Spain"))\]\)''',
         'to print a value use: `print(dict["key"])`'],
    ]

    helpers.test_assignment()


@pytest.mark.dictionary
def test_family(helpers):
    helpers.set_student_file('family_members_average_age.py')
    helpers.expected_pycode = [
        # Define a dictionary called ages, ages should be empty in it this time
        [r'''^ages\s*=\s*\{\}$''',
         'define a dictionary using `ages = {}`'],
        # Add your family members names to the dictionary with their ages.
        # for example: “Samira”:8
        [r'''(ages\.update\({)|(ages\[.*\]=\d*)''',
         'add a member using dict.update() or dict(key)=value'],
        # Print the dictionary
        [r'''^print\(.*\bages\b.*\)''',
         'print the dictionary using print(dict)'],
        # Calculate the average age in your family using the dictionary
        # and print it.
        [r'''(for.*in ages\.values\(\):)|(sum\(ages\.values\(\)\))|''' +
         r'''(ages\[.*\]\s*\+\s*ages\[.*\])''',
         'sum the members by using: sum(dict.values() or ' +
         'for loop on dict.values or by adding dict[key]'],
        [r'''(\/\s*len\(ages\))|(\/\s*\d)''',
         'to calculate average you can divide by using len(dict)'],
    ]

    helpers.expected_stdout = [
        [r'''\'\w*\':\s\d*''',
         'please print the dictionary `ages`'],
        [r'''\'\w*\':\s\d*''',
         r'^[^{].*\b\d*\b'],
    ]

    helpers.test_assignment()
