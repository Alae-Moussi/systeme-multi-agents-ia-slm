 Voici les tests unitaires pour la Todo App API REST en utilisant pytest et le client de test Flask :

```python
import json
from unittest.mock import patch
import pytest
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
tasks = []

def test_get_tasks():
    with app.test_client() as client:
        # Initial state (empty list)
        response = client.get('/tasks')
        assert response.status_code == 200
        data = json.loads(response.data.decode())
        assert data['tasks'] == []

        # Add a task and verify it's returned
        post_task({'title': 'Test Task'})
        response = client.get('/tasks')
        assert response.status_code == 200
        data = json.loads(response.data.decode())
        assert len(data['tasks']) == 1
        assert data['tasks'][0]['title'] == 'Test Task'

def test_post_task():
    with app.test_client() as client:
        # Invalid request (no title)
        response = client.post('/tasks', data={})
        assert response.status_code == 400
        data = json.loads(response.data.decode())
        assert data['error'] == 'Title is required'

        # Valid request
        response = client.post('/tasks', data={'title': 'Test Task'})
        assert response.status_code == 201
        data = json.loads(response.data.decode())
        assert len(tasks) == 1
        assert data['task']['id'] == 1
        assert data['task']['title'] == 'Test Task'
        assert not data['task']['completed']

def test_get_task():
    with app.test_client() as client:
        # Initial state (empty list)
        response = client.get('/tasks/1')
        assert response.status_code == 404
        data = json.loads(response.data.decode())
        assert data['error'] == 'Task not found'

        # Add a task and verify it can be fetched
        post_task({'title': 'Test Task'})
        response = client.get('/tasks/1')
        assert response.status_code == 200
        data = json.loads(response.data.decode())
        assert data['task']['id'] == 1
        assert data['task']['title'] == 'Test Task'
        assert not data['task']['completed']

def test_put_task():
    with app.test_client() as client:
        # Initial state (empty list)
        response = client.put('/tasks/1')
        assert response.status_code == 404
        data = json.loads(response.data.decode())
        assert data['error'] == 'Task not found'

        # Add a task and update it
        post_task({'title': 'Test Task'})
        updated_data = {'title': 'Updated Test Task', 'completed': True}
        with patch.object(request, 'get_json') as mock_get_json:
            mock_get_json.return_value = updated_data
            response = client.put('/tasks/1')
            assert response.status_code == 200
            data = json.loads(response.data.decode())
            assert data['task']['id'] == 1
            assert data['task']['title'] == 'Updated Test Task'
            assert data['task']['completed'] == True

def test_delete_task():
    with app.test_client() as client:
        # Initial state (empty list)
        response = client.delete('/tasks/1')
        assert response.status_code == 404
        data = json.loads(response.data.decode())
        assert data['error'] == 'Task not found'

        # Add a task and delete it
        post_task({'title': 'Test Task'})
        response = client.delete('/tasks/1')
        assert response.status_code == 200
        data = json.loads(response.data.decode())
        assert data['result'] == 'Task deleted'
        assert len(tasks) == 0

@patch('flask.request.get_json', return_value=None)
def test_invalid_post_task(mock_get_json):
    with app.test_client() as client:
        response = client.post('/tasks')
        assert response.status_code == 400
        data = json.loads(response.data.decode())
        assert data['error'] == 'Title is required'
```

Ce code contient des tests unitaires pour les différentes fonctions de l'API REST :
- `test_get_tasks()` vérifie que la fonction GET /tasks renvoie une liste
- `test_post_task()` vérifie que la fonction POST /tasks crée une tâche
- `test_get_task()` vérifie que la fonction GET /tasks/<id> renvoie une tâche spécifique ou une erreur lorsque l'ID est incorrect
- `test_put_task()` vérifie que la fonction PUT /tasks/<id> met à jour une tâche existante
- `test_delete_task()` vérifie que la fonction DELETE /tasks/<id> supprime une tâche spécifique ou renvoie une erreur lorsque l'ID est incorrect