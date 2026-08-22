import sqlite3
from datetime import datetime, timedelta

def init_db(db_path="market_data.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS levels (
            pair TEXT, level REAL, type TEXT, score INTEGER, PRIMARY KEY (pair, level)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cooldowns (
            pair TEXT, level REAL, last_alerted TIMESTAMP, PRIMARY KEY (pair, level)
        )
    ''')
    conn.commit()
    conn.close()

def save_levels(pair, levels, db_path="market_data.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM levels WHERE pair = ?', (pair,))
    for l in levels:
        cursor.execute('''
            INSERT OR REPLACE INTO levels (pair, level, type, score) VALUES (?, ?, ?, ?)
        ''', (pair, l['level'], l['type'], l['score']))
    conn.commit()
    conn.close()

def get_levels(pair, db_path="market_data.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT level, type, score FROM levels WHERE pair = ?', (pair,))
    rows = cursor.fetchall()
    conn.close()
    return [{"level": r[0], "type": r[1], "score": r[2]} for r in rows]

def check_cooldown(pair, level, cooldown_hours=4, db_path="market_data.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT last_alerted FROM cooldowns WHERE pair = ? AND level = ?', (pair, level))
    row = cursor.fetchone()
    conn.close()
    if not row:
        return True
    last_alerted = datetime.fromisoformat(row[0])
    return (datetime.now() - last_alerted) > timedelta(hours=cooldown_hours)

def set_cooldown(pair, level, db_path="market_data.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO cooldowns (pair, level, last_alerted) VALUES (?, ?, ?)
    ''', (pair, level, datetime.now().isoformat()))
    conn.commit()
    conn.close()
