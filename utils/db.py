# utils/db.py
import sqlite3

def init_db(db_name="scraper_data.db"):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS news (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT,
                    description TEXT,
                    source TEXT,
                    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )''')
    conn.commit()
    conn.close()

def insert_news(title, description, source, db_name="scraper_data.db"):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute("INSERT INTO news (title, description, source) VALUES (?, ?, ?)", (title, description, source))
    conn.commit()
    conn.close()

def get_all_news(db_name="scraper_data.db"):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute("SELECT * FROM news")
    rows = c.fetchall()
    conn.close()
    return rows
