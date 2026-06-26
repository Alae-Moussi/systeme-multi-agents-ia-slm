# Agent 1 : Rédacteur & Concepteur
# Rôle : Analyser le besoin utilisateur et générer un cahier des charges

from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate 
import json
import os

# ============================================================
# 1. CONNEXION AU MODÈLE (Mistral via Ollama)
# ============================================================
llm = OllamaLLM(model="mistral")

# ============================================================
# 2. LE PROMPT — c'est l'instruction qu'on donne à l'agent
# ============================================================
prompt_template = PromptTemplate(
    input_variables=["besoin_utilisateur"],
    template="""
Tu es un architecte logiciel expert. 
L'utilisateur veut créer : {besoin_utilisateur}

Génère un cahier des charges en JSON avec exactement cette structure :
{{
  "nom_projet": "...",
  "description": "...",
  "fonctionnalites": ["...", "...", "..."],
  "technique": {{
    "frontend": "...",
    "backend": "...",
    "base_de_donnees": "..."
  }},
  "architecture": "...",
  "flux_utilisateur": ["...", "...", "..."],
  "uml_diagramme": "..."
}}

CONTRAINTES CRUCIALES POUR LA SÉLECTION DES TECHNOLOGIES :
- Pour le "frontend", tu dois UNIQUEMENT utiliser : "HTML/CSS" ou "HTML/CSS/JS". Interdiction absolue d'inventer ou d'utiliser React, Angular ou Vue.
- Pour le "backend", tu dois UNIQUEMENT utiliser : "Flask". Interdiction absolue d'inventer ou d'utiliser Node.js, Express, Django ou FastAPI.

CONTRAINTE POUR L'UML :
- Dans la clé "uml_diagramme", génère une chaîne de caractères contenant le code textuel Mermaid.js complet pour un diagramme de classes (classDiagram) représentant le modèle de données et les contrôleurs de l'application (Ex: class Tache {{ +int id \n +String titre }}).

Réponds UNIQUEMENT avec le JSON, rien d'autre.
"""
)

# ============================================================
# 3. LA CHAÎNE — connecte le prompt au modèle
# ============================================================
chain = prompt_template | llm

# ============================================================
# 4. FONCTION PRINCIPALE DE L'AGENT
# ============================================================
def analyser_besoin(besoin_utilisateur: str) -> dict:
    print(f"\n🔍 Agent 1 analyse le besoin : {besoin_utilisateur}")
    print("⏳ Génération du cahier des charges...")
    
    # Appel au modèle
    resultat_brut = chain.invoke({"besoin_utilisateur": besoin_utilisateur})
    
    # Nettoyer et parser le JSON
    try:
        # Extraire uniquement la partie JSON
        debut = resultat_brut.find("{")
        fin = resultat_brut.rfind("}") + 1
        json_propre = resultat_brut[debut:fin]
        cahier_des_charges = json.loads(json_propre)
    except Exception as e:
        print(f"⚠️ Erreur parsing JSON : {e}")
        cahier_des_charges = {"erreur": str(e), "brut": resultat_brut}
    
    # Sauvegarder dans output/
    os.makedirs("output", exist_ok=True)
    with open("output/cahier_des_charges.json", "w", encoding="utf-8") as f:
        json.dump(cahier_des_charges, f, ensure_ascii=False, indent=2)
    
    print("✅ Cahier des charges généré et sauvegardé !")
    return cahier_des_charges


# ============================================================
# 5. TEST DIRECT DE L'AGENT
# ============================================================
if __name__ == "__main__":
    besoin = "une application web de gestion de tâches (Todo App)"
    resultat = analyser_besoin(besoin)
    print("\n📄 Résultat :")
    print(json.dumps(resultat, ensure_ascii=False, indent=2))