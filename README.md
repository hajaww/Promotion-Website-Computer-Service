# AACell - Website Servis Elektronik

Website untuk manajemen servis perangkat elektronik (HP, Laptop, Tablet, Smartwatch) dengan fitur cek status dan admin panel.

## 🚀 Fitur

### User Features:
- ✅ **Cek Status Servis** - Customer bisa cek status servis dengan nomor nota
- ✅ **Testimoni** - Halaman testimoni dari customer
- ✅ **Contact** - Informasi kontak dan lokasi toko
- ✅ **WhatsApp Integration** - Quick chat ke WhatsApp

### Admin Features:
- ✅ **Login Admin** - Secure login dengan username/password
- ✅ **CRUD Data Servis** - Tambah, edit, hapus data servis
- ✅ **Status Management** - Update status servis secara real-time
- ✅ **Database SQLite** - Data tersimpan di database, bukan JSON

## 📦 Teknologi

- **Backend**: Flask (Python)
- **Database**: SQLite
- **Frontend**: HTML, CSS, JavaScript
- **Icons**: Font Awesome
- **Design**: Modern dark theme dengan glassmorphism

## 🔧 Instalasi

### 1. Clone Repository
```bash
git clone https://github.com/hajaww/Promotion-Website-Computer-Service.git
cd Promotion-Website-Computer-Service
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Initialize Database
```bash
python3 init_db.py
```

Database `aacell.db` akan terbuat dengan sample data.

### 4. Run Application
```bash
python3 app.py
```

Aplikasi akan berjalan di `http://localhost:5003`

## 👤 Login Admin

**Username**: `admin`  
**Password**: `admin123`

⚠️ **PENTING**: Ganti password di production!

## 📊 Database Schema

### Tabel: `servis_status`

| Field | Type | Description |
|-------|------|-------------|
| id | INTEGER | Primary key (auto increment) |
| nota | TEXT | Nomor nota servis (unique) |
| nama | TEXT | Nama pelanggan |
| no_telepon | TEXT | Nomor telepon |
| perangkat | TEXT | Jenis perangkat (Laptop, HP, dll) |
| kerusakan | TEXT | Deskripsi kerusakan |
| status | TEXT | Status servis (menunggu-konfirmasi, sedang-dikerjakan, menunggu-sparepart, selesai) |
| tanggal_masuk | TEXT | Tanggal masuk servis |
| estimasi_selesai | TEXT | Estimasi tanggal selesai |
| keterangan | TEXT | Keterangan tambahan |
| created_at | TIMESTAMP | Waktu dibuat |
| updated_at | TIMESTAMP | Waktu terakhir diupdate |

## 🌐 Deployment

### Deploy ke Platform Cloud:

#### **Option 1: Railway.app**
1. Push ke GitHub
2. Connect repository ke Railway
3. Set environment variables jika perlu
4. Deploy otomatis!

#### **Option 2: PythonAnywhere**
1. Upload files ke server
2. Setup virtual environment
3. Configure WSGI
4. Run aplikasi

#### **Option 3: Heroku**
```bash
heroku create aacell-servis
git push heroku main
```

### Environment Variables (Production):
```bash
SECRET_KEY=your-secret-key-here
FLASK_ENV=production
```

## 📱 Fitur WhatsApp

Update nomor WhatsApp di:
- `/templates/check.html` - untuk tombol WhatsApp di hasil cek status
- `/templates/contact.html` - untuk tombol contact WhatsApp

Cari: `6281223447569` dan ganti dengan nomor Anda.

## 🎨 Customization

### Warna Theme
Edit di `/static/css/style.css`:
```css
:root {
    --primary-500: #3b82f6;  /* Warna utama */
    --gray-900: #0f172a;     /* Background gelap */
    /* ... */
}
```

### Logo & Branding
Replace file di `/static/`:
- `logo.png` - Logo utama
- `electronic.png` - Gambar background

## 📄 File Structure

```
Promotion-Website-Computer-Service/
├── app.py                 # Main Flask application
├── init_db.py            # Database initialization script
├── requirements.txt      # Python dependencies
├── aacell.db            # SQLite database (auto-generated)
├── data/
│   └── testimoni.json   # Testimoni data (JSON)
├── static/
│   ├── css/
│   │   └── style.css    # Main stylesheet
│   ├── js/
│   │   └── script.js    # JavaScript
│   ├── logo.png
│   └── electronic.png
├── templates/
│   ├── base.html        # Base template
│   ├── index.html       # Homepage
│   ├── check.html       # Cek status page
│   ├── admin_servis.html # Admin panel
│   ├── login.html       # Login page
│   ├── contact.html     # Contact page
│   └── testimoni.html   # Testimonial page
└── README.md
```

## 🔒 Security Notes

1. **Change Secret Key**: Update `app.secret_key` di `app.py`
2. **Change Admin Password**: Update `ADMIN_PASSWORD` di `app.py`
3. **Use HTTPS**: Di production, selalu gunakan HTTPS
4. **Database Backup**: Backup `aacell.db` secara berkala

## 📞 Support

Untuk pertanyaan atau masalah:
- WhatsApp: 081223447569
- Email: aacell@example.com

## 📝 License

MIT License - Feel free to use and modify!

---

**Developed with ❤️ by AACell Team**
