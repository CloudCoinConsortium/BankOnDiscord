from datetime import datetime
import mysql.connector
from mysql.connector import Error
import hikari
import os
from dotenv import load_dotenv
from constants import pcbaseUrl, pay_url, prefix_discord
from playcoin.orders import insert_order
from playcoin.dbpool import connection_pool

load_dotenv()  # take environment variables from .env.

async def SaveSalesOrder(wallet, rate, amount, event: hikari.DMMessageCreateEvent):

    conn = connection_pool.get_connection() # Get a connection from the pool
    cursor = conn.cursor()

    # Check if a record exists with the given uid and status = 1
    query_check = "SELECT COUNT(*) FROM sales_order WHERE uid = %s AND status = 1"
    cursor.execute(query_check, (wallet + '@discord',))
    existing_count = cursor.fetchone()[0]

    # Get the current datetime
    saleorderdate = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if existing_count > 0:
        # Update the existing record
        query = """
            UPDATE sales_order 
            SET rate = %s, amount = %s, saleorderdate = %s 
            WHERE uid = %s AND status = 1
            """
        record = (rate, amount, saleorderdate, wallet + '@discord')
    else:
        # Insert a new record
        query = """
            INSERT INTO sales_order (uid, rate, amount, status, saleorderdate) 
            VALUES (%s, %s, %s, %s, %s)
            """
        record = (wallet + '@discord', rate, amount, 1, saleorderdate)

    cursor.execute(query, record)
    conn.commit()

    print("Record inserted or updated successfully in sales_order table")
    await event.message.respond("Sales Order Saved.")

    cursor.close()
    conn.close()  # Return the connection to the pool
