"""
LLM wrapper using the tool-as-schema pattern.

We register a single tool whose input_schema matches DocumentExtract, then
force the LLM to call it. We extract validated JSON from the tool_use block.
"""
from anthropic import Anthropic
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_exponential

from schemas import DocumentExtract

load_dotenv()
_client = Anthropic()

MODEL = "claude-sonnet-4-6"
PRICE_IN = 3.0 / 1_000_000
PRICE_OUT = 15.0 / 1_000_000

_total_cost = 0.0


def get_cost() -> float:
    return _total_cost


SAVE_TOOL = {
    "name": "save_extract",
    "description": "Save the structured extraction of the document.",
    "input_schema": DocumentExtract.model_json_schema(),
}

SYSTEM = (
    "You extract structured information from a document. "
    "Call `save_extract` exactly once with the result. "
    "Set confidence < 0.7 if the document is ambiguous, truncated, or hard to parse."
)


@retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=10))
def extract_document(text: str) -> DocumentExtract:
    global _total_cost

    # TODO: call _client.messages.create with:
    #   model=MODEL, max_tokens=2000, system=SYSTEM,
    #   tools=[SAVE_TOOL],
    #   tool_choice={"type": "tool", "name": "save_extract"},
    #   messages=[{"role": "user", "content": text}]
    response = ...

    # TODO: update _total_cost from response.usage tokens.

    # TODO: find the tool_use block, validate with DocumentExtract.model_validate().
    raise NotImplementedError("fill the TODOs")
