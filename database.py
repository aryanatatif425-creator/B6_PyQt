import sqlite3
import pandas as pd

class NewsDatabase:
    """
    TUGAS DATA ENGINEER:
    Fokus di file ini untuk mengurus penyimpanan data (SQLite & Excel).
    """
    def __init__(self, db_name="news_b6.db"):
        self.db_name = db_name
        self.create_table()

    def create_table(self):
        """
        TUGAS DATA ENGINEER: Buat tabel SQLite di sini.
        """
        conn = sqlite3.connect(self.db_name)
        # TODO: Jalankan perintah CREATE TABLE IF NOT EXISTS
        # Kolom: url (TEXT PRIMARY KEY), title (TEXT), date (TEXT), content (TEXT)
        conn.commit()
        conn.close()

    def save_article(self, data):
        """
        TUGAS DATA ENGINEER: Simpan satu data berita (dict) ke database.
        """
        conn = sqlite3.connect(self.db_name)
        # TODO: Jalankan perintah INSERT OR IGNORE INTO
        conn.commit()
        conn.close()

    def export_to_excel(self, file_path):
        """
        TUGAS DATA ENGINEER: Ambil data dari SQLite lalu simpan ke Excel.
        """
        conn = sqlite3.connect(self.db_name)
        # TODO: Gunakan Pandas read_sql_query dan to_excel
        conn.close()
