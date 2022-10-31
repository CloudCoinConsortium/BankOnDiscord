import hikari
import requests
from constants import baseUrl
# shows the name of the users own wallet
async def MyWallet(wallet, event: hikari.DMMessageCreateEvent):
    await event.message.respond(str(wallet))
    
