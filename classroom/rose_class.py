import argparse
import logging
import course_creator
import connect_service
import content_edit


def main():
    '''
    Getting user input and preforming corresponding actions.
    Available functions:
    - Create course in classroom.
    - Update teacher list.
    - Update student list.
    '''

    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser(description='ROSE Classroom')
    parser.add_argument('--course', action='store_true',
                        help='A flag for course actions, stores True. '
                             'Has to be followed by an action as --create. '
                             'If not specified, will be False.')
    parser.add_argument('--create', '-c', dest='name',
                        help='Creating a new instance using given name. '
                             'If not specified, cannot be created. '
                             'Follows an instance type as --course. '
                             'For creating Topics, Assignments and more '
                             'please specify the course/topic id using -i.')
    parser.add_argument('--print', '-p', action="store_true",
                        help='Printing existing instances.')
    parser.add_argument('--teacher_list', '-t', dest='teacher_list',
                        help='Adding teachers using a list, '
                             'expects a csv file. '
                             'If course exists, '
                             'please provide course ID using -i.')
    parser.add_argument('--student_list', '-s', dest='student_list',
                        help='Adding students using a list, '
                             'expects csv file. '
                             'If course exists, '
                             'please provide course ID using -i.')
    parser.add_argument('--id', '-i',
                        help='Specifies an instance id. Can be used for '
                             'adding student lists or teacher lists, adding '
                             'Topics, Homework and more. '
                             'Please specify the needed action. '
                             'Use combined with instance type as --course.')

    args = parser.parse_args()

    '''Set up the service to google classroom'''
    service = connect_service.create_service()

    if args.course:
        if args.name:
            args.id = course_creator.create_course(service, args.name)
            print(f'The id returned {args.id}')
        elif args.print:
            course_creator.print_courses(service)
        elif not args.id:
            print('Please use --help to inspect the possible actions.')
        else:
            if args.teacher_list:
                course_creator.create_invitation(service, args, 'TEACHER')

            if args.student_list:
                course_creator.create_invitation(service, args, 'STUDENT')

            no_list = args.student_list is None and args.teacher_list is None
            if (no_list):
                print('Please use -h to check the available actions.')


if __name__ == '__main__':
    main()
