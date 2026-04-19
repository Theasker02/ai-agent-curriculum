# Week 1 — Nền tảng: Agent đơn

**Mục tiêu:** hiểu chính xác 1 agent gồm những gì, build được agent loop tối thiểu có tool + structured output.
**Thời gian:** 1 tuần.
**Lab:** `labs/lab-01-hello-agent/`

## Lý thuyết

### 1. Agent = gì?

Agent KHÔNG phải "LLM trả lời thông minh". Agent là:

```
while not done:
    response = LLM(prompt + history + tools)
    if response.stop_reason == "tool_use":
        tool_result = execute_tool(response.tool_call)
        history.append(tool_result)
    else:
        done = True
```

Bắt buộc có: **(1) tools, (2) loop, (3) điều kiện dừng, (4) state/history**. Thiếu 1 trong 4 → không phải agent, chỉ là prompt.

### 2. Tool use

Tool = schema JSON + handler code. LLM không tự chạy tool — mình chạy, feed kết quả lại.

```python
tools = [{
    "name": "do_x",
    "description": "Tả ngắn gọn, tự nhiên. LLM đọc cái này để quyết định có gọi hay không.",
    "input_schema": {"type": "object", "properties": {...}, "required": [...]},
}]
```

Quy tắc vàng:
- **Description tự nhiên, không jargon.** LLM đọc đây để chọn tool.
- **Schema chặt** (required, enum khi có thể) → giảm hallucination.
- **Tool idempotent** nếu có thể → LLM đôi khi gọi lại, đừng để gọi 2 lần tạo 2 record.

### 3. Structured output

2 cách chính:

| Cách | Khi nào dùng |
|---|---|
| JSON mode thô | Extract đơn giản, không quá chặt |
| **Tool-as-schema** | Default — ổn định 10× hơn JSON mode thô |

Tool-as-schema: đăng ký 1 tool có `input_schema` khớp dataclass/Pydantic, ép `tool_choice` → LLM buộc gọi → lấy `tool_use.input`.

### 4. Prompt caching

Phần prompt tĩnh (system + tool defs + doc lớn) có thể cache. Hit cache = giá 1/10.

```python
{"type": "text", "text": LARGE_STATIC, "cache_control": {"type": "ephemeral"}}
```

Dùng khi: system + tool defs dài hơn ~1000 tokens và lặp lại nhiều request.

### 5. Model routing trong 1 agent

1 agent có thể gọi **nhiều model khác nhau** trong 1 flow:

- Classify intent / extract đơn giản → tier rẻ.
- Reasoning / quyết định hành động → tier trung.
- Reasoning cực khó → tier cao (rare).

Pattern này gọi là **model routing** hoặc **cascade**. Áp dụng ở lab-03 tuần 3.

### 6. Provider abstraction (nền tảng)

Đừng viết agent logic gọi thẳng SDK 1 provider. Wrap qua 1 interface:

```python
class LLMClient(Protocol):
    def complete(self, messages, tools, **kw) -> Response: ...
```

Agent logic gọi interface. Đổi provider = đổi adapter, không đổi agent.

## Lab tuần 1

Đến `labs/lab-01-hello-agent/README.md`. Làm đúng acceptance criteria.

## Deliverable

- [ ] Lab-01 chạy pass.
- [ ] Viết ~150 từ trả lời: "Khi nào dùng tool use, khi nào chỉ prompt là đủ?"
- [ ] Note 3 concept khó nhất vào `reference/glossary-vn.md` nếu chưa có.

## Bẫy

- **Over-prompt.** System prompt 2000 từ → cắt còn 500, move constraint vào tool description.
- **Không loop.** Gọi LLM 1 lần, thấy `tool_use` rồi in ra — chưa execute. Agent phải **loop tới khi `end_turn`**.
- **Hard-code model.** Rải `model="..."` khắp code → 1 biến `DEFAULT_MODEL`.
- **`while True` không max_iters.** LLM hallucinate có thể loop vô hạn — đặt `MAX_ITERS = 10`.
