function fetchPlayerList() {
  // Iegūstam istabas kodu no kāda avota, piemēram, no HTML elementa
  var roomCode = document.getElementById('room-code').getAttribute('data-room-code');

  // Veidojam AJAX pieprasījumu uz serveri, nododot istabas kodu
  $.ajax({
    url: `/game-room/fetch-players/${roomCode}/`,
    type: 'GET',
    success: function(data) {
      // Atjaunojam spēlētāju sarakstu ar jauno HTML fragmentu
      $('#player-list').html(data.player_list_html);
    },
    error: function(xhr, status, error) {
      console.log(error); // Varat izvadīt kļūdu konsolē, lai labāk saprastu, kas notiek
    }
  });
}
function updatePlayerCountAndList() {
  var roomCode = document.getElementById('room-code').getAttribute('data-room-code');
  var url = `/game-room/get-player-count/${roomCode}/`;

  fetch(url)
    .then(response => response.json())
    .then(data => {
      var playerCount = data.player_count;
      var maxPlayers = data.max_players;
      var playerListHtml = data.player_list_html;

      var playerCountSpan = document.getElementById('player-count');
      playerCountSpan.textContent = playerCount + ' / ' + maxPlayers;

      var playerListElement = document.getElementById('player-list');
      playerListElement.innerHTML = playerListHtml;
    })
    .catch(error => {
      console.error('Error:', error);
    });
}

// Atjauno spēlētāju skaitu un sarakstu ik pēc 5 sekundēm
setInterval(updatePlayerCountAndList, 5000);
// Atjauno spēlētāju sarakstu ik pēc 5 sekundēm
setInterval(fetchPlayerList, 5000);
