 Voici un exemple de code Python Flask complet pour une API REST Todo App :

```python
from flask import Flask, request, jsonify, make_response, abort
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

tasks = []

# GET /tasks → retourne toutes les tâches
@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})

# POST /tasks → crée une tâche
@app.route('/tasks', methods=['POST'])
def post_task():
    data = request.get_json()
    if not data or 'title' not in data:
        abort(400, description="Title is missing.")

    task = {'id': len(tasks) + 1, 'title': data['title'], 'completed': False}
    tasks.append(task)
    return make_response(jsonify({'task': task}), 201)

# DELETE /tasks/<id> → supprime une tâche
@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    for task in tasks:
        if task['id'] == id:
            tasks.remove(task)
            return make_response(jsonify({'result': 'success'}), 200)
    abort(404, description="Task not found.")

# PUT /tasks/<id> → met à jour une tâche
@app.route('/tasks/<int:id>', methods=['PUT'])
def put_task(id):
    data = request.get_json()

    for task in tasks:
        if task['id'] == id:
            if 'title' in data:
                task['title'] = data['title']
            if 'completed' in data:
                task['completed'] = data['completed']
            return make_response(jsonify({'task': task}), 200)
    abort(404, description="Task not found.")

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
```