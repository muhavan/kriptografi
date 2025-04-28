### Aplikasi Enkripsi File Hybrid

Aplikasi Enkripsi File Hybrid adalah solusi keamanan data yang menggabungkan kekuatan dari beberapa algoritma kriptografi untuk memberikan perlindungan maksimal terhadap file-file penting Anda. Dengan mengkombinasikan algoritma enkripsi simetris (AES-256) dan asimetris (RSA dan ECC), aplikasi ini menawarkan keamanan berlapis yang sulit untuk dibobol.

## Daftar Isi

- [Fitur Utama](#fitur-utama)
- [Teknologi yang Digunakan](#teknologi-yang-digunakan)
- [Persyaratan Sistem](#persyaratan-sistem)
- [Instalasi](#instalasi)



- [Keamanan](#keamanan)
- [Lisensi](#lisensi)
- [Kontak](#kontak)


Enkripsi hybrid mengatasi keterbatasan dari masing-masing jenis enkripsi:

- **Enkripsi simetris** (AES): Cepat dan efisien untuk file besar, tetapi memiliki tantangan dalam pertukaran kunci
- **Enkripsi asimetris** (RSA, ECC): Aman untuk pertukaran kunci, tetapi lambat untuk file besar


Dengan menggabungkan keduanya, aplikasi ini memberikan keamanan optimal dan kinerja yang baik.

## Fitur Utama

- **Enkripsi File Hybrid**: Mengenkripsi file menggunakan AES-256 dengan kunci yang dilindungi oleh RSA
- **Tanda Tangan Digital Ganda**: Menggunakan RSA dan ECC untuk memverifikasi keaslian dan integritas file
- **Verifikasi Integritas**: Memastikan file tidak diubah setelah dienkripsi
- **Antarmuka Web yang Intuitif**: Mudah digunakan tanpa pengetahuan teknis yang mendalam
- **Mendukung Berbagai Format File**: Dapat mengenkripsi berbagai jenis file (gambar, dokumen, teks, dll.)
- **Mode Gelap/Terang**: Antarmuka yang nyaman untuk berbagai kondisi pencahayaan


## Teknologi yang Digunakan

- **Backend**:

- Python 3.7+
- Flask (Web framework)
- Cryptography (Library untuk enkripsi RSA dan AES)
- ECDSA (Library untuk tanda tangan digital berbasis kurva eliptik)
- Hashlib (Library untuk fungsi hash)
- Pillow (Untuk pemrosesan gambar)
- NumPy (Untuk operasi matematika)



- **Frontend**:

- HTML5
- CSS3 (dengan Tailwind CSS)
- JavaScript (Vanilla JS)





## Persyaratan Sistem

- Python 3.7 atau lebih baru
- Pip (Python package manager)
- Browser web modern (Chrome, Firefox, Safari, Edge)
- Minimal 512MB RAM
- 100MB ruang disk kosong


## Instalasi

### Metode 1: Instalasi Standar

1. Clone repositori ini atau download sebagai ZIP dan ekstrak:

```shellscript
git clone https://github.com/muhavan/kriptografi.git
cd enkripsi-file-hybrid
```


2. Buat virtual environment (sangat direkomendasikan):

```shellscript
python -m venv venv
```


3. Aktifkan virtual environment:

1. Windows:

```shellscript
venv\Scripts\activate
```


2. macOS/Linux:

```shellscript
source venv/bin/activate
```





4. Install dependensi:

```shellscript
pip install -r requirements.txt
```


5. Jalankan aplikasi:

```shellscript
python app.py
```


6. Buka browser dan akses `http://127.0.0.1:5000/`


### Metode 2: Menggunakan Docker

1. Pastikan Docker sudah terinstal di sistem Anda
2. Build image Docker:

```shellscript
docker build -t enkripsi-file-hybrid .
```


3. Jalankan container:

```shellscript
docker run -p 5000:5000 enkripsi-file-hybrid
```


4. Buka browser dan akses `http://localhost:5000/`


## Penggunaan

### Mengenkripsi File

1. Buka halaman "Enkripsi Hybrid" dari menu navigasi
2. Klik tombol "Hasilkan Pasangan Kunci RSA & ECC" untuk membuat kunci baru

**Penting**: Simpan kunci privat RSA yang dihasilkan di tempat yang aman, Anda akan membutuhkannya untuk dekripsi


## Keamanan

### Kekuatan Algoritma

- **AES-256**: Standar enkripsi simetris yang diakui secara global, dengan panjang kunci 256-bit yang dianggap sangat aman
- **RSA-2048**: Algoritma enkripsi asimetris dengan panjang kunci 2048-bit, memberikan keamanan yang kuat untuk enkripsi kunci
- **ECC (NIST P-256)**: Algoritma kurva eliptik yang menawarkan keamanan setara dengan RSA tetapi dengan kunci yang lebih pendek

### Area yang Membutuhkan Kontribusi

- Peningkatan UI/UX
- Optimasi kinerja untuk file besar
- Penambahan fitur enkripsi batch
- Peningkatan manajemen kunci
- Penambahan dukungan untuk lebih banyak format file
- Penerjemahan ke bahasa lain


## Lisensi

Proyek ini dilisensikan ©17.6A.27.

Dibuat dengan ❤️ oleh Tim Pengembang Enkripsi File Hybrid