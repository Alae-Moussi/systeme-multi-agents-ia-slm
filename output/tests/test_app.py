 Voici les tests unitaires pour votre application REST Flask en utilisant pytest :

```python
import pytest
from flask import Flask, request
from unittest.mock import Mock, patch
from your_app import app, students, Student

app_tester = app.test_client()

def test_list_students():
    # Tests if GET /students returns a list
    with app_tester as client:
        response = client.get('/students')
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) > 0

def test_add_student():
    # Tests if POST /students creates a student
    with app_tester as client:
        data = {'id': None, 'nom': 'Doe', 'prenom': 'John'}
        response = client.post('/students', json=data)
        assert response.status_code == 201
        created_student = Student(len(students) + 1, data['nom'], data['prenom'])
        assert students[-1] == created_student
        data = response.get_json()
        assert data == {'id': created_student.id, 'nom': created_student.nom, 'prenom': created_student.prenom}

def test_get_student():
    # Tests if GET /students/<int:id> returns the correct student
    with app_tester as client:
        first_student = Student(1, 'Doe', 'John')
        students.append(first_student)
        response = client.get(f'/students/{first_student.id}')
        assert response.status_code == 200
        data = response.get_json()
        assert data == {'id': first_student.id, 'nom': first_student.nom, 'prenom': first_student.prenom}

def test_update_student():
    # Tests if PUT /students/<int:id> updates the correct student
    with app_tester as client:
        first_student = Student(1, 'Doe', 'John')
        students.append(first_student)
        data = {'nom': 'Smith'}
        response = client.put(f'/students/{first_student.id}', json=data)
        assert response.status_code == 200
        updated_student = Student(1, data['nom'], first_student.prenom)
        assert students[-1] == updated_student
        data = response.get_json()
        assert data == {'id': updated_student.id, 'nom': updated_student.nom, 'prenom': first_student.prenom}

def test_delete_student():
    # Tests if DELETE /students/<int:id> deletes the correct student
    with app_tester as client:
        first_student = Student(1, 'Doe', 'John')
        students.append(first_student)
        response = client.delete(f'/students/{first_student.id}')
        assert response.status_code == 200
        assert first_student not in students
```

Ces tests vérifient que les différentes routes fonctionnent correctement en envoyant des requêtes HTTP simulées à votre application Flask. Ils utilisent un client de test Flask pour tester les différents cas d'utilisation de l'application, y compris la création, la récupération, la mise à jour et la suppression de données.