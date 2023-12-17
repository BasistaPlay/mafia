$(document).ready(function () {
	const roomHeader = document.getElementById('roomHeader');
	const roomCodeElement = $('#roomCode');

	const roomCode = roomCodeElement.data('room-code');

	roomHeader.addEventListener('click', () => {
		roomCodeElement.text(
			roomCodeElement.text() === '******' ? roomCode : '******'
		);
	});
});


// Funkcija, lai iegūtu CSRF token no sīkdatnēm
function getCookie(name) {
	let cookieValue = null;
	if (document.cookie && document.cookie !== '') {
		const cookies = document.cookie.split(';');
		for (let i = 0; i < cookies.length; i++) {
			const cookie = cookies[i].trim();
			// Atrodam CSRF token sīkdatnē
			if (cookie.startsWith(name + '=')) {
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				break;
			}
		}
	}
	return cookieValue
}

const roomMessages = document.getElementById('room-messages');
const wsProtocol = window.location.protocol === 'https:' ? 'wss://' : 'ws://'
const roomCode = $('#roomCode').data('room-code');

const socket = new WebSocket(
	wsProtocol + window.location.host + `/ws/room/${roomCode}/`
);


socket.addEventListener('message', event => {
	const data = JSON.parse(event.data);

	if (data.message) {
		// Atjauniniet tērzēšanas logu ar ziņojumiem
		appendRoomMessage(data.message);
	}

	if (data.message_leave) {
		// Attēlojiet iziešanas ziņojumu tērzēšanas logā
		appendLeaveMessage(data.message_leave);
	}

	if (data.message_join) {
		// Attēlojiet pievienošanās ziņojumu tērzēšanas logā
		appendJoinRoomMessage(data.message_join);
	}

	if (data.player_list) {
		// Atjaunojiet spēlētāju sarakstu klienta pusē
		updatePlayerList(data.player_list);
	}

	if (data.player_count !== undefined && data.max_players !== undefined) {
		const playerCountElement = document.getElementById('player-count');
		if (playerCountElement) {
			playerCountElement.innerHTML = `${data.player_count} / ${data.max_players}`;
		}
	}

	if (data.message) {
		appendMessage(data.message)
	}
	

});

function appendLeaveMessage(message) {
	// Attēlo ziņojumu tērzēšanas logā (HTML).
	const messageElement = document.createElement('p');
	messageElement.setAttribute('class', 'message-leave');
	messageElement.textContent = message;
	roomMessages.appendChild(messageElement);

	// Uzstāda timeout, lai noņemtu ziņojumu pēc 10 sekundēm.
	setTimeout(() => {
		roomMessages.removeChild(messageElement);
	}, 10000) // 10000 milisekundes (10 sekundes)
}

function appendJoinRoomMessage(message) {
	// Attēlo ziņojumu tērzēšanas logā (HTML).
	const messageElement = document.createElement('p');
	messageElement.setAttribute('class', 'message-Join');
	messageElement.textContent = message;
	roomMessages.appendChild(messageElement);

	// Uzstāda timeout, lai noņemtu ziņojumu pēc 10 sekundēm.
	setTimeout(() => {
		roomMessages.removeChild(messageElement)
	}, 10000) // 10000 milisekundes (10 sekundes)
}

function updatePlayerList(playerList) {
	const playerListElement = document.getElementById('player-list') // Aizvietojiet ar jūsu spēlētāju saraksta HTML elementu
	playerListElement.innerHTML = '' // Notīra esošo sarakstu

	playerList.forEach(player => {
		const playerElement = document.createElement('li');
		playerElement.className = 'player-list';
		playerElement.setAttribute('data-player-id', player.id);

		if (player.is_owner) {
			const crownIcon = document.createElement('i');
			crownIcon.className = 'fas fa-crown';
			playerElement.appendChild(crownIcon);

			const strongElement = document.createElement('strong')
			strongElement.textContent = player.username;
			playerElement.appendChild(strongElement);
		} else {
			playerElement.textContent = player.username;
		}

		playerListElement.appendChild(playerElement)
	})
}

function updatePlayerCount(playerCount, maxPlayers) {
	const playerCountSpan = document.getElementById('player-count')
	if (playerCountSpan) {
		playerCountSpan.textContent = `${playerCount} / ${maxPlayers}`
	}
}