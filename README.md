# Aplikasi Web Kriptografi

Aplikasi web ini mendemonstrasikan berbagai teknik kriptografi termasuk enkripsi simetris, asimetris, tanda tangan hybrid, hashing, dan sandi Caesar. Aplikasi ini dibuat menggunakan Python dan Flask.

## Persyaratan

Untuk menjalankan aplikasi ini, Anda memerlukan:

- Python 3.7 atau lebih baru
- Pip (Python package manager)
- Semua dependensi yang tercantum dalam `requirements.txt`

## Instalasi

1. Clone repositori ini atau download sebagai ZIP dan ekstrak
2. Buka terminal dan navigasi ke direktori proyek
3. Buat virtual environment (opsional tapi direkomendasikan):
   \`\`\`
   python -m venv venv
   \`\`\`
4. Aktifkan virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`
5. Install dependensi:
   \`\`\`
   pip install -r requirements.txt
   \`\`\`

## Menjalankan Aplikasi

1. Pastikan Anda berada di direktori proyek dan virtual environment aktif
2. Jalankan aplikasi:
   \`\`\`
   python app.py
   \`\`\`
3. Buka browser dan akses `http://127.0.0.1:5000/`

## Fitur Utama

### 1. Enkripsi Simetris

Enkripsi simetris menggunakan kunci yang sama untuk enkripsi dan dekripsi data.

- Buka halaman Enkripsi Simetris
- Klik "Buat Kunci" untuk menghasilkan kunci Fernet
- Masukkan pesan yang ingin dienkripsi
- Klik "Enkripsi" untuk mengenkripsi pesan
- Untuk mendekripsi, masukkan teks terenkripsi dan kunci, lalu klik "Dekripsi"

### 2. Enkripsi Asimetris

Enkripsi asimetris menggunakan sepasang kunci (publik dan privat) untuk komunikasi yang aman.

- Buka halaman Enkripsi Asimetris
- Klik "Buat Pasangan Kunci" untuk menghasilkan kunci RSA
- Untuk enkripsi, masukkan pesan dan gunakan kunci publik
- Untuk dekripsi, masukkan teks terenkripsi dan gunakan kunci privat

### 3. Tanda Tangan Hybrid

Tanda tangan hybrid mengkombinasikan RSA dan ECC untuk keamanan tinggi.

#### Menandatangani Dokumen:
1. Buka halaman Tanda Tangan Hybrid
2. Klik "Buat Pasangan Kunci RSA & ECC"
3. Pilih dokumen yang ingin ditandatangani
4. Klik "Tandatangani Dokumen"
5. Download file metadata dan dokumen terenkripsi

#### Verifikasi Dokumen:
1. Buka tab "Verifikasi Dokumen"
2. Upload dokumen terenkripsi
3. Upload file metadata
4. Klik "Verifikasi Dokumen"
5. Sistem akan menampilkan hasil verifikasi

### 4. Hashing

Hashing mengubah data menjadi string dengan ukuran tetap.

- Buka halaman Hashing
- Masukkan pesan yang ingin di-hash
- Pilih algoritma hash (MD5, SHA-1, SHA-256, SHA-512)
- Klik "Hasilkan Hash"

### 5. Sandi Caesar

Sandi Caesar adalah teknik enkripsi klasik yang menggeser huruf dalam alfabet.

- Buka halaman Sandi Caesar
- Masukkan pesan
- Atur nilai pergeseran (1-25)
- Klik "Enkripsi" atau "Dekripsi"

## Teknologi yang Digunakan

- **Python**: Bahasa pemrograman utama
- **Flask**: Web framework
- **Cryptography**: Library untuk enkripsi simetris dan asimetris
- **ECDSA**: Library untuk tanda tangan digital berbasis kurva eliptik
- **Hashlib**: Library untuk fungsi hash
- **QRCode**: Library untuk menghasilkan QR code
- **OpenCV & pyzbar**: Library untuk membaca QR code
- **Tailwind CSS**: Framework CSS untuk styling

## Catatan Keamanan

Aplikasi ini dibuat untuk tujuan pendidikan dan demonstrasi. Beberapa catatan keamanan:

- Jangan gunakan kunci yang dihasilkan untuk data sensitif di lingkungan produksi
- MD5 dan SHA-1 dianggap tidak aman untuk aplikasi kriptografi modern
- Sandi Caesar sangat mudah dipecahkan dan tidak boleh digunakan untuk keamanan nyata
- Dalam aplikasi nyata, kunci privat harus disimpan dengan aman dan tidak boleh dibagikan

## Lisensi

Proyek ini dilisensikan di bawah MIT License.
