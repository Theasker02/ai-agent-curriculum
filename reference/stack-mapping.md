# Stack Mapping — Claude ↔ OpenAI ↔ Gemini

Concept core giống nhau. API khác nhau ở tên field + 1–2 chi tiết.

## Model naming (tier equivalent, 2026-04)

| Tier | Claude | OpenAI | Gemini |
|---|---|---|---|
| Top reasoning | claude-opus-4-7 | gpt-5-pro | gemini-2.5-pro |
| Default | claude-sonnet-4-6 | gpt-5 | gemini-2.5-flash |
| Cheap bulk | claude-haiku-4-5 | gpt-5-mini | gemini-2.5-flash-lite |

Giá biến động, check console mỗi quý.

## Message format

### Claude

```python
messages = [
    {"role": "user", "content": "hi"},
    {"role": "assistant", "content": "hello"},
]
# system is a SEPARATE field, not in messages
client.messages.create(model=..., system="...", messages=messages)
```

### OpenAI

```python
messages = [
    {"role": "system", "content": "..."},
    {"role": "user", "content": "hi"},
]
client.chat.completions.create(model=..., messages=messages)
```

Khác biệt: Claude tách `system`, OpenAI gộp vào `messages`.

### Gemini

```python
# SDK native: genai.GenerativeModel(...).generate_content(...)
# Qua OpenAI-compat gateway: giống OpenAI.
```

## Tool use

### Claude

```python
tools = [{
    "name": "get_weather",
    "description": "...",
    "input_schema": {"type": "object", "properties": {...}},
}]
# response.content is a list of blocks. Filter block.type == "tool_use".
# Tool result: content=[{"type": "tool_result", "tool_use_id": ..., "content": ...}]
```

### OpenAI

```python
tools = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "...",
        "parameters": {"type": "object", "properties": {...}},
    },
}]
# response.choices[0].message.tool_calls — list of ToolCall objects
# Tool result: role="tool", tool_call_id=..., content=...
```

Khác biệt: Claude dùng `input_schema`, OpenAI dùng `parameters`. Claude `tool_use_id`, OpenAI `tool_call_id`. Cả hai là JSON Schema chuẩn.

### Gemini

```python
# function_declarations với parameters giống OpenAI.
```

## Structured output

| Provider | Cách khuyến nghị |
|---|---|
| Claude | Tool-as-schema với forced `tool_choice` |
| OpenAI | `response_format={"type": "json_schema", ...}` (native structured output) |
| Gemini | `response_schema=...` |

Cả 3 đều ổn định. Tool-as-schema portable nhất vì cả 3 đều có tool use.

## Streaming

| Provider | API |
|---|---|
| Claude | `with client.messages.stream(...) as stream:` |
| OpenAI | `stream=True`, iterate chunks |
| Gemini | `generate_content(stream=True)` |

## Caching

| Provider | Field |
|---|---|
| Claude | `cache_control: {"type": "ephemeral"}` trong content block |
| OpenAI | Tự động (prompt caching implicit với prompts > 1024 tokens) |
| Gemini | `cached_content` object, phải tạo trước |

Claude rõ ràng nhất (explicit). OpenAI giấu, không kiểm soát.

## Khi nào chọn provider nào

| Use case | Lựa chọn |
|---|---|
| Đọc/sửa code | Claude (Sonnet/Opus) |
| Reasoning dài + thinking rõ | Claude (extended thinking) |
| Function calling agent nhiều tool | Claude hoặc OpenAI, 50-50 |
| Classify/extract đơn giản rẻ | Gemini Flash Lite |
| Multi-modal video | Gemini |
| ChatGPT ecosystem / RAG native | OpenAI Assistants API |
| Rẻ nhất (có gateway lắp Gemini web) | Gemini qua gateway |

## Portable code pattern

Wrap provider vào 1 interface:

```python
class LLMClient(Protocol):
    def complete(self, messages: list, tools: list, **kwargs) -> Response: ...

class AnthropicAdapter: ...
class OpenAIAdapter: ...
```

Agent logic gọi interface, không gọi SDK trực tiếp. Khi đổi provider, đổi adapter thôi.

Nhiều team triển khai pattern này ở tầng HTTP bằng cách expose OpenAI-compatible schema (`/v1/chat/completions`) — gateway đứng giữa agent và provider thật, app không cần biết đang dùng backend nào.

## Cost comparison cheat (xấp xỉ USD / 1M tokens in, 2026-04)

| Model | In | Out |
|---|:-:|:-:|
| Opus 4.7 | ~15 | ~75 |
| Sonnet 4.6 | ~3 | ~15 |
| Haiku 4.5 | ~1 | ~5 |
| GPT-5 | ~2.5 | ~10 |
| GPT-5-mini | ~0.25 | ~1 |
| Gemini 2.5 Pro | ~1.25 | ~5 |
| Gemini 2.5 Flash | ~0.075 | ~0.3 |

Gemini Flash rẻ gấp 40× Sonnet. Use case classify bulk: Gemini. Reasoning: Claude.
