import sqlite3
from datetime import datetime

import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os
from playcoin.dbpool import connection_pool

load_dotenv()  # take environment variables from .env.

def get_keys_by_walletname(walletname):
    conn = connection_pool.get_connection() # Get a connection from the pool
    cursor = conn.cursor()
    
    query = "SELECT cid, secret FROM ppkeys WHERE uid = %s"
    cursor.execute(query, (walletname,))
    rows = cursor.fetchall()

    keys = [{'cid': cid, 'key': key_value} for cid, key_value in rows]

    cursor.close()
    conn.close()  # Return the connection to the pool

    return keys

def get_sales_config_by_wallet(walletname):
    conn = connection_pool.get_connection() # Get a connection from the pool
    cursor = conn.cursor()

    query = "SELECT rate, amount FROM sales_config WHERE uid = %s"
    cursor.execute(query, (walletname,))
    row = cursor.fetchone()

    if row:
        rate, amount = row
        sales_config = {'rate': rate, 'amount': amount}
    else:
        sales_config = {'rate': 0, 'amount': 0}

    cursor.close()
    conn.close()  # Return the connection to the pool

    return sales_config

def get_sales_config_by_wallet1(walletname):
    conn = connection_pool.get_connection() # Get a connection from the pool
    cursor = conn.cursor()

    query = "SELECT rate, amount FROM sales_config WHERE uid = %s"
    cursor.execute(query, (walletname,))
    rows = cursor.fetchall()

    # Assuming that there is only one record for each uid
    # If there are multiple records, you can modify this to return a list of dictionaries
    config = [{'rate': rate, 'amount': amount} for rate, amount in rows]

    cursor.close()
    conn.close()  # Return the connection to the pool

    return config


def insert_order(orderId, qty, price, buyer, seller, status):
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect('../orders.db')
        cursor = conn.cursor()

        # Get the current datetime
        datetime_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Insert a new row into the "orders" table
        insert_query = """
            INSERT INTO orders (orderid,qty, price, buyer, seller, datetime, status)
            VALUES (?,?, ?, ?, ?, ?, ?)
        """
        data = (orderId, qty, price, buyer, seller, datetime_now, status)
        cursor.execute(insert_query, data)

        # Commit the transaction
        conn.commit()

        # Retrieve the last inserted id
        last_inserted_id = cursor.lastrowid

        # Close the connection
        conn.close()

        return last_inserted_id

    except sqlite3.Error as e:
        print("Error during insertion:", e)
        return None
