import mysql.connector
from mysql.connector import Error
import hikari
import os
from dotenv import load_dotenv
from constants import pcbaseUrl, pay_url
from playcoin.orders import insert_order
from playcoin.dbpool import connection_pool

load_dotenv()  # take environment variables from .env.

async def SaveKeys(wallet, event: hikari.DMMessageCreateEvent, cid, key):
    
        conn = connection_pool.get_connection() # Get a connection from the pool
        cursor = conn.cursor()
            
            # Added ON DUPLICATE KEY UPDATE clause to update row if uid already exists
        query = """
            INSERT INTO ppkeys (uid, cid, secret) 
            VALUES (%s, %s, %s) 
            ON DUPLICATE KEY UPDATE 
            cid = VALUES(cid), 
            secret = VALUES(secret)
            """
        record = (wallet, cid, key)
            
        cursor.execute(query, record)
        conn.commit()
            
        print("Record inserted or updated successfully in ppkeys table")

        await event.message.respond("Keys Saved.")
