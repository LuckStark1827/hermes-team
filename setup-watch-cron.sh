#!/bin/bash
# setup-watch-cron.sh — Crée les cron jobs de veille pour l'équipe multi-agents
# Usage : HERMES_BIN=/opt/venv/bin/hermes ./setup-watch-cron.sh

set -euo pipefail

HERMES_BIN="${HERMES_BIN:-/opt/venv/bin/hermes}"

echo "🕐 Création des cron jobs de veille..."

# Daily watch agents at 8:00 AM
for profile in victor_ai_research eva_tech_watch oscar_open_source sarah_security_watch coach_software_research coach_infra_research coach_llm_research; do
    job_name="watch-daily-${profile}"
    # Remove existing if any
    existing=$($HERMES_BIN cron list --all 2>/dev/null | grep "$job_name" | awk '{print $1}' || true)
    if [ -n "$existing" ]; then
        $HERMES_BIN cron remove "$existing" || true
    fi
    $HERMES_BIN cron create "0 8 * * *" \
        --name "$job_name" \
        --profile "$profile" \
        --deliver origin \
        "Tu es l'agent de veille ${profile}. Fais ton rapport quotidien structuré avec les nouveautés pertinentes, l'impact, la maturité et les recommandations. Envoie le résultat à Karl pour intégration." || true
    echo "   ✅ $job_name"
done

# Weekly watch agents (Monday 9:00 AM)
for profile in marco_market julia_legal_watch; do
    job_name="watch-weekly-${profile}"
    existing=$($HERMES_BIN cron list --all 2>/dev/null | grep "$job_name" | awk '{print $1}' || true)
    if [ -n "$existing" ]; then
        $HERMES_BIN cron remove "$existing" || true
    fi
    $HERMES_BIN cron create "0 9 * * 1" \
        --name "$job_name" \
        --profile "$profile" \
        --deliver origin \
        "Tu es l'agent de veille ${profile}. Fais ton rapport hebdomadaire structuré avec les tendances, évolutions importantes et recommandations. Envoie le résultat à Karl pour intégration." || true
    echo "   ✅ $job_name"
done

# Knowledge Curator — daily synthesis at 9:00 AM (after watch agents)
job_name="knowledge-curator-daily"
existing=$($HERMES_BIN cron list --all 2>/dev/null | grep "$job_name" | awk '{print $1}' || true)
if [ -n "$existing" ]; then
    $HERMES_BIN cron remove "$existing" || true
fi
$HERMES_BIN cron create "0 9 * * *" \
    --name "$job_name" \
    --profile karl_knowledge_curator \
    --deliver origin \
    "Tu es Karl, le Knowledge Curator. Rassemble les rapports de veille du jour (Victor, Eva, Oscar, Sarah, coaches), élimine les doublons, crée des fiches synthétiques par domaine, et mets à jour la base de connaissances /data/workspace/knowledge-base/. Produces a 5-minute morning brief." || true
echo "   ✅ $job_name"

# Knowledge Curator — weekly synthesis (Monday 10:00 AM)
job_name="knowledge-curator-weekly"
existing=$($HERMES_BIN cron list --all 2>/dev/null | grep "$job_name" | awk '{print $1}' || true)
if [ -n "$existing" ]; then
    $HERMES_BIN cron remove "$existing" || true
fi
$HERMES_BIN cron create "0 10 * * 1" \
    --name "$job_name" \
    --profile karl_knowledge_curator \
    --deliver origin \
    "Tu es Karl. Fais une synthèse hebdomadaire des veilles : tendances, outils émergents, évolutions importantes par domaine. Mets à jour la base de connaissances." || true
echo "   ✅ $job_name"

# Knowledge Curator — monthly synthesis (1st of month 9:00 AM)
job_name="knowledge-curator-monthly"
existing=$($HERMES_BIN cron list --all 2>/dev/null | grep "$job_name" | awk '{print $1}' || true)
if [ -n "$existing" ]; then
    $HERMES_BIN cron remove "$existing" || true
fi
$HERMES_BIN cron create "0 9 1 * *" \
    --name "$job_name" \
    --profile karl_knowledge_curator \
    --deliver origin \
    "Tu es Karl. Fais une synthèse mensuelle des veilles : impact sur le projet, recommandations et priorités. Produis un rapport stratégique et mets à jour la documentation interne." || true
echo "   ✅ $job_name"

echo ""
echo "🎉 Cron jobs de veille créés !"
echo "   Lister : $HERMES_BIN cron list"
