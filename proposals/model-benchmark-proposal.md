# 🧪 Proposition de benchmark modèles Ollama — VPS 8 Go RAM CPU only

## 🔍 Infos du VPS trouvées automatiquement

| Ressource | Valeur |
|---|---|
| IP | `93.127.213.204` |
| Port Ollama exposé | `32768` |
| Utilisateur SSH | `voyagecollab` |
| Clé SSH | `/data/workspace/vps_ssh_key.pem` |
| RAM totale | **7.8 Go** |
| RAM disponible | **6.8 Go** |
| CPU | 2 cœurs AMD EPYC |
| GPU | **Aucun** |
| Disque libre | **82 Go** |
| Ollama | Docker container `ollama-9wke-ollama-1` |
| Modèles actuellement installés | **Aucun** |

## ⚠️ Conséquence sur la sélection

Avec **8 Go RAM et CPU only**, il faut rester sur des modèles **légers et bien quantifiés** :
- Préférer les tags **Q4_K_M** ou **Q4_0**.
- Viser des modèles **≤ 9B paramètres** pour éviter le swap/OOM.
- Laisser au moins **1 Go de RAM libre** pour l'OS et Docker.

## 🎯 Liste proposée de 10 modèles (adaptée au VPS)

| # | Modèle | Tag | Taille estimée | RAM estimée | Justification |
|---|---|---|---|---|---|
| 1 | **Gemma 3** | `gemma3:4b` | ~2.5 GB | ~4-5 GB | Léger, bon en instruction, idéal pour agents simples |
| 2 | **Gemma 3** | `gemma3:12b` | ~8 GB | ~14-16 GB | ⚠️ Trop gros pour 8 Go — **à tester avec précaution** ou remplacer par `gemma3:4b-it-q8_0` |
| 3 | **Gemma 4** | `gemma4:12b` | ~8 GB | ~14-16 GB | ⚠️ Trop gros aussi — à ignorer si RAM insuffisante |
| 4 | **Mistral Small** | `mistral-small:22b` | ~14 GB | ~28-32 GB | ❌ **Trop gros** pour ce VPS |
| 5 | **DeepSeek V2** | `deepseek-v2:16b` | ~10 GB | ~20-24 GB | ❌ **Trop gros** pour ce VPS |
| 6 | **DeepSeek V3** | `deepseek-v3` | > 100 GB | ❌ **Incompatible** |
| 7 | **Qwen 2.5** | `qwen2.5:7b` | ~4.5 GB | ~8-9 GB | Excellent multilingue, rentre dans la RAM |
| 8 | **Qwen 2.5** | `qwen2.5:3b` | ~2 GB | ~4-5 GB | Très léger, bonne surprise possible |
| 9 | **Qwen 2.5 Coder** | `qwen2.5-coder:7b` | ~4.5 GB | ~8-9 GB | Si on veut tester aussi la génération de code |
| 10 | **Llama 3.1/3.2** | `llama3.2:3b` | ~2 GB | ~4-5 GB | Référence Meta, très rapide en CPU |

## 🔄 Proposition revue et réaliste pour 8 Go RAM

Compte tenu des contraintes, je te propose plutôt cette **liste de 8 modèles testables en sécurité** :

| # | Modèle | Tag | Taille estimée | RAM estimée | Objectif du test |
|---|---|---|---|---|---|
| 1 | Gemma 3 | `gemma3:4b` | ~2.5 GB | ~4-5 GB | Référence légère Google |
| 2 | Gemma 3 | `gemma3:4b-it-q8_0` | ~4 GB | ~6-7 GB | Version plus précise du 4B |
| 3 | Gemma 4 | `gemma4:4b` | ~3 GB | ~5-6 GB | Dernière génération légère (si dispo) |
| 4 | Qwen 2.5 | `qwen2.5:3b` | ~2 GB | ~4-5 GB | Très léger, multilingue |
| 5 | Qwen 2.5 | `qwen2.5:7b` | ~4.5 GB | ~8-9 GB | Référence polyvalente |
| 6 | Qwen 2.5 Coder | `qwen2.5-coder:7b` | ~4.5 GB | ~8-9 GB | Pour tâches code /
| 7 | Llama 3.2 | `llama3.2:3b` | ~2 GB | ~4-5 GB | Référence Meta rapide |
| 8 | Mistral | `mistral:7b` | ~4 GB | ~7-8 GB | Référence française classique |

> **Note** : les modèles 12B+ (Gemma 12b, Mistral Small 22b, DeepSeek V2/V3) sont théoriquement meilleurs mais **ne rentreront pas dans 8 Go RAM CPU-only** sans swap extrême. Ils ne sont donc pas proposés pour ce VPS.

## 👤 Agent le plus adapté

**Antoine** (`antoine_sysadmin`) est le meilleur agent pour ce benchmark, pas Juliette.

Pourquoi ?
- Ce benchmark est avant tout une opération **SSH + Docker + Ollama CLI + monitoring ressources**.
- Antoine a déjà les outils `terminal`, `file`, `web`.
- Je lui ai ajouté `code_execution` et `skills`.
- Son modèle est passé à `kimi-k2.7-code` pour concevoir et analyser le benchmark.
- Le skill `model-benchmarker` lui a été assigné.

Juliette reste plus pertinente pour l'analyse de données *après coup* si besoin, mais l'exécution technique du benchmark est du ressort d'Antoine.

## ✅ Validation demandée

Avant de lancer le benchmark autonome, j'ai besoin de ta validation pour :
1. **La liste des 8 modèles ci-dessus**
2. **Le prompt de test** (itinéraire Lisbonne)
3. **Le cleanup automatique** après chaque modèle (recommandé pour libérer la RAM)
4. **Le nombre de runs par modèle** (1 run rapide ou 3 runs pour moyenne ?)

Réponds par : **"OK lance"**, ou dis-moi quels modèles retirer/ajouter.

## 🛠️ Script prêt

`/data/workspace/hermes-team/scripts/model-benchmark.py`

Il détecte automatiquement le conteneur Docker Ollama, vérifie la RAM/disque, pull/test/rm chaque modèle, et génère un rapport CSV + markdown.
