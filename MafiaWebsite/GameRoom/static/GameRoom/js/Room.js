$(document).ready(function() {
    // Ievērojiet, ka ir jāielādē jQuery bibliotēka
  
    // Ievērojam čata formas iesniegšanas notikumu
    $('#chat-form').submit(function(event) {
      event.preventDefault();  // Apturēt formas noklusējuma iesniegšanu
  
      // Iegūstam ziņas tekstu no ievades lauka
      var message = $('#message-input').val();
  
      // Iegūstam CSRF token no sīkdatnes
      var csrftoken = getCookie('csrftoken');
  
      // Iesniegt ziņu serverim, izmantojot AJAX pieprasījumu
      $.ajax({
        url: '/game-room/send-message/',  // Jūsu apstrādes skats
        method: 'POST',
        data: {
          'message': message
        },
        headers: {
          'X-CSRFToken': csrftoken  // Iekļauj CSRF token headerī
        },
        success: function(response) {
          // Veiksmīga atbilde no servera
          console.log('Message sent successfully');
          // Veikt vajadzīgos soļus pēc ziņas nosūtīšanas, piemēram, atjaunot čatu
        },
        error: function(error) {
          // Kļūda sazinoties ar serveri
          console.log('Error sending message:', error);
        }
      });
  
      // Notīrīt ievades lauku pēc ziņas nosūtīšanas
      $('#message-input').val('');
    });
  
    // Funkcija, kas atgriež CSRF token no sīkdatnes
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
  });
  