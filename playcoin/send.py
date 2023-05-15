from unicodedata import numeric
import hikari
import requests
from constants import pcbaseUrl
import json
import time
from playcoin.lib import getSendWalletName
# move cloudcoins to another wallet 

async def Send(wallet, event: hikari.DMMessageCreateEvent, towallet: str, amount):
    transferUrl = pcbaseUrl + 'transfer'
    towallet = getSendWalletName(towallet)
    print('moving from :'+ str(wallet) + ' to :', towallet, transferUrl )
    moveJson = {'srcname': wallet , 'dstname': towallet , 'amount' : float(amount), 'tag': ''}
    print(moveJson)
    json_string = json.dumps(moveJson) 
    moveresponse = requests.post(transferUrl, json_string)
    moveresponsejson = moveresponse.json()
    print(moveresponsejson)
    depositstatus = moveresponsejson['payload']['status']
    TASK_URL = pcbaseUrl + 'tasks/' + moveresponsejson['payload']['id']
    # poll for task status till status is changed to completed

    while depositstatus == 'running':
        taskresponse = requests.get(TASK_URL)
        taskresponsejson = taskresponse.json()
        depositstatus = taskresponsejson['payload']['status']
        # in case of error show appropriate message to user
        if(depositstatus == 'error'):
            await event.message.respond("Move failed: " + taskresponsejson['payload']['data']['message'])

        time.sleep(1)
        target = towallet
        if(towallet == 'Default'): target = 'Owner'
        # when completed show success response to the user

        if(depositstatus == 'completed'):
            if(taskresponsejson['status'] == 'success'):
                await event.message.respond("Move completed: " + str(amount) + ' coins moved to ' + towallet)


