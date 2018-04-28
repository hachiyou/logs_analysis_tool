#!/usr/bin/env python3.6.5

# import print_function so that python2 will be able to use the end parameter
from __future__ import print_function
import sys
import newsdb
from newsdb import execute_query


def display_ui():
    """Display a text UI for options,
    sends the user input to other functions.
    """
    print('''
==============================================
|| Thank you for using the reporting tool.  ||
|| Options:                                 ||
|| [1] Show articles.                       ||
|| [2] Show authors.                        ||
|| [3] Show erroneous access percentage.    ||
|| [Q] Quit.                                ||
==============================================
Input: ''', end='')
    return check_version_input()


def main():
    """Main function."""

    # Create the view so that all the infos are clearly presented.
    newsdb.__create_view()
    command = str(display_ui())

    # Continue the program until option Q is selected.
    while command.upper() != 'Q':
        if command == '1':
            command = str(display_ui())
        elif command == '2':
            command = str(display_ui())
        elif command == '3':
            command = str(display_ui())
        command = str(display_ui())
    # Exit the program after Q is pressed.
    sys.exit()


def check_version_input(prompt=""):
    """Checking the version of python, and use the appropriate input function.

    Arg:
        prompt (str): a string to display when prompting for input.
    """
    if sys.version_info[0] < 3:
        return raw_input(prompt)
    else:
        return input(string)


if __name__ == '__main__':
    main()
