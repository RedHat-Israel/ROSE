import os
import datetime as dt
from tester import Tester
import color_print
import command_dictionary as cd

class PythonTester(Tester):

    def __init__(self, home, exe_module):
        self.home = home
        self.exe_module = exe_module
        # self.exercise_commands = exe_module.exercise_commands
        # self.exercise_paths = exe_module.exercise_paths
        # self.exercise_deleted_paths = exe_module.exercise_deleted_paths

    def test(self):
        pass
        # if condition:
        #     return True
        # else:
        #     return False     