"""
Setting colors for the output:
green for positive feedback
red negative feedback
yellow for commands and paths
"""
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"


def info(feedback, new_line=True):
    print_color(feedback, YELLOW, new_line)


def positive(feedback, new_line=True):
    print_color(feedback, GREEN, new_line)


def negative(feedback, new_line=True):
    print_color(feedback, RED, new_line)


def print_color(feedback, color, new_line):
    """
    Used to print in color with an option for new line.
    """
    if new_line:
        p_end = "\n"
    else:
        p_end = ""
    print(f"{color} {feedback}\033[00m", end=p_end)
