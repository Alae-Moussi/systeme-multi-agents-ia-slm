# Comparaison Mistral 7B vs Phi-3 Mini
from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate
import time
import json

# ============================================================
# PROMPT DE TEST — même prompt pour les 2 modèles
# ============================================================
prompt = PromptTemplate(
    input_variables=["besoin"],
    template="""
Tu es un architecte logiciel expert.
L'utilisateur veut créer : {besoin}

Génère un cahier des charges en JSON avec cette structure :
{{
  "nom_projet": "...",
  "description": "...",
  "fonctionnalites": ["...", "...", "..."],
  "technique": {{
    "frontend": "...",
    "backend": "...",
    "base_de_donnees": "..."
  }}
}}
Réponds UNIQUEMENT avec le JSON.
"""
)

besoin_test = "une application web de gestion de tâches"

resultats = {}

# ============================================================
# TEST MISTRAL 7B
# ============================================================
print("\n🔵 Test Mistral 7B...")
llm_mistral = OllamaLLM(model="mistral")
chain_mistral = prompt | llm_mistral

debut = time.time()
reponse_mistral = chain_mistral.invoke({"besoin": besoin_test})
duree_mistral = round(time.time() - debut, 2)

# Compter les tokens approximatifs
tokens_mistral = len(reponse_mistral.split())

resultats["mistral"] = {
    "modele": "Mistral 7B",
    "taille": "4.4 GB",
    "duree_secondes": duree_mistral,
    "tokens_generes": tokens_mistral,
    "vitesse_tok_s": round(tokens_mistral / duree_mistral, 2),
    "reponse": reponse_mistral
}
print(f"✅ Mistral terminé en {duree_mistral}s")

# ============================================================
# TEST PHI-3 MINI
# ============================================================
print("\n🟢 Test Phi-3 Mini...")
llm_phi3 = OllamaLLM(model="phi3:mini")
chain_phi3 = prompt | llm_phi3

debut = time.time()
reponse_phi3 = chain_phi3.invoke({"besoin": besoin_test})
duree_phi3 = round(time.time() - debut, 2)

tokens_phi3 = len(reponse_phi3.split())

resultats["phi3"] = {
    "modele": "Phi-3 Mini",
    "taille": "2.3 GB",
    "duree_secondes": duree_phi3,
    "tokens_generes": tokens_phi3,
    "vitesse_tok_s": round(tokens_phi3 / duree_phi3, 2),
    "reponse": reponse_phi3
}
print(f"✅ Phi-3 Mini terminé en {duree_phi3}s")

# ============================================================
# RAPPORT DE COMPARAISON
# ============================================================
print("\n" + "="*50)
print("📊 RAPPORT DE COMPARAISON")
print("="*50)

for nom, data in resultats.items():
    print(f"\n🔹 {data['modele']}")
    print(f"   Taille      : {data['taille']}")
    print(f"   Durée       : {data['duree_secondes']} secondes")
    print(f"   Tokens      : {data['tokens_generes']}")
    print(f"   Vitesse     : {data['vitesse_tok_s']} tok/s")

print("\n" + "="*50)
vitesse_ratio = round(resultats['phi3']['duree_secondes'] / resultats['mistral']['duree_secondes'] * 100)
print(f"⚡ Phi-3 Mini est {100 - vitesse_ratio}% plus rapide que Mistral 7B")
print(f"📦 Phi-3 Mini est {round(4.4/2.3, 1)}x plus léger que Mistral 7B")
print("="*50)

# Sauvegarder le rapport
with open("output/comparaison_modeles.json", "w", encoding="utf-8") as f:
    json.dump(resultats, f, ensure_ascii=False, indent=2)

print("\n✅ Rapport sauvegardé dans output/comparaison_modeles.json")