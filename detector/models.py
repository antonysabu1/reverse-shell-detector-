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
            payload_snippet TEXT,
            confidence REAL DEFAULT 0.0,
            reason TEXT DEFAULT '',
            action_taken TEXT DEFAULT 'Detected'
        )
    ''')
    
    # Check if confidence, reason, and action_taken columns exist (for migration if table already existed)
    cursor.execute("PRAGMA table_info(alerts)")
    columns = [col[1] for col in cursor.fetchall()]
    
    if "confidence" not in columns:
        cursor.execute("ALTER TABLE alerts ADD COLUMN confidence REAL DEFAULT 0.0")
    if "reason" not in columns:
        cursor.execute("ALTER TABLE alerts ADD COLUMN reason TEXT DEFAULT ''")
    if "action_taken" not in columns:
        cursor.execute("ALTER TABLE alerts ADD COLUMN action_taken TEXT DEFAULT 'Detected'")
    
    conn.commit()
    conn.close()
    print("[*] Database initialized at", DB_PATH)

def save_alert(shell_type, src_ip, dst_ip, dst_port, payload_snippet, confidence=0.0, reason='', action_taken='Detected'):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Clean up snippet for display
    if isinstance(payload_snippet, bytes):
        clean_snippet = payload_snippet.decode(errors='ignore')[:100]
    else:
        clean_snippet = str(payload_snippet)[:100]
    
    cursor.execute('''
        INSERT INTO alerts (shell_type, src_ip, dst_ip, dst_port, payload_snippet, confidence, reason, action_taken)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (shell_type, src_ip, dst_ip, dst_port, clean_snippet, confidence, reason, action_taken))
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
