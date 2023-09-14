var isPrivateCheckbox = document.getElementById('is-private')
var passwordField = document.getElementById('password-field')

isPrivateCheckbox.addEventListener('change', function () {
	if (isPrivateCheckbox.checked) {
		passwordField.disabled = false
	} else {
		passwordField.value = ''
		passwordField.disabled = true
	}
})

document.addEventListener('DOMContentLoaded', function () {
	var playerCountInput = document.getElementById('player-count-input')
	var minusButton = document.querySelector('.minus')
	var plusButton = document.querySelector('.plus')
	var num = document.querySelector('.num')
	let a = parseInt(num.innerText, 10)

	if (playerCountInput && minusButton && plusButton && num) {
		minusButton.addEventListener('click', function () {
			if (a > 6) {
				a--
				a = a < 10 ? '0' + a : a
				num.innerText = a
				playerCountInput.value = a
				updateButtons(a)
			}
		})

		plusButton.addEventListener('click', function () {
			if (a < 12) {
				a++
				a = a < 10 ? '0' + a : a
				num.innerText = a
				playerCountInput.value = a
				updateButtons(a)
			}
		})

		function updateButtons(value) {
			if (value <= 6) {
				minusButton.style.display = 'none'
				plusButton.style.display = 'inline'
			} else if (value >= 12) {
				plusButton.style.display = 'none'
				minusButton.style.display = 'inline'
			} else {
				minusButton.style.display = 'inline'
				plusButton.style.display = 'inline'
			}
		}

		updateButtons(a)
	}
})
