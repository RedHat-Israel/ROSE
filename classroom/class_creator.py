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
                'description': """We'll be learning about coding from a
                                combination of lectures, class work,
                                and home projects. Let's start!""",
                'ownerId': 'me',
                'courseState': 'PROVISIONED'}
    course = service.courses().create(body=course_data).execute()
    print(f"Course created: {course.get('name')} {course.get('id')}")
    return course.get('id')
