from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

# File to save tasks
DATA_FILE = 'tasks.json'

def load_tasks():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    with open(DATA_FILE, 'w') as f:
        json.dump(tasks, f)

tasks = load_tasks()

@app.route('/')
def index():
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add():
    task_text = request.form.get('task')
    if task_text:
        tasks.append({
            "id": len(tasks) + 1, 
            "task": task_text, 
            "done": False
        })
        save_tasks(tasks)
    return redirect(url_for('index'))

@app.route('/done/<int:task_id>')
def done(task_id):
    for task in tasks:
        if task['id'] == task_id:
            task['done'] = not task['done']
            break
    save_tasks(tasks)
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
def delete(task_id):
    global tasks
    tasks = [task for task in tasks if task['id'] != task_id]
    save_tasks(tasks)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)