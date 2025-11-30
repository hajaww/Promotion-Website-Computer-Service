from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import os, json, threading, sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'selebew'  # Ganti dengan key yang aman

# Hardcoded admin credentials
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'admin123'

# Database configuration
DB_PATH = os.path.join(os.path.dirname(__file__), 'aacell.db')

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
os.makedirs(DATA_DIR, exist_ok=True)
TESTIMONI_FILE = os.path.join(DATA_DIR, 'testimoni.json')

_lock = threading.Lock()

# Database helper functions
def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
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
    
    conn.commit()
    conn.close()

def load_testimoni():
    if os.path.isfile(TESTIMONI_FILE):
        try:
            with open(TESTIMONI_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, list):
                    return data
        except Exception as e:
            print(f"[server-debug] Failed to load testimonials: {e}")
    return []

def save_testimoni():
    try:
        with open(TESTIMONI_FILE, 'w', encoding='utf-8') as f:
            json.dump(testimoni_data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"[server-debug] Failed to save testimonials: {e}")

testimoni_data = load_testimoni()  # persisted testimonials

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/testimoni', methods=['GET', 'POST'])
def testimoni():
    if request.method == 'POST':
        nama = request.form.get('nama')
        pesan = request.form.get('pesan')
        rating = request.form.get('rating', '5')  # Default to 5 stars if not provided
        if nama and pesan:
            with _lock:
                testimoni_data.insert(0, {"nama": nama, "pesan": pesan, "rating": int(rating)})
                save_testimoni()
                # Debug: print server-side testimonial count after insert
                print(f"[server-debug] POST added testimonial. total testimoni_data = {len(testimoni_data)}", flush=True)
                for i, t in enumerate(testimoni_data[:5]):
                    print(f"[server-debug] {i}: nama={t.get('nama')!r} pesan={t.get('pesan')!r} rating={t.get('rating')!r}", flush=True)
        return redirect(url_for('testimoni'))  
    
    # Google Reviews data
    google_reviews = [
        {
            "nama": "Fian Septiansyah",
            "pesan": "one of best smartwatch service!. Pertama kali service smartwatch disini honest review : dari awal sampai selesai service pelayanannya sangat sangat ramah , kooperatif, informatif, detail menjelaskan kerusakan unit yang di service, selalu update progres service sampai selesai jadi kita sebagai customer aman nyaman, worth for the price. pokonya aa cellcom salah satu tempat service smartwatch terbaik! Bisa service segala unit electronic juga seperti camera, laptop, handphone dll. Highly recommend 🫡✨🔝",
            "rating": 5,
            "waktu": "4 Bulan Lalu",
            "avatar": "F",
            "gambar": "/static/electronic.png"
        },
        {
            "nama": "Kresna Arya (mr1bug)",
            "pesan": "Service jam coros pace 2 disini, terbaik bang Arie - Dijelasin biaya biaya nya, tanpa surprise dadakan. - selalu kirim video update nya. Jangan ragu service disini.",
            "rating": 5,
            "waktu": "5 bulan lalu",
            "avatar": "K",
            "gambar": "/static/logo.png"
        },
        {
            "nama": "Budi Santoso",
            "pesan": "AACell adalah tempat servis laptop terbaik di daerah ini. Mereka bisa memperbaiki berbagai merek laptop dengan cepat dan harga bersaing. Pelayanan sangat baik!",
            "rating": 5,
            "waktu": "3 minggu lalu",
            "avatar": "B",
            "gambar": "/static/electronic.png"
        },
        {
            "nama": "Dewi Kusuma",
            "pesan": "Sudah 3 kali bawa laptop ke AACell untuk servis. Setiap kali hasilnya selalu memuaskan. Teknisi profesional dan sparepart yang digunakan berkualitas. Terima kasih AACell!",
            "rating": 5,
            "waktu": "1 bulan lalu",
            "avatar": "D",
            "gambar": "/static/logo.png"
        },
        {
            "nama": "Rafi Pratama",
            "pesan": "Servis cepat dan harga transparan. AACell berhasil memperbaiki laptop gaming saya yang overheating. Sekarang performanya kembali optimal. Recommended banget!",
            "rating": 5,
            "waktu": "2 minggu lalu",
            "avatar": "R",
            "gambar": "/static/electronic.png"
        },
        {
            "nama": "Rafi Pratama",
            "pesan": "Servis cepat dan harga transparan. AACell berhasil memperbaiki laptop gaming saya yang overheating. Sekarang performanya kembali optimal. Recommended banget!",
            "rating": 5,
            "waktu": "2 minggu lalu",
            "avatar": "R",
            "gambar": "/static/electronic.png"
        }
    ]
    
    # Debug: log on GET render how many testimonials will be sent to template
    print(f"[server-debug] GET /testimoni rendering {len(testimoni_data)} testimonials", flush=True)
    return render_template('testimoni.html', testimoni_data=testimoni_data, google_reviews=google_reviews)

@app.route('/api/testimoni')
def api_testimoni():
    return jsonify(testimoni_data)

@app.route('/admin/clear-testimoni')
def clear_testimoni():
    token = request.args.get('token')
    if token != 'dev':
        return 'Unauthorized', 401
    with _lock:
        testimoni_data.clear()
        save_testimoni()
    return 'Cleared'

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/check', methods=['GET', 'POST'])
def check():
    hasil = None
    if request.method == 'POST':
        nomor = request.form.get('nomor', '').strip().upper()
        if nomor:
            conn = get_db_connection()
            # Search by nota or nama
            hasil = conn.execute(
                'SELECT * FROM servis_status WHERE UPPER(nota) = ? OR UPPER(nama) LIKE ?',
                (nomor, f'%{nomor}%')
            ).fetchone()
            conn.close()
            
            if hasil:
                hasil = dict(hasil)
    
    return render_template('check.html', hasil=hasil)

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Redirect to home if already logged in
    if 'username' in session:
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['username'] = username
            flash('Login berhasil!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Username atau password salah.', 'error')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    # Registration disabled - redirect to login
    flash('Registrasi tidak tersedia. Silakan hubungi administrator.', 'error')
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Anda telah logout.', 'info')
    return redirect(url_for('home'))

@app.route('/admin/servis', methods=['GET', 'POST'])
def admin_servis():
    # Check if user is logged in
    if 'username' not in session:
        flash('Silakan login terlebih dahulu untuk mengakses halaman admin.', 'error')
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    edit_data = None
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'add':
            # Tambah data servis baru
            nota = request.form.get('nota', '').strip().upper()
            nama = request.form.get('nama', '').strip()
            no_telepon = request.form.get('no_telepon', '').strip()
            perangkat = request.form.get('perangkat', '').strip()
            kerusakan = request.form.get('kerusakan', '').strip()
            status = request.form.get('status', 'menunggu-konfirmasi')
            tanggal_masuk = request.form.get('tanggal_masuk', '')
            estimasi_selesai = request.form.get('estimasi_selesai', '')
            keterangan = request.form.get('keterangan', '').strip()
            
            # Check if nota already exists
            existing = conn.execute('SELECT id FROM servis_status WHERE nota = ?', (nota,)).fetchone()
            
            if existing:
                flash(f'Nomor nota {nota} sudah ada! Gunakan nomor nota yang berbeda.', 'error')
            else:
                try:
                    conn.execute('''
                        INSERT INTO servis_status 
                        (nota, nama, no_telepon, perangkat, kerusakan, status, tanggal_masuk, estimasi_selesai, keterangan)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (nota, nama, no_telepon, perangkat, kerusakan, status, tanggal_masuk, estimasi_selesai, keterangan))
                    conn.commit()
                    flash(f'Data servis {nota} berhasil ditambahkan!', 'success')
                except Exception as e:
                    flash(f'Error: {str(e)}', 'error')
            
            conn.close()
            return redirect(url_for('admin_servis'))
        
        elif action == 'edit':
            # Edit data servis
            old_nota = request.form.get('old_nota')
            nota = request.form.get('nota', '').strip().upper()
            nama = request.form.get('nama', '').strip()
            no_telepon = request.form.get('no_telepon', '').strip()
            perangkat = request.form.get('perangkat', '').strip()
            kerusakan = request.form.get('kerusakan', '').strip()
            status = request.form.get('status', 'menunggu-konfirmasi')
            tanggal_masuk = request.form.get('tanggal_masuk', '')
            estimasi_selesai = request.form.get('estimasi_selesai', '')
            keterangan = request.form.get('keterangan', '').strip()
            
            try:
                conn.execute('''
                    UPDATE servis_status 
                    SET nota=?, nama=?, no_telepon=?, perangkat=?, kerusakan=?, status=?, 
                        tanggal_masuk=?, estimasi_selesai=?, keterangan=?, updated_at=CURRENT_TIMESTAMP
                    WHERE nota=?
                ''', (nota, nama, no_telepon, perangkat, kerusakan, status, tanggal_masuk, estimasi_selesai, keterangan, old_nota))
                conn.commit()
                flash(f'Data servis {nota} berhasil diupdate!', 'success')
            except Exception as e:
                flash(f'Error: {str(e)}', 'error')
            
            conn.close()
            return redirect(url_for('admin_servis'))
        
        elif action == 'edit_form':
            # Show edit form
            nota = request.form.get('nota')
            servis = conn.execute('SELECT * FROM servis_status WHERE nota = ?', (nota,)).fetchone()
            if servis:
                edit_data = dict(servis)
        
        elif action == 'delete':
            # Delete data servis
            nota = request.form.get('nota')
            try:
                conn.execute('DELETE FROM servis_status WHERE nota = ?', (nota,))
                conn.commit()
                flash(f'Data servis {nota} berhasil dihapus!', 'success')
            except Exception as e:
                flash(f'Error: {str(e)}', 'error')
            
            conn.close()
            return redirect(url_for('admin_servis'))
    
    # GET request - load all data
    servis_list = conn.execute('SELECT * FROM servis_status ORDER BY created_at DESC').fetchall()
    servis_list = [dict(row) for row in servis_list]
    conn.close()
    
    return render_template('admin_servis.html', servis_list=servis_list, edit_data=edit_data)


if __name__ == '__main__':
    # Initialize database if not exists
    if not os.path.exists(DB_PATH):
        print("Initializing database...")
        init_db()
        # Add sample data
        conn = get_db_connection()
        cursor = conn.cursor()
        
        sample_data = [
            ('S001', 'Budi Santoso', '081234567890', 'Laptop', 'Layar pecah, tidak bisa menyala', 
             'sedang-dikerjakan', '2024-01-15', '2024-01-20', 'Sedang proses pergantian LCD'),
            ('S002', 'Siti Aminah', '082345678901', 'Smartphone', 'Baterai cepat habis, charging lambat', 
             'menunggu-sparepart', '2024-01-16', '2024-01-25', 'Menunggu baterai original dari supplier'),
            ('S003', 'Ahmad Rizki', '083456789012', 'Tablet', 'Touchscreen tidak responsif', 
             'selesai', '2024-01-10', '2024-01-14', 'Servis selesai, sudah dicek dan berfungsi normal'),
        ]
        
        cursor.executemany('''
            INSERT INTO servis_status 
            (nota, nama, no_telepon, perangkat, kerusakan, status, tanggal_masuk, estimasi_selesai, keterangan)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', sample_data)
        
        conn.commit()
        conn.close()
        print("✅ Database initialized with sample data!")
    
    app.run(debug=True, port=5003)
