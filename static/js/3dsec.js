function _3dsec(stripe_publishable_key, pi_secret) {
    document.addEventListener("DOMContentLoaded", function(event){
      var stripe = Stripe(stripe_publishable_key);

      stripe.confirmCardPayment(pi_secret).then(function(result) {
        if (result.error) {
          // Display error.message in your UI.
          $("#3ds_result").text("Spróbuj ponownie na <br /> Twoje Konto -> zamówienia");
          $("#3ds_result").addClass("text-danger");
          $("#3ds_result").addClass("testSucces");
        } else {
          // The payment has succeeded. Display a success message.
          $("#3ds_result").text("Thank you for payment");
          
          $("#3ds_result").html('<a href="https://ww-tech.pl/">Transakcja zakończona sukcesem <br />Powrót na strone główną</a>');
          $("#3ds_result").addClass("testSucces");
        }
      });
    }); // DOMContentLoaded
}