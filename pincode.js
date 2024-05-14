const pincodeInput = document.getElementById('pincode-input');
const submitButton = document.getElementById('submit-button');
const websiteInterface = document.getElementById('website-interface');
const pincodePrompt = document.getElementById('pincode-prompt');

submitButton.addEventListener('click', () => {
  const pincode = pincodeInput.value;
  if (isServiceAvailable(pincode)) {
    pincodePrompt.style.display = 'none';
    websiteInterface.style.display = 'block';
  } else {
    alert('Sorry, we do not offer services in this area.');
  }
});

function isServiceAvailable(pincode) {
  return pincode === '123456';
}

// Display the pincode prompt popup
pincodePrompt.style.display = 'block';