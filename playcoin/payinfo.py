import hikari
from playcoin.dbpool import connection_pool

async def SetupPayInfo(wallet, event: hikari.DMMessageCreateEvent, rate: str, amount: str): 
    conn = connection_pool.get_connection() # Get a connection from the pool
    cursor = conn.cursor()

    # Corrected the field names and types in the INSERT INTO statement and ON DUPLICATE KEY UPDATE clause
    query = """
        INSERT INTO sales_config (uid, rate, amount) 
        VALUES (%s, %s, %s) 
        ON DUPLICATE KEY UPDATE 
        rate = VALUES(rate), 
        amount = VALUES(amount)
        """
    record = (wallet, float(rate), float(amount))

    cursor.execute(query, record)
    conn.commit()

    print("Record inserted or updated successfully in pay info table")
   
    await event.message.respond('Payment info configured.')
