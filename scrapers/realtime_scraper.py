# scrapers/realtime_scraper.py
from apscheduler.schedulers.background import BackgroundScheduler
import requests
from bs4 import BeautifulSoup
from .base_scraper import BaseScraper

class RealtimeScraper(BaseScraper):
    def __init__(self, interval=300):
        self.scheduler = BackgroundScheduler()
        self.interval = interval

    def fetch_data(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "xml")
            items = soup.find_all("item")
            results = []
            for item in items:
                title = item.title.get_text() if item.title else ""
                description = item.description.get_text() if item.description else ""
                results.append({"title": title, "description": description})
            return results
        else:
            print("Error fetching realtime data:", response.status_code)
            return []

    def start_realtime(self, url, job_function):
        def job_wrapper():
            data = self.fetch_data(url)
            job_function(data)
        self.scheduler.add_job(job_wrapper, 'interval', seconds=self.interval)
        self.scheduler.start()

    def stop_realtime(self):
        self.scheduler.shutdown()
