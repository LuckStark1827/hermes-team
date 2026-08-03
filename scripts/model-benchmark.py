#!/usr/bin/env python3
"""
model-benchmark.py — benchmark autonome de modèles Ollama locaux via Docker.

Usage:
    python3 model-benchmark.py --models gemma3:4b,qwen2.5:7b,...

Configuration par défaut pour le VPS Ollama de l'utilisateur :
    host: 93.127.213.204:32768
    ssh_user: voyagecollab
    ssh_key: /data/workspace/vps_ssh_key.pem
    ollama_container: auto-détecté
"""

import argparse
import csv
import json
import os
import re
import subprocess
import time
import urllib.request
from pathlib import Path
from typing import Optional

DEFAULT_HOST = "http://93.127.213.204:32768"
DEFAULT_SSH_USER = "voyagecollab"
DEFAULT_SSH_KEY = "/data/workspace/vps_ssh_key.pem"

PROMPT = """Tu es un assistant voyage. Un groupe de 4 amis part 5 jours à Lisbonne en octobre.
Budget total : 1 500 € hors transports.
Ils aiment : la gastronomie, les quartiers historiques, la musique live, et une excursion à la journée.
Construis un itinéraire détaillé jour par jour avec :
- horaires approximatifs,
- 2-3 lieux ou activités par jour,
- options resto midi/soir dans le budget,
- une suggestion d'excursion à la journée,
- un conseil pratique spécifique chaque jour.
Réponse en français, structurée en markdown."""


class BenchResult:
    def __init__(self, model: str):
        self.model = model
        self.installed = False
        self.pull_time_s: Optional[float] = None
        self.total_time_s: Optional[float] = None
        self.tokens_per_second: Optional[float] = None
        self.output_tokens: Optional[int] = None
        self.ram_used_mb: Optional[float] = None
        self.vram_used_mb: Optional[float] = None
        self.model_size_gb: Optional[float] = None
        self.disk_free_before_gb: Optional[float] = None
        self.disk_free_after_gb: Optional[float] = None
        self.quality_score: Optional[float] = None
        self.output_text = ""
        self.error = ""


def ssh(host: str, user: str, key: str, command: str, timeout: int = 60) -> tuple[int, str, str]:
    ssh_cmd = ["ssh", "-o", "StrictHostKeyChecking=no", "-o", "BatchMode=yes"]
    if key:
        ssh_cmd += ["-i", key]
    ssh_cmd += [f"{user}@{host}", command]
    r = subprocess.run(ssh_cmd, capture_output=True, text=True, timeout=timeout)
    return r.returncode, r.stdout, r.stderr


def get_container(host: str, user: str, key: str) -> Optional[str]:
    rc, out, _ = ssh(host, user, key,
        "docker ps --format '{{.Names}}' | grep ollama | head -1")
    name = out.strip()
    return name if name else None


def get_hardware(host: str, user: str, key: str) -> dict:
    hw = {}
    rc, out, _ = ssh(host, user, key,
        "free -m | awk '/Mem:/ {print $1,$2,$7}' && echo '---' && df -h / | awk 'NR==2 {print $4}'")
    if rc == 0:
        lines = out.splitlines()
        if lines and "Mem:" in lines[0]:
            parts = lines[0].split()
            hw["ram_total_mb"] = int(parts[1])
            hw["ram_available_mb"] = int(parts[2])
        if len(lines) > 2:
            hw["disk_free"] = lines[2].strip()
    return hw


def ollama_api(host: str, endpoint: str, payload: dict = None, timeout: int = 300) -> tuple[Optional[dict], Optional[float]]:
    url = f"{host}/api/{endpoint}"
    try:
        data = json.dumps(payload or {}).encode()
        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"}, method="POST")
        start = time.time()
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read().decode()
            elapsed = time.time() - start
            return json.loads(body), elapsed
    except Exception as e:
        print(f"[ERREUR API {endpoint}] {e}")
        return None, None


def ollama_list(host: str) -> list[str]:
    try:
        req = urllib.request.Request(f"{host}/api/tags")
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
        return [m["name"] for m in data.get("models", [])]
    except Exception as e:
        print(f"[ERREUR] Impossible de lister les modèles : {e}")
        return []


def docker_exec_pull(host: str, user: str, key: str, container: str, model: str) -> tuple[bool, float]:
    start = time.time()
    rc, out, err = ssh(host, user, key,
        f"docker exec {container} ollama pull {model}", timeout=600)
    return rc == 0, time.time() - start


def docker_exec_rm(host: str, user: str, key: str, container: str, model: str) -> None:
    ssh(host, user, key, f"docker exec {container} ollama rm {model}", timeout=60)


def get_ram(host: str, user: str, key: str) -> Optional[float]:
    rc, out, _ = ssh(host, user, key, "free -m | awk '/Mem:/ {print $3}'", timeout=10)
    try:
        return float(out.strip())
    except Exception:
        return None


def evaluate_quality(text: str) -> float:
    score = 0.0
    if "#" in text or "##" in text or "**" in text:
        score += 1.0
    for i in range(1, 6):
        if f"jour {i}" in text.lower() or f"day {i}" in text.lower():
            score += 0.2
    elements = ["restaurant", "midi", "soir", "excursion", "conseil", "horaire", "lieu", "activité"]
    for el in elements:
        if el in text.lower():
            score += 0.25
    if "€" in text or "euro" in text.lower():
        score += 0.3
    if len(text) > 800:
        score += 0.5
    return min(round(score, 2), 5.0)


def parse_size(s: str) -> Optional[float]:
    m = re.match(r"([0-9.]+)([GMTP]?)", s.upper())
    if not m:
        return None
    val, unit = float(m.group(1)), m.group(2)
    multipliers = {"": 1, "K": 1/1024/1024, "M": 1/1024, "G": 1, "T": 1024, "P": 1024*1024}
    return round(val * multipliers.get(unit, 1), 2)


def run_benchmark(host: str, models: list[str], user: str, key: str) -> list[BenchResult]:
    container = get_container(host.replace("http://", "").split(":")[0], user, key)
    if not container:
        print("[ERREUR] Conteneur Ollama introuvable")
        return []
    print(f"Conteneur Ollama : {container}")

    installed = ollama_list(host)
    print(f"Modèles déjà installés : {installed}")

    results = []
    rc, df_out, _ = ssh(host.replace("http://", "").split(":")[0], user, key,
                        "df -h / | awk 'NR==2 {print $4}'")
    disk_free_before = parse_size(df_out.strip()) if rc == 0 else None

    for model in models:
        print(f"\n{'='*60}\nBenchmark : {model}\n{'='*60}")
        res = BenchResult(model)
        res.disk_free_before_gb = disk_free_before

        # Pull if needed
        if model in installed:
            res.installed = True
            print("Déjà installé.")
        else:
            print("Téléchargement...")
            ok, pull_time = docker_exec_pull(host.replace("http://", "").split(":")[0], user, key, container, model)
            if not ok:
                res.error = "Échec du pull"
                results.append(res)
                continue
            res.pull_time_s = round(pull_time, 2)
            res.installed = True
            print(f"Pull terminé en {pull_time:.1f}s")

        # Generate
        print("Génération en cours...")
        data, elapsed = ollama_api(host, "generate", {"model": model, "prompt": PROMPT, "stream": False, "options": {"num_predict": 1024}})
        if data is None:
            res.error = "Échec de la génération"
            docker_exec_rm(host.replace("http://", "").split(":")[0], user, key, container, model)
            results.append(res)
            continue

        res.total_time_s = round(elapsed or 0, 2)
        res.output_text = data.get("response", "")
        res.output_tokens = data.get("eval_count", 0)
        if res.total_time_s and res.output_tokens:
            res.tokens_per_second = round(res.output_tokens / res.total_time_s, 2)
        res.quality_score = evaluate_quality(res.output_text)
        res.ram_used_mb = get_ram(host.replace("http://", "").split(":")[0], user, key)

        # Cleanup to free RAM for next model
        docker_exec_rm(host.replace("http://", "").split(":")[0], user, key, container, model)

        rc2, df_out2, _ = ssh(host.replace("http://", "").split(":")[0], user, key,
                              "df -h / | awk 'NR==2 {print $4}'")
        if rc2 == 0:
            res.disk_free_after_gb = parse_size(df_out2.strip())

        print(f"Tokens: {res.output_tokens}, tokens/s: {res.tokens_per_second}, qualité: {res.quality_score}/5, temps: {res.total_time_s:.1f}s")
        results.append(res)

    return results


def save_report(results: list[BenchResult], out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    csv_path = out_dir / "benchmark_results.csv"
    md_path = out_dir / "benchmark_report.md"

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["model", "installed", "pull_time_s", "total_time_s", "tokens_per_second",
                         "output_tokens", "ram_used_mb", "disk_free_before_gb", "disk_free_after_gb", "quality_score", "error"])
        for r in results:
            writer.writerow([r.model, r.installed, r.pull_time_s, r.total_time_s, r.tokens_per_second,
                             r.output_tokens, r.ram_used_mb, r.disk_free_before_gb, r.disk_free_after_gb,
                             r.quality_score, r.error])

    with open(md_path, "w", encoding="utf-8") as f:
        f.write("# 🧪 Rapport de benchmark modèles Ollama locaux\n\n")
        f.write("| Modèle | Tokens/s | Temps total | Tokens | RAM (MB) | Qualité | Erreur |\n")
        f.write("|---|---|---|---|---|---|---|\n")
        for r in results:
            f.write(f"| {r.model} | {r.tokens_per_second or '-'} | {r.total_time_s or '-'}s | {r.output_tokens or '-'} | "
                    f"{r.ram_used_mb or '-'} | {r.quality_score or '-'}/5 | {r.error or '-'} |\n")
        f.write("\n## Recommandations (score qualité × vitesse)\n\n")
        scored = [(r, (r.quality_score or 0) * (r.tokens_per_second or 0)) for r in results if r.quality_score and r.tokens_per_second]
        scored.sort(key=lambda x: x[1], reverse=True)
        for i, (r, score) in enumerate(scored[:5], 1):
            f.write(f"{i}. **{r.model}** — score = {score:.1f}, {r.tokens_per_second} tokens/s, qualité {r.quality_score}/5\n")

    print(f"\n✅ Rapport sauvegardé dans {out_dir}")


def main():
    parser = argparse.ArgumentParser(description="Benchmark de modèles Ollama locaux")
    parser.add_argument("--host", default=DEFAULT_HOST, help="URL Ollama")
    parser.add_argument("--models", required=True, help="Liste de modèles séparés par des virgules")
    parser.add_argument("--ssh-user", default=DEFAULT_SSH_USER, help="Utilisateur SSH")
    parser.add_argument("--ssh-key", default=DEFAULT_SSH_KEY, help="Clé SSH privée")
    parser.add_argument("--out", default="/data/workspace/knowledge-base/model-benchmarks", help="Dossier de sortie")
    args = parser.parse_args()

    models = [m.strip() for m in args.models.split(",") if m.strip()]
    host_ip = args.host.replace("http://", "").replace("https://", "").split(":")[0]

    hw = get_hardware(host_ip, args.ssh_user, args.ssh_key)
    print("Hardware détecté :", json.dumps(hw, indent=2, ensure_ascii=False))

    results = run_benchmark(args.host, models, args.ssh_user, args.ssh_key)
    save_report(results, Path(args.out))


if __name__ == "__main__":
    main()
