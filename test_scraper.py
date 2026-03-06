import unittest
import datetime
from scraper import NewsScraper

class TestB6Scraper(unittest.TestCase):
    """
    TUGAS QA & AUTOMATION ENGINEER:
    Lengkapi logika pengujian di bawah ini untuk memastikan mesin Scraper 
    milik Backend tidak memiliki celah error (Bug).
    """

    def setUp(self):
        # Inisialisasi sebelum tiap tes dimulai
        self.scraper = NewsScraper(headless=True)

    def tearDown(self):
        # Tutup browser setelah tiap tes selesai
        self.scraper.stop_driver()

    # --- 1. PENGUJIAN KONTRAK DATA ---
    def test_data_structure(self):
        """TES: Pastikan Dictionary hasil scrape punya 4 kunci wajib & tipe data benar."""
        # TODO: Panggil scrape_article() dan cek kunci: url, title, date, content.
        pass

    # --- 2. PENGUJIAN LOGIKA TANGGAL ---
    def test_date_parsing_indonesian(self):
        """TES: Pastikan format '10 Maret 2026' berubah jadi objek Date beneran."""
        # TODO: Masukkan teks Indo, cek apakah hasilnya datetime.date(2026, 3, 10).
        pass

    def test_date_parsing_english(self):
        """TES: Pastikan format 'March 10, 2026' juga bisa terbaca."""
        # TODO: Masukkan teks Inggris, cek apakah hasilnya datetime.date(2026, 3, 10).
        pass

    def test_date_parsing_relative(self):
        """TES: (Tantangan) Pastikan teks '2 jam yang lalu' bisa dikonversi ke tanggal hari ini."""
        # TODO: Masukkan teks relatif, cek apakah hasilnya date.today().
        pass

    # --- 3. PENGUJIAN PENGAMBILAN LINK ---
    def test_link_extraction_is_list(self):
        """TES: Pastikan get_article_links mengembalikan List, bukan string atau None."""
        # TODO: Cek tipe data kembalian dari fungsi get_article_links.
        pass

    def test_link_limit_precision(self):
        """TES: Pastikan jika diminta 3 link, yang dikasih beneran cuma 3 link."""
        # TODO: Panggil fungsi dengan limit=3, cek len(hasil) == 3.
        pass

    # --- 4. PENGUJIAN ERROR HANDLING (STRESS TEST) ---
    def test_invalid_url_handling(self):
        """TES: Pastikan aplikasi tidak CRASH jika dikasih URL yang salah/ngawur."""
        # TODO: Masukkan URL 'bukan-url', pastikan program tidak berhenti mendadak.
        pass

    def test_empty_page_handling(self):
        """TES: Pastikan aplikasi tetap aman jika membuka halaman yang tidak ada beritanya."""
        # TODO: Tes pada halaman kosong, pastikan kembaliannya list kosong [].
        pass

if __name__ == '__main__':
    unittest.main()
