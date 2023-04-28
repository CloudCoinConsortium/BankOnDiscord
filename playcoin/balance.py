import hikari
import requests
from constants import baseUrl
# shows the name of the users own wallet
async def Balance(wallet, event: hikari.DMMessageCreateEvent):
    walletName = str(wallet)
    await event.message.respond(f"Your PlayCoin Balance is {walletName}")
    
