from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your_default_secret_key')

# Database simulasi
daftar_tamu = []
daftar_reservasi = []
daftar_kamar = {
    'Santika': {
        'gambar': 'https://dynamic-media-cdn.tripadvisor.com/media/photo-o/08/70/a6/aa/hotel-santika-palu.jpg?w=500&h=-1&s=1',
        'kamar': [
            {'id': 101, 'tipe': 'Superior(Santika)', 'harga': 650000, 'status': 'Tersedia', 'fasilitas': ['TV', 'AC', 'WiFi']},
            {'id': 102, 'tipe': 'Deluxe(Santika)', 'harga': 800000, 'status': 'Tersedia', 'fasilitas': ['TV', 'AC', 'WiFi', 'Dapur']},
        ],
    },
    'Best Western': {
        'gambar': 'https://s-light.tiket.photos/t/01E25EBZS3W0FY9GTG6C42E1SE/t_htl-mobile/tix-hotel/images-web/2024/09/18/781ae9fa-8273-4e7f-9429-314867219a80-1726627518543-ad6b5d811cf50c1fddb4e23c57d759dd.jpg',
        'kamar': [
            {'id': 201, 'tipe': 'Superior(Best Western)', 'harga': 800000, 'status': 'Tersedia', 'fasilitas': ['TV', 'AC', 'WiFi']},
            {'id': 202, 'tipe': 'Deluxe(Best Western)', 'harga': 1000000, 'status': 'Tersedia', 'fasilitas': ['TV', 'AC', 'WiFi', 'Minibar']},
        ],
    },
    'Swiss-Bell': {
        'gambar': 'https://cf.bstatic.com/xdata/images/hotel/max1024x768/330250807.jpg?k=5a3a4c2b60c71e4d2d2acdbb374369e141321e4479f3368ba8863dd965f946c3&o=',
        'kamar': [
            {'id': 301, 'tipe': 'Deluxe(Swiss-Bell)', 'harga': 750000, 'status': 'Tersedia', 'fasilitas': ['TV', 'AC', 'WiFi']},
            {'id': 302, 'tipe': 'Superior Deluxe(Swiss-Bell)', 'harga': 900000, 'status': 'Tersedia', 'fasilitas': ['TV', 'AC', 'WiFi', 'Jacuzzi']},
        ],
    },
}

@app.route('/')
def index():
    return render_template('index.html', daftar_kamar=daftar_kamar)

@app.route('/about', methods=['GET', 'POST'])
def about():
    if request.method == 'POST':
        return render_template('about.html', reservasi=request.form)
    return render_template('about.html')

@app.route('/rooms')
def rooms():
    return render_template('rooms.html', daftar_kamar=daftar_kamar)

@app.route('/booking', methods=['GET', 'POST'])
def booking():
    if request.method == 'POST':
        if not all([request.form.get('nama'), request.form.get('email'), request.form.get('telepon'),
                    request.form.get('hotel'), request.form.get('kamar_id'),
                    request.form.get('check_in'), request.form.get('check_out'),
                    request.form.get('jumlah_tamu')]):
            flash('Semua field harus diisi!', 'danger')
            return redirect(url_for('booking'))

        reservasi = {
            'nama': request.form.get('nama'),
            'email': request.form.get('email'),
            'telepon': request.form.get('telepon'),
            'hotel': request.form.get('hotel'),
            'kamar_id': request.form.get('kamar_id'),
            'check_in': request.form.get('check_in'),
            'check_out': request.form.get('check_out'),
            'jumlah_tamu': request.form.get('jumlah_tamu'),
            'status': 'Menunggu Konfirmasi',
            'timestamp': datetime.now()
        }
        daftar_reservasi.append(reservasi)
        flash('Reservasi berhasil dibuat! Kami akan menghubungi Anda untuk konfirmasi.', 'success')
        return render_template('about.html', reservasi=reservasi)
    return render_template('booking.html', daftar_kamar=daftar_kamar)

@app.route('/Check-in', methods=['GET'])
def checkin():
    return render_template('Chek-in Result.html', reservasi=daftar_reservasi)

@app.route('/admin')
def admin():
    return render_template('admin.html', reservasi=daftar_reservasi, tamu=daftar_tamu)

if __name__ == '__main__':
    app.run(debug=True)
