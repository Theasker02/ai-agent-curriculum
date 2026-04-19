# Week 0 — Setup & SDK Basics

**Mục tiêu:** môi trường chạy được, bạn gọi được LLM API và hiểu request/response cơ bản.
**Thời gian:** 0.5–2 ngày.

## Checklist

- [ ] Python 3.11+ (`python --version`)
- [ ] `pip install anthropic python-dotenv`
- [ ] API key tại provider (Anthropic/OpenAI/Gemini) — nạp credit nhỏ để thử
- [ ] Lưu `.env` (KHÔNG commit): `ANTHROPIC_API_KEY=...`
- [ ] Clone repo này, tạo venv

## Warm-up (tự viết, không copy)

Mục đích: gọi được 1 request đơn giản, in response + usage tokens.

```python
import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
client = Anthropic()

response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=200,
    messages=[{"role": "user", "content": "Giải thích agent loop trong 3 câu."}],
)
print(response.content[0].text)
print(f"Tokens: in={response.usage.input_tokens} out={response.usage.output_tokens}")
```

## Concept cốt lõi cần nằm lòng

| Concept | Giải thích 1 câu | Tại sao quan trọng |
|---|---|---|
| Context window | Tổng tokens 1 request chịu được | Vượt = cắt hoặc lỗi |
| Token | ~4 ký tự EN, ~2 ký tự VN | Đơn vị tính tiền |
| Input vs output price | Output đắt gấp ~5× input | Đừng in lại context vào output |
| Temperature | 0 = xác định, 1 = sáng tạo | Agent thường 0–0.2 |
| Stop reason | `end_turn`, `max_tokens`, `tool_use` | Agent loop rẽ nhánh theo đây |
| Model tier | cheap / default / premium | Chọn theo cost-vs-quality |

## Quy tắc chọn model (áp dụng xuyên suốt)

- Default tier trung bình (Sonnet-class) cho mọi task.
- Hạ tier rẻ khi task đơn giản + bulk (classify, extract đơn giản).
- Lên tier cao khi reasoning khó (code phức tạp, multi-step logic).

Tránh: hard-code 1 model khắp codebase → 1 biến `DEFAULT_MODEL` trong config.

## Checklist hoàn thành

- [ ] Warm-up script chạy được, in response + usage.
- [ ] Biết 3 tier model + khi nào dùng.
- [ ] Đọc lướt `reference/stack-mapping.md` để thấy 3 provider giống/khác chỗ nào.

## Bẫy thường gặp

- Commit `.env` vào git — check `.gitignore` trước commit đầu.
- Dùng model cũ (3.x) vì tutorial cũ — luôn check model mới nhất.
- `print(response)` xem lộn xộn — `response.content` là list, lấy `[0].text`.
