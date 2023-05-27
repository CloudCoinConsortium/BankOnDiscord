import aiosqlite
import hikari

# Establish a connection to the SQLite database
# If the database does not exist, it will be created

async def SetupPayInfo(wallet, event: hikari.DMMessageCreateEvent, userId: str, paypalId: str):
    async with aiosqlite.connect('payinfo.db') as db:
        # Create a cursor
        cursor = await db.cursor()

        # Create table - payment_info
        await cursor.execute('''
            CREATE TABLE IF NOT EXISTS payment_info
            (id INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT, user_id INTEGER UNIQUE)
            ''')

        # Insert a row of data, or replace existing row if a conflict occurs
        await cursor.execute("INSERT OR REPLACE INTO payment_info (email, user_id) VALUES (?, ?)", (paypalId, userId))

        # Commit the changes
        await db.commit()
        
        await event.message.respond('Payment info configured. Your paypal id is :' + paypalId) 
