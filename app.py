from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

DATABASE = 'todos.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute(
        '''CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            completed INTEGER NOT NULL DEFAULT 0
        );'''
    )
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    conn = get_db_connection()
    todos = conn.execute('SELECT * FROM todos').fetchall()
    conn.close()
    return render_template('list.html', todos=todos)

@app.route('/add', methods=('POST',))
def add():
    title = request.form['title']
    if title:
        conn = get_db_connection()
        conn.execute('INSERT INTO todos (title, completed) VALUES (?, 0)', (title,))
        conn.commit()
        conn.close()
    return redirect(url_for('index'))

@app.route('/toggle/<int:id>', methods=('POST',))
def toggle(id):
    conn = get_db_connection()
    conn.execute('UPDATE todos SET completed = NOT completed WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>', methods=('POST',))
def delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM todos WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
