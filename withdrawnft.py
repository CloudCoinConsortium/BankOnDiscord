from tokenize import Number
import hikari
import requests
from datetime import datetime
from constants import baseUrl
from table2ascii import table2ascii as t2a, PresetStyle
import base64
import json
import time
import os

async def WithdrawNFT(wallet, event: hikari.DMMessageCreateEvent, sn: Number):
    withdrawNFTUrl = baseUrl + 'nfts/' + sn + '/png'
    exportnftUrl = baseUrl + 'exportsns'
    nftWalletName = 'NFTs.' + wallet

    fullpath = os.path.join(os.getcwd(), 'nft')
    exportpath = os.path.join(fullpath, 'export')
    foldername = os.path.join(exportpath, str(wallet))
    print(foldername)
    if(not os.path.exists(foldername)):
        os.mkdir(foldername)

    print(withdrawNFTUrl)
    print(exportnftUrl)
    #nftresponse  = requests.get(withdrawNFTUrl)

    # nftresponsejson =nftresponse.json()
    # exportresponse = requests.post(exportnftUrl)
    exportJson = {'name': nftWalletName , 'type': 'png' , 'folder' : foldername, 'tag': '', 'sns': [int(sn)]}
    json_string = json.dumps(exportJson) 
    print(json_string)
    exportresponse = requests.post(exportnftUrl, json_string)
    exportresponsejson = exportresponse.json()
    print(exportresponsejson)
    depositstatus = exportresponsejson['payload']['status']
    TASK_URL = baseUrl + 'tasks/' + exportresponsejson['payload']['id']
    while depositstatus == 'running':
        taskresponse = requests.get(TASK_URL)
        taskresponsejson = taskresponse.json()
        depositstatus = taskresponsejson['payload']['status']
        if(depositstatus == 'error'):
            await event.message.respond("Move failed: " + taskresponsejson['payload']['data']['message'])

        time.sleep(1)
        if(depositstatus == 'completed'):
            if(taskresponsejson['status'] == 'success'):
                print(str(taskresponsejson['payload']['data']))
                for filename in os.listdir(foldername):
                    f = os.path.join(foldername, filename)
                    if os.path.isfile(f):
                        with open(f, "rb") as fh:
                            fh = hikari.File(f)
                            await event.message.respond(fh)
                for filename in os.listdir(foldername):
                    f = os.path.join(foldername, filename)
                    os.remove(f)
                await event.message.respond("NFT withdrawn completed: ")


                # await event.message.respond("Export completed: " + str(taskresponsejson['payload']['data']['amount']) + ' coins moved to ' + target)



            

