import unittest
import os
import sqlite3
from datetime import datetime
from scraper import NewsScraper
from database import NewsDatabase

class TestB6Scraper(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Siapkan environment testing."""
        cls.test_db_name = "B6_PyQt_Full/test_b6.db"
        cls.db = NewsDatabase(cls.test_db_name)
        cls.scraper = NewsScraper(headless=True)
        cls.target_url = "https://www.kompas.com/"

    @classmethod
    def tearDownClass(cls):
        """Bersihkan file setelah tes selesai."""
        if os.path.exists("B6_PyQt_Full/test_b6.db"):
            try:
                os.remove("B6_PyQt_Full/test_b6.db")
            except:
                pass
        cls.scraper.stop_driver()

    def test_01_database_creation(self):
        """Uji apakah tabel database berhasil dibuat."""
        conn = sqlite3.connect("B6_PyQt_Full/test_b6.db")
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='articles'")
        table_exists = cursor.fetchone()
        conn.close()
        self.assertIsNotNone(table_exists, "Tabel 'articles' harus ada di database.")

    def test_02_get_links(self):
        """Uji apakah scraper bisa mendapatkan link dari homepage."""
        links = self.scraper.get_links(self.target_url, limit=2)
        self.assertIsInstance(links, list)
        self.assertGreater(len(links), 0, "Harus menemukan minimal 1 link berita.")

    def test_03_scrape_article_content(self):
        """Uji ekstraksi konten dari satu link berita."""
        links = self.scraper.get_links(self.target_url, limit=1)
        if links:
            data = self.scraper.scrape_article(links[0])
            self.assertIn('title', data)
            self.assertIn('content', data)
            self.assertNotEqual(data['title'], "No Title")

    def test_04_database_save_and_filter(self):
        """Uji simpan data dan filter tanggal di database."""
        test_data = {
            "url": "https://test.com/news-unique-123",
            "title": "Berita Tes Unit",
            "date": "2026-03-07",
            "content": "Konten tes."
        }
        self.db.save_article(test_data)
        df = self.db.get_filtered_articles("2026-03-01", "2026-03-30")
        self.assertGreater(len(df), 0)

if __name__ == "__main__":
    unittest.main()
