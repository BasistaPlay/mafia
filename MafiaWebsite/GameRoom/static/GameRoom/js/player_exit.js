$(document).ready(function () {
    var roomCode = $('#room-code').data('room-code');
    var currentUsername = $('#current-username').data('current-username');
    var csrftoken = $('[name=csrfmiddlewaretoken]').val();

    function checkUserStatus() {
        $.ajax({
            url: '/game-room/check-user-status/',
            type: 'POST',
            data: {
                room_code: roomCode,
                current_username: currentUsername,
                csrfmiddlewaretoken: csrftoken
            },
            success: function(response) {
                console.log(response.message);
            },
            error: function(error) {
                console.log('Error checking user status:', error);
            }
        });
    }

    // Palaist pirmo reizi un pēc tam ik pēc 5 sekundēm
    checkUserStatus();
    setInterval(checkUserStatus, 5000);

    $(window).on('beforeunload', function() {
        $.ajax({
            url: '/game-room/leave-room/',
            type: 'POST',
            data: {
                room_code: roomCode,
                current_username: currentUsername,
                csrfmiddlewaretoken: csrftoken
            },
            async: false,
            success: function(response) {
                console.log(response.message);
            },
            error: function(error) {
                console.log('Error leaving room:', error);
            }
        });
    });
});
