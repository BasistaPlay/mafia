$(document).ready(function() {
  const roomHeader = document.getElementById('roomHeader');
  const roomCodeElement = $('#roomCode');
  
  const roomCode = roomCodeElement.data('room-code');
  
  roomHeader.addEventListener('click', () => {
    roomCodeElement.text(roomCodeElement.text() === '******' ? roomCode : '******');
  });
});

document.addEventListener("DOMContentLoaded", function() {
  setInterval(updatePlayerCount, 5000); // Atjaunina spēlētāju skaitu ik pēc 5 sekundēm
});

function updatePlayerCount() {
  const playerCountSpan = document.getElementById('player-count');
  if (playerCountSpan) {
    var roomCode = document.getElementById('room-code').getAttribute('data-room-code');
    fetch(`/game-room/update-player-count/${roomCode}/`, {
      method: 'GET',
    })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          playerCountSpan.textContent = `${data.player_count} / ${data.max_players}`;
        }
      })
      .catch(error => {
        console.error('Error updating player count:', error);
      });
  }
}

// Pārbauda, vai visi spēlētāji ir gatavi
function areAllPlayersReady() {
  // Jūsu kods, kas pārbauda, vai visi spēlētāji ir gatavi
  // Šeit jums jāatgriež true, ja visi ir gatavi, un false, ja nav
  return true; // Piemērs: vienmēr atgriež true, lai pārbaudītu, ka spēle ir gatava
}

// Parāda ziņojumu "Spēle sākas"
function showGameStartMessage() {
  const gameStartMessage = document.getElementById("game-start-message");
  gameStartMessage.style.display = "block";
}

// // Kad spēles sākšanas poga tiek noklikšķināta
// document.getElementById("start-game-button").addEventListener("click", function () {
//   if (areAllPlayersReady()) {
//     // Ja visi spēlētāji ir gatavi, tad izsauc funkciju, kas parāda ziņojumu
//     showGameStartMessage();
//   } else {
//     alert("Gaidiet, līdz visi spēlētāji ir gatavi!");
//   }
// });


// const roomMessages = document.getElementById("room-messages"); // Iegūstam elementu, kurā tiks attēloti ziņojumi.
// const wsProtocol = window.location.protocol === "https:" ? "wss://" : "ws://";
// const roomCode = $('#roomCode').data('room-code');
// const socket = new WebSocket(wsProtocol + window.location.host + `/ws/some_path/${roomCode}/`);

// socket.onopen = (e) => {
//     console.log("WebSocket connection opened.");
// };

// socket.onmessage = (e) => {
//     const data = JSON.parse(e.data);
//     if (data.message) {
//         appendRoomMessage(data.message);
//     }
//     if (data.leaveMessage) {
//         appendRoomMessage(data.leaveMessage);
//     }
// };

// // ... citas WebSocket funkcijas ...

// function appendRoomMessage(message) {
//     // Attēlo ziņojumu tērzēšanas logā (HTML).
//     const messageElement = document.createElement("p");
//     messageElement.textContent = message;
//     roomMessages.appendChild(messageElement);
// }


const roomMessages = document.getElementById("room-messages"); // Iegūstam elementu, kurā tiks attēloti ziņojumi.
const wsProtocol = window.location.protocol === "https:" ? "wss://" : "ws://";
const roomCode = $('#roomCode').data('room-code');
const socket = new WebSocket(wsProtocol + window.location.host + `/ws/some_path/${roomCode}/`);

socket.onopen = (e) => {
    console.log("WebSocket connection opened.");
};

socket.onmessage = (e) => {
    const data = JSON.parse(e.data);
    if (data.message) {
        appendRoomMessage(data.message);
    }
    if (data.leaveMessage) {
        appendLeaveMessage(data.leaveMessage);
    }
    if (data.join_message) {
      appendJoinRoomMessage(data.joinMessage);
  }
};

// ... citas WebSocket funkcijas ...

// function appendRoomMessage(message) {
//     // Attēlo ziņojumu tērzēšanas logā (HTML).
//     const messageElement = document.createElement("p");
//     messageElement.textContent = message;
//     messageElement.classList.add("message-leave")
//     roomMessages.appendChild(messageElement);
// }

function appendRoomMessage(message) {
  // Attēlo ziņojumu tērzēšanas logā (HTML).
  const messageElement = document.createElement("p");
  messageElement.setAttribute("class", "message-leave");
  messageElement.textContent = message;
  roomMessages.appendChild(messageElement);

  // Uzstāda timeout, lai noņemtu ziņojumu pēc 10 sekundēm.
  setTimeout(() => {
      roomMessages.removeChild(messageElement);
  }, 10000); // 10000 milisekundes (10 sekundes)
}

function appendJoinRoomMessage(message) {
  // Attēlo ziņojumu tērzēšanas logā (HTML).
  const messageElement = document.createElement("p");
  messageElement.setAttribute("class", "message-Join");

  messageElement.textContent = message;
  roomMessages.appendChild(messageElement);

  // Uzstāda timeout, lai noņemtu ziņojumu pēc 10 sekundēm.
  setTimeout(() => {
      roomMessages.removeChild(messageElement);
  }, 10000); // 10000 milisekundes (10 sekundes)
}