import hikari
import requests
from constants import baseUrl
# shows total coins in the user balance
async def ShowCoins(wallet, event: hikari.DMMessageCreateEvent):
    wallet = wallet.replace("#","%23")
    # make Check wallet api call
    checkWalletUrl = baseUrl + 'wallets/' + wallet
    response = requests.get(checkWalletUrl)
    responsejson = response.json()
    # in case of success show the balance else display 0
    if(responsejson['status'] == 'success'):
        await event.message.respond("Balance: " + str(responsejson['payload']['balance']))
    else:
        await event.message.respond("Balance: " + str(0))

    embed = hikari.Embed()
    embed.title = "Wallet Name: " + str(wallet)

    embed.description = "Wallet Balance: 0"
    ch = event.message.fetch_channel
    hikari.File('')
    
