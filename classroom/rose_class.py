import argparse
import importlib
import logging
import os.path
import sys
import class_creator
import connect_service


def main():
    '''
    Getting user input and preforming corresponding actions.
    Available functions:
    - Create class in classroom.
    - Update teacher list.
    - Update student list.
    '''
    
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser(description='ROSE Classroom')
    parser.add_argument('--create_class', '-c', dest='class_name',
                        help='Creating a new class using given name. '
                            'If not specified, '
                            'class won\'t be created.')
    parser.add_argument('--print_class', '-p', action="store_true",
                        help='Printing existing classes.')
    parser.add_argument('--teacher_list', '-t', dest='teacher_list',
                        help='Adding teachers using a list. '
                            'Expects csv file.'
                            'If class exists,'
                            'please provide class ID using -i.')
    parser.add_argument('--student_list', '-s', dest='student_list',
                        help='Adding students using a list. '
                            'Expects csv file.'
                            'If class exists,'
                            'please provide class ID using -i.')
    parser.add_argument('--class_id', '-i',
                        help='Specifies a class id for adding student '
                            'lists or teacher lists.'
                            'Use combined with -t and/or -s')

    args = parser.parse_args()

    '''Set up the service to google classroom'''
    service = connect_service.create_service()

    if args.class_name is not None:
        args.class_id = class_creator.create_course(service, args.class_name)

    if args.print_class:
        class_creator.print_courses(service)

    if args.class_id is None and not args.print_class:
        print('Please use --help to inspect the possible actions.')
    else:
        if args.teacher_list is not None:
            pass

        if args.student_list is not None:
            pass

        if (args.student_list is None and args.teacher_list is None
            and not args.print_class):
            print('Please use -s to update student list',
                  'or/and -t to update teacher list.')

if __name__ == '__main__':
    main()