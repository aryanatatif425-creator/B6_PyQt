import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QTableWidget, QProgressBar, QLabel, 
                             QLineEdit, QPushButton, QHeaderView)
from PyQt6.QtCore import QThread, pyqtSignal

# MENGHUBUNGKAN KERJAAN TIM (Import file lokal)
try:
    from scraper import NewsScraper
    from database import NewsDatabase
except ImportError:
    print("PERINGATAN: File scraper.py atau database.py belum lengkap!")

class ScraperThread(QThread):
    """
    ENGINE (KOKI): Menjalankan proses di background.
    """
    progress = pyqtSignal(int)
    article_scraped = pyqtSignal(dict) # Sinyal kirim data per berita
    finished = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, url, limit):
        super().__init__()
        self.url = url
        self.limit = limit
        self.scraper = NewsScraper()
        self.db = NewsDatabase()

    def run(self):
        try:
            self.progress.emit(10)
            
            # 1. Ambil Link (Panggil fungsi milik Backend)
            links = self.scraper.get_article_links(self.url, self.limit)
            
            total = len(links)
            if total == 0:
                self.error.emit("Tidak ditemukan link berita.")
                return

            for i, link in enumerate(links):
                # 2. Ambil Isi Berita (Panggil fungsi milik Backend)
                data = self.scraper.scrape_article(link)
                
                # 3. Simpan ke Database (Panggil fungsi milik Data Engineer)
                self.db.save_article(data)
                
                # 4. Kirim ke UI (Tugas Lead Dev)
                self.article_scraped.emit(data)
                
                # Update progress bar
                p_val = 10 + int((i + 1) / total * 90)
                self.progress.emit(p_val)

            self.scraper.stop_driver()
            self.progress.emit(100)
            self.finished.emit()
        except Exception as e:
            self.error.emit(str(e))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("B6 News Scraper Pro")
        self.resize(1000, 600)
        self.init_ui()
        self.load_styles()

    def init_ui(self):
        """
        TUGAS FRONTEND DESIGNER:
        Tulis format tampilan (Widget, Tombol, Tabel) di sini.
        """
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # --- BAGIAN INPUT (TODO: Frontend percantik di sini) ---
        input_layout = QHBoxLayout()
        self.url_input = QLineEdit("https://www.kompas.com/")
        self.scrape_btn = QPushButton("Mulai Scraping")
        self.scrape_btn.clicked.connect(self.start_scraping)
        
        input_layout.addWidget(QLabel("URL Target:"))
        input_layout.addWidget(self.url_input)
        input_layout.addWidget(self.scrape_btn)
        layout.addLayout(input_layout)

        # --- BAGIAN PROGRESS (Tugas Lead Dev) ---
        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)

        # --- BAGIAN TABEL (TODO: Frontend atur kolom di sini) ---
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Tanggal", "Judul Berita", "URL"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.table)

        # --- TOMBOL EKSPOR (TODO: Frontend tambah tombol Excel di sini) ---
        self.export_btn = QPushButton("Ekspor ke Excel")
        layout.addWidget(self.export_btn)

    def load_styles(self):
        """
        TUGAS FRONTEND: Membaca file CSS/QSS.
        """
        try:
            with open("styles.qss", "r") as f:
                self.setStyleSheet(f.read())
        except:
            pass

    def start_scraping(self):
        url = self.url_input.text()
        self.thread = ScraperThread(url, 5) # Default limit 5 berita
        self.thread.progress.connect(self.progress_bar.setValue)
        self.thread.article_scraped.connect(self.add_to_table)
        self.thread.start()

    def add_to_table(self, data):
        """
        TUGAS FRONTEND: Cara menampilkan data ke tabel.
        """
        row = self.table.rowCount()
        self.table.insertRow(row)
        # Sesuai Kontrak Data: url, title, date, content
        self.table.setItem(row, 0, QTableWidgetItem(str(data['date'])))
        self.table.setItem(row, 1, QTableWidgetItem(data['title']))
        self.table.setItem(row, 2, QTableWidgetItem(data['url']))

if __name__ == "__main__":
    from PyQt6.QtWidgets import QTableWidgetItem # Import lokal untuk fungsi add_to_table
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
