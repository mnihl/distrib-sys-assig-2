import sqlite3

DB_NAME = 'transactions.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer TEXT,
            timestamp TEXT,
            status TEXT,
            vendor_id TEXT,
            amount REAL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            transaction_id INTEGER,
            timestamp TEXT,
            is_fraudulent BOOLEAN,
            confidence REAL,
            FOREIGN KEY (transaction_id) REFERENCES transactions(id)
        )
    ''')
    conn.commit()
    conn.close()

def get_connection():
    return sqlite3.connect(DB_NAME)
