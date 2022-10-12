import hikari
import requests
from datetime import datetime
from constants import baseUrl
from table2ascii import table2ascii as t2a, PresetStyle
import base64

async def ShowNFT(wallet, event: hikari.DMMessageCreateEvent):
    showNFTUrl = baseUrl + 'nfts?nft_name=NFTs.' + wallet
    showresponse = requests.get(showNFTUrl)
    showresponsejson = showresponse.json()
    statementheader = ["S.No.", "SN" ,"Title","Description", ""]
    nfts = []
    sno = 1
    print(showresponsejson)
    if( showresponsejson['status'] != 'success'):
        await event.message.respond(showresponsejson['payload']['message'])
        return
    if(showresponsejson['payload'] is None):
        await event.message.respond('No NFTs found. Please use /nft create to create an NFT')
        return
    for trans in showresponsejson['payload']:
        nfts.append([sno,trans['sn'], trans['hostname'], trans['description'], ''])
        sno = sno + 1
    
    output = t2a(
    header=statementheader,
    body=nfts,
    style=PresetStyle.thin_compact)

    await event.message.respond(f"```\n{output}\n```")
    await event.message.respond('Enter /nft withdraw sn to withdraw NFT')



