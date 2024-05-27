const pincodeInput = document.getElementById('pincode-input');
const submitButton = document.getElementById('submit-button');
const websiteInterface = document.getElementById('website-interface');
const pincodePrompt = document.getElementById('pincode-prompt');

submitButton.addEventListener('click', () => {
  pincode = pincodeInput.value;
  if (isValidPincode(pincode)) {
    pincodePrompt.style.display = 'none';
    websiteInterface.style.display = 'block';
			$.ajax({ 
				url: '/pincode_post', 
				type: 'POST', 
				data: { 'pin': pincode }, 
				success: function(response) { 
					document.getElementById('output').innerHTML = response; 
				}, 
				error: function(error) { 
					console.log(error); 
				} 
			}); 
		} 
  else {
    alert('Pincode is invalid. Enter a valid 6 digit pincode');
  }
});

function isValidPincode(pincode) {
	return /^\d{6}$/.test(pincode);
  }

// Display the pincode prompt popup
pincodePrompt.style.display = 'block';