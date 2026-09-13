"""
🌐 WEB APPLICATION BACKEND WITH AUTHENTICATION & ROLE-BASED PRIVACY ACCESS (RBAC)
Cung cấp REST API, Đăng nhập Phân quyền Vai trò & MCP Server Agent System cho VinUni Academic Portal.
"""

import os
import sys
import json
import time
from flask import Flask, render_template, request, jsonify, session

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from mcp_server import MCPAcademicServer
from providers import get_llm_provider
from prompts import CHATBOT_BASELINE_PROMPT, REACT_AGENT_SYSTEM_PROMPT, MAX_ITERATIONS
from tools import STUDENT_DATABASE, LECTURER_DATABASE, USER_ACCOUNTS
from app import load_test_cases, save_waterfall_trace

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = "vinuni_academic_portal_secret_key_2026"

# Khởi tạo singleton MCP Server & LLM Provider
mcp_server = MCPAcademicServer()
provider = get_llm_provider()


def get_current_user_context():
    """Lấy thông tin học viên hiện tại từ session hoặc mặc định SV2026_HUNG"""
    user_key = session.get("user_key", "SV2026_HUNG")
    return USER_ACCOUNTS.get(user_key, USER_ACCOUNTS["SV2026_HUNG"])


@app.route("/")
def index():
    """Trang chủ VinUni English Learning Assistant"""
    return render_template("index.html")


@app.route("/api/login", methods=["POST"])
def login():
    """API Đăng nhập tài khoản & Chuyển đổi Học viên"""
    data = request.json or {}
    username = data.get("username", "").strip()
    password = data.get("password", "").strip()

    account = USER_ACCOUNTS.get(username)
    if not account:
        account = next((acc for acc in USER_ACCOUNTS.values() if acc.get("student_id", "").lower() == username.lower()), None)

    if account:
        session["user_key"] = account["student_id"]
        return jsonify({
            "status": "SUCCESS",
            "message": f"Đăng nhập thành công học viên {account['full_name']}",
            "user": account
        })
    else:
        return jsonify({
            "status": "UNAUTHORIZED",
            "message": "Không tìm thấy mã học viên!"
        }), 401


@app.route("/api/logout", methods=["POST"])
def logout():
    """API Đăng xuất"""
    session.pop("user_key", None)
    return jsonify({"status": "SUCCESS", "message": "Đã đăng xuất"})


@app.route("/api/current-user", methods=["GET"])
def current_user():
    """Trả về tài khoản học viên đang đăng nhập"""
    user = get_current_user_context()
    return jsonify({"user": user, "available_accounts": USER_ACCOUNTS})


@app.route("/api/system-status", methods=["GET"])
def system_status():
    """Trả về thông tin hệ thống"""
    llm_provider_name = provider.__class__.__name__
    llm_model = getattr(provider, "model_name", "Offline-Mock-Model")
    tools_count = len(mcp_server.list_tools())
    user = get_current_user_context()
    return jsonify({
        "status": "ONLINE",
        "provider": llm_provider_name,
        "model": llm_model,
        "mcp_server": "VinUni-Pedagogical-MCPAcademicServer",
        "tools_count": tools_count,
        "current_user": user
    })


@app.route("/api/chat", methods=["POST"])
def api_chat():
    """API gửi câu hỏi đến Pedagogical ReAct Agent"""
    data = request.json or {}
    query = data.get("query", "").strip()
    if not query:
        return jsonify({"error": "Query cannot be empty"}), 400

    user_context = get_current_user_context()
    step_traces = []
    tools_list = mcp_server.list_tools()
    step = 0
    start_total_time = time.time()

    # Bổ sung thông tin bối cảnh học viên vào System Prompt để LLM nhận diện
    context_prompt = (
        f"{REACT_AGENT_SYSTEM_PROMPT}\n\n"
        f"BỐI CẢNH HỌC VIÊN ĐANG ĐĂNG NHẬP (CURRENT STUDENT CONTEXT):\n"
        f"- Họ và tên: {user_context.get('full_name', 'Đặng Quang Hùng')}\n"
        f"- Mã học viên: {user_context.get('student_id', 'SV2026_HUNG')}\n"
        f"- Khóa học: {user_context.get('current_course', 'IELTS Foundation')}\n"
        f"- Unit hiện tại: {user_context.get('current_unit', 3)}\n"
        f"- Trợ giảng (TA) phụ trách: {user_context.get('ta_assigned', 'Ms. Lan Anh')}\n"
    )

    while step < MAX_ITERATIONS:
        step += 1
        step_start_time = time.time()
        
        # Gọi LLM với Native Tool Calling Specs
        llm_response = provider.generate_with_tools(query, tools_list, system_prompt=context_prompt)
        latency_ms = round((time.time() - step_start_time) * 1000, 2)
        thought = llm_response.get("thought", "Đang suy luận...")

        # Trường hợp 1: Trả lời văn bản trực tiếp (Direct Answer)
        if llm_response.get("type") == "text":
            final_content = llm_response.get("content", "")
            step_traces.append({
                "step": step,
                "type": "FINAL_ANSWER",
                "thought": thought,
                "output": final_content,
                "latency_ms": latency_ms
            })
            break

        # Trường hợp 2: LLM đề xuất gọi Tool (Action)
        elif llm_response.get("type") == "tool_call":
            tool_name = llm_response.get("tool_name")
            arguments = llm_response.get("arguments", {})

            # Gọi Tool qua MCP Server truyền kèm User Context để kiểm tra phân quyền RBAC
            mcp_result = mcp_server.call_tool(tool_name, arguments, user_context=user_context)
            obs_data = mcp_result.get("result", {})

            if obs_data.get("status") == "PERMISSION_DENIED":
                final_answer = obs_data.get("message", "🚫 Truy cập bị từ chối do vi phạm quy định bảo mật quyền riêng tư.")
            elif obs_data.get("status") == "SUCCESS":
                final_answer = obs_data.get("message", f"Hoàn tất xử lý qua MCP Server: {json.dumps(obs_data, ensure_ascii=False)}")
            elif obs_data.get("status") == "NOT_FOUND":
                final_answer = obs_data.get("message", "Không tìm thấy dữ liệu yêu cầu.")
            else:
                final_answer = obs_data.get("message", f"Phản hồi từ công cụ: {json.dumps(obs_data, ensure_ascii=False)}")

            step_traces.append({
                "step": step,
                "type": "TOOL_EXECUTION",
                "thought": thought,
                "tool_name": tool_name,
                "arguments": arguments,
                "observation": obs_data,
                "latency_ms": latency_ms
            })

            # Tạo bước Final Answer nối tiếp
            step_traces.append({
                "step": step + 1,
                "type": "FINAL_ANSWER",
                "thought": "Đã tổng hợp kết quả Observation từ MCP Server.",
                "output": final_answer,
                "latency_ms": 10.0
            })
            break

    total_latency_ms = round((time.time() - start_total_time) * 1000, 2)
    save_waterfall_trace(step_traces)

    return jsonify({
        "query": query,
        "user_context": user_context,
        "traces": step_traces,
        "total_steps": len(step_traces),
        "total_latency_ms": total_latency_ms
    })


@app.route("/api/compare", methods=["POST"])
def api_compare():
    """API so sánh phản hồi song song với kiểm tra bảo mật"""
    data = request.json or {}
    query = data.get("query", "").strip()
    if not query:
        return jsonify({"error": "Query cannot be empty"}), 400

    user_context = get_current_user_context()

    # 1. Baseline Chatbot
    t0 = time.time()
    baseline_response = provider.generate(query, system_prompt=CHATBOT_BASELINE_PROMPT)
    baseline_latency = round((time.time() - t0) * 1000, 2)

    # 2. ReAct Agent
    t1 = time.time()
    tools_list = mcp_server.list_tools()
    agent_llm_res = provider.generate_with_tools(query, tools_list, system_prompt=REACT_AGENT_SYSTEM_PROMPT)
    agent_latency = round((time.time() - t1) * 1000, 2)

    tool_used = None
    tool_args = None
    observation = None
    agent_thought = agent_llm_res.get("thought", "")

    if agent_llm_res.get("type") == "tool_call":
        tool_used = agent_llm_res.get("tool_name")
        tool_args = agent_llm_res.get("arguments", {})
        mcp_res = mcp_server.call_tool(tool_used, tool_args, user_context=user_context)
        observation = mcp_res.get("result", {})
        agent_answer = observation.get("message", json.dumps(observation, ensure_ascii=False))
    else:
        agent_answer = agent_llm_res.get("content", "")

    return jsonify({
        "query": query,
        "baseline": {
            "response": baseline_response,
            "latency_ms": baseline_latency
        },
        "react_agent": {
            "thought": agent_thought,
            "tool_used": tool_used,
            "arguments": tool_args,
            "observation": observation,
            "response": agent_answer,
            "latency_ms": agent_latency
        }
    })


@app.route("/api/tools", methods=["GET"])
def get_tools():
    """Trả về danh sách tất cả 10 Tools trên MCP Server"""
    return jsonify({
        "server": mcp_server.server_name,
        "version": mcp_server.version,
        "tools": mcp_server.list_tools()
    })


@app.route("/api/call-tool", methods=["POST"])
def call_tool_direct():
    """Gọi thử nghiệm trực tiếp 1 Tool trên MCP Server có kiểm tra RBAC"""
    data = request.json or {}
    tool_name = data.get("tool_name")
    arguments = data.get("arguments", {})
    user_context = get_current_user_context()
    if not tool_name:
        return jsonify({"error": "Tool name is required"}), 400

    mcp_result = mcp_server.call_tool(tool_name, arguments, user_context=user_context)
    return jsonify(mcp_result)


@app.route("/api/database", methods=["GET"])
def get_database():
    """Trả về Mock Databases"""
    return jsonify({
        "students": STUDENT_DATABASE,
        "lecturers": LECTURER_DATABASE
    })


@app.route("/api/trace-waterfall", methods=["GET"])
def get_trace_waterfall():
    """Trả về tệp trace log Waterfall mới nhất"""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    trace_path = os.path.join(base_dir, "docs", "trace_waterfall.json")
    if os.path.exists(trace_path):
        try:
            with open(trace_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return jsonify({"status": "SUCCESS", "traces": data})
        except Exception as e:
            return jsonify({"status": "ERROR", "error": str(e)}), 500
    return jsonify({"status": "NOT_FOUND", "traces": []})


if __name__ == "__main__":
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", 5000))
    print("==========================================================")
    print(f"🚀 VINUNI ACADEMIC PORTAL RUNNING AT: http://{host}:{port}")
    print("==========================================================")
    app.run(host=host, port=port, debug=True)
