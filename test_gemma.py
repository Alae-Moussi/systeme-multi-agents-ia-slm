from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate
import time

# 1. On configure le modèle Gemma 2B
print("⏳ Initialisation de Gemma 2B...")
llm_gemma = OllamaLLM(model="gemma:2b")

# 2. Le prompt de test pour le cahier des charges
prompt = PromptTemplate(
    input_variables=["besoin"],
    template="""Tu es un architecte logiciel expert.
L'utilisateur veut créer : {besoin}

Génère un cahier des charges en JSON avec cette structure stricte :
{{
  "nom_projet": "...",
  "description": "...",
  "fonctionnalites": ["...", "..."]
}}
Réponds UNIQUEMENT avec le JSON, sans explications."""
)

chain = prompt | llm_gemma

# 3. Exécution du test
besoin_test = "Une application web de gestion de contacts"
print(f"🚀 Envoi du prompt à Gemma 2B pour : '{besoin_test}'...")

debut = time.time()
reponse = chain.invoke({"besoin": besoin_test})
fin = time.time()

print("\n📊 --- RÉSULTATS GEMMA 2B ---")
print(f"⏱️ Temps d'exécution : {round(fin - debut, 2)} secondes")
print("📝 Réponse générée :")
print(reponse)