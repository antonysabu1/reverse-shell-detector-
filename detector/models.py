import sqlite3
import datetime
import os

DB_PATH = "/data/alerts.db"

def init_db():
    # Ensure the /data directory exists
    os.makedirs("/data", exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create the alerts table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            shell_type TEXT,
            src_ip TEXT,
            dst_ip TEXT,
            dst_port INTEGER,
            payload_snippet TEXT
        )
    ''')
    
    conn.commit()
    conn.close()
    print("[*] Database initialized at", DB_PATH)

def save_alert(shell_type, src_ip, dst_ip, dst_port, payload_snippet):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Clean up snippet for display
    clean_snippet = str(payload_snippet)[:100]
    
    cursor.execute('''
        INSERT INTO alerts (shell_type, src_ip, dst_ip, dst_port, payload_snippet)
        VALUES (?, ?, ?, ?, ?)
    ''', (shell_type, src_ip, dst_ip, dst_port, clean_snippet))
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
