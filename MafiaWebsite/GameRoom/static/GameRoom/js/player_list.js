// room_actions.js

function updatePlayerList() {
    var roomCode = $('#room-code').data('room-code');
    var currentUsername = $('#current-username').data('current-username');

    $.ajax({
        url: '/game-room/fetch-players/' + roomCode + '/',
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            var playerListContainer = $('#player-list');
            playerListContainer.empty();

            data.players.forEach(function (player) {
                var playerHTML = '<li>';

                if (player.is_owner) {
                    playerHTML += '<strong>' + player.username + '  </strong><i class="fas fa-crown"></i>';
                } else {
                    playerHTML += player.username;
                }

                // Pārbaudām, vai lietotājvārds sakrīt ar pašreizējā lietotāja lietotājvārdu, lai pievienotu pogas
                if (!player.is_owner && player.username !== currentUsername) {
                    playerHTML +=
                        '<a href="/game-room/room/' + roomCode + '/remove-player/' + player.id + '">Remove</a>' +
                        '<a href="/game-room/change-owner/' + roomCode + '/' + player.id + '">Assign as Owner</a>';
                }

                playerHTML += '</li>';
                playerListContainer.append(playerHTML);
            });
        },
        error: function (error) {
            console.log('Error fetching players:', error);
        },
    });
}

// Izmantojot funkciju, izsaucam to bez argumentiem
updatePlayerList();

// Atjauno spēlētāju sarakstu ik pēc 5 sekundēm
setInterval(function () {
    updatePlayerList();
}, 5000);
