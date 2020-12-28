# Managing a Course in Classroom

## Setup

1. Create a credentials.json file by using [google quickstart](https://developers.google.com/classroom/quickstart/python) (step 1)  
   Choose your app name, desktop app, and press the button 'download client configuration'.  
   Save the file in the rose classroom directory.

2. Make sure that the following packages are installed: (step 2 in google guide, also included in ROSE pipfile for developers)
   - google-api-python-client
   - google-auth-httplib2
   - google-auth-oauthlib

3. In first run, an app authentication window will pop. Authorization for classroom.courses and classroom.rosters, allow both (creates token.pickle file).

## Functionality

First, make sure you are running the commands from the **classroom** directory.

### Course management:  
Each command will start with:  

        `python rose_class.py --course

For creating a course use:  

        `python rose_class.py --course -c "course name"`

For retrieving existing courses and their IDs use:  

        `python rose_class.py --course -p`

For addressing a specific course use ID:

        `python rose_class.py --course -i ID`

For adding students using a list  
(requires course ID and a file with mail addresses, accepts csv files):  

        `python rose_class.py --course -i ID -s file_path`

For adding teachers using a list  
(requires course ID and a file with mail addresses, accepts csv files):  

        `python rose_class.py --course -i ID -t file_path`

## Notice

- A mail can be added to teacher list or student list, not both.
- Only one invitation can exist for each mail. Before sending a new invitation the old one must be canceled.

### Topics management:  
Each command will start with:  

        `python rose_class.py --topic

For creating a topic in a course use (have to specify the course ID):  

        `python rose_class.py --course -i ID --topic -c "topic name"`

For retrieving existing topics in a course and their IDs use (have to specify the course ID):  

        `python rose_class.py --course -i ID --topic -p`