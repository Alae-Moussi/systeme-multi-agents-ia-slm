# Agent 2 : Développeur
# Rôle : Lire le cahier des charges et générer le code de l'application

from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate
import json
import os

# ============================================================
# 1. CONNEXION AU MODÈLE
# ============================================================
llm = OllamaLLM(model="mistral")

# ============================================================
# 2. PROMPTS POUR CHAQUE FICHIER À GÉNÉRER
# ============================================================
prompt_html = PromptTemplate(
    input_variables=["cahier"],
    template="""
Tu es un développeur web expert.
Voici le cahier des charges : {cahier}

Génère UNIQUEMENT le code HTML complet d'une Todo App.
- Interface propre et moderne
- Formulaire pour ajouter une tâche
- Liste des tâches avec bouton supprimer et compléter
- CSS inclus dans la balise <style>
- JavaScript inclus dans la balise <script>
- Tout dans un seul fichier HTML
Réponds UNIQUEMENT avec le code HTML, rien d'autre.
"""
)

prompt_backend = PromptTemplate(
    input_variables=["cahier"],
    template="""
Tu es un développeur backend expert.
Voici le cahier des charges : {cahier}

Génère UNIQUEMENT le code Python Flask complet pour une Todo App API REST :
- GET /tasks → retourne toutes les tâches
- POST /tasks → crée une tâche
- DELETE /tasks/<id> → supprime une tâche
- PUT /tasks/<id> → met à jour une tâche
- Utilise une liste Python simple (pas de base de données)
- Inclus Flask-CORS pour connecter au frontend
Réponds UNIQUEMENT avec le code Python, rien d'autre.
"""
)

# ============================================================
# 3. FONCTION PRINCIPALE
# ============================================================
def generer_code(cahier_des_charges: dict) -> dict:
    print("\n👨‍💻 Agent 2 génère le code de l'application...")
    
    # Convertir le cahier en texte pour le prompt
    cahier_texte = json.dumps(cahier_des_charges, ensure_ascii=False)
    
    # Générer le frontend
    print("⏳ Génération du frontend (HTML/CSS/JS)...")
    chain_html = prompt_html | llm
    code_html = chain_html.invoke({"cahier": cahier_texte})
    
    # Générer le backend
    print("⏳ Génération du backend (Flask)...")
    chain_backend = prompt_backend | llm
    code_backend = chain_backend.invoke({"cahier": cahier_texte})
    
    # Sauvegarder les fichiers générés
    os.makedirs("output/app", exist_ok=True)
    
    with open("output/app/index.html", "w", encoding="utf-8") as f:
        f.write(code_html)
    
    with open("output/app/app.py", "w", encoding="utf-8") as f:
        f.write(code_backend)
    
    # Résumé
    fichiers = {
        "frontend": "output/app/index.html",
        "backend": "output/app/app.py"
    }
    
    print("✅ Code généré et sauvegardé !")
    return fichiers


# ============================================================
# 4. TEST DIRECT
# ============================================================
if __name__ == "__main__":
    # Lire le cahier des charges produit par Agent 1
    with open("output/cahier_des_charges.json", "r", encoding="utf-8") as f:
        cahier = json.load(f)
    
    print(f"📄 Cahier des charges chargé : {cahier['nom_projet']}")
    fichiers = generer_code(cahier)
    
    print("\n📁 Fichiers générés :")
    for nom, chemin in fichiers.items():
        print(f"  ✓ {nom} → {chemin}")