# Lab 01 — Hello Agent

**Tuần:** 1
**Thời gian:** 1–2 ngày
**Prerequisite:** Week 0 done.

## Mục tiêu

Build 1 agent loop tối thiểu: LLM + 2 tool + structured output.

## Yêu cầu chức năng

Agent nhận câu hỏi từ CLI, decide tool nào cần gọi:

1. `get_weather(city)` — mock trả weather fake (hard-code hoặc random).
2. `calculator(expression)` — eval biểu thức toán an toàn (KHÔNG dùng `eval()` thô, dùng `ast.literal_eval` hoặc `simpleeval`).
3. Cuối cùng, gọi `return_answer(answer, sources)` — tool-as-schema để output có cấu trúc.

## Acceptance criteria

```bash
$ python main.py "Thời tiết Hà Nội cộng 10 độ là bao nhiêu?"
{
  "answer": "Thời tiết Hà Nội hiện 25°C, cộng 10 độ = 35°C",
  "sources": ["get_weather(Hanoi)", "calculator(25+10)"]
}
```

- [ ] Agent gọi ≥ 2 tool khác nhau trong 1 query.
- [ ] Output cuối là JSON valid theo schema của `return_answer`.
- [ ] Agent loop dừng đúng khi `stop_reason == "end_turn"`.
- [ ] Log từng tool call ra stdout.
- [ ] Token total < 2000 cho query đơn giản.

## Structure

```
lab-01-hello-agent/
├── main.py            ← TODO: viết agent loop
├── tools.py           ← TODO: implement get_weather, calculator
├── requirements.txt   ← đã có
├── .env.example       ← copy sang .env
└── README.md          ← file này
```

## Gợi ý (đừng đọc nếu muốn tự nghĩ)

1. `main.py`:
   - Parse `sys.argv[1]` làm user input.
   - Tạo `messages = [{"role": "user", "content": ...}]`.
   - Loop: call `client.messages.create(model, tools, messages)`.
   - Nếu `stop_reason == "tool_use"`: extract tool_use block, chạy handler, append tool_result vào messages, loop tiếp.
   - Nếu `end_turn`: break.

2. `tools.py`: dict `TOOLS = {"get_weather": ..., "calculator": ..., "return_answer": ...}` với 2 key: `schema` (đưa cho LLM) và `handler` (function thật).

3. An toàn calculator: `simpleeval` package hoặc regex filter chỉ chấp nhận `0-9+-*/.()` .

## Phản biện khi làm

- Nếu code quá 150 LOC, mày đang over-engineer. Target ~80 LOC.
- Tool result PHẢI append vào `messages` với `role: "user"` và `content: [{"type": "tool_result", "tool_use_id": ..., "content": ...}]` — không phải string thường.
- Đừng dùng `while True` không có max_iters. Đặt `MAX_ITERS = 10` để tránh loop vô hạn khi LLM hallucinate.

## Khi xong

- Chạy `python main.py "..."` với 3 query khác nhau.
- Ghi cost/tokens vào comment đầu file.
- Chuyển sang `week-2-pipeline.md`.
