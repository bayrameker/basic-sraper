# scrapers/topic_scraper.py
import time
import requests
import urllib.parse
from bs4 import BeautifulSoup
from .base_scraper import BaseScraper
from selenium_manager import SeleniumManager

class TopicScraper(BaseScraper):
    def __init__(self, num_results=3):
        self.num_results = num_results

    def fetch_data(self, query):
        # Sorguyu URL encode ederek Google arama URL'sini oluşturuyoruz.
        encoded_query = urllib.parse.quote(query)
        search_url = f"https://www.google.com/search?q={encoded_query}"

        # SeleniumManager ile tarayıcıyı başlatıyoruz.
        sm = SeleniumManager(headless=True)
        driver = sm.driver
        driver.get(search_url)
        time.sleep(3)
        html = driver.page_source
        sm.quit()

        soup = BeautifulSoup(html, "html.parser")
        links = []
        # Google arama sonuçlarında, linkler genellikle /url?q=... formatında gelir.
        for a in soup.find_all("a", href=True):
            href = a['href']
            if href.startswith("/url?q="):
                actual_url = href.split("/url?q=")[1].split("&")[0]
                actual_url = urllib.parse.unquote(actual_url)
                if actual_url.startswith("http"):
                    links.append(actual_url)
        links = list(dict.fromkeys(links))  # Tekrarlayanları kaldırıyoruz

        results = []
        for link in links[:self.num_results]:
            # Burada içerik için temel bir extraction yapılıyor; NewspaperScraper ayrı içerik alacak.
            try:
                response = requests.get(link, timeout=10)
                response.encoding = response.apparent_encoding
                html = response.text
                soup_link = BeautifulSoup(html, "html.parser")
                title = soup_link.title.get_text(strip=True) if soup_link.title else ""
            except Exception as e:
                title = f"Hata: {e}"
            results.append({"url": link, "title": title})
        return results
