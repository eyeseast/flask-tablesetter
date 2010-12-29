import argparse
import logging
import os
import shutil
import sys

parser = argparse.ArgumentParser()
parser.add_argument('path', default='.',
                    help="Path to a table_setter directory, "
                    "or a target if creating one")

subcommands = parser.add_subparsers()



def _install(args):
    """
    Create a new TableSetter instance and install template files
    in given path.
    """
    import table_setter
    root = os.path.abspath(os.path.dirname(table_setter.__file__))
    template = os.path.join(root, 'template')
    path = os.path.abspath(args.path)
    shutil.copytree(template, path)


def _start(args):
    """
    Add args.path to sys.path
    import app
    app.run()
    """
    sys.path.insert(0, args.path)
    from app import app
    app.run(args.host, args.port)
    
# set up the parser
parser = argparse.ArgumentParser()
subcommands = parser.add_subparsers()

# install command
install = subcommands.add_parser('install', help="Install a new table_setter directory at PATH")
install.set_defaults(func=_install)

# start command
start = subcommands.add_parser('start', help="Run table_setter on a Flask server")
start.set_defaults(func=_start)
start.add_argument('-b', '--host', default='127.0.0.1', dest='host',
                   help="Bind to this host")
start.add_argument('-p', '--port', default=5000, type=int, dest='port',
                   help="Listen on this port")
start.add_argument('--logging', default='INFO', dest='logging',
                   help="Set logging level")


# add path positional arg after subcommands
parser.add_argument('path', default='.',
                    help="Path to a table_setter directory, "
                    "or a target if creating one")

