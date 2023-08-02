function checkAndDeleteRoom(roomCode) {
  $.ajax({
    url: '/game-room/check-and-delete-room/' + roomCode + '/',
    method: 'GET',
    success: function(response) {
      if (response.status === 'deleted') {
        // Ja serveris atgriež "deleted" atbildi, nozīmē, ka istaba tika izdzēsta
        // Varat veikt vajadzīgos soļus, lai redirektētu lietotāju vai parādītu kādu paziņojumu
        alert('Istaba tika izdzēsta, jo tajā vairs nav cilvēku.');
        window.location.href = '/some-other-page/'; // piemēram, pāradresē lietotāju uz citu lapu
      } else {
        // Ja istaba netika izdzēsta, varat izpildīt citas darbības vai parādīt paziņojumu
        console.log('Istaba vēl pastāv, cilvēki joprojām ir istabā.');
      }
    },
    error: function(error) {
      // Kļūda sazinoties ar serveri
      console.log('Error checking and deleting room:', error);
    }
  });
}