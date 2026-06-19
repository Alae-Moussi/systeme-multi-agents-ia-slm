 Voici les tests unitaires pour le code Flask en utilisant Pytest :

```python
import os
from unittest.mock import patch
import pytest
from flask import Flask
from flask_cors import CORS
from application import app, tasks

def create_app():
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    return app

@pytest.fixture(scope='module')
def client():
    app = create_app()
    with app.test_client() as testing_client:
        yield testing_client

def test_get_all_tasks():
    # Ajout de tâches pour les tests suivants
    add_task('Test 1')
    add_task('Test 2')

    with client as c:
        response = c.get('/tasks')
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 2
        assert data[0]['id'] == 1 and data[1]['id'] == 2

def test_add_new_task():
    with client as c:
        response = c.post('/tasks', json={'title': 'Test 3'})
        assert response.status_code == 201
        data = response.get_json()
        assert len(data) == 1 and data['id'] > 2

def test_get_specific_task():
    add_task('Test 4')

    with client as c:
        response = c.get('/tasks/1')  # Vérifie que le premier élément de la liste peut être récupéré
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 1 and data['id'] == 1

def test_update_specific_task():
    add_task('Test 5')

    with client as c:
        response = c.put('/tasks/1', json={'title': 'Updated Test'})
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 1 and data['id'] == 1 and data['title'] == 'Updated Test'

def test_delete_specific_task():
    add_task('Test 6')

    with client as c:
        response = c.delete('/tasks/1')  # Vérifie que la première tâche peut être supprimée
        assert response.status_code == 204
        tasks_after_deletion = [task for task in tasks if task['id'] != 1]
        assert len(tasks_after_deletion) == 5 and 'Test 6' in [task['title'] for task in tasks_after_deletion]

@patch('os.getenv')
def test_app_runs(mock_getenv):
    mock_getenv.return_value = 'test'
    with app.test_client() as c:
        c.get('/')  # Vérifie que l'application se lance correctement lors du test
```

Il est important d'ajouter la fonction `create_app()` pour permettre à Pytest de créer une instance de l'application Flask spécifique aux tests. Dans cette fonction, on active le mode de test (TESTING) et désactive CSRF pour permettre les requêtes POST, PUT et DELETE.

Le client de test Flask est utilisé avec la fonction `client()` dans chaque test pour exécuter des requêtes HTTP vers l'application.