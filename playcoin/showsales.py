import hikari
import mysql.connector
from mysql.connector import Error
from table2ascii import table2ascii as t2a, PresetStyle
from dotenv import load_dotenv
import os

load_dotenv()  # take environment variables from .env.

async def ShowSales(event: hikari.DMMessageCreateEvent, page: str):
    RECORDS_PER_PAGE = 10  # number of records to display per page

    # Convert page to integer and calculate offset
    try:
        page_num = int(page)
    except ValueError:
        await event.message.respond("Invalid page number. Please enter a valid number.")
        return

    if page_num < 1:
        await event.message.respond("Page numbers start at 1.")
        return

    offset = (page_num - 1) * RECORDS_PER_PAGE

    # Prepare header and records list
    statementheader = ["S.No.", "Qty", "Price", "Buyer", "Seller", "Date"]
    records = []

    # Connect to database and fetch records
    try:
        conn = mysql.connector.connect(
            host=os.getenv('HOST'), 
            user=os.getenv('USER'), 
            password=os.getenv('PASSWORD'), 
            database=os.getenv('DATABASE')
        ) 
        if conn.is_connected():
            cursor = conn.cursor()
            query = "SELECT qty, price, buyer, seller, datetime FROM orders WHERE status=2 ORDER BY datetime DESC LIMIT %s OFFSET %s"
            cursor.execute(query, (RECORDS_PER_PAGE, offset))
            rows = cursor.fetchall()

            # Populate records list with fetched rows
            for index, row in enumerate(rows, start=1):
                records.append([index, *row])  # S.No. will be the index

    except Error as e:
        print("Error while connecting to MySQL", e)

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

    output = t2a(
    header=statementheader,
    body=records,
    style=PresetStyle.thin_compact)

    # Respond with ASCII table
    await event.message.respond(f"```\n{output}\n```")  # Wrap in code block to maintain format in Discord
