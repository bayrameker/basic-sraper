# scrapers/base_scraper.py
from abc import ABC, abstractmethod

class BaseScraper(ABC):
    @abstractmethod
    def fetch_data(self, query_or_url):
        pass
