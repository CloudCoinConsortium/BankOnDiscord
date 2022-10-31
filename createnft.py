import hikari
import requests
from datetime import datetime
from constants import baseUrl
import os
import json
import time
# Create NFT with the supplied png file from the coins in the user's wallet
async def CreateNFT(wallet, event: hikari.DMMessageCreateEvent, title: str, desc: str):
    createNFTUrl = baseUrl + 'nfts/export'
    nftWalletName = 'NFTs.' + wallet
    nftWalletNameget = 'NFTs.' + wallet.replace("#","%23")
    
    nftSyncUrl = baseUrl + 'nftsync?nft_name=' + nftWalletNameget
    nftpath = os.path.join(os.getcwd(), 'nft')
    exportpath = os.path.join(nftpath, 'export')
    importpath = os.path.join(nftpath, 'import')
    foldername = os.path.join(exportpath, str(wallet))
    importfoldername = os.path.join(importpath, str(wallet))
    # check if import and export folder exists and if not create them 
    if(not os.path.exists(foldername)):
        os.mkdir(foldername)
    if(not os.path.exists(importfoldername)):
        os.mkdir(importfoldername)

    # check for attachments    
    if (len(event.message.attachments) == 0):
        await event.message.respond('Please attach a .PNG file')
        return
    for coin in event.message.attachments:
        fdata = await coin.read()
        filename = os.path.join(importfoldername,coin.filename)
        await event.message.respond('Processing file: ' + coin.filename)
        # copy coins to the import folders one by one
        with open(filename, "wb") as binary_file:
            binary_file.write(fdata)
        nftJson = { 'name': wallet, 'amount' :1 , 'template_path': filename, 'nft_name': nftWalletName, 'domain_name': 'raidacloud.com', 'text': title, 'x': 100, "y": 100, 'font_size': 24, 'host_name' : title, 'description': desc}
        nftSyncJson = {'domain_name': 'raidacloud.com', 'host_name' : title, 'create_txt': True, 'nft_name': nftWalletName }

        json_string = json.dumps(nftJson) 
        moveresponse = requests.post(createNFTUrl, json_string)
        moveresponsejson = moveresponse.json()
        print(moveresponsejson)
        depositstatus = moveresponsejson['payload']['status']
        TASK_URL = baseUrl + 'tasks/' + moveresponsejson['payload']['id']
        # poll for task status till status is changed to completed

        while depositstatus == 'running':
            taskresponse = requests.get(TASK_URL)
            taskresponsejson = taskresponse.json()
            print(taskresponsejson)
            depositstatus = taskresponsejson['payload']['status']
            time.sleep(2)
            # in case task was unsuccessful, send appropriate response the user
            if(depositstatus == 'error'):
                await event.message.respond(taskresponsejson['payload']['data']['message'])
                return
            if(depositstatus == 'completed'):
                json_string = json.dumps(nftSyncJson) 
                print(json_string)
                # sync the created NFT's DNS records
                syncresponse = requests.post(nftSyncUrl, json_string)
                syncresponsejson = syncresponse.json()
                print(syncresponsejson)
                if(syncresponsejson['status'] == 'success'):
                    await event.message.respond('NFT for ' + coin.filename + ' synced successfully')
                # delete the files from import folder
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
