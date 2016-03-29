# -*- coding: utf-8 -*-
import sqlite3
from contextlib import closing
from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash



# configuration

DEBUG = True

DATABASE = 'db/database.db'

from main import app

app.config.from_object(__name__)



def connect_db():
    """Connects to the specific database."""
    #rv = sqlite3.connect(app.config['DATABASE'])
    rv = sqlite3.connect('F:\hebjybb\db\database.db')
    rv.row_factory = sqlite3.Row
    return rv
    #return sqlite3.connect('db/database.db')

def init_db():
    """Initializes the database."""
    with app.app_context():
        db = get_db()
        with app.open_resource('db/database.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv