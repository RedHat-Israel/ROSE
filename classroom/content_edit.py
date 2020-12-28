"""
Topics in classroom
"""


def print_topics(service, course_id):
    # Call the Classroom API
    results = service.courses().topics().list(courseId=course_id).execute()
    topics = results.get('topic', [])

    if not topics:
        print('No topics found.')
    else:
        print('Topics:')
        for topic in topics:
            print(f"Title: {topic['name']}, ID: {topic['topicId']}")


def create_topic(service, title, course_id):
    topic = {'name': title}
    new_topic = service.courses().topics().create(
                                            courseId=course_id,
                                            body=topic).execute()
    print(f"Topic created: {new_topic['name']} {new_topic['topicId']}")


"""
Topics in classroom
"""
