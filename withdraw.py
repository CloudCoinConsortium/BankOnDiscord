from fileinput import close
import hikari
import requests
from constants import baseUrl
import json
import os
import time
# withdraw coins from users wallet given an amount
async def Withdraw(wallet, event: hikari.DMMessageCreateEvent, amount):
    fullpath = os.path.join(os.getcwd(), 'export')
    foldername = os.path.join(fullpath, str(wallet))
    # check if export folder exists and if not create it
    if(not os.path.exists(foldername)):
        os.mkdir(foldername)
    withdrawUrl = baseUrl + 'export'
    moveJson = {'name': wallet , 'type': 'png' , 'amount' : int(amount), 'tag': '', 'folder': foldername}
    json_string = json.dumps(moveJson) 
    moveresponse = requests.post(withdrawUrl, json_string)
    moveresponsejson = moveresponse.json()
    depositstatus = moveresponsejson['payload']['status']
    TASK_URL = baseUrl + 'tasks/' + moveresponsejson['payload']['id']
    # poll for task status till status is changed to completed

    try:
        while depositstatus == 'running':
            taskresponse = requests.get(TASK_URL)
            taskresponsejson = taskresponse.json()
            depositstatus = taskresponsejson['payload']['status']
            time.sleep(2)
            # show appropriate response in case of error

            if(depositstatus == 'error'):
                    await event.message.respond(taskresponsejson['payload']['data']['message'])
            # if completed return the coins to user and delete the files

            if(depositstatus == 'completed'):
                for filename in os.listdir(foldername):
                    f = os.path.join(foldername, filename)
                    if os.path.isfile(f):
                        with open(f, "rb") as fh:
                            fh = hikari.File(f)
                            await event.message.respond(fh)
                for filename in os.listdir(foldername):
                    f = os.path.join(foldername, filename)
                    os.remove(f)
            

                await event.message.respond('Coins Withdrawn')
    except:
        await event.message.respond('An Error occured while depositting ')



