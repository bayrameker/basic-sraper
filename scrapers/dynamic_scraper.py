# scrapers/dynamic_scraper.py
import time
from selenium_manager import SeleniumManager
from .base_scraper import BaseScraper

class DynamicScraper(BaseScraper):
    def fetch_data(self, url):
        sm = SeleniumManager(headless=True)
        driver = sm.driver
        driver.get(url)
        time.sleep(3)
        page_source = driver.page_source
        sm.quit()
        return page_source
