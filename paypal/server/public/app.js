paypal
  .Buttons({
    // Sets up the transaction when a payment button is clicked
    createOrder: function(data, actions) {
      // This function sets up the details of the transaction
      const urlParams = new URLSearchParams(window.location.search);
      const orderID = urlParams.get('orderID');
      return orderID;
    },

    // Finalize the transaction after payer approval
    onApprove: function (data, actions) {
      return fetch(`/api/orders/${data.orderID}/capture`, {
        method: "post",
      })
        .then((response) => response.json())
        .then(function (orderData) {
          // Successful capture! For dev/demo purposes:
          console.log(
            "Capture result",
            orderData,
            JSON.stringify(orderData, null, 2)
          );
          var transaction = orderData.purchase_units[0].payments.captures[0];
          alert(
            "Transaction " +
              transaction.status +
              ": " +
              transaction.id +
              "\n\nSee console for all available details"
          );
        });
    },
  })
  .render("#paypal-button-container");
