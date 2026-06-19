# Agent 3 : Testeur
# Rôle : Analyser le code généré et produire des tests + rapport qualité

from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate
import os

# ============================================================
# 1. CONNEXION AU MODÈLE
# ============================================================
llm = OllamaLLM(model="mistral")

# ============================================================
# 2. PROMPTS
# ============================================================
prompt_tests = PromptTemplate(
    input_variables=["code_backend"],
    template="""
Tu es un expert en tests logiciels.
Voici le code backend Flask : {code_backend}

Génère des tests unitaires Python avec pytest pour tester :
- GET /tasks → doit retourner une liste
- POST /tasks → doit créer une tâche
- DELETE /tasks/<id> → doit supprimer une tâche
- PUT /tasks/<id> → doit mettre à jour une tâche

Utilise le client de test Flask (app.test_client()).
Réponds UNIQUEMENT avec le code Python pytest, rien d'autre.
"""
)

prompt_rapport = PromptTemplate(
    input_variables=["code_html", "code_backend"],
    template="""
Tu es un expert en qualité logicielle.
Analyse ce code :

FRONTEND : {code_html}
BACKEND : {code_backend}

Génère un rapport qualité en JSON avec cette structure :
{{
  "score_global": "..../10",
  "frontend": {{
    "points_positifs": ["..."],
    "points_negatifs": ["..."],
    "score": "..../10"
  }},
  "backend": {{
    "points_positifs": ["..."],
    "points_negatifs": ["..."],
    "score": "..../10"
  }},
  "recommandations": ["...", "...", "..."]
}}
Réponds UNIQUEMENT avec le JSON, rien d'autre.
"""
)

# ============================================================
# 3. FONCTION PRINCIPALE
# ============================================================
def tester_application() -> dict:
    print("\n🧪 Agent 3 analyse et teste l'application...")

    # Lire les fichiers générés par Agent 2
    with open("output/app/index.html", "r", encoding="utf-8") as f:
        code_html = f.read()

    with open("output/app/app.py", "r", encoding="utf-8") as f:
        code_backend = f.read()

    # Générer les tests
    print("⏳ Génération des tests unitaires...")
    chain_tests = prompt_tests | llm
    code_tests = chain_tests.invoke({"code_backend": code_backend})

    # Sauvegarder les tests
    os.makedirs("output/tests", exist_ok=True)
    with open("output/tests/test_app.py", "w", encoding="utf-8") as f:
        f.write(code_tests)

    # Générer le rapport qualité
    print("⏳ Génération du rapport qualité...")
    chain_rapport = prompt_rapport | llm
    rapport_brut = chain_rapport.invoke({
        "code_html": code_html[:2000],  # limite pour le contexte
        "code_backend": code_backend[:2000]
    })

    # Parser le rapport JSON
    import json
    try:
        debut = rapport_brut.find("{")
        fin = rapport_brut.rfind("}") + 1
        rapport = json.loads(rapport_brut[debut:fin])
    except:
        rapport = {"brut": rapport_brut}

    # Sauvegarder le rapport
    with open("output/tests/rapport_qualite.json", "w", encoding="utf-8") as f:
        json.dump(rapport, f, ensure_ascii=False, indent=2)

    print("✅ Tests et rapport générés !")
    return rapport


# ============================================================
# 4. TEST DIRECT
# ============================================================
if __name__ == "__main__":
    rapport = tester_application()
    import json
    print("\n📊 Rapport Qualité :")
    print(json.dumps(rapport, ensure_ascii=False, indent=2))