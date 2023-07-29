import express from "express";
import * as paypal from "./paypal.js";
import fetch from "node-fetch";
import { config } from "dotenv";
import axios from "axios";
import { pool } from './db.js';

config(); // Loads .env file

const { CLIENT_ID, APP_SECRET, PCBASE_URL, base } = process.env;
const pcbaseUrl = PCBASE_URL || '';
const transferUrl = pcbaseUrl + 'transfer';

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
  console.log(cid)
  console.log(key)
  console.log('Body:',JSON.stringify(req.body))
  const order = await paypal.newOrder(req.body, cid, key);
  res.json(order);
});

async function getPPKeyByOrderId(orderId) {
    return new Promise((resolve, reject) => {
      const sql = `
        SELECT ppkeys.*
        FROM ppkeys
        INNER JOIN orders ON ppkeys.uid = orders.buyer
        WHERE orders.orderid = ?
      `;
    
      pool.query(sql, [orderId], function(error, results, fields) {
        if (error) reject(error);
        if (results.length > 0) {
            resolve(results[0]);
          } else {
            resolve({uid: '', cid: '', secret: ''});
          }
      });
    });
  }

app.post("/api/orders/:orderId/capture", async (req, res) => {
  const { orderId } = req.params;

  pool.query('SELECT * FROM orders WHERE orderid = ?', [orderId], async (err, oresult) => {
    if (err) {
      console.log('Error during selection:', err);
      res.status(500).send('An error occurred while fetching the order.');
      return;
    }
    
    if (oresult.length > 0) {
      const order = oresult[0];
      console.log(order);

      if(order && order.status === '1') {
        const sanitizedWallet = order.seller.replace('%23','#');
        const sanitizedWallet2 = order.buyer.replace('%23','#');
  
        const moveJson = {'srcname': sanitizedWallet , 'dstname': sanitizedWallet2 , 'amount' : parseInt(order.qty), 'tag': ''};
        console.log(moveJson);
        const json_string = JSON.stringify(moveJson);
        const moveresponse = await axios.post(transferUrl, json_string);
        const moveresponsejson = moveresponse.data;
        let depositstatus = moveresponsejson.payload.status;
      
        const TASK_URL = pcbaseUrl + 'tasks/' + moveresponsejson.payload.id;
        let taskresponsejson ='';
        while (depositstatus === 'running') {
          const taskresponse = await axios.get(TASK_URL);
          taskresponsejson = taskresponse.data;
          depositstatus = taskresponsejson.payload.status;
      
          if (depositstatus === 'error') {
            console.log('Transfer failed: ' + taskresponsejson.payload.data.message);
            const keys = await getPPKeyByOrderId(orderId)
            console.log('Got Keys: ',keys)
            const capture = await paypal.getcapturePayment(orderId, keys)
            paypal.refundPayment(capture.captureId, capture.accessToken)
          }
      
          await new Promise((resolve) => setTimeout(resolve, 1000));
        }
  
        if (depositstatus === 'completed' && taskresponsejson.status === 'success') {
            pool.query('UPDATE orders SET status = ? WHERE orderid = ?', [2, orderId], function (error, result) {
              if (error) {
                console.error('Error updating orders:', error);
                return;
              }
              
              if (result.affectedRows === 0) {
                console.log('Could not change status');
              } else {
                console.log(`Order ${orderId} status updated to completed.`);
              }
          
              // Updating the amount in the sales_config table
              pool.query('UPDATE sales_config SET amount = amount - ? WHERE uid = ?', [order.qty, sanitizedWallet], function(error, result) {
                if (error) {
                  console.error('Error updating sales_config:', error);
                  return;
                }
          
                if (result.affectedRows === 0) {
                  console.log('Could not update amount in sales_config');
                } else {
                  console.log(`Amount updated in sales_config for wallet ${wallet}.`);
                }
              });
          
              console.log('Transfer completed: ' + taskresponsejson.payload.data.amount + ' coins moved to ');
            });
          }
          
          
        res.json(order);
  
      } else if (order && order.status === '2') {
        res.status(400).send({'msg':'Order already processed'});
      } else {
        res.status(404).send({'msg':'Order not found'});
      }
    } else {
      res.status(404).send('Order not found.');
    }
  });
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

app.listen(3456);
console.log('listening')