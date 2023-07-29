import hikari
from mysql.connector import Error
from table2ascii import table2ascii as t2a, PresetStyle
from playcoin.dbpool import connection_pool  # Import the connection pool

async def ShowSaleOrders(event: hikari.DMMessageCreateEvent, page: str):
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
    statementheader = ["S.No.", "SELLER", "Rate", "Amount", "Status", "Date"]
    records = []

    # Get a connection from the connection pool
    conn = connection_pool.get_connection()
    cursor = conn.cursor()

    try:
        query = "SELECT uid, rate, amount, status, saleorderdate FROM sales_order where status=1 ORDER BY saleorderdate DESC LIMIT %s OFFSET %s"
        cursor.execute(query, (RECORDS_PER_PAGE, offset))
        rows = cursor.fetchall()

        # Populate records list with fetched rows
        for index, row in enumerate(rows, start=1):
            records.append([index, *row])  # S.No. will be the index

    except Error as e:
        print("Error while querying MySQL", e)

    finally:
        cursor.close()
        conn.close()  # Return the connection to the pool

    output = t2a(
    header=statementheader,
    body=records,
    style=PresetStyle.thin_compact)

    # Respond with ASCII table
    await event.message.respond(f"```\n{output}\n```")  # Wrap in code block to maintain format in Discord
