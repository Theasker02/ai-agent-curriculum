"""Critic sub-agent: reviews findings, flags gaps, approves or rejects."""
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
_client = Anthropic()

MODEL = "claude-sonnet-4-6"

REVIEW_TOOL = {
    "name": "submit_review",
    "description": "Submit review decision: approved + gap summary.",
    "input_schema": {
        "type": "object",
        "properties": {
            "approved": {"type": "boolean"},
            "gaps": {"type": "string", "description": "Short summary of missing evidence or contradictions, if any."},
        },
        "required": ["approved", "gaps"],
    },
}

SYSTEM = (
    "You are the Critic. Review the findings against the original question. "
    "Approve only if findings cover the scope, have concrete evidence, and are consistent. "
    "Be strict: a finding with vague evidence is not acceptable."
)


def review(question: str, findings: list[dict]) -> dict:
    user = f"Original question: {question}\n\nFindings:\n"
    for i, f in enumerate(findings, 1):
        user += f"\n[{i}] sub_q: {f.get('sub_question')}\n    claim: {f.get('claim')}\n    evidence: {f.get('evidence')}\n"

    # TODO: call Claude, return tool_use input dict {"approved": bool, "gaps": str}.
    raise NotImplementedError("fill in")
