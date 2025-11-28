from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import os, json, threading

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Ganti dengan key yang aman

users = [
    {'gmail': 'admin@gmail.com', 'password': 'admin123'},
    {'gmail': 'user@gmail.com', 'password': 'user123'}
]  # Array sementara untuk menyimpan pengguna

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
os.makedirs(DATA_DIR, exist_ok=True)
TESTIMONI_FILE = os.path.join(DATA_DIR, 'testimoni.json')

_lock = threading.Lock()

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

servis_data = [
    {"nota": "S001", "nama": "Rafi", "status": "Sedang Dikerjakan"},
    {"nota": "S002", "nama": "Dewi", "status": "Menunggu Sparepart"},
    {"nota": "S003", "nama": "Budi", "status": "Selesai - Siap Diambil"},
]

testimoni_data = testimoni_data  # keep loaded

servis_data = [
    {"nota": "S001", "nama": "Rafi", "status": "Sedang Dikerjakan"},
    {"nota": "S002", "nama": "Dewi", "status": "Menunggu Sparepart"},
    {"nota": "S003", "nama": "Budi", "status": "Selesai - Siap Diambil"},
]

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
        nomor = request.form.get('nomor')
        for s in servis_data:
            if s["nota"] == nomor or s["nama"].lower() == nomor.lower():
                hasil = s
                break
    return render_template('check.html', hasil=hasil)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        gmail = request.form.get('gmail')
        password = request.form.get('password')
        for user in users:
            if user['gmail'] == gmail and user['password'] == password:
                session['gmail'] = gmail
                flash('Login berhasil!', 'success')
                return redirect(url_for('home'))
        flash('Gmail atau password salah.', 'error')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        gmail = request.form.get('gmail')
        password = request.form.get('password')
        if any(user['gmail'] == gmail for user in users):
            flash('Gmail sudah terdaftar.', 'error')
        else:
            users.append({'gmail': gmail, 'password': password})
            flash('Registrasi berhasil! Silakan login.', 'success')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('gmail', None)
    flash('Anda telah logout.', 'info')
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True, port=5003)
