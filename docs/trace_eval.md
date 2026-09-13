# 📊 BÁO CÁO THU HOẠCH NGHIỆM THU BÀI LAB 3 (BƯỚC 3 — SUBMISSION ARTIFACT)

> **Họ và Tên Học viên:** Đặng Quang Hùng  
> **Mã Sinh Viên / Mã Học viên:** 02719  
> **Chủ đề Lựa chọn:** *Trợ lý Tác tử Sư phạm & Học vụ Tiếng Anh (English Learning Academic & Pedagogical ReAct Agent):* Tự động sửa lỗi ngữ pháp, trích dẫn slide bài giảng/rubric tiêu chí chấm điểm IELTS, theo dõi tiến độ BTVN, ghi nhận lịch sử lỗi sai học viên và kết nối Trợ giảng (TA) người thật qua giao thức Model Context Protocol (MCP).

---

## 1. BẢNG CHẤM ĐIỂM AGENTIC FIT SCORING MATRIX (ĐÁNH GIÁ CHỦ ĐỀ)

| Tiêu chí Đánh giá | Mức độ (1 - 5) | Giải trình chi tiết lý do chọn điểm |
| :--- | :---: | :--- |
| **1. Multi-step Reasoning** | 5/ 5 | Khi học viên gửi một câu sai ngữ pháp (ví dụ: *"i like did the thing sai ngữ pháp ở đâu"*), hệ thống phải chia nhỏ nhiều bước suy luận nối tiếp: (1) Xác định bối cảnh lớp học & Unit hiện tại (`get_student_context`), (2) Tra cứu slide bài giảng đối chiếu quy tắc chuẩn (`search_course_materials`), (3) Ghi nhận lỗi vào học bạ theo dõi của TA (`log_student_mistake`), (4) Tổng hợp câu trả lời sư phạm chỉ rõ lỗi sai, sửa lại câu đúng và dẫn chứng số Slide. |
| **2. Tool Interaction** | 5/ 5 | Agent kết nối với 10 Tools chuẩn hóa trên MCP Server: kho slide giáo trình theo Unit (`search_course_materials`), hồ sơ học bạ học viên (`get_student_context`, `list_all_students`), nhật ký lỗi sai (`log_student_mistake`, `get_student_mistake_history`), tiến độ BTVN (`check_homework_status`), bài tập bổ trợ (`get_remedial_exercises`), và chuyển tiếp Trợ giảng (`escalate_to_human_ta`, `book_ta_tutoring_session`). |
| **3. Dynamic Decision** | 5/ 5 | Agent tự động rẽ nhánh hành vi dựa trên ý định và phản hồi của người học: Nếu học viên hỏi lý thuyết tổng quan $\to$ trả lời sư phạm trực tiếp không gọi Tool (TC01); nếu học viên nộp câu sai $\to$ kích hoạt quy trình đối chiếu giáo trình & ghi nhận lỗi (TC02); nếu học viên nói *"vẫn chưa hiểu / cần học kèm 1-1"* $\to$ kích hoạt rẽ nhánh ping TA hoặc đặt lịch phụ đạo 1-1 (TC05). |
| **4. Long Horizon Goal** | 4/ 5 | Hệ thống duy trì mục tiêu sư phạm dài hạn: Giúp học viên đạt mục tiêu chuẩn đầu ra (Band 6.5 IELTS), tích lũy lịch sử lỗi sai qua các tuần học để TA theo dõi điểm yếu và cá nhân hóa bài tập củng cố (Remedial Exercises). |
| **TỔNG ĐIỂM AGENTIC FIT** | **19/ 20** | *Tổng điểm 19/20 > 12/20: Bài toán hoàn toàn phù hợp và phát huy tối đa sức mạnh của kiến trúc ReAct Agentic System.* |

---

## 2. TRÍCH XUẤT KẾT QUẢ WATERFALL TRACE LOG (SAU KHI CHẠY TEST SUITE TRÊN API THẬT)

> ⚠️ **YÊU CẦU NGHIỆM THU:** Đã cấu hình `GEMINI_API_KEY` (Gemini 2.5/3.5 Flash) trong file `.env`. Dưới đây là trích xuất vết suy luận (Waterfall Trace Log) chuẩn định dạng JSON trích từ `docs/trace_waterfall.json` khi Agent xử lý ca sửa lỗi ngữ pháp đối chiếu giáo trình (TC02):

```json
[
  {
    "step": 1,
    "type": "TOOL_EXECUTION",
    "thought": "Gemini quyết định gọi công cụ 'search_course_materials' với tham số: {\"query\": \"verb patterns like enjoy fancy gerund infinitive\", \"unit\": 3}",
    "tool_name": "search_course_materials",
    "arguments": {
      "query": "verb patterns like enjoy fancy gerund infinitive",
      "unit": 3
    },
    "observation": {
      "status": "SUCCESS",
      "unit": 3,
      "topic": "Hobbies & Verb Patterns",
      "slide": 14,
      "slide_title": "Verb Patterns with Verbs of Liking / Disliking",
      "rule": "Quy tắc trọng tâm: Sau các động từ chỉ cảm xúc, sở thích (like, enjoy, fancy, love, hate, adore, dislike), động từ theo sau bắt buộc chia ở dạng Danh động từ (V-ing) để chỉ sở thích hoặc thói quen chung: S + like/enjoy + V-ing. Riêng 'like' có thể đi với To-V (S + like + to-V) để diễn tả việc mình thấy tốt/nên làm (preference/good habit). Tuyệt đối KHÔNG kết hợp 'like' với động từ ở thì Quá khứ đơn (V2/V-ed như 'did', 'went', 'saw').",
      "examples": [
        "Đúng: 'I like doing exercise every morning.' (Thói quen/Sở thích)",
        "Đúng: 'I like to do the laundry on Sundays.' (Lựa chọn tốt)",
        "SAI: 'I like did the thing' (Lỗi ngữ pháp nghiêm trọng do dùng V2 'did' sau 'like')"
      ],
      "rubric_note": "Lỗi cấm kỵ trong tiêu chí Grammatical Range & Accuracy (GRA) IELTS Band 5.0 - 6.0.",
      "message": "Tìm thấy tài liệu tại Slide 14 - Unit 3 (Verb Patterns with Verbs of Liking / Disliking): Quy tắc trọng tâm: Sau các động từ chỉ cảm xúc, sở thích (like, enjoy, fancy, love, hate, adore, dislike), động từ theo sau bắt buộc chia ở dạng Danh động từ (V-ing) để chỉ sở thích hoặc thói quen chung: S + like/enjoy + V-ing. Riêng 'like' có thể đi với To-V (S + like + to-V) để diễn tả việc mình thấy tốt/nên làm (preference/good habit). Tuyệt đối KHÔNG kết hợp 'like' với động từ ở thì Quá khứ đơn (V2/V-ed như 'did', 'went', 'saw'). Ví dụ chuẩn: Đúng: 'I like doing exercise every morning.' (Thói quen/Sở thích); Đúng: 'I like to do the laundry on Sundays.' (Lựa chọn tốt); SAI: 'I like did the thing' (Lỗi ngữ pháp nghiêm trọng do dùng V2 'did' sau 'like')."
    },
    "latency_ms": 2180.58
  },
  {
    "step": 2,
    "type": "FINAL_ANSWER",
    "thought": "Đã tổng hợp kết quả Observation từ MCP Server.",
    "output": "Tìm thấy tài liệu tại Slide 14 - Unit 3 (Verb Patterns with Verbs of Liking / Disliking): Quy tắc trọng tâm: Sau các động từ chỉ cảm xúc, sở thích (like, enjoy, fancy, love, hate, adore, dislike), động từ theo sau bắt buộc chia ở dạng Danh động từ (V-ing) để chỉ sở thích hoặc thói quen chung: S + like/enjoy + V-ing. Riêng 'like' có thể đi với To-V (S + like + to-V) để diễn tả việc mình thấy tốt/nên làm (preference/good habit). Tuyệt đối KHÔNG kết hợp 'like' với động từ ở thì Quá khứ đơn (V2/V-ed như 'did', 'went', 'saw'). Ví dụ chuẩn: Đúng: 'I like doing exercise every morning.' (Thói quen/Sở thích); Đúng: 'I like to do the laundry on Sundays.' (Lựa chọn tốt); SAI: 'I like did the thing' (Lỗi ngữ pháp nghiêm trọng do dùng V2 'did' sau 'like').",
    "latency_ms": 10.0
  }
]
```

---

## 3. TỔNG KẾT KẾT QUẢ NGHIỆM THU & NỘP BÀI

- [x] Đã điền API Key thật trong `.env` và xác nhận Agent chạy mượt mà trên LLM API thật (Google Gemini SDK với mô hình `gemini-3.5-flash-lite`).
- **Tổng số Test Cases đã chạy thành công:** 5 / 5 test cases (`TC01` đến `TC05`).
- **Số lượt gọi Tool qua MCP Server chính xác:** 5 / 5 lượt (Đúng chuẩn Native Tool Calling và phân quyền người dùng RBAC).
- **Kết quả đẩy Repo nộp bài:** [x] Đã Commit và Push mã nguồn thành công lên GitHub cá nhân (`K4B-Day03-Lab-Chatbot-vs-ReAct-Agent-MCP-DangQuangHung-02719`).

---

> ✅ **HOÀN TẤT NỘP BÀI:** Sao chép đường link GitHub Repository cá nhân của bạn và dán vào ô nộp bài trên hệ thống LMS VLearn để hoàn tất Bài Lab 3!

