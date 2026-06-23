 Voici un exemple de code Python pour la Todo App API REST en utilisant Flask et Flask-CORS :

```python
from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

tasks = []

@app.route('/tasks', methods=['GET'])
def get_all_tasks():
    return jsonify({'tasks': tasks})

@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    if not data:
        return 'Error: No task provided.', 400

    new_task = {
        'id': len(tasks) + 1,
        'title': data['title'],
        'description': data.get('description'),
        'completed': False
    }

    tasks.append(new_task)
    return jsonify({'task': new_task}), 201

@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    global tasks
    try:
        index = tasks.index(next(filter(lambda x: x['id'] == id, tasks)))
        tasks.pop(index)
        return '', 204
    except StopIteration:
        return 'Error: Task not found.', 404

@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    data = request.get_json()
    if not data:
        return 'Error: No task provided.', 400

    try:
        task = next(filter(lambda x: x['id'] == id, tasks))
    except StopIteration:
        return 'Error: Task not found.', 404

    task.update(data)
    return jsonify({'task': task}), 200

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(port=port, debug=True)
```