const pincodeInput = document.getElementById('pincode-input');
const submitButton = document.getElementById('submit-button');
const websiteInterface = document.getElementById('website-interface');

submitButton.addEventListener('click', () => {
  const pincode = pincodeInput.value;
  if (isSixDigitNumber(pincode)) {
    window.location.href = "file:///C:/Imp Files/Price Comparision Website/Website/search.html";
    
  } else {
    alert('Sorry, we do not offer services in this area.');
  }
});

function isSixDigitNumber(pincode) {
  // Use a regular expression to match exactly six digits
  const regex = /^\d{6}$/; 
  return regex.test(pincode);
}