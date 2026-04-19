"""Minimal JSON-file state store. Swap for SQLite when you outgrow it."""
import json
from datetime import datetime, timezone
from pathlib import Path

STATE_FILE = Path(".state.json")


def load_state() -> dict:
    if not STATE_FILE.exists():
        return {"processed": {}}
    return json.loads(STATE_FILE.read_text())


def save_state(state: dict) -> None:
    STATE_FILE.write_text(json.dumps(state, indent=2))


def is_processed(state: dict, name: str) -> bool:
    return name in state.get("processed", {})


def mark_processed(state: dict, name: str) -> dict:
    state.setdefault("processed", {})[name] = datetime.now(timezone.utc).isoformat()
    return state
