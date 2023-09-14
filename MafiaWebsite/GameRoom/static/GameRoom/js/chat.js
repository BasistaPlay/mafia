document.addEventListener('DOMContentLoaded', function () {
        const chatLog = document.querySelector('#chat-box');
        const chatMessage = document.querySelector('#message-input');
        const chatSend = document.querySelector('#send-button');
        const roomCode = $('#roomCode').data('room-code')

        // Izveidojiet WebSocket savienojumu
        const socket = new WebSocket(
            'ws://' + window.location.host + `/ws/chat/${roomCode}/`
        );

        // Atverot WebSocket savienojumu
        socket.onopen = function (event) {
            console.log('WebSocket is open now.');
        };

        chatSend.addEventListener('click', sendMessage);

        chatMessage.addEventListener('keyup', function (event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        });

        // Saņemot WebSocket ziņojumu
        socket.onmessage = function (event) {
            const data = JSON.parse(event.data);

            if (data.username && data.message) {
                chatLog.innerHTML += `<p><strong>${data.username}:</strong> ${data.message}</p>`;
            }
        };

        function sendMessage() {
            const messageInput = document.getElementById('message-input');
            const message = messageInput.value;

            const messageData = {
								'type': 'chat_message',
                'message': message,
            };

            socket.send(JSON.stringify(messageData));
            messageInput.value = '';
        }

    });