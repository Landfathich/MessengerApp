// Автопрокрутка к новым сообщениям
function scrollToBottom() {
    const chatMessages = document.getElementById('chatMessages');
    if (chatMessages) {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
}

// Автовысота textarea
function autoResize(textarea) {
    textarea.style.height = 'auto';
    textarea.style.height = Math.min(textarea.scrollHeight, 120) + 'px';
}

// Добавление нового сообщения в чат
function addMessageToChat(messageData) {
    const chatMessages = document.getElementById('chatMessages');
    if (!chatMessages) return;

    // Убираем сообщение "нет сообщений" если оно есть
    const emptyChat = chatMessages.querySelector('.empty-chat');
    if (emptyChat) {
        emptyChat.remove();
    }

    // Парсим сообщение (формат: "username: message")
    const colonIndex = messageData.indexOf(':');
    let username = 'Неизвестный';
    let messageText = messageData;

    if (colonIndex !== -1) {
        username = messageData.substring(0, colonIndex).trim();
        messageText = messageData.substring(colonIndex + 1).trim();
    }

    const isOwn = username === document.body.getAttribute('data-current-username');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isOwn ? 'own' : 'other'}`;

    const avatar = isOwn ?
        document.body.getAttribute('data-user-initial') :
        username.charAt(0).toUpperCase();

    const time = new Date().toLocaleTimeString('ru-RU', {
        hour: '2-digit',
        minute: '2-digit',
        hour12: false
    });

    messageDiv.innerHTML = `
        ${!isOwn ? `<div class="message-avatar">${username.charAt(0).toUpperCase()}</div>` : ''}
        
        <div class="message-content">
            ${!isOwn ? `<div class="message-sender">${username}</div>` : ''}
            
            <div class="message-text">${messageText}</div>
            
            <div class="message-time">${time}</div>
        </div>

        ${isOwn ? `<div class="message-avatar">${avatar}</div>` : ''}
    `;

    chatMessages.appendChild(messageDiv);
    scrollToBottom();
}

// Отправка сообщения
function sendMessage() {
    const messageInput = document.getElementById('messageInput');
    const message = messageInput.value.trim();

    if (message && window.chatSocket) {
        window.chatSocket.send(JSON.stringify({
            'message': message
        }));
        messageInput.value = '';
        autoResize(messageInput);
    }
}

// Инициализация чата
function initializeChat(conversationId, currentUsername) {
    window.chatSocket = new WebSocket('ws://' + window.location.host + '/ws/chat/' + conversationId + '/');

    window.chatSocket.onmessage = function (event) {
        const data = JSON.parse(event.data);
        addMessageToChat(data.message); // Передаем все сообщение
    };

    window.chatSocket.onopen = function () {
        console.log('WebSocket connected');
    };

    window.chatSocket.onerror = function (error) {
        console.error('WebSocket error:', error);
    };

    // Обработчики событий для поля ввода
    const messageInput = document.getElementById('messageInput');
    const sendButton = document.querySelector('.send-button');

    if (messageInput) {
        messageInput.addEventListener('keypress', function (e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendMessage();
            }
        });

        messageInput.addEventListener('input', function () {
            autoResize(this);
        });

        // Фокус на поле ввода
        messageInput.focus();
    }

    if (sendButton) {
        sendButton.addEventListener('click', sendMessage);
    }

    // Прокрутка при загрузке
    window.addEventListener('load', scrollToBottom);
}