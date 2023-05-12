
from constants import prefix_telegram
from telegram import Update

def getWalletName(update: Update) -> None:
    user = update.effective_user
    if user:
        name = user.first_name
        if user.username:
            name = user.username
    wallet = prefix_telegram + name
    return wallet
