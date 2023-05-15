from constants import prefix_telegram
from telegram import Update

def getSendWalletName(input_str):
    parts = input_str.split("@")
    if len(parts) != 2:
        raise print("Invalid input format. Expected: 'user@network'")

    user = parts[0]
    network = parts[1]

    if network == "telegram":
        prefix = "tg_"
    elif network == "discord":
        prefix = "dsc_"
    elif network == "whatsapp":
        prefix = "wht_"
    elif network == "skype":
        prefix = "sky_"
    else:
        raise print("Invalid network specified in the input")

    return prefix + user


def getWalletName(update: Update) -> None:
    user = update.effective_user
    if user:
        name = user.first_name
        if user.username:
            name = user.username
    wallet = prefix_telegram + name
    return wallet
