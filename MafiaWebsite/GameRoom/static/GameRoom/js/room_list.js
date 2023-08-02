// Iegūst elementu, kuram jātiek atjauninātam
const roomListContainer = document.getElementById("room-list-container");

// Funkcija, kas atjaunina istabu sarakstu no servera un atjauno HTML
function updateRoomList() {
  // Iestata XMLHttpRequest objektu
  var xhr = new XMLHttpRequest();

  // Uzstāda pieprasījuma metodi un URL
  xhr.open("GET", "/game-room/get-room-list/", true); // Nomainiet "/api/get_rooms/" ar savu servera ceļu

  // Uzstāda, ka vēlamies saņemt datu tipu "html"
  xhr.responseType = "html";

  // Funkcija, kas tiks izsaukta, kad pieprasījums būs veiksmīgs
  xhr.onload = function () {
    if (xhr.status === 200) {
      // Iegūst jauno sarakstu no atbildes
      var newRoomList = xhr.response;

      // Atjauno saraksta datus
      roomListContainer.innerHTML = newRoomList;
    }
  };

  // Funkcija, kas tiks izsaukta, ja pieprasījums neizdosies
  xhr.onerror = function () {
    console.error("Failed to update room list.");
  };

  // Sūta pieprasījumu
  xhr.send();
}

// Iestatiet setInterval, lai izsauktu funkciju ik pēc 5 sekundēm
setInterval(updateRoomList, 5000); // 5000 milisekundes = 5 sekundes