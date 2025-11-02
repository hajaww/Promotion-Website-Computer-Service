from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

testimoni_data = [
    {"nama": "Rafi", "pesan": "Pelayanan cepat dan ramah!", "rating": 5},
    {"nama": "Dewi", "pesan": "Laptop saya jadi seperti baru lagi, mantap!", "rating": 5}
]

servis_data = [
    {"nota": "S001", "nama": "Rafi", "status": "Sedang Dikerjakan"},
    {"nota": "S002", "nama": "Dewi", "status": "Menunggu Sparepart"},
    {"nota": "S003", "nama": "Budi", "status": "Selesai - Siap Diambil"},
]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/testimoni', methods=['GET', 'POST'])
def testimoni():
    if request.method == 'POST':
        nama = request.form.get('nama')
        pesan = request.form.get('pesan')
        rating = request.form.get('rating', '5')  # Default to 5 stars if not provided
        if nama and pesan:
            testimoni_data.insert(0, {"nama": nama, "pesan": pesan, "rating": int(rating)})
        return redirect(url_for('testimoni'))  
    return render_template('testimoni.html', testimoni_data=testimoni_data)

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

@app.route('/test')
def test():
    return '<h1 style="color: white; background: black; padding: 50px;">Website Berfungsi! Konten Putih di Background Hitam</h1>'


if __name__ == '__main__':
    app.run(debug=True, port=5003)
