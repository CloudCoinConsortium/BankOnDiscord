from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import requests
from constants import pcbaseUrl,prefix_telegram
from lib import getWalletName
import os
import time
from gen_locker import generate_alphanumeric_code

# shows total coins in the user balance

def withdraw_command(update: Update, context: CallbackContext) -> None:
    wallet = getWalletName(update)
    wallet = wallet.replace("#","%23")
    print(wallet)
    # make Check wallet api call
    checkWalletUrl = pcbaseUrl + 'wallets/' + wallet
    response = requests.get(checkWalletUrl)
    responsejson = response.json()
    amount = context.args[0]
    print(responsejson)
    # in case of success show the balance else display 0
    walletJson = { 'name': wallet}
    code = generate_alphanumeric_code()
            
    if(responsejson['status'] == 'error' and responsejson['payload']['message']  == 'Wallet not found'):
        createWalletUrl = pcbaseUrl + 'wallets'
        createresponse = requests.post(createWalletUrl, json= walletJson)
        createresponsejson = createresponse.json()
        print(createresponsejson)
        print(f"New Wallet created ")
        update.message.reply_text("Deposit: " + str(0))

    walletJson = { 'name': wallet, 'amount': float(amount),'transmit_code': code}
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
            update.message.reply_text(f"Could not lock coins from locker {code}. {message}")
        if(lockstatus == 'completed' and actionstatus == 'success'):
            update.message.reply_text(f"Coins locked into locker {code}")
            update.message.reply_text(f"Type /balance to know your balance.")
    else:
        update.message.reply_text(f"Unable to lock coins into {code}")
