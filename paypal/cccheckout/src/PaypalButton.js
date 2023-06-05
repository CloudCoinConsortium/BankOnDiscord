// import React, { useEffect, useRef } from 'react';

// function PayPalButton({ total }) {

//   useEffect(() => {
//     window.paypal.Buttons({
//       createOrder: (data, actions, err) => {
//         return actions.order.create({
//           intent: "CAPTURE",
//           purchase_units: [
//             {
//               description: "Your order description",
//               amount: {
//                 currency_code: "USD",
//                 value: total,
//               },
//             },
//           ],
//         });
//       },
//       onApprove: async (data, actions) => {
//         const order = await actions.order.capture();
//         console.log(order);
//         // Here you can call your backend API to save the order details
//       },
//       onError: (err) => {
//         console.log(err);
//       },
//     })
//     .render(paypal.current);
//   }, []);

//   return (
//     <div>
//       <div ref={paypal}></div>
//     </div>
//   );
// }

// export default PayPalButton;
