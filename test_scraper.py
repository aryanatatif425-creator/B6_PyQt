# test_scraper.py
import unittest
import datetime
from unittest import mock

# Mock driver yang sederhana: menyediakan page_source dan get()
class _MockDriver:
    def __init__(self):
        self.page_source = ""

    def get(self, url):
        # Sesuaikan konten berdasarkan URL agar tests deterministik
        if url.endswith("/") or "main" in url:
            # halaman daftar artikel (3 link)
            self.page_source = """
                <html><body>
                    <a href="http://news.test/article1">Article 1</a>
                    <a href="http://news.test/article2">Article 2</a>
                    <a href="http://news.test/article3">Article 3</a>
                    <!-- pagination contoh -->
                    <a href="http://news.test/?page=2">Next</a>
                </body></html>
            """
        elif "article1" in url:
            self.page_source = """
                <html><body>
                    <h1>Judul Artikel Satu</h1>
                    <time>10 Maret 2026</time>
                    <p>Paragraf pertama isi artikel satu.</p>
                    <p>Paragraf kedua isi artikel satu.</p>
                </body></html>
            """
        elif "article2" in url:
            self.page_source = """
                <html><body>
                    <h1>Article Two Title</h1>
                    <time>March 10, 2026</time>
                    <p>Article two first paragraph.</p>
                </body></html>
            """
        elif "article3" in url:
            # contoh halaman tanpa <h1> / tanpa <p>
            self.page_source = "<html><body>No news here</body></html>"
        else:
            self.page_source = "<html><body>Empty</body></html>"

    # optional: beberapa implementasi scraper mungkin memanggil find_elements
    def find_elements(self, by=None, value=None):
        # kembalikan list kosong agar pemanggilan driver.find_elements tidak crash
        return []

class TestScraperPairedWithProvidedImplementation(unittest.TestCase):
    def setUp(self):
        # import NewsScraper dari file scraper.py
        try:
            from scraper import NewsScraper
        except Exception as e:
            self.skipTest(f"Module 'scraper' or class 'NewsScraper' tidak ditemukan: {e}")

        # buat instance (sesuaikan bila konstruktor beda)
        try:
            self.scraper = NewsScraper(headless=True)
        except TypeError:
            # fallback kalau konstruktor tanpa argumen
            self.scraper = NewsScraper()

        # Ganti start_driver sehingga tidak membuka Chrome sesungguhnya.
        # start_driver() akan meng-assign mock driver ke self.scraper.driver
        def _fake_start_driver():
            self.scraper.driver = _MockDriver()

        # override start_driver method pada instance
        self.scraper.start_driver = _fake_start_driver

    def tearDown(self):
        # panggil stop_driver jika ada untuk kebersihan
        try:
            if hasattr(self.scraper, "stop_driver"):
                self.scraper.stop_driver()
        except Exception:
            pass

    # --- 1. KONTRAK DATA scrape_article ---
    def test_scrape_article_contract(self):
        """Hasil scrape_article(url) harus dict dengan kunci url,title,date,content."""
        if not hasattr(self.scraper, "scrape_article"):
            self.skipTest("Method scrape_article(url) belum diimplementasikan.")

        url = "http://news.test/article1"
        try:
            result = self.scraper.scrape_article(url)
        except NotImplementedError:
            self.skipTest("scrape_article belum diimplementasikan (NotImplementedError).")
        except Exception as e:
            self.fail(f"scrape_article melempar exception saat diuji: {e}")

        self.assertIsInstance(result, dict, "scrape_article harus mengembalikan dict.")
        for k in ("url", "title", "date", "content"):
            self.assertIn(k, result, f"Key '{k}' wajib ada di hasil scrape_article.")

        self.assertIsInstance(result["url"], str)
        self.assertTrue(result["url"], "result['url'] tidak boleh kosong.")
        self.assertIsInstance(result["title"], str, "result['title'] harus string.")
        # date boleh date/datetime/None/str; utamakan date/datetime
        self.assertTrue(
            result["date"] is None
            or isinstance(result["date"], (datetime.date, datetime.datetime, str)),
            "result['date'] harus None, str, date, atau datetime."
        )
        self.assertIsInstance(result["content"], str, "result['content'] harus string.")
        self.assertTrue(result["content"], "result['content'] tidak boleh kosong.")

    # --- 2. PENGUJIAN PENGAMBILAN LINK ---
    def test_get_article_links_returns_list(self):
        """get_article_links harus mengembalikan list URL (tipe list)."""
        if not hasattr(self.scraper, "get_article_links"):
            self.skipTest("Method get_article_links(main_url, limit=...) belum diimplementasikan.")

        try:
            links = self.scraper.get_article_links("http://news.test/")
        except NotImplementedError:
            self.skipTest("get_article_links belum diimplementasikan (NotImplementedError).")
        except Exception as e:
            self.fail(f"get_article_links melempar exception saat diuji: {e}")

        self.assertIsInstance(links, list, "get_article_links harus mengembalikan list.")
        # jika list tidak kosong, pastikan isinya string (URL).
        if links:
            self.assertTrue(all(isinstance(x, str) for x in links),
                            "Semua elemen hasil get_article_links harus string (URL).")

    def test_get_article_links_respects_limit(self):
        """Jika parameter limit diberikan, jumlah link yang dikembalikan <= limit."""
        if not hasattr(self.scraper, "get_article_links"):
            self.skipTest("Method get_article_links(main_url, limit=...) belum diimplementasikan.")

        try:
            links = self.scraper.get_article_links("http://news.test/", limit=2)
        except TypeError:
            # mungkin signature berbeda (mis. positional); coba alternatif
            try:
                links = self.scraper.get_article_links("http://news.test/", 2)
            except Exception as e:
                self.skipTest(f"get_article_links tidak dapat dipanggil dengan limit pada environment ini: {e}")
        except NotImplementedError:
            self.skipTest("get_article_links belum diimplementasikan (NotImplementedError).")
        except Exception as e:
            self.fail(f"get_article_links melempar exception saat diuji: {e}")

        self.assertIsInstance(links, list)
        # hanya cek bahwa panjangnya tidak melebihi limit (jika fungsi mendukung limit)
        self.assertLessEqual(len(links), 2, "Saat meminta limit=2, hasil harus berisi paling banyak 2 link.")

    # --- 3. PENGUJIAN PARSING TANGGAL ---
    def test_parse_date_indonesian(self):
        """parse_date('10 Maret 2026') -> datetime.date(2026,3,10)"""
        if not hasattr(self.scraper, "parse_date"):
            self.skipTest("Method parse_date(text) belum diimplementasikan.")
        src = "10 Maret 2026"
        try:
            out = self.scraper.parse_date(src)
        except NotImplementedError:
            self.skipTest("parse_date belum diimplementasikan (NotImplementedError).")
        except Exception as e:
            self.fail(f"parse_date melempar exception saat diuji: {e}")

        # normalize
        if isinstance(out, datetime.datetime):
            outd = out.date()
        elif isinstance(out, datetime.date):
            outd = out
        else:
            self.fail(f"parse_date harus mengembalikan datetime.date atau datetime.datetime, dapat {type(out)}")

        self.assertEqual(outd, datetime.date(2026, 3, 10),
                         f"parse_date('{src}') harus -> 2026-03-10, dapat {outd}")

    def test_parse_date_english(self):
        """parse_date('March 10, 2026') -> datetime.date(2026,3,10)"""
        if not hasattr(self.scraper, "parse_date"):
            self.skipTest("Method parse_date(text) belum diimplementasikan.")
        src = "March 10, 2026"
        try:
            out = self.scraper.parse_date(src)
        except Exception as e:
            self.fail(f"parse_date melempar exception saat diuji: {e}")

        if isinstance(out, datetime.datetime):
            outd = out.date()
        elif isinstance(out, datetime.date):
            outd = out
        else:
            self.fail(f"parse_date harus mengembalikan datetime.date atau datetime.datetime, dapat {type(out)}")

        self.assertEqual(outd, datetime.date(2026, 3, 10),
                         f"parse_date('{src}') harus -> 2026-03-10, dapat {outd}")

    def test_parse_date_relative_hours(self):
        """parse_date('2 jam yang lalu') -> tanggal hari ini (relative parsing)."""
        if not hasattr(self.scraper, "parse_date"):
            self.skipTest("Method parse_date(text) belum diimplementasikan.")
        src = "2 jam yang lalu"
        try:
            out = self.scraper.parse_date(src)
        except Exception as e:
            self.fail(f"parse_date melempar exception saat diuji: {e}")

        if isinstance(out, datetime.datetime):
            outd = out.date()
        elif isinstance(out, datetime.date):
            outd = out
        else:
            self.fail(f"parse_date harus mengembalikan datetime.date atau datetime.datetime, dapat {type(out)}")

        self.assertEqual(outd, datetime.date.today(),
                         f"parse_date('{src}') relatif harus -> hari ini ({datetime.date.today()}), dapat {outd}")

if __name__ == "__main__":
    unittest.main()