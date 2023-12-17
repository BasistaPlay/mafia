function getCookie(name) {
	let cookieValue = null
	if (document.cookie && document.cookie !== '') {
		const cookies = document.cookie.split(';');
		for (let i = 0; i < cookies.length; i++) {
			const cookie = cookies[i].trim();
			// Atrodam CSRF token sīkdatnē
			if (cookie.startsWith(name + '=')) {
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				break;
			}
		}
	}
	return cookieValue
}

const inputFields = document.querySelectorAll('.input-field')
const codeHiddenInput = document.getElementById('code_hidden')
const submitButton = document.getElementById('submit_button')

inputFields.forEach((input, index, arr) => {
	input.addEventListener('input', () => {
		if (input.value.length === 1) {
			if (index < arr.length - 1) {
				arr[index + 1].focus()
			}
			if (index === arr.length - 1) {
				submitButton.style.display = 'none'
				let codeValue = ''
				inputFields.forEach(input => {
					codeValue += input.value
				})
				codeHiddenInput.value = codeValue
				if (codeValue.length === 6) {
					document.querySelector('.Room_code').submit()
				}
			}
		}
	})

	input.addEventListener('keydown', event => {
		if (event.key === 'Backspace' && index > 0) {
			const value = input.value
			if (!value) {
				arr[index - 1].focus()
				arr[index - 1].value = ''
			}
		}
	})
})
