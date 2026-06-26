import streamlit as st
import json
import time
import os
from agents.agent1_concepteur import analyser_besoin
from agents.agent2_developpeur import generer_code
from agents.agent3_testeur import tester_application
from agents.agent4_deployeur import generer_infrastructure

st.set_page_config(
    page_title="Système Multi-Agents IA",
    page_icon="🤖",
    layout="wide"
)

# ============================================================
# INITIALISATION SESSION STATE
# ============================================================
if "etape" not in st.session_state:
    st.session_state.etape = 0
if "besoin" not in st.session_state:
    st.session_state.besoin = ""
if "cahier" not in st.session_state:
    st.session_state.cahier = None
if "duree1" not in st.session_state:
    st.session_state.duree1 = 0
if "duree2" not in st.session_state:
    st.session_state.duree2 = 0
if "duree3" not in st.session_state:
    st.session_state.duree3 = 0
if "duree4" not in st.session_state:
    st.session_state.duree4 = 0

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.header("📋 Les 4 Agents")
    st.markdown("""
    **Agent 1 — Concepteur**
    Analyse le besoin et génère le cahier des charges
    
    **Agent 2 — Développeur**
    Génère le code HTML + Flask
    
    **Agent 3 — Testeur**
    Génère les tests et le rapport qualité
    
    **Agent 4 — Déployeur**
    Génère le Dockerfile et docker-compose
    """)
    st.divider()
    st.markdown("**Modèle IA :** Mistral 7B")
    st.markdown("**Orchestration :** Graphe d'État")
    st.divider()

    # Progression visuelle
    st.header("🔄 Progression")
    etapes_noms = ["Saisie", "Agent 1", "Validation", "Agent 2", "Agent 3", "Agent 4", "Terminé"]
    for i, nom in enumerate(etapes_noms):
        if i < st.session_state.etape:
            st.success(f"✅ {nom}")
        elif i == st.session_state.etape:
            st.info(f"⏳ {nom}")
        else:
            st.text(f"⬜ {nom}")

    # Bouton reset
    st.divider()
    if st.button("🔄 Recommencer à zéro", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# ============================================================
# TITRE PRINCIPAL
# ============================================================
st.title("🤖 Plateforme Multi-Agents IA — Vue Globale")
st.markdown("### Suivi complet et affichage cumulé du pipeline de développement")
st.divider()

# ============================================================
# BLOC 0 — SAISIE DU BESOIN (Toujours visible au début)
# ============================================================
st.subheader("💬 Étape 1 : Expression du besoin utilisateur")
if st.session_state.etape == 0:
    besoin_saisi = st.text_area(
        "Que veux-tu créer ?",
        placeholder="Ex: Une application web de gestion de tâches avec priorités",
        height=100
    )
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🚀 Lancer le Pipeline d'Agents", use_container_width=True):
            if besoin_saisi:
                st.session_state.besoin = besoin_saisi
                st.session_state.etape = 1
                st.rerun()
            else:
                st.warning("⚠️ Décris ton application d'abord !")
else:
    st.info(f"**Besoin traité :** {st.session_state.besoin}")

# ============================================================
# BLOC 1 — EXÉCUTION AGENT 1
# ============================================================
if st.session_state.etape == 1:
    with st.spinner("🧠 Agent 1 (Concepteur) analyse le besoin et structure le JSON..."):
        debut = time.time()
        cahier = analyser_besoin(st.session_state.besoin)
        st.session_state.duree1 = round(time.time() - debut, 2)
        st.session_state.cahier = cahier
        st.session_state.etape = 2
    st.rerun()

# Affichage de l'Agent 1 dès qu'il a travaillé (Reste visible jusqu'à la fin)
if st.session_state.etape >= 2:
    st.divider()
    st.subheader(f"📋 Agent 1 — Concepteur (Traité en {st.session_state.duree1}s)")
    
    # Mode Validation Humaine (HITL) uniquement à l'étape 2
    if st.session_state.etape == 2:
        st.warning("👤 Human-in-the-Loop : Vous pouvez modifier le cahier des charges ci-dessous avant de générer le code.")
        cahier_json = json.dumps(st.session_state.cahier, ensure_ascii=False, indent=2)
        cahier_modifie = st.text_area("Spécifications JSON modifiables :", value=cahier_json, height=250)
        
        if st.button("✅ Valider le cahier des charges et lancer l'Agent 2", use_container_width=True):
            try:
                st.session_state.cahier = json.loads(cahier_modifie)
                os.makedirs("output", exist_ok=True)
                with open("output/cahier_des_charges.json", "w", encoding="utf-8") as f:
                    json.dump(st.session_state.cahier, f, ensure_ascii=False, indent=2)
                st.session_state.etape = 3
                st.rerun()
            except json.JSONDecodeError:
                st.error("❌ Structure JSON invalide ! Vérifiez vos modifications.")
    else:
        # Affichage simple pour le reste du pipeline
        with st.expander("🔍 Voir le Cahier des Charges Spécifié (JSON)"):
            st.json(st.session_state.cahier)

# ============================================================
# BLOC 2 — EXÉCUTION AGENT 2
# ============================================================
if st.session_state.etape == 3:
    with st.spinner("👨‍💻 Agent 2 (Développeur) génère le code Flask et HTML..."):
        debut = time.time()
        generer_code(st.session_state.cahier)
        st.session_state.duree2 = round(time.time() - debut, 2)
        st.session_state.etape = 4
    st.rerun()

# Affichage de l'Agent 2 dès qu'il a travaillé (Reste visible)
if st.session_state.etape >= 4:
    st.divider()
    st.subheader(f"👨‍💻 Agent 2 — Développeur (Traité en {st.session_state.duree2}s)")
    col1, col2 = st.columns(2)
    with col1:
        with st.expander("🌐 Voir le code Frontend (index.html)"):
            with open("output/app/index.html", "r", encoding="utf-8") as f:
                st.code(f.read(), language="html")
    with col2:
        with st.expander("🐍 Voir le code Backend API (app.py)"):
            with open("output/app/app.py", "r", encoding="utf-8") as f:
                st.code(f.read(), language="python")

# ============================================================
# BLOC 3 — EXÉCUTION AGENT 3
# ============================================================
if st.session_state.etape == 4:
    with st.spinner("🧪 Agent 3 (Testeur) écrit les scripts de tests unitaires..."):
        debut = time.time()
        tester_application()
        st.session_state.duree3 = round(time.time() - debut, 2)
        st.session_state.etape = 5
    st.rerun()

# Affichage de l'Agent 3 dès qu'il a travaillé (Reste visible)
if st.session_state.etape >= 5:
    st.divider()
    st.subheader(f"🧪 Agent 3 — Assurance Qualité & Testeur (Traité en {st.session_state.duree3}s)")
    col1, col2 = st.columns(2)
    with col1:
        with st.expander("📝 Scripts de tests unitaires (test_app.py)"):
            if os.path.exists("output/tests/test_app.py"):
                with open("output/tests/test_app.py", "r", encoding="utf-8") as f:
                    st.code(f.read(), language="python")
    with col2:
        with st.expander("📊 Rapport de conformité syntaxique"):
            if os.path.exists("output/tests/rapport_qualite.json"):
                with open("output/tests/rapport_qualite.json", "r", encoding="utf-8") as f:
                    st.json(json.load(f))

# ============================================================
# BLOC 4 — EXÉCUTION AGENT 4
# ============================================================
if st.session_state.etape == 5:
    with st.spinner("🐳 Agent 4 (Déployeur) prépare l'environnement Docker..."):
        debut = time.time()
        generer_infrastructure()
        st.session_state.duree4 = round(time.time() - debut, 2)
        st.session_state.etape = 6
    st.rerun()

# Affichage de l'Agent 4 et écran de livraison final !
if st.session_state.etape >= 6:
    st.divider()
    st.subheader(f"🐳 Agent 4 — Déployeur Infrastructure (Traité en {st.session_state.duree4}s)")
    col1, col2 = st.columns(2)
    with col1:
        with st.expander("🐳 Recette de conteneurisation (Dockerfile)"):
            with open("output/app/Dockerfile", "r", encoding="utf-8") as f:
                st.code(f.read(), language="docker")
    with col2:
        with st.expander("⚙️ Architecture multi-services (docker-compose.yml)"):
            with open("output/app/docker-compose.yml", "r", encoding="utf-8") as f:
                st.code(f.read(), language="yaml")

    # Grand panneau final tout en bas de la page
    st.divider()
    st.balloons()
    st.success("🎉 PIPELINE MULTI-AGENTS ENTIÈREMENT EXÉCUTÉ ET LIVRÉ !")
    
    total = round(st.session_state.duree1 + st.session_state.duree2 + st.session_state.duree3 + st.session_state.duree4, 2)
    st.metric(label="⏱️ Temps de calcul cumulé total (Inférence locale CPU)", value=f"{total} secondes (~{round(total/60, 1)} minutes)")