import fetch from "node-fetch";
import "dotenv/config"; // loads env variables from .env file

const { CLIENT_ID, APP_SECRET } = process.env;
const base = "https://api-m.sandbox.paypal.com";

export async function newOrder(body, cid, key) {

  const accessToken = await generateUserAccessToken(cid, key);
  const url = `${base}/v2/checkout/orders`;
  console.log(body)
  console.log(accessToken)
  const response = await fetch(url, {
    method: "post",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${accessToken}`,
    },
    body: JSON.stringify({
      intent: "CAPTURE",
      purchase_units: body,
    }),
  });
  const data = await response.json();
  console.log(data);
  return data;
}

export async function getcapturePayment(orderId, keys) {
  const accessToken = await generateUserAccessToken(keys.cid, keys.secret);
  const url = `${base}/v2/checkout/orders/${orderId}/capture`;
  const response = await fetch(url, {
    method: "post",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${accessToken}`,
    },
  });
  const data = await response.json();
  //console.log(data);
  // The capture ID should be in the data object here.
  const captureId = data.purchase_units[0].payments.captures[0].id;
  return { orderId, captureId, accessToken };
}


export async function createOrder() {
  const accessToken = await generateAccessToken();
  const url = `${base}/v2/checkout/orders`;
  const response = await fetch(url, {
    method: "post",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${accessToken}`,
    },
    body: JSON.stringify({
      intent: "CAPTURE",
      purchase_units: [
        {
          amount: {
            currency_code: "USD",
            value: "1.50",
          },
        },
      ],
    }),
  });
  const data = await response.json();
  console.log('Data:',data);
  return data;
}

export async function refundPayment(captureId, accessToken) {
  //const accessToken = await generateAccessToken();
  console.log(accessToken)
  const url = `${base}/v2/payments/captures/${captureId}/refund`;
  const response = await fetch(url, {
    method: "post",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${accessToken}`,
    },
  });
  const data = await response.json();
  console.log('Refund Processed:',data);
  return data;
}


export async function capturePayment(orderId) {
  const accessToken = await generateAccessToken();
  const url = `${base}/v2/checkout/orders/${orderId}/capture`;
  const response = await fetch(url, {
    method: "post",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${accessToken}`,
    },
  });
  const data = await response.json();
  console.log("Capture result:", JSON.stringify(data));
  return data;
}

export async function generateAccessToken() {
  const response = await fetch(base + "/v1/oauth2/token", {
    method: "post",
    body: "grant_type=client_credentials",
    headers: {
      Authorization:
        "Basic " + Buffer.from(CLIENT_ID + ":" + APP_SECRET).toString("base64"),
    },
  });
  const data = await response.json();
  return data.access_token;
}

export async function generateUserAccessToken(cid, key) {
  const response = await fetch(base + "/v1/oauth2/token", {
    method: "post",
    body: "grant_type=client_credentials",
    headers: {
      Authorization:
        "Basic " + Buffer.from(cid + ":" + key).toString("base64"),
    },
  });
  const data = await response.json();
  return data.access_token;
}
