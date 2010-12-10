Python TableSetter
==================

This is a Python version (almost a port) of ProPublica's [TableSetter](http://propublica.github.com/table-setter/) project. It works with [Python TableFu](http://github.com/eyeseast/python-tablefu) to convert CSV files (including Google Spreadsheets) to styled HTML.

Install
-------

    $ python setup.py install

Or

    $ pip install -e git+git://github.com/eyeseast/flask-tablesetter.git

Installing creates the `table-setter` executable (this may change, since ProPublica's version uses the same name). Use this to create a new workspace, run the development server and build out static versions of your tables.

This isn't done, and is probably full of bugs.