function showAlert(message) {
  var alertMessage = document.getElementById('alert-message');
  alertMessage.textContent = message;
  alertMessage.classList.remove('hidden');
  setTimeout(function() {
    alertMessage.classList.add('hidden');
  }, 2000); // 10 seconds (10000 milliseconds)
}
