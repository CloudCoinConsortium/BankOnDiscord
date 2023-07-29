import mysql.connector
from datetime import datetime

def insert_order(orderId, qty, price, buyer, seller, status):
    try:
        # Connect to the MySQL database
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123456",
            database="ccmarketplace"
        )
        cursor = conn.cursor()

        # Create the "orders" table if it doesn't exist
        create_table_query = """
            CREATE TABLE IF NOT EXISTS orders (
                id INT AUTO_INCREMENT PRIMARY KEY,
                orderid VARCHAR(255),
                qty FLOAT,
                price FLOAT,
                buyer VARCHAR(255),
                seller VARCHAR(255),
                datetime TIMESTAMP,
                status VARCHAR(255)
            )
        """
        cursor.execute(create_table_query)

        # Get the current datetime
        datetime_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Insert a new row into the "orders" table
        insert_query = """
            INSERT INTO orders (orderid,qty, price, buyer, seller, datetime, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        data = (orderId, float(qty), float(price), buyer, seller, datetime_now, status)
        cursor.execute(insert_query, data)

        # Commit the transaction
        conn.commit()

        # Retrieve the last inserted id
        last_inserted_id = cursor.lastrowid

        # Close the connection
        conn.close()

        return last_inserted_id

    except mysql.connector.Error as e:
        print("Error during insertion:", e)
        return None
