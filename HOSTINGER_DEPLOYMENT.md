# Panduan Lengkap Hosting Aplikasi Kriptografi di Hostinger

Panduan ini menjelaskan cara mendeploy aplikasi Flask **Enkripsi File Hybrid** ke hosting **Hostinger**.

Terdapat 2 jenis hosting di Hostinger yang umum digunakan untuk menjalankan Python:
1. **Opsi 1: Hostinger Web / Cloud Hosting (hPanel - Fitur Python App)** *(Paling mudah jika paket hosting Anda mendukung Python)*
2. **Opsi 2: Hostinger VPS (Ubuntu / Debian + Gunicorn + Nginx)** *(Paling stabil dan fleksibel)*

---

## 📁 Struktur File Proyek yang Sudah Dirapikan

```text
kriptografi/
├── app.py                  # Factory Flask & seluruh routing API/Halaman
├── config.py               # Konfigurasi terpusat (Development & Production)
├── hybrid_signature.py     # Logika kriptografi inti (AES-256, RSA-2048, ECC NIST256p)
├── wsgi.py                 # Entry point untuk server produksi (Gunicorn / VPS)
├── passenger_wsgi.py       # Entry point untuk Hostinger hPanel/cPanel (Phusion Passenger)
├── requirements.txt        # Daftar dependensi Python
├── .env.example            # Contoh template environment variables
├── .htaccess               # Konfigurasi keamanan Apache/LiteSpeed web server
├── .gitignore              # Mengabaikan venv, cache, dan file upload agar repo bersih
├── static/                 # Folder aset statis standar Flask
│   └── images/             # Gambar & ikon (favicon.ico, favicon.png, kriptografi.png)
├── templates/              # File template Jinja2 HTML
│   ├── base.html
│   ├── index.html
│   └── hybrid-encription.html
├── uploaded_files/         # Tempat penyimpanan sementara file upload (.gitkeep)
└── signed_files/           # Tempat penyimpanan file hasil enkripsi (.gitkeep)
```

> ⚠️ **PERINGATAN PENTING SEBELUM UPLOAD:**
> **JANGAN PERNAH** mengunggah folder `venv` dari komputer Windows Anda ke server Linux hosting. Folder `venv` di Windows berisi file binary `.exe` yang tidak bisa berjalan di Linux dan ukurannya sangat besar. Lingkungan Python virtual harus dibuat langsung di server hosting.

---

## OPSI 1: Hostinger Web / Cloud Hosting (hPanel Python App)

Fitur ini menggunakan **Phusion Passenger** (WSGI runner) di atas server LiteSpeed/CloudLinux.

### Langkah 1: Siapkan File Proyek
1. Di komputer lokal Anda, buat file arsip **ZIP** dari folder proyek `kriptografi`.
2. **Pastikan TIDAK menyertakan folder `venv/` dan `__pycache__/`** ke dalam ZIP.

### Langkah 2: Buat Python App di hPanel
1. Login ke akun [Hostinger hPanel](https://hpanel.hostinger.com/).
2. Masuk ke menu **Websites** > klik **Manage** pada domain Anda.
3. Di panel pencarian sebelah kiri, cari dan pilih menu **"Python"** (atau **"Setup Python App"**).
4. Klik tombol **"Create Application"** lalu isi formulir:
   - **Python version**: Pilih `3.10` atau `3.11` (direkomendasikan).
   - **Application root**: Isi nama folder proyek, misalnya `kriptografi` atau `public_html`.
   - **Application URL**: Pilih domain Anda (misal `domainanda.com`).
   - **Application startup file**: Ketik `passenger_wsgi.py` *(file ini sudah kami buatkan)*.
   - **Application Entry point**: Ketik `application` *(sudah disesuaikan di passenger_wsgi.py)*.
5. Klik **Create**.

### Langkah 3: Upload File Proyek
1. Buka menu **File Manager** di hPanel.
2. Masuk ke direktori yang Anda tentukan di **Application root** (misalnya `public_html` atau `kriptografi`).
3. Upload file ZIP proyek Anda, lalu klik kanan dan pilih **Extract**.
4. Pastikan file `passenger_wsgi.py`, `app.py`, `config.py`, `requirements.txt`, folder `static/`, dan `templates/` berada langsung di dalam folder root aplikasi tersebut.

### Langkah 4: Konfigurasi File `.env`
1. Di File Manager, cari file `.env.example`.
2. Ubah nama (Rename) atau salin menjadi `.env`.
3. Buka file `.env` dan sesuaikan:
   ```ini
   FLASK_ENV=production
   FLASK_DEBUG=0
   SECRET_KEY=masukkan-kunci-acak-panjang-di-sini
   MAX_UPLOAD_MB=16
   ```
   *(Tips: Anda bisa membuat SECRET_KEY acak dengan menjalankan `python -c "import secrets; print(secrets.token_hex(32))"`).*

### Langkah 5: Install Dependensi (Requirements)
Ada 2 cara:

#### Cara A: Melalui Menu Python App di hPanel (Paling Mudah)
1. Kembali ke menu **Python** di hPanel.
2. Pada baris aplikasi Anda, temukan bagian **Configuration files** atau tombol **Run Pip Install**.
3. Pilih file `requirements.txt` lalu klik tombol **Run Pip Install**.
4. Tunggu beberapa saat hingga semua library (`Flask`, `cryptography`, `ecdsa`, `numpy`, dll.) selesai diinstall.

#### Cara B: Melalui SSH / Terminal hPanel
1. Aktifkan akses SSH di menu **Advanced > SSH Access**.
2. Buka terminal atau SSH ke akun hosting Anda:
   ```bash
   ssh u123456789@ip_server -p port
   ```
3. Aktifkan virtual environment yang otomatis dibuat oleh Hostinger (hPanel menampilkan command aktivasi di bagian atas menu Python, misalnya):
   ```bash
   source /home/u123456789/virtualenv/kriptografi/3.10/bin/activate
   ```
4. Masuk ke direktori aplikasi dan jalankan pip:
   ```bash
   cd ~/public_html
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

### Langkah 6: Atur Izin Folder (Permissions)
Aplikasi membutuhkan hak akses untuk menyimpan file unggahan dan file enkripsi sementara:
- Klik kanan folder `uploaded_files` di File Manager > **Permissions** > ubah menjadi `755` (atau `775`).
- Lakukan hal yang sama untuk folder `signed_files`.

### Langkah 7: Restart Aplikasi
1. Di menu **Python** hPanel, klik tombol **Restart** pada aplikasi Anda.
2. Buka domain Anda di browser (`https://domainanda.com`). Aplikasi Anda sekarang sudah online!

---

## OPSI 2: Hostinger VPS (Virtual Private Server - Ubuntu / Debian)

Jika Anda menyewa paket VPS Hostinger (KVM VPS), Anda memiliki akses root penuh. Ini adalah cara standar industri menggunakan **Gunicorn** dan **Nginx**.

### Langkah 1: Update Server & Install Paket Dasar
Hubungkan ke VPS via SSH (`ssh root@ip_vps_anda`):
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip python3-venv git nginx
```

### Langkah 2: Clone atau Upload Proyek
```bash
sudo mkdir -p /var/www/kriptografi
cd /var/www/kriptografi

# Anda bisa git clone atau upload file ke direktori ini:
git clone https://github.com/muhavan/kriptografi.git .
```

### Langkah 3: Setup Virtual Environment & Install Dependensi
```bash
# Buat virtual environment Linux
python3 -m venv venv

# Aktifkan virtual environment
source venv/bin/activate

# Install dependensi
pip install --upgrade pip
pip install -r requirements.txt
```

### Langkah 4: Setup Environment Variables
```bash
cp .env.example .env
nano .env
```
Isi dengan konfigurasi production:
```ini
FLASK_ENV=production
FLASK_DEBUG=0
SECRET_KEY=kunci-rahasia-produksi-anda
MAX_UPLOAD_MB=16
```

### Langkah 5: Atur Hak Akses Folder
```bash
sudo chown -R www-data:www-data /var/www/kriptografi
sudo chmod -R 775 /var/www/kriptografi/uploaded_files
sudo chmod -R 775 /var/www/kriptografi/signed_files
```

### Langkah 6: Buat Systemd Service (Gunicorn)
Buat file service agar aplikasi berjalan otomatis di background dan auto-restart jika server reboot:
```bash
sudo nano /etc/systemd/system/kriptografi.service
```
Tempelkan konfigurasi berikut:
```ini
[Unit]
Description=Gunicorn instance to serve Kriptografi Flask App
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/kriptografi
Environment="PATH=/var/www/kriptografi/venv/bin"
ExecStart=/var/www/kriptografi/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:5000 wsgi:app

Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

Nyalakan service:
```bash
sudo systemctl daemon-reload
sudo systemctl start kriptografi
sudo systemctl enable kriptografi
sudo systemctl status kriptografi
```

### Langkah 7: Konfigurasi Nginx Reverse Proxy
Buat file konfigurasi Nginx:
```bash
sudo nano /etc/nginx/sites-available/kriptografi
```
Tempelkan konfigurasi berikut (ganti `domainanda.com` dengan nama domain Anda):
```nginx
server {
    listen 80;
    server_name domainanda.com www.domainanda.com;

    client_max_body_size 20M;

    # Static assets dilayani langsung oleh Nginx untuk kecepatan optimal
    location /static/ {
        alias /var/www/kriptografi/static/;
        expires 30d;
        add_header Cache-Control "public, no-transform";
    }

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Aktifkan konfigurasi dan restart Nginx:
```bash
sudo ln -s /etc/nginx/sites-available/kriptografi /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Langkah 8: Pasang SSL Gratis (Let's Encrypt / HTTPS)
```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d domainanda.com -d www.domainanda.com
```

---

## 🛠️ Panduan Troubleshooting

1. **Error 500 Internal Server Error di hPanel:**
   - Cek log error di File Manager pada folder root aplikasi, cari file `stderr.log` atau buka menu **Access/Error Logs** di hPanel.
   - Pastikan startup file di hPanel sudah diisi `passenger_wsgi.py` dan Entry Point adalah `application`.
   - Pastikan semua dependensi di `requirements.txt` sudah terinstall di virtual environment.

2. **Error "No module named '...'":**
   - Artinya salah satu library belum terinstall. Jalankan `pip install -r requirements.txt` di dalam virtual environment.

3. **Error "Permission Denied" saat upload file:**
   - Periksa izin folder `uploaded_files` dan `signed_files`. Pastikan permission-nya `755` atau `775`.

4. **Gambar atau Favicon tidak muncul:**
   - Pastikan folder `static/images/` ada dan berisi `favicon.ico`, `favicon.png`, `kriptografi.png`.
