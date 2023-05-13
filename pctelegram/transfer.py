from unicodedata import numeric
import requests
from constants import pcbaseUrl
import json
import time
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from constants import pcbaseUrl,prefix_telegram
from lib import getWalletName

def transfer_command(update: Update, context: CallbackContext) -> None:
    wallet = getWalletName(update)
    wallet = wallet.replace("#","%23")
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


