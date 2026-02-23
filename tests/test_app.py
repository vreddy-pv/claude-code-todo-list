import sys
import os
# Ensure the root package is on sys.path for tests
root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if root not in sys.path:
    sys.path.insert(0, root)

from mytodo import app, init_db
import pytest

@pytest.fixture
def client():
    db_path = 'todos.db'
    try:
        os.remove(db_path)
    except FileNotFoundError:
        pass
    except PermissionError:
        pass
    init_db()
    with app.test_client() as client:
        yield client
    try:
        os.remove(db_path)
    except FileNotFoundError:
        pass
    except PermissionError:
        pass
def test_add_todo(client):
    response = client.post('/add', data={'title': 'Test item'}, follow_redirects=True)
    assert response.status_code == 200
    assert b'Test item' in response.data

def test_toggle_todo(client):
    client.post('/add', data={'title': 'Toggle test'}, follow_redirects=True)
    import sqlite3
    conn = sqlite3.connect('todos.db')
    todo = conn.execute('SELECT id, completed FROM todos WHERE title = ?', ('Toggle test',)).fetchone()
    todo_id, completed = todo
    client.post(f'/toggle/{todo_id}', follow_redirects=True)
    todo = conn.execute('SELECT completed FROM todos WHERE id = ?', (todo_id,)).fetchone()
    assert todo[0] != completed
