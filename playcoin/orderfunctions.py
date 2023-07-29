import sqlite3
from datetime import datetime

import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

load_dotenv()  # take environment variables from .env.

def get_keys_by_walletname(walletname):
    try:
        conn = mysql.connector.connect(
            host=os.getenv('HOST'), 
            user=os.getenv('USER'), 
            password=os.getenv('PASSWORD'), 
            database=os.getenv('DATABASE')
        )        
        if conn.is_connected():
            cursor = conn.cursor()
            query = "SELECT cid, secret FROM ppkeys WHERE uid = %s"
            print(query)
            print(walletname)
            cursor.execute(query, (walletname,))
            rows = cursor.fetchall()
            
            keys = []
            for row in rows:
                cid, key_value = row
                key = {'cid': cid, 'key': key_value}
                keys.append(key)
            print(keys)
            # Return the list of dictionaries (keys)
            return keys

    except Error as e:
        print("Error while connecting to MySQL", e)

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
            print("MySQL connection is closed")


def get_keys_by_walletname1(walletname):
    conn = sqlite3.connect('../ppkeys.db')
    cursor = conn.cursor()
    table_name = 'ppkeys'
    select_statement = f"SELECT cid, key FROM {table_name} WHERE uid = ?"
    cursor.execute(select_statement, (walletname,))
    rows = cursor.fetchall()
    conn.close()
    keys = []
    for row in rows:
        cid, key_value = row
        key = {'cid': cid, 'key': key_value}
        keys.append(key)

    # Return the list of dictionaries (keys)
    return keys


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
