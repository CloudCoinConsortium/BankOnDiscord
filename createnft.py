import hikari
import requests
from datetime import datetime
from constants import baseUrl
import os
import json
import time

async def CreateNFT(wallet, event: hikari.DMMessageCreateEvent, title: str, desc: str):
    createNFTUrl = baseUrl + 'nfts/export'
    nftWalletName = 'NFTs.' + wallet
    nftSyncUrl = baseUrl + 'nftsync?nft_name=' + nftWalletName
    nftpath = os.path.join(os.getcwd(), 'nft')
    exportpath = os.path.join(nftpath, 'export')
    importpath = os.path.join(nftpath, 'import')
    foldername = os.path.join(exportpath, str(wallet))
    importfoldername = os.path.join(importpath, str(wallet))

    if(not os.path.exists(foldername)):
        os.mkdir(foldername)
    if(not os.path.exists(importfoldername)):
        os.mkdir(importfoldername)

    
    if (len(event.message.attachments) == 0):
        await event.message.respond('Please attach a .PNG file')
        return
    for coin in event.message.attachments:
        fdata = await coin.read()
        filename = os.path.join(importfoldername,coin.filename)
        await event.message.respond('Processing file: ' + coin.filename)
        with open(filename, "wb") as binary_file:
            binary_file.write(fdata)
        nftJson = { 'name': wallet, 'amount' :1 , 'template_path': filename, 'nft_name': nftWalletName, 'domain_name': 'raidacloud.com', 'text': title, 'x': 100, "y": 100, 'font_size': 24, 'host_name' : title, 'description': desc}
        nftSyncJson = {'domain_name': 'raidacloud.com', 'host_name' : title, 'create_txt': True, 'nft_name': nftWalletName }

        print(nftJson)
        json_string = json.dumps(nftJson) 
        moveresponse = requests.post(createNFTUrl, json_string)
        moveresponsejson = moveresponse.json()
        print(moveresponsejson)
        depositstatus = moveresponsejson['payload']['status']
        TASK_URL = baseUrl + 'tasks/' + moveresponsejson['payload']['id']
        while depositstatus == 'running':
            taskresponse = requests.get(TASK_URL)
            taskresponsejson = taskresponse.json()
            print(taskresponsejson)
            depositstatus = taskresponsejson['payload']['status']
            time.sleep(2)
            if(depositstatus == 'error'):
                await event.message.respond(taskresponsejson['payload']['data']['message'])
                return
            if(depositstatus == 'completed'):
                json_string = json.dumps(nftSyncJson) 
                print(json_string)
                syncresponse = requests.post(nftSyncUrl, json_string)
                syncresponsejson = syncresponse.json()
                print(syncresponsejson)
                if(syncresponsejson['status'] == 'success'):
                    await event.message.respond('NFT for ' + coin.filename + ' synced successfully')

                for filename in os.listdir(foldername):
                    f = os.path.join(foldername, filename)
                    if os.path.isfile(f):
                        with open(f, "rb") as fh:
                            fh = hikari.File(f)
                            await event.message.respond(fh)
            for filename in os.listdir(foldername):
                f = os.path.join(foldername, filename)
                os.remove(f)

        await event.message.respond('NFTs Created')
