# Panduan Hosting Aplikasi Kriptografi Hybrid di Hostinger (Versi Statis Murni)

Aplikasi **Kriptografi File Hybrid** ini sekarang telah dikonversi menjadi **Aplikasi Web Statis Murni (100% Client-Side)**.

### 🌟 Keunggulan Versi Statis:
1. **Bisa Dihosting di Semua Paket Hostinger** (Single, Premium, Business, Cloud, maupun VPS) tanpa memerlukan server Python/Node.js sama sekali.
2. **Keamanan Tertinggi (Zero-Knowledge Privacy)**: File dan kunci privat diproses langsung di memori browser pengguna via **Web Cryptography API** bawaan browser. Tidak ada data yang dikirim ke server.
3. **Kecepatan Instan**: Enkripsi dan dekripsi berkas berjalan dalam hitungan milidetik secara lokal di komputer pengguna.
4. **Bisa Langsung Di-deploy via Git Onboarding Hostinger** (file `package.json` sudah disediakan).

---

## 📁 Struktur File Proyek Statis

```text
kriptografi/
├── index.html              # Halaman Beranda & Visualisasi Arsitektur
├── hybrid-encription.html  # Studio Enkripsi, Verifikasi & Dekripsi Berkas
├── package.json            # Konfigurasi otomatis untuk Git Deployment Hostinger
├── static/
│   ├── css/
│   │   └── style.css       # Design System & Styling Responsif
│   ├── js/
│   │   ├── crypto-engine.js # Mesin Kriptografi Client-Side (AES-256, RSA, ECC, SHA-256)
│   │   ├── translations.js  # Mesin Bilingual (Indonesia & Inggris)
│   │   └── main.js          # Utilitas UI (Drag-Drop, Toast, Copy, Download)
│   └── images/
│       ├── favicon.ico
│       ├── favicon.png
│       └── kriptografi.png
└── README.md
```

---

## CARA DEPLOY KE HOSTINGER

Terdapat 2 cara mudah untuk mengonlinekan website ini di Hostinger:

### METODE 1: Langsung Pakai Fitur Git Onboarding di Hostinger (Paling Direkomendasikan)

Jika Anda sudah menghubungkan akun GitHub Anda ke Hostinger seperti pada screenshot:
1. **Push pembaruan kode ini ke GitHub Anda**:
   Buka terminal di komputer Anda, jalankan:
   ```bash
   git add .
   git commit -m "Convert to 100% client-side static web app"
   git push origin main
   ```
2. **Buka kembali layar Hostinger Git Onboarding**:
   - Refresh halaman Hostinger yang tadi menampilkan peringatan `package.json`.
   - Karena file `package.json`, `index.html`, dan `hybrid-encription.html` sudah tersedia, Hostinger akan mendeteksinya secara otomatis.
3. Klik tombol **Deploy** / **Selanjutnya**.
4. Website Anda langsung aktif dan live di domain Hostinger Anda!

---

### METODE 2: Upload Manual via File Manager Hostinger (Alternatif Cepat)

Jika Anda ingin langsung mengunggahnya tanpa Git:
1. Di komputer lokal Anda, buat file **ZIP** yang berisi:
   - `index.html`
   - `hybrid-encription.html`
   - `package.json`
   - Folder `static/` (beserta isinya: `css/`, `js/`, `images/`)
2. Buka [Hostinger hPanel](https://hpanel.hostinger.com/).
3. Masuk ke menu **Websites** > klik **Manage** pada domain Anda.
4. Buka menu **File Manager** (atau cari "File Manager").
5. Masuk ke folder **`public_html`**.
6. Klik tombol **Upload** di pojok kanan atas, lalu upload file ZIP Anda.
7. Klik kanan pada file ZIP di File Manager, lalu pilih **Extract**.
8. Pastikan file `index.html`, `hybrid-encription.html`, dan folder `static/` berada langsung di dalam folder `public_html` (bukan di dalam subfolder lagi).
9. Buka domain Anda di browser (misalnya `https://domainanda.com`). Website langsung aktif dan siap digunakan!

---

## 🔒 Uji Coba Fungsi Kriptografi Setelah Online:
1. Buka halaman **Studio Enkripsi** (`/hybrid-encription.html`).
2. Klik tombol **"Generate Kunci Otomatis"** untuk membuat kunci privat RSA-2048 & ECC NIST-P256.
3. Tarik berkas apa saja (gambar, dokumen, PDF) ke dalam dropzone.
4. Klik **"Enkripsi & Tandatangani Berkas"**.
5. Unduh kedua file yang dihasilkan: `encrypted_<nama_file>.bin` dan `metadata_<nama_file>.json`.
6. Buka tab **Verifikasi Integritas** untuk membuktikan keaslian dokumen.
7. Buka tab **Dekripsi Dokumen** untuk membuka kembali dokumen asli dengan kunci privat RSA Anda.
