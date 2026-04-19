# Lab 04 — Mini Multi-Agent

**Tuần:** 3 (nhánh Multi-agent)
**Thời gian:** ~1.5 tuần
**Prerequisite:** Lab-02 done.

## Cảnh báo trước khi bắt đầu

> Multi-agent debug khó gấp ~5× pipeline đơn. **Chỉ làm lab này nếu use case thực yêu cầu.** Nếu chưa chắc, chọn Lab-03 (batch) thay thế — phổ biến hơn rất nhiều.

## Mục tiêu

Build 1 orchestrator nhỏ điều phối 3 sub-agent chuyên trách, mỗi sub có role + tool + schema output riêng. Học **role separation**, **evidence gate**, **context isolation**.

## Scenario generic: Research Assistant

Orchestrator nhận 1 câu hỏi research → điều phối:

1. **Planner** — chia câu hỏi thành 2–3 sub-question cụ thể.
2. **Researcher** — với mỗi sub-question, produce findings (mock data trong lab).
3. **Critic** — đọc findings, check gaps/contradictions, approve hoặc request rework.

Nếu Critic reject → rework 1 lần. Sau đó force-pass hoặc fail.

Domain generic: research có thể là "technical decision", "market analysis", "code refactor plan"… Lab dùng scenario generic để bạn tự đổi domain.

## Pattern đang học

```
User question
    │
    ▼
Orchestrator ──► Planner   ─► sub-questions[]
    │
    ├──────────► Researcher ─► findings[]     (per sub-question)
    │
    └──────────► Critic     ─► approved?, gaps
                                │
                   rejected ◄───┘ (rework at most once)
                                │
                     approved? ─► FinalReport
```

## Acceptance criteria

- [ ] `python orchestrator.py "câu hỏi"` chạy qua Planner → Researcher → Critic.
- [ ] Mỗi sub-agent có system prompt + tool-as-schema RIÊNG.
- [ ] Evidence gate: Researcher không được claim "done" nếu findings rỗng.
- [ ] Critic có quyền reject, orchestrator rework tối đa 1 lần.
- [ ] Log rõ input + output mỗi sub-agent để audit.
- [ ] Context isolation: Planner KHÔNG thấy findings raw; Researcher KHÔNG thấy critic state.

## Structure

```
lab-04-multi-agent-mini/
├── orchestrator.py      ← driver (TODO)
├── agents/
│   ├── __init__.py
│   ├── planner.py       ← TODO
│   ├── researcher.py    ← TODO (mocks research, không thực sự search web)
│   └── critic.py        ← TODO
├── requirements.txt
├── .env.example
└── README.md
```

## Gợi ý kiến trúc

```python
def run(question: str) -> dict:
    plan = planner.plan(question)                     # sub_questions: list[str]
    verify(plan, required=["sub_questions"])
    if not plan["sub_questions"]:
        raise OrchestratorError("planner returned empty plan")

    findings = [researcher.research(q) for q in plan["sub_questions"]]
    for f in findings:
        verify(f, required=["claim", "evidence"])
        if not f["evidence"]:
            raise OrchestratorError("researcher returned no evidence")

    review = critic.review(question, findings)
    if not review["approved"]:
        findings = [researcher.research(q, prior=f, feedback=review["gaps"])
                    for q, f in zip(plan["sub_questions"], findings)]
        review = critic.review(question, findings)
        # after 1 rework, accept whatever we have

    return {"question": question, "findings": findings, "review": review}
```

Mỗi sub-agent KHÔNG biết về nhau — chỉ biết input/output schema của mình.

## Phản biện

- **Pattern này over-engineer cho câu hỏi đơn giản.** 1 call Sonnet đủ cho 80% case. Multi-agent lợi khi cần multiple perspectives hoặc evidence audit.
- **Context bloat:** đừng truyền hết findings cho Critic — truyền summary. Giảm token, giảm hallucination.
- **Sub-agent ảo tưởng "done":** LLM hay claim pass mà không verify. Bắt buộc evidence field trong schema, orchestrator reject nếu rỗng.
- **Infinite rework:** cap ở 1 lần. Nếu vẫn fail, accept output current hoặc return error — không loop vô hạn.

## Khi xong

- Benchmark cost so với "1 call Sonnet trả lời thẳng" câu hỏi tương tự. Multi-agent đáng không?
- Thử scenario mà ép Critic reject (câu hỏi mơ hồ) → xem rework loop hoạt động đúng không.
