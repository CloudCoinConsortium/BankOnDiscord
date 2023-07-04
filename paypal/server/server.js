import express from "express";
import * as paypal from "./paypal.js";
import fetch from "node-fetch";
import "dotenv/config"; // loads env variables from .env file
import * as sqlite from 'sqlite';
import sqlite3 from 'sqlite3';
import { open } from 'sqlite';
import axios from "axios";
const { CLIENT_ID, APP_SECRET } = process.env;
const base = "https://api-m.sandbox.paypal.com";
const pcbaseUrl ='http://localhost:8004/api/v1/'
const transferUrl = pcbaseUrl + 'transfer'

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
      console.log(order)
      if(order.status === '1') {
        const sanitizedWallet = order.seller.replace('%23','#');
        const sanitizedWallet2 = order.buyer.replace( '%23','#');
  
    
        const moveJson = {'srcname': sanitizedWallet , 'dstname': sanitizedWallet2 , 'amount' : parseInt(order.qty), 'tag': ''}
        console.log(moveJson)
        const json_string = JSON.stringify(moveJson);
        const moveresponse = await axios.post(transferUrl, json_string);
        const moveresponsejson = moveresponse.data;
        let depositstatus = moveresponsejson.payload.status;
      
        const TASK_URL = pcbaseUrl + 'tasks/' + moveresponsejson.payload.id;
        let taskresponsejson =''
        while (depositstatus === 'running') {
          const taskresponse = await axios.get(TASK_URL);
           taskresponsejson = taskresponse.data;
          depositstatus = taskresponsejson.payload.status;
      
          // In case of error, show appropriate message to the user
          if (depositstatus === 'error') {
            console.log('Transfer failed: ' + taskresponsejson.payload.data.message);
          }
      
          await new Promise((resolve) => setTimeout(resolve, 1000));
        }
  
        if (depositstatus === 'completed') {
          if (taskresponsejson.status === 'success') {
            const result = await db.run(
              'UPDATE orders SET status = ? WHERE orderid = ?',
              2,
              orderId
            );
          
            if (result.changes === 0) {
              console.log('could not change status')
            } else {
              console.log(`Order ${orderId} status updated to completed.`);
            }
      
            console.log(
              'Transfer completed: ' +
                taskresponsejson.payload.data.amount +
                ' coins moved to ' 
            );
          }
        }
        res.json(order);
  
      } 
      if(order.status === '2') {
        res.status(400).send({'msg':'Order already processed'});
      }
    } else {
      res.status(404).send({'msg':'Order not found'});
    }
  } catch (err) {
    console.log(err)
    res.status(500).json({ error: err.message });
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