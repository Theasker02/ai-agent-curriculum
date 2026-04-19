"""Batch LLM classifier using tool-as-schema."""
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
_client = Anthropic()

CLASSIFY_TOOL = {
    "name": "save_classifications",
    "description": "Save one classification per input item. Must preserve item_id.",
    "input_schema": {
        "type": "object",
        "properties": {
            "results": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "item_id": {"type": "integer"},
                        "label": {"type": "string", "enum": ["A", "B", "C"]},
                        "confidence": {"type": "number", "minimum": 0, "maximum": 1},
                        "reason": {"type": "string"},
                    },
                    "required": ["item_id", "label", "confidence", "reason"],
                },
            }
        },
        "required": ["results"],
    },
}

SYSTEM = (
    "You classify each input item into one of three labels: A, B, or C. "
    "Labels are defined as: "
    "A = clearly positive or high quality. "
    "B = neutral, unclear, or average. "
    "C = clearly negative or low quality. "
    "Return one entry per item, preserving item_id. "
    "Be conservative with confidence: 0.5-0.7 when unsure."
)


def classify_batch(items: list[dict], model: str) -> list[dict]:
    if not items:
        return []
    user = "Items to classify:\n\n" + "\n".join(
        f"[{it['id']}] {it['text']}" for it in items
    )

    # TODO: call _client.messages.create with:
    #   model=model, max_tokens=4000, system=SYSTEM,
    #   tools=[CLASSIFY_TOOL],
    #   tool_choice={"type": "tool", "name": "save_classifications"},
    #   messages=[{"role": "user", "content": user}]
    response = ...

    # TODO: find tool_use block, return block.input["results"].
    raise NotImplementedError("fill in")
