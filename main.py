from flask import Flask, render_template, request, redirect
import os
import sqlite3

app = Flask(__name__)
VERSION = "v0.1"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, 'tasks.db')

def init_db():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            due_date DATE NOT NULL,
            completed INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return redirect('/todolist')

@app.route('/todolist')
def todolist():
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()
    cursor.execute("SELECT id, content, due_date, completed FROM tasks")
    tasks = cursor.fetchall()
    connection.close()
    return render_template('index.html', tasks=tasks, version=VERSION)

@app.route('/add', methods=['POST'])
def add_task():
    content = request.form['content']
    due_date = request.form['due_date']

    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()
    cursor.execute("INSERT INTO tasks (content, due_date) VALUES (?, ?)", (content, due_date))
    connection.commit()
    connection.close()
    return redirect('/todolist')

@app.route('/delete/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()
    try:
        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        connection.commit()
    except Exception as e:
        print(f"Error deleting task: {e}")
        return "An error occurred while deleting the task.", 500
    finally:
        connection.close()
        return "", 204

if __name__ == '__main__':
    init_db()
    app.run(debug=True)