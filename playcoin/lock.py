import hikari
import requests
import time
from constants import pcbaseUrl
# shows the name of the users own wallet
async def Lock(wallet,code,amount, event: hikari.DMMessageCreateEvent):
    walletName = str(wallet)
    print(code)
    print(amount)
    walletJson = { 'name': walletName, 'amount': float(amount),'transmit_code': code}
    print(walletJson)
    fullUrl = pcbaseUrl + 'locker' 
    lockresponse = requests.post(fullUrl, json= walletJson)
    lockresponsejson = lockresponse.json()
    print(lockresponsejson)
    if (lockresponsejson['status'] != 'error'):
        lockstatus = lockresponsejson['payload']['status']
        TASK_URL = pcbaseUrl + 'tasks/' + lockresponsejson['payload']['id']
    # poll for task status till status is changed to completed

        while lockstatus == 'running':
            taskresponse = requests.get(TASK_URL)
            taskresponsejson = taskresponse.json()
            lockstatus = taskresponsejson['payload']['status']
            actionstatus = taskresponsejson["status"]
            print(taskresponsejson)
            print(lockstatus)
            time.sleep(2)
        if(lockstatus == 'error'):
            message = taskresponsejson['payload']['data']['message']
            await event.message.respond(f"Could not remove coins from locker {code}. {message}")
        if(lockstatus == 'completed' and actionstatus == 'success'):
            await event.message.respond(f"Coins removed from locker {code}")
            await event.message.respond(f"Type /balance to know your balance.")
    else:
        await event.message.respond(f"Unable to lock coins into {code}")
