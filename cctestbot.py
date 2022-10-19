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

#https://patchwork.systems/programming/hikari-discord-bot/introduction-and-basic-bot.html

bot = hikari.GatewayBot(token = os.environ['CCBOT_TOKEN'])

@bot.listen(hikari.GuildMessageCreateEvent)
async def print_message(event):
    print(event.content)

@bot.listen(hikari.DMMessageCreateEvent)
async def ping(event: hikari.DMMessageCreateEvent) -> None:
    # If a non-bot user sends a message "hk.ping", respond with "Pong!"
    # We check there is actually content first, if no message content exists,
    # we would get `None' here.

    if not event.content:
        return
    walletName = str(event.author)
    
    mainphrases = ['/bank', '/help','/nft']
    nftphrases = ['create', 'show','help', 'withdraw']
    command = event.content.split()

    mainphrase = command[0].lower()

    
    if(command[0].upper() == '/NFT'):
        if(len(command) > 1):
            phrase = command[1]
            if(not phrase in nftphrases):
                await event.message.respond('Invalid Command')
                helpContent = await NFTHelp()
                await event.message.respond(helpContent)

            if(phrase=='create'):
                if(len(command) == 2):
                    await event.message.respond('You must provide a title for NFT')
                    return
                if(len(command) == 3):
                    await event.message.respond('You must provide a description for NFT')
                    return
                title = command[2]
                paramlength = len(command)
                desc = ''
                for i in range(3, paramlength):
                    desc = desc + ' ' + command[i]
                await CreateNFT(walletName, event= event, title= title, desc= desc)
            if(phrase=='show'):
                await ShowNFT(walletName,event=event)
            if(phrase=='help'):
                helpContent = await NFTHelp()
                await event.message.respond(helpContent)
            if(phrase == 'withdraw'):
                if(len(command) == 2):
                    await event.message.respond('You must provide a SN to withdraw NFT')
                    return
                sn = command[2]
                await WithdrawNFT(walletName, event= event, sn= sn)

    bankphrases = ['deposit', 'showcoins', 'balance','whatsmywallet','statement', 'deletewallet', 'withdraw', 'transfer', 'pay','help', 'move', 'bet']

    if(command[0] == '/bank'):
        if(len(command) > 1):
            phrase = command[1]
            if(not phrase in bankphrases):
                await event.message.respond('Invalid Command')
                helpContent = await Help()
                await event.message.respond(helpContent)
            if(phrase == 'deposit'):
                await Deposit(wallet= walletName, event=event)
            if(phrase == 'showcoins'):
                await ShowCoins(wallet= walletName, event=event)
            if(phrase == 'balance'):
                await ShowCoins(wallet= walletName, event=event)
            if(phrase == 'whatsmywallet'):
                await MyWallet(wallet= walletName, event=event)
            if(phrase == 'statement'):
                page = 1
                if(len(command) == 2):
                    page = "1"
                if(len(command) > 2):
                    page = command[2]
                await Statement(wallet= walletName, event=event, page= page)
            if(phrase == 'deletewallet'):
                await DeleteWallet(wallet= walletName, event=event)
            if(phrase == 'withdraw'):
                if(len(command) == 2):
                    await event.message.respond('You must provide an amount to withdraw Cloudcoins')
                    return
                amount = command[2]
                await Withdraw(wallet= walletName, event=event, amount= amount)
            if(phrase == 'transfer'):
                amount = command[2]
                skywallet = command[3]
                if(len(command) == 2):
                    await event.message.respond('You must provide a wallet name for transfer')
                    return
                await Transfer(wallet= walletName, event=event, amount= amount, skywallet= skywallet)
            if(phrase == 'pay'):
                amount = command[2]
                await Pay(wallet= walletName, event=event, amount=amount)
            if(phrase == 'bet'):
                if(len(command) == 2):
                    await event.message.respond('You must provide an amount')
                    return
                amount = command[2]
                
                description = 'Bet placed by ' + walletName + ' for ' + str(amount) + ' Cloudcoins'
                await Bet(wallet= walletName, event=event, towallet='Default', amount=amount, description= description)

            if(phrase == 'move'):
                towallet = command[2]
                amount = command[3]
                await Move(wallet=walletName, event=event, towallet= towallet, amount= amount)

    if(command[0] == '/help'):
        if(len(command) == 1):
            helpContent = await Help()
            await event.message.respond(helpContent)
        else:
            helpContent = await ChooseHelp(command[1])
            await event.message.respond(helpContent)

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