"""Session-level claim ledger — dedup, block counter, forensic record."""
import json
import pathlib
import time


HOOK_DIR = pathlib.Path(__file__).parent
LEDGER_DIR = HOOK_DIR / "ledger"
LEDGER_DIR.mkdir(parents=True, exist_ok=True)


class Ledger:
    def __init__(self, session_id: str):
        # Sanitize session_id for filesystem
        safe_id = "".join(c if c.isalnum() or c in "-_" else "_" for c in str(session_id))[:80]
        self.path = LEDGER_DIR / f"{safe_id}.json"
        if self.path.exists():
            try:
                self.state = json.loads(self.path.read_text())
            except Exception:
                self.state = self._fresh()
        else:
            self.state = self._fresh()
        self.state["turns"] = self.state.get("turns", 0) + 1
        self.state["last_seen"] = time.time()

    @staticmethod
    def _fresh():
        return {
            "verified": {},
            "unknown": {},
            "blocks": 0,
            "turns": 0,
            "first_seen": time.time(),
        }

    def is_verified(self, key: str) -> bool:
        return key in self.state["verified"]

    def record_batch(self, results):
        for r in results:
            bucket = "verified" if r["status"] == "verified" else "unknown"
            claim = r["claim"]
            self.state[bucket][claim.key] = {
                "text": claim.text[:300],
                "kind": claim.kind,
                "ts": time.time(),
                "evidence_snippet": r.get("evidence", "")[:200],
            }
        self._flush()

    def bump_block(self):
        self.state["blocks"] = self.state.get("blocks", 0) + 1
        self._flush()

    def block_count(self) -> int:
        return self.state.get("blocks", 0)

    def _flush(self):
        try:
            self.path.write_text(json.dumps(self.state, indent=2))
        except Exception:
            pass
