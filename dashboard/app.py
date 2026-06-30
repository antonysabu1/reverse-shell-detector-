from flask import Flask, render_template, jsonify
import sqlite3
import os

app = Flask(__name__)
DB_PATH = "/data/alerts.db"

def get_db_connection():
    # If the detector hasn't created the DB yet, create an empty one to avoid crashes
    if not os.path.exists("/data"):
        os.makedirs("/data", exist_ok=True)
        
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    
    # Ensure table exists just in case Dashboard starts before Detector
    conn.execute('''
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            shell_type TEXT,
            src_ip TEXT,
            dst_ip TEXT,
            dst_port INTEGER,
            payload_snippet TEXT,
            confidence REAL DEFAULT 0.0,
            reason TEXT DEFAULT ''
        )
    ''')
    
    # Check if confidence and reason columns exist (for migration if table already existed)
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(alerts)")
    columns = [col[1] for col in cursor.fetchall()]
    
    if "confidence" not in columns:
        cursor.execute("ALTER TABLE alerts ADD COLUMN confidence REAL DEFAULT 0.0")
    if "reason" not in columns:
        cursor.execute("ALTER TABLE alerts ADD COLUMN reason TEXT DEFAULT ''")
        
    conn.commit()
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/alerts')
def api_alerts():
    conn = get_db_connection()
    alerts = conn.execute('SELECT * FROM alerts ORDER BY id DESC LIMIT 50').fetchall()
    conn.close()
    
    # Convert sqlite3.Row objects to dicts
    return jsonify([dict(ix) for ix in alerts])

if __name__ == '__main__':
    print("[*] Starting ShellSnare Dashboard on port 8080...")
    app.run(host='0.0.0.0', port=8080)
