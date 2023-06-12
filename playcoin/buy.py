import hikari
import requests
import json
from constants import pcbaseUrl, pay_url
# shows total coins in the user balance

async def Buy(wallet, event: hikari.DMMessageCreateEvent):
    wallet = wallet.replace("#","%23")

    url = "http://localhost:3000/api/order"

    payload = json.dumps([
  {
    "reference_id": "PUHF",
    "amount": {
      "currency_code": "USD",
      "value": "175.00",
      "breakdown": {
        "item_total": {
          "currency_code": "USD",
          "value": "175.00"
        },
        "shipping": {
          "currency_code": "USD",
          "value": "0.00"
        }
      }
    },
    "items": [
      {
        "name": "Enterprise Subscription",
        "description": "Enterprise Subscription: 1 year",
        "sku": "sku01",
        "unit_amount": {
          "currency_code": "USD",
          "value": "175.00"
        },
        "quantity": "1",
        "category": "DIGITAL_GOODS"
      }
    ]
  }
])
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    responseJson = response.json()
    print(response.text)
    print(json.dumps(response.json()))
    if responseJson['status'] == "CREATED":
        print('Order created:' + responseJson['id'])
        url = pay_url + '?orderID=' + responseJson['id']
        await event.message.respond("Please make a payment to :\n" + url)

    
