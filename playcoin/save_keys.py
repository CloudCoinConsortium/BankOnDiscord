import hikari
import requests
import json
from constants import pcbaseUrl, pay_url
from playcoin.orders import insert_order
import sqlite3

# shows total coins in the user balance

async def SaveKeys(wallet, event: hikari.DMMessageCreateEvent, cid, key):
    wallet = wallet.replace("#","%23")
    conn = sqlite3.connect('../ppkeys.db')
    cursor = conn.cursor()

    table_name = 'ppkeys'

    table_schema = '''
    CREATE TABLE IF NOT EXISTS ppkeys (
        walletname TEXT PRIMARY KEY,
        cid TEXT,
        key TEXT
    )
'''
    # Execute the table creation statement
    cursor.execute(table_schema)
    insert_statement = f"INSERT OR REPLACE INTO {table_name} (walletname, cid, key) VALUES (?, ?, ?)"
    cursor.execute(insert_statement, (wallet, cid, key))
    conn.commit()
    conn.close()
    await event.message.respond("Keys Saved.")


