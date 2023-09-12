import os
import datetime as dt
import color_print
import command_dictionary as cd

# set from rose_check.py from the check_exercise file.
HOME = ""
COMMANDS = []
PATHS = []
DELETED_PATHS = []


def get_student_commands():
    """
    Checks student history file for key commands in the past 'x' days.
    """
    shell_type = os.path.basename(os.environ["SHELL"])
    # used to get the epoch for x days back
    past_date = str((dt.datetime.today() - dt.timedelta(days=10)).timestamp())
    hist_path = HOME + "/." + shell_type + "_history"

    my_commands = []
    with open(hist_path, "r") as rf:
        for line in rf:
            if line[2:12] >= past_date:
                my_commands.append(line[:-1])
    return my_commands


def print_command_description(command):
    if cd.command_dictionary.get(command) is not None:
        print(f" for {cd.command_dictionary[command]} ... ", end="")
    else:
        print(" checking command structure", end="")


def used_all_commands():
    student_commands = get_student_commands()
    num_of_used_commands = 0
    print("Checking used commands...")
    for command in COMMANDS:
        # color_print.info('"' + command + '"', 0)
        color_print.info(command, 0)
        print_command_description(command)

        # Print feedback about the command
        if not any(
            command in performed_command for performed_command in student_commands
        ):
            color_print.negative("Missing")
        else:
            color_print.positive("Used")
            num_of_used_commands += 1

    print(f"Got {str(num_of_used_commands)} out of {str(len(COMMANDS))}\n")
    if num_of_used_commands == len(COMMANDS):
        return True
    return False


def created(check_path):
    if os.path.exists(check_path):
        color_print.positive("Created")
        return 1
    else:
        color_print.negative("Missing")
        return 0


def deleted(check_path):
    if not os.path.exists(check_path):
        color_print.positive("Deleted")
        return 1
    else:
        color_print.negative("Was not deleted")
        return 0


def check_all_paths(path_type):
    """
    paths_to_check will get a list of exercise paths to create or delete.
    path_type will get CREATED or DELETED.
    """
    case_type = {"created": created, "deleted": deleted}
    path_to_check = {"created": PATHS, "deleted": DELETED_PATHS}
    num_of_paths = 0
    print("Checking " + path_type + " directories or files...")
    for cur_path in path_to_check[path_type]:
        check_path = HOME + cur_path
        # color_print.info('"' + check_path + '"', 0)
        color_print.info(check_path, 0)
        print(" ... ", end="")

        num_of_paths += case_type[path_type](check_path)
    print(
        f"{path_type.capitalize()} {str(num_of_paths)} out of "
        f"{str(len(path_to_check[path_type]))} directories.\n"
    )
    if num_of_paths == len(path_to_check[path_type]):
        return True
    return False


def is_exercise_done():
    check_commands = used_all_commands()
    check_paths = check_all_paths("created")

    # run the function only if the check is needed
    if len(DELETED_PATHS) > 0:
        check_deleted_paths = check_all_paths("deleted")
    else:
        check_deleted_paths = True

    if check_commands and check_paths and check_deleted_paths:
        return True
    else:
        return False
