from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from pchelp import Help
import os
from dotenv import load_dotenv
from constants import prefix_telegram
from balance import balance_command
from withdraw import withdraw_command
from deposit import deposit_command
load_dotenv()

def getWalletName(username: str) -> None:
    return prefix_telegram + username

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(Help())

def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(Help())
def mywallet_command(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    if user:
        name = user.first_name
        if user.username:
            name = user.username
        print(getWalletName(name))
        update.message.reply_text(f'Your wallet name is: {name}!')

def main() -> None:
    # Replace 'TOKEN' with your Bot's API token
    print(os.getenv('TELEGRAM_TOKEN_PCBOT'))
    updater = Updater(os.getenv('TELEGRAM_TOKEN_PCBOT'), use_context=True)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("mywallet", mywallet_command))
    dispatcher.add_handler(CommandHandler("balance", balance_command))
    dispatcher.add_handler(CommandHandler("deposit", deposit_command))
    dispatcher.add_handler(CommandHandler("withdraw", withdraw_command))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
