"""Reporting: counts per label + accuracy vs ground truth."""
import json
from pathlib import Path
from collections import Counter
from db import get_all


def print_report() -> None:
    rows = get_all()
    counts = Counter(r["label"] for r in rows)
    tiers = Counter(r["model_tier"] for r in rows)
    print("\n=== Classification counts ===")
    for k, v in sorted(counts.items()):
        print(f"  {k}: {v}")
    print(f"\n=== Model tiers used ===")
    for k, v in sorted(tiers.items()):
        print(f"  {k}: {v}")


def evaluate(truth_path: Path) -> None:
    truth = {int(json.loads(l)["id"]): json.loads(l)["label"]
             for l in truth_path.read_text().splitlines() if l.strip()}
    rows = get_all()

    total = correct = 0
    per_label = {"A": [0, 0], "B": [0, 0], "C": [0, 0]}  # [correct, total]
    for r in rows:
        if r["item_id"] not in truth:
            continue
        total += 1
        exp = truth[r["item_id"]]
        per_label[exp][1] += 1
        if r["label"] == exp:
            correct += 1
            per_label[exp][0] += 1

    print(f"\n=== Accuracy: {correct}/{total} = {100*correct/max(total,1):.1f}% ===")
    for label, (c, t) in per_label.items():
        print(f"  {label}: {c}/{t}")
