"""Verifier — runs claims through search_backend with caching + budget."""
import concurrent.futures
import hashlib
import json
import os
import pathlib
import subprocess
import sys
import time


HOOK_DIR = pathlib.Path(__file__).parent
CACHE_DIR = HOOK_DIR / "cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)
CACHE_TTL = 7 * 86400  # 7 days


def _cache_path(key: str) -> pathlib.Path:
    return CACHE_DIR / f"{key}.json"


def _cached(key: str):
    p = _cache_path(key)
    if p.exists() and time.time() - p.stat().st_mtime < CACHE_TTL:
        try:
            return json.loads(p.read_text())
        except Exception:
            return None
    return None


def _write_cache(key: str, value: dict):
    try:
        _cache_path(key).write_text(json.dumps(value))
    except Exception:
        pass


def _score(claim_text: str, evidence: str) -> str:
    """Conservative scorer — only verified on substantial token overlap."""
    if not evidence:
        return "unknown"
    ev = evidence.lower()
    tokens = {t.strip(".,;:()\"'") for t in claim_text.lower().split() if len(t) > 4}
    if not tokens:
        return "unknown"
    hits = sum(1 for t in tokens if t in ev)
    if hits >= max(2, len(tokens) // 3):
        return "verified"
    return "unknown"


def _verify_one(claim) -> dict:
    hit = _cached(claim.key)
    if hit is not None:
        return {**hit, "claim": claim, "cached": True}

    query = claim.text[:200]
    try:
        r = subprocess.run(
            ["python3", str(HOOK_DIR / "search_backend.py"), query],
            capture_output=True, text=True, timeout=4.5,
        )
        result = json.loads(r.stdout.strip() or "{}")
    except Exception as e:
        result = {"status": "error", "evidence": "", "error": str(e)[:150]}

    if result.get("status") == "no_backend":
        out = {"status": "no_backend", "evidence": "", "claim": claim, "cached": False}
        # Don't cache no_backend — user may add a key later
        return out

    score = _score(claim.text, result.get("evidence", ""))
    out = {
        "status": score,
        "evidence": result.get("evidence", "")[:500],
        "urls": result.get("urls", [])[:3],
        "claim": claim,
        "cached": False,
    }
    _write_cache(claim.key, {k: v for k, v in out.items() if k != "claim"})
    return out


def verify_batch(claims, time_budget: float = 12.0) -> list[dict]:
    deadline = time.time() + max(2.0, time_budget)
    results = []
    if not claims:
        return results

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
        futures = {ex.submit(_verify_one, c): c for c in claims}
        for fut in concurrent.futures.as_completed(futures):
            if time.time() > deadline:
                # Abort remaining; mark them as unknown
                for c in futures.values():
                    if not any(r["claim"].key == c.key for r in results):
                        results.append({
                            "status": "unknown", "evidence": "",
                            "claim": c, "cached": False, "timeout": True,
                        })
                break
            try:
                results.append(fut.result(timeout=0.5))
            except Exception:
                pass
    return results
