# 🤖 Système Multi-Agents IA pour le Développement Automatisé d'Applications Web

## 📋 Description
Système basé sur une approche **Agentic AI** utilisant **LangChain** et **Mistral 7B** (Small Language Model),
capable d'automatiser les différentes phases du développement d'une application web
à travers une collaboration entre 4 agents intelligents.

## 🏗️ Architecture du Système
```
Entrée Utilisateur (texte)
         ↓
 [Agent 1 - Concepteur]  → cahier_des_charges.json
         ↓
 [Agent 2 - Développeur] → index.html + app.py
         ↓
 [Agent 3 - Testeur]     → test_app.py + rapport_qualite.json
         ↓
 [Agent 4 - Déployeur]   → Dockerfile + docker-compose.yml
```

## 🤖 Les 4 Agents

### Agent 1 — Rédacteur & Concepteur
- **Entrée** : Besoin utilisateur en texte libre
- **Sortie** : `output/cahier_des_charges.json`
- **Rôle** : Analyse le besoin et génère un cahier des charges structuré

### Agent 2 — Développeur
- **Entrée** : `output/cahier_des_charges.json`
- **Sortie** : `output/app/index.html` + `output/app/app.py`
- **Rôle** : Génère le code frontend (HTML/CSS/JS) et backend (Flask)

### Agent 3 — Testeur
- **Entrée** : `output/app/index.html` + `output/app/app.py`
- **Sortie** : `output/tests/test_app.py` + `output/tests/rapport_qualite.json`
- **Rôle** : Génère les tests unitaires et le rapport qualité

### Agent 4 — Déployeur
- **Entrée** : `output/app/app.py` + `output/cahier_des_charges.json`
- **Sortie** : `output/app/Dockerfile` + `output/app/docker-compose.yml`
- **Rôle** : Génère l'infrastructure Docker pour le déploiement

## 🛠️ Technologies Utilisées
- **Orchestration** : LangChain + LangChain-Ollama
- **Small LLM** : Mistral 7B (via Ollama)
- **Interface** : Streamlit
- **Backend généré** : Flask (Python)
- **Frontend généré** : HTML5 + CSS3 + JavaScript
- **DevOps généré** : Docker + docker-compose

## 🚀 Installation et Lancement

### Prérequis
- Python 3.10+
- [Ollama](https://ollama.com) installé

### Étapes
```bash
# 1. Cloner le projet
git clone https://github.com/Alae-Moussi/systeme-multi-agents-ia-slm.git
cd systeme-multi-agents-ia-slm

# 2. Créer l'environnement virtuel
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# 3. Installer les dépendances
pip install langchain langchain-ollama langchain-core streamlit

# 4. Télécharger le modèle Mistral
ollama pull mistral

# 5. Lancer l'interface
streamlit run app_streamlit.py
```

## 📁 Structure du Projet
```
multi_agents_project/
├── agents/
│   ├── agent1_concepteur.py
│   ├── agent2_developpeur.py
│   ├── agent3_testeur.py
│   └── agent4_deployeur.py
├── output/
│   ├── cahier_des_charges.json
│   ├── app/
│   │   ├── index.html
│   │   ├── app.py
│   │   ├── Dockerfile
│   │   └── docker-compose.yml
│   └── tests/
│       ├── test_app.py
│       └── rapport_qualite.json
├── app_streamlit.py
├── main.py
└── README.md
```

## 📊 Performances Observées (Mistral 7B sur CPU)
| Agent | Temps moyen |
|-------|-------------|
| Agent 1 — Concepteur | ~145 secondes |
| Agent 2 — Développeur | ~782 secondes |
| Agent 3 — Testeur | ~1299 secondes |
| Agent 4 — Déployeur | ~403 secondes |
| **Total pipeline** | **~2629 secondes** |

## ⚠️ Limites et Améliorations
- Mistral 7B sur CPU est lent → GPU dédié ou modèle plus petit recommandé
- Le JSON généré peut parfois être mal formaté → parsing robuste ajouté
- Pas de mémoire persistante entre sessions

## 👤 Auteur
**Alae Moussi** — Projet académique IA Générative & Systèmes Multi-Agents