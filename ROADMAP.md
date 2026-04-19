# ROADMAP — 4 tuần AI Agent cho Senior Dev

## Decision Tree lộ trình

```
[Start: senior dev thạo Python/HTTP/DB, chưa build agent]
  │
  ├─ Đã gọi LLM API ≥ 5 lần?
  │     NO  → Week-0 đọc kỹ "SDK basics" (1-2 ngày)
  │     YES → Week-0 chỉ setup env (nửa ngày)
  │
  ├─ Week 1: Nền — agent loop + tool use + structured output
  │   Lab-01: agent đơn có tool (toy use case)
  │
  ├─ Week 2: Pattern ứng dụng — pipeline + memory + HITL
  │   Lab-02: pipeline xử lý document (generic)
  │
  ├─ Week 3: CHỌN 1 NHÁNH (không học cả 3)
  │     ├─ Batch processing           → Lab-03 (classifier generic)
  │     └─ Multi-agent coordination   → Lab-04 (orchestrator + sub-agent)
  │
  ├─ Week 4: Production — deploy, log, eval, cost
  │
  └─ Xuyên suốt: reference/reasoning-discipline.md
```

Luật ép nhánh tuần 3: chọn theo **use case thực** sắp làm. Chưa có dự án → mặc định Batch (phổ biến nhất).

---

## Matrix 1 — Lab theo mục đích học

| Lab | Archetype | Học được | Tuần |
|---|---|---|:-:|
| **01 hello-agent** | Agent đơn | Agent loop, tool use, structured output | 1 |
| **02 doc-pipeline** | Pipeline tuyến tính | Memory, state, HITL, retry, validation | 2 |
| **03 batch-classifier** | Pipeline + routing | Batch, cascade model, eval, cost control | 3 (nhánh A) |
| **04 multi-agent** | Orchestrator | Sub-agent, evidence gate, context isolation | 3 (nhánh B) |

---

## Matrix 2 — Stack

| Stack | Mentor kèm được | Depth / abstraction | Khuyến nghị |
|---|:-:|:-:|---|
| **Claude API raw + MCP** | Cao | Thấp (hiểu sâu) | **Trục chính** |
| OpenAI SDK + LangGraph | Trung | Cao (debug khó) | Phụ lục tuần 4 |
| Provider-agnostic adapter | Cao | Trung | Học pattern ở tuần 1 |

Raw SDK thắng framework ở **debug production**. Senior bị abstraction che khuất thường ức chế hơn fresher.

---

## Matrix 3 — Khi nào KHÔNG dùng agent

Quan trọng ngang với "khi nào dùng". Phần lớn senior thất bại ở đây.

| Use case | Giải pháp đúng |
|---|---|
| Parse structured input (CSV, JSON) | Code thường |
| Regex / rule-based đủ chính xác | Code thường |
| Gọi API ổn định, output xác định | Code thường + 1 lần LLM extract |
| Cần xác định 100% đúng (financial, medical) | Code thường + human review, KHÔNG agent |
| Task có < 10 input case | Viết 10 if-else, không cần LLM |

Quy tắc: **agent = khi input/output đa dạng đến mức không viết được luật**. Còn lại → code thường.

---

## Giả định | Vì sao | Nếu sai

| Giả định | Vì sao | Nếu sai thì sao |
|---|---|---|
| Senior thạo Python/HTTP/DB | Định nghĩa senior | Frontend-only → thêm 3 ngày Python async + `httpx` |
| Có 4 tuần thực (~15h/tuần) | Chuẩn cho 1 skill mới | < 2 tuần: cắt week-3; 8+ tuần: thêm capstone |
| OK với Claude-first stack | Mentor stack match | Công ty dùng OpenAI: swap thứ tự Matrix 2 |
| Có API key | Lab cần gọi LLM | Không có: dùng Claude CLI free tier hoặc gateway community |

---

## Lịch chi tiết

| Tuần | Focus | Deliverable |
|---|---|---|
| 0 | Setup + SDK basics | `warmup.py` chạy được |
| 1 | Agent đơn + tool use | Lab-01 pass acceptance |
| 2 | Pipeline + memory + HITL | Lab-02 pass acceptance |
| 3 | Chọn 1 nhánh | Lab-03 HOẶC Lab-04 pass |
| 4 | Production | Dockerize lab tuần 3 + eval suite |

## Tham chiếu trong quá trình học

- `reference/reasoning-discipline.md` — đọc tuần 1, review cuối mỗi tuần
- `reference/prompt-patterns.md` — 7 pattern dùng đi dùng lại
- `reference/stack-mapping.md` — Claude ↔ OpenAI ↔ Gemini
- `reference/glossary-vn.md` — 40 thuật ngữ EN-VN

Version-date: 2026-04-19. SDK/doc có thể đổi — luôn đối chiếu nguồn chính thức.
