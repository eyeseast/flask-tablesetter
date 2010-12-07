#!/usr/bin/env python
"""
This module contains settings and basic files needed to run a table_setter instance.
"""
import os
from table_setter.app import TableSetter, urls

settings = {
    'debug': True
}

ts = TableSetter(os.getcwd())
application = ts.create_app(**settings)