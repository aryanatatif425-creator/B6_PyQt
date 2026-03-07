import time
import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class NewsScraper:
    """
    TUGAS BACKEND SPECIALIST:
    Fokus di file ini untuk mengambil data dari internet.
    """
    def __init__(self, headless=True):
        self.chrome_options = Options()
        if headless: self.chrome_options.add_argument("--headless")
        self.driver = None

    def start_driver(self):
        if not self.driver:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=self.chrome_options)

    def stop_driver(self):
        if self.driver: self.driver.quit()
        self.driver = None

    def get_article_links(self, main_url, limit=5):
        """
        TUGAS BACKEND: Tulis baris kode untuk mencari link berita di sini.
        """
        self.start_driver()
        self.driver.get(main_url)
        # TODO: Cari link berita menggunakan BeautifulSoup atau driver.find_elements
        return [] # Kembalikan list URL

    def scrape_article(self, url):
        """
        TUGAS BACKEND: Tulis baris kode untuk ambil Judul & Isi di sini.
        """
        self.start_driver()
        self.driver.get(url)
        # TODO: Gunakan BeautifulSoup untuk ambil tag <h1> (Judul) dan <p> (Isi)
        
        # WAJIB MENGIKUTI KONTRAK DATA:
        return {
            "url": url,
            "title": "Hasil Judul",
            "date": datetime.date.today(), # Gunakan parse_date() nanti
            "content": "Hasil Isi Berita"
        }

    def parse_date(self, text):
        """
        TUGAS BACKEND: Ubah teks tanggal jadi objek Date.
        """
        return datetime.date.today()
