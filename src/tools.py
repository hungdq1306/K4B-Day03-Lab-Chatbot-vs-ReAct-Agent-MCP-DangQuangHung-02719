"""
🛠️ ENGLISH LEARNING ACADEMIC ASSISTANT - PEDAGOGICAL REACT AGENT TOOLS & DATABASE
Chứa 10 Tools sư phạm, Kho giáo trình theo Unit, Hồ sơ học viên & Hệ thống theo dõi lỗi sai (Mistake Tracking).
"""

import json
from typing import Dict, Any, List, Optional

# ==============================================================================
# 1. HỒ SƠ TÀI KHOẢN & HỌC VIÊN (STUDENT PROFILES & USER ACCOUNTS)
# ==============================================================================

STUDENT_PROFILES = {
    "SV2026_HUNG": {
        "student_id": "SV2026_HUNG",
        "full_name": "Đặng Quang Hùng",
        "current_course": "IELTS Foundation",
        "current_unit": 3,
        "unit_title": "Unit 3: Hobbies & Verb Patterns (Gerund vs Infinitive)",
        "target_band": "6.5 IELTS",
        "ta_assigned": "Ms. Lan Anh (IELTS 8.0)",
        "ta_email": "lananh.ta@vinuni.edu.vn",
        "current_status": "Đang theo học tuần thứ 3",
        "homework_status": {
            "unit": 3,
            "title": "BTVN Unit 3: Verb Patterns & Daily Activities",
            "status": "Đang làm dở (Pending - Đã nộp 2/5 bài tập)",
            "deadline": "23:59 Chủ Nhật tuần này"
        },
        "mistake_history": [
            {"date": "10/09/2026", "unit": 2, "error_type": "Verb Pattern", "details": "Dùng 'enjoy went' thay vì 'enjoy going'", "count": 1},
            {"date": "12/09/2026", "unit": 3, "error_type": "Verb Pattern", "details": "Dùng 'love played' thay vì 'love playing'", "count": 2}
        ]
    },
    "SV2026_MAI": {
        "student_id": "SV2026_MAI",
        "full_name": "Lê Hoàng Mai",
        "current_course": "IELTS Intensive",
        "current_unit": 5,
        "unit_title": "Unit 5: Complex Sentences & Inversion",
        "target_band": "7.5 IELTS",
        "ta_assigned": "Mr. Minh Trí (IELTS 8.5)",
        "ta_email": "minhtri.ta@vinuni.edu.vn",
        "current_status": "Đang theo học tuần thứ 5",
        "homework_status": {
            "unit": 5,
            "title": "BTVN Unit 5: Inversion & Cleft Sentences in Writing Task 2",
            "status": "Đã nộp đầy đủ (Điểm: 8.5/10 - Nhận xét tốt)",
            "deadline": "Đã hoàn thành"
        },
        "mistake_history": [
            {"date": "05/09/2026", "unit": 4, "error_type": "Inversion", "details": "Thiếu trợ động từ đảo ngữ: 'Rarely I have seen'", "count": 1}
        ]
    },
    "SV2026_NAM": {
        "student_id": "SV2026_NAM",
        "full_name": "Trần Hải Nam",
        "current_course": "Grammar & Speaking Booster",
        "current_unit": 2,
        "unit_title": "Unit 2: Narrative Tenses & Past Habits",
        "target_band": "6.0 IELTS",
        "ta_assigned": "Ms. Thu Hà (IELTS 8.0)",
        "ta_email": "thuha.ta@vinuni.edu.vn",
        "current_status": "Đang theo học tuần thứ 2",
        "homework_status": {
            "unit": 2,
            "title": "BTVN Unit 2: Narrative Tenses & used to/would",
            "status": "Chưa nộp (Cảnh báo quá hạn 1 ngày)",
            "deadline": "Hôm qua 23:59"
        },
        "mistake_history": [
            {"date": "08/09/2026", "unit": 1, "error_type": "Tense Confusion", "details": "Nhầm lẫn giữa Past Simple và Past Continuous", "count": 3}
        ]
    }
}

STUDENT_DATABASE = STUDENT_PROFILES
USER_ACCOUNTS = STUDENT_PROFILES

# ==============================================================================
# 2. KHO GIÁO TRÌNH & SLIDE BÀI GIẢNG (COURSE MATERIALS & SLIDES)
# ==============================================================================

COURSE_MATERIALS = {
    3: {
        "unit": 3,
        "course": "IELTS Foundation",
        "topic": "Hobbies & Verb Patterns",
        "slides": [
            {
                "slide": 14,
                "title": "Verb Patterns with Verbs of Liking / Disliking",
                "rules": (
                    "Quy tắc trọng tâm: Sau các động từ chỉ cảm xúc, sở thích (like, enjoy, fancy, love, hate, adore, dislike), "
                    "động từ theo sau bắt buộc chia ở dạng Danh động từ (V-ing) để chỉ sở thích hoặc thói quen chung: S + like/enjoy + V-ing. "
                    "Riêng 'like' có thể đi với To-V (S + like + to-V) để diễn tả việc mình thấy tốt/nên làm (preference/good habit). "
                    "Tuyệt đối KHÔNG kết hợp 'like' với động từ ở thì Quá khứ đơn (V2/V-ed như 'did', 'went', 'saw')."
                ),
                "examples": [
                    "Đúng: 'I like doing exercise every morning.' (Thói quen/Sở thích)",
                    "Đúng: 'I like to do the laundry on Sundays.' (Lựa chọn tốt)",
                    "SAI: 'I like did the thing' (Lỗi ngữ pháp nghiêm trọng do dùng V2 'did' sau 'like')"
                ],
                "rubric_note": "Lỗi cấm kỵ trong tiêu chí Grammatical Range & Accuracy (GRA) IELTS Band 5.0 - 6.0."
            },
            {
                "slide": 15,
                "title": "Gerund vs Infinitive: Fixed Verb Lists",
                "rules": (
                    "Nhóm 1 (+ V-ing): enjoy, avoid, admit, mind, practice, suggest.\n"
                    "Nhóm 2 (+ To-V): decide, hope, promise, refuse, manage, want.\n"
                    "Nhóm 3 (cả hai, nghĩa không đổi): like, love, hate, start, begin."
                ),
                "examples": [
                    "I enjoy reading science fiction books.",
                    "She decided to take the IELTS exam in October."
                ],
                "rubric_note": "Cần học thuộc 15 động từ phổ biến trong bảng tổng kết trang 42 sách giáo trình."
            }
        ]
    },
    2: {
        "unit": 2,
        "course": "Grammar & Speaking Booster",
        "topic": "Narrative Tenses & Past Habits",
        "slides": [
            {
                "slide": 8,
                "title": "Past Continuous vs Past Simple in Storytelling",
                "rules": "Hành động dài đang xảy ra dùng Quá khứ tiếp diễn (was/were + V-ing), hành động ngắn xen vào dùng Quá khứ đơn (V2/V-ed).",
                "examples": [
                    "I was walking home when it suddenly started to rain."
                ],
                "rubric_note": "Mấu chốt để đạt Band 6.0+ tiêu chí Fluency & Coherence trong IELTS Speaking Part 2."
            }
        ]
    },
    5: {
        "unit": 5,
        "course": "IELTS Intensive",
        "topic": "Complex Sentences & Inversion",
        "slides": [
            {
                "slide": 21,
                "title": "Negative Adverb Inversion (Đảo ngữ với Trạng từ Phủ định)",
                "rules": "Cấu trúc: Trạng từ phủ định (Rarely, Seldom, Hardly, Under no circumstances) + Trợ động từ (do/does/did/have/has/modal) + Chủ ngữ + Động từ chính.",
                "examples": [
                    "Rarely have I seen such dedication.",
                    "Under no circumstances should students plagiarize essays."
                ],
                "rubric_note": "Cấu trúc điểm nhấn giúp nâng Band điểm GRA từ 7.0 lên 8.0 trong Writing Task 2."
            }
        ]
    }
}

# Danh bạ Trợ giảng (TA Directory)
TA_DIRECTORY = {
    "Ms. Lan Anh": {
        "name": "Ms. Lan Anh",
        "role": "Lead Teaching Assistant (IELTS 8.0)",
        "email": "lananh.ta@vinuni.edu.vn",
        "assigned_classes": ["IELTS Foundation", "IELTS Basic"],
        "office_hours": "Thứ 3 & Thứ 6 (18:00 - 20:30)",
        "telegram": "@lananh_ielts_ta",
        "status": "Available"
    },
    "Mr. Minh Trí": {
        "name": "Mr. Minh Trí",
        "role": "Senior Academic Tutor (IELTS 8.5)",
        "email": "minhtri.ta@vinuni.edu.vn",
        "assigned_classes": ["IELTS Intensive", "Writing Masterclass"],
        "office_hours": "Thứ 2 & Thứ 5 (19:00 - 21:00)",
        "telegram": "@minhtri_academic",
        "status": "Available"
    },
    "Ms. Thu Hà": {
        "name": "Ms. Thu Hà",
        "role": "Speaking & Grammar Tutor (IELTS 8.0)",
        "email": "thuha.ta@vinuni.edu.vn",
        "assigned_classes": ["Grammar & Speaking Booster"],
        "office_hours": "Thứ 4 & Thứ 7 (14:00 - 16:30)",
        "telegram": "@thuha_tutoring",
        "status": "Available"
    }
}

LECTURER_DATABASE = TA_DIRECTORY

# Kho bài tập bổ trợ củng cố (Remedial Exercises)
REMEDIAL_EXERCISES = {
    "verb_pattern": [
        {
            "question": "He enjoys (watch / watching / watched) football matches with his father on weekends.",
            "answer": "watching",
            "explanation": "Sau động từ 'enjoy' bắt buộc dùng V-ing (watching)."
        },
        {
            "question": "I like (to cook / cook / cooked) for my family when I have free time.",
            "answer": "to cook (hoặc cooking)",
            "explanation": "Sau 'like' dùng 'to cook' hoặc 'cooking', không dùng động từ nguyên thể không to hay quá khứ."
        }
    ],
    "inversion": [
        {
            "question": "Hardly ______ (he arrived / had he arrived) when the presentation started.",
            "answer": "had he arrived",
            "explanation": "Đảo ngữ với Hardly: Hardly + had + S + V3/ed."
        }
    ]
}


# ==============================================================================
# 3. KHAI BÁO 10 SCHEMAS CÔNG CỤ SƯ PHẠM (10 PEDAGOGICAL TOOLS SCHEMA)
# ==============================================================================

TOOLS_SCHEMA = [
    # Tool 1: Lấy bối cảnh học tập của học viên
    {
        "name": "get_student_context",
        "description": "Lấy bối cảnh học tập của học viên: lớp học hiện tại, Unit đang học, giáo trình, mục tiêu Band điểm và Trợ giảng (TA) phụ trách.",
        "parameters": {
            "type": "object",
            "properties": {
                "student_id": {
                    "type": "string",
                    "description": "Mã học viên (ví dụ: 'SV2026_HUNG', 'SV2026_MAI', 'SV2026_NAM')"
                }
            },
            "required": ["student_id"]
        }
    },

    # Tool 2: Tra cứu slide và tài liệu giáo trình lớp học
    {
        "name": "search_course_materials",
        "description": "Tra cứu slide bài giảng, quy tắc ngữ pháp chuẩn, ví dụ minh họa và rubric chấm điểm theo Unit trong giáo trình của trung tâm.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Từ khóa cấu trúc ngữ pháp cần tra (ví dụ: 'verb pattern like enjoy fancy', 'gerund infinitive')"
                },
                "unit": {
                    "type": "integer",
                    "description": "Số thứ tự Unit đang học (ví dụ: 3, 2, 5)"
                },
                "course_name": {
                    "type": "string",
                    "description": "Tên khóa học (tùy chọn, ví dụ: 'IELTS Foundation')"
                }
            },
            "required": ["query", "unit"]
        }
    },

    # Tool 3: Ghi nhận lỗi sai vào nhật ký học tập của học viên
    {
        "name": "log_student_mistake",
        "description": "Ghi nhận lỗi sai ngữ pháp mới vào hồ sơ theo dõi học tập của học viên để TA và Giảng viên theo dõi trong buổi học tiếp theo.",
        "parameters": {
            "type": "object",
            "properties": {
                "student_id": {
                    "type": "string",
                    "description": "Mã học viên mắc lỗi (ví dụ: 'SV2026_HUNG')"
                },
                "error_type": {
                    "type": "string",
                    "description": "Loại lỗi sai (ví dụ: 'Verb Pattern', 'Tense Confusion', 'Inversion')"
                },
                "details": {
                    "type": "string",
                    "description": "Chi tiết lỗi sai cụ thể của câu (ví dụ: 'Dùng like + did (V2) thay vì like + doing/to do')"
                },
                "unit": {
                    "type": "integer",
                    "description": "Unit tương ứng của bài học (ví dụ: 3)"
                }
            },
            "required": ["student_id", "error_type", "details"]
        }
    },

    # Tool 4: Xem lịch sử các lần mắc lỗi trước đây của học viên
    {
        "name": "get_student_mistake_history",
        "description": "Tra cứu lịch sử học tập xem học viên này đã mắc lỗi ngữ pháp này bao nhiêu lần trong quá khứ.",
        "parameters": {
            "type": "object",
            "properties": {
                "student_id": {
                    "type": "string",
                    "description": "Mã học viên cần xem lịch sử (ví dụ: 'SV2026_HUNG')"
                },
                "grammar_topic": {
                    "type": "string",
                    "description": "Chủ đề ngữ pháp cần lọc (mặc định: 'ALL')"
                }
            },
            "required": ["student_id"]
        }
    },

    # Tool 5: Kiểm tra tình trạng làm bài tập về nhà (BTVN)
    {
        "name": "check_homework_status",
        "description": "Kiểm tra tình trạng làm bài tập về nhà của tuần hiện tại (Đã nộp, Đang làm dở, Chưa làm, Hạn nộp).",
        "parameters": {
            "type": "object",
            "properties": {
                "student_id": {
                    "type": "string",
                    "description": "Mã học viên cần kiểm tra BTVN (ví dụ: 'SV2026_HUNG')"
                },
                "unit": {
                    "type": "integer",
                    "description": "Unit bài tập cần xem (ví dụ: 3)"
                }
            },
            "required": ["student_id"]
        }
    },

    # Tool 6: Chuyển tiếp / Ping Trợ giảng người thật (Human TA Escalation)
    {
        "name": "escalate_to_human_ta",
        "description": "Kích hoạt gửi thông báo ping Trợ giảng (TA) người thật khi học viên vẫn không hiểu bài sau khi giải thích hoặc yêu cầu hỗ trợ trực tiếp.",
        "parameters": {
            "type": "object",
            "properties": {
                "student_id": {
                    "type": "string",
                    "description": "Mã học viên cần hỗ trợ (ví dụ: 'SV2026_HUNG')"
                },
                "topic": {
                    "type": "string",
                    "description": "Chủ đề hoặc cấu trúc học viên đang gặp khúc mắc"
                },
                "student_message": {
                    "type": "string",
                    "description": "Câu hỏi hoặc vướng mắc chi tiết của học viên gửi tới TA"
                },
                "priority": {
                    "type": "string",
                    "description": "Mức độ ưu tiên ('NORMAL' hoặc 'URGENT')"
                }
            },
            "required": ["student_id", "topic", "student_message"]
        }
    },

    # Tool 7: Đặt lịch hẹn kèm 1-1 với Trợ giảng (TA Tutoring)
    {
        "name": "book_ta_tutoring_session",
        "description": "Đặt lịch hẹn phụ đạo 1-1 với Trợ giảng (TA) để giải đáp sâu về các phần ngữ pháp học viên bị hổng kiến thức.",
        "parameters": {
            "type": "object",
            "properties": {
                "student_id": {
                    "type": "string",
                    "description": "Mã học viên đăng ký (ví dụ: 'SV2026_HUNG')"
                },
                "ta_name": {
                    "type": "string",
                    "description": "Tên Trợ giảng (ví dụ: 'Ms. Lan Anh', 'Mr. Minh Trí')"
                },
                "timeslot": {
                    "type": "string",
                    "description": "Khung giờ học phụ đạo (ví dụ: '19:00 Thứ 6 18/09/2026')"
                },
                "topic": {
                    "type": "string",
                    "description": "Nội dung ôn tập cần phụ đạo (ví dụ: 'Củng cố Verb Patterns & Gerund Unit 3')"
                }
            },
            "required": ["student_id", "ta_name", "timeslot", "topic"]
        }
    },

    # Tool 8: Cung cấp bài tập luyện tập bổ trợ tức thì (Remedial Exercises)
    {
        "name": "get_remedial_exercises",
        "description": "Lấy 2-3 câu bài tập củng cố nhanh kèm lời giải thích theo đúng Unit để học viên tự luyện tập ngay sau khi sửa lỗi.",
        "parameters": {
            "type": "object",
            "properties": {
                "grammar_topic": {
                    "type": "string",
                    "description": "Chủ đề ngữ pháp (ví dụ: 'verb_pattern', 'inversion')"
                },
                "unit": {
                    "type": "integer",
                    "description": "Unit bài học (ví dụ: 3)"
                }
            },
            "required": ["grammar_topic"]
        }
    },

    # Tool 9: Danh sách học viên trong lớp
    {
        "name": "list_all_students",
        "description": "Xem danh sách học viên trong toàn bộ các lớp hoặc lọc theo khóa học.",
        "parameters": {
            "type": "object",
            "properties": {
                "class_filter": {
                    "type": "string",
                    "description": "Tên lớp/khóa học cần lọc (tùy chọn, ví dụ: 'IELTS Foundation')"
                }
            },
            "required": []
        }
    },

    # Tool 10: Xem đề cương lộ trình toàn khóa học (Syllabus)
    {
        "name": "list_course_syllabus",
        "description": "Tra cứu lộ trình các Unit bài học trong khóa học tiếng Anh.",
        "parameters": {
            "type": "object",
            "properties": {
                "course_name": {
                    "type": "string",
                    "description": "Tên khóa học (mặc định: 'IELTS Foundation')"
                }
            },
            "required": []
        }
    }
]


# ==============================================================================
# 4. HÀM THỰC THI TOOL (EXECUTION LAYER)
# ==============================================================================

def execute_get_student_context(student_id: str) -> str:
    """Thực thi lấy bối cảnh lớp học & học viên"""
    sid = student_id.strip().upper()
    profile = STUDENT_PROFILES.get(sid)
    if not profile:
        # Fallback tìm kiếm linh hoạt
        matched = next((p for s, p in STUDENT_PROFILES.items() if sid in s or s in sid), None)
        if matched:
            profile = matched
            sid = matched["student_id"]

    if profile:
        res = {
            "status": "SUCCESS",
            "student_id": sid,
            "full_name": profile["full_name"],
            "current_course": profile["current_course"],
            "current_unit": profile["current_unit"],
            "unit_title": profile["unit_title"],
            "target_band": profile["target_band"],
            "ta_assigned": profile["ta_assigned"],
            "ta_email": profile["ta_email"],
            "message": (
                f"Học viên: {profile['full_name']} ({sid}) - Lớp: {profile['current_course']} - "
                f"Đang học: Unit {profile['current_unit']} ({profile['unit_title']}). "
                f"Mục tiêu: {profile['target_band']}, TA phụ trách: {profile['ta_assigned']}."
            )
        }
        return json.dumps(res, ensure_ascii=False)
    return json.dumps({"status": "NOT_FOUND", "message": f"Không tìm thấy học viên có mã '{student_id}' trong hệ thống."}, ensure_ascii=False)


def execute_search_course_materials(query: str, unit: int = 3, course_name: str = "IELTS Foundation") -> str:
    """Thực thi tra cứu slide bài giảng & rubric giáo trình"""
    unit_data = COURSE_MATERIALS.get(unit)
    if not unit_data:
        # Tìm unit gần nhất
        unit_data = COURSE_MATERIALS.get(3)

    slides = unit_data.get("slides", [])
    q_lower = query.lower()
    matched_slide = None

    for s in slides:
        if any(term in s["rules"].lower() or term in s["title"].lower() for term in q_lower.split()):
            matched_slide = s
            break

    if not matched_slide and slides:
        matched_slide = slides[0]

    if matched_slide:
        formatted_examples = "\n  • ".join(matched_slide["examples"])
        res = {
            "status": "SUCCESS",
            "unit": unit,
            "topic": unit_data.get("topic", "Verb Patterns"),
            "slide": matched_slide["slide"],
            "slide_title": matched_slide["title"],
            "rule": matched_slide["rules"],
            "examples": matched_slide["examples"],
            "rubric_note": matched_slide["rubric_note"],
            "message": (
                f"📖 [GIẢI ĐÁP NGỮ PHÁP & TRÍCH DẪN GIÁO TRÌNH]\n"
                f"📌 Tài liệu tham khảo: Slide {matched_slide['slide']} - Unit {unit} ({matched_slide['title']})\n"
                f"💡 Quy tắc trọng tâm: {matched_slide['rules']}\n"
                f"✏️ Câu sửa chuẩn & Ví dụ đối chiếu:\n  • {formatted_examples}\n"
                f"⚠️ Lưu ý tiêu chí IELTS: {matched_slide['rubric_note']}"
            )
        }
        return json.dumps(res, ensure_ascii=False)

    return json.dumps({"status": "NOT_FOUND", "message": f"Không tìm thấy slide cho Unit {unit} với từ khóa '{query}'."}, ensure_ascii=False)


def execute_log_student_mistake(student_id: str, error_type: str, details: str, unit: int = 3) -> str:
    """Thực thi ghi nhận lỗi sai vào hồ sơ theo dõi của học viên"""
    sid = student_id.strip().upper()
    profile = STUDENT_PROFILES.get(sid)
    if profile:
        new_entry = {
            "date": "13/09/2026 (Hôm nay)",
            "unit": unit,
            "error_type": error_type,
            "details": details,
            "count": len(profile.get("mistake_history", [])) + 1
        }
        profile["mistake_history"].append(new_entry)
        total_times = len([m for m in profile["mistake_history"] if m["error_type"].lower() in error_type.lower()])
        msg = (
            f"✅ Đã ghi nhận lỗi '{error_type}' ({details}) vào hồ sơ học viên {profile['full_name']} ({sid}). "
            f"Học viên đã mắc lỗi thuộc dạng này tổng cộng {total_times} lần. Dữ liệu đã chuyển sang sổ theo dõi của TA {profile['ta_assigned']}."
        )
        return json.dumps({"status": "SUCCESS", "student_id": sid, "logged_entry": new_entry, "total_mistakes_in_topic": total_times, "message": msg}, ensure_ascii=False)
    return json.dumps({"status": "NOT_FOUND", "message": f"Không tìm thấy học viên '{student_id}' để ghi nhận lỗi."}, ensure_ascii=False)


def execute_get_student_mistake_history(student_id: str, grammar_topic: str = "ALL") -> str:
    """Thực thi xem lịch sử mắc lỗi của học viên"""
    sid = student_id.strip().upper()
    profile = STUDENT_PROFILES.get(sid)
    if profile:
        history = profile.get("mistake_history", [])
        if grammar_topic != "ALL":
            history = [h for h in history if grammar_topic.lower() in h["error_type"].lower()]
        
        detail_lines = [f"- {h['date']} (Unit {h['unit']}): {h['error_type']} - {h['details']}" for h in history]
        msg = f"Lịch sử lỗi sai của học viên {profile['full_name']} ({len(history)} lần ghi nhận): \n" + "\n".join(detail_lines)
        return json.dumps({"status": "SUCCESS", "student_id": sid, "history": history, "count": len(history), "message": msg}, ensure_ascii=False)
    return json.dumps({"status": "NOT_FOUND", "message": f"Không tìm thấy học viên '{student_id}'."}, ensure_ascii=False)


def execute_check_homework_status(student_id: str, unit: int = 3) -> str:
    """Thực thi kiểm tra tình trạng bài tập về nhà"""
    sid = student_id.strip().upper()
    profile = STUDENT_PROFILES.get(sid)
    if profile:
        hw = profile.get("homework_status", {})
        msg = (
            f"Tình trạng BTVN của học viên {profile['full_name']} ({sid}): "
            f"Bài tập: {hw.get('title', 'N/A')} - Trạng thái: {hw.get('status', 'N/A')} - Hạn nộp: {hw.get('deadline', 'N/A')}."
        )
        return json.dumps({"status": "SUCCESS", "student_id": sid, "data": hw, "message": msg}, ensure_ascii=False)
    return json.dumps({"status": "NOT_FOUND", "message": f"Không tìm thấy dữ liệu BTVN cho học viên '{student_id}'."}, ensure_ascii=False)


def execute_escalate_to_human_ta(student_id: str, topic: str, student_message: str, priority: str = "NORMAL") -> str:
    """Thực thi chuyển tiếp ca khó hoặc ping Trợ giảng người thật"""
    sid = student_id.strip().upper()
    profile = STUDENT_PROFILES.get(sid, {})
    ta_name = profile.get("ta_assigned", "Ms. Lan Anh")
    ta_info = TA_DIRECTORY.get(ta_name, TA_DIRECTORY["Ms. Lan Anh"])

    ticket_id = f"ESC-{sid}-2026"
    msg = (
        f"🚨 [TICKET #{ticket_id} ĐÃ TẠO]: Đã ping thông báo tới Trợ giảng người thật {ta_name} ({ta_info['email']}, {ta_info['telegram']}). "
        f"Nội dung cần hỗ trợ: '{topic}' - Lời nhắn học viên: '{student_message}'. Mức ưu tiên: {priority}. "
        f"TA {ta_name} sẽ liên hệ hỗ trợ bạn trong khung giờ trực tiếp ({ta_info['office_hours']})!"
    )
    return json.dumps({
        "status": "SUCCESS",
        "ticket_id": ticket_id,
        "ta_assigned": ta_name,
        "ta_contact": ta_info["telegram"],
        "priority": priority,
        "message": msg
    }, ensure_ascii=False)


def execute_book_ta_tutoring_session(student_id: str, ta_name: str, timeslot: str, topic: str) -> str:
    """Thực thi đặt lịch học kèm 1-1 với TA"""
    sid = student_id.strip().upper()
    profile = STUDENT_PROFILES.get(sid, {})
    booking_id = f"TUTOR-{sid}-09"
    msg = (
        f"📅 Đặt lịch phụ đạo 1-1 thành công! "
        f"Học viên: {profile.get('full_name', sid)} ({sid}) | Trợ giảng: {ta_name} | Thời gian: {timeslot} | "
        f"Chuyên đề ôn tập: '{topic}'. Mã buổi học: {booking_id}. Link phòng học trực tuyến đã gửi về email học viên."
    )
    return json.dumps({
        "status": "SUCCESS",
        "booking_id": booking_id,
        "student_id": sid,
        "ta_name": ta_name,
        "timeslot": timeslot,
        "topic": topic,
        "message": msg
    }, ensure_ascii=False)


def execute_get_remedial_exercises(grammar_topic: str, unit: int = 3) -> str:
    """Thực thi cung cấp bài tập củng cố tức thì"""
    key = "verb_pattern" if "verb" in grammar_topic.lower() or "like" in grammar_topic.lower() else "inversion"
    exercises = REMEDIAL_EXERCISES.get(key, REMEDIAL_EXERCISES["verb_pattern"])
    
    formatted = []
    for i, ex in enumerate(exercises, 1):
        formatted.append(f"Câu {i}: {ex['question']}\n   👉 Đáp án: {ex['answer']} ({ex['explanation']})")
    
    msg = f"Bài tập củng cố Unit {unit} ({key.upper()}):\n" + "\n".join(formatted)
    return json.dumps({"status": "SUCCESS", "topic": key, "exercises": exercises, "message": msg}, ensure_ascii=False)


def execute_list_all_students(class_filter: str = "") -> str:
    """Thực thi lấy danh sách toàn bộ học viên"""
    results = []
    cf = class_filter.strip().lower()
    for sid, p in STUDENT_PROFILES.items():
        if not cf or cf in p["current_course"].lower():
            results.append({
                "student_id": sid,
                "full_name": p["full_name"],
                "course": p["current_course"],
                "unit": p["current_unit"],
                "target": p["target_band"],
                "ta": p["ta_assigned"]
            })
    msg = f"Tìm thấy {len(results)} học viên: " + ", ".join([f"{r['full_name']} ({r['student_id']} - Lớp {r['course']})" for r in results])
    return json.dumps({"status": "SUCCESS", "count": len(results), "data": results, "message": msg}, ensure_ascii=False)


def execute_list_course_syllabus(course_name: str = "IELTS Foundation") -> str:
    """Thực thi xem đề cương khóa học"""
    syllabus = [
        {"unit": 1, "topic": "Introductions & Present Tenses", "focus": "Present Simple vs Present Continuous"},
        {"unit": 2, "topic": "Memories & Narrative Tenses", "focus": "Past Simple, Past Continuous & Used to"},
        {"unit": 3, "topic": "Hobbies & Verb Patterns", "focus": "Gerund vs Infinitive (like, enjoy + V-ing/to-V)"},
        {"unit": 4, "topic": "Future Plans & Predictions", "focus": "Will, Be Going to, Present Continuous for Future"},
        {"unit": 5, "topic": "Academic Arguments & Complex Sentences", "focus": "Conditionals, Relative Clauses & Inversion"}
    ]
    lines = [f"Unit {s['unit']}: {s['topic']} (Trọng tâm: {s['focus']})" for s in syllabus]
    msg = f"Đề cương khóa học '{course_name}':\n" + "\n".join(lines)
    return json.dumps({"status": "SUCCESS", "course": course_name, "syllabus": syllabus, "message": msg}, ensure_ascii=False)


# Router gọi tool thực tế (10 Tools)
TOOL_ROUTER = {
    "get_student_context": execute_get_student_context,
    "search_course_materials": execute_search_course_materials,
    "log_student_mistake": execute_log_student_mistake,
    "get_student_mistake_history": execute_get_student_mistake_history,
    "check_homework_status": execute_check_homework_status,
    "escalate_to_human_ta": execute_escalate_to_human_ta,
    "book_ta_tutoring_session": execute_book_ta_tutoring_session,
    "get_remedial_exercises": execute_get_remedial_exercises,
    "list_all_students": execute_list_all_students,
    "list_course_syllabus": execute_list_course_syllabus
}

# ==============================================================================
# 5. OPEN EXECUTION DISPATCHER
# ==============================================================================

def dispatch_tool_call(tool_name: str, arguments: Dict[str, Any], user_context: Optional[Dict[str, Any]] = None) -> str:
    """
    Hàm thực thi Tool trực tiếp của Trợ lý Học vụ Tiếng Anh (Open Execution Layer).
    """
    if tool_name not in TOOL_ROUTER:
        return json.dumps({"status": "UNKNOWN_TOOL", "error": f"Tool '{tool_name}' không tồn tại!"}, ensure_ascii=False)

    try:
        return TOOL_ROUTER[tool_name](**arguments)
    except Exception as e:
        return json.dumps({"status": "EXECUTION_ERROR", "error": str(e)}, ensure_ascii=False)
