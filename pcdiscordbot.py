import hikari
import os
from help import Help, ChooseHelp, NFTHelp
from showcoins import ShowCoins
from deposit import Deposit
from statement import Statement
from pay import Pay
from move import Move
from withdraw import Withdraw
from deletewallet import DeleteWallet
from mywallet import MyWallet
from transfer import Transfer
from createnft import CreateNFT
from shownfts import ShowNFT
from withdrawnft import WithdrawNFT
from bet import Bet
from playcoin.balance import Balance
from playcoin.unlock import Unlock
from playcoin.lock import Lock

#https://patchwork.systems/programming/hikari-discord-bot/introduction-and-basic-bot.html

bot = hikari.GatewayBot(token = '')

@bot.listen(hikari.GuildMessageCreateEvent)
async def print_message(event):
    print(event)
    print(event.content)

@bot.listen(hikari.DMMessageCreateEvent)
async def ping(event: hikari.DMMessageCreateEvent) -> None:
    # If a non-bot user sends a message "hk.ping", respond with "Pong!"
    # We check there is actually content first, if no message content exists,
    # we would get `None' here.
    # in case of empty content return from the routine
    if not event.content:
        return
    # Wallet name is user name
    walletName = str(event.author)
    # the array below contain allowed command phrases. if the command phrase is anything else the bot returns an error
    mainphrases = ['/bank', '/help','/nft']
    nftphrases = ['create', 'show','help', 'withdraw']
    command = event.content.split()

    mainphrase = command[0].lower()

    # check for main phrase to be NFT command if so process NFT commands

    bankphrases = ['deposit', 'showcoins', 'balance','whatsmywallet','statement', 'deletewallet', 'withdraw', 'transfer', 'pay','help', 'move', 'bet']
    # check for main phrase to be bank command if so process wallet commands
    if(command[0] == "/balance"):
        print("Checking balance")
        await Balance(wallet= walletName, event=event)
    if(command[0] == "/unlock"):
        await Unlock(wallet= walletName, code= command[1], event=event)
    if(command[0] == "/lock"):
        print("Removing coins")
        code = command[1]
        amount = command[2]
        await Lock(wallet= walletName,code=code, amount=amount, event=event)

    if(command[0] == '/help'):
        if(len(command) == 1):
            helpContent = await Help()
            await event.message.respond(helpContent)
        else:
            helpContent = await ChooseHelp(command[1])
            await event.message.respond(helpContent)
    # sample ping for bot health check
    if event.content.startswith("ping"):
        await event.message.respond(str(event.author) + "-Pong!")

@bot.listen(hikari.GuildMessageCreateEvent)
async def ping(event: hikari.GuildMessageCreateEvent) -> None:
    # If a non-bot user sends a message "hk.ping", respond with "Pong!"
    # We check there is actually content first, if no message content exists,
    # we would get `None' here.
    if event.is_bot or not event.content:
        return

    if event.content.startswith("ping"):
        await event.message.respond("Pong!")

bot.run()