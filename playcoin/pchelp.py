async def Help():
    balanceContent = await balanceHelp()
    mainContent = await MainHelp()
    lockContent = await lockHelp()
    removeContent = await removeHelp()
    myWalletContent = await MyWalletHelp()
    return mainContent  + balanceContent + lockContent + removeContent + myWalletContent

async def MainHelp():
    return '**✳️ WELCOME TO PLAYCOIN BOT ✳️**\nThis bot allows you to Remove or put your Playcoins in a locker. This software is provided free of charge with all bugs, defects and vulnerabilities. \n\n**BASIC COMMANDS**'

async def removeHelp():
    return '\n\n**🧾 UNLOCK**\n`/unlock <locker-code>` removes the coins from the locker code and places them in your play coin wallet'

async def lockHelp():
    return '\n\n**🧾 LOCK**\n`/lock <locker-code> <amount>` Moves the play coins from your wallet into the locker code.\n.'

async def balanceHelp():
    return '\n\n**🔎 BALANCE**\n`/bank balance` Returns the number of coins in  your Coin Bank.\nNo extra information is required.'

async def MyWalletHelp():
    return '\n\n** 🧾 my wallet **\n `/mywallet` shows the name of your wallet.'




