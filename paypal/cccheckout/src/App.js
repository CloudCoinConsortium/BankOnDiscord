import React, { useState } from "react";
import Product from "./components/Product";
import PayPalCheckout from "./components/PayPalCheckout";
import "./App.css";

function App() {
  const [checkout, setCheckOut] = useState(false);


  return (
  
      <div className="App">
        <header className="App-header">
          {checkout ? (
            <PayPalCheckout />
          ) : (
            <div className="Product">
              <button
                className="checkout"
                onClick={() => {
                  setCheckOut(true);
                }}
              >
                Add to Cart & Checkout
              </button>
              <Product />
            </div>
          )}
        </header>
     
      </div>
 
  );
}

export default App;
