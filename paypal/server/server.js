import express from "express";
import * as paypal from "./paypal.js";
import fetch from "node-fetch";
import "dotenv/config"; // loads env variables from .env file

const { CLIENT_ID, APP_SECRET } = process.env;
const base = "https://api-m.sandbox.paypal.com";
console.log(CLIENT_ID)

const app = express();

app.use(express.static("public"));
app.use(express.json());
app.post("/api/orders", async (req, res) => {
  const order = await paypal.createOrder();
  res.json(order);
});

app.post("/api/order", async (req, res) => {
  console.log('Body:',JSON.stringify(req.body))
  const order = await paypal.newOrder(req.body);
  res.json(order);
});

app.post("/api/orders/:orderId/capture", async (req, res) => {
  const { orderId } = req.params;
  const captureData = await paypal.capturePayment(orderId);
  res.json(captureData);
});

app.get("/api/token", async (req, res) => {
  const response = await fetch(base + "/v1/oauth2/token", {
    method: "post",
    body: "grant_type=client_credentials",
    headers: {
      Authorization:
        "Basic " + Buffer.from(CLIENT_ID + ":" + APP_SECRET).toString("base64"),
    },
  });
  const data = await response.json();
  res.json(data);  
  

});



app.listen(3000);
console.log('listening')