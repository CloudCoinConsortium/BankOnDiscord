from audioop import reverse
from tokenize import Number
import hikari
import requests
from datetime import datetime
from constants import baseUrl
from table2ascii import table2ascii as t2a, PresetStyle

async def Statement(wallet, event: hikari.DMMessageCreateEvent, page):
    wallet = wallet.replace("#","%23")
    statementUrl = baseUrl + 'wallets/' + wallet + '?contents=true' 
    response = requests.get(statementUrl)
    responsejson = response.json()
    statementheader = ["S.No." ,"Date","Type", "Description", "Amount", "Balance"]
    records = []
    if(responsejson['status'] == 'error'):
        if(responsejson['payload']['message'] == 'Wallet not found'):
            await event.message.respond('No statements')        
    sno = 1
    numrecs = len(responsejson['payload']['transactions'])
    arr = (responsejson['payload']['transactions'])
    reverserecs = arr[::-1]

    numpages = numrecs / 10
    remainder = numrecs % 10
    if(remainder > 0):
        numpages = numpages +1
        numpages = round(numpages)
    pagestart = (int(page) -1) * 10
    pageend = pagestart + 10
    sno = pagestart + 1
    for x in range(pagestart, pageend):
        if (x< len(reverserecs)):
            rec = reverserecs[x]
            date = rec['datetime'].split('T')
            records.append([sno, date[0],rec['type'], rec['message'], rec['amount'], rec['running_balance']])
            sno = sno + 1

    output = t2a(
    header=statementheader,
    body=records,
    style=PresetStyle.thin_compact)
    await event.message.respond(f"```\n{output}\n```")
    await event.message.respond('Page ' + str(page) + ' of ' + str(int(numpages)))



