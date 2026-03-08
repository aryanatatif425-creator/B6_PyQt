import time
import re
from datetime import datetime
from urllib.parse import urljoin
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
        if headless:
            self.chrome_options.add_argument("--headless")
            self.chrome_options.add_argument("--disable-gpu") # Tambahan dari Hilman agar lebih stabil
        self.driver = None

    def start_driver(self):
        if not self.driver:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=self.chrome_options)

    def stop_driver(self):
        if self.driver:
            self.driver.quit()
        self.driver = None

    def get_article_links(self, main_url, limit=10):
        """
        GENERAL HEURISTIC: Mengambil link berita utama dari homepage/kategori.
        (Nama disesuaikan dengan kontrak tes: get_article_links)
        """
        self.start_driver()
        self.driver.get(main_url)
        time.sleep(3) # Delay sesuai ketentuan
        
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        links = []
        
        # Cari semua tag 'a' yang mengandung link berita
        # Heuristic: Link berita biasanya memiliki kedalaman URL > 2 atau mengandung pola tanggal/read
        for a in soup.find_all('a', href=True):
            href = urljoin(main_url, a['href'])
            
            # Filter agar tidak mengambil link sosial media, iklan, atau anchor (#)
            if any(x in href for x in ['facebook', 'twitter', 'instagram', 'whatsapp', 'linkedin', 'ads']):
                continue
            
            # Pola umum link berita (mengandung read/article/tanggal atau minimal 3 segment path)
            if re.search(r'/(read|article|v|berita|news|detail|[\d]{4}/[\d]{2})/', href) or href.count('/') >= 4:
                if href not in links:
                    links.append(href)
                    if len(links) >= limit:
                        break
        return links

    def scrape_article(self, url):
        """
        GENERAL HEURISTIC: Mengambil konten berita menggunakan meta-tags & tag umum (H1, P).
        """
        self.start_driver()
        self.driver.get(url)
        time.sleep(2) # Delay kesopanan
        
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        
        # 1. Judul (Heuristic: Meta title atau H1 pertama)
        title = ""
        meta_title = soup.find('meta', property='og:title')
        if meta_title:
            title = meta_title['content']
        else:
            h1 = soup.find('h1')
            title = h1.get_text().strip() if h1 else "No Title"

        # 2. Tanggal (Heuristic: Cari di meta tags publish_time)
        pub_date = datetime.now().strftime("%Y-%m-%d") # Fallback today
        date_tags = [
            ('meta', {'property': 'article:published_time'}),
            ('meta', {'name': 'pubdate'}),
            ('meta', {'name': 'publish-date'}),
            ('time', {}),
            ('meta', {'itemprop': 'datePublished'})
        ]
        
        for tag, attrs in date_tags:
            found = soup.find(tag, attrs)
            if found:
                content = found.get('content') or found.get('datetime') or found.get_text()
                # Ekstrak YYYY-MM-DD menggunakan regex
                match = re.search(r'(\d{4}-\d{2}-\d{2})', str(content))
                if match:
                    pub_date = match.group(1)
                    break

        # 3. Konten (Heuristic: Div dengan tag P terbanyak atau tag <article>)
        content_text = ""
        article_tag = soup.find('article')
        if article_tag:
            content_text = "\n".join([p.get_text().strip() for p in article_tag.find_all('p')])
        else:
            # Cari div yang isinya banyak tag p (umumnya body berita)
            divs = soup.find_all('div')
            best_div = max(divs, key=lambda d: len(d.find_all('p')), default=None)
            if best_div:
                content_text = "\n".join([p.get_text().strip() for p in best_div.find_all('p')])

        return {
            "url": url,
            "title": title,
            "date": pub_date,
            "content": content_text[:1000] + "..." if content_text else "No Content"
        }
