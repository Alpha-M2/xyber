// Xyber Documentation RAG Chatbot - Frontend JavaScript

const API_BASE_URL = window.location.origin;
const HEALTH_CHECK_INTERVAL = 5000; // 5 seconds

// DOM Elements
const chatContainer = document.getElementById("chatContainer");
const questionInput = document.getElementById("questionInput");
const queryForm = document.getElementById("queryForm");
const sendBtn = document.getElementById("sendBtn");
const clearBtn = document.getElementById("clearBtn");
const statusDot = document.getElementById("statusDot");
const statusText = document.getElementById("statusText");
const statsElement = document.getElementById("stats");
const ingestModal = document.getElementById("ingestModal");
const ingestBtn = document.getElementById("ingestBtn");
const ingestCancelBtn = document.getElementById("ingestCancelBtn");
const ingestStatus = document.getElementById("ingestStatus");

let isLoading = false;
let isHealthy = false;

// Initialize
document.addEventListener("DOMContentLoaded", () => {
    // Add ingest button to header
    const headerContent = document.querySelector(".header-content");
    const ingestBtnHeader = document.createElement("button");
    ingestBtnHeader.className = "btn btn-secondary";
    ingestBtnHeader.style.position = "absolute";
    ingestBtnHeader.style.bottom = "10px";
    ingestBtnHeader.style.right = "30px";
    ingestBtnHeader.textContent = "📥 Ingest Docs";
    ingestBtnHeader.addEventListener("click", () => ingestModal.classList.add("show"));
    
    const headerContainer = document.querySelector(".header");
    headerContainer.appendChild(ingestBtnHeader);

    // Event listeners
    queryForm.addEventListener("submit", handleQuery);
    clearBtn.addEventListener("click", clearChat);
    ingestBtn.addEventListener("click", startIngestion);
    ingestCancelBtn.addEventListener("click", () => ingestModal.classList.remove("show"));
    document.querySelector(".modal .close").addEventListener("click", () => {
        ingestModal.classList.remove("show");
    });

    // Auto-expand textarea
    questionInput.addEventListener("input", function () {
        this.style.height = "auto";
        this.style.height = Math.min(this.scrollHeight, 150) + "px";
    });

    // Start health check and initial load
    checkHealth();
    loadStats();
    setInterval(checkHealth, HEALTH_CHECK_INTERVAL);
    setInterval(loadStats, 10000); // Update stats every 10 seconds
});

// Check backend health
async function checkHealth() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        if (response.ok) {
            const data = await response.json();
            updateStatus(true, data.message);
            isHealthy = true;
        } else {
            updateStatus(false, "Service unavailable");
            isHealthy = false;
        }
    } catch (error) {
        updateStatus(false, "Connection failed");
        isHealthy = false;
    }
}

// Update status display
function updateStatus(healthy, message) {
    statusDot.className = healthy ? "status-dot active" : "status-dot";
    statusText.textContent = message;
}

// Load statistics
async function loadStats() {
    try {
        const response = await fetch(`${API_BASE_URL}/stats`);
        if (response.ok) {
            const data = await response.json();
            statsElement.innerHTML = `📊 Documents indexed: <strong>${data.total_chunks}</strong> chunks`;
        }
    } catch (error) {
        statsElement.innerHTML = "📊 Stats unavailable";
    }
}

// Handle query submission
async function handleQuery(e) {
    e.preventDefault();

    const question = questionInput.value.trim();
    if (!question) return;

    if (!isHealthy) {
        addMessage("system", "⚠️ Backend service is not available. Please try again in a moment.");
        return;
    }

    // Add user message
    addMessage("user", question);
    questionInput.value = "";
    questionInput.style.height = "auto";
    isLoading = true;
    sendBtn.disabled = true;

    try {
        // Show loading indicator
        const loadingMessage = addMessage("system", '<span class="loading"></span><span class="loading"></span><span class="loading"></span>');

        const response = await fetch(`${API_BASE_URL}/query`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ question }),
        });

        if (!response.ok) {
            const error = await response.json();
            removeMessage(loadingMessage);
            addMessage(
                "system",
                `❌ Error: ${error.detail || "Failed to process query"}`
            );
            return;
        }

        const data = await response.json();
        removeMessage(loadingMessage);

        // Add assistant response
        let responseText = data.answer;
        if (data.sources && data.sources.length > 0) {
            responseText += `\n\n📚 <strong>Sources:</strong>\n`;
            data.sources.forEach((source) => {
                responseText += `• ${source}\n`;
            });
        }

        addMessage("system", responseText);

        // Update stats
        loadStats();
    } catch (error) {
        console.error("Query error:", error);
        addMessage("system", `❌ Error: ${error.message}`);
    } finally {
        isLoading = false;
        sendBtn.disabled = false;
        questionInput.focus();
    }
}

// Add message to chat
function addMessage(role, content) {
    const messageDiv = document.createElement("div");
    messageDiv.className = `message ${role === "user" ? "user" : "system"}`;

    const contentDiv = document.createElement("div");
    contentDiv.className = "message-content";
    contentDiv.innerHTML = content;

    messageDiv.appendChild(contentDiv);
    chatContainer.appendChild(messageDiv);

    // Scroll to bottom
    setTimeout(() => {
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }, 0);

    return messageDiv;
}

// Remove message from chat
function removeMessage(messageDiv) {
    if (messageDiv && messageDiv.parentNode) {
        messageDiv.parentNode.removeChild(messageDiv);
    }
}

// Clear chat
function clearChat() {
    if (confirm("Are you sure you want to clear the chat?")) {
        chatContainer.innerHTML = `
            <div class="message system-message">
                <div class="message-content">
                    <p>Chat cleared. Ask me anything about Xyber documentation!</p>
                </div>
            </div>
        `;
    }
}

// Start document ingestion
async function startIngestion() {
    ingestBtn.disabled = true;
    ingestStatus.className = "ingest-status show";
    ingestStatus.textContent = "Starting ingestion...";

    try {
        const response = await fetch(`${API_BASE_URL}/ingest`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ clear_first: true }),
        });

        if (response.ok) {
            const data = await response.json();
            ingestStatus.className = "ingest-status show success";
            ingestStatus.innerHTML = `
                ✅ Ingestion started!<br>
                <small>This may take a few minutes. Check back later to see updated stats.</small>
            `;

            // Close modal after 3 seconds
            setTimeout(() => {
                ingestModal.classList.remove("show");
                ingestStatus.className = "ingest-status";
            }, 3000);

            // Poll for stats update
            pollStatsUpdate();
        } else {
            const error = await response.json();
            ingestStatus.className = "ingest-status show error";
            ingestStatus.textContent = `❌ Error: ${error.detail || "Ingestion failed"}`;
        }
    } catch (error) {
        ingestStatus.className = "ingest-status show error";
        ingestStatus.textContent = `❌ Error: ${error.message}`;
    } finally {
        ingestBtn.disabled = false;
    }
}

// Poll for stats update after ingestion
function pollStatsUpdate() {
    let pollCount = 0;
    const maxPolls = 120; // 10 minutes with 5-second intervals

    const pollInterval = setInterval(() => {
        loadStats();
        pollCount++;

        if (pollCount >= maxPolls) {
            clearInterval(pollInterval);
        }
    }, 5000);
}

// Handle modal close
window.addEventListener("click", (event) => {
    if (event.target === ingestModal) {
        ingestModal.classList.remove("show");
    }
});
