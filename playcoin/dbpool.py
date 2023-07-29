# db_pool.py

import mysql.connector
from mysql.connector import pooling
import os
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

db_config = {
    "host": os.getenv('HOST'),
    "user": os.getenv('USER'),
    "password": os.getenv('PASSWORD'),
    "database": os.getenv('DATABASE')
}

# Create a connection pool with 10 connections
connection_pool = mysql.connector.pooling.MySQLConnectionPool(pool_name="mypool", pool_size=10, **db_config)
