async def Help():
    balanceContent = await balanceHelp()
    mainContent = await MainHelp()
    lockContent = await lockHelp()
    depositContent = await depositHelp()
    myWalletContent = await MyWalletHelp()
    return mainContent  + balanceContent + lockContent + depositContent + myWalletContent

async def MainHelp():
    return '**✳️ WELCOME TO PLAYCOIN BOT ✳️**\nThis bot allows you to Remove or put your Playcoins in a locker. This software is provided free of charge with all bugs, defects and vulnerabilities. \n\n**BASIC COMMANDS**'

async def depositHelp():
    return '\n\n**🧾 DEPOSIT**\n`/deposit <code>`\nSends a code that is then turned into a group of coins. Returns a status.Sample: \n/deposit YA7-BU9E'

async def lockHelp():
    return '\n\n**🧾 WITHDRAW**\n`/withdraw <amount>`\nRemoves coins from your wallet and returns a code that you can give to your friends. Specify the amount of coins you want to withdraw in the command. Sample:\n/withdraw 99.0921'

async def balanceHelp():
    return '\n\n**🔎 BALANCE**\n`/bank balance` Returns the number of coins in  your Coin Bank.\nNo extra information is required.'

async def MyWalletHelp():
    return '\n\n** 🧾 my wallet **\n `/mywallet` shows the name of your wallet.'




