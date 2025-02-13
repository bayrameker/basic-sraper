# scrapers/google_scraper.py
import requests
from bs4 import BeautifulSoup
from .base_scraper import BaseScraper

class GoogleScraper(BaseScraper):
    def __init__(self):
        self.base_url = "https://www.google.com/search?q="

    def fetch_data(self, query):
        url = self.base_url + query
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/90.0.4430.85 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        results = []
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            for g in soup.find_all("div", class_="BNeawe"):
                results.append(g.get_text())
        else:
            print(f"Hata: {response.status_code}")
        return results
