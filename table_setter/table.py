"""
The Table class handles listing and getting of CSVs, and passing
those to TableFu instances.
"""
import os
import urllib2
import yaml

from table_fu import TableFu
from table_setter import TableError

class TableDoesNotExist(Exception):
    "Error for when a YAML file isn't there"

class Table(object):
    """
    A table takes an open YAML file and extracts everything necessary to make a nice HTML table.
    
    Usage::
    
    >>> table = Table(open('template/tables/example.yml'))
    >>> print(table.deck)
    <p>The financial crisis has contributed to the failure of scores of banks this year. We've put together a handy chart of the fallen banks, the federal agency that provided oversight to each one, and the major public enforcement that occurred against the bank prior to its collapse. It's all sortable state, date, or even regulatory agency.</p>
    
    The Table class also handles loading CSV files from remote URLs or the filesystem
    """
    
    def __init__(self, yml_file):
        self.yml_file = yml_file
        self.tables_dir = os.path.abspath(os.path.dirname(yml_file.name))
        self.options = yaml.load(yml_file)['table']
        
        # metadata
        self.title = self.options.get('title', '')
        self.deck = self.options.get('deck', '')
        self.footer = self.options.get('footer', '')
        self.live = self.options.get('live', False)
        self.per_page = self.options.get('per_page', 20)
        self.hard_paginate = self.options.get('hard_paginate', False)
        
        # the csv file
        self.google_key = self.options.get('google_key', None)
        self.filename = self._get_filename()
        self.url = self._get_url()
        self._data = None
    
    def __str__(self):
        return self.title
        
    @property
    def data(self):
        """
        Loading is deferred until we specifically ask for data,
        since hitting the filesystem again or pulling from a 
        remote URL is time-consuming.
        """
        if self._data is not None:
            return self._data
        else:
            self._data = self._open()
            return self._data
    
    @property
    def faceted(self):
        return self.options.has_key('faceting')

    @property
    def sortable(self):
        if self.faceted or self.hard_paginate:
            return False
        else:
            return True
    
    def _get_filename(self):
        if self.options.has_key('file'):
            f = self.options['file']
            if os.path.isfile(f):
                return os.path.abspath(f)
            elif os.path.isfile(os.path.join(self.tables_dir, f)):
                return os.path.abspath(os.path.join(self.tables_dir, f))
            else:
                return f
        else:
            return None
    
    def _get_url(self):
        if self.options.has_key('url'):
            return self.options['url']
        elif self.options.has_key('google_key'):
            return "http://spreadsheets.google.com/pub?key=%s&output=csv" % self.options['google_key']
        else:
            return None

    def _open(self):
        if self.url:
            f = urllib2.urlopen(self.url)
        elif self.filename:
            f = open(self.filename, 'rb')
        else: # there's neither a url nor a file
            raise TableError("You must specify a google_key, URL or local file containing CSV data")
        
        t = TableFu(f, **self.options.get('column_options', {}))
        if self.options.get('faceting', False):
            return t.facet_by(self.options['faceting']['facet_by'])
        return t

    @staticmethod
    def get(table_path, slug):
        """
        Get a table with a path and slug. Used in handlers.
        """
        fn = os.path.join(table_path, slug + '.yml')
        try:
            f = open(fn)
            table = Table(f)
            f.close()
            return table
        except IOError:
            raise TableDoesNotExist("No table found with slug %s in %s" % (slug, table_path))
    
    @staticmethod
    def all(table_path):
        """
        Return a dictionary mapping slugs to Table instances,
        based on a given table_path. Used in handlers.
        """
        results = {}
        yml_files = [fn for fn in os.listdir(table_path) if fn.endswith('.yml')]
        for f in yml_files:
            slug, ext = os.path.splitext(f)
            results[slug] = Table.get(table_path, slug)
        
        return results
        


