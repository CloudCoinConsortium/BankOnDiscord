from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import requests
from constants import pcbaseUrl,prefix_telegram
from lib import getWalletName
# shows total coins in the user balance

def balance_command(update: Update, context: CallbackContext) -> None:
    wallet = getWalletName(update)
    wallet = wallet.replace("#","%23")
    print(wallet)
    # make Check wallet api call
    checkWalletUrl = pcbaseUrl + 'wallets/' + wallet
    response = requests.get(checkWalletUrl)
    responsejson = response.json()
    # in case of success show the balance else display 0
    if(responsejson['status'] == 'success'):
        update.message.reply_text("Balance: " + str(responsejson['payload']['balance']))
    else:
        update.message.reply_text("Balance: " + str(0))
    
