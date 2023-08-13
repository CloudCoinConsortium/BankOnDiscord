async def Help():
    depositContent = await DepositHelp()
    withdrawContent = await WithdrawHelp()
    mainContent = await MainHelp()
    moveContent = await moveHelp()
    payContent = await payHelp()
    balanceContent = await balanceHelp()
    statementContent = await statementHelp()
    deletewalletContent  = await deletewalletHelp()
    return mainContent + depositContent + withdrawContent + moveContent + payContent + balanceContent + statementContent + deletewalletContent

async def MainHelp():
     return '**✳️ WELCOME TO COIN BOT ✳️**\nThis bot allows you to deposit, withdraw, transfer, and pay out cloud currencies using folders on a shared server. This software is provided free of charge with all bugs, defects and vulnerabilities by the CloudCoin Consortium.\n\nThis bot stores your coins on a remote server where they can be accessed from any device using chat programs such as Discord or Telegram. It is important to understand that the remote server does not have data supremacy and coins can be lost and hacked. Please do not store large amounts of coins here.\n\n**BASIC COMMANDS**'

async def MainNFTHelp():
    return '**✳️ WELCOME TO CLOUDCOIN NFT VAULT ✳️**\nThis bot allows you to create, list and withdraw NFTs powered by CloudCoin. This software is provided free of charge with all bugs, defects and vulnerabilities included free from the CloudCoin Consoritum. \n\n**BASIC COMMANDS ➡️**'

async def statementHelp():
    return '\n\n**🧾 STATEMENT**\n`/statement <page>` Returns records of transactions as a set of 100 records.\ne.g. /statement 1 returns first page of your latest transaction records'

async def balanceHelp():
    return '\n\n**🔎 BALANCE**\n`/balance` Returns the number of coins in  your folder.'

async def deletewalletHelp():
    return '\n\n**🗑️ DELETE FOLDER **\n`/deletefolder` Deletes your folder if it\'s empty.\nPlease withdraw all your coins before issuing this command.'

async def payHelp():
     return "\n\n**❤️ PAY**\n`/pay <amount> <description>` Moves coins from your folder into the bot's folder and tells the bot about the payment.\nRequires the number of coins to give to the bot: `/pay 50` where 50 is the number of coins to give the bot. Unless you are specifically trying to pay the bot, use transfer instead."
    
async def moveHelp():
   return '\n\n**↔️ TRANSFER**\n`/transfer <amount> <username> <description>` Transfers coins from your folder to the folder of another person.\nRequires the number of coins to transfer, the name of the user that will receive them and an optional description. The description maybe required if the receiver needs to know who you are.  If you are sending coins to another chat program, like from Discord to Telegram, you will need to put an @telegram or @discord at the end of the username. : `/transfer 10 larryG#3345@discord For purchase 28837` where 10 is the number of coins to transfer and larryG#3345 is user to receive the coins. If there is no folder yet for the receiver, the receiver must include the bot and issue the command: new. A folder will be created for that person.'

async def WithdrawHelp():
    return '\n\n**📤 WITHDRAW CODE**\n`/withdraw <amount> <description>` Removes coins from your folder and puts them in a locker on the RAIDA. Returns the locker key that you can give to others.\nRequires the amount of coins to be removed: `/withdraw 33` where 33 is the number of coins to be removed. Description is optional'

async def WithdrawFileHelp():
    return '\n\n**📤 WITHDRAW FILE**\n`/withdrawfile <amount> <description>` Removes coins from your folder and returns them as a file. You can give this file to others.\nRequires the amount of coins to be removed: `/withdraw 33` where 33 is the number of coins to be removed. Description is optional'


async def DepositHelp():
    return '\n\n** 📥 DEPOSIT CODE**\n`/deposit <description>` Creates a folder if one does not exist. Takes the locker number you provided to the RAIDA and downloads any coins there to your folder.\n Includes the description (optional) in your statements.'

async def DepositFileHelp():
    return '\n\n** 📥 DEPOSIT FILE**\n`/depositfile <description>` Creates a folder if one does not exist. To upload coins to your folderk, first type /depositfile. Before you submit this command, click the “+” icon to the left of the text box and select a coin file to upload. Once your file is uploaded, submit the command. only files with .bin, .stack and .png are allowed. Description is optional.'

async def AddAPI():
     return '\n\n** 🔑 ADD SALES API**\n`/api <PayPal api key>` Allows you to upload an API Key for PayPal that allows a coin buyer to put dollars into your PayPal account. \n`api M7zJ4i4NVDNLid7drBGEFWxSb8MnVonawWuu5JGr6AHVJkK6-HF6aqx_K630tRCyF8G2dkjlz1-GKvyV`\nThis is required to sell your coins. Instructions for creating an API key are here: https://www.paypal.com/us/cshelp/article/how-do-i-create-rest-api-credentials-ts1949'
async def SellCoins():
     return '\n\n** 💸 SELL COINS**\n`/sell <amount> <price>` Marks the amount of coins you specified for sale at the price you specified. \n`/sell 25 .03` puts 25 coins up for sale at $.03 each.'

async def BuyCoins():
     return '\n\n** ❤️ BUY COINS**\n`/buy <amount> <price>` Attempts to buy the number of coins at the price you specified. Requires that there are enough coins for sale at that price.  \n`/buy 20 .03` will give you a link to purchase them with dollars. The link is only good for a few minutes. After you make the purchase, check your balance or statement to see if it worked.'

async def CoinExchanges():
     return '\n\n** 👀 SHOW EXCHANGES**\n`/exchanges` Shows the past exchanges and their prices and dates. Note, it is a common practice for sellers to create fake transactions that are at higher prices in order to fool buyers into paying too much thinking the price is higher than it is. Buyer beware.'

async def DeleteAIP():
    return '\n\n** 🗑🚫 DELETE API **\nDeletes your API Key.\n\tRequest:\n `/deleteapi`\nReturns success statement. Sales will become impossible.'


async def ShowCoinsHelp():
    return '\n\n** 👀 SHOWCOINS **\nShows the serial numbers of all the coins in your folder. Only used for NFTs.\n\tRequest:\n `/showcoins`\nReturns a list of serial numbers.'

async def NFTCreateHelp():
    return '\n\n** 🎨 CREATE**\n`/nft create title description\nThis bot allows you to create NFTs from your cloudcoins in CloudBank. You must have a non zero balance in your wallet to create an NFT. This will create a new NFT wallet for you on the server.\n\n '
    
async def NFTsHOWHelp():
    return '\n\n**👀 SHOW**\n`/nft show Lists all the NFTs created by you in tabular format\n\n '
    
async def NFTWithdrawHelp():
    return '\n\n**📤 WITHDRAW**\n`/nft withdraw withdraws an NFT and sends back the PNG by discord bot\n\n '

async def ChooseHelp(help):
    if(help == 'deletewallet'):
        content = await DeleteWalletHelp()
        return content
    if(help == 'showcoins'):
        content = await ShowCoinsHelp()
        return content
    if(help == 'deposit'):
        content = await DepositHelp()
        return content

async def NFTHelp():
        mainContent = await MainNFTHelp()
        nftCreateContent = await NFTCreateHelp()
        nftshowContent = await NFTsHOWHelp()
        nftWithdrawHelp = await NFTWithdrawHelp()
        return mainContent + nftCreateContent + nftshowContent + nftWithdrawHelp



