from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import requests
from constants import pcbaseUrl
from lib import getWalletName, getSendWalletName
import time
import json
# shows total coins in the user balance

def send_command(update: Update, context: CallbackContext) -> None:
    wallet = getWalletName(update)
    amount = context.args[0]
    target = context.args[1]
    towallet = getSendWalletName(target)
    wallet = wallet.replace("#","%23")
    # towallet = towallet.replace("#","%23")
    
    print(wallet)
    print(towallet)
    # make Check wallet api call
    transferUrl = pcbaseUrl + 'transfer'
    towallet = context.args[1]
    amount = context.args[0]
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
            update.message.reply_text("Move failed: " + taskresponsejson['payload']['data']['message'])

        time.sleep(1)
        target = towallet
        if(towallet == 'Default'): target = 'Owner'
        # when completed show success response to the user

        if(depositstatus == 'completed'):
            if(taskresponsejson['status'] == 'success'):
                update.message.reply_text("Move completed: " + str(amount) + ' coins moved to ' + target)


