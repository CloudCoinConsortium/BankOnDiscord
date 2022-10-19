from ast import While
from urllib import response
import hikari
import requests
from constants import baseUrl
import os
import json
import time
from showcoins import ShowCoins
async def Deposit(wallet, event: hikari.DMMessageCreateEvent):
    nftWalletName =  "NFTs." + wallet
    walletget = wallet.replace("#","%23")
    checkWalletUrl = baseUrl + 'wallets/' + walletget + '?contents=false'
    response = requests.get(checkWalletUrl)
    responsejson = response.json()
    fullpath = os.path.join(os.getcwd(), 'import')
    if(responsejson['status'] != 'success'):
        print('Wallet does not exist.Creating new one')
        createWalletUrl = baseUrl + 'wallets'
        walletJson = { 'name': wallet}
        nftwalletJson = {'name': nftWalletName}
        createresponse = requests.post(createWalletUrl, json= walletJson)
        createresponsejson = createresponse.json()
        nftcreateresponse = requests.post(createWalletUrl, json= nftwalletJson)
        nftcreateresponsejson = nftcreateresponse.json()
        
        if(createresponsejson['status'] == 'success'):
            print('Wallet Created successfully')
            await event.message.respond("New Wallet created for you. your wallet name is:" + wallet)
    print('Depositing', len(event.message.attachments), ' files')
    await event.message.respond('Starting Coins deposit...')
    if (len(event.message.attachments) == 0):
        await event.message.respond('No Coins found')
    else:
        for coin in event.message.attachments:
            try:
                fdata = await coin.read()
                filename = os.path.join(fullpath, coin.filename)
                await event.message.respond('Processing file: ' + coin.filename)
                with open(filename, "wb") as binary_file:
                    binary_file.write(fdata)
                depositUrl = baseUrl + 'import'
                depositJson = {"name": wallet, "items":[{"type":"file", "data":filename}]}
                json_string = json.dumps(depositJson) 
                depositresponse = requests.post(depositUrl, json_string)
                depositresponsejson = depositresponse.json()
                depositstatus = depositresponsejson['payload']['status']
                TASK_URL = baseUrl + 'tasks/' + depositresponsejson['payload']['id']
                while depositstatus == 'running':
                    taskresponse = requests.get(TASK_URL)
                    taskresponsejson = taskresponse.json()
                    depositstatus = taskresponsejson['payload']['status']
                    time.sleep(2)
                if(depositstatus == 'completed'):
                    authentic = taskresponsejson['payload']['data']['pown_results']['authentic']
                    counterfeit = taskresponsejson['payload']['data']['pown_results']['counterfeit']
                    total = taskresponsejson['payload']['data']['pown_results']['total']
                    unknown = taskresponsejson['payload']['data']['pown_results']['unknown']
                    await event.message.respond('Coins imported..\nTotal: ' + str(total) + '\nAuthentic: '+ str(authentic) + '\nCounterfeit:' + str(counterfeit) + '\nUnknown: ' + str(unknown))
            except:
                await event.message.respond('An Error occured while depositting '+ coin.filename + '. Please check your file or try again')
            await ShowCoins(wallet, event)

    return ''
