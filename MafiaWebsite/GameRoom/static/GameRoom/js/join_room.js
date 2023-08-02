const inputFields = document.querySelectorAll('.input-field');
const codeHiddenInput = document.getElementById('code_hidden');
const submitButton = document.getElementById('submit_button');
const passwordInput = document.querySelector('.password');

// Funkcija, lai pārbaudītu, vai visi ievades lauki ir aizpildīti
function checkInputs() {
  let codeValue = '';
  inputFields.forEach((input) => {
    codeValue += input.value.trim();
  });
  codeHiddenInput.value = codeValue;

  // Parādīt iesniegšanas pogu, ja visi ievades lauki ir aizpildīti
  if (codeValue.length === 6) {
    submitButton.style.display = 'none';
  } else {
    submitButton.style.display = 'none';
  }
}

// Automātiski fokusēties uz pirmo ievades lauku
inputFields[0].focus();

// Pievienot notikumu klausītājus ievades laukiem, lai pārvietotos uz nākamo lauku ievades laikā
inputFields.forEach((input, index, arr) => {
  input.addEventListener('input', (event) => {
    const value = event.target.value;
    if (value && index < arr.length - 1) {
      arr[index + 1].focus();
    }
    checkInputs();

    // Pārbaudīt, vai ir ievadīti visi 6 simboli un automātiski iesniegt formu
    if (index === arr.length - 1 && value && value.length === 1) {
      submitButton.click();
    }
  });

  // Pievienot notikumu klausītāju, lai pārvaldītu "Backspace" taustiņu un pārslēgtos uz iepriekšējo lauku
  input.addEventListener('keydown', (event) => {
    if (event.key === 'Backspace' && index > 0) {
      const value = event.target.value;
      if (!value) {
        arr[index - 1].focus();
        arr[index - 1].value = '';
      }
      checkInputs();
    }
  });
});

// Pievienot notikumu klausītāju formu iesniegšanai
document.querySelector('.Room_code').addEventListener('submit', (event) => {
  event.preventDefault();

  // Iegūt istabas kodu un paroli
  const roomCode = codeHiddenInput.value;
  const password = passwordInput ? passwordInput.value : '';

  // Izveidot FormData objektu ar istabas kodu un paroli
  const formData = new FormData();
  formData.append('room_code', roomCode);
  formData.append('password', password);

  // Veikt POST pieprasījumu serverim, lai pievienotos istabai
  fetch(joinRoomURL, {
    method: 'POST',
    body: formData,
    headers: {
      'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
    },
  })
    .then((response) => {
      if (response.ok) {
        // Novirzīt uz vēlamo istabu, ja parole ir pareiza
        window.location.href = `/game-room/room/${roomCode}/`;
      } else {
        // Apstrādāt nepareizu paroli vai citas kļūdas šeit
      }
    })
    .catch((error) => {
      // Apstrādāt fetch kļūdas šeit
    });
});

// Izsaukt checkInputs funkciju sākotnēji, lai pārbaudītu ievades laukus lapas ielādes laikā
checkInputs();