# LAPORAN ARSITEKTUR & ALUR KERJA APLIKASI
## B6 NEWS SCRAPPER (PROYEK WEB SCRAPING - KELOMPOK B6)

---

### 1. PENDAHULUAN
Aplikasi **B6 News Scrapper** adalah perangkat lunak berbasis Desktop yang dirancang untuk melakukan ekstraksi data berita secara otomatis dari berbagai portal berita digital. Aplikasi ini dikembangkan menggunakan bahasa pemrograman **Python** dengan antarmuka grafis (**GUI**) berbasis **PyQt6**. Keunggulan utama aplikasi ini adalah kemampuannya melakukan scraping secara *general* (Heuristic) tanpa terpaku pada satu struktur website spesifik.

### 2. ARSITEKTUR SISTEM
Aplikasi menggunakan pola desain modular yang memisahkan tanggung jawab antara antarmuka, logika robot, dan penyimpanan data:

*   **Antarmuka (Frontend):** Menggunakan **PyQt6** dengan desain modern (Slate-Emerald Theme). Dilengkapi dengan fitur *Interactive Table* yang mendukung *Double-Click to Open* untuk memudahkan validasi data oleh pengguna.
*   **Engine Scraper (Backend):** 
    *   **Selenium:** Bertindak sebagai *driver* browser otomatis untuk menangani rendering JavaScript pada portal berita modern.
    *   **BeautifulSoup4:** Digunakan untuk melakukan *parsing* dokumen HTML yang telah dirender oleh Selenium guna mencari pola data (Heuristic Parsing).
*   **Penyimpanan Data (Data Layer):**
    *   **SQLite3:** Database relasional lokal untuk menyimpan data hasil scraping secara permanen agar tidak hilang saat aplikasi ditutup.
    *   **Pandas:** Digunakan untuk pengolahan data tabel dan melakukan ekspor data ke format **Excel (.xlsx)**.
*   **Concurrency:** Menggunakan **QThread** untuk menjalankan proses scraping di latar belakang (*Background Thread*), sehingga UI tetap responsif (tidak *freeze*) selama proses pengambilan data berlangsung.

### 3. ALUR KERJA (WORKFLOW) SCRAPING
Proses ekstraksi data pada B6 News Scrapper mengikuti alur berikut:

1.  **Input Pengguna:** User memasukkan URL target (Homepage/Kategori), limit jumlah berita, dan rentang tanggal (Start - End Date).
2.  **Inisialisasi Thread:** Saat tombol "START SCRAPING" diklik, aplikasi memicu `ScraperThread`.
3.  **Discovery (Link Harvesting):** Robot Selenium membuka URL target dan mencari pola link berita secara otomatis menggunakan metode *Heuristic URL Pattern* (mencari URL yang mengandung pola `/read/`, `/article/`, atau pola tanggal).
4.  **Extraction (Data Scraping):** Untuk setiap link yang ditemukan:
    *   Robot membuka link artikel tersebut.
    *   Melakukan ekstraksi **Judul** (dari Meta Tags/H1).
    *   Melakukan ekstraksi **Tanggal** (dari Meta Published Time).
    *   Melakukan ekstraksi **Isi Berita** (dari tag Article/Div dengan paragraf terbanyak).
5.  **Filtering & Validation:** Sistem memverifikasi apakah tanggal berita masuk ke dalam rentang yang diminta user. Jika ya, data dianggap valid.
6.  **Persistence:** Data valid disimpan ke **SQLite** menggunakan perintah `INSERT OR IGNORE` untuk mencegah duplikasi data (URL unik).
7.  **UI Update:** Sistem mengirimkan sinyal ke UI untuk memperbarui tabel secara *real-time* dan menggerakkan *Progress Bar*.
8.  **Finalization:** Setelah limit tercapai, driver Selenium ditutup secara otomatis untuk membebaskan memori.

### 4. FITUR NILAI TAMBAH (OPTIONAL)
*   **General Heuristic:** Tidak terpaku pada satu website (bisa digunakan di Kompas, Detik, Tempo, dsb).
*   **Date Range Filtering:** Memungkinkan riset berita pada periode waktu tertentu.
*   **Excel Export:** Konversi database lokal ke file laporan profesional.
*   **Modern Vampire/Emerald UI:** User experience yang nyaman dan estetik.
*   **Error Handling:** Penanganan otomatis jika koneksi terputus atau link tidak valid.

---
*Dibuat oleh Kelompok B6 - Maret 2026*
