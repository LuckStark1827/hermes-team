# 🎨 Équipe UI/UX VoyageCollab — Constitution et plan d'action

## Agents mobilisés

| Agent | Rôle | Modèle | Mission dans cette refonte |
|---|---|---|---|
| **Mateo** (`mateo_ux_designer`) | UX/UI Designer | `kimi-k2.7-code` | Direction artistique, audit, maquettes, spécifications |
| **Thomas** (`thomas_product`) | Product Manager | `deepseek-v4-pro` | Priorisation, user stories, mesures de succès |
| **Pierre** (`pierre_frontend`) | Frontend Engineer | `kimi-k2.7-code` | Implémentation React/Tailwind |
| **Lucas** (`lucas_software`) | Software Engineer | `deepseek-v4-pro` | Architecture front, composants réutilisables |
| **Sophie** (`sophie_qa`) | QA Tester | `kimi-k2.6` | Tests accessibilité, responsive, parcours |
| **Maxime** (`maxime_security`) | Security Engineer | `kimi-k2.7-code` | Vérifier que la refonte n'introduit pas de failles |

## Brief pour Hugo

Hugo doit planifier la refonte UI/UX de VoyageCollab en 5 phases :

1. **Fondations design system** — Mateo + Lucas
2. **Navigation / Home / Auth** — Mateo + Pierre
3. **Dashboard + création voyage** — Pierre + Thomas + Lucas
4. **Page voyage (timeline, carte, dépenses, sondages, etc.)** — Pierre + Mateo
5. **Accessibilité + QA** — Sophie + Mateo + Maxime

## Livrables attendus

- `tailwind.config.js` avec les tokens VoyageCollab
- Composants atomiques (Button, Input, Card, Badge, Avatar, Skeleton, Toast)
- Refonte pages Home, Login, Register, Dashboard, TripPage
- Wizard d'ajout de carte en 2-3 étapes
- Drag & drop timeline
- Mobile-first responsive
- Accessibilité WCAG 2.1 AA

## Rapports déjà disponibles

- `/data/workspace/knowledge-base/voyagecollab-ux-redesign.md` — audit complet + direction artistique
- `/data/workspace/knowledge-base/model-benchmarks/benchmark_report_final.md` — benchmark modèles Ollama
