# Glossary EN-VN — 40 thuật ngữ cốt lõi

Gặp term nào chưa rõ, tra đây trước khi Google.

| EN | VN | Giải thích 1 câu |
|---|---|---|
| Agent | Tác tử | Chương trình dùng LLM để tự quyết định bước tiếp theo trong vòng lặp có tool |
| Agent loop | Vòng lặp tác tử | `while not done: LLM → tool → result → LLM` cho đến khi LLM nói "xong" |
| LLM | Mô hình ngôn ngữ lớn | Claude, GPT, Gemini… cái nhận text trả text |
| Context window | Cửa sổ ngữ cảnh | Tổng tokens (in + out) 1 request chứa được |
| Token | Token | ~4 ký tự EN, ~2 ký tự VN; đơn vị tính tiền |
| Prompt | Lời nhắc / câu đầu vào | Text gửi cho LLM |
| System prompt | Prompt hệ thống | Hướng dẫn role/rules gửi kèm mỗi request |
| Temperature | Độ ngẫu nhiên | 0 = xác định, 1 = sáng tạo; agent thường 0–0.2 |
| Tool use | Gọi công cụ | LLM trả JSON báo "gọi tool X với arg Y", code mình chạy và feed kết quả lại |
| Tool schema | Giản đồ công cụ | JSON Schema mô tả tên/args của tool cho LLM |
| Structured output | Đầu ra có cấu trúc | Output JSON theo schema, không phải text tự do |
| Tool-as-schema | Dùng tool làm schema | Pattern ép structured output bằng cách đăng ký tool rồi ép `tool_choice` |
| JSON mode | Chế độ JSON | Ép LLM trả JSON thuần (kém ổn hơn tool-as-schema) |
| Stop reason | Lý do dừng | `end_turn`, `tool_use`, `max_tokens` — agent loop rẽ nhánh theo cái này |
| Prompt caching | Cache lời nhắc | Cache phần prompt tĩnh, giá 1/10 khi hit; TTL 5 phút |
| Streaming | Truyền phần dần | Nhận response từng chunk thay vì đợi cả khối |
| Pipeline | Dây chuyền | Kiến trúc tuyến tính step A → B → C, không loop |
| Memory (conversation) | Trí nhớ hội thoại | `messages[]` list trong 1 session |
| Memory (episodic) | Trí nhớ sự kiện | Lưu DB giữa các session |
| RAG | Truy hồi + sinh | Retrieval-Augmented Generation: tìm doc liên quan, nhét vào prompt |
| Vector DB | DB vector | Tìm theo nghĩa (embedding similarity) |
| Embedding | Nhúng | Vector số biểu diễn đoạn text, dùng để so nghĩa |
| HITL | Người trong vòng | Human-in-the-loop: người duyệt output trước khi execute |
| Centaur pattern | Mẫu nhân mã | Kiến trúc người + AI + code cùng ra quyết định |
| Orchestrator | Nhạc trưởng | Agent cha điều phối các sub-agent |
| Sub-agent | Tác tử con | Agent chuyên 1 role, được orchestrator gọi |
| Evidence gate | Cổng bằng chứng | Sub-agent claim "done" phải kèm proof (file/diff) |
| Blast radius | Bán kính ảnh hưởng | Thay đổi này ảnh hưởng bao nhiêu file / hệ thống |
| Guardrail | Rào chắn | Check input/output để tránh abuse (token cap, content filter) |
| Retry / backoff | Thử lại / lùi dần | Gọi lại API khi lỗi, delay tăng dần (exponential) |
| Idempotent | Bất biến khi lặp | Gọi 2 lần cùng input cho cùng kết quả, không tạo dup |
| Eval | Đánh giá | Test cho agent — scenario + expected output |
| LLM-as-judge | LLM làm trọng tài | Dùng LLM khác đánh giá output của LLM chính |
| Hallucination | Ảo giác | LLM tự bịa thông tin không có trong input |
| Prompt injection | Tiêm lời nhắc | User input chèn instruction lấn át system prompt |
| MCP | Model Context Protocol | Chuẩn kết nối tool/data với LLM, do Anthropic mở |
| Function calling | Gọi hàm | Tên cũ của tool use (OpenAI dùng từ này) |
| Cost tier | Bậc chi phí | Model rẻ / trung / đắt; route task theo bậc |
| Model routing | Định tuyến mô hình | Chọn model phù hợp per-step (Haiku classify, Sonnet reasoning) |
| Cascade | Tầng | Thử cheap trước, escalate expensive khi confidence thấp |
| Provider abstraction | Trừu tượng provider | Wrap SDK để đổi Claude ↔ OpenAI ↔ Gemini không đổi logic |
| Rate limit | Giới hạn tần suất | Cap request/minute của API, cần retry khi 429 |
| Reasoning discipline | Kỷ luật tư duy | MECE + clarify + counter-argument + 5-step verify |
| MECE | Đầy đủ không trùng | Mutually Exclusive, Collectively Exhaustive khi liệt kê |
| Decision tree | Cây quyết định | Nhánh if-else nhiều tầng để chọn path |
| Decision matrix | Ma trận quyết định | Bảng option × tiêu chí để so sánh |
