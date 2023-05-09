async def Help():
    balanceContent = await balanceHelp()
    transferContent = await transferHelp()
    mainContent = await MainHelp()
    lockContent = await lockHelp()
    depositContent = await depositHelp()
    myWalletContent = await MyWalletHelp()
    return mainContent  + balanceContent + lockContent + depositContent + transferContent + myWalletContent

async def MainHelp():
    return '**✳️ WELCOME TO PLAYCOIN BOT ✳️**\nThis bot allows you to Remove or put your Playcoins in a locker. This software is provided free of charge with all bugs, defects and vulnerabilities. \n\n**BASIC COMMANDS**'

async def depositHelp():
    return '\n\n**🧾 DEPOSIT**\n`/deposit <code>`\nSends a code that is then turned into a group of coins. Returns a status.Sample: \n/deposit YA7-BU9E'

async def transferHelp():
    return "\n\n** ⮂ TRANSFER ** \n Moves coins from your account to another Discord users account.\nExample:\n/transfer <amount> <discord user>\nsuch as:\n/transfer 10.33 JohnDoe#0982Note, the reciever will need to install the PCBOT before they can get their money. "

async def lockHelp():
    return '\n\n**🧾 WITHDRAW**\n`/withdraw <amount>`\nRemoves coins from your wallet and returns a code that you can give to your friends. Specify the amount of coins you want to withdraw in the command. Sample:\n/withdraw 99.0921'

async def balanceHelp():
    return '\n\n**🔎 BALANCE**\n`/bank balance` Returns the number of coins in  your Coin Bank.\nNo extra information is required.'

async def MyWalletHelp():
    return '\n\n** 🧾 MY WALLET **\n `/mywallet` shows the name of your wallet.'




