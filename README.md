# 🚀 B6 NEWS SCRAPER PRO - PANDUAN TIM

Gunakan panduan ini agar pengerjaan lancar. Baca pelan-pelan ya, guys!

---

## 🛑 Step 0: Syarat Wajib (Sebelum Mulai)
Pastikan laptop kalian sudah punya dua barang ini:
1.  **Python 3.10 ke atas:** Pas instal, **WAJIB CENTANG** kotak "Add Python to PATH".
2.  **Google Chrome:** Versi terbaru. (Kita pake Selenium, jadi butuh Chrome).

---

## 🛠️ Step 1: Persiapan (Cara Install Library)

1.  **Buka Terminal di Folder Ini:**
    *   Buka folder `B6_PyQt` di File Explorer.
    *   Klik kanan di area kosong sambil tekan tombol **Shift** di keyboard.
    *   Pilih **"Open PowerShell window here"** atau **"Open in Terminal"**.

2.  **Install Amunisi (Library):**
    Ketik perintah ini di terminal, lalu Enter:
    ```
    pip install -r requirements.txt
    ```

---

## ❓ Solusi Jika Ada Error (Troubleshooting)

**1. Muncul Error: "pip is not recognized"**
*   **Artinya:** Python belum masuk ke PATH Windows kalian.
*   **Solusi:** Coba ganti perintahnya jadi:
    ```
    python -m pip install -r requirements.txt
    ```
    Atau:
    ```
    py -m pip install -r requirements.txt
    ```

**2. Muncul Error: "Python was not found"**
*   **Solusi:** Kalian harus install ulang Python dan pastikan centang **"Add Python to PATH"** saat di awal instalasi.

---

## 📜 PERJANJIAN DATA (KONTRAK WAJIB)
Biar program kita nggak crash pas digabungin, semua data berita **WAJIB** pake format ini:

**Satu Berita = Dictionary**
```python
{
    "url": "https://...",      # Wajib Teks (String)
    "title": "Judul Berita",   # Wajib Teks (String)
    "date": date_object,       # Wajib Objek datetime.date (Bukan Teks!)
    "content": "Isi berita..." # Wajib Teks (String)
}
```

---

## 👥 SIAPA KERJAIN APA?
Gue (Arya) udah nyiapin "rumah" masing-masing. Kalian cuma boleh edit bagian yang ada tanda `# TODO`:

1.  **Lead Dev (Arya):** Integrasi `main.py` dan bantu kalian kalau mentok.
2.  **Backend Specialist:** Fokus di `scraper.py` (Bikin robot Selenium).
3.  **Frontend Designer:** Fokus di `styles.qss` dan `main.py` bagian `init_ui`.
4.  **Data Engineer:** Fokus di `database.py` (SQLite & Ekspor Excel).
5.  **QA Engineer:** Fokus di `test_scraper.py` (Tes kualitas kerjaan Backend).

---

## 🏃‍♂️ Cara Menjalankan Aplikasi
Kalau semua sudah siap, ketik:
```
python main.py
```
*(Kalau gagal, coba `py main.py`)*

---
**Semangat,Gusy**
