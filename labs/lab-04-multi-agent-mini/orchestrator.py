"""
Lab 04 - Multi-Agent Orchestrator (skeleton).

Flow: Planner -> Researcher (per sub-question) -> Critic (approve or rework once).

Run:
    python orchestrator.py "Làm thế nào để giảm chi phí LLM cho pipeline classify 10K items/day?"
"""
import json
import sys

from agents import planner, researcher, critic


class OrchestratorError(Exception):
    pass


def verify(obj: dict, required: list[str]) -> None:
    for k in required:
        if not obj.get(k):
            raise OrchestratorError(f"missing required field `{k}`")


def run(question: str) -> dict:
    print(f"[orchestrator] planner: {question}")
    plan = planner.plan(question)
    verify(plan, required=["sub_questions"])
    if not plan["sub_questions"]:
        raise OrchestratorError("planner returned empty sub_questions")
    print(f"[orchestrator] plan: {plan['sub_questions']}")

    print(f"[orchestrator] researcher: {len(plan['sub_questions'])} sub-questions")
    findings = []
    for q in plan["sub_questions"]:
        f = researcher.research(q)
        verify(f, required=["claim", "evidence"])
        if not f["evidence"]:
            raise OrchestratorError(f"researcher returned no evidence for {q!r}")
        findings.append(f)

    print(f"[orchestrator] critic: reviewing findings")
    review = critic.review(question, findings)
    if not review.get("approved"):
        print(f"[orchestrator] critic rejected: {review.get('gaps')} — reworking once")
        # TODO (rework): call researcher.research again for each sub-question,
        # passing prior findings + feedback. Re-run critic once more.
        # After 1 rework, accept whatever we have — do not loop.
        ...

    return {"question": question, "plan": plan, "findings": findings, "review": review}


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python orchestrator.py 'your question'")
        sys.exit(1)
    try:
        result = run(sys.argv[1])
        print("\n=== FINAL ===")
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except OrchestratorError as e:
        print(f"[fail] {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
