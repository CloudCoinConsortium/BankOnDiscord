import hikari
import requests
import time
from constants import pcbaseUrl
# shows the name of the users own wallet
async def Unlock(wallet,code, event: hikari.DMMessageCreateEvent):
    walletName = str(wallet)
    walletUrl = pcbaseUrl + 'wallets/' + walletName
    walletResponse = requests.get(walletUrl)
    wJson = walletResponse.json()
    if((wJson['status'] == "error") and (wJson["payload"]["message"] == "Wallet not found")):
        createWalletUrl = pcbaseUrl + 'wallets'
        walletJson = { 'name': wallet}
        createresponse = requests.post(createWalletUrl, json= walletJson)
        createresponsejson = createresponse.json()
        #await event.message.respond(f"New Wallet created ")

        
    fullUrl = pcbaseUrl + 'locker/' + code
    unlockresponse = requests.post(fullUrl, json= walletJson)
    unlockresponsejson = unlockresponse.json()
    print(unlockresponsejson)
    if (unlockresponsejson['status'] != 'error'):
        unlockstatus = unlockresponsejson['payload']['status']
        TASK_URL = pcbaseUrl + 'tasks/' + unlockresponsejson['payload']['id']
        print(TASK_URL)
        # poll for task status till status is changed to completed

        while unlockstatus == 'running':
            taskresponse = requests.get(TASK_URL)
            taskresponsejson = taskresponse.json()
            unlockstatus = taskresponsejson['payload']['status']
            actionstatus = taskresponsejson["status"]
            print(taskresponsejson)
            print(unlockstatus)
            time.sleep(2)
        if(unlockstatus == 'error'):
            await event.message.respond(f"Could not remove coins from locker {code}")
        if(unlockstatus == 'completed' and actionstatus == 'success'):
            await event.message.respond(f"Coins removed from locker {code}")
            await event.message.respond(f"Type /balance to know your balance.")
    else:
        await event.message.respond(f"Can not remove coins from locker {code}")
