 ```python
from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

tasks = []

def get_tasks():
    return tasks

def add_task(title):
    max_id = len(tasks) if tasks else 0
    new_id = max_id + 1
    new_task = {'id': new_id, 'title': title}
    tasks.append(new_task)
    return new_task

def update_task(id, title=None):
    for task in tasks:
        if task['id'] == id:
            if title:
                task['title'] = title
            return task
    return None

def delete_task(id):
    for index, task in enumerate(tasks):
        if task['id'] == id:
            tasks.pop(index)
            return True
    return False

@app.route('/tasks', methods=['GET'])
def get_all_tasks():
    return jsonify(get_tasks())

@app.route('/tasks', methods=['POST'])
def add_new_task():
    title = request.json.get('title')
    if not title:
        return jsonify({'error': 'Title is required'}), 400
    new_task = add_task(title)
    return jsonify(new_task), 201

@app.route('/tasks/<int:id>', methods=['GET'])
def get_specific_task(id):
    task = update_task(id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    return jsonify(task), 200

@app.route('/tasks/<int:id>', methods=['PUT'])
def update_specific_task(id):
    title = request.json.get('title')
    if not title:
        return jsonify({'error': 'Title is required'}), 400
    task = update_task(id, title)
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    return jsonify(task), 200

@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_specific_task(id):
    success = delete_task(id)
    if success:
        return '', 204
    return jsonify({'error': 'Task not found'}), 404

if __name__ == "__main__":
    app.run(debug=True)
```