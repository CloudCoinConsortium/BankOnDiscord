import React, { useState } from "react";
import "./product.style.css";
import "../assests/laptop.jpg";



function App() {
 
  return (
    <div className="Product-container">
      <header className="Product-content">
      
        <div className="product">
           
          <img src={require("../assests/laptop.jpg")} alt="laptop" />
          
        </div>
        <div className="desc">
          <h2> MacBook Pro</h2>
          <p>
               Lorem ipsum dolor sit amet consectetur adipisicing elit. Maxime mollitia,
               molestiae quas vel sint commodi repudiandae consequuntur voluptatum laborum
          </p>
          <h3>Price: $1.00</h3>
      
        </div>
     
      </header>
    </div>
  );
}

export default App;