 Voici les tests unitaires PyTest pour la Todo App API REST en utilisant Flask et Flask-CORS :

```python
import sys
import json
from unittest.mock import patch
import pytest
from flask import Flask, request, jsonify, abort
from flask_cors import CORS

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
        abort(400)

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
        abort(404)

@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    data = request.get_json()
    if not data:
        abort(400)

    try:
        task = next(filter(lambda x: x['id'] == id, tasks))
    except StopIteration:
        abort(404)

    task.update(data)
    return jsonify({'task': task}), 200

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as c:
        yield c

def test_get_all_tasks(client):
    with patch.object(app, 'get_all_tasks') as mock_get_all_tasks:
        mock_get_all_tasks.return_value = jsonify({'tasks': [{'id': 1, 'title': 'test'}, {'id': 2, 'title': 'another test'}]})
        response = client.get('/tasks')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data['tasks']) == 2
        assert data['tasks'][0]['id'] == 1
        assert data['tasks'][1]['id'] == 2

def test_create_task(client):
    with patch.object(app, 'create_task') as mock_create_task:
        mock_create_task.return_value = jsonify({'task': {'id': 1, 'title': 'test', 'description': '', 'completed': False}})
        response = client.post('/tasks', data=json.dumps({'title': 'test'}))
        assert response.status_code == 201
        data = json.loads(response.data)
        assert len(tasks) == 1
        assert data['task']['id'] == 1

def test_delete_task(client):
    tasks.append({'id': 1, 'title': 'test'})
    with patch.object(app, 'delete_task') as mock_delete_task:
        mock_delete_task.return_value = '', 204
        response = client.delete('/tasks/1')
        assert response.status_code == 204
        assert len(tasks) == 0

def test_update_task(client):
    tasks.append({'id': 1, 'title': 'test', 'description': ''})
    with patch.object(app, 'update_task') as mock_update_task:
        mock_update_task.return_value = jsonify({'task': {'id': 1, 'title': 'updated test', 'description': 'new description'}})
        response = client.put('/tasks/1', data=json.dumps({'title': 'updated test', 'description': 'new description'}))
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['task']['id'] == 1
        assert data['task']['title'] == 'updated test'
        assert data['task']['description'] == 'new description'
```

Les tests s'exécutent avec la commande `pytest` dans un terminal.