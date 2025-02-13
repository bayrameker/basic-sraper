import time
import urllib.parse
import logging
from bs4 import BeautifulSoup
from newspaper import Article
from selenium_manager import SeleniumManager

class CombinedScraper:
    def __init__(self, num_results=3, max_attempts=3, headless=False):
        """
        :param num_results: Çekilecek makale sayısı
        :param max_attempts: CAPTCHA durumunda yapılacak maksimum deneme sayısı
        :param headless: Gerçek tarayıcı modunu kullanmak için headless mod kapalı (False)
        """
        self.num_results = num_results
        self.max_attempts = max_attempts
        self.headless = headless  # Gerçek kullanıcı davranışı için headless kapalı
        self.logger = logging.getLogger(__name__)
        # Gerçekçi bir user-agent belirliyoruz.
        self.user_agent = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/115.0.0.0 Safari/537.36"
        )

    def _init_driver(self):
        # SeleniumManager, tarayıcınızın sürümünü tespit edip uygun driver'ı yükleyecektir.
        sm = SeleniumManager(headless=self.headless)
        driver = sm.driver
        # Gerçek kullanıcı davranışını taklit etmek için user-agent ve navigator.webdriver gizleme komutlarını ekliyoruz.
        driver.execute_cdp_cmd(
            'Page.addScriptToEvaluateOnNewDocument',
            {'source': '''
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
            '''}
        )
        return sm, driver

    def fetch_data(self, query):
        self.logger.info("CombinedScraper: Sorgu: '%s'", query)
        encoded_query = urllib.parse.quote(query)
        search_url = f"https://www.google.com/search?q={encoded_query}"
        self.logger.debug("CombinedScraper: Search URL: %s", search_url)

        sm, driver = self._init_driver()

        attempts = 0
        html = ""
        while attempts < self.max_attempts:
            driver.get(search_url)
            time.sleep(3)  # Sayfanın tam yüklenmesi için bekleme
            # Gerçek kullanıcı davranışını simüle etmek adına sayfada kaydırma yapıyoruz.
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight/3);")
            time.sleep(1)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
            time.sleep(1)
            
            html = driver.page_source
            lower_html = html.lower()
            if ("captcha" in lower_html) or ("recaptcha" in lower_html) or ("our systems have detected unusual traffic" in lower_html):
                self.logger.warning(
                    "CombinedScraper: CAPTCHA tespit edildi. Yeniden deniyor... (Deneme %d/%d)",
                    attempts + 1, self.max_attempts
                )
                attempts += 1
                time.sleep(5)
            else:
                break

        sm.quit()

        if attempts == self.max_attempts and (("captcha" in lower_html) or ("recaptcha" in lower_html)):
            self.logger.error("CombinedScraper: CAPTCHA engeli nedeniyle sonuç alınamıyor.")
            return []

        soup = BeautifulSoup(html, "html.parser")
        links = []
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if href.startswith("/url?q="):
                actual_url = href.split("/url?q=")[1].split("&")[0]
                actual_url = urllib.parse.unquote(actual_url)
                if actual_url.startswith("http"):
                    links.append(actual_url)
        # Tekrar eden linkleri kaldırıyoruz.
        links = list(dict.fromkeys(links))
        self.logger.info("CombinedScraper: Bulunan link sayısı: %d", len(links))

        results = []
        count = 0
        for link in links:
            if count >= self.num_results:
                break
            self.logger.info("CombinedScraper: İşleniyor: %s", link)
            try:
                article = Article(link)
                article.download()
                article.parse()
                results.append({
                    "url": link,
                    "title": article.title,
                    "content": article.text
                })
                count += 1
            except Exception as e:
                self.logger.error("CombinedScraper: Hata link %s -> %s", link, str(e))
        return results
