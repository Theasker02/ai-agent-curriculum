"""
Lab 02 - Document Pipeline (skeleton).

Pipeline:
  input/*.txt  ->  LLM extract  ->  Pydantic validate  ->  [HITL if low conf]  ->  output/*.{json,md}

Run:
    python main.py
"""
from pathlib import Path

from schemas import DocumentExtract
from llm import extract_document, get_cost
from hitl import approve
from state import load_state, save_state, is_processed, mark_processed

INPUT_DIR = Path("input")
OUTPUT_DIR = Path("output")
LOW_CONF_THRESHOLD = 0.7


def render_markdown(ex: DocumentExtract) -> str:
    lines = [f"# {ex.title}", "", ex.summary, "", "## Key points"]
    lines += [f"- {p}" for p in ex.key_points]
    lines += ["", "## Entities"]
    lines += [f"- **{e.kind}**: {e.value}" for e in ex.entities]
    return "\n".join(lines)


def process_file(path: Path) -> None:
    text = path.read_text(encoding="utf-8")

    # TODO (1): extract = extract_document(text)  -> DocumentExtract
    extract: DocumentExtract = ...

    # TODO (2): if extract.confidence < LOW_CONF_THRESHOLD, call approve(extract);
    # return early if rejected.

    # TODO (3): write JSON + markdown into OUTPUT_DIR.
    ...


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)
    state = load_state()

    for path in sorted(INPUT_DIR.glob("*.txt")):
        if is_processed(state, path.name):
            print(f"[skip] {path.name}")
            continue
        print(f"[process] {path.name}")
        try:
            process_file(path)
        except Exception as e:
            print(f"[error] {path.name}: {e}")
            continue
        state = mark_processed(state, path.name)
        save_state(state)

    print(f"[cost] total: ${get_cost():.4f}")


if __name__ == "__main__":
    main()
