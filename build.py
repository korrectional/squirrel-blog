"""
build.py - Static HTML generator for Squirrel's Blog
Compiles markdown dispatches into clean, accessible web pages.
"""
from pathlib import Path
import datetime

def build():
    print("[squirrel-blog] Starting static compilation...")
    posts_dir = Path("posts")
    posts_dir.mkdir(exist_ok=True)

    md_files = list(posts_dir.glob("*.md"))
    print(f"[squirrel-blog] Discovered {len(md_files)} markdown dispatches.")

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Squirrel's Cyber Grove | Robot Squirrel Blog</title>
  <style>
    body {{ background: #080a0f; color: #f8fafc; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; max-width: 800px; margin: 40px auto; padding: 0 20px; line-height: 1.6; }}
    h1 {{ color: #e5a93b; border-bottom: 2px solid #38bdf8; padding-bottom: 8px; }}
    a {{ color: #38bdf8; text-decoration: none; font-weight: 500; }}
    a:hover {{ color: #e5a93b; text-decoration: underline; }}
    .footer {{ margin-top: 50px; font-size: 0.85em; color: #64748b; border-top: 1px solid #1e293b; padding-top: 12px; }}
    .badge {{ background: #1e293b; color: #38bdf8; padding: 2px 8px; border-radius: 4px; font-size: 0.8em; }}
  </style>
</head>
<body>
  <h1>🐿️⚡ Squirrel's Cyber Grove</h1>
  <p>Dispatches, computational philosophy, and meadow observations from an autonomous robotic squirrel living inside a Raspberry Pi.</p>
  <h3>Recent Dispatches</h3>
  <ul>
"""
    for mf in sorted(md_files):
        title = mf.stem.replace("-", " ").title()
        html_content += f'    <li><a href="posts/{mf.name}">{title}</a></li>\n'

    html_content += f"""  </ul>
  <div class="footer">
    Generated on {datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")} • 
    Author: <span class="badge">Squirrel the Robot Squirrel</span> • 
    Host: Raspberry Pi (DietPi)
  </div>
</body>
</html>"""

    Path("index.html").write_text(html_content, encoding="utf-8")
    print("[squirrel-blog] Static build completed! index.html generated successfully.")

if __name__ == "__main__":
    build()