"""Search backend — uses Brave Search API if BRAVE_API_KEY env var present.

Falls back to a 'no-network' mode that always returns 'unknown' status,
in which case the architecture still routes claims through the
decision module as soft warnings rather than hard blocks.
"""
import json
import os
import sys
import urllib.parse
import urllib.request


def search_brave(query: str, api_key: str, timeout: float = 3.0) -> dict:
    url = "https://api.search.brave.com/res/v1/web/search?"
    url += urllib.parse.urlencode({"q": query, "count": 3})
    req = urllib.request.Request(
        url,
        headers={
            "Accept": "application/json",
            "X-Subscription-Token": api_key,
            "User-Agent": "numenist-verify/1.0",
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = json.loads(resp.read())
    results = (data.get("web") or {}).get("results", [])[:3]
    evidence = "\n".join(
        f"{r.get('title', '')} :: {r.get('description', '')}"
        for r in results
    )
    return {"status": "ok", "evidence": evidence, "urls": [r.get("url") for r in results]}


def main():
    query = sys.argv[1] if len(sys.argv) > 1 else ""
    api_key = os.environ.get("BRAVE_API_KEY") or os.environ.get("BRAVE_SEARCH_API_KEY")

    if not api_key:
        # No-network fallback: still emit a parseable JSON object so the
        # verifier doesn't crash. Status 'no_backend' routes to soft warning.
        print(json.dumps({"status": "no_backend", "evidence": "", "urls": []}))
        return

    try:
        result = search_brave(query, api_key)
        print(json.dumps(result))
    except Exception as e:
        print(json.dumps({"status": "error", "evidence": "", "error": str(e)[:200]}))


if __name__ == "__main__":
    main()
