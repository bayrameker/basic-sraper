import logging
from newspaper import Article
from .base_scraper import BaseScraper

class NewspaperScraper(BaseScraper):
    def fetch_data(self, url):
        logging.info(f"NewspaperScraper: {url} üzerinde makale indiriliyor...")
        try:
            article = Article(url)
            article.download()
            article.parse()
            logging.info("NewspaperScraper: Makale başarıyla ayrıştırıldı.")
            return article.text
        except Exception as e:
            logging.error(f"NewspaperScraper: {url} üzerinde hata oluştu: {e}")
            return ""
