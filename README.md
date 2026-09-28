# Aplikasi Enkripsi File Hybrid (AES-256 + RSA-2048 + ECC)

Aplikasi Enkripsi File Hybrid adalah solusi keamanan data yang menggabungkan kekuatan dari beberapa algoritma kriptografi untuk memberikan perlindungan maksimal terhadap file-file penting Anda. Dengan mengkombinasikan algoritma enkripsi simetris (**AES-256**) dan asimetris (**RSA-2048** dan **ECC NIST256p**), aplikasi ini menawarkan keamanan berlapis yang sangat kuat.

![screen](/static/images/kriptografi.png)

## 🚀 Fitur Utama

- **Enkripsi File Hybrid**: Enkripsi payload dokumen menggunakan AES-256 (CBC mode) dengan kunci acak yang dibuat dinamis.
- **Enkripsi Kunci Asimetris**: Kunci AES dienkripsi dengan RSA-2048 (OAEP SHA-256).
- **Tanda Tangan Digital Ganda**: Integritas file dan keaslian dokumen divalidasi menggunakan RSA-PSS dan ECC (ECDSA NIST-256p).
- **Verifikasi Dokumen**: Memeriksa apakah file masih asli dan belum dimodifikasi sejak ditandatangani.
- **Dekripsi Dokumen & Pratinjau**: Dekripsi langsung file terenkripsi serta preview langsung di browser untuk gambar, teks, dan dokumen.
- **Generator Kunci**: Fitur pembuatan pasangan kunci publik dan privat RSA serta ECC langsung di antarmuka web.
- **Dukungan Bilingual (ID / EN)**: Tersedia pengalih bahasa instan (Bahasa Indonesia & English) tanpa reload halaman.

---

## 📁 Struktur Direktori

```text
kriptografi/
├── app.py                  # Factory Flask & seluruh routing API/Halaman
├── config.py               # Pengaturan konfigurasi terpusat (Dev/Prod)
├── hybrid_signature.py     # Engine kriptografi (AES, RSA, ECC)
├── wsgi.py                 # WSGI entry point untuk Gunicorn / VPS
├── passenger_wsgi.py       # WSGI entry point untuk Hostinger hPanel/cPanel
├── requirements.txt        # Dependensi proyek
├── .env.example            # Template variabel environment
├── .gitignore              # Konfigurasi pengabaian file Git
├── .htaccess               # Proteksi Apache/LiteSpeed web server
├── HOSTINGER_DEPLOYMENT.md # Panduan lengkap hosting di Hostinger
├── static/                 # Aset statis frontend
│   ├── css/
│   │   └── style.css       # Design system, glassmorphism & animasi
│   ├── js/
│   │   ├── main.js         # Utilitas toast, copy, drag & drop
│   │   └── translations.js # Kamus bahasa bilingual (ID / EN)
│   └── images/             # Gambar & ikon web
├── templates/              # Antarmuka web HTML Jinja2
│   ├── base.html
│   ├── index.html
│   └── hybrid-encription.html
├── uploaded_files/         # Direktori temporary upload
└── signed_files/           # Direktori temporary file terenkripsi
```

---

## 🛠️ Teknologi yang Digunakan

- **Backend**:
  - Python 3.8+
  - Flask 2.3+ (Web Framework)
  - Cryptography (RSA & AES-256)
  - ECDSA (Elliptic Curve Cryptography)
  - Hashlib (SHA-256)
  - Gunicorn & Phusion Passenger (Production WSGI)

- **Frontend**:
  - HTML5 & CSS3
  - Tailwind CSS
  - JavaScript (Vanilla JS Fetch API)

---

## 💻 Cara Menjalankan Secara Lokal

1. **Clone repository ini**:
   ```bash
   git clone https://github.com/muhavan/kriptografi.git
   cd kriptografi
   ```

2. **Buat dan aktifkan Virtual Environment**:
   - **Windows**:
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```
   - **macOS / Linux**:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install Dependensi**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Buat file `.env`** (opsional untuk lokal):
   ```bash
   cp .env.example .env
   ```

5. **Jalankan Aplikasi**:
   ```bash
   python app.py
   ```
   Akses di browser melalui `http://127.0.0.1:5000/`.

---

## 🌐 Cara Hosting di Hostinger

Aplikasi ini sudah dipersiapkan dan dioptimalkan secara langsung untuk dihosting di Hostinger, baik menggunakan:
1. **Hostinger Web / Cloud Hosting (hPanel Python App)**
2. **Hostinger VPS (Ubuntu / Debian + Gunicorn + Nginx)**

Silakan baca panduan lengkap langkah demi langkah pada file [HOSTINGER_DEPLOYMENT.md](file:///c:/Users/EVAN/Desktop/kriptografi/HOSTINGER_DEPLOYMENT.md).

---

## 📄 Lisensi

Proyek ini dilisensikan © 17.6A.27.
Dibuat dengan ❤️ oleh Tim Pengembang Enkripsi File Hybrid