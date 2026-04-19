"""
Lab 03 - Batch Classifier (skeleton).

Run:
    python main.py --batch-size 20
"""
import argparse
import json
from pathlib import Path

from db import init_db, get_unclassified_ids, save_classification
from cascade import classify_with_cascade
from report import print_report, evaluate


def load_items(path: Path) -> list[dict]:
    return [json.loads(l) for l in path.read_text().splitlines() if l.strip()]


def chunks(seq, n):
    for i in range(0, len(seq), n):
        yield seq[i:i + n]


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--batch-size", type=int, default=20)
    p.add_argument("--data", default="data/items.jsonl")
    p.add_argument("--truth", default="data/ground_truth.jsonl")
    args = p.parse_args()

    init_db()
    items = load_items(Path(args.data))

    todo_ids = get_unclassified_ids([it["id"] for it in items])
    todo = [it for it in items if it["id"] in todo_ids]
    print(f"[todo] {len(todo)} items to classify (batch size {args.batch_size})")

    # TODO (1): iterate todo in chunks of args.batch_size; call classify_with_cascade,
    # then save_classification for each result.
    ...

    # TODO (2): evaluate against truth, then print_report.
    ...

    raise NotImplementedError("fill the TODOs")


if __name__ == "__main__":
    main()
