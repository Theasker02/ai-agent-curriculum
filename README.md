# AI Agent Curriculum

Lộ trình 4 tuần cho senior dev tiếp cận AI agent: học **nền tảng** (cách agent hoạt động) + **pattern ứng dụng** (cách chọn kiến trúc cho use case thực).

Curriculum không gắn với domain cụ thể — bạn sẽ học pattern chung, rồi tự ánh xạ vào dự án của mình.

## Cách dùng

1. Fork repo này về máy.
2. Đọc [`ROADMAP.md`](./ROADMAP.md) để hiểu tổng thể (decision tree + matrix).
3. Làm theo thứ tự `weeks/week-0` → `week-4`. Mỗi tuần có 1 lab trong `labs/`.
4. Khi bí, mở `reference/` — đặc biệt `reasoning-discipline.md` đọc xuyên suốt.
5. Lab có skeleton + `TODO` marker. Tự code, không copy hoàn chỉnh.

## Nguyên tắc

- **Nền trước, framework sau:** học Claude SDK thô → LangGraph/CrewAI là phụ lục. Senior cần hiểu thấp mới debug được production.
- **Pattern, không domain:** mỗi lab là 1 archetype (agent đơn / pipeline / classifier / multi-agent). Dataset generic, bạn tự đổi sang domain mình.
- **Quick win tuần 1, ép chọn nhánh tuần 3:** không học cả 3 archetype. Chọn nhánh theo dự án thực sắp làm.
- **Reasoning discipline song song:** MECE + counter-argument + 5-step verify từ ngày 1.

## Yêu cầu môi trường

- Python 3.11+
- `ANTHROPIC_API_KEY` (hoặc tương đương — mapping provider ở `reference/stack-mapping.md`)
- Docker (chỉ cho tuần 4)

## Kết quả sau 4 tuần

- Hiểu agent loop, tool use, structured output, memory, HITL, multi-agent.
- Build được 1 agent hoàn chỉnh theo archetype đã chọn.
- Biết khi nào **không** nên dùng agent (phần lớn use case vẫn là script thường).
- Có thói quen clarify-gate + counter-argument trước khi code.

## Stack

Claude API làm trục chính. Mapping sang OpenAI/Gemini ở `reference/stack-mapping.md` — bạn có thể swap provider sau khi làm xong lab.
