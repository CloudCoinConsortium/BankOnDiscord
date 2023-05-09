from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from pchelp import Help
import os
from dotenv import load_dotenv

load_dotenv()
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(Help())

def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(Help())

def main() -> None:
    # Replace 'TOKEN' with your Bot's API token
    print(os.getenv('TELEGRAM_TOKEN_PCBOT'))
    updater = Updater(os.getenv('TELEGRAM_TOKEN_PCBOT'), use_context=True)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
