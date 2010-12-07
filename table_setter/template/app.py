from flask import abort, Flask
from table_setter.table import Table, TableDoesNotExist

app = Flask(__name__)
app.debug = True

@app.route('/')
def index():
    tables = Table.all('tables')
    return render_template('index.html', tables=tables)

@app.route('/<slug>')
def table(slug):
    try:
        table = Table.get('tables', slug)
    except TableDoesNotExist:
        abort(404)
    
    return render_template('table.html', table=table)

if __name__ == "__main__":
    app.run()