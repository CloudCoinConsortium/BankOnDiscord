import express from "express";
import * as paypal from "./paypal.js";
import fetch from "node-fetch";
import "dotenv/config"; // loads env variables from .env file
import * as sqlite from 'sqlite';
import sqlite3 from 'sqlite3';
import { open } from 'sqlite';

const { CLIENT_ID, APP_SECRET } = process.env;
const base = "https://api-m.sandbox.paypal.com";
console.log(CLIENT_ID)

let db;

async function setupDatabase() {
  db = await open({
    filename: '../../orders.db',
    driver: sqlite3.Database,
  });
}

await setupDatabase()
const app = express();

app.use(express.urlencoded({ extended: true }));
app.use(express.static("public"));
app.use(express.json());
app.post("/api/orders", async (req, res) => {
  const order = await paypal.createOrder();
  res.json(order);
});

app.post("/api/order", async (req, res) => {
  const cid = req.query.cid;
  const key = req.query.key;

  console.log('Body:',JSON.stringify(req.body))
  const order = await paypal.newOrder(req.body, cid, key);
  res.json(order);
});

app.post("/api/orders/:orderId/capture", async (req, res) => {
  const { orderId } = req.params;
  //const captureData = await paypal.capturePayment(orderId);
  try {
    const order = await db.get('SELECT * FROM orders WHERE orderid = ?', orderId);

    if (order) {
      res.json(order);
    } else {
      res.status(404).send('Order not found');
    }
  } catch (err) {
    console.log(err)
    //res.status(500).json({ error: err.message });
  }

  console.log('order successful', orderId)
 // res.json({})
  //res.json(captureData);
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