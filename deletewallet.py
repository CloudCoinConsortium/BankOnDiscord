import hikari
import requests
from constants import baseUrl
import json
# delete the users wallet if its empty
async def DeleteWallet(wallet, event: hikari.DMMessageCreateEvent):
    print('Deleting wallet', wallet)
    # encode # as special character to be used in url
    wallet = wallet.replace("#","%23")
    nftwallet = nftwallet.replace("#","%23")
    nftwallet = "NFTs." + wallet
    deleteUrl = baseUrl + 'wallets/' + str(wallet)
    nftdeleteUrl = baseUrl + 'wallets/' + str(nftwallet)

    response = requests.delete(deleteUrl)
    nftresponse = requests.delete(nftdeleteUrl)
    
    responsejson = response.json()
    nftresponsejson = nftresponse.json()
    
    print(responsejson)
    # check for delete response and send it to the user
    if(responsejson['status'] == 'success' and nftresponsejson['status'] == 'success'):
        await event.message.respond('Wallet deleted successfully')
    else:
        await event.message.respond('We could not delete your wallet. Please try again later!!')




