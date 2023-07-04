import sqlite3
from datetime import datetime

def insert_order(orderId, qty, price, buyer, seller, status):
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect('orders.db')
        cursor = conn.cursor()

# Create the "orders" table if it doesn't exist
        create_table_query = """
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                orderid TEXT,
                qty REAL,
                price REAL,
                buyer TEXT,
                seller TEXT,
                datetime TEXT,
                status TEXT
            )
        """
        cursor.execute(create_table_query)
        # Get the current datetime
        datetime_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Insert a new row into the "orders" table
        insert_query = """
            INSERT INTO orders (orderid,qty, price, buyer, seller, datetime, status)
            VALUES (?,?, ?, ?, ?, ?, ?)
        """
        print(orderId)
        data = (orderId, float(qty), float(price), buyer, seller, datetime_now, '1')
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
