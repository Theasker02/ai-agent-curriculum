"""Minimal human-in-the-loop approval via CLI prompt."""
import json
from schemas import DocumentExtract


def approve(extract: DocumentExtract) -> bool:
    print("\n--- LOW CONFIDENCE OUTPUT ---")
    print(json.dumps(extract.model_dump(), ensure_ascii=False, indent=2))
    print(f"confidence = {extract.confidence:.2f}")
    return input("Approve and save? [y/N] ").strip().lower() == "y"
