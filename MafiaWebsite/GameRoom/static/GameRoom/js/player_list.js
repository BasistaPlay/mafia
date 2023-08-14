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
                var playerHTML = '<li data-player-id="' + player.id + '">';

                if (player.is_owner) {
                    playerHTML += '<strong>' + player.username + '  </strong><i class="fas fa-crown"></i>';
                } else {
                    playerHTML += player.username;
                }

                var removePlayerLink = '';
                var assignOwnerLink = '';

                // Pārbaudām, vai lietotājvārds sakrīt ar pašreizējā lietotāja lietotājvārdu, lai pievienotu pogas
                if (!player.is_owner && player.username !== currentUsername) {
                    // Iegūstam spēlētāja ID no paslēptā div elementa
                    var playerId = $(playerHTML).find('.hidden-player-id').text();

                    removePlayerLink = '<a href="/game-room/room/' + roomCode + '/remove-player/' + playerId + '">Remove</a>';
                    assignOwnerLink = '<a href="/game-room/change-owner/' + roomCode + '/' + playerId + '">Assign as Owner</a>';
                    console.log(playerId);
                }

                playerHTML += removePlayerLink + assignOwnerLink + '</li>';
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
