# chrome_driver.py
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def get_chrome_driver(headless=True, additional_options=None):
    """
    ChromeDriver'ı başlatır ve döndürür.
    - headless: Tarayıcıyı görünmez modda çalıştırır.
    - additional_options: Ek argüman listesi (örneğin, "--window-size=1920,1080")
    """
    options = Options()
    if headless:
        options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    
    if additional_options:
        for opt in additional_options:
            options.add_argument(opt)
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver
