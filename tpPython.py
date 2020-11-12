from flask import Flask
import sqlite3
from flask import render_template
import os
import click
from flask import current_app, g
from flask.cli import with_appcontext

app = Flask(__name__, static_folder="./templates")

app.secret_key = b'tartiflette69latrick'

##Function for the connection to the database##
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            os.path.join(app.instance_path, 'tp.db'),
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db
##------------------------------------------##

##Function to close the database instance##
def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()
##----------------------------------------##

#Functions to initialize the database
def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')
##----------------------------------------##

####Main functions for the app####



####----------------------------------####

##-------------Routage-------------##
@app.route('/login')
def login():
    return render_template('index.html')

@app.route('/homePage')
def homePage():
    return render_template('mainPage.html')

####----------------------------------####

app.teardown_appcontext(close_db)
app.cli.add_command(init_db_command)