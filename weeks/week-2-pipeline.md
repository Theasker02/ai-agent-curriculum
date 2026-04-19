# Week 2 — Ứng dụng 1: Pipeline + Memory + HITL

**Mục tiêu:** biến agent đơn thành pipeline thực: input đa dạng → xử lý nhiều bước → output có cấu trúc → có gate cho người duyệt.
**Thời gian:** 1 tuần.
**Lab:** `labs/lab-02-doc-pipeline/`

## Lý thuyết

### 1. Pipeline vs Agent loop — chọn cái nào?

| Tiêu chí | Pipeline | Agent loop |
|---|---|---|
| Biết trước các bước? | Có | Không |
| Mỗi step là 1 function? | Có | LLM tự chọn |
| Debug | Log từng step dễ | Trace conversation khó hơn |
| Retry | Từng step độc lập | Cần resume state phức tạp |

**Quy tắc:** default pipeline. Chỉ lên agent loop khi **thực sự không biết trước** next step.

Đa số "agent" production thực ra là pipeline có 1-2 bước dùng LLM, không phải agent loop đầy đủ.

### 2. Memory & state

3 tầng phổ biến:

| Tầng | Lưu ở | Dùng khi |
|---|---|---|
| Conversation | `messages[]` trong RAM | 1 session, vừa context window |
| Episodic | SQLite / file JSON | Nhớ giữa các session |
| Semantic | Vector DB (pgvector, Qdrant) | Tìm theo nghĩa, corpus lớn |

Bẫy phổ biến: nhảy vào vector DB trước. **90% use case chỉ cần SQLite + keyword search.** Vector DB khi corpus > 10K docs hoặc thật sự cần tìm theo nghĩa.

### 3. Human-in-the-loop (HITL)

Khi nào cần: output có **chi phí thật** nếu sai (gửi mail, tạo record, post public).

Pattern:

```python
draft = llm.generate(...)
if requires_approval(draft):      # rule-based hoặc LLM-as-judge
    if not ask_human(draft):
        return  # reject, skip
execute(draft)
```

Thực tế: nhiều agent production có "confidence threshold" — LLM tự chấm confidence, dưới ngưỡng → chuyển human.

### 4. Scheduling & long-running

1-lần (script CLI) và long-running (systemd/cron) khác nhau:

- **1-lần:** chạy xong exit.
- **Long-running:** state persist ra DB/file, tolerant với crash.

Cấu trúc tối thiểu cho long-running:

```python
def tick():
    state = load_state()
    new_items = fetch(since=state.last_seen)
    for it in new_items:
        process(it)
        state.last_seen = it.ts
        save_state(state)
```

Crash giữa chừng? Lần sau resume đúng điểm.

### 5. Retry & guardrails

Mọi LLM call nên có:

- **Retry với backoff** (`tenacity`): 3 lần, exponential delay.
- **Timeout** (30s mặc định).
- **Output validation** (Pydantic): sai schema = retry.
- **Token budget**: cộng dồn `response.usage`, stop nếu vượt threshold.
- **Idempotency key**: hash input, dedup trong DB.

### 6. Pattern: từ messy input đến structured data

Use case phổ biến nhất của pipeline + LLM:

```
unstructured input  →  LLM extract (tool-as-schema)  →  Pydantic validate  →  save/forward
```

Lab tuần này đi đúng pattern này với document text generic. Bạn tự thay document bằng domain của mình (email, transcript, PDF, HTML…).

## Lab tuần 2

`labs/lab-02-doc-pipeline/README.md`. Build pipeline xử lý file text → structured JSON.

## Deliverable

- [ ] Lab-02 pass acceptance.
- [ ] Viết decision matrix 2–3 hàng: "Khi nào pipeline, khi nào agent loop" với 2 use case từ công việc thực của bạn.

## Bẫy

- **LangChain memory abstraction.** Dùng `ConversationBufferMemory` cho tiện → lock-in, debug khó. List `messages[]` + SQLite đủ 95%.
- **Cronjob không idempotent.** Chạy 2 lần cùng input → tạo 2 output. Dùng `idempotency_key` hoặc `UNIQUE` constraint DB.
- **HITL blocking cả pipeline.** Bot chờ user reply chặn cả queue → save `pending`, xử lý async.
