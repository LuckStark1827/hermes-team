#!/bin/bash
# setup-teams.sh — Crée les profiles Hermes pour l'équipe multi-agents nommée
# Usage : HERMES_BIN=/chemin/vers/hermes ./setup-teams.sh

set -euo pipefail

HERMES_BIN="${HERMES_BIN:-hermes}"
if ! command -v "$HERMES_BIN" &> /dev/null; then
    echo "❌ Hermes CLI non trouvé dans le PATH."
    echo "   Définis HERMES_BIN=/chemin/vers/hermes ou ajoute hermes au PATH."
    exit 1
fi

# Liste des profiles à créer (prénom_rôle)
PROFILES=(
    hugo_orchestrator
    theo_router
    lucas_software
    pierre_frontend
    paul_backend
    antoine_sysadmin
    maxime_security
    sophie_qa
    juliette_data
    camille_docs
    emma_assistant
    louis_business
    thomas_product
    lea_marketing
    nico_monitoring
)

# Mapping fournisseur/modèle par profile (adapter les valeurs selon tes credentials)
declare -A PROVIDERS=(
    [hugo_orchestrator]=openrouter
    [theo_router]=openrouter
    [lucas_software]=openrouter
    [pierre_frontend]=openrouter
    [paul_backend]=openrouter
    [antoine_sysadmin]=openrouter
    [maxime_security]=openrouter
    [sophie_qa]=openrouter
    [juliette_data]=openrouter
    [camille_docs]=openrouter
    [emma_assistant]=openrouter
    [louis_business]=openrouter
    [thomas_product]=openrouter
    [lea_marketing]=openrouter
    [nico_monitoring]=openrouter
)

declare -A MODELS=(
    [hugo_orchestrator]=deepseek/deepseek-chat-v4-pro
    [theo_router]=kimi/kimi-k3
    [lucas_software]=kimi/kimi-k3
    [pierre_frontend]=kimi/kimi-k2.7-code
    [paul_backend]=kimi/kimi-k3
    [antoine_sysadmin]=deepseek/deepseek-chat-v4
    [maxime_security]=deepseek/deepseek-chat-v4-pro
    [sophie_qa]=kimi/kimi-k2.7-code
    [juliette_data]=kimi/kimi-k2.7-code
    [camille_docs]=deepseek/deepseek-flash
    [emma_assistant]=deepseek/deepseek-flash
    [louis_business]=kimi/kimi-k2.7-code
    [thomas_product]=deepseek/deepseek-chat-v4
    [lea_marketing]=deepseek/deepseek-flash
    [nico_monitoring]=deepseek/deepseek-flash
)

echo "🚀 Création des profiles Hermes multi-agents..."

for profile in "${PROFILES[@]}"; do
    if $HERMES_BIN profile show "$profile" &> /dev/null; then
        echo "   ⚠️  Profile '$profile' existe déjà — saut."
    else
        echo "   ➕ Création de '$profile'..."
        $HERMES_BIN profile create "$profile"
    fi

    provider="${PROVIDERS[$profile]}"
    model="${MODELS[$profile]}"
    echo "   🔧 Config provider/model : $provider / $model"
    $HERMES_BIN config set model.provider "$provider" --profile "$profile" || true
    $HERMES_BIN config set model.default "$model" --profile "$profile" || true
done

echo ""
echo "📝 Configuration des toolsets par rôle..."

configure_profile() {
    local profile=$1
    shift
    local enable_list=("$@")
    local all_toolsets=(safe web search browser terminal file code_execution vision image_gen video tts skills memory session_search delegation cronjob clarify messaging todo kanban debugging homeassistant discord discord_admin feishu_doc feishu_drive yuanbao spotify)

    for t in "${all_toolsets[@]}"; do
        $HERMES_BIN tools disable "$t" --profile "$profile" || true
    done
    for t in "${enable_list[@]}"; do
        $HERMES_BIN tools enable "$t" --profile "$profile" || true
    done
}

configure_profile hugo_orchestrator       safe delegation memory session_search
echo "   ✅ hugo_orchestrator : safe, delegation, memory, session_search"

configure_profile theo_router             memory web skills
echo "   ✅ theo_router : memory, web, skills"

configure_profile lucas_software          file terminal code_execution skills web
echo "   ✅ lucas_software : file, terminal, code_execution, skills, web"

configure_profile pierre_frontend         file code_execution web vision
echo "   ✅ pierre_frontend : file, code_execution, web, vision"

configure_profile paul_backend            file terminal code_execution web
echo "   ✅ paul_backend : file, terminal, code_execution, web"

configure_profile antoine_sysadmin        terminal file web
echo "   ✅ antoine_sysadmin : terminal, file, web"

configure_profile maxime_security         terminal web search file
echo "   ✅ maxime_security : terminal, web, search, file"

configure_profile sophie_qa               file terminal code_execution
echo "   ✅ sophie_qa : file, terminal, code_execution"

configure_profile juliette_data           terminal code_execution web
echo "   ✅ juliette_data : terminal, code_execution, web"

configure_profile camille_docs            file web memory
echo "   ✅ camille_docs : file, web, memory"

configure_profile emma_assistant          web memory session_search skills
echo "   ✅ emma_assistant : web, memory, session_search, skills"

configure_profile louis_business          web memory code_execution
echo "   ✅ louis_business : web, memory, code_execution"

configure_profile thomas_product          web memory file
echo "   ✅ thomas_product : web, memory, file"

configure_profile lea_marketing           web memory file
echo "   ✅ lea_marketing : web, memory, file"

configure_profile nico_monitoring         terminal web cronjob
echo "   ✅ nico_monitoring : terminal, web, cronjob"

echo ""
echo "📦 Installation des skills de base..."
$HERMES_BIN skills install hermes-agent --profile hugo_orchestrator || true
$HERMES_BIN skills install github-pr-workflow --profile lucas_software || true
$HERMES_BIN skills install systematic-debugging --profile lucas_software || true

echo ""
echo "🎉 Équipe multi-agents prête !"
echo "   Lancer Hugo (orchestrateur) : hermes --profile hugo_orchestrator"
echo "   Lister les profiles           : hermes profile list"
