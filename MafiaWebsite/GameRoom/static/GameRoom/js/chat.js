// chat.js

function setupChat(roomCode, csrfToken) {
    // Ievērojam taustiņa "Enter" nospiešanas notikumu ievades laukā
    $('#message-input').keypress(function(event) {
      // Pārbaudām, vai ir nospiesta taustiņa "Enter"
      if (event.which === 13) {
        // Izpildām tādu pašu darbību kā klikšķināt uz "Send" pogas
        sendMessage();
      }
    });
  
    // Ievērojam čata formas iesniegšanas notikumu, ja tiek klikšķināta "Send" poga
    $('#send-button').click(sendMessage);
  
    function sendMessage() {
      var message = $('#message-input').val();
  
      // iesniegt ziņu serverim, izmantojot AJAX pieprasījumu
      $.ajax({
        url: '/game-room/send-message/' + roomCode + '/',
        method: 'POST',
        data: {
          'message': message,
          'csrfmiddlewaretoken': csrfToken,
        },
        success: function(response) {
          // Veiksmīga atbilde no servera
          console.log('Message sent successfully');
          // Veikt vajadzīgos soļus pēc ziņas nosūtīšanas, piemēram, atjaunot čatu
          $('#message-input').val('');
          fetchChatMessages();
        },
        error: function(error) {
          // Kļūda sazinoties ar serveri
          console.log('Error sending message:', error);
        }
      });
    }
  
    function fetchChatMessages() {
      $.ajax({
        url: '/game-room/fetch-messages/' + roomCode + '/',
        method: 'GET',
        success: function(response) {
          // Veiksmīga atbilde no servera ar jaunajiem čata ierakstiem
          var messages = response.messages;
          var chatMessagesHtml = '';
  
          // Iterēt caur katru ierakstu un pievienot lietotājvārdu un ziņu HTML
          for (var i = 0; i < messages.length; i++) {
            var message = messages[i];
            var chatMessage = '<div class="Chats"><strong>' + message.sender + ':</strong> ' + message.message + '</div>';
            chatMessagesHtml += chatMessage;
          }
  
          // Pievienot jauno HTML saturu chat logam
          $('#chat-messages').html(chatMessagesHtml);
        },
        error: function(error) {
          // Kļūda sazinoties ar serveri
          console.log('Error fetching chat messages:', error);
        }
      });
    }
  
    // Iestatīt atkārtotu funkciju izsaukumu, lai automātiski atjaunotu čatu (piemēram, ik pēc 5 sekundēm)
    setInterval(fetchChatMessages, 5000);
  
    // Izsaukt funkciju, lai ielādētu esošos čata ierakstus, kad skats ir gatavs
    $(window).on('load', function() {
      fetchChatMessages();
    });
  }
  

  