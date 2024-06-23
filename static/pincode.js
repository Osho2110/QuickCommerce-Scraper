const pincodeInput = document.getElementById('pincode-input');
const submitButton = document.getElementById('submit-button');
const loadingPopup = document.getElementById('loading-popup');

console.log('pincodeInput:', pincodeInput);
console.log('submitButton:', submitButton);

pincodeInput.addEventListener('keypress', (event) => {
    if (event.key === 'Enter') {
        event.preventDefault();
        SendPin();
    }
});

submitButton.addEventListener('click', (event) => {
    event.preventDefault();
    SendPin();
});

function SendPin(){
  const pincode = pincodeInput.value;
  if (isValidPincode(pincode)) {
	showLoadingPopup();
			$.ajax({ 
				url: '/pincode_post', 
				type: 'POST', 
				data: { 'pin': pincode }, 
				success: function(data) { 
					hideLoadingPopup();
					if (data.redirect) {
						window.location.href = data.redirect;
					}
				}, 
				error: function(error) {
					hideLoadingPopup(); 
					console.log(error); 
				} 
 
			}); 
		} 
  else {
    alert('Pincode is invalid. Enter a valid 6 digit pincode');
  }
};

function isValidPincode(pincode) {
	return /^\d{6}$/.test(pincode);
  }

  function showLoadingPopup() {
    loadingPopup.style.display = 'flex';
}

function hideLoadingPopup() {
    loadingPopup.style.display = 'none';
}