import ApiService from "../services/apiService.js";
import notify from "../utils/notifications.js";
import theme from "../utils/theme.js";
import { exportToJSON } from "../utils/export.js";

const AgentName = "agent";
let activeSessionId = "";
let chatHistory = [];

document.addEventListener("DOMContentLoaded", () => {
    initChat();
});

function initChat() {
    const newSessionButton = document.getElementById("new-session");
    newSessionButton.addEventListener("click", createSession);
    listSessions();
}

// DOM elements
const messagesEl = document.getElementById("messages");
const form = document.getElementById("chat-form");
const input = document.getElementById("message-input");
const sendBtn = document.getElementById("send-btn");
const voiceBtn = document.getElementById("voice-btn");
const fileInput = document.getElementById("file-input");
const uploadList = document.getElementById("upload-list");
const sessionsListWrapper = document.getElementById("sessions-list");

// Voice recognition setup
let recognition = null;
let isRecording = false;

// Text-to-Speech setup
let ttsEnabled = localStorage.getItem('ttsEnabled') === 'true';
const synth = window.speechSynthesis;

function speakText(text) {
    if (!ttsEnabled || !synth) return;
    synth.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 1.0;
    utterance.pitch = 1.0;
    utterance.volume = 1.0;
    synth.speak(utterance);
}

if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = true;
    recognition.lang = 'en-US';

    recognition.onstart = () => {
        isRecording = true;
        voiceBtn.classList.add('recording');
        voiceBtn.innerHTML = '<i class="fa fa-stop"></i>';
        notify.info('Listening...');
    };

    recognition.onresult = (event) => {
        const transcript = Array.from(event.results)
            .map(result => result[0].transcript)
            .join('');
        input.value = transcript;
    };

    recognition.onend = () => {
        isRecording = false;
        voiceBtn.classList.remove('recording');
        voiceBtn.innerHTML = '<i class="fa fa-microphone"></i>';
    };

    recognition.onerror = (event) => {
        console.error('Speech recognition error:', event.error);
        notify.error('Voice input failed: ' + event.error);
        isRecording = false;
        voiceBtn.classList.remove('recording');
        voiceBtn.innerHTML = '<i class="fa fa-microphone"></i>';
    };
} else {
    console.warn('Speech recognition not supported');
    if (voiceBtn) voiceBtn.style.display = 'none';
}

function listSessions() {
    ApiService.get(`/apps/${AgentName}/users/user/sessions`)
        .then((sessions) => {
            if (sessions.length) {
                activeSessionId = sessions[0].id;
                for (let i = 0; i < sessions.length; i++) {
                    createSessionElement(sessions[i].id);
                }
            }
        })
        .catch((error) => console.error(error));
}

function createSessionElement(id) {
    const li = document.createElement("li");
    li.setAttribute("id", `id-${id}`);
    li.setAttribute("class", "session-item");
    const deleteIcon = document.createElement("i");
    deleteIcon.setAttribute("class", "fa fa-trash delete-session");
    deleteIcon.onclick = (event) => deleteSession(event, id);
    const spanEl = document.createElement("span");
    spanEl.innerHTML = id;
    if (activeSessionId === id) {
        const existingSessions =
            sessionsListWrapper.querySelectorAll(".session-item");
        if (existingSessions.length) {
            for (let j = 0; j < existingSessions.length; j++) {
                existingSessions[j].classList.remove("active");
            }
        }
        li.classList.add("active");
        updateActiveSession(id);
    }
    li.onclick = () => updateActiveSession(id);
    li.appendChild(spanEl);
    li.appendChild(deleteIcon);
    sessionsListWrapper.appendChild(li);
}

function createSession() {
    ApiService.post(`/apps/${AgentName}/users/user/sessions`, {})
        .then((session) => {
            activeSessionId = session.id;
            messagesEl.innerHTML = "";
            createSessionElement(session.id);
            notify.success("New session created!");
        })
        .catch((error) => {
            console.error("Session creation error:", error);
            notify.error("Failed to create session. Check console for details.");
        });
}

function deleteSession(event, id) {
    event.stopPropagation();
    ApiService.delete(`/apps/${AgentName}/users/user/sessions/${id}`)
        .then(() => {
            const session = document.getElementById(`id-${id}`);
            const wasActive = session.classList.contains("active");
            if (wasActive) {
                const firstSession = document.querySelector(".session-item");
                if (firstSession) {
                    firstSession.classList.add("active");
                    activeSession = firstSession.getAttribute("id");
                }
            }
            session.parentNode.removeChild(session);
            notify.success("Session deleted!");
        })
        .catch((error) => {
            console.error(error);
            notify.error("Failed to delete session.");
        });
}

function updateActiveSession(id) {
    ApiService.get(`/apps/${AgentName}/users/user/sessions/${id}`)
        .then((sessionResponse) => {
            const existingSessions =
                sessionsListWrapper.querySelectorAll(".session-item");
            if (existingSessions.length) {
                for (let j = 0; j < existingSessions.length; j++) {
                    existingSessions[j].classList.remove("active");
                }
            }
            const listEl = document.getElementById(`id-${id}`);
            activeSessionId = id;
            listEl.classList.add("active");
            messagesEl.innerHTML = "";
            renderEvents(sessionResponse.events);
        })
        .catch((error) => console.error(error));
}

function renderEvents(events) {
    chatHistory = [];
    for (let i = 0; i < events.length; i++) {
        if (events[i].content) {
            appendMessage(events[i].content, events[i].content.role);
            chatHistory.push({
                role: events[i].content.role,
                message: events[i].content.parts?.[0]?.text || "[Non-text content]",
                timestamp: new Date().toISOString()
            });
        }
    }
}

// Export chat history
function exportChat() {
    if (chatHistory.length === 0) {
        notify.warning("No messages to export.");
        return;
    }
    exportToJSON(chatHistory, `chat_${activeSessionId}_${new Date().toISOString().split('T')[0]}.json`);
    notify.success("Chat exported successfully!");
}

// Clear chat
function clearChat() {
    messagesEl.innerHTML = "";
    chatHistory = [];
    notify.info("Chat cleared.");
}

// Helpers
function appendMessage(content, who = "model") {
    const el = document.createElement("div");
    let textToSpeak = '';
    if (content.parts) {
        for (let i = 0; i < content.parts.length; i++) {
            const part = content.parts[i];
            if (part.functionResponse) {
                el.className = `message model function`;
                el.innerHTML = `<i class="fa fa-check"></i> ${part.functionResponse.name}`;
            } else {
                el.className = `message ${who}`;
                if (part.text) {
                    el.innerHTML = marked.parse(part.text);
                    if (who === 'model') textToSpeak = part.text;
                }
                if (part.functionCall) {
                    el.classList.add("function");
                    el.innerHTML = `<i class="fa fa-bolt"></i> ${part.functionCall.name}`;
                }
                if (part.inlineData) {
                    const mediaEl = createMediaElement(part.inlineData);
                    if (mediaEl) {
                        el.appendChild(mediaEl);
                    }
                }
            }
        }
    }
    messagesEl.appendChild(el);
    messagesEl.scrollTop = messagesEl.scrollHeight;
    if (textToSpeak && who === 'model') speakText(textToSpeak);
    return el;
}

function createMediaElement({ data, mimeType, displayName }) {
    const wrapper = document.createElement("div");
    wrapper.className = "message-media";
    const encrpytedData = data.replace(/_/g, "/").replace(/-/g, "+");
    if (mimeType.startsWith("image/")) {
        const img = document.createElement("img");
        img.src = `data:${mimeType};base64,${encrpytedData}`;
        img.alt = displayName;
        img.loading = "lazy";
        wrapper.appendChild(img);
    } else {
        // For non-image files, show a download link
        const link = document.createElement("a");
        link.href = `data:${mimeType};base64,${encrpytedData}`;
        link.download = displayName;
        link.innerHTML = `<i class="fa fa-download"></i> ${displayName}`;
        wrapper.appendChild(link);
    }

    return wrapper;
}

function setSending(isSending) {
    sendBtn.disabled = isSending;
    input.disabled = isSending;
}

// File handling
let currentFile = null;
const filePreview = document.createElement("div");
filePreview.className = "file-preview";
form.insertBefore(filePreview, form.firstChild);

async function fileToBase64(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = () => {
            // Extract the base64 data from the DataURL
            const base64Data = reader.result.split(",")[1];
            resolve({
                data: base64Data,
                displayName: file.name,
                mimeType: file.type,
            });
        };
        reader.onerror = (error) => reject(error);
    });
}

function showFilePreview(file) {
    filePreview.innerHTML = "";
    if (!file) return;

    const wrapper = document.createElement("div");
    wrapper.className = "preview-wrapper";

    if (file.type.startsWith("image/")) {
        const img = document.createElement("img");
        img.className = "message-media preview";
        const reader = new FileReader();
        reader.onload = (e) => (img.src = e.target.result);
        reader.readAsDataURL(file);
        wrapper.appendChild(img);
    } else {
        const fileInfo = document.createElement("div");
        fileInfo.className = "file-info";
        fileInfo.innerHTML = `<i class="fa fa-file"></i> ${file.name}`;
        wrapper.appendChild(fileInfo);
    }

    const removeBtn = document.createElement("button");
    removeBtn.className = "remove-preview";
    removeBtn.innerHTML = '<i class="fa fa-times"></i>';
    removeBtn.onclick = clearFilePreview;
    wrapper.appendChild(removeBtn);

    filePreview.appendChild(wrapper);
}

function clearFilePreview() {
    filePreview.innerHTML = "";
    currentFile = null;
    fileInput.value = "";
}

async function sendMessage(text, attachedFile = null) {
    if (!text && !attachedFile) return;

    // Show user's message
    setSending(true);
    const parts = [];

    if (text) {
        parts.push({ text });
    }

    if (attachedFile) {
        const base64Data = await fileToBase64(attachedFile);
        parts.push({ inlineData: base64Data });
    }

    appendMessage({ parts }, "user");
    chatHistory.push({
        role: "user",
        message: text || "[File attachment]",
        timestamp: new Date().toISOString()
    });
    clearFilePreview();

    const payload = {
        appName: AgentName,
        newMessage: { role: "user", parts },
        sessionId: activeSessionId,
        stateDelta: null,
        streaming: false,
        userId: "user",
    };

    try {
        await ApiService.postWithStream("/run_sse", payload, async (chunk) => {
            if (chunk && typeof chunk === "object") {
                appendMessage(chunk.content, "model");
                messagesEl.scrollTop = messagesEl.scrollHeight;
            }
        });
    } catch (err) {
        console.error("Chat error:", err);
        notify.error("Failed to send message.");
    } finally {
        setSending(false);
    }
}

// Setup theme toggle
function setupThemeToggle() {
    const themeBtn = document.getElementById("theme-toggle");
    if (themeBtn) {
        themeBtn.addEventListener("click", () => {
            const newTheme = theme.toggle();
            themeBtn.innerHTML = newTheme === 'dark' ? '<i class="fa fa-sun"></i>' : '<i class="fa fa-moon"></i>';
        });
    }
}

// Setup export button
function setupExport() {
    const exportBtn = document.getElementById("export-chat-btn");
    if (exportBtn) {
        exportBtn.addEventListener("click", exportChat);
    }
}

// Setup clear button
function setupClear() {
    const clearBtn = document.getElementById("clear-chat-btn");
    if (clearBtn) {
        clearBtn.addEventListener("click", clearChat);
    }
}

// Setup TTS toggle
function setupTTS() {
    const ttsBtn = document.getElementById('tts-toggle');
    if (ttsBtn) {
        ttsBtn.classList.toggle('active', ttsEnabled);
        ttsBtn.innerHTML = ttsEnabled ? '<i class="fa fa-volume-up"></i>' : '<i class="fa fa-volume-mute"></i>';
        ttsBtn.addEventListener('click', () => {
            ttsEnabled = !ttsEnabled;
            localStorage.setItem('ttsEnabled', ttsEnabled);
            ttsBtn.classList.toggle('active', ttsEnabled);
            ttsBtn.innerHTML = ttsEnabled ? '<i class="fa fa-volume-up"></i>' : '<i class="fa fa-volume-mute"></i>';
            notify.info(ttsEnabled ? 'Text-to-Speech enabled' : 'Text-to-Speech disabled');
            if (!ttsEnabled) synth.cancel();
        });
    }
}

// Initialize enhancements
setupThemeToggle();
setupExport();
setupClear();
setupTTS();

// File input handler
fileInput.addEventListener("change", (e) => {
    const file = e.target.files[0];
    if (file) {
        currentFile = file;
        showFilePreview(file);
    }
});

// Voice button handler
if (voiceBtn && recognition) {
    voiceBtn.addEventListener('click', () => {
        if (isRecording) {
            recognition.stop();
        } else {
            recognition.start();
        }
    });
}

// Form submit
form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const text = input.value.trim();
    input.value = "";
    await sendMessage(text, currentFile);
});
