import os
import tornado.httpserver
import tornado.ioloop
import tornado.web

from table_setter.table import Table, TableDoesNotExist


class TableSetter(object):
    """
    A TableSetter instance contains an entire app, pointing to
    table files (in YAML), templates and static files.
    """
    def __init__(self, path, **options):
        self.configure(path)
    
    def create_app(self, handlers=None, default_host="", transforms=None, wsgi=False, **settings):
        """
        Return an instance of tornado.web.Application, using settings from TableSetter
        """
        settings = self.settings(**settings)
        if not handlers:
            handlers = urls
        else:
            handlers =+ urls
        return tornado.web.Application(handlers, default_host, transforms, wsgi, **settings)
    
    def configure(self, path):
        self.project_dir = os.path.abspath(path)
        self.tables_dir = os.path.abspath(os.path.join(self.project_dir, 'tables'))
        self.static_dir = os.path.abspath(os.path.join(self.project_dir, 'static'))
        self.templates_dir = os.path.abspath(os.path.join(self.project_dir, 'templates'))        
    
    def settings(self, **kwargs):
        "Return a settings dictionary that can be used in a Tornado application"
        settings_dict = {
            'table_path': self.tables_dir,
            'template_path': self.templates_dir,
            'static_path': self.static_dir,
        }
        settings_dict.update(kwargs)
        return settings_dict


class IndexHandler(tornado.web.RequestHandler):
    """
    Builds an index of public tables based on yaml files
    in the table directory.
    
    Must be included in an application with 'table_path' setting
    defined, otherwise YAML lookup will fail.
    """
    def get(self):
        tables = Table.all(self.settings['table_path'])
        self.render('index.html', tables=tables)
        

class TableHandler(tornado.web.RequestHandler):
    """
    Built a single table, given a slug
    """
    def get(self, slug):
        try:
            table = Table.get(self.settings['table_path'], slug)
        except TableDoesNotExist:
            raise tornado.web.HTTPError(404)
        

urls = [
    (r'/', IndexHandler),
    (r'/([-\w]+)/?', TableHandler),
]
