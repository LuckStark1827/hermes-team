# Équipe Multi-Agents Hermes

Cet workspace contient la configuration source de l'équipe multi-agents déployée dans Hermes.

## 🧠 Équipe de production (15 agents)

| Agent | Prénom | Rôle | Modèle | Provider |
|---|---|---|---|---|
| `hugo_orchestrator` | Hugo | Orchestrateur central | `mistralai/mistral-medium-3.5` | openrouter |
| `theo_router` | Théo | Model Router | `kimi/kimi-k2.7` | openrouter |
| `lucas_software` | Lucas | Software Engineer | `kimi/kimi-k2.7` | openrouter |
| `pierre_frontend` | Pierre | Frontend Engineer | `kimi/kimi-k2.6` | openrouter |
| `paul_backend` | Paul | Backend Engineer | `kimi/kimi-k2.7` | openrouter |
| `antoine_sysadmin` | Antoine | SysAdmin / DevOps | `kimi/kimi-k2.6` | openrouter |
| `maxime_security` | Maxime | Security Engineer | `deepseek/deepseek-chat-v4-pro` | openrouter |
| `sophie_qa` | Sophie | QA Tester | `kimi/kimi-k2.6` | openrouter |
| `juliette_data` | Juliette | Data Analyst | `kimi/kimi-k2.6` | openrouter |
| `camille_docs` | Camille | Documentation | `deepseek/deepseek-flash` | openrouter |
| `emma_assistant` | Emma | Assistant Personnel | `deepseek/deepseek-flash` | openrouter |
| `louis_business` | Louis | Business Manager | `kimi/kimi-k2.6` | openrouter |
| `thomas_product` | Thomas | Product Manager | `mistralai/mistral-medium-3.5` | openrouter |
| `lea_marketing` | Léa | Marketing | `deepseek/deepseek-flash` | openrouter |
| `nico_monitoring` | Nico | Monitoring Agent | `deepseek/deepseek-flash` | openrouter |

## 🔭 Équipe de veille (10 agents)

| Agent | Prénom | Rôle | Fréquence | Modèle |
|---|---|---|---|---|
| `victor_ai_research` | Victor | AI Research Analyst | Quotidien | `kimi/kimi-k2.6` |
| `eva_tech_watch` | Eva | Tech Watch Analyst | Quotidien | `deepseek/deepseek-flash` |
| `oscar_open_source` | Oscar | Open Source Analyst | Quotidien | `deepseek/deepseek-flash` |
| `sarah_security_watch` | Sarah | Security Watch | Quotidien | `kimi/kimi-k2.6` |
| `marco_market` | Marco | Market Analyst | Hebdomadaire | `deepseek/deepseek-flash` |
| `julia_legal_watch` | Julia | Legal Watch | Hebdomadaire | `deepseek/deepseek-flash` |
| `coach_software_research` | Coach Software | Veille métier Software | Quotidien | `kimi/kimi-k2.6` |
| `coach_infra_research` | Coach Infra | Veille métier Infra | Quotidien | `kimi/kimi-k2.6` |
| `coach_llm_research` | Coach LLM | Veille métier LLM | Quotidien | `kimi/kimi-k2.7` |
| `karl_knowledge_curator` | Karl | Knowledge Curator | Q/H/M | `glm-5.2` |

## 🕐 Livrable quotidien Telegram — 8h00

Un seul cron job consolidé déclenche tous les matins à 8h :

- **Nom** : `morning-watch-digest`
- **Agent** : `karl_knowledge_curator`
- **Script** : `~/.hermes/scripts/morning-watch-digest.py`
- **Livraison** : Telegram (`TELEGRAM_CHAT_ID`)

Le script :
1. Lance les 7 agents de veille quotidiens (Victor, Eva, Oscar, Sarah, Coach Software, Coach Infra, Coach LLM).
2. Demande à Karl de synthétiser un digest matinal de 5 minutes.
3. Envoie le digest sur Telegram.
4. Sauvegarde le digest dans `/data/workspace/knowledge-base/morning-brief-YYYY-MM-DD.md`.

## 📱 Configuration Telegram

Ajoute dans chaque `.env` de profile (en priorité `/data/profiles/karl_knowledge_curator/.env`) :

```bash
TELEGRAM_BOT_TOKEN=ton_token
TELEGRAM_CHAT_ID=ton_chat_id
```

Pour obtenir le `chat_id`, envoie `/start` à `@userinfobot` sur Telegram.

## ⚠️ Prérequis

Tous les agents utilisent **OpenRouter**. Il faut ajouter dans chaque `.env` :

```bash
OPENROUTER_API_KEY=sk-or-v1-...
```

Ou utiliser `hermes config set openrouter.api_key <key>` dans chaque profile.

## 🔧 Binaire Hermes

Le binaire est à `/opt/venv/bin/hermes`. S'il n'est pas dans le PATH, utiliser ce chemin absolu.

## 🚀 Utilisation

Parler à l'orchestrateur :

```bash
/opt/venv/bin/hermes chat --profile hugo_orchestrator
```

Lancer un agent de veille manuellement :

```bash
/opt/venv/bin/hermes chat --profile victor_ai_research "Fais ton rapport quotidien sur l'IA."
```

Lister les cron jobs :

```bash
/opt/venv/bin/hermes cron list
```

Forcer le digest du matin :

```bash
TELEGRAM_CHAT_ID=xxx TELEGRAM_BOT_TOKEN=xxx \
/opt/venv/bin/hermes cron run morning-watch-digest
```

## 📁 Fichiers importants

- `setup-teams.sh` : création des 15 agents de production
- `setup-watch-cron.sh` : ancien script de cron (remplacé par le digest consolidé)
- `scripts/morning-watch-digest.py` : script du digest Telegram
- `team-config.json` : mapping complet profile/prénom/modèle
- `profiles/*/SKILL.md` : skills personnalisés par agent
