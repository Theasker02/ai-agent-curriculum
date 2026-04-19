# Week 3 — Chọn 1 nhánh (batch / multi-agent)

**Mục tiêu:** đi sâu 1 archetype, **không học cả hai**.
**Thời gian:** 1.5 tuần.

## Luật ép nhánh

Chọn theo **use case thực** sắp làm:

| Use case | Nhánh |
|---|---|
| Xử lý khối lượng lớn với classify/extract/transform | **A. Batch** (lab-03) |
| Nhiều role chuyên trách phối hợp trên 1 task | **B. Multi-agent** (lab-04) |
| Chưa có use case cụ thể | **A. Batch** (phổ biến hơn) |

Phản biện: **không chọn Multi-agent vì "nghe ngầu"**. Multi-agent debug khó gấp ~5× batch pipeline. 70%+ use case thực chỉ cần pipeline + tool use.

---

## Nhánh A — Batch Processing + Model Routing

**Lab:** `labs/lab-03-batch-classifier/`

### Concept thêm

- **Batch:** gộp N items / request → giảm cost (prompt 1 lần, output nhiều items). Sweet spot: 10–20 items/batch. > 50 → LLM miss.
- **Cascade model:** chạy tier rẻ trước. Items có confidence thấp → escalate tier cao. Lợi khi >70% item dễ.
- **Confidence scoring:** ép LLM trả `{result, confidence, reason}`. Filter threshold trước khi dùng.
- **Idempotent + cache:** hash input → cache kết quả. Rerun không tốn tiền.
- **Eval:** giữ ground-truth set nhỏ, đo accuracy sau mỗi đổi prompt/model.

### Khi nào nhánh này phù hợp

- Xử lý >100 items/batch mỗi lần.
- Schema output cố định, input đa dạng.
- Cost quan trọng (classify/extract/moderation…).

### Khi nào KHÔNG phù hợp

- < 20 items tổng → viết code tay rẻ hơn.
- Cần reasoning dài cho từng item → gửi đơn lẻ.
- Dataset đủ lớn (>10K labeled) → fine-tune model nhỏ còn rẻ hơn.

### Deliverable

- Lab-03 pass: classifier accuracy vượt baseline, cost trong budget.
- Benchmark: batch size nào tối ưu (thử 5/10/20/50 → chart latency vs cost).

---

## Nhánh B — Multi-Agent Coordination

**Lab:** `labs/lab-04-multi-agent-mini/`

### Concept thêm

- **Orchestrator + sub-agent:** 1 agent điều phối, nhiều sub-agent chuyên trách. Orchestrator không tự làm việc tay chân, chỉ delegate.
- **Role separation:** mỗi sub-agent có prompt + tool + schema output RIÊNG. Đừng share tool.
- **Evidence gate:** sub-agent claim "done" phải trả kèm proof (output có field bắt buộc). Thiếu = reject.
- **Blast radius awareness:** sub-agent có whitelist phạm vi được phép thay đổi.
- **Context isolation:** đừng truyền hết context cho mọi sub — mỗi sub chỉ nhận đủ cho role của nó. Giảm token + giảm hallucination.

### Khi nào nhánh này phù hợp

- Task có ≥ 3 role khác biệt rõ ràng (ví dụ nghiên cứu + viết + review).
- Cần audit được từng bước (sub-agent X quyết định gì, evidence đâu).
- Output cần multiple perspectives (critic/devil's advocate).

### Khi nào KHÔNG phù hợp

- Task đơn bước → 1 agent đủ, dồn lại.
- Sub-agent chỉ wrap 1 LLM call → xoá orchestrator, gọi thẳng.
- Debug time > saved time → đừng multi-agent.

Câu hỏi kiểm tra mỗi lần thêm sub-agent: "Nếu dồn sub này với sub kia thành 1, có hỏng gì không?" Nếu không → dồn.

### Deliverable

- Lab-04 pass: orchestrator điều phối 3 sub, có evidence gate, có test case reject.
- Log rõ từng sub-agent input/output để audit.

---

## Deliverable chung cuối tuần 3

- Lab của nhánh đã chọn chạy pass.
- Reflection ~200 từ: "Tại sao tôi chọn nhánh X cho use case Y của tôi?"

## Phản biện xuyên nhánh

- **A (Batch):** có vẻ nhàm. Nhưng đây là 70% thị trường. Đừng coi thường.
- **B (Multi-agent):** senior dev hay over-engineer ở đây. Default nghi ngờ: mỗi sub-agent phải justify được lý do tồn tại.
