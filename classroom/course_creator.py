import csv
import os
from googleapiclient import errors


def print_courses(service):
    # Call the Classroom API
    results = service.courses().list(pageSize=10).execute()
    courses = results.get('courses', [])

    if not courses:
        print('No courses found.')
    else:
        print('Courses:')
        for course in courses:
            print(f"Title: {course['name']}, ID: {course['id']}")


def create_course(service, course_name):
    course_data = {'name': course_name,
                   'descriptionHeading': 'Welcome to ' + course_name,
                   'description': ("We'll be learning about coding from a " +
                                   "combination of lectures, course work, " +
                                   "and home projects. Let's start!"),
                   'ownerId': 'me',
                   'courseState': 'PROVISIONED'}
    course = service.courses().create(body=course_data).execute()
    print(f"Course created: {course.get('name')} {course.get('id')}")
    return course.get('id')


def load_list(list_path):
    '''
    Load student/teacher list from csv file.
    '''
    if not os.path.exists(list_path):
        print(f"This path does not exist: {list_path}.")
        return None
    with open(list_path, mode='r') as csv_file:
        mail_list = []
        csv_reader = csv.reader(csv_file, delimiter=',')
        if csv_reader is None:
            print("The list is empty.")
            return mail_list
        for row in csv_reader:
            if "gmail.com" in row[0]:
                mail_list.append(row[0])
            else:
                print(f"Not added, {row[0]} is an invalid mail address.")
        return mail_list


def create_invitation(service, args, invite_type):
    """
    Uses:
    - service - connection to google classroom.
    - args - for list path and course ID.
    - invite_type - for specifying the invitation type - STUDENT or TEACHER
    Function:
    - Creates invitations using the mail list.
    """
    if invite_type == 'STUDENT':
        list_path = args.student_list
    else:
        list_path = args.teacher_list
    mail_list = load_list(list_path)
    if len(mail_list) > 0:
        for mail in mail_list:
            invitation = {
                'courseId': args.id,
                'role': invite_type,
                'userId': mail,
            }
            try:
                service.invitations().create(body=invitation).execute()
                print(f'Invitation was sent to {mail}')
            except errors.HttpError as e:
                if '409' in str(e):
                    print(f'Not added, {mail} has a pending invitation.')
                elif '400' in str(e):
                    print(f'Not added, {mail} already listed in course.')
                else:
                    print('No permissions or wrong course ID.')
