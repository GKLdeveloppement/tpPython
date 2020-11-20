from flask import (Flask, current_app, g,
                   render_template, request,
                   redirect, url_for, session)
from flask.cli import with_appcontext
from markupsafe import escape
import sys
import os
import click
import traceback
import sqlite3

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
    return db

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')
##----------------------------------------##


####Main functions for the app####

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form.get("username")
        return redirect(url_for('homePage'))
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('homePage'))

@app.route('/homePage', methods=['GET', 'POST'])
def homePage():
    if 'username' in session:
        return render_template('homePage.html', VarUsername =session['username'])
    return 'You are not logged in'


@app.route('/viewList', methods=['GET','POST'])
def viewList():
    try:
        #Can't get the id of the user who logged in the session so we give a default value 1 for fkUser
        conn = get_db()
        userGameList = conn.execute('SELECT gameName, plateform FROM game INNER JOIN userGame ON fkGame=idGame WHERE fkUser=1').fetchall()
    except sqlite3.Error as error:
        print('SQLite error: %s' % (' '.join(error.args)))
        print("Exception class is: ", error.__class__)
        print('SQLite traceback: ')
        exc_type, exc_value, exc_tb = sys.exc_info()
        print(traceback.format_exception(exc_type, exc_value, exc_tb))
        return "Error"
    return render_template('yourList.html', userGameList = userGameList)

@app.route('/addGame', methods=['GET','POST'])
def addGame():
    try:
        conn = get_db()
        gameList = conn.execute('SELECT * FROM game').fetchall()
    except sqlite3.Error as error:
        print('SQLite error: %s' % (' '.join(error.args)))
        print("Exception class is: ", error.__class__)
        print('SQLite traceback: ')
        exc_type, exc_value, exc_tb = sys.exc_info()
        print(traceback.format_exception(exc_type, exc_value, exc_tb))
        return "Error"
    return render_template('addGame.html', gameList = gameList)

@app.route('/addG', methods=['GET','POST'])
def addG():
    session['username'] = session.get("username")
    # conn1 = get_db()
    #The query to get te id of the user who logged in the session not worked
    # idUser = conn1.execute('SELECT idUser FROM user WHERE username = (?)', (session['username'],)) #Not worked
    if request.method=="POST":
        if 'add-game' in request.form:
            try:
                conn = get_db()
                #Get user's game choice from form
                idGameChoose = request.form.get("gameList")
                #default variable for run the function addG
                idUser = 1
                #Stock both variables in a table to use it in the request as params
                reqParam = [idGameChoose, idUser]
                conn.execute('INSERT INTO userGame (fkGame, fkUser) VALUES (?, ?)',reqParam) #mettre variable
                conn.commit()
            except sqlite3.Error as error:
                #Error handle
                print('SQLite error: %s' % (' '.join(error.args)))
                print("Exception class is: ", error.__class__)
                print('SQLite traceback: ')
                exc_type, exc_value, exc_tb = sys.exc_info()
                print(traceback.format_exception(exc_type, exc_value, exc_tb))
                return "Error"
    return redirect(url_for('addGame'))
####----------------------------------####

app.teardown_appcontext(close_db)
app.cli.add_command(init_db_command)
