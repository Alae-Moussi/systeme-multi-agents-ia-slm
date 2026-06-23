 Voici ci-dessous le code Python Flask complet pour la Todo App API REST demandée :

```python
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

tasks = []

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})

@app.route('/tasks', methods=['POST'])
def post_task():
    data = request.get_json()

    if not data or 'title' not in data:
        response = make_response(jsonify({'error': 'Title is required'}), 400)
        response.mimetype = 'application/json'
        return response

    title = data['title']
    new_task = {'id': len(tasks) + 1, 'title': title, 'completed': False}
    tasks.append(new_task)
    response = make_response(jsonify({'task': new_task}), 201)
    response.mimetype = 'application/json'
    return response

@app.route('/tasks/<id>', methods=['GET'])
def get_task(id):
    for task in tasks:
        if task['id'] == int(id):
            return jsonify({'task': task})
    response = make_response(jsonify({'error': 'Task not found'}), 404)
    response.mimetype = 'application/json'
    return response

@app.route('/tasks/<id>', methods=['PUT'])
def put_task(id):
    for index, task in enumerate(tasks):
        if task['id'] == int(id):
            data = request.get_json()

            if 'title' in data:
                task['title'] = data['title']

            if 'completed' in data:
                task['completed'] = data['completed']

            response = make_response(jsonify({'task': task}), 200)
            response.mimetype = 'application/json'
            return response
    response = make_response(jsonify({'error': 'Task not found'}), 404)
    response.mimetype = 'application/json'
    return response

@app.route('/tasks/<id>', methods=['DELETE'])
def delete_task(id):
    for index, task in enumerate(tasks):
        if task['id'] == int(id):
            tasks.pop(index)
            response = make_response(jsonify({'result': 'Task deleted'}), 200)
            response.mimetype = 'application/json'
            return response
    response = make_response(jsonify({'error': 'Task not found'}), 404)
    response.mimetype = 'application/json'
    return response

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
```