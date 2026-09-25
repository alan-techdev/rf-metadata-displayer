'''
Steps:
>>> pwd
>>> python -m venv .venv
>>> source ./venv/bin/activate
>>> pip install -e .
>>> rfmetadata

'''
import sys
from argparse import ArgumentParser, Namespace

from PySide6 import QtWidgets

from rfmetadata import (
    __author__,
    __description__,
    __license__,
    __title__,
    __url__,
    __version__,
)  # type:ignore
from rfmetadata._help import bug_reporting
from rfmetadata.windows.main_window import MainWindow

"""
A- Make the project in edit mode
$ pwd
/home/alan/workspace-python/RTL-SDR/rf-metadata-displayer
$ pip install -e .
$ rfmetadata setting.json -vvv -ld /home/alan/tmp

//////////////////////////////////////////

B- Using PYTHONPATH (Not recommended)
Linux:
=====
$ export PYTHONPATH=/home/alan/workspace-python/RTL-SDR/rf-metadata-displayer/src
$ pwd
 /home/alan/workspace-python/RTL-SDR/rf-metadata-displayer/src
$ python rfmetadata setting.json -vvv -ld /home/alan/tmp

Windows:
========
set PYTHONPATH=/home/alan/workspace-python/RTL-SDR/rf-metadata-displayer/src
echo %PYTHONPATH%
python rfmetadata setting.json -vvv -ld /home/alan/tmp
Note: Check the device manager from the control panel for the port name
"""
def main()-> None:

    """
    The main function is called only when the script is executed directly,
    Execute data acquisition system using RTL-SDR devices.
    It initializes a logging manager and configures it based on command-line arguments, responsible
    for managing data flow between different components of the system.


    """
    # https://docs.python.org/3/howto/argparse.html
    parser = ArgumentParser(
        prog = "rfmetadata",
        usage="rfmetadata [-h] [-ld dir] [-v] [--version] [--author] [--report-bug] [--description] [--license] [--title] [--url]",
        description=" The gui for Radio Frequency Scanner which capture given power threshold"
    )

    parser.add_argument(
        "-ld",
        "--log_directory",
        help="store output log in a directory",
        type=str,
        metavar="dir",
    )
    parser.add_argument("-v",
                         "--verbose", help="increase output verbosity.Default to Error if not supplied, 40 is Debug", type=int, metavar="", default=0)

    parser.add_argument("--version", action="store_true", help="Display current library version")
    parser.add_argument("--author", action="store_true", help="Display author information")
    parser.add_argument("--report-bug", action="store_true", help="Library detail information to report a bug")
    parser.add_argument("--description", action="store_true", help="Display description of the package")
    parser.add_argument("--license", action="store_true", help="Display license information")
    parser.add_argument("--title", action="store_true", help="Display title of the package")
    parser.add_argument("--url", action="store_true", help="Display read the docs url of the package")

    args: Namespace = parser.parse_args()

    if args.version:
        print(f"Version: {__version__}")
        return

    if args.author:
        print(f"Author: {__author__}")
        return

    if args.report_bug:
        bug_reporting()
        return

    if args.description:
        print(f"Description: {__description__}")
        return

    if args.license:
        print(f"License: {__license__}")
        return

    if args.title:
        print(f"Title: {__title__}")
        return

    if args.url:
        print(f"URL: {__url__}")
        return

    app = QtWidgets.QApplication()

    widget = MainWindow()
    widget.show()

    sys.exit(app.exec())

# this is important so that it does not run from pytest
if __name__ == "__main__":
    main()
