# Fournisseurs et modèles IA par agent

Chaque agent a un **provider/modèle par défaut** calibré sur la complexité de ses tâches. **Théo (theo_router)** peut réviser dynamiquement ces choix en fonction du contexte, du budget et des performances observées.

## Modèles disponibles

| Modèle | Provider | Type | Usage |
|--------|----------|------|-------|
| `kimi/kimi-k3` | OpenRouter | API | Raisonnement complexe, code, architecture |
| `kimi/kimi-k2.7-code` | OpenRouter | API | Code optimisé (frontend, QA, data, business) |
| `deepseek/deepseek-chat-v4-pro` | OpenRouter | API | Très haute complexité, orchestration, sécurité |
| `deepseek/deepseek-chat-v4` | OpenRouter | API | Complexité élevée, product, sysadmin |
| `deepseek/deepseek-flash` | OpenRouter | API | Tâches simples, rapides, peu coûteuses |
| `ollama/llama3.2` | Ollama | Local | Summaries, formatage, assistant léger |
| `ollama/qwen2.5-coder:14b` | Ollama | Local | Code simple, scripts shell |
| `ollama/deepseek-r1:8b` | Ollama | Local | Raisonnement court en local |

## Attribution par agent

| Agent | Modèle par défaut | Justification |
|-------|-------------------|---------------|
| **Hugo** (Hugo) | `deepseek/deepseek-chat-v4-pro` | Planification, délégation, synthèse de haut niveau |
| **Théo** (Router) | `kimi/kimi-k3` | Décision rapide et raisonnée sur le routing |
| **Lucas** (Software) | `kimi/kimi-k3` | Architecture, intégration, code complexe |
| **Pierre** (Frontend) | `kimi/kimi-k2.7-code` | Code frontend précis et concis |
| **Paul** (Backend) | `kimi/kimi-k3` | API, DB, logique métier |
| **Antoine** (SysAdmin) | `deepseek/deepseek-chat-v4` | Infrastructure, scripts, déploiement |
| **Maxime** (Security) | `deepseek/deepseek-chat-v4-pro` | Analyse approfondie de vulnérabilités |
| **Sophie** (QA) | `kimi/kimi-k2.7-code` | Tests unitaires, scénarios edge cases |
| **Juliette** (Data) | `kimi/kimi-k2.7-code` | Analyse de données, scripts Python |
| **Camille** (Docs) | `deepseek/deepseek-flash` | Rédaction légère, rapide |
| **Emma** (Assistant) | `deepseek/deepseek-flash` | Questions générales, recherche web |
| **Louis** (Business) | `kimi/kimi-k2.7-code` | Calculs, projections, tableaux |
| **Thomas** (Product) | `deepseek/deepseek-chat-v4` | Spécifications, priorisation |
| **Léa** (Marketing) | `deepseek/deepseek-flash` | SEO, contenu, réseaux |
| **Nico** (Monitoring) | `deepseek/deepseek-flash` | Rapports système récurrents |

## Stratégie de routing dynamique (Théo)

Théo peut choisir un modèle différent du modèle par défaut selon :

1. **Complexité** : `pro` si critique, `flash` si trivial.
2. **Budget** : forcer Ollama si le budget est faible.
3. **Latence** : privilégier les modèles rapides pour les tâches interactives.
4. **Historique** : réutiliser le modèle qui a donné les meilleurs résultats sur ce type de tâche.
5. **Disponibilité** : fallback si un provider est indisponible.

## Format de décision Théo

```json
{
  "agent": "pierre_frontend",
  "task": "Créer la page checkout Stripe",
  "default_model": "kimi/kimi-k2.7-code",
  "recommended_model": "kimi/kimi-k3",
  "reason": "Interaction tierce Stripe + state complexe",
  "estimated_cost_usd": 0.03,
  "budget_status": "OK",
  "fallback": "kimi/kimi-k2.7-code"
}
```

## Modification des modèles

Pour changer le modèle d'un agent :

```bash
hermes config set model.default kimi/kimi-k3 --profile pierre_frontend
hermes config set model.provider openrouter --profile pierre_frontend
```

Pour relancer tout le setup avec d'autres modèles, édite `setup-teams.sh` (tableau `MODELS`) puis réexécute.
