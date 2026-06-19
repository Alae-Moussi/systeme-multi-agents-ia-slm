import json
import os
from agents.agent1_concepteur import analyser_besoin
from agents.agent2_developpeur import generer_code
from agents.agent3_testeur import tester_application
from agents.agent4_deployeur import generer_infrastructure

def executer_pipeline_multi_agents(besoin: str):
    print("🚀 DÉMARRAGE DU SYSTÈME MULTI-AGENTS 🚀")
    print("="*50)
    
    # Étape 1 : Conception
    cahier = analyser_besoin(besoin)
    
    # Étape 2 : Développement
    fichiers = generer_code(cahier)
    
    # Étape 3 : Tests & Qualité
    rapport = tester_application()
    
    # Étape 4 : DevOps & Docker
    infra = generer_infrastructure()
    
    print("="*50)
    print("🎉 PIPELINE TERMINÉ AVEC SUCCÈS !")
    print(f"L'application conteneurisée est prête dans : output/app/")

if __name__ == "__main__":
    besoin_utilisateur = "Une application web de gestion de bibliothèque pour gérer des livres"
    executer_pipeline_multi_agents(besoin_utilisateur)