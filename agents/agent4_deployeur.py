# Agent 4 : Déployeur & DevOps
# Rôle : Analyser l'application et générer la configuration Docker complète

from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate
import os

# ============================================================
# 1. CONNEXION AU MODÈLE
# ============================================================
llm = OllamaLLM(model="mistral")

# ============================================================
# 2. PROMPTS POUR L'INFRASTRUCTURE DOCKER
# ============================================================
prompt_dockerfile = PromptTemplate(
    input_variables=["code_backend"],
    template="""Tu es un ingénieur DevOps expert.
Voici le code backend de l'application Flask : {code_backend}

Génère UNIQUEMENT le fichier 'Dockerfile' pour ce backend Flask.
- Utilise une image de base Python légère (ex: python:3.10-slim)
- Configure le dossier de travail /app
- Copie les fichiers nécessaires
- Installe les dépendances requises (flask, flask-cors, gunicorn)
- Expose le port 5000
- Utilise gunicorn pour lancer l'application en production

Réponds UNIQUEMENT avec le contenu du Dockerfile, aucun texte autour, aucune balise de code markdown.
"""
)

prompt_compose = PromptTemplate(
    input_variables=["architecture"],
    template="""Tu es un architecte d'infrastructure Cloud Senior.
En te basant sur cette description d'architecture : {architecture}

Génère UNIQUEMENT le fichier 'docker-compose.yml' complet pour orchestrer l'application.
- Service 'backend' qui build le Dockerfile local, mappe le port 5000:5000
- Service 'frontend' qui utilise une image Nginx légère pour servir le fichier index.html statique, mappe le port 80:80
- Assure-toi que les volumes et la dépendance (depends_on) soient configurés proprement.

Réponds UNIQUEMENT avec le code YAML valide, aucun texte avant ou après.""")

# ============================================================
# 3. FONCTION PRINCIPALE
# ============================================================
def generer_infrastructure() -> dict:
    print("\n🐳 Agent 4 configure l'infrastructure DevOps...")
    
    # Lire le code du backend pour ajuster le Dockerfile
    with open("output/app/app.py", "r", encoding="utf-8") as f:
        code_backend = f.read()
        
    # Lire le cahier des charges pour l'architecture globale
    import json
    with open("output/cahier_des_charges.json", "r", encoding="utf-8") as f:
        cahier = json.load(f)
    architecture_texte = json.dumps(cahier.get("technique", {}))

    # 1. Génération du Dockerfile Backend
    print("⏳ Génération du Dockerfile...")
    chain_dockerfile = prompt_dockerfile | llm
    contenu_dockerfile = chain_dockerfile.invoke({"code_backend": code_backend})

    # 2. Génération du Docker Compose
    print("⏳ Génération du docker-compose.yml...")
    chain_compose = prompt_compose | llm
    contenu_compose = chain_compose.invoke({"architecture": architecture_texte})

    # Sauvegarder l'infrastructure dans le dossier de l'application
    os.makedirs("output/app", exist_ok=True)
    
    with open("output/app/Dockerfile", "w", encoding="utf-8") as f:
        f.write(contenu_dockerfile.strip())
        
    with open("output/app/docker-compose.yml", "w", encoding="utf-8") as f:
        f.write(contenu_compose.strip())

    # Générer aussi un fichier requirements.txt minimal pour le conteneur backend
    with open("output/app/requirements.txt", "w", encoding="utf-8") as f:
        f.write("flask\nflask-cors\ngunicorn\n")

    fichiers_infra = {
        "dockerfile": "output/app/Dockerfile",
        "docker_compose": "output/app/docker-compose.yml"
    }
    
    print("✅ Infrastructure Docker générée et sauvegardée avec succès !")
    return fichiers_infra

# ============================================================
# 4. TEST DIRECT
# ============================================================
if __name__ == "__main__":
    infra = generer_infrastructure()
    print("\n📁 Fichiers DevOps créés :")
    for nom, chemin in infra.items():
        print(f"  ✓ {nom} → {chemin}")