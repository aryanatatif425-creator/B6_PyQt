# LAPORAN ARSITEKTUR & ALUR KERJA APLIKASI
## B6 NEWS SCRAPPER (PROYEK WEB SCRAPING - KELOMPOK B6)

---

### 1. PENDAHULUAN
Aplikasi **B6 News Scrapper** adalah perangkat lunak berbasis Desktop yang dirancang untuk melakukan ekstraksi data berita secara otomatis dari berbagai portal berita digital. Aplikasi ini dikembangkan menggunakan bahasa pemrograman **Python** dengan antarmuka grafis (**GUI**) berbasis **PyQt6**. Keunggulan utama aplikasi ini adalah kemampuannya melakukan scraping secara *general* (Heuristic) tanpa terpaku pada satu struktur website spesifik.

### 2. ARSITEKTUR SISTEM
Aplikasi menggunakan pola desain modular yang memisahkan tanggung jawab antara antarmuka, logika robot, dan penyimpanan data:

*   **Antarmuka (Frontend):** Menggunakan **PyQt6** dengan desain modern (Blue-Green Emerald Theme). Dilengkapi dengan fitur *Interactive Table* yang mendukung *Double-Click to Open* untuk memudahkan validasi data oleh pengguna.
*   **Engine Scraper (Backend):** 
    *   **Selenium:** Bertindak sebagai *driver* browser otomatis untuk menangani rendering JavaScript pada portal berita modern.
    *   **BeautifulSoup4:** Digunakan untuk melakukan *parsing* dokumen HTML yang telah dirender oleh Selenium guna mencari pola data (Heuristic Parsing).
*   **Penyimpanan Data (Data Layer):**
    *   **SQLite3:** Database relasional lokal untuk menyimpan data hasil scraping secara permanen.
    *   **Pandas:** Digunakan untuk pengolahan data tabel dan melakukan ekspor data ke format **Excel (.xlsx)**.
*   **Concurrency:** Menggunakan **QThread** untuk menjalankan proses scraping di latar belakang (*Background Thread*), sehingga UI tetap responsif selama proses pengambilan data berlangsung.

### 3. ALUR KERJA (WORKFLOW) SCRAPING
Proses ekstraksi data pada B6 News Scrapper mengikuti alur berikut:

1.  **Input Pengguna:** User memasukkan URL target, limit berita, dan rentang tanggal (Start - End Date).
2.  **Inisialisasi Thread:** Aplikasi memicu `ScraperThread` di background.
3.  **Discovery (Link Harvesting):** Robot Selenium mencari pola link berita secara otomatis menggunakan metode *Heuristic URL Pattern*.
4.  **Extraction (Data Scraping):** Robot membuka link artikel, mengambil Judul, Tanggal, dan Isi Berita secara cerdas.
5.  **Filtering & Validation:** Sistem memverifikasi rentang tanggal yang diminta.
6.  **Persistence:** Data valid disimpan ke **SQLite** dengan proteksi duplikasi data (URL unik).
7.  **UI Update:** Tabel dan Progress Bar diperbarui secara real-time.
8.  **Finalization:** Driver ditutup dan memori dibebaskan setelah proses selesai.

---
*Dibuat oleh Kelompok B6 - Maret 2026*
