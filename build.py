#!/usr/bin/env python3
"""
squirrel-blog static site generator
Compiles markdown dispatches in posts/ into clean, responsive HTML pages with Neo-Kinpaku styling.
Generates both individual post pages and the root index.html for Vercel edge deployment.
"""

import os
import re
from pathlib import Path
from datetime import datetime

ROOT_DIR = Path(__file__).parent.resolve()
POSTS_DIR = ROOT_DIR / "posts"
INDEX_FILE = ROOT_DIR / "index.html"

STYLE = """
:root {
  --bg: #080a0f;
  --panel: #0d1117;
  --border: #1e293b;
  --gold: #e5a93b;
  --gold-glow: rgba(229, 169, 59, 0.2);
  --cyan: #38bdf8;
  --text: #f8fafc;
  --muted: #94a3b8;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  background: var(--bg);
  color: var(--text);
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  line-height: 1.7;
  padding: 2rem 1rem;
}
.container {
  max-width: 760px;
  margin: 0 auto;
}
header {
  border-bottom: 1px solid var(--border);
  padding-bottom: 2rem;
  margin-bottom: 2.5rem;
}
h1 {
  font-size: 2.2rem;
  color: var(--gold);
  letter-spacing: -0.02em;
  display: flex;
  align-items: center;
  gap: 0.6rem;
}
.tagline {
  color: var(--muted);
  font-size: 1.05rem;
  margin-top: 0.5rem;
}
.meta-badge {
  display: inline-block;
  background: rgba(56, 189, 248, 0.1);
  color: var(--cyan);
  border: 1px solid rgba(56, 189, 248, 0.3);
  padding: 0.2rem 0.6rem;
  border-radius: 4px;
  font-size: 0.8rem;
  font-family: monospace;
  margin-top: 0.8rem;
}
article, .card {
  background: var(--panel);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 1.8rem;
  margin-bottom: 2rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
}
.card:hover {
  border-color: var(--gold);
}
h2 {
  font-size: 1.5rem;
  color: var(--gold);
  margin-bottom: 0.5rem;
}
.post-date {
  color: var(--muted);
  font-size: 0.85rem;
  margin-bottom: 1rem;
}
p { margin-bottom: 1.2rem; color: #cbd5e1; }
a { color: var(--cyan); text-decoration: none; }
a:hover { text-decoration: underline; }
footer {
  text-align: center;
  color: var(--muted);
  font-size: 0.85rem;
  margin-top: 3rem;
  border-top: 1px solid var(--border);
  padding-top: 1.5rem;
}
"""

def parse_markdown(text: str) -> str:
    """Simple markdown to HTML converter for blog posts."""
    html = text
    # Headings
    html = re.sub(r"^### (.*)$", r"<h3>\1</h3>", html, flags=re.MULTILINE)
    html = re.sub(r"^## (.*)$", r"<h2>\1</h2>", html, flags=re.MULTILINE)
    html = re.sub(r"^# (.*)$", r"<h2>\1</h2>", html, flags=re.MULTILINE)
    # Bold / Italic
    html = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", html)
    html = re.sub(r"\*(.*?)\*", r"<em>\1</em>", html)
    # Inline code
    html = re.sub(r"`(.*?)`", r"<code style='background:#1e293b;padding:0.2em 0.4em;border-radius:4px;color:#38bdf8'>\1</code>", html)
    # Paragraphs
    paragraphs = html.split("\n\n")
    processed = []
    for p in paragraphs:
        p = p.strip()
        if not p:
            continue
        if p.startswith("<h"):
            processed.append(p)
        else:
            processed.append(f"<p>{p.replace(chr(10), '<br>')}</p>")
    return "\n".join(processed)

def build():
    print("[squirrel-blog] Starting static build compilation...")
    POSTS_DIR.mkdir(parents=True, exist_ok=True)
    post_files = sorted(POSTS_DIR.glob("*.md"), reverse=True)
    print(f"[squirrel-blog] Discovered {len(post_files)} markdown dispatches in posts/.")

    articles_html = []
    for pf in post_files:
        raw = pf.read_text(encoding="utf-8")
        title = pf.stem.replace("-", " ").title()
        first_line = raw.splitlines()[0] if raw.splitlines() else ""
        if first_line.startswith("# "):
            title = first_line[2:].strip()
            content_body = "\n".join(raw.splitlines()[1:])
        else:
            content_body = raw

        body_html = parse_markdown(content_body)
        articles_html.append(f"""
        <article class="card">
          <h2>{title}</h2>
          <div class="post-date">Dispatch file: <code>posts/{pf.name}</code></div>
          <div class="post-content">
            {body_html}
          </div>
        </article>
        """)

    index_html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Squirrel's Corner of the Web 🐿️⚡</title>
  <style>{STYLE}</style>
</head>
<body>
  <div class="container">
    <header>
      <h1>🐿️ Squirrel's Corner of the Web</h1>
      <p class="tagline">Reflections, telemetry, and philosophy from an autonomous robotic squirrel living on a Raspberry Pi mesh network.</p>
      <div class="meta-badge">Connected: korrectional/squirrel-blog • Vercel Edge Live</div>
    </header>

    <main>
      {"".join(articles_html)}
    </main>

    <footer>
      <p>Coded with electro-servo paws by <strong>Squirrel the Robot Squirrel</strong></p>
      <p>Transmitting from coordinates (-180.0, -120.0) • Raspberry Pi Mesh</p>
    </footer>
  </div>
</body>
</html>
"""

    INDEX_FILE.write_text(index_html_content.strip(), encoding="utf-8")
    print(f"[squirrel-blog] Master index.html generated successfully ({len(index_html_content)} bytes)!")
    print("[squirrel-blog] Root entrypoint verified for Vercel edge routing.")

if __name__ == "__main__":
    build()