import re
import subprocess
import sys
import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import SessionNotCreatedException

class SeleniumManager:
    def __init__(self, headless=True):
        self.options = Options()
        if headless:
            self.options.add_argument("--headless")
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--disable-dev-shm-usage")
        self.options.add_argument("--ignore-certificate-errors")
        # İsterseniz user-agent, otomasyon bayrakları vb. ek seçenekler burada da ayarlanabilir.
        self.driver = self._init_driver()

    def _get_chrome_version(self):
        try:
            if sys.platform.startswith("win"):
                process = subprocess.Popen(
                    ["reg", "query", r"HKEY_CURRENT_USER\Software\Google\Chrome\BLBeacon", "/v", "version"],
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
                )
                stdout, _ = process.communicate()
                version_match = re.search(r"\d+\.\d+\.\d+\.\d+", stdout.decode())
                if version_match:
                    version_str = version_match.group()
                    return int(version_str.split(".")[0])
            elif sys.platform.startswith("darwin"):
                process = subprocess.Popen(
                    ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "--version"],
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE
                )
                stdout, _ = process.communicate()
                version_match = re.search(r"\d+\.\d+\.\d+\.\d+", stdout.decode())
                if version_match:
                    return int(version_match.group().split(".")[0])
            else:
                process = subprocess.Popen(
                    ["google-chrome", "--version"],
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE
                )
                stdout, _ = process.communicate()
                version_match = re.search(r"\d+\.\d+\.\d+\.\d+", stdout.decode())
                if version_match:
                    return int(version_match.group().split(".")[0])
        except Exception:
            return None
        return None

    def _init_driver(self):
        chrome_version = self._get_chrome_version() or 108
        try:
            driver = uc.Chrome(options=self.options, version_main=chrome_version)
        except SessionNotCreatedException as e:
            msg = str(e)
            version_match = re.search(r"Current browser version is (\d+)", msg)
            if version_match:
                version = int(version_match.group(1))
                driver = uc.Chrome(options=self.options, version_main=version)
            else:
                raise e
        return driver

    def quit(self):
        if self.driver:
            try:
                self.driver.quit()
            except Exception:
                pass
            finally:
                try:
                    self.driver.__class__.__del__ = lambda x: None
                except Exception:
                    pass
