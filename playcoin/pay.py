import hikari
from playcoin.move import Move
# make payment to Discord bot owner's wallet
async def Pay(wallet, event: hikari.DMMessageCreateEvent, amount):
    # call Move with default wallet. it can be replaced with any other wallet in which you want to recieve the cloudcoins
    await Move(wallet=wallet, event= event, towallet='Default', amount=amount)

