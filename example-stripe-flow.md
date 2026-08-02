# Exemple de flux "Ajouter un système de paiement Stripe"

Ce document montre comment Hugo délègue à l'équipe.

## 1. Utilisateur → Hugo

> Ajoute un système de paiement Stripe sur mon site.

## 2. Hugo → Théo (Router IA)

Prompt délégué :

```text
Tâche : implémenter un système de paiement Stripe complet (backend + frontend + tests + déploiement).
Qualité requise : production-ready, sécurisé.
Budget restant aujourd'hui : 4.20 USD.
Agents concernés : paul_backend, pierre_frontend, sophie_qa, antoine_sysadmin, camille_docs.
Quel modèle recommandes-tu pour chaque agent ?
```

Réponse attendue de Théo :

```json
{
  "agent": "paul_backend",
  "task": "implémentation routes API Stripe",
  "recommended_model": "kimi/kimi-k3",
  "reason": "code sensible + intégration tierce + webhooks",
  "estimated_cost_usd": 0.35,
  "estimated_latency_ms": 3500,
  "fallback_model": "kimi/kimi-k2.7-code",
  "budget_status": "OK",
  "notes": "Backend critique : privilégier Kimi K3."
}
```

## 3. Hugo → Thomas (Product Manager)

```text
Découpe la demande "Ajouter un système de paiement Stripe" en user stories et tâches techniques.
Critères : sécurisé, testable, déployable sur notre VPS.
```

Réponse attendue de Thomas :

- User Story 1 : l'utilisateur peut payer via Stripe Checkout.
- User Story 2 : le backend reçoit et traite les webhooks Stripe.
- User Story 3 : l'administrateur peut voir l'historique des paiements.
- Tâches : backend routes, frontend page, tests, config env, docs, déploiement.

## 4. Hugo → parallel subagents (modèles validés par Théo)

```python
delegate_task(tasks=[
    {
        "goal": "Backend : créer les routes API Stripe (création session checkout, webhook events, stockage des paiements). Stack : FastAPI + PostgreSQL. Modèle : kimi/kimi-k3.",
        "context": "Le repo est à /data/workspace/mon-projet. Utilise les variables STRIPE_SECRET_KEY et STRIPE_WEBHOOK_SECRET. Demande à sysadmin de les configurer.",
        "toolsets": ["file", "terminal", "code_execution", "web"]
    },
    {
        "goal": "Frontend : créer la page de paiement Stripe Checkout avec React + Tailwind. Bouton 'Payer' redirige vers Stripe.",
        "context": "Le frontend est dans /data/workspace/mon-projet/frontend. Utilise la route POST /api/payment/create-checkout-session.",
        "toolsets": ["file", "code_execution", "web"]
    },
    {
        "goal": "QA : planifier et écrire les tests pour le paiement Stripe (succès, échec, webhook invalide).",
        "context": "Stack pytest côté backend et Vitest côté frontend. Les routes sont /api/payment/create-checkout-session et /api/webhooks/stripe.",
        "toolsets": ["file", "terminal", "code_execution"]
    },
    {
        "goal": "SysAdmin : configurer les variables d'environnement Stripe sur le VPS et préparer le déploiement.",
        "context": "VPS Ubuntu avec Docker Compose. Variables : STRIPE_PUBLISHABLE_KEY, STRIPE_SECRET_KEY, STRIPE_WEBHOOK_SECRET.",
        "toolsets": ["terminal", "file", "web"]
    },
    {
        "goal": "Docs : mettre à jour le README avec le flow Stripe, les variables d'environnement et comment tester.",
        "context": "Le README est /data/workspace/mon-projet/README.md. Demande à backend les endpoints exacts si besoin.",
        "toolsets": ["file", "web"]
    }
])
```

## 5. Hugo synthétise

Réponse à l'utilisateur :

```markdown
J'ai lancé l'implémentation Stripe avec 5 agents (modèles validés par Théo) :

- **Thomas** : a découpé la demande en 3 user stories.
- **Paul** : crée les routes checkout + webhook + stockage DB.
- **Pierre** : ajoute la page de paiement Stripe Checkout.
- **Sophie** : écrit les tests de succès/échec/webhook.
- **Antoine** : configure les variables d'env et prépare le déploiement.
- **Camille** : met à jour le README.

Prochaine étape : valider le flux de test en local avant déploiement sur le VPS.
Souhaites-tu que je lance les tests maintenant ?
```
