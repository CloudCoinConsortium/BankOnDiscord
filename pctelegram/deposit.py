from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import requests
from constants import pcbaseUrl,prefix_telegram
from lib import getWalletName
import os
import time
# shows total coins in the user balance

def deposit_command(update: Update, context: CallbackContext) -> None:
    wallet = getWalletName(update)
    wallet = wallet.replace("#","%23")
    print(wallet)
    # make Check wallet api call
    checkWalletUrl = pcbaseUrl + 'wallets/' + wallet
    response = requests.get(checkWalletUrl)
    responsejson = response.json()
    code = context.args[0]
    print(responsejson)
    # in case of success show the balance else display 0
    walletJson = { 'name': wallet}

    if(responsejson['status'] == 'error' and responsejson['payload']['message']  == 'Wallet not found'):
        createWalletUrl = pcbaseUrl + 'wallets'
        createresponse = requests.post(createWalletUrl, json= walletJson)
        createresponsejson = createresponse.json()
        print(createresponsejson)
        print(f"New Wallet created ")
        update.message.reply_text("Deposit: " + str(0))

    fullUrl = pcbaseUrl + 'locker/' + code
    print(fullUrl)
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
            update.message.reply_text(f"Could not remove coins from locker {code}")
        if(unlockstatus == 'completed' and actionstatus == 'success'):
            update.message.reply_text(f"Coins removed from locker {code}")
            update.message.reply_text(f"Type /balance to know your balance.")
    else:
        update.message.reply_text(f"Can not remove coins from locker {code}")
    
