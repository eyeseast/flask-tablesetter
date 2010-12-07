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
    Start up a tornado server, using a TableSetter instance
    """
    from table_setter.app import TableSetter
    from tornado.httpserver import HTTPServer
    from tornado.ioloop import IOLoop
    from tornado.options import _LogFormatter
        
    # logging
    log_level = getattr(logging, args.logging.upper(), 'INFO')
    logger = logging.getLogger('TableSetter')
    logger.setLevel(log_level)
    handler = logging.StreamHandler()
    handler.setLevel(log_level)
    handler.setFormatter(_LogFormatter(color=False))
    logger.addHandler(handler)
    
    # create the Tornado app and spin up a server
    ts = TableSetter(args.path)
    app = ts.create_app()
    server = HTTPServer(app)
    server.listen(args.port)
    try:
        print "Spinning up a Tornado server on port %s\n" % args.port
        IOLoop.instance().start()
    except KeyboardInterrupt:
        print "\nShutting down...\n"
        IOLoop.instance().stop()

# set up the parser
parser = argparse.ArgumentParser()
subcommands = parser.add_subparsers()

# install command
install = subcommands.add_parser('install', help="Install a new table_setter directory at PATH")
install.set_defaults(func=_install)

# start command
start = subcommands.add_parser('start', help="Run table_setter on a Tornado server")
start.set_defaults(func=_start)
start.add_argument('-p', '--port', default=8888, type=int,
                   help="Listen on this port")
start.add_argument('--logging', default='INFO',
                   help="Set logging level")


# add path positional arg after subcommands
parser.add_argument('path', default='.',
                    help="Path to a table_setter directory, "
                    "or a target if creating one")

