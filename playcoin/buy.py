import hikari
import requests
import json
from constants import pcbaseUrl, pay_url
from playcoin.orders import insert_order
from playcoin.orderfunctions import get_keys_by_walletname, get_sales_config_by_wallet
from playcoin.lib import getSendWalletName

async def Buy(wallet, event: hikari.DMMessageCreateEvent, qty, price, seller):
    seller = getSendWalletName(seller)
    sales_config = get_sales_config_by_wallet(walletname=seller)
    if price < sales_config['rate']:
        await event.message.respond("Insufficient rate\n")
        return       
    if sales_config['amount'] < qty:
        await event.message.respond("Not enough coins for sale\n")
        return       

    keys = get_keys_by_walletname(walletname=seller)
    if(len(keys) == 0):
        await event.message.respond("This Wallet is not configured for sale. Please contact the seller\n")
        return       
    wallet = wallet.replace("#","%23")
    seller = getSendWalletName(seller)
    #print(seller)
    # make Check wallet api call
    checkWalletUrl = pcbaseUrl + 'wallets/' + seller.replace("#","%23")
    #print(checkWalletUrl)
    response = requests.get(checkWalletUrl)
    responsejson = response.json()
    balance = 0
    print(balance)
    # in case of success show the balance else display 0
    if(responsejson['status'] == 'success'):
        balance = int(responsejson['payload']['balance'])

    if(balance < qty):
        await event.message.respond("Can not buy.\n")
        #return
    key = ''
    cid =''
    for key in keys:
      cid = key['cid']
      key = key['key']
      #print(f"CID: {key['cid']}, Key: {key['key']}")
    url = "{}api/order/?cid={}&key={}".format(pay_url, cid, key)  
    #print(url)
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
    #print(payload)
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    responseJson = response.json()
    #print(response.text)
    #print(json.dumps(response.json()))
    if responseJson['status'] == "CREATED":
        orderId = responseJson['id']
        order_id  = insert_order(orderId=orderId, qty=qty, price=price,buyer= wallet.replace("%23","#"), seller=seller, status=1)
        if order_id is not None:
          print("Order insertion succeeded. ID:", order_id)
        else:
          print("Order insertion failed.")        
        print('Order created:' + responseJson['id'])
        url = pay_url + '?orderID=' + responseJson['id']
        await event.message.respond("Please make a payment to :\n" + url)

    
