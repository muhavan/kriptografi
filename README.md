### Aplikasi Enkripsi File Hybrid

Aplikasi Enkripsi File Hybrid adalah solusi keamanan data yang menggabungkan kekuatan dari beberapa algoritma kriptografi untuk memberikan perlindungan maksimal terhadap file-file penting Anda. Dengan mengkombinasikan algoritma enkripsi simetris (AES-256) dan asimetris (RSA dan ECC), aplikasi ini menawarkan keamanan berlapis yang sulit untuk dibobol.

![screen](/images/kriptografi.png)

## Teknologi yang Digunakan

- **Backend**:

- Python 3.7+
- Flask (Web framework)
- Cryptography (Library untuk enkripsi RSA dan AES)
- ECDSA (Library untuk enkripsi file digital berbasis kurva eliptik)
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

## Lisensi

Proyek ini dilisensikan ©17.6A.27.

Dibuat dengan ❤️ oleh Tim Pengembang Enkripsi File Hybrid