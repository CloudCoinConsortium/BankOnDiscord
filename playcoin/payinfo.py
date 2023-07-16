import hikari

# Establish a connection to the SQLite database
# If the database does not exist, it will be created

async def SetupPayInfo(wallet, event: hikari.DMMessageCreateEvent, userId: str, paypalId: str):        
        await event.message.respond('Payment info configured. Your paypal id is :' + paypalId) 
