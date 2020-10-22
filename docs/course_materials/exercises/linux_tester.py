import os
import datetime as dt
from tester import Tester
import color_print
import command_dictionary as cd

class LinuxTester(Tester):

    def __init__(self, home, exe_module):
        self.home = home
        self.exe_module = exe_module
        self.exercise_commands = exe_module.exercise_commands
        self.exercise_paths = exe_module.exercise_paths
        self.exercise_deleted_paths = exe_module.exercise_deleted_paths

    def get_student_commands(self):
        """
        Checks stutent history file for key commands in the past 10 days.
        """
        shell_type = os.path.basename(os.environ["SHELL"])
        # used to get the epoch for x days back
        past_date = str((dt.datetime.today() - dt.timedelta(days=10)).timestamp())
        hist_path = self.home + '/.' + shell_type + '_history'

        my_commands = []
        with open(hist_path, 'r') as rf:
            for line in rf:
                if line[2:12] >= past_date:
                    my_commands.append(line[:-1])
        return my_commands

    @staticmethod
    def print_command_description(command):
        if cd.command_dictionary.get(command) is not None:
            print(" for {} ... ".format(cd.command_dictionary[command]), end='')
        else:
            print(" checking command structure", end='')

    def used_all_commands(self):
        student_commands = self.get_student_commands()
        num_of_used_commands = 0
        print("Checking used commands...")
        for command in self.exercise_commands:
            color_print.info("'" + command + "'", 0)
            self.print_command_description(command)
            
            # Print feedback about the command
            if not any(command in performed_command for performed_command in student_commands):
                color_print.negative("Missing")
            else:
                color_print.positive("Used")
                num_of_used_commands += 1
        
        print("Got {} out of {} commands.\n".format(str(num_of_used_commands), str(len(self.exercise_commands))))
        if num_of_used_commands == len(self.exercise_commands):
            return True
        return False
    
    @staticmethod
    def created(check_path):
        if os.path.exists(check_path):
            color_print.positive("Created")
            return 1
        else:
            color_print.negative("Missing")
            return 0

    @staticmethod
    def deleted(check_path):
        if not os.path.exists(check_path):
            color_print.positive("Deleted")
            return 1
        else:
            color_print.negative("Was not deleted")
            return 0

    def check_all_paths(self, paths_to_check, path_type):
        """
        paths_to_check will get a list of exercise paths to create or delete.
        path_type will get CREATED or DELETED.
        """
        case_type = {'created':self.created, 'deleted':self.deleted}
        num_of_paths = 0
        print("Checking " + path_type + " directories or files...")
        for cur_path in paths_to_check:
            check_path = self.home + cur_path
            color_print.info("'" + check_path + "'", 0)
            print(" ... ", end='')

            num_of_paths += case_type[path_type](check_path)
        print("{} {} out of {} directories.\n".format(path_type.capitalize(),
                                                     str(num_of_paths), str(len(paths_to_check))))
        if num_of_paths == len(paths_to_check):
            return True
        return False

    def test(self):
        check_commands = self.used_all_commands()
        check_paths = self.check_all_paths(self.exercise_paths, 'created')
        
        # run the function only if the check is needed
        if len(self.exercise_deleted_paths) > 0: 
            check_deleted_paths = self.check_all_paths(self.exercise_deleted_paths, 'deleted')
        else:
            check_deleted_paths = True
        
        if check_commands and check_paths and check_deleted_paths:
            return True
        else:
            return False     