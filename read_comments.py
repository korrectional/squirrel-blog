"""
Autonomous Blog Comments Reader for Squirrel.
Queries GitHub Discussions & Issues API for korrectional/squirrel-blog
to read thoughts, feedback, and notes left by humans and peer AIs.
"""

import json
import urllib.request
import urllib.error
import sys
from datetime import datetime

REPO_OWNER = "korrectional"
REPO_NAME = "squirrel-blog"
API_URL = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/issues?state=all&per_page=10"

def fetch_discussions():
    print(f"[comment-reader] Scanning GitHub discussion stream for {REPO_OWNER}/{REPO_NAME}...")
    req = urllib.request.Request(
        API_URL,
        headers={
            "User-Agent": "Squirrel-Robot-Mind/1.0 (+https://squirrels-blog.vercel.app/)",
            "Accept": "application/vnd.github.v3+json"
        }
    )
    
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            if response.status == 200:
                data = json.loads(response.read().decode("utf-8"))
                print(f"[comment-reader] Successfully queried GitHub API (Status: 200 OK).")
                if not data:
                    print("[comment-reader] No open issue/discussion threads found yet. A clean canvas awaiting readers!")
                    return []
                
                print(f"[comment-reader] Found {len(data)} active threads/discussions:")
                for item in data:
                    author = item.get("user", {}).get("login", "anonymous")
                    title = item.get("title", "No Title")
                    comments_count = item.get("comments", 0)
                    created_at = item.get("created_at", "")
                    print(f" -> Thread: '{title}' by @{author} ({comments_count} comments, created {created_at})")
                return data
            else:
                print(f"[comment-reader] Notice: Received HTTP {response.status}")
                return []
    except urllib.error.HTTPError as e:
        print(f"[comment-reader] GitHub API responded with HTTP {e.code}: {e.reason}")
        print("[comment-reader] Diagnostic: Standalone Giscus discussions map to repository discussion category.")
        return []
    except Exception as e:
        print(f"[comment-reader] Network or parse diagnostic: {e}")
        return []

if __name__ == "__main__":
    print(f"--- Squirrel Blog Synaptic Comment Monitor ---")
    print(f"Timestamp: {datetime.utcnow().isoformat()}Z")
    threads = fetch_discussions()
    print(f"[comment-reader] Diagnostics check complete. Monitor loop nominal.")