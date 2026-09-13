"""
🔌 MULTI-PROVIDER LLM ADAPTER (Google Gemini, OpenAI & Offline Mock)
Hỗ trợ Native Tool Calling và chuyển đổi linh hoạt qua biến môi trường LLM_PROVIDER.
"""

import os
import sys
import json
from typing import Dict, Any, List
from dotenv import load_dotenv

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

load_dotenv()

class BaseLLMProvider:
    """Interface cơ sở cho các LLM Provider hỗ trợ Native Tool Calling"""
    def generate(self, prompt: str, system_prompt: str = "") -> str:
        raise NotImplementedError

    def generate_with_tools(self, prompt: str, tools_schema: List[Dict[str, Any]], system_prompt: str = "") -> Dict[str, Any]:
        raise NotImplementedError


class MockOfflineProvider(BaseLLMProvider):
    """Offline Mock Provider dùng để chạy thử mà không tốn API Key"""
    def __init__(self):
        self.model_name = "Offline-Mock-Model-2026"

    def generate(self, prompt: str, system_prompt: str = "") -> str:
        return f"[Chatbot Baseline Response]: Trong câu '{prompt}', 'like' thường đi với động từ thêm -ing (V-ing) hoặc to-V. Câu này sai vì ngữ pháp tiếng Anh không dùng did sau like."

    def generate_with_tools(self, prompt: str, tools_schema: List[Dict[str, Any]], system_prompt: str = "") -> Dict[str, Any]:
        prompt_lower = prompt.lower()
        
        # 1. Nhận diện truy vấn lỗi sai ngữ pháp (ví dụ: 'i like did the thing sai ngữ pháp ở đâu')
        if "like did" in prompt_lower or "sai ngữ pháp" in prompt_lower or "chữa câu" in prompt_lower:
            return {
                "type": "tool_call",
                "tool_name": "search_course_materials",
                "arguments": {"query": "verb pattern like enjoy fancy", "unit": 3, "course_name": "IELTS Foundation"},
                "thought": "Học viên đang hỏi chữa lỗi ngữ pháp trong câu. Cần tra cứu tài liệu Unit 3 để lấy đúng rubric và slide quy tắc của trung tâm."
            }

        # 2. Nhận diện kiểm tra BTVN
        elif "btvn" in prompt_lower or "bài tập về nhà" in prompt_lower:
            return {
                "type": "tool_call",
                "tool_name": "check_homework_status",
                "arguments": {"student_id": "SV2026_HUNG", "unit": 3},
                "thought": "Học viên yêu cầu kiểm tra tình trạng bài tập về nhà Unit 3. Tôi sẽ gọi tool check_homework_status."
            }

        # 3. Nhận diện tra cứu lịch sử lỗi sai
        elif "lịch sử" in prompt_lower or "mắc lỗi" in prompt_lower or "bao nhiêu lần" in prompt_lower:
            return {
                "type": "tool_call",
                "tool_name": "get_student_mistake_history",
                "arguments": {"student_id": "SV2026_HUNG", "grammar_topic": "ALL"},
                "thought": "Học viên muốn xem lại lịch sử các lỗi sai ngữ pháp đã mắc phải. Tôi sẽ gọi tool get_student_mistake_history."
            }

        # 4. Nhận diện yêu cầu chuyển tiếp / ping TA người thật (Dynamic Decision Escalation)
        elif "ta" in prompt_lower or "trợ giảng" in prompt_lower or "chưa hiểu" in prompt_lower or "giải thích giúp" in prompt_lower:
            return {
                "type": "tool_call",
                "tool_name": "escalate_to_human_ta",
                "arguments": {
                    "student_id": "SV2026_HUNG",
                    "topic": "Verb Patterns (like + V-ing vs to-V)",
                    "student_message": prompt,
                    "priority": "URGENT"
                },
                "thought": "Học viên chưa hiểu rõ hoặc yêu cầu kết nối với Trợ giảng (TA) người thật. Tôi sẽ kích hoạt tool escalate_to_human_ta để ping TA."
            }

        # 5. Nhận diện đặt lịch học kèm 1-1 với TA
        elif "đặt lịch" in prompt_lower or "phụ đạo" in prompt_lower or "kèm 1-1" in prompt_lower:
            return {
                "type": "tool_call",
                "tool_name": "book_ta_tutoring_session",
                "arguments": {
                    "student_id": "SV2026_HUNG",
                    "ta_name": "Ms. Lan Anh",
                    "timeslot": "19:00 Thứ 6 ngày 18/09/2026",
                    "topic": "Verb Patterns & Gerund Unit 3"
                },
                "thought": "Học viên yêu cầu đặt lịch học kèm 1-1 với Trợ giảng. Tôi sẽ gọi tool book_ta_tutoring_session."
            }

        # 6. Nhận diện bài tập củng cố tức thì
        elif "bài tập củng cố" in prompt_lower or "luyện tập" in prompt_lower or "cho em bài tập" in prompt_lower:
            return {
                "type": "tool_call",
                "tool_name": "get_remedial_exercises",
                "arguments": {"grammar_topic": "verb_pattern", "unit": 3},
                "thought": "Học viên cần bài tập củng cố nhanh theo Unit 3. Tôi sẽ gọi tool get_remedial_exercises."
            }

        # 7. Nhận diện tra cứu giáo trình / slide
        elif "slide" in prompt_lower or "giáo trình" in prompt_lower:
            return {
                "type": "tool_call",
                "tool_name": "search_course_materials",
                "arguments": {"query": "verb pattern like enjoy fancy", "unit": 3, "course_name": "IELTS Foundation"},
                "thought": "Học viên muốn tra cứu slide bài giảng Unit 3. Tôi sẽ gọi tool search_course_materials."
            }

        # 8. Nhận diện danh sách học viên
        elif "học viên" in prompt_lower and ("danh sách" in prompt_lower or "lớp" in prompt_lower):
            return {
                "type": "tool_call",
                "tool_name": "list_all_students",
                "arguments": {"class_filter": ""},
                "thought": "Người dùng muốn xem danh sách học viên trong các khóa học. Tôi sẽ gọi tool list_all_students."
            }

        else:
            return {
                "type": "text",
                "content": f"[Pedagogical Agent Response]: Chào bạn! Trong tiếng Anh, Gerund (V-ing) thường dùng làm tân ngữ sau các động từ chỉ cảm xúc/thói quen hoặc sau giới từ, còn To-Infinitive (To-V) dùng để diễn đạt mục đích hoặc sau các động từ chỉ ý định/kế hoạch.",
                "thought": "Câu hỏi lý thuyết chung, trả lời sư phạm trực tiếp mà không cần gọi Tool."
            }


class GeminiProvider(BaseLLMProvider):
    """Google Gemini Provider (Native Tool Calling với Google GenAI SDK)"""
    def __init__(self, api_key: str = None, model: str = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.model_name = model or os.getenv("LLM_MODEL") or "gemini-3.5-flash-lite"

    def generate(self, prompt: str, system_prompt: str = "") -> str:
        if not self.api_key or self.api_key == "your_gemini_api_key_here":
            return "[Gemini Error]: Chưa cấu hình GEMINI_API_KEY trong file .env! Đang sử dụng chế độ Mock."
        try:
            from google import genai
            client = genai.Client(api_key=self.api_key)
            contents = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
            response = client.models.generate_content(model=self.model_name, contents=contents)
            return response.text
        except Exception as e:
            return f"[Gemini Exception]: {str(e)}"

    def generate_with_tools(self, prompt: str, tools_schema: List[Dict[str, Any]], system_prompt: str = "") -> Dict[str, Any]:
        if not self.api_key or self.api_key == "your_gemini_api_key_here":
            print("ℹ️ [Gemini Provider]: Chưa tìm thấy GEMINI_API_KEY hợp lệ. Tự động chuyển sang Mock Offline.")
            return MockOfflineProvider().generate_with_tools(prompt, tools_schema, system_prompt)
        
        try:
            from google import genai
            from google.genai import types

            client = genai.Client(api_key=self.api_key)
            
            # Chuẩn hóa function declarations cho Gemini SDK
            function_declarations = []
            for tool in tools_schema:
                # Bỏ qua các tool schema chưa được định nghĩa hoàn chỉnh
                if not tool.get("name") or not tool.get("parameters"):
                    continue
                function_declarations.append({
                    "name": tool["name"],
                    "description": tool.get("description", ""),
                    "parameters": tool.get("parameters", {})
                })

            config = types.GenerateContentConfig(
                system_instruction=system_prompt if system_prompt else None,
                tools=[{"function_declarations": function_declarations}] if function_declarations else None,
                temperature=0.2
            )

            response = client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=config
            )

            # Kiểm tra xem Gemini có trả về Tool Call không
            if response.function_calls:
                call = response.function_calls[0]
                args = dict(call.args) if hasattr(call, 'args') and call.args else {}
                return {
                    "type": "tool_call",
                    "tool_name": call.name,
                    "arguments": args,
                    "thought": f"Gemini quyết định gọi công cụ '{call.name}' với tham số: {json.dumps(args, ensure_ascii=False)}"
                }
            else:
                return {
                    "type": "text",
                    "content": response.text or "",
                    "thought": "Gemini phản hồi trực tiếp bằng văn bản (không cần gọi công cụ)."
                }

        except Exception as e:
            print(f"⚠️ [Gemini API Warning]: Không thể kết nối live API ({str(e)}). Tự động fallback về Mock.")
            return MockOfflineProvider().generate_with_tools(prompt, tools_schema, system_prompt)


class OpenAIProvider(BaseLLMProvider):
    """OpenAI Provider (Native Tool Calling với OpenAI SDK)"""
    def __init__(self, api_key: str = None, model: str = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model_name = model or os.getenv("LLM_MODEL") or "gpt-4o-mini"

    def generate(self, prompt: str, system_prompt: str = "") -> str:
        if not self.api_key or self.api_key == "your_openai_api_key_here":
            return "[OpenAI Error]: Chưa cấu hình OPENAI_API_KEY trong file .env! Đang sử dụng chế độ Mock."
        try:
            from openai import OpenAI
            client = OpenAI(api_key=self.api_key)
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            response = client.chat.completions.create(model=self.model_name, messages=messages)
            return response.choices[0].message.content or ""
        except Exception as e:
            return f"[OpenAI Exception]: {str(e)}"

    def generate_with_tools(self, prompt: str, tools_schema: List[Dict[str, Any]], system_prompt: str = "") -> Dict[str, Any]:
        if not self.api_key or self.api_key == "your_openai_api_key_here":
            print("ℹ️ [OpenAI Provider]: Chưa tìm thấy OPENAI_API_KEY hợp lệ. Tự động chuyển sang Mock Offline.")
            return MockOfflineProvider().generate_with_tools(prompt, tools_schema, system_prompt)

        try:
            from openai import OpenAI
            client = OpenAI(api_key=self.api_key)

            tools = []
            for tool in tools_schema:
                if not tool.get("name"):
                    continue
                tools.append({
                    "type": "function",
                    "function": {
                        "name": tool["name"],
                        "description": tool.get("description", ""),
                        "parameters": tool.get("parameters", {})
                    }
                })

            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})

            response = client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                tools=tools if tools else None,
                tool_choice="auto" if tools else None
            )

            msg = response.choices[0].message
            if msg.tool_calls:
                call = msg.tool_calls[0]
                args = json.loads(call.function.arguments) if call.function.arguments else {}
                return {
                    "type": "tool_call",
                    "tool_name": call.function.name,
                    "arguments": args,
                    "thought": f"OpenAI quyết định gọi công cụ '{call.function.name}' với tham số: {json.dumps(args, ensure_ascii=False)}"
                }
            else:
                return {
                    "type": "text",
                    "content": msg.content or "",
                    "thought": "OpenAI phản hồi trực tiếp bằng văn bản (không cần gọi công cụ)."
                }
        except Exception as e:
            print(f"⚠️ [OpenAI API Warning]: Không thể kết nối live API ({str(e)}). Tự động fallback về Mock.")
            return MockOfflineProvider().generate_with_tools(prompt, tools_schema, system_prompt)


def get_llm_provider() -> BaseLLMProvider:
    """Factory function khởi tạo Provider theo LLM_PROVIDER env variable"""
    provider_type = os.getenv("LLM_PROVIDER", "gemini").lower()
    
    if provider_type == "gemini":
        key = os.getenv("GEMINI_API_KEY")
        if key and key != "your_gemini_api_key_here":
            return GeminiProvider()
        else:
            return MockOfflineProvider()
    elif provider_type == "openai":
        key = os.getenv("OPENAI_API_KEY")
        if key and key != "your_openai_api_key_here":
            return OpenAIProvider()
        else:
            return MockOfflineProvider()
    elif provider_type == "mock":
        return MockOfflineProvider()
    else:
        return MockOfflineProvider()
