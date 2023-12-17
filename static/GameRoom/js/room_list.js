const roomListBody = document.getElementById('room-list-body');
const wsProtocol = window.location.protocol === 'https:' ? 'wss://' : 'ws://';
const csrfToken = getCsrfToken();

const socket = new WebSocket(
    `${wsProtocol}${window.location.host}/ws/room-list/?csrf_token=${csrfToken}`
);

socket.addEventListener('open', () => {
    const message = {
        type: 'get_rooms',
    };
    socket.send(JSON.stringify(message));
});

socket.addEventListener('message', (event) => {
    const data = JSON.parse(event.data);

    if (data.type === 'room_update') {
        roomListBody.innerHTML = '';

        data.rooms.forEach((room) => {
            if (room.player_count !== room.max_players) {
                const row = document.createElement('tr');
                row.classList.add('data');

                const codeCell = document.createElement('th');
                codeCell.textContent = room.code;
                row.appendChild(codeCell);

                const playerCountCell = document.createElement('th');
                playerCountCell.innerHTML = `
                    <span class="player-count" data-player-count="${room.player_count}">
                        ${room.player_count}
                    </span> / 
                    <span class="max-players" data-max-players="${room.max_players}">
                        ${room.max_players}
                    </span>
                `;
                row.appendChild(playerCountCell);

                const isPrivateCell = document.createElement('th');
                isPrivateCell.innerHTML = room.is_private
                    ? '<i class="fas fa-lock"></i>'
                    : '<i class="fas fa-unlock" style="color: #ffffff;"></i>';
                row.appendChild(isPrivateCell);

                const joinCell = document.createElement('th');
                if (room.is_private) {
                    joinCell.innerHTML = `
                        <form method="post" name="join-room-form" class="join-room-form" data-room-code="${room.code}">
                            <input type="hidden" name="room_code" value="${room.code}">
                            <input class="password" type="password" name="password" placeholder="Enter the password" data-room-code="${room.code}">
                            <input type="hidden" name="csrfmiddlewaretoken" value="${csrfToken}">
                            <button class="join-room-link" type="submit">Join</button>
                        </form>
                    `;
                } else {
                    joinCell.innerHTML = `
                        <form method="post" name="join-room-form" class="join-room-form" data-room-code="${room.code}">
                            <input type="hidden" name="room_code" value="${room.code}">
                            <input type="hidden" name="csrfmiddlewaretoken" value="${csrfToken}">
                            <button class="join-room-link" type="submit">Join</button>
                        </form>
                    `;
                }
                row.appendChild(joinCell);

                roomListBody.appendChild(row);
            }
        });
    } else if (data.type === 'success') {
        // Apstrādājam veiksmes ziņojumus (piemēram, kad lietotājs pievienojas istabai)
        console.log(data.message);
    } else if (data.type === 'error') {
        // Apstrādājam kļūdas ziņojumus (piemēram, kad ievadīta nepareiza parole)
        console.error(data.error);
    }
});

// Atjaunojam datus ik pec 15 sekundēm
setInterval(() => {
    console.log('refresh')
    const message = {
        type: 'get_rooms',
    };
    socket.send(JSON.stringify(message));
}, 15000);

function getCsrfToken() {
    const csrfCookie = document.cookie.match(/csrftoken=([^;]+)/);
    return csrfCookie ? csrfCookie[1] : null;
}