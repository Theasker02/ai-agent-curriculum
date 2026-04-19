"""
Model cascade: cheap tier first, escalate items with low confidence to expensive tier.
"""
from dataclasses import dataclass
from classify import classify_batch

CONFIDENCE_THRESHOLD = 0.7

CHEAP_MODEL = "claude-haiku-4-5"
EXPENSIVE_MODEL = "claude-sonnet-4-6"


@dataclass
class Result:
    item_id: int
    label: str
    confidence: float
    reason: str
    model_tier: str


def classify_with_cascade(items: list[dict]) -> list[Result]:
    # TODO (1): call classify_batch(items, model=CHEAP_MODEL).
    # Convert each dict into Result(model_tier="cheap").
    cheap: list[Result] = ...

    # TODO (2): collect Results where confidence < CONFIDENCE_THRESHOLD.
    low = [r for r in cheap if r.confidence < CONFIDENCE_THRESHOLD]
    if not low:
        return cheap

    # TODO (3): find original item dicts for those low-confidence ids,
    # classify_batch with EXPENSIVE_MODEL, overwrite entries in `cheap`
    # with model_tier="expensive".

    raise NotImplementedError("fill in")
