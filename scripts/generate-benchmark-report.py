#!/usr/bin/env python3
"""
generate-benchmark-report.py — génère le rapport visuel et écrit du benchmark.

Usage:
    python3 generate-benchmark-report.py --csv /data/workspace/knowledge-base/model-benchmarks/benchmark_results.csv
"""

import argparse
import csv
import json
import os
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


def load_csv(path: str) -> list[dict]:
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


def parse_float(v: str) -> float | None:
    try:
        return float(v) if v and v != "-" else None
    except ValueError:
        return None


def parse_int(v: str) -> int | None:
    try:
        return int(v) if v and v != "-" else None
    except ValueError:
        return None


def generate_charts(rows: list[dict], out_dir: Path) -> None:
    models = [r["model"] for r in rows if not r.get("error")]
    tokens_per_sec = [parse_float(r["tokens_per_second"]) for r in rows if not r.get("error")]
    quality = [parse_float(r["quality_score"]) for r in rows if not r.get("error")]
    total_time = [parse_float(r["total_time_s"]) for r in rows if not r.get("error")]
    ram = [parse_float(r["ram_used_mb"]) for r in rows if not r.get("error")]

    # 1. Tokens/s
    plt.figure(figsize=(10, 6))
    plt.barh(models, [v or 0 for v in tokens_per_sec], color="steelblue")
    plt.xlabel("Tokens par seconde")
    plt.title("Vitesse de génération par modèle")
    plt.tight_layout()
    plt.savefig(out_dir / "tokens_per_second.png", dpi=150)
    plt.close()

    # 2. Quality score
    plt.figure(figsize=(10, 6))
    plt.barh(models, [v or 0 for v in quality], color="seagreen")
    plt.xlabel("Score qualité / 5")
    plt.title("Qualité de l'itinéraire généré")
    plt.xlim(0, 5)
    plt.tight_layout()
    plt.savefig(out_dir / "quality_score.png", dpi=150)
    plt.close()

    # 3. Time
    plt.figure(figsize=(10, 6))
    plt.barh(models, [v or 0 for v in total_time], color="coral")
    plt.xlabel("Temps total (s)")
    plt.title("Temps de génération par modèle")
    plt.tight_layout()
    plt.savefig(out_dir / "total_time.png", dpi=150)
    plt.close()

    # 4. RAM
    plt.figure(figsize=(10, 6))
    plt.barh(models, [v or 0 for v in ram], color="mediumpurple")
    plt.xlabel("RAM utilisée (MB)")
    plt.title("Empreinte mémoire par modèle")
    plt.tight_layout()
    plt.savefig(out_dir / "ram_usage.png", dpi=150)
    plt.close()

    # 5. Scatter quality vs speed
    plt.figure(figsize=(8, 6))
    valid = [(m, t, q) for m, t, q in zip(models, tokens_per_sec, quality) if t and q]
    if valid:
        m_names, t_vals, q_vals = zip(*valid)
        plt.scatter(t_vals, q_vals, s=150, c="teal", alpha=0.7)
        for m, t, q in valid:
            plt.annotate(m, (t, q), textcoords="offset points", xytext=(5, 5), fontsize=8)
        plt.xlabel("Tokens/s")
        plt.ylabel("Qualité / 5")
        plt.title("Compromis vitesse vs qualité")
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(out_dir / "quality_vs_speed.png", dpi=150)
        plt.close()

    print(f"✅ Graphiques générés dans {out_dir}")


def generate_markdown(rows: list[dict], out_dir: Path) -> str:
    # Sort by quality*speed score
    def score(r: dict) -> float:
        t = parse_float(r.get("tokens_per_second", "")) or 0
        q = parse_float(r.get("quality_score", "")) or 0
        return t * q

    ranked = sorted(rows, key=score, reverse=True)

    md = "# 🧪 Rapport de benchmark — Modèles Ollama locaux\n\n"
    md += "## Résumé exécutif\n\n"
    md += "Ce benchmark compare 8 modèles LLM locaux sur un VPS **8 Go RAM, CPU only (2 cœurs)**.\n"
    md += "Le test consiste à générer un itinéraire de voyage à Lisbonne pour 4 amis, budget 1 500 €.\n\n"

    md += "## Tableau comparatif\n\n"
    md += "| Modèle | Tokens/s | Temps (s) | Tokens | RAM (MB) | Qualité / 5 | Erreur |\n"
    md += "|---|---|---|---|---|---|---|\n"
    for r in rows:
        md += f"| {r['model']} | {r.get('tokens_per_second','-')} | {r.get('total_time_s','-')} | " \
              f"{r.get('output_tokens','-')} | {r.get('ram_used_mb','-')} | {r.get('quality_score','-')} | {r.get('error','-')} |\n"

    md += "\n## 🏆 Classement (qualité × vitesse)\n\n"
    for i, r in enumerate(ranked[:5], 1):
        if r.get("error"):
            continue
        t = parse_float(r.get("tokens_per_second", "")) or 0
        q = parse_float(r.get("quality_score", "")) or 0
        md += f"{i}. **{r['model']}** — score {t*q:.1f}, {t} tokens/s, qualité {q}/5\n"

    md += "\n## 📊 Graphiques\n\n"
    md += f"![Tokens/s](MEDIA:{out_dir}/tokens_per_second.png)\n\n"
    md += f"![Qualité](MEDIA:{out_dir}/quality_score.png)\n\n"
    md += f"![Temps](MEDIA:{out_dir}/total_time.png)\n\n"
    md += f"![RAM](MEDIA:{out_dir}/ram_usage.png)\n\n"
    md += f"![Vitesse vs Qualité](MEDIA:{out_dir}/quality_vs_speed.png)\n\n"

    md += "\n## 🎯 Recommandations pour l'équipe Hermès\n\n"
    if ranked and not ranked[0].get("error"):
        best = ranked[0]
        md += f"- **Meilleur compromis global** : `{best['model']}`\n"
        md += "- **Agents légers** (docs, assistant, marketing, monitoring) : utiliser le modèle le plus rapide \u003e 5 tokens/s\n"
        md += "- **Agents techniques** (backend, sécurité, software) : privilégier le meilleur score qualité\n"
        md += "- **Veille quotidienne (Karl)** : choisir un modèle rapide et stable, pas forcément le plus gros\n"

    md += "\n## ⚠️ Limites du benchmark\n\n"
    md += "- Test réalisé sur CPU uniquement, pas de GPU.\n"
    md += "- Un seul prompt de test (itinéraire voyage). Les résultats peuvent varier selon la tâche.\n"
    md += "- La qualité est évaluée par heuristique automatique, pas par jugement humain.\n"

    md_path = out_dir / "benchmark_report_final.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md)

    print(f"✅ Rapport markdown généré : {md_path}")
    return str(md_path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", default="/data/workspace/knowledge-base/model-benchmarks/benchmark_results.csv", help="Fichier CSV de résultats")
    parser.add_argument("--out", default="/data/workspace/knowledge-base/model-benchmarks", help="Dossier de sortie")
    args = parser.parse_args()

    rows = load_csv(args.csv)
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    generate_charts(rows, out_dir)
    generate_markdown(rows, out_dir)

    # Save JSON for further use
    json_path = out_dir / "benchmark_results.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)
    print(f"✅ JSON exporté : {json_path}")


if __name__ == "__main__":
    main()
