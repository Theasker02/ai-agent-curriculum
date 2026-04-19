"""Planner sub-agent: breaks a question into 2-3 sub-questions."""
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
_client = Anthropic()

MODEL = "claude-sonnet-4-6"

PLAN_TOOL = {
    "name": "submit_plan",
    "description": "Submit the decomposition of the question into 2-3 concrete sub-questions.",
    "input_schema": {
        "type": "object",
        "properties": {
            "sub_questions": {
                "type": "array",
                "items": {"type": "string"},
                "minItems": 2,
                "maxItems": 3,
            },
            "rationale": {"type": "string"},
        },
        "required": ["sub_questions", "rationale"],
    },
}

SYSTEM = (
    "You are the Planner. Given a research question, return 2-3 concrete sub-questions "
    "that together cover the scope. Do NOT attempt to answer. Always call `submit_plan`."
)


def plan(question: str) -> dict:
    # TODO: call _client.messages.create with tools=[PLAN_TOOL], forced tool_choice.
    # Return the tool_use input dict.
    raise NotImplementedError("fill in")
