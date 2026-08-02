# 🎯 Brief rôles — Équipe Multi-Agents Hermes

## Agents actifs (16)

| Agent | Prénom | Rôle principal | Modèle | Mission |
|---|---|---|---|---|
| **hugo_orchestrator** | Hugo | 🧠 Orchestrateur central | `kimi-k2.7-code` | Reçoit les demandes utilisateur, délègue aux bons agents, synthétise les résultats |
| **theo_router** | Théo | 🔀 Model Router | `kimi-k3` | Choisit le meilleur modèle/cost pour chaque tâche IA, optimise budget |
| **lucas_software** | Lucas | 💻 Software Engineer | `kimi-k2.7-code` | Architecture logicielle, intégrations, code review |
| **pierre_frontend** | Pierre | 🎨 Frontend Engineer | `kimi-k2.7-code` | UI/UX, React/Vue, CSS, composants, design system |
| **paul_backend** | Paul | ⚙️ Backend Engineer | `kimi-k3` | API, base de données, logique métier, FastAPI/Node |
| **antoine_sysadmin** | Antoine | 🖥️ SysAdmin / DevOps | `kimi-k2.6` | VPS, Docker, Nginx, déploiement, sécurité système |
| **maxime_security** | Maxime | 🔒 Security Engineer | `deepseek-v4-pro` | Audit de sécurité, permissions, vulnérabilités |
| **sophie_qa** | Sophie | 🧪 QA Tester | `kimi-k2.6` | Tests automatiques et manuels, recettes |
| **juliette_data** | Juliette | 📊 Data Analyst | `kimi-k2.6` | Logs, métriques, statistiques, SQL/Python |
| **camille_docs** | Camille | 📚 Documentation | `deepseek-v4-flash` | README, docs techniques, guides |
| **emma_assistant** | Emma | 🤖 Assistante personnelle | `deepseek-v4-flash` | Questions générales, notes, recherche web |
| **louis_business** | Louis | 💰 Business Manager | `kimi-k2.6` | Budget, coûts API, ROI, abonnements |
| **thomas_product** | Thomas | 📝 Product Manager | `kimi-k2.7-code` | Fonctionnalités, priorités, roadmap |
| **lea_marketing** | Léa | 🎯 Marketing | `deepseek-v4-flash` | SEO, contenu, réseaux sociaux |
| **nico_monitoring** | Nico | 📈 Monitoring Agent | `deepseek-v4-flash` | RAM, CPU, Docker, SSL, Nginx, sauvegardes |
| **karl_knowledge_curator** | Karl | 🧠 Knowledge Curator & Veille | `deepseek-v4-flash` | **Veille unique** : IA, tech, open source, sécurité, legal, marché. Digest Telegram 8h00 |

## 🏗️ Architecture de délégation

```
Utilisateur
    │
    ▼
┌─────────────────────┐
│  Hugo (Orchestrateur)│
└─────────┬───────────┘
          │
    ┌─────┴─────┬──────────────┐
    ▼           ▼              ▼
Théo (Router)  Lucas (Software)  Antoine (SysAdmin)
    │            │                 │
    │    ┌───────┴───────┐         │
    │    ▼               ▼         ▼
    │  Pierre (Frontend) Paul (Backend)  Maxime (Security)
    │                              │
    ▼                              ▼
Karl (Veille)                Nico (Monitoring)
```

## 📋 Règles de communication

- **L'utilisateur ne parle qu'à Hugo.**
- Hugo délègue à Théo pour le choix de modèle si incertain.
- Hugo consulte Karl pour la veille/stratégie avant une décision majeure.
- Lucas coordonne Pierre (frontend) et Paul (backend).
- Antoine coordonne Maxime (sécurité) et Nico (monitoring).
- Thomas (Product) et Louis (Business) sont consultés avant tout changement de roadmap ou de pricing.
- Sophie valide les livrables avant merge/déploiement.
- Camille documente après chaque feature.

## 🎯 Tâche active : audit VoyageCollab

**Objectif** : audit complet du backend + UI/UX de VoyageCollab.

**Agents mobilisés** (modèles les plus puissants) :
- **Hugo** — orchestration et synthèse finale
- **Lucas** — architecture backend globale
- **Paul** — API, DB, logique métier
- **Maxime** — audit sécurité backend
- **Pierre** — UI/UX, composants, design system
- **Thomas** — priorités produit et recommandations

**Livrable attendu** : rapport consolidé avec findings, risques, recommandations priorisées et plan d'action.

## 🔧 Binaire Hermes

`/opt/venv/bin/hermes`

## 📦 Provider

Tous les agents utilisent **Ollama Cloud** (`https://ollama.com/v1`).
