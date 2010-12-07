"""
TableSetter is a Python implementation of ProPublica's app of the same name.
It uses a similar, though more Pythonic, API. The goal of the app is to
make it easy to go from spreadsheet to interactive HTML table.
"""
__version__ = "0.1"
__author__ = "Chris Amico"

class TableError(Exception):
    "Exception class for all TableSetter modules"
