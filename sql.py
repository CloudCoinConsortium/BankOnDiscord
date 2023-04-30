import sqlite3

def create_wallets_table():
    conn = sqlite3.connect('wallets.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS wallets (username TEXT PRIMARY KEY, discordwallet TEXT, telegramwallet TEXT)''')

    conn.commit()
    conn.close()

def save_wallet_data(username, wallet1name, wallet2name):
    conn = sqlite3.connect('wallets.db')
    c = conn.cursor()

    c.execute("INSERT OR REPLACE INTO wallets (username, wallet1name, wallet2name) VALUES (?, ?, ?)", (username, wallet1name, wallet2name))

    conn.commit()
    conn.close()

def create_otp_table():
    conn = sqlite3.connect('wallets.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS otp_data (user_name TEXT PRIMARY KEY,discord TEXT, otp TEXT)''')

    conn.commit()
    conn.close()

def save_otp_data(user_name, otp, discord):
    conn = sqlite3.connect('otp.db')
    c = conn.cursor()

    c.execute("INSERT OR REPLACE INTO otp_data (user_name,discord, otp) VALUES (?, ?)", (user_name,discord, otp))

    conn.commit()
    conn.close()
