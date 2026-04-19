# Lab 03 — Batch Classifier + Model Cascade

**Tuần:** 3 (nhánh Batch)
**Thời gian:** ~1.5 tuần
**Prerequisite:** Lab-02 done.

## Mục tiêu

Build pipeline classify khối lượng lớn: **N items → phân loại label + confidence → lưu DB → report**. Học **batch** và **cascade model** (tier rẻ trước, escalate khi confidence thấp).

Domain generic: input là text + metadata, label là 1 trong `{A, B, C}`. Bạn tự ánh xạ sang use case thực: spam filter, quality tier, sentiment, risk bucket, category…

## Pattern đang học

```
items  →  batch(N)  →  LLM cheap tier  →  confidence >= T?  →  yes: keep
                                                            →  no:  retry with expensive tier
                                                                    ↓
                                                                SQLite (idempotent)
                                                                    ↓
                                                                Report / eval
```

## Input

`data/items.jsonl` — 30 mock items. Format:

```json
{"id": 1, "text": "...", "meta": {...}}
```

## Output

SQLite `data/classified.db`:

```sql
CREATE TABLE classifications (
  item_id INTEGER PRIMARY KEY,
  label TEXT,         -- A | B | C
  confidence REAL,    -- 0..1
  reason TEXT,
  model_tier TEXT,    -- cheap | expensive
  classified_at TIMESTAMP
);
```

Plus: ground truth file `data/ground_truth.jsonl` để bạn đo accuracy.

## Acceptance criteria

- [ ] Batch: mỗi request gửi 10–20 items.
- [ ] Cascade: chạy cheap tier trước. Items `confidence < 0.7` → retry expensive tier.
- [ ] Idempotent: rerun không classify trùng (check DB trước mỗi item).
- [ ] Cost tracking: in cheap vs expensive cost riêng.
- [ ] Accuracy > baseline trên ground truth set.
- [ ] Report đơn giản: count mỗi label + accuracy per-label.

## Structure

```
lab-03-batch-classifier/
├── main.py              ← driver (TODO)
├── classify.py          ← batch LLM classifier (TODO)
├── cascade.py           ← cheap->expensive routing (TODO)
├── db.py                ← SQLite wrapper
├── report.py            ← accuracy + counts
├── data/
│   ├── items.jsonl
│   └── ground_truth.jsonl
├── requirements.txt
├── .env.example
└── README.md
```

## Gợi ý

- Batch prompt: liệt kê items với ID rõ ràng, yêu cầu LLM trả theo thứ tự + preserve ID.
- Tool-as-schema với `input_schema` là `list[object]` có item_id bắt buộc → buộc LLM không miss ID.
- Cascade: sau batch đầu, `[r for r in results if r.confidence < 0.7]` → gửi tiếp với model đắt.
- Batch size sweet spot 10–20. Thử 5/10/20/50 → note latency + accuracy + cost.

## Phản biện

- Batch quá to → LLM miss items hoặc confuse ID → sai. Cap 20.
- Cascade không luôn rẻ hơn. Nếu >80% item cần escalate → bỏ cascade, chạy thẳng expensive.
- **LLM không phải lúc nào cũng đúng classifier.** Dataset lớn (>10K labeled) → fine-tune model nhỏ rẻ hơn 100×. LLM mạnh khi cold-start, schema đổi thường, hoặc reasoning per-item.

## Khi xong

- Chạy với 3 batch size khác nhau, chart latency/accuracy/cost.
- Thử với model rẻ ngoài Anthropic (qua gateway OpenAI-compat) xem ảnh hưởng ra sao.
