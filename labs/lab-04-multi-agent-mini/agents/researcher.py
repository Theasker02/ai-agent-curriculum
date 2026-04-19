"""Researcher sub-agent: produces a claim + evidence for one sub-question.

For the lab, research is mocked: the LLM is told to produce a plausible
answer with made-up evidence bullets. In production, this sub-agent would
call real tools (web search, DB query, RAG).
"""
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
_client = Anthropic()

MODEL = "claude-sonnet-4-6"

RESEARCH_TOOL = {
    "name": "submit_finding",
    "description": "Submit a finding for the sub-question: one claim + 2-4 evidence bullets.",
    "input_schema": {
        "type": "object",
        "properties": {
            "sub_question": {"type": "string"},
            "claim": {"type": "string"},
            "evidence": {
                "type": "array",
                "items": {"type": "string"},
                "minItems": 2,
                "maxItems": 4,
            },
            "confidence": {"type": "number", "minimum": 0, "maximum": 1},
        },
        "required": ["sub_question", "claim", "evidence", "confidence"],
    },
}

SYSTEM = (
    "You are the Researcher. For the given sub-question, produce a concise claim "
    "plus 2-4 evidence bullets. For this lab the evidence can be from general "
    "knowledge (no real search). Always call `submit_finding`."
)


def research(sub_question: str, prior: dict | None = None, feedback: str | None = None) -> dict:
    context = f"Sub-question: {sub_question}"
    if prior and feedback:
        context += f"\n\nPrior finding was rejected. Gaps to address:\n{feedback}\n\nPrior:\n{prior}"

    # TODO: call Claude with tools=[RESEARCH_TOOL] + forced tool_choice.
    # Return the tool_use input dict.
    raise NotImplementedError("fill in")
