/* ==========================================================================
   VINUNI AI ACADEMIC ASSISTANT - FRONTEND LOGIC (10 ADVANCED TOOLS)
   ========================================================================== */

document.addEventListener("DOMContentLoaded", () => {
    initNavigationTabs();
    fetchSystemStatus();
    fetchToolsSchema();
});

// NAVIGATION TAB SWITCHER
function initNavigationTabs() {
    const tabs = document.querySelectorAll(".nav-tab");
    tabs.forEach(tab => {
        tab.addEventListener("click", () => {
            tabs.forEach(t => t.classList.remove("active"));
            document.querySelectorAll(".tab-pane").forEach(pane => pane.classList.remove("active"));
            
            tab.classList.add("active");
            const targetId = tab.getAttribute("data-tab");
            const targetPane = document.getElementById(targetId);
            if (targetPane) targetPane.classList.add("active");
        });
    });
}

// FETCH SYSTEM STATUS
async function fetchSystemStatus() {
    try {
        const res = await fetch("/api/system-status");
        const data = await res.json();
        if (data.status === "ONLINE") {
            document.getElementById("sys-provider").textContent = `LLM: ${data.provider}`;
            document.getElementById("sys-model").textContent = `Model: ${data.model}`;
            document.getElementById("sys-mcp").textContent = `MCP Server: ${data.tools_count} Tools Online`;
        }
    } catch (e) {
        console.error("Failed to fetch system status", e);
    }
}

// QUICK FILL CHAT INPUT
function quickFill(text) {
    const input = document.getElementById("chat-input");
    input.value = text;
    input.focus();
    const tab1 = document.querySelector('[data-tab="tab-chat"]');
    if (tab1) tab1.click();
}

// AUTO EXPAND TEXTAREA ON KEYDOWN
function handleKeyDown(event) {
    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        document.getElementById("chat-form").requestSubmit();
    }
}

// HANDLE INTERACTIVE CHAT SUBMIT
async function handleChatSubmit(event) {
    event.preventDefault();
    const input = document.getElementById("chat-input");
    const query = input.value.trim();
    if (!query) return;

    const messagesContainer = document.getElementById("chat-messages");
    
    // Remove welcome card if present
    const welcome = messagesContainer.querySelector(".welcome-card");
    if (welcome) welcome.remove();

    // 1. Render User Message
    const userRow = document.createElement("div");
    userRow.className = "msg-row";
    userRow.innerHTML = `<div class="msg-user">${escapeHtml(query)}</div>`;
    messagesContainer.appendChild(userRow);

    // Clear input
    input.value = "";

    // 2. Render Loading Indicator
    const agentContainer = document.createElement("div");
    agentContainer.className = "msg-agent-container";
    
    const loadingCard = document.createElement("div");
    loadingCard.className = "step-card thought";
    loadingCard.innerHTML = `<div class="card-header"><i class="fa-solid fa-spinner fa-spin"></i> ReAct Agent đang suy luận và xử lý câu hỏi...</div>`;
    agentContainer.appendChild(loadingCard);
    messagesContainer.appendChild(agentContainer);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;

    // 3. Send API Request
    try {
        const res = await fetch("/api/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ query: query })
        });
        const data = await res.json();
        
        // Remove loading card
        loadingCard.remove();

        if (data.traces && data.traces.length > 0) {
            data.traces.forEach(trace => {
                const stepCard = document.createElement("div");
                
                if (trace.type === "TOOL_EXECUTION") {
                    stepCard.className = "step-card action";
                    stepCard.innerHTML = `
                        <div class="card-header"><i class="fa-solid fa-brain"></i> Step ${trace.step} Thought & Tool Action</div>
                        <p><strong>Thought:</strong> ${escapeHtml(trace.thought)}</p>
                        <div class="json-badge"><strong>Action Proposed:</strong> ${escapeHtml(trace.tool_name)}(${JSON.stringify(trace.arguments, null, 2)})</div>
                        
                        <div style="margin-top: 10px;" class="step-card observation">
                            <div class="card-header" style="color: #059669;"><i class="fa-solid fa-eye"></i> Observation từ MCP Server</div>
                            <div class="json-badge">${escapeHtml(JSON.stringify(trace.observation, null, 2))}</div>
                        </div>
                    `;
                } else if (trace.type === "FINAL_ANSWER") {
                    stepCard.className = "step-card final";
                    stepCard.innerHTML = `
                        <div class="card-header"><i class="fa-solid fa-flag-checkered"></i> Final Answer</div>
                        <p><strong>Thought:</strong> ${escapeHtml(trace.thought)}</p>
                        <div style="margin-top: 8px; font-size: 14px; line-height: 1.6; color: #0f172a; font-weight: 500;">${escapeHtml(trace.output)}</div>
                    `;
                }
                
                agentContainer.appendChild(stepCard);
            });
        }
    } catch (err) {
        loadingCard.className = "step-card thought";
        loadingCard.innerHTML = `<div class="card-header" style="color: #dc2626;"><i class="fa-solid fa-triangle-exclamation"></i> Lỗi xử lý: ${err.message}</div>`;
    }

    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

// RUN COMPARISON
async function runComparison() {
    const input = document.getElementById("compare-input").value.trim();
    if (!input) return;

    const baselineBox = document.getElementById("baseline-output");
    const agentBox = document.getElementById("agent-output");

    baselineBox.innerHTML = `<p class="placeholder-text"><i class="fa-solid fa-spinner fa-spin"></i> Đang gọi Chatbot Baseline...</p>`;
    agentBox.innerHTML = `<p class="placeholder-text"><i class="fa-solid fa-spinner fa-spin"></i> ReAct Agent đang suy luận qua MCP Server...</p>`;

    try {
        const res = await fetch("/api/compare", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ query: input })
        });
        const data = await res.json();

        // Update Baseline
        document.getElementById("baseline-latency").textContent = `${data.baseline.latency_ms} ms`;
        baselineBox.innerHTML = `
            <div style="white-space: pre-wrap;">${escapeHtml(data.baseline.response)}</div>
            <div style="margin-top: 16px; padding: 10px; background: #fef3c7; border: 1px solid #fde68a; border-radius: 8px; font-size: 12px; color: #92400e;">
                ⚠️ <strong>Hạn chế:</strong> Chatbot Baseline không kết nối MCP Server, không thể tra cứu thông tin thời gian thực.
            </div>
        `;

        // Update ReAct Agent
        document.getElementById("agent-latency").textContent = `${data.react_agent.latency_ms} ms`;
        let agentHtml = ``;
        if (data.react_agent.thought) {
            agentHtml += `<p style="margin-bottom: 8px;"><strong>🧠 Thought:</strong> ${escapeHtml(data.react_agent.thought)}</p>`;
        }
        if (data.react_agent.tool_used) {
            agentHtml += `<div class="json-badge" style="margin-bottom: 12px;">🛠️ <strong>Tool Call:</strong> ${data.react_agent.tool_used}(${JSON.stringify(data.react_agent.arguments)})</div>`;
        }
        agentHtml += `<div style="padding: 12px; background: #eff6ff; border: 1px solid #bfdbfe; border-radius: 8px; font-weight: 500; color: #1e40af;">
            🏁 <strong>Final Answer:</strong> ${escapeHtml(data.react_agent.response)}
        </div>`;
        agentBox.innerHTML = agentHtml;

    } catch (e) {
        baselineBox.innerHTML = `<span style="color: #dc2626;">Lỗi kết nối API</span>`;
        agentBox.innerHTML = `<span style="color: #dc2626;">Lỗi kết nối API</span>`;
    }
}

// FETCH TOOLS SCHEMA
async function fetchToolsSchema() {
    try {
        const res = await fetch("/api/tools");
        const data = await res.json();
        const container = document.getElementById("tools-schema-list");
        if (data.tools) {
            container.innerHTML = "";
            data.tools.forEach((tool, idx) => {
                const toolCard = document.createElement("div");
                toolCard.className = "step-card action";
                toolCard.style.marginBottom = "16px";
                toolCard.innerHTML = `
                    <div class="card-header"><i class="fa-solid fa-gears"></i> ${idx + 1}. ${tool.name}</div>
                    <p style="font-size: 13px; color: #475569; margin-bottom: 6px;">${escapeHtml(tool.description)}</p>
                    <div class="json-badge">${escapeHtml(JSON.stringify(tool.parameters, null, 2))}</div>
                `;
                container.appendChild(toolCard);
            });
        }
    } catch (e) {
        console.error("Failed to fetch tools schema", e);
    }
}

// UTILITY: ESCAPE HTML
function escapeHtml(text) {
    if (typeof text !== "string") return text;
    return text
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}
