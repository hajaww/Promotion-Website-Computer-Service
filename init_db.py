import sqlite3
import os

# Path to database
DB_PATH = os.path.join(os.path.dirname(__file__), 'aacell.db')

def init_database():
    """Initialize database and create table"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create servis_status table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS servis_status (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nota TEXT UNIQUE NOT NULL,
            nama TEXT NOT NULL,
            no_telepon TEXT,
            perangkat TEXT NOT NULL,
            kerusakan TEXT NOT NULL,
            status TEXT DEFAULT 'menunggu-konfirmasi',
            tanggal_masuk TEXT NOT NULL,
            estimasi_selesai TEXT,
            keterangan TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Check if table is empty, add sample data
    cursor.execute('SELECT COUNT(*) FROM servis_status')
    count = cursor.fetchone()[0]
    
    if count == 0:
        sample_data = [
        ]
        
        cursor.executemany('''
            INSERT INTO servis_status 
            (nota, nama, no_telepon, perangkat, kerusakan, status, tanggal_masuk, estimasi_selesai, keterangan)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', sample_data)
        
        print("✅ Sample data added successfully!")
    
    conn.commit()
    conn.close()
    print(f"✅ Database initialized: {DB_PATH}")

if __name__ == '__main__':
    init_database()
