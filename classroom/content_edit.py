import os
from googleapiclient import errors

"""
Topics in classroom
"""
def print_topics(service):
    # TODO: adapt the function for topics
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

def create_topic(service, title, course_id):
    topic = {'name': title}
    new_topic = service.courses().topics().create(
                                            courseId=course_id,
                                            body=topic).execute()
    print(f"Topic created: {new_topic['name']} {new_topic['id']}")