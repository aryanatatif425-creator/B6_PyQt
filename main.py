import sys
import os
import webbrowser
from datetime import datetime
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QTableWidget, QProgressBar, QLabel, 
                             QLineEdit, QPushButton, QHeaderView, QTableWidgetItem,
                             QMessageBox, QFileDialog, QDateEdit, QFrame)
from PyQt6.QtCore import QThread, pyqtSignal, Qt, QDate

# Impor file lokal
try:
    from scraper import NewsScraper
    from database import NewsDatabase
except ImportError:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from scraper import NewsScraper
    from database import NewsDatabase

class ScraperThread(QThread):
    progress = pyqtSignal(int)
    log_msg = pyqtSignal(str)
    article_scraped = pyqtSignal(dict)
    finished = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, url, limit, start_date, end_date):
        super().__init__()
        self.url = url
        self.limit = limit
        self.start_date = start_date
        self.end_date = end_date
        self.scraper = NewsScraper(headless=True)
        self.db = NewsDatabase()

    def run(self):
        try:
            self.log_msg.emit(f"Connecting to: {self.url}...")
            self.progress.emit(10)
            
            links = self.scraper.get_links(self.url, self.limit)
            total = len(links)
            
            if total == 0:
                self.error.emit("No valid news links found.")
                return

            self.log_msg.emit(f"Found {total} links. Processing...")

            scraped_count = 0
            for i, link in enumerate(links):
                data = self.scraper.scrape_article(link)
                
                article_date = data['date']
                if self.start_date <= article_date <= self.end_date:
                    self.db.save_article(data)
                    self.article_scraped.emit(data)
                    scraped_count += 1
                    self.log_msg.emit(f"Success: {data['title'][:50]}...")
                else:
                    self.log_msg.emit(f"Skipped (Wrong Date): {data['title'][:50]}...")
                
                p_val = 10 + int((i + 1) / total * 90)
                self.progress.emit(p_val)

            self.scraper.stop_driver()
            self.log_msg.emit(f"Done! {scraped_count} articles added.")
            self.progress.emit(100)
            self.finished.emit()
        except Exception as e:
            self.error.emit(str(e))
            if self.scraper: self.scraper.stop_driver()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("B6 News Scrapper") # JUDUL BARU
        self.resize(1100, 750)
        self.db = NewsDatabase()
        self.init_ui()
        self.load_styles()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # TITLE SECTION
        title_label = QLabel("B6 NEWS SCRAPPER") # JUDUL BARU
        title_label.setStyleSheet("font-size: 26px; font-weight: bold; color: #10b981;")
        layout.addWidget(title_label)

        # TOP BAR
        top_bar = QHBoxLayout()
        self.url_input = QLineEdit("https://www.kompas.com/")
        self.url_input.setPlaceholderText("Enter Target URL...")
        
        self.limit_input = QLineEdit("10")
        self.limit_input.setFixedWidth(60)
        self.limit_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.scrape_btn = QPushButton("START SCRAPING")
        self.scrape_btn.setFixedWidth(180)
        self.scrape_btn.clicked.connect(self.start_scraping)
        
        top_bar.addWidget(QLabel("URL Target:"))
        top_bar.addWidget(self.url_input)
        top_bar.addWidget(QLabel("Limit:"))
        top_bar.addWidget(self.limit_input)
        top_bar.addWidget(self.scrape_btn)
        layout.addLayout(top_bar)

        # FILTER BAR
        filter_bar = QHBoxLayout()
        filter_bar.addWidget(QLabel("Date Range:"))
        
        today = QDate.currentDate()
        self.start_date_edit = QDateEdit(today.addDays(-7))
        self.start_date_edit.setCalendarPopup(True)
        self.end_date_edit = QDateEdit(today)
        self.end_date_edit.setCalendarPopup(True)
        
        filter_bar.addWidget(self.start_date_edit)
        filter_bar.addWidget(QLabel("to"))
        filter_bar.addWidget(self.end_date_edit)
        filter_bar.addStretch()
        
        self.export_btn = QPushButton("EXPORT EXCEL")
        self.export_btn.setObjectName("export_btn")
        self.export_btn.setFixedWidth(150)
        self.export_btn.clicked.connect(self.export_data)
        filter_bar.addWidget(self.export_btn)
        layout.addLayout(filter_bar)

        # SEPARATOR
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet("background-color: #1e293b;")
        layout.addWidget(line)

        # PROGRESS SECTION
        self.log_label = QLabel("Status: Ready")
        self.log_label.setStyleSheet("color: #94a3b8; font-style: italic;")
        layout.addWidget(self.log_label)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedHeight(12)
        layout.addWidget(self.progress_bar)

        # TABLE SECTION
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Date", "Headline", "Link Source"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setShowGrid(False)
        self.table.setAlternatingRowColors(True)
        self.table.setFocusPolicy(Qt.FocusPolicy.NoFocus) # Matikan efek focus bawaan
        self.table.setStyleSheet("QTableWidget { gridline-color: transparent; }")
        
        # FITUR KLIK 2X (DOUBLE CLICK)
        self.table.itemDoubleClicked.connect(self.open_link)
        
        layout.addWidget(self.table)

    def load_styles(self):
        style_path = os.path.join(os.path.dirname(__file__), "styles.qss")
        if os.path.exists(style_path):
            with open(style_path, "r") as f:
                self.setStyleSheet(f.read())

    def open_link(self, item):
        """Membuka link berita di browser saat diklik dua kali pada baris mana saja."""
        row = item.row()
        url_item = self.table.item(row, 2) # Kolom ke-2 adalah URL
        if url_item:
            url = url_item.text()
            webbrowser.open(url)

    def start_scraping(self):
        url = self.url_input.text().strip()
        if not url:
            QMessageBox.warning(self, "Error", "Please enter a URL first!")
            return
            
        limit = int(self.limit_input.text()) if self.limit_input.text().isdigit() else 10
        start_d = self.start_date_edit.date().toString("yyyy-MM-dd")
        end_d = self.end_date_edit.date().toString("yyyy-MM-dd")

        self.scrape_btn.setEnabled(False)
        self.scrape_btn.setText("SCRAPING...")
        self.table.setRowCount(0)
        
        self.thread = ScraperThread(url, limit, start_d, end_d)
        self.thread.progress.connect(self.progress_bar.setValue)
        self.thread.log_msg.connect(self.log_label.setText)
        self.thread.article_scraped.connect(self.add_to_table)
        self.thread.finished.connect(self.on_finished)
        self.thread.error.connect(self.on_error)
        self.thread.start()

    def add_to_table(self, data):
        row = self.table.rowCount()
        self.table.insertRow(row)
        self.table.setItem(row, 0, QTableWidgetItem(data['date']))
        self.table.setItem(row, 1, QTableWidgetItem(data['title']))
        self.table.setItem(row, 2, QTableWidgetItem(data['url']))

    def on_finished(self):
        self.scrape_btn.setEnabled(True)
        self.scrape_btn.setText("START SCRAPING")
        self.log_label.setText("Status: Completed")
        QMessageBox.information(self, "Success", "Scraping completed!")

    def on_error(self, msg):
        self.scrape_btn.setEnabled(True)
        self.scrape_btn.setText("START SCRAPING")
        QMessageBox.critical(self, "Error", f"Failed: {msg}")

    def export_data(self):
        start_d = self.start_date_edit.date().toString("yyyy-MM-dd")
        end_d = self.end_date_edit.date().toString("yyyy-MM-dd")
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Export File", "", "Excel (*.xlsx)")
        
        if file_path:
            if self.db.export_to_excel(file_path, start_d, end_d):
                QMessageBox.information(self, "Success", f"Data exported to {file_path}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()