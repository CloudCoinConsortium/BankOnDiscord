import hikari
import requests
from constants import pcbaseUrl, pay_url
# shows total coins in the user balance

async def Buy(wallet, event: hikari.DMMessageCreateEvent):
    wallet = wallet.replace("#","%23")

    await event.message.respond("Please make a payment to :\n" + pay_url)

    
