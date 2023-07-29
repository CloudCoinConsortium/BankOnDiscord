#!/usr/bin/env python3

import hikari
import os
from playcoin.pchelp import Help
from showcoins import ShowCoins
from deposit import Deposit
from playcoin.statement import Statement
from playcoin.pay import Pay
from playcoin.move import Move
from playcoin.balance import Balance
from playcoin.unlock import Unlock
from playcoin.lock import Lock
from playcoin.send import Send
from playcoin.savesales import SaveSalesOrder
from gen_locker import generate_alphanumeric_code
from constants import prefix_discord, pay_url
from playcoin.buy import Buy
from playcoin.payinfo import SetupPayInfo
from playcoin.save_keys import SaveKeys
from playcoin.showsaleorders import ShowSaleOrders
from decimal import Decimal
from playcoin.showsales import ShowSales
#https://patchwork.systems/programming/hikari-discord-bot/introduction-and-basic-bot.html
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('PCBOT_TOKEN')
bot = hikari.GatewayBot(token = token)


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
    walletName = prefix_discord + str(event.author)
    #walletName = 'Zaxius#0286'
    # the array below contain allowed command phrases. if the command phrase is anything else the bot returns an error
    mainphrases = ['/mywallet', '/help','/balance', 'statement','/transfer','/deposit', '/withdraw', '/pay']
    command = event.content.split()

    mainphrase = command[0].lower()
    # check for main phrase to be NFT command if so process NFT commands

    bankphrases = ['deposit', 'showcoins', 'balance','whatsmywallet','statement', 'deletewallet', 'withdraw', 'transfer', 'pay','help', 'move', 'bet']
    # check for main phrase to be bank command if so process wallet commands

    if(command[0] == "/setup_paypal_keys"):
        cid = command[1]
        secret = command[2]
        await SaveKeys(wallet=walletName,event=event ,cid = cid, key= secret)

    if(command[0] == "/post_saleorder"):
        rate = command[1]
        amount = command[2]
        await SaveSalesOrder(wallet=str(event.author),event=event ,rate = rate, amount= amount)

    if(command[0] == "/show_sellorders"):
        await ShowSaleOrders(event=event , page = 1)


    if(command[0] == "/showsales"):
        print('Showing coins')
        if(len(command) ==2):
            page = command[1]
        else:
            page = 1
        await ShowSales(event=event, page=page)


    if(command[0] == "/buy"):
        print('Buying coins')
        rate = Decimal(command[1])
        qty = Decimal(command[2])
        seller = command[3]
        await Buy(wallet=walletName, event=event, qty= qty, price= rate, seller=seller)
        
    if(command[0] == "/setup_sales"):
        if(len(command) < 3):
            await event.message.respond('Insufficient parameters')
        else:
            rate = command[1]
            qty = command[2]
            await SetupPayInfo(wallet=walletName,event=event,rate=rate,amount= qty)

    if(command[0] == "/mywallet"):
        await event.message.respond(str(event.author))    
    if(command[0] == "/balance"):
        await Balance(wallet= walletName, event=event)
    if(command[0] == '/statement'):
        page = 1
        if(len(command) == 2):
            page = "1"
            if(len(command) > 2):
                page = command[2]
        await Statement(wallet= walletName, event=event, page= page)
    if(command[0] == '/send'):
        towallet = command[2]
        amount = command[1]
        if(len(command) == 2):
            await event.message.respond('You must provide a wallet name for transfer')
            return
        await Send(wallet=walletName, event=event, towallet= towallet, amount= amount)
    if(command[0] == '/transfer'):
        towallet = command[2]
        amount = command[1]
        if(len(command) == 2):
            await event.message.respond('You must provide a wallet name for transfer')
            return
        await Move(wallet=walletName, event=event, towallet= towallet, amount= amount)
    if(command[0] == '/pay'):
        amount = command[1]
        await Pay(wallet= walletName, event=event, amount=amount)

    if(command[0] == "/deposit"):
        if(len(command) < 2):
            await event.message.respond('Insufficient parameters.')    
        await Unlock(wallet= walletName, code= command[1], event=event)
    if(command[0] == "/withdraw"):
        if(len(command) < 2):
            await event.message.respond('Insufficient parameters.')    
        else:
            print("Removing coins")
            code = generate_alphanumeric_code()
            amount = command[1]
            await Lock(wallet= walletName,code=code, amount=amount, event=event)

    if(command[0] == '/help'):
        if(len(command) == 1):
            helpContent = await Help()
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