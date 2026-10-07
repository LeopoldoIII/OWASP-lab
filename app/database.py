import sqlite3
import os

DB_PATH = "owasp_lab.db"

def _connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes the database schema and seeds initial test data."""
    conn = _connect()
    cursor = conn.cursor()

    # Users Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT,
            role TEXT DEFAULT 'user'
        )
    """)

    # Private Notes Table (for IDOR tests)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            is_private INTEGER DEFAULT 1,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    # Seed initial test records
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO users (username, password, email, role) VALUES ('admin', 'AdminPass2026!', 'admin@lab.local', 'admin')")
        cursor.execute("INSERT INTO users (username, password, email, role) VALUES ('alice', 'AliceSecret123', 'alice@lab.local', 'user')")
        cursor.execute("INSERT INTO users (username, password, email, role) VALUES ('bob', 'BobPassword456', 'bob@lab.local', 'user')")

        # Insert private notes (IDOR demo)
        cursor.execute("INSERT INTO notes (user_id, title, content) VALUES (1, 'Admin Secret Note', 'Server Master Secret Key is SUP3R_S3CR3T_K3Y_2026')")
        cursor.execute("INSERT INTO notes (user_id, title, content) VALUES (2, 'Alice Personal Notes', 'Grocery list: Milk, Bread, Cryptography research')")
        cursor.execute("INSERT INTO notes (user_id, title, content) VALUES (3, 'Bob Secret Project', 'Security strategy planning meeting on Friday')")

    conn.commit()
    conn.close()

def get_raw_db_connection():
    """Raw SQLite connection for unparameterized query vulnerability demonstrations."""
    conn = _connect()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT 1 FROM users LIMIT 1")
    except sqlite3.OperationalError:
        conn.close()
        init_db()
        conn = _connect()
    return conn

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")
