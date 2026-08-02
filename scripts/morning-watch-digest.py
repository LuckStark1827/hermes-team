#!/usr/bin/env python3
"""
morning-watch-digest.py — version directe Ollama + sources web

1. Collecte des actualités depuis des sources rapides (Hacker News, arXiv, GitHub trending).
2. Appelle directement l'API Ollama Cloud pour synthétiser un digest.
3. Envoie le digest sur Telegram à 8h00.
"""

import os
import sys
import json
import datetime
import urllib.request
import urllib.parse
import textwrap

OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "https://ollama.com/v1")
OLLAMA_API_KEY = os.environ.get("OLLAMA_API_KEY")
OLLAMA_API_KEY = os.environ.get("OLLAMA_API_KEY")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "deepseek-v4-flash")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")


def ollama_chat(prompt: str) -> str:
    """Call Ollama chat completions API directly."""
    if not OLLAMA_API_KEY:
        return "⚠️ OLLAMA_API_KEY manquant."
    url = f"{OLLAMA_BASE_URL}/chat/completions"
    payload = {
        "model": OLLAMA_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3,
        "max_tokens": 2500,
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={
        "Authorization": f"Bearer {OLLAMA_API_KEY}",
        "Content-Type": "application/json",
    }, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            result = json.loads(resp.read())
            return result["choices"][0]["message"]["content"]
    except Exception as e:
        return f"⚠️ Erreur Ollama API: {e}"


def fetch_hackernews() -> str:
    """Fetch top stories from Hacker News and filter recent/popular tech stories."""
    try:
        req = urllib.request.Request(
            "https://hn.algolia.com/api/v1/search_by_date?query=AI+LLM+security+open+source&tags=story&hitsPerPage=20"
        )
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read())
        hits = data.get("hits", [])
        lines = ["🔥 Hacker News — stories tech/AI:"]
        for h in hits[:10]:
            title = h.get("title", "no title")
            url = h.get("url") or f"https://news.ycombinator.com/item?id={h.get('objectID')}"
            lines.append(f"- {title} ({url})")
        return "\n".join(lines)
    except Exception as e:
        return f"⚠️ HN fetch error: {e}"


def fetch_arxiv() -> str:
    """Fetch recent AI papers from arXiv."""
    try:
        today = datetime.date.today()
        three_days_ago = today - datetime.timedelta(days=3)
        query = urllib.parse.quote("cat:cs.AI OR cat:cs.LG OR cat:cs.CL")
        url = (
            f"http://export.arxiv.org/api/query?search_query={query}"
            f"&start=0&max_results=10&sortBy=submittedDate&sortOrder=descending"
        )
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=20) as resp:
            xml = resp.read().decode("utf-8")
        import re
        entries = re.findall(r"<entry>(.*?)</entry>", xml, re.DOTALL)
        lines = ["🧠 arXiv — papiers récents cs.AI/LG/CL:"]
        for entry in entries[:5]:
            title = re.search(r"<title>(.*?)</title>", entry, re.DOTALL)
            link = re.search(r"<id>(.*?)</id>", entry, re.DOTALL)
            summary = re.search(r"<summary>(.*?)</summary>", entry, re.DOTALL)
            title = title.group(1).replace("\n", " ").strip() if title else "no title"
            link = link.group(1).strip() if link else ""
            summary_text = summary.group(1).replace("\n", " ").strip()[:200] + "..." if summary else ""
            lines.append(f"- {title} ({link})")
            if summary_text:
                lines.append(f"  {summary_text}")
        return "\n".join(lines)
    except Exception as e:
        return f"⚠️ arXiv fetch error: {e}"


def fetch_github_trending() -> str:
    """Fetch trending repos from GitHub (use search for last created)."""
    try:
        week_ago = (datetime.date.today() - datetime.timedelta(days=7)).isoformat()
        query = urllib.parse.quote(f"created:>{week_ago} stars:>50 language:python OR language:typescript")
        url = f"https://api.github.com/search/repositories?q={query}&sort=stars&order=desc&per_page=10"
        req = urllib.request.Request(url, headers={"Accept": "application/vnd.github.v3+json"})
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read())
        items = data.get("items", [])
        lines = ["🔥 GitHub — projets trending récents:"]
        for item in items[:7]:
            name = item.get("full_name", "")
            desc = item.get("description") or ""
            url_repo = item.get("html_url", "")
            stars = item.get("stargazers_count", 0)
            lines.append(f"- {name} ⭐{stars} ({url_repo})")
            if desc:
                lines.append(f"  {desc}")
        return "\n".join(lines)
    except Exception as e:
        return f"⚠️ GitHub fetch error: {e}"


def send_telegram(message: str) -> bool:
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID not set; skipping Telegram send.", file=sys.stderr)
        return False
    chunks = textwrap.wrap(message, width=4000, break_long_words=False, replace_whitespace=False)
    for i, chunk in enumerate(chunks):
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": chunk,
            "parse_mode": "Markdown",
            "disable_web_page_preview": True,
        }
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        try:
            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"}, method="POST")
            with urllib.request.urlopen(req, timeout=30) as resp:
                resp.read()
            print(f"Telegram chunk {i+1}/{len(chunks)} sent.", file=sys.stderr)
        except Exception as e:
            print(f"Telegram send failed: {e}", file=sys.stderr)
            return False
    return True


def main():
    today = datetime.date.today().isoformat()
    print(f"[{datetime.datetime.now().isoformat()}] Collecting watch sources...", file=sys.stderr)
    sources = [
        fetch_arxiv(),
        fetch_hackernews(),
        fetch_github_trending(),
    ]
    raw_sources = "\n\n".join(sources)

    prompt = f"""Tu es Karl, le Knowledge Curator. Voici des sources brutes de veille du jour.
Synthétise-les en un **digest matinal** de 5 minutes de lecture.

{raw_sources}

Format obligatoire :
- Titre : 🌅 Digest de veille — {today}
- 5 à 8 points clés maximum
- Pour chaque point : titre, résumé (2-3 phrases), impact (🔴/🟡/🟢), maturité (expérimental/stable/production), recommandation (adopter/tester/surveiller/ignorer)
- Section finale "⚡ Actions prioritaires du jour" avec les 3 recommandations les plus importantes
- Mentionne les agents concernés (Lucas, Paul, Antoine, Hugo, etc.) quand pertinent

Sois factuel, concis et actionnable."""

    print(f"[{datetime.datetime.now().isoformat()}] Calling Ollama {OLLAMA_MODEL}...", file=sys.stderr)
    digest = ollama_chat(prompt)

    kb_path = "/data/workspace/knowledge-base"
    os.makedirs(kb_path, exist_ok=True)
    digest_file = os.path.join(kb_path, f"morning-brief-{today}.md")
    with open(digest_file, "w", encoding="utf-8") as f:
        f.write(digest)
    print(f"Saved digest to {digest_file}", file=sys.stderr)

    ok = send_telegram(digest)
    if ok:
        print("Digest Telegram sent.", file=sys.stderr)
    else:
        print("Digest NOT sent to Telegram.", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
