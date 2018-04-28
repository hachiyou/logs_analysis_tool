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


def parse_query_display(query, selectN):
    """Submit the query to database functions,
    then parse and display the result

    Args:
        query (str) : SQL query
        selectN (str) : an input taken from user to tell
            the database how many result should be display.
    """

    # Check the pass-in selectN argument
    if type(selectN) is str and not selectN.isdigit():
        selectN = 0

    r = execute_query(query, selectN)

    # Parsing the result and displaying them on screen.

    print("\n" + "- "*30)

    if query == newsdb.SELECT_ALL_ARTICLES:
        print("Lists of all articles."
              if selectN == 0
              else "Top " + str(selectN) + " articles with most views:")
        for row in r:
            print(row[1] + " - " + str(row[2]) + " views.")
    elif query == newsdb.SELECT_ALL_AUTHORS:
        print("Lists of all authors."
              if selectN == 0
              else "Top " + str(selectN) + " authors with most views:")
        for row in r:
            print(row[0] + " - " + str(row[2])
                  + " views across all the articles.")
    else:
        print("Lists of all dates with 1% errors or more:")
        for row in r:
            print(row[0].strftime("%B %d, %Y") + " - " + str(row[1]))
    print("- "*30 + "\n")


def main():
    """Main function."""

    # Create the view so that all the infos are clearly presented.
    newsdb.__create_view()
    command = str(display_ui())

    # Continue the program until option Q is selected.
    while command.upper() != 'Q':
        if command == '1':
            parse_query_display(
                newsdb.SELECT_ALL_ARTICLES,
                check_version_input("Show top Nth (default = 0, 0 for show all): "))  # noqa
        elif command == '2':
            parse_query_display(
                newsdb.SELECT_ALL_AUTHORS,
                check_version_input("Show top Nth (default = 0, 0 for show all): "))  # noqa
        elif command == '3':
            parse_query_display(newsdb.SELECT_ERROR_DATE, 0)
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
