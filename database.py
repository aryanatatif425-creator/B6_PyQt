import sqlite3
import pandas as pd
from datetime import datetime

class NewsDatabase:
    def __init__(self, db_name="news_scraper.db"):
        self.db_name = db_name
        self.create_table()

    def create_table(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS articles (
                url TEXT PRIMARY KEY,
                title TEXT,
                publish_date TEXT,
                content TEXT,
                scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()

    def save_article(self, data):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        try:
            # Pastikan publish_date dalam format YYYY-MM-DD untuk kemudahan filter
            cursor.execute('''
                INSERT OR IGNORE INTO articles (url, title, publish_date, content)
                VALUES (?, ?, ?, ?)
            ''', (data['url'], data['title'], data['date'], data['content']))
            conn.commit()
        except Exception as e:
            print(f"Database Error: {e}")
        finally:
            conn.close()

    def get_filtered_articles(self, start_date=None, end_date=None):
        conn = sqlite3.connect(self.db_name)

        query = "SELECT publish_date, title, url FROM articles"
        params = []
        
        if start_date and end_date:
            query += " WHERE publish_date BETWEEN ? AND ?"
            params = [start_date, end_date]
            
        df = pd.read_sql_query(query, conn, params=params)
        conn.close()
        return df

    def export_to_excel(self, file_path, start_date=None, end_date=None):
        try:
            df = self.get_filtered_articles(start_date, end_date)
            df.to_excel(file_path, index=False)
            return True
        except Exception as e:
            print(f"Export Error: {e}")
            return False
