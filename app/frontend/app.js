const API_BASE = 'http://localhost:5000/api';
let currentSessionId = 'default';

function initTheme() {
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);
    updateThemeIcon(savedTheme);
}

function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    updateThemeIcon(newTheme);
}

function updateThemeIcon(theme) {
    const icon = document.getElementById('themeToggle');
    icon.textContent = theme === 'dark' ? '☀️' : '🌙';
}

document.addEventListener('DOMContentLoaded', () => {
    initTheme();
    checkServerHealth();
    loadSessions();
    loadCurrentSession();
});

async function checkServerHealth() {
    try {
        const response = await fetch(`${API_BASE}/health`);
        if (!response.ok) {
            throw new Error('Server not responding');
        }
        console.log('Server is running');
    } catch (error) {
        console.error('Server health check failed:', error);
        const messagesDiv = document.getElementById('messages');
        const theme = document.documentElement.getAttribute('data-theme');
        const bgColor = theme === 'dark' ? '#1e293b' : '#fff3cd';
        const textColor = theme === 'dark' ? '#f1f5f9' : '#856404';
        const borderColor = theme === 'dark' ? '#334155' : '#ffc107';
        
        messagesDiv.innerHTML = `
            <div class="message assistant">
                <div class="message-bubble" style="background: ${bgColor}; border-color: ${borderColor}; color: ${textColor};">
                    <strong>⚠️ Server Connection Error</strong><br>
                    Cannot connect to the backend server at ${API_BASE}.<br>
                    <br>
                    <strong>To fix this:</strong><br>
                    1. Make sure the Flask server is running:<br>
                       &nbsp;&nbsp;<code>cd app\\server</code><br>
                       &nbsp;&nbsp;<code>python main.py</code><br>
                    2. The server should be running on http://localhost:5000<br>
                    3. Refresh this page after starting the server
                </div>
            </div>
        `;
    }
}

async function loadSessions() {
    try {
        const response = await fetch(`${API_BASE}/sessions`);
        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }
        const data = await response.json();
        
        const sessionsList = document.getElementById('sessionsList');
        sessionsList.innerHTML = '';
        
        if (data.sessions && data.sessions.length > 0) {
            data.sessions.forEach(sessionId => {
                const sessionItem = document.createElement('div');
                sessionItem.className = 'session-item';
                sessionItem.textContent = sessionId;
                sessionItem.onclick = () => switchSession(sessionId);
                if (sessionId === currentSessionId) {
                    sessionItem.classList.add('active');
                }
                sessionsList.appendChild(sessionItem);
            });
        } else {
            sessionsList.innerHTML = '<p style="color: #6c757d; font-size: 0.9rem;">No sessions yet</p>';
        }
    } catch (error) {
        console.error('Error loading sessions:', error);
        const sessionsList = document.getElementById('sessionsList');
        sessionsList.innerHTML = '<p style="color: #dc3545; font-size: 0.9rem;">Cannot connect to server</p>';
    }
}

function createNewSession() {
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    currentSessionId = `session-${timestamp}`;
    document.getElementById('sessionSelect').value = 'new';
    clearMessages();
    loadSessions();
}

async function loadSession() {
    const sessionId = document.getElementById('sessionSelect').value;
    if (sessionId === 'new') {
        createNewSession();
        return;
    }
    switchSession(sessionId);
}

async function switchSession(sessionId) {
    currentSessionId = sessionId;
    document.getElementById('sessionSelect').value = sessionId;
    
    document.querySelectorAll('.session-item').forEach(item => {
        item.classList.remove('active');
        if (item.textContent === sessionId) {
            item.classList.add('active');
        }
    });
    
    await loadCurrentSession();
}

async function loadCurrentSession() {
    try {
        const response = await fetch(`${API_BASE}/sessions/${currentSessionId}/messages`);
        if (!response.ok) {
            if (response.status === 404) {
                clearMessages();
                return;
            }
            throw new Error(`Server error: ${response.status}`);
        }
        const data = await response.json();
        
        clearMessages();
        
        if (data.messages && data.messages.length > 0) {
            data.messages.forEach(msg => {
                addMessage(msg.role, msg.content, msg.created_at);
            });
        }
    } catch (error) {
        console.error('Error loading session:', error);
    }
}

async function sendMessage() {
    const input = document.getElementById('messageInput');
    const message = input.value.trim();
    
    if (!message) return;
    
    const sendButton = document.getElementById('sendButton');
    sendButton.disabled = true;
    sendButton.innerHTML = '<div class="loading"></div>';
    
    addMessage('user', message);
    input.value = '';
    
    try {
        const response = await fetch(`${API_BASE}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message,
                session_id: currentSessionId
            })
        });
        
        if (!response.ok) {
            throw new Error(`Server error: ${response.status} ${response.statusText}`);
        }
        
        const data = await response.json();
        
        if (data.error) {
            addMessage('assistant', `Error: ${data.error}`, new Date().toISOString());
        } else {
            addMessage('assistant', data.response, new Date().toISOString());
        }
        
        loadSessions();
        
    } catch (error) {
        console.error('Error sending message:', error);
        let errorMsg = `Connection Error: ${error.message}`;
        if (error.message.includes('Failed to fetch') || error.message.includes('NetworkError')) {
            errorMsg = 'Cannot connect to server. Make sure the Flask server is running on http://localhost:5000';
        }
        addMessage('assistant', errorMsg, new Date().toISOString());
    } finally {
        sendButton.disabled = false;
        sendButton.textContent = 'Send';
    }
}

function addMessage(role, content, timestamp) {
    const messagesDiv = document.getElementById('messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}`;
    
    const bubble = document.createElement('div');
    bubble.className = 'message-bubble';
    bubble.textContent = content;
    
    const time = document.createElement('div');
    time.className = 'message-time';
    if (timestamp) {
        const date = new Date(timestamp);
        time.textContent = date.toLocaleTimeString();
    }
    
    messageDiv.appendChild(bubble);
    messageDiv.appendChild(time);
    messagesDiv.appendChild(messageDiv);
    
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

function clearMessages() {
    document.getElementById('messages').innerHTML = '';
}

function handleKeyPress(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}
