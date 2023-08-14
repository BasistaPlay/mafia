document.addEventListener("DOMContentLoaded", function() {
  setInterval(updateRooms, 5000); // Atjaunina istabu sarakstu ik pēc 5 sekundēm
});

function updateRooms() {
  $.ajax({
    url: '/game-room/get_room_data/', // Aizvietojiet ar savu URL
    type: 'GET',
    dataType: 'json',
    success: function(data) {
      var roomListBody = document.getElementById('room-list-body');
      roomListBody.innerHTML = ''; // Notīra esošo sarakstu

      data.room_data.forEach(room => {
        if (room.player_count < room.max_players) {
          var roomRow = document.createElement('tr');
          roomRow.classList.add('data');

          var roomCodeCell = document.createElement('td');
          roomCodeCell.textContent = room.code;
          roomRow.appendChild(roomCodeCell);

          var playerCountCell = document.createElement('td');
          var playerCountSpan = document.createElement('span');
          playerCountSpan.classList.add('player-count');
          playerCountSpan.dataset.playerCount = room.player_count;
          playerCountSpan.textContent = room.player_count;
          playerCountCell.appendChild(playerCountSpan);

          playerCountCell.innerHTML += ' / ';

          var maxPlayersSpan = document.createElement('span');
          maxPlayersSpan.classList.add('max-players');
          maxPlayersSpan.dataset.maxPlayers = room.max_players;
          maxPlayersSpan.textContent = room.max_players;
          playerCountCell.appendChild(maxPlayersSpan);

          roomRow.appendChild(playerCountCell);

          var privateCell = document.createElement('td');
          if (room.is_private) {
            var privateIcon = document.createElement('i');
            privateIcon.classList.add('fas', 'fa-lock');
            privateCell.appendChild(privateIcon);
          } else {
            var privateIcon = document.createElement('i');
            privateIcon.classList.add('fas', 'fa-unlock');
            privateIcon.style.color = '#ffffff';
            privateCell.appendChild(privateIcon);
          }
          roomRow.appendChild(privateCell);

          var joinCell = document.createElement('td');
          var joinLink = document.createElement('a');
          joinLink.classList.add('join-room-link');
          joinLink.href = '#';
          joinLink.textContent = 'Join';
          joinLink.onclick = function() {
            joinRoom(room.code);
            return false; // Lai novērstu noklikšķināšanu saitē
          };
          joinCell.appendChild(joinLink);
          roomRow.appendChild(joinCell);

          roomListBody.appendChild(roomRow);
        }
        });

      setupPasswordInputs();
    },
    error: function(error) {
      console.error('Kļūda atjauninot istabu sarakstu:', error);
    }
  });
}

function joinRoom(roomCode) {
  // Jūsu esošā koda loģika, piemēram, localStorage saglabāšana utt.

  // Pāradresācija uz jūsu apstrādes funkciju ar pareizi sagatavotiem datiem
  handleJoinRoom(roomCode);
}

function handleJoinRoom(roomCode) {
  const formData = new FormData();
  formData.append('real_code', roomCode);

  fetch('/game-room/join-room/', {
    method: 'POST',
    body: formData,
    headers: {
      'X-CSRFToken': getCookie('csrftoken'),
    },
  })
    .then(response => {
      if (response.ok) {
        // Pāradresācija uz vēlamo istabu
        window.location.href = `/game-room/room/${roomCode}/`;
      } else {
        // Apstrādāt kļūdas, ja tādas ir
        const errorContainer = document.querySelector('.error');
        errorContainer.textContent = 'Room is full or there was an error.';
        errorContainer.style.display = 'block';
      }
    })
    .catch(error => {
      // Apstrādāt fetch kļūdas, ja tādas ir
      console.error('Error joining room:', error);
    });
}

// Palīgfunkcija, lai iegūtu CSRF token no sīkfaila
function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
