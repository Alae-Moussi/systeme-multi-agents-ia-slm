import streamlit as st
import json
import time
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
    st.markdown("**Orchestration :** LangChain")
    st.divider()

    # Progression visuelle
    st.header("🔄 Progression")
    etapes = ["Agent 1", "Validation", "Agent 2", "Agent 3", "Agent 4"]
    for i, nom in enumerate(etapes):
        if i < st.session_state.etape:
            st.success(f"✅ {nom}")
        elif i == st.session_state.etape:
            st.info(f"⏳ {nom}")
        else:
            st.text(f"⬜ {nom}")

    # Bouton reset
    st.divider()
    if st.button("🔄 Recommencer", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# ============================================================
# TITRE
# ============================================================
st.title("🤖 Système Multi-Agents IA")
st.markdown("### Génération automatique d'applications web")
st.divider()

# ============================================================
# ETAPE 0 — SAISIE DU BESOIN
# ============================================================
if st.session_state.etape == 0:
    st.subheader("💬 Décris ton application")
    besoin = st.text_area(
        "Que veux-tu créer ?",
        placeholder="Ex: Une application web de gestion de tâches avec priorités",
        height=100
    )
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🚀 Lancer Agent 1", use_container_width=True):
            if besoin:
                with st.spinner("Agent 1 analyse le besoin..."):
                    debut = time.time()
                    cahier = analyser_besoin(besoin)
                    st.session_state.duree1 = round(time.time() - debut, 2)
                    st.session_state.cahier = cahier
                    st.session_state.etape = 1
                st.rerun()
            else:
                st.warning("⚠️ Décris ton application d'abord !")

# ============================================================
# ETAPE 1 — HUMAN IN THE LOOP : VALIDATION DU CAHIER DES CHARGES
# ============================================================
elif st.session_state.etape == 1:
    st.subheader("🔍 Agent 1 — Concepteur")
    st.success(f"✅ Cahier des charges généré en {st.session_state.duree1} secondes")
    
    st.divider()
    
    # HUMAN IN THE LOOP
    st.subheader("👤 Validation Humaine — Human-in-the-Loop")
    st.info("📋 Vérifiez et modifiez le cahier des charges avant de continuer")
    
    cahier_json = json.dumps(st.session_state.cahier, ensure_ascii=False, indent=2)
    cahier_modifie = st.text_area(
        "Cahier des charges (modifiable) :",
        value=cahier_json,
        height=350
    )
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Valider et continuer", use_container_width=True):
            try:
                cahier_valide = json.loads(cahier_modifie)
                st.session_state.cahier = cahier_valide
                # Sauvegarder la version validée
                import os
                os.makedirs("output", exist_ok=True)
                with open("output/cahier_des_charges.json", "w", encoding="utf-8") as f:
                    json.dump(cahier_valide, f, ensure_ascii=False, indent=2)
                st.session_state.etape = 2
                st.rerun()
            except json.JSONDecodeError:
                st.error("❌ JSON invalide ! Corrigez la syntaxe avant de valider.")
    with col2:
        if st.button("🔄 Régénérer Agent 1", use_container_width=True):
            st.session_state.etape = 0
            st.rerun()

# ============================================================
# ETAPE 2 — AGENT 2 DEVELOPPEUR
# ============================================================
elif st.session_state.etape == 2:
    st.subheader("🔍 Agent 1 — Concepteur")
    st.success(f"✅ Cahier des charges validé en {st.session_state.duree1} secondes")

    st.divider()
    st.subheader("👨‍💻 Agent 2 — Développeur")
    with st.spinner("Génération du code en cours... (1-2 min)"):
        debut = time.time()
        generer_code(st.session_state.cahier)
        st.session_state.duree2 = round(time.time() - debut, 2)
        st.session_state.etape = 3
    st.rerun()

# ============================================================
# ETAPE 3 — AGENT 3 TESTEUR
# ============================================================
elif st.session_state.etape == 3:
    st.subheader("🔍 Agent 1 ✅")
    st.success(f"Cahier des charges validé en {st.session_state.duree1}s")
    st.subheader("👨‍💻 Agent 2 ✅")
    st.success(f"Code généré en {st.session_state.duree2}s")

    col1, col2 = st.columns(2)
    with col1:
        with st.expander("🌐 Voir le code HTML"):
            with open("output/app/index.html", "r", encoding="utf-8") as f:
                st.code(f.read(), language="html")
    with col2:
        with st.expander("🐍 Voir le code Flask"):
            with open("output/app/app.py", "r", encoding="utf-8") as f:
                st.code(f.read(), language="python")

    st.divider()
    st.subheader("🧪 Agent 3 — Testeur")
    with st.spinner("Génération des tests..."):
        debut = time.time()
        rapport = tester_application()
        st.session_state.duree3 = round(time.time() - debut, 2)
        st.session_state.etape = 4
    st.rerun()

# ============================================================
# ETAPE 4 — AGENT 4 DEPLOYEUR
# ============================================================
elif st.session_state.etape == 4:
    st.subheader("🔍 Agent 1 ✅ | 👨‍💻 Agent 2 ✅ | 🧪 Agent 3 ✅")
    st.success(f"Tests générés en {st.session_state.duree3}s")

    st.divider()
    st.subheader("🐳 Agent 4 — Déployeur")
    with st.spinner("Génération de l'infrastructure Docker..."):
        debut = time.time()
        generer_infrastructure()
        st.session_state.duree4 = round(time.time() - debut, 2)
        st.session_state.etape = 5
    st.rerun()

# ============================================================
# ETAPE 5 — RÉSULTAT FINAL
# ============================================================
elif st.session_state.etape == 5:
    st.subheader("🎉 Pipeline Terminé avec Human-in-the-Loop !")
    
    total = round(
        st.session_state.duree1 + st.session_state.duree2 +
        st.session_state.duree3 + st.session_state.duree4, 2
    )
    
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Agent 1", f"{st.session_state.duree1}s")
    col2.metric("Agent 2", f"{st.session_state.duree2}s")
    col3.metric("Agent 3", f"{st.session_state.duree3}s")
    col4.metric("Agent 4", f"{st.session_state.duree4}s")
    col5.metric("⏱️ Total", f"{total}s")

    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        with st.expander("🐳 Voir le Dockerfile"):
            with open("output/app/Dockerfile", "r", encoding="utf-8") as f:
                st.code(f.read(), language="docker")
    with col2:
        with st.expander("⚙️ Voir docker-compose.yml"):
            with open("output/app/docker-compose.yml", "r", encoding="utf-8") as f:
                st.code(f.read(), language="yaml")

    st.info("📁 Tous les fichiers sont dans le dossier output/")