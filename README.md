# B6 News Scrapper Pro

Aplikasi Desktop berbasis **Python** untuk melakukan scraping berita secara otomatis dari berbagai portal berita digital menggunakan **Selenium** dan **BeautifulSoup4**. Dirancang dengan antarmuka **PyQt6** yang modern dan responsif.

---

## Fitur Utama

- **General Heuristic Scraper**: Mampu mengekstraksi data dari berbagai portal berita (Kompas, Detik, Tempo, dll.) secara otomatis tanpa konfigurasi khusus per website.
- **Date Range Filtering**: Fitur filter berita berdasarkan rentang tanggal tertentu (Start Date - End Date).
- **Multi-threaded Processing**: Proses scraping berjalan di latar belakang (*background thread*), sehingga aplikasi tetap responsif dan tidak *freeze*.
- **Interactive Results Table**: Menampilkan hasil secara real-time. Klik dua kali (**Double-Click**) pada baris tabel untuk membuka artikel di browser.
- **Excel Export**: Menyimpan hasil scraping langsung ke format file **.xlsx** (Excel).
- **Automated Logging**: Dilengkapi dengan status log dan *progress bar* untuk memantau proses scraping.
- **Unit Testing Ready**: Tersedia skrip pengujian otomatis untuk memastikan keandalan sistem.

---

## Prasyarat (Prerequisites)

Sebelum menjalankan aplikasi, pastikan sistem Anda memiliki:
1. **Python 3.8** atau versi yang lebih baru.
2. **Google Chrome Browser** (Versi terbaru).
3. Koneksi internet yang stabil.

---

## Panduan Instalasi

1. **Clone/Download Proyek**: Unduh seluruh isi folder ini.
2. **Instal Dependensi**: Buka terminal/CMD di folder proyek dan jalankan perintah:
   ```bash
   pip install -r requirements.txt
   ```

---

## Cara Penggunaan

1. **Jalankan Aplikasi**:
   ```bash
   python main.py
   ```
2. **Input URL Target**: Masukkan link utama berita (Homepage atau halaman Kategori).
3. **Set Limit**: Tentukan berapa banyak link berita yang ingin dicari (Default: 10).
4. **Set Filter Tanggal**: Pilih rentang tanggal berita yang ingin diambil.
5. **Mulai Scraping**: Klik tombol **"START SCRAPING"**.
6. **Buka Artikel**: Klik dua kali pada baris di tabel untuk membaca berita di browser.
7. **Ekspor Data**: Klik tombol **"EXPORT EXCEL"** untuk menyimpan semua data hasil filter ke file Excel.

---

## Pengujian Sistem (Testing)

Untuk memastikan semua modul (Scraper, Database, dan Driver) berfungsi dengan baik di perangkat Anda, jalankan perintah:
```bash
python test_scraper.py
```

---

##  Struktur Proyek

- `main.py`: Kode utama untuk antarmuka GUI dan logika threading.
- `scraper.py`: Mesin pencari berita (Selenium & BeautifulSoup).
- `database.py`: Logika penyimpanan SQLite dan fitur ekspor Excel.
- `styles.qss`: File desain tema (Blue-Green Emerald).
- `test_scraper.py`: Skrip pengujian otomatis (Unit Testing).
- `requirements.txt`: Daftar pustaka Python yang diperlukan.
- `Laporan_Arsitektur.md`: Penjelasan teknis mengenai cara kerja sistem.

---
