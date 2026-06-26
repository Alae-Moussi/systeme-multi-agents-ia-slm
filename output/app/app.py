from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
# Configuration de CORS pour autoriser l'accès depuis ton fichier index.html local
CORS(app)

students = []

class Student:
    def __init__(self, id, nom, prenom):
        self.id = id
        self.nom = nom
        self.prenom = prenom

def get_student(id):
    for student in students:
        if student.id == id:
            return student
    return None

# Changement de /students à /etudiants pour correspondre au fichier HTML
@app.route('/etudiants', methods=['GET'])
def list_students():
    result = []
    for student in students:
        result.append({"id": student.id, "nom": student.nom, "prenom": student.prenom})
    return jsonify(result)

@app.route('/etudiants/<int:id>', methods=['GET'])
def get_student_by_id(id):
    student = get_student(id)
    if student:
        return jsonify({"id": student.id, "nom": student.nom, "prenom": student.prenom})
    else:
        return jsonify({"error": "Étudiant non trouvé."}), 404

@app.route('/etudiants', methods=['POST'])
def add_student():
    data = request.get_json()
    
    # CORRECTION : On ne vérifie plus 'id' ici, car l'ID est généré automatiquement par le serveur
    if data and 'nom' in data and 'prenom' in data:
        # Génération d'un ID unique incrémental
        next_id = len(students) + 1 if len(students) == 0 else max(s.id for s in students) + 1
        
        new_student = Student(next_id, data['nom'], data['prenom'])
        students.append(new_student)
        return jsonify({"id": new_student.id, "nom": new_student.nom, "prenom": new_student.prenom}), 201
    else:
        return jsonify({"error": "Données invalides. 'nom' et 'prenom' sont requis."}), 400

@app.route('/etudiants/<int:id>', methods=['PUT'])
def update_student(id):
    student = get_student(id)
    if student:
        data = request.get_json()
        if 'nom' in data or 'prenom' in data:
            if 'nom' in data:
                student.nom = data['nom']
            if 'prenom' in data:
                student.prenom = data['prenom']
            return jsonify({"id": student.id, "nom": student.nom, "prenom": student.prenom})
        else:
            return jsonify({"error": "Données invalides."}), 400
    else:
        return jsonify({"error": "Étudiant non trouvé."}), 404

@app.route('/etudiants/<int:id>', methods=['DELETE'])
def delete_student(id):
    student = get_student(id)
    if student:
        students.remove(student)
        return jsonify({"result": "Étudiant supprimé."})
    else:
        return jsonify({"error": "Étudiant non trouvé."}), 404

if __name__ == "__main__":
    app.run(debug=True, port=5000)