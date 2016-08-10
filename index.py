# -*- coding: utf-8 -*-
import os
import sqlite3
from flask import Flask, render_template
from flask import g

DATABASE = os.path.dirname(__file__)+'/db/poems.db'

app = Flask(__name__)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.route('/')
def main():
    return '<a href="/authors">По автору</a>'

@app.route('/authors')
def authors():
    cur = get_db().cursor()

    all_authors = []
    for row in cur.execute("SELECT * FROM author ORDER BY name"):
        author = {
            'id':row[0],
            'name': row[1]
        }
        all_authors.append(author)
    # cc = cur.execute("SELECT * FROM author ORDER BY name")
    # all_authors = cc.fetchall()
    # cc.close()
    return render_template('authors.html', all_authors=all_authors)
    # return 'Here are list of authors'

@app.route('/author/<int:author_id>')
def show_author(author_id):
    cur = get_db().cursor()

    all_poems = []
    for row in cur.execute("SELECT * FROM poem WHERE author_id= %d ORDER BY name" % author_id):
        poem = {
            'id':row[0],
            'name': row[2]
        }
        all_poems.append(poem)
    # cc = cur.execute("SELECT * FROM author ORDER BY name")
    # all_authors = cc.fetchall()
    # cc.close()
    return render_template('author.html', all_poems=all_poems)

@app.route('/poem/<int:poem_id>')
def show_poem(poem_id):
    cur = get_db().cursor()
    cur.execute("SELECT * FROM poem WHERE id= %d" % poem_id)
    poem = cur.fetchone()
    return render_template('poem.html', name=poem[2], text=poem[3])

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

if __name__ == '__main__':
    app.run()

