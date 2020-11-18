from flask import Flask
import sqlite3
from flask import render_template
import os
import click
from flask import current_app, g
from flask.cli import with_appcontext
from flask import request
import sys
import traceback

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

#Show the logs of the errors
def errorLog():
    print('SQLite error: %s' % (' '.join(error.args)))
    print("Exception class is: ", error.__class__)
    print('SQLite traceback: ')
    exc_type, exc_value, exc_tb = sys.exc_info()
    print(traceback.format_exception(exc_type, exc_value, exc_tb))
    return "Error"
##----------------------------------------##

####Main functions for the app####



####----------------------------------####

##-------------Routage-------------##
#Gérer les connexions et les sessions des utilisateurs
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/homePage')
def homePage():
#faire un select en prenant en compte l'id de la session courante de l'utilisateur sur la table de jonction
#et afficher les jeux de cette table où l'id de celui-ci est présent
#voir viewList
    return render_template('homePage.html')


@app.route('/viewList', methods=['GET','POST'])
def viewList():
    try:
        conn = get_db()
        userGameList = conn.execute('SELECT userName FROM user').fetchall()
    except sqlite3.Error as error:
        errorLog()
    return render_template('homePage.html', userGameList = userGameList)

@app.route('/addGame', methods=['GET','POST'])
def addGame():
    try:
        conn = get_db()
        gameList = conn.execute('SELECT * FROM game').fetchall()
        # for i in gameList:
        #     for x in i:
        #         print(x)
    except sqlite3.Error as error:
        errorLog()
    return render_template('addGame.html', gameList = gameList)

@app.route('/addG', methods=['GET','POST'])
def addG():
    #need to check if the user is logged in?
    if request.method=="POST":
        if 'add-game' in request.form:
            #userId = #getuserid
            try:
                conn = get_db()
                gameChoose = request.form
                print(gameChoose)
                conn.execute('INSERT INTO game (gameName, plateform) VALUES ("azertyuiop", "PS4")') #mettre variable
                conn.commit()
            except sqlite3.Error as error:
                errorLog()
    return render_template('addGame.html')
####----------------------------------####

app.teardown_appcontext(close_db)
app.cli.add_command(init_db_command)