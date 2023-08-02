var isPrivateCheckbox = document.getElementById('is-private');
var passwordField = document.getElementById('password-field');

isPrivateCheckbox.addEventListener('change', function() {
  if (isPrivateCheckbox.checked) {
    passwordField.disabled = false;
  } else {
    passwordField.value = '';
    passwordField.disabled = true;
  }
});

isPrivateCheckbox.addEventListener('click', function() {
  if (!isPrivateCheckbox.checked) {
    passwordField.value = '';
  }
});

const socialButtons = document.querySelectorAll('.social div');

socialButtons.forEach(button => {
  button.addEventListener('mouseenter', () => {
    button.classList.add('snake-animation');
  });

  button.addEventListener('mouseleave', () => {
    button.classList.remove('snake-animation');
  });
});

function togglePasswordVisibility() {
    var passwordInput = document.getElementById("password");
    var toggleIcon = document.getElementsByClassName("toggle-password")[0];

    if (passwordInput.type === "password") {
        passwordInput.type = "text";
        toggleIcon.classList.remove("visible");
    } else {
        passwordInput.type = "password";
        toggleIcon.classList.add("visible");
    }
}

const plus = document.querySelector(".plus"),
    minus = document.querySelector(".minus"),
    num = document.querySelector(".num");
    let a = 1;
    plus.addEventListener("click", ()=>{
      a++;
      a = (a < 10) ? "0" + a : a;
      num.innerText = a;
    });
    minus.addEventListener("click", ()=>{
      if(a > 1){
        a--;
        a = (a < 10) ? "0" + a : a;
        num.innerText = a;
      }
    });


    // Iegūst span elementu un inputa elementu
    document.addEventListener("DOMContentLoaded", function() {
      var playerCountSpan = document.getElementById("player-count");
      var playerCountInput = document.getElementById("player-count-input");
    
      if (playerCountSpan && playerCountInput) {
        playerCountInput.value = playerCountSpan.textContent;
      }
    });
