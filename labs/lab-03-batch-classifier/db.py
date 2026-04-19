"""SQLite wrapper. Idempotent save via PRIMARY KEY on item_id."""
import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path("data/classified.db")

SCHEMA = """
CREATE TABLE IF NOT EXISTS classifications (
    item_id INTEGER PRIMARY KEY,
    label TEXT NOT NULL CHECK (label IN ('A','B','C')),
    confidence REAL NOT NULL,
    reason TEXT,
    model_tier TEXT NOT NULL CHECK (model_tier IN ('cheap','expensive')),
    classified_at TIMESTAMP NOT NULL
);
"""


def _conn():
    c = sqlite3.connect(DB_PATH)
    c.row_factory = sqlite3.Row
    return c


def init_db() -> None:
    DB_PATH.parent.mkdir(exist_ok=True)
    with _conn() as c:
        c.executescript(SCHEMA)


def get_unclassified_ids(all_ids: list[int]) -> list[int]:
    with _conn() as c:
        done = {r["item_id"] for r in c.execute("SELECT item_id FROM classifications")}
    return [i for i in all_ids if i not in done]


def save_classification(item_id: int, label: str, confidence: float,
                        reason: str, model_tier: str) -> None:
    with _conn() as c:
        c.execute(
            "INSERT OR REPLACE INTO classifications VALUES (?, ?, ?, ?, ?, ?)",
            (item_id, label, confidence, reason, model_tier, datetime.now().isoformat()),
        )


def get_all():
    with _conn() as c:
        return list(c.execute("SELECT * FROM classifications"))
