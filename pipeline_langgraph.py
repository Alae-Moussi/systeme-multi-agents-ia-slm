# Pipeline Multi-Agents avec LangGraph
# Remplace le pipeline linéaire simple par un graphe d'état

from langgraph.graph import StateGraph, END
from typing import TypedDict, Optional
from agents.agent1_concepteur import analyser_besoin
from agents.agent2_developpeur import generer_code
from agents.agent3_testeur import tester_application
from agents.agent4_deployeur import generer_infrastructure
import json

# ============================================================
# 1. DÉFINIR L'ÉTAT PARTAGÉ ENTRE LES AGENTS
# C'est la mémoire commune de tout le système
# ============================================================
class EtatSysteme(TypedDict):
    besoin_utilisateur: str
    cahier_des_charges: Optional[dict]
    fichiers_generes: Optional[dict]
    rapport_tests: Optional[dict]
    infrastructure: Optional[dict]
    erreurs: Optional[list]
    etape_actuelle: str

# ============================================================
# 2. DÉFINIR LES NOEUDS DU GRAPHE (chaque agent = un noeud)
# ============================================================

def noeud_agent1(etat: EtatSysteme) -> EtatSysteme:
    """Noeud Agent 1 — Concepteur"""
    print("\n🔵 [LangGraph] Agent 1 — Concepteur")
    try:
        cahier = analyser_besoin(etat["besoin_utilisateur"])
        return {
            **etat,
            "cahier_des_charges": cahier,
            "etape_actuelle": "agent1_complete",
            "erreurs": []
        }
    except Exception as e:
        return {
            **etat,
            "erreurs": [f"Agent 1 erreur: {str(e)}"],
            "etape_actuelle": "erreur"
        }

def noeud_agent2(etat: EtatSysteme) -> EtatSysteme:
    """Noeud Agent 2 — Développeur"""
    print("\n🟢 [LangGraph] Agent 2 — Développeur")
    try:
        fichiers = generer_code(etat["cahier_des_charges"])
        return {
            **etat,
            "fichiers_generes": fichiers,
            "etape_actuelle": "agent2_complete"
        }
    except Exception as e:
        return {
            **etat,
            "erreurs": etat.get("erreurs", []) + [f"Agent 2 erreur: {str(e)}"],
            "etape_actuelle": "erreur"
        }

def noeud_agent3(etat: EtatSysteme) -> EtatSysteme:
    """Noeud Agent 3 — Testeur"""
    print("\n🟡 [LangGraph] Agent 3 — Testeur")
    try:
        rapport = tester_application()
        return {
            **etat,
            "rapport_tests": rapport,
            "etape_actuelle": "agent3_complete"
        }
    except Exception as e:
        return {
            **etat,
            "erreurs": etat.get("erreurs", []) + [f"Agent 3 erreur: {str(e)}"],
            "etape_actuelle": "erreur"
        }

def noeud_agent4(etat: EtatSysteme) -> EtatSysteme:
    """Noeud Agent 4 — Déployeur"""
    print("\n🔴 [LangGraph] Agent 4 — Déployeur")
    try:
        infra = generer_infrastructure()
        return {
            **etat,
            "infrastructure": infra,
            "etape_actuelle": "pipeline_complete"
        }
    except Exception as e:
        return {
            **etat,
            "erreurs": etat.get("erreurs", []) + [f"Agent 4 erreur: {str(e)}"],
            "etape_actuelle": "erreur"
        }

# ============================================================
# 3. LOGIQUE DE ROUTAGE — décide quel agent appeler ensuite
# ============================================================
def router(etat: EtatSysteme) -> str:
    """Décide la prochaine étape selon l'état actuel"""
    etape = etat.get("etape_actuelle", "")
    erreurs = etat.get("erreurs", [])

    # Si erreur → fin du pipeline
    if etape == "erreur" or erreurs:
        print(f"\n❌ Erreur détectée : {erreurs}")
        return END

    # Routing normal
    if etape == "agent1_complete":
        return "agent2"
    elif etape == "agent2_complete":
        return "agent3"
    elif etape == "agent3_complete":
        return "agent4"
    elif etape == "pipeline_complete":
        return END
    else:
        return END

# ============================================================
# 4. CONSTRUIRE LE GRAPHE
# ============================================================
def construire_graphe():
    """Construit et compile le graphe LangGraph"""
    
    graphe = StateGraph(EtatSysteme)

    # Ajouter les noeuds
    graphe.add_node("agent1", noeud_agent1)
    graphe.add_node("agent2", noeud_agent2)
    graphe.add_node("agent3", noeud_agent3)
    graphe.add_node("agent4", noeud_agent4)

    # Point d'entrée
    graphe.set_entry_point("agent1")

    # Ajouter les edges conditionnels
    graphe.add_conditional_edges("agent1", router)
    graphe.add_conditional_edges("agent2", router)
    graphe.add_conditional_edges("agent3", router)
    graphe.add_conditional_edges("agent4", router)

    return graphe.compile()

# ============================================================
# 5. LANCER LE PIPELINE
# ============================================================
def executer_pipeline_langgraph(besoin: str):
    print("🚀 DÉMARRAGE PIPELINE LANGGRAPH")
    print("="*50)

    # État initial
    etat_initial = {
        "besoin_utilisateur": besoin,
        "cahier_des_charges": None,
        "fichiers_generes": None,
        "rapport_tests": None,
        "infrastructure": None,
        "erreurs": [],
        "etape_actuelle": "debut"
    }

    # Construire et exécuter le graphe
    app = construire_graphe()
    etat_final = app.invoke(etat_initial)

    print("\n" + "="*50)
    if etat_final.get("etape_actuelle") == "pipeline_complete":
        print("🎉 PIPELINE LANGGRAPH TERMINÉ AVEC SUCCÈS !")
        print(f"✅ Projet : {etat_final['cahier_des_charges'].get('nom_projet', 'N/A')}")
    else:
        print("❌ Pipeline terminé avec erreurs :")
        for err in etat_final.get("erreurs", []):
            print(f"   - {err}")

    return etat_final

if __name__ == "__main__":
    besoin = "Une application web de gestion de contacts"
    executer_pipeline_langgraph(besoin)# Pipeline Multi-Agents avec LangGraph
# Remplace le pipeline linéaire simple par un graphe d'état

from langgraph.graph import StateGraph, END
from typing import TypedDict, Optional
from agents.agent1_concepteur import analyser_besoin
from agents.agent2_developpeur import generer_code
from agents.agent3_testeur import tester_application
from agents.agent4_deployeur import generer_infrastructure
import json

# ============================================================
# 1. DÉFINIR L'ÉTAT PARTAGÉ ENTRE LES AGENTS
# C'est la mémoire commune de tout le système
# ============================================================
class EtatSysteme(TypedDict):
    besoin_utilisateur: str
    cahier_des_charges: Optional[dict]
    fichiers_generes: Optional[dict]
    rapport_tests: Optional[dict]
    infrastructure: Optional[dict]
    erreurs: Optional[list]
    etape_actuelle: str

# ============================================================
# 2. DÉFINIR LES NOEUDS DU GRAPHE (chaque agent = un noeud)
# ============================================================

def noeud_agent1(etat: EtatSysteme) -> EtatSysteme:
    """Noeud Agent 1 — Concepteur"""
    print("\n🔵 [LangGraph] Agent 1 — Concepteur")
    try:
        cahier = analyser_besoin(etat["besoin_utilisateur"])
        return {
            **etat,
            "cahier_des_charges": cahier,
            "etape_actuelle": "agent1_complete",
            "erreurs": []
        }
    except Exception as e:
        return {
            **etat,
            "erreurs": [f"Agent 1 erreur: {str(e)}"],
            "etape_actuelle": "erreur"
        }

def noeud_agent2(etat: EtatSysteme) -> EtatSysteme:
    """Noeud Agent 2 — Développeur"""
    print("\n🟢 [LangGraph] Agent 2 — Développeur")
    try:
        fichiers = generer_code(etat["cahier_des_charges"])
        return {
            **etat,
            "fichiers_generes": fichiers,
            "etape_actuelle": "agent2_complete"
        }
    except Exception as e:
        return {
            **etat,
            "erreurs": etat.get("erreurs", []) + [f"Agent 2 erreur: {str(e)}"],
            "etape_actuelle": "erreur"
        }

def noeud_agent3(etat: EtatSysteme) -> EtatSysteme:
    """Noeud Agent 3 — Testeur"""
    print("\n🟡 [LangGraph] Agent 3 — Testeur")
    try:
        rapport = tester_application()
        return {
            **etat,
            "rapport_tests": rapport,
            "etape_actuelle": "agent3_complete"
        }
    except Exception as e:
        return {
            **etat,
            "erreurs": etat.get("erreurs", []) + [f"Agent 3 erreur: {str(e)}"],
            "etape_actuelle": "erreur"
        }

def noeud_agent4(etat: EtatSysteme) -> EtatSysteme:
    """Noeud Agent 4 — Déployeur"""
    print("\n🔴 [LangGraph] Agent 4 — Déployeur")
    try:
        infra = generer_infrastructure()
        return {
            **etat,
            "infrastructure": infra,
            "etape_actuelle": "pipeline_complete"
        }
    except Exception as e:
        return {
            **etat,
            "erreurs": etat.get("erreurs", []) + [f"Agent 4 erreur: {str(e)}"],
            "etape_actuelle": "erreur"
        }

# ============================================================
# 3. LOGIQUE DE ROUTAGE — décide quel agent appeler ensuite
# ============================================================
def router(etat: EtatSysteme) -> str:
    """Décide la prochaine étape selon l'état actuel"""
    etape = etat.get("etape_actuelle", "")
    erreurs = etat.get("erreurs", [])

    # Si erreur → fin du pipeline
    if etape == "erreur" or erreurs:
        print(f"\n❌ Erreur détectée : {erreurs}")
        return END

    # Routing normal
    if etape == "agent1_complete":
        return "agent2"
    elif etape == "agent2_complete":
        return "agent3"
    elif etape == "agent3_complete":
        return "agent4"
    elif etape == "pipeline_complete":
        return END
    else:
        return END

# ============================================================
# 4. CONSTRUIRE LE GRAPHE
# ============================================================
def construire_graphe():
    """Construit et compile le graphe LangGraph"""
    
    graphe = StateGraph(EtatSysteme)

    # Ajouter les noeuds
    graphe.add_node("agent1", noeud_agent1)
    graphe.add_node("agent2", noeud_agent2)
    graphe.add_node("agent3", noeud_agent3)
    graphe.add_node("agent4", noeud_agent4)

    # Point d'entrée
    graphe.set_entry_point("agent1")

    # Ajouter les edges conditionnels
    graphe.add_conditional_edges("agent1", router)
    graphe.add_conditional_edges("agent2", router)
    graphe.add_conditional_edges("agent3", router)
    graphe.add_conditional_edges("agent4", router)

    return graphe.compile()

# ============================================================
# 5. LANCER LE PIPELINE
# ============================================================
def executer_pipeline_langgraph(besoin: str):
    print("🚀 DÉMARRAGE PIPELINE LANGGRAPH")
    print("="*50)

    # État initial
    etat_initial = {
        "besoin_utilisateur": besoin,
        "cahier_des_charges": None,
        "fichiers_generes": None,
        "rapport_tests": None,
        "infrastructure": None,
        "erreurs": [],
        "etape_actuelle": "debut"
    }

    # Construire et exécuter le graphe
    app = construire_graphe()
    etat_final = app.invoke(etat_initial)

    print("\n" + "="*50)
    if etat_final.get("etape_actuelle") == "pipeline_complete":
        print("🎉 PIPELINE LANGGRAPH TERMINÉ AVEC SUCCÈS !")
        print(f"✅ Projet : {etat_final['cahier_des_charges'].get('nom_projet', 'N/A')}")
    else:
        print("❌ Pipeline terminé avec erreurs :")
        for err in etat_final.get("erreurs", []):
            print(f"   - {err}")

    return etat_final

if __name__ == "__main__":
    besoin = "Une application web de gestion de contacts"
    executer_pipeline_langgraph(besoin)