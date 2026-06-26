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
Voici le cahier des charges de l'application : {cahier}

En te basant STRICTEMENT sur les fonctionnalités et le nom du projet décrits ci-dessus, génère le code HTML complet de l'interface utilisateur.
- Crée une interface propre, moderne et responsive adaptée au thème spécifique du projet.
- Intègre des formulaires, des tableaux ou des listes dynamiques pour afficher et gérer les entités décrites (ex: si c'est une gestion d'étudiants, crée des champs pour le nom, la note, etc.).
- Inclus le CSS complet directement dans la balise <style>.
- Inclus le JavaScript complet dans la balise <script> pour lier cette interface aux futurs endpoints de l'API Backend Flask.
- Tout le code frontend doit tenir dans un seul et unique fichier HTML.

Réponds UNIQUEMENT avec le code HTML propre, aucun texte d'introduction.
"""
)

prompt_backend = PromptTemplate(
    input_variables=["cahier"],
    template="""
Tu es un développeur backend expert en Python et Flask.
Voici le cahier des charges de l'application : {cahier}

En te basant STRICTEMENT sur les fonctionnalités et l'architecture décrites ci-dessus, génère le code complet d'une API REST fonctionnelle avec Flask (`app.py`).
- Crée des routes HTTP (GET, POST, PUT, DELETE) logiques et nommées d'après les entités du projet (ex: /students, /elements, /produits au lieu de /tasks).
- Utilise une structure de stockage temporaire en mémoire vive (listes ou dictionnaires Python) adaptée pour manipuler ces objets.
- Active CORS via `CORS(app)` pour que le frontend HTML puisse consommer cette API sans blocage de sécurité.
- Ne mets aucun blabla explicatif ni de délimiteurs de code markdown (comme ```python). Le fichier doit démarrer directement par l'import des modules.

Réponds UNIQUEMENT avec le code Python valide, rien d'autre.
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