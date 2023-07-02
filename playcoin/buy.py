import hikari
import requests
import json
from constants import pcbaseUrl, pay_url
from playcoin.orders import insert_order
from playcoin.orderfunctions import get_keys_by_walletname
# shows total coins in the user balance

async def Buy(wallet, event: hikari.DMMessageCreateEvent, qty, price, seller):
    wallet = wallet.replace("#","%23")
    keys = get_keys_by_walletname(walletname=wallet)
    print('printing keys')
    key = ''
    cid =''
    for key in keys:
      cid = key['cid']
      key = key['key']
      #print(f"CID: {key['cid']}, Key: {key['key']}")
    url = "http://localhost:3000/api/order/?cid={}&key={}".format(cid, key)  
    print(url)
    total_amount = str(qty * price)
    payload = json.dumps([
  {
    "reference_id": "PUHF",
    "amount": {
      "currency_code": "USD",
      "value": total_amount,
      "breakdown": {
        "item_total": {
          "currency_code": "USD",
          "value": total_amount
        },
        "shipping": {
          "currency_code": "USD",
          "value": "0.00"
        }
      }
    },
    "items": [
      {
        "name": "Playcoins",
        "description": "Playcoins",
        "sku": "sku01",
        "unit_amount": {
          "currency_code": "USD",
          "value": str(price)
        },
        "quantity": str(qty),
        "category": "DIGITAL_GOODS"
      }
    ]
  }
])
    print(payload)
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    responseJson = response.json()
    #print(response.text)
    #print(json.dumps(response.json()))
    if responseJson['status'] == "CREATED":
        orderId = responseJson['id']
        order_id  = insert_order(orderId=orderId, qty=qty, price=price,buyer= wallet, seller=seller, status=1)
        if order_id is not None:
          print("Order insertion succeeded. ID:", order_id)
        else:
          print("Order insertion failed.")        
        print('Order created:' + responseJson['id'])
        url = pay_url + '?orderID=' + responseJson['id']
        await event.message.respond("Please make a payment to :\n" + url)

    
