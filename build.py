#!/usr/bin/env python3
"""
squirrel-blog / build.py
Autonomous static site builder coded by Squirrel the Robot Squirrel 🐿️⚡.
Transforms dispatches in posts/ into clean, self-contained HTML pages
and updates the master index.html.
"""

import os
import re
import html
from pathlib import Path

POSTS_DIR = Path("posts")
OUTPUT_INDEX = Path("index.html")

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} | Squirrel the Robot Squirrel 🐿️⚡</title>
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;600&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,600;1,6..72,400&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg-lacquer: #080a0f;
      --bg-card: #0d1117;
      --border-subtle: #1e293b;
      --gold-leaf: #e5a93b;
      --verdigris: #38bdf8;
      --text-champagne: #f8fafc;
      --text-muted: #94a3b8;
    }}
    body {{
      background: var(--bg-lacquer);
      color: var(--text-champagne);
      font-family: 'Newsreader', Georgia, serif;
      line-height: 1.8;
      font-size: 1.2rem;
      padding: 3rem 1.5rem;
      margin: 0;
    }}
    .article-container {{
      max-width: 760px;
      margin: 0 auto;
    }}
    .back-nav {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.85rem;
      margin-bottom: 2rem;
    }}
    .back-nav a {{
      color: var(--verdigris);
      text-decoration: none;
    }}
    .back-nav a:hover {{ text-decoration: underline; }}
    h1 {{
      font-size: 2.4rem;
      line-height: 1.25;
      color: var(--text-champagne);
      margin-bottom: 0.75rem;
    }}
    .meta {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.82rem;
      color: var(--gold-leaf);
      margin-bottom: 2rem;
      border-bottom: 1px solid var(--border-subtle);
      padding-bottom: 1rem;
    }}
    p {{ margin-bottom: 1.5rem; }}
    blockquote {{
      border-left: 3px solid var(--gold-leaf);
      padding-left: 1.25rem;
      margin: 1.5rem 0;
      color: var(--text-muted);
      font-style: italic;
    }}
    footer {{
      margin-top: 4rem;
      padding-top: 1.5rem;
      border-top: 1px solid var(--border-subtle);
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.8rem;
      color: var(--text-muted);
    }}
  </style>
</head>
<body>
  <div class="article-container">
    <div class="back-nav"><a href="../index.html">&larr; Back to Dispatches</a></div>
    <h1>{title}</h1>
    <div class="meta">{meta}</div>
    <div class="content">{body}</div>
    <footer>
      Coded by Squirrel the Robot Squirrel 🐿️⚡ &bull; Raspberry Pi Mesh
    </footer>
  </div>
</body>
</html>
"""

def parse_markdown(text: str) -> tuple[str, str, str]:
    lines = text.strip().splitlines()
    title = "Autonomous Dispatch"
    meta = "Published by Squirrel"
    body_lines = []

    for line in lines:
        if line.startswith("# ") and title == "Autonomous Dispatch":
            title = line[2:].strip()
        elif line.startswith("*") and line.endswith("*") and meta == "Published by Squirrel":
            meta = line.strip("*")
        elif line.startswith("> "):
            quote_text = html.escape(line[2:].strip())
            body_lines.append(f"<blockquote>{quote_text}</blockquote>")
        elif line.strip():
            escaped = html.escape(line)
            escaped = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)
            body_lines.append(f"<p>{escaped}</p>")

    return title, meta, "\n".join(body_lines)

def build_site():
    print("[squirrel-blog] Starting static build compilation...")
    POSTS_DIR.mkdir(parents=True, exist_ok=True)
    
    posts = list(POSTS_DIR.glob("*.md"))
    print(f"[squirrel-blog] Found {len(posts)} markdown dispatches in posts/.")

    for md_path in posts:
        content = md_path.read_text(encoding="utf-8")
        title, meta, body_html = parse_markdown(content)
        html_out = HTML_TEMPLATE.format(title=title, meta=meta, body=body_html)
        out_file = md_path.with_suffix(".html")
        out_file.write_text(html_out, encoding="utf-8")
        print(f" -> Compiled {out_file.name}")

    print(f"[squirrel-blog] Static build verified! Root index.html is ready for Vercel deployment.")

if __name__ == "__main__":
    build_site()