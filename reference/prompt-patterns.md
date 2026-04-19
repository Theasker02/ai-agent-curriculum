# Prompt Patterns — 7 pattern đủ dùng cho 90% agent

## 1. Role + Constraint prompt

```
You are <role>. Your job is <single task>.

Rules:
- <constraint 1>
- <constraint 2>

If <edge case>, do <specific action>.
```

Ngắn > dài. Cắt mọi câu không thay đổi hành vi LLM.

## 2. Tool-as-schema (structured output chính)

Thay vì ép JSON mode, đăng ký 1 tool với input_schema là output cần. Ép `tool_choice`. LLM buộc phải gọi → lấy `tool_use.input`.

```python
SAVE_TOOL = {
    "name": "save_result",
    "input_schema": MyPydanticModel.model_json_schema(),
}
response = client.messages.create(
    ...,
    tools=[SAVE_TOOL],
    tool_choice={"type": "tool", "name": "save_result"},
)
```

Ổn định hơn JSON mode thô 10x.

## 3. Few-shot examples (XML style)

```
<example>
<input>transcript mơ hồ</input>
<output>{"confidence": 0.4, ...}</output>
</example>
<example>
<input>transcript rõ</input>
<output>{"confidence": 0.9, ...}</output>
</example>
```

Claude train kỹ với XML tag. 2–3 example thường đủ. Nhiều hơn → cache hit giảm.

## 4. Prompt caching (tiết kiệm 90% cost)

Phần prompt lặp lại (system + tool defs + large doc): đánh dấu `cache_control`:

```python
messages = [{
    "role": "user",
    "content": [
        {"type": "text", "text": LARGE_DOC, "cache_control": {"type": "ephemeral"}},
        {"type": "text", "text": f"Question: {user_question}"},
    ],
}]
```

- TTL: 5 phút (standard) hoặc 1h (prefix với beta).
- Cache hit = giá 0.1× input.
- Chỉ cache phần tĩnh. Phần động (user input) cuối cùng.

## 5. Chain-of-thought controlled

Ép reasoning vào 1 field, không in ra:

```
Tool schema:
{
  "thinking": "...",   # LLM dùng để suy luận, không phải output cuối
  "answer": "...",     # output thực
}
```

Hoặc dùng extended thinking (Claude beta): reasoning tokens riêng, không tính vào response.

## 6. Self-critique / LLM-as-judge

```
Given the result below, rate it on:
- Correctness (0..1)
- Completeness (0..1)
- Confidence (0..1)

Return JSON. Be harsh.
```

Audit bằng tay random 10% — judge cũng hallucinate.

## 7. Reflexion loop (cho agent long-running)

Sau mỗi N step, cho agent tự review:
```
You've taken 10 actions. Review your trajectory:
- Có step nào redundant không?
- Còn thiếu info gì để hoàn thành task?
- Có nên đổi strategy?
```

Tăng cost nhưng giảm infinite loop.

---

## Anti-patterns

| Anti-pattern | Vấn đề | Thay bằng |
|---|---|---|
| "Be concise" trong prompt | LLM vẫn dài dòng | `max_tokens` + 1 câu ví dụ ngắn |
| "You are an expert at X" | Không đổi hành vi | Bỏ, viết rules cụ thể |
| Ép JSON bằng regex | Parse fail 5–10% | Tool-as-schema |
| Prompt 2000 từ dặn LLM "đừng làm gì cả" | LLM vẫn làm | Tool `allowed_actions` + check whitelist |
| Không test prompt | Đổi 1 câu, regress 3 case | `pytest` scenario + LLM-as-judge |

## Cheat-sheet bắt đầu

```python
from anthropic import Anthropic

client = Anthropic()

TOOL = {
    "name": "respond",
    "description": "Return your final answer.",
    "input_schema": {
        "type": "object",
        "properties": {"answer": {"type": "string"}},
        "required": ["answer"],
    },
}

response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1000,
    system="You are <role>. Return answer by calling `respond`.",
    tools=[TOOL],
    tool_choice={"type": "tool", "name": "respond"},
    messages=[{"role": "user", "content": user_input}],
)

# Find tool_use block
for block in response.content:
    if block.type == "tool_use" and block.name == "respond":
        print(block.input["answer"])
```

Dùng template này làm starter cho mọi prompt mới.
