# Reasoning Discipline — đọc xuyên suốt 4 tuần

Senior dev đã có coding discipline. Kỹ năng tách biệt giữa "agent engineer tốt" và "coder gọi LLM" nằm ở đây.

## 1. Clarify-first (ambiguity gate)

Trước khi viết code / gọi LLM, hỏi lại khi có ít nhất 1 trong:
- Task có ≥ 2 cách hiểu hợp lý.
- Blast radius > 1 file hoặc chạm shared system (DB, deploy, config).
- Thiếu thông tin bắt buộc (schema, version, ngưỡng).

Không hỏi với task đọc thuần, confirm "ok/tiếp", câu chào.

**Quy tắc:** câu hỏi làm rõ luôn đi kèm **phương án mặc định** + **phản biện ngắn**, để người kia có thể trả lời "OK default" mà không phải tự nghĩ.

Ví dụ xấu: "Bạn muốn dùng Haiku hay Sonnet?"
Ví dụ tốt: "Mặc định tao dùng Haiku vì batch classify + 80% confidence là đủ. Rủi ro: ~15% case Haiku miss nuance — sẽ escalate lên Sonnet khi confidence < 0.7. Đồng ý?"

## 2. Counter-argument (phản biện) — BẮT BUỘC với mọi đề xuất kỹ thuật

Với **mọi** thay đổi config, refactor, thêm dependency, đổi kiến trúc → phải nêu ≥ 1 rủi ro / trade-off / edge case trước khi làm.

Không phản biện cho: confirm, báo cáo trạng thái, câu hỏi tra cứu.

Phản biện phải **cụ thể**: chỉ rõ file / flow / kịch bản. Không "có thể có vấn đề".

## 3. Chọn khung tư duy theo độ phức tạp (MECE-first)

- **MECE** (mặc định): mọi lần phân loại / liệt kê option phải Mutually Exclusive, Collectively Exhaustive.
- **Decision tree**: khi quyết định có **điều kiện phân nhánh** (if-else nhiều tầng).
- **Decision matrix**: khi so sánh **≥ 3 phương án trên ≥ 2 tiêu chí**.

Chọn khung **nhẹ nhất đủ dùng**. Task có 1 lựa chọn hiển nhiên → nói thẳng, không ép khung.

## 4. 5-step verification (trước khi claim "done" / "pass")

1. Identify the proof command.
2. Run the FULL command (không cached, không truncated).
3. Đọc COMPLETE output + exit code.
4. Verify output MATCHES claim.
5. ONLY THEN make the claim.

Áp dụng: test pass? chạy đủ test suite và đọc cuối. Agent "done"? mở file ra check diff thực sự.

## 5. Giả định tường minh

Khi task chạm > 1 file, liệt kê bảng:

| Giả định | Vì sao | Nếu sai |
|---|---|---|

Tầm thường nghe, nhưng ép mình viết ra buộc não phải phát hiện giả định ngầm.

## 6. Áp dụng vào agent engineering

| Nguyên tắc | Áp dụng agent |
|---|---|
| Clarify-first | Hỏi user schema output trước khi tune prompt 10 lần |
| Counter-argument | "Thêm RAG để xử lý X" — rủi ro: vector DB thêm latency + cost + chỗ bug. Dùng SQLite keyword search trước? |
| MECE | Phân loại tool: data-read / data-write / external-action. Không trộn |
| 5-step verify | LLM claim "classified all 30 items" — SELECT COUNT(*) FROM classifications, check đúng 30 |
| Giả định | "Giả định Haiku đủ cho classify" → nếu sai: accuracy < 80% → cascade Sonnet |

## 7. Anti-patterns thường thấy ở senior mới làm agent

| Anti-pattern | Triệu chứng | Fix |
|---|---|---|
| Prompt 2000 từ | System prompt dài, output vẫn sai | Cắt còn 500 từ, move constraints vào tool schema |
| "Agent sẽ tự hiểu" | Không eval, tin LLM | Viết 20 test case scenario, chạy mỗi lần đổi prompt |
| Vector DB từ đầu | Corpus 100 docs đã dùng Qdrant | SQLite FTS trước, upgrade khi > 10K |
| Multi-agent cho task đơn | Orchestrator 500 LOC fix bug 1-dòng | 1 call Sonnet đủ |
| Hard-code model | `model="claude-sonnet-4-6"` 20 chỗ | 1 biến `DEFAULT_MODEL`, inject qua config |
| Không log cost | "Sao hết tiền" | Log mỗi call, dashboard từ ngày 1 |

## 8. Bài tập cuối tuần (tự eval)

Cuối mỗi tuần, trả lời:
1. Quyết định kỹ thuật nào tuần này tao đã làm MÀ KHÔNG phản biện?
2. Có khoảnh khắc nào claim "done" mà không verify đủ 5-step?
3. Giả định nào ngầm mà nếu sai sẽ làm lab fail?

Nộp reflection cho mentor.
