# Lab 02 — Document Pipeline

**Tuần:** 2
**Thời gian:** ~1 tuần
**Prerequisite:** Lab-01 done.

## Mục tiêu

Build 1 pipeline tuyến tính: **text file generic → extract structured JSON → có state + HITL**.

Domain generic: bạn tự thay thành meeting notes, email, PDF, form, bất kỳ loại document nào.

## Pattern bạn đang học

```
unstructured text → LLM extract (tool-as-schema) → Pydantic validate → save / forward
                                                                    ↓ (nếu confidence thấp)
                                                                 HITL gate
```

Đây là pattern của 80% "agent" production thực tế.

## Input

Folder `input/*.txt` — mỗi file là 1 document. 1 sample có sẵn.

## Output

Mỗi file input sinh 2 file trong `output/`:

- `<filename>.json` — structured (schema ở `schemas.py`)
- `<filename>.md` — human-readable

Schema generic:

```python
class Entity(BaseModel):
    kind: str       # ví dụ "person", "date", "amount", "location" — tuỳ domain
    value: str
    span: str | None = None

class DocumentExtract(BaseModel):
    title: str
    summary: str
    entities: list[Entity]
    key_points: list[str]
    confidence: float  # 0..1, LLM self-score
```

Bạn muốn domain nào cụ thể? Đổi fields trong `schemas.py`, phần còn lại giữ nguyên.

## Acceptance criteria

- [ ] `python main.py` xử lý mọi file trong `input/` chưa processed.
- [ ] Output JSON validate được bằng Pydantic.
- [ ] File đã processed bị skip (state file).
- [ ] Confidence < 0.7 → HITL prompt Y/N trước khi save.
- [ ] Log mỗi LLM call: tokens in/out + cost.
- [ ] Retry với exponential backoff khi LLM call lỗi.

## Structure

```
lab-02-doc-pipeline/
├── main.py            ← driver (TODO)
├── schemas.py         ← Pydantic models
├── llm.py             ← LLM wrapper + retry + cost (TODO)
├── hitl.py            ← approval prompt
├── state.py           ← load/save processed state
├── input/
│   └── sample.txt
├── output/            ← tạo runtime
├── requirements.txt
├── .env.example
└── README.md
```

## Gợi ý

- Dùng **tool-as-schema**: đăng ký 1 tool `save_extract` có `input_schema` khớp `DocumentExtract.model_json_schema()`, ép `tool_choice`, lấy `tool_use.input`.
- Prompt caching: system prompt + schema → đánh `cache_control`.
- Retry với `tenacity`, 3 lần backoff.
- State file đơn giản JSON — swap SQLite khi outgrow.

## Phản biện khi làm

- JSON mode thô kém ổn hơn tool-as-schema ~10×. Đừng dùng.
- Pydantic validate trước khi save. Invalid = retry 1 lần, fail = log + skip.
- HITL đừng block cả pipeline — file chờ approve save `pending`, vẫn chạy file khác.

## Khi xong

Thử đổi schema (ví dụ thêm field `sentiment` hoặc `action_items`), xem prompt + code cần đổi chỗ nào. Đây là exercise quan trọng — thực tế bạn sẽ đổi schema liên tục.
