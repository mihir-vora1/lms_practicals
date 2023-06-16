// Handle form submission
var form = document.getElementById('payment-form');
var submitButton = document.getElementById('submit-payment');

submitButton.addEventListener('click', function(event) {
  event.preventDefault();

  // Collect the payment details from the form
  var cardElement = elements.create('card');
  stripe.createPaymentMethod({
    type: 'card',
    card: cardElement,
  }).then(function(result) {
    if (result.error) {
      // Handle errors from Stripe.js
      console.log(result.error);
    } else {
      // Retrieve the payment method ID from the result
      var paymentMethodId = result.paymentMethod.id;

      // Include the payment method ID in your form submission
      // and submit the form to your server
      var hiddenInput = document.createElement('input');
      hiddenInput.setAttribute('type', 'hidden');
      hiddenInput.setAttribute('name', 'payment_method_id');
      hiddenInput.setAttribute('value', paymentMethodId);
      form.appendChild(hiddenInput);

      form.submit();
    }
  });
});