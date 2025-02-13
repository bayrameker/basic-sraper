

```markdown
# Rich Scraper Library Project
```

This project is a comprehensive scraping library that collects and processes data from various sources. It supports multiple scraping modes, including:

- **Google Scraper:** Fetches text from Google search results.
- **Dynamic Scraper:** Uses Selenium to scrape content from dynamic web pages.
- **Realtime Scraper:** Extracts data from real-time feeds (RSS/Atom).
- **Topic Scraper:** Performs a Google search based on a topic and collects related content.
- **Combined Scraper:** First performs a Google search and then uses Newspaper3k to extract article content from the resulting links.

Additionally, the project includes NLP processing, flexible data saving (CSV, JSON, XML), and advanced logging capabilities.

---

## Features

- **Multiple Scraping Modes:**  
  Use different scrapers to fetch data from various sources in one unified project.
  
- **Advanced CAPTCHA Handling:**  
  The Combined Scraper retries automatically (default 3 attempts) if it detects a CAPTCHA. For more natural behavior, consider running without headless mode.
  
- **NLP Processing:**  
  Process fetched text using functions for summarization and lemmatization.
  
- **Data Saving:**  
  Save scraped data in JSON, CSV, or XML formats.
  
- **Dynamic Browser Management:**  
  Uses Selenium with `undetected-chromedriver` to automatically adjust to your installed version of Chrome.
  
- **Flexible Logging:**  
  Configure log levels (DEBUG, INFO, WARNING, ERROR) via command-line parameters.

---

## Requirements

- **Python 3.8+**
- [Selenium](https://pypi.org/project/selenium/)
- [undetected-chromedriver](https://pypi.org/project/undetected-chromedriver/)
- [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/)
- [newspaper3k](https://pypi.org/project/newspaper3k/)
- [spaCy](https://pypi.org/project/spacy/)
- [APScheduler](https://pypi.org/project/APScheduler/)
- [lxml](https://pypi.org/project/lxml/)
- Other dependencies: requests, urllib, re, subprocess, etc.

---

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/scraper_project.git
   cd scraper_project
   ```

2. **Create and Activate a Virtual Environment:**

   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Linux/MacOS:
   source venv/bin/activate
   ```

3. **Install the Required Packages:**

   If you have a `requirements.txt` file:
   ```bash
   pip install -r requirements.txt
   ```
   Otherwise, install the dependencies manually using `pip install` commands.

---

## Usage

Run the project using the main entry point `main.py`. The script accepts several command-line parameters.

### Example Command

To run the Combined Scraper mode:

```bash
python main.py --mode combined --query "morning news" --loglevel DEBUG
```

### Command-line Parameters

- `--mode`  
  The mode to run. Options: `google`, `dynamic`, `realtime`, `topic`, `combined`, or `db`.

- `--query`  
  The search query (required for Google, Topic, and Combined modes).

- `--url`  
  The URL for Dynamic or Realtime modes.

- `--interval`  
  Refresh interval in seconds for Realtime mode (default is 300).

- `--save_format`  
  Data saving format: `json`, `csv`, or `xml`.

- `--output`  
  Output filename for saved data.

- `--loglevel`  
  Log level (`DEBUG`, `INFO`, `WARNING`, or `ERROR`). For example, use `--loglevel DEBUG` for detailed logs.

---

## Project Structure

```
scraper_project/
│
├── main.py                  # Main entry point of the project
├── scrapers/
│   ├── base_scraper.py      # Base class for all scrapers
│   ├── google_scraper.py    # Scraper for Google search results
│   ├── dynamic_scraper.py   # Dynamic web scraper using Selenium
│   ├── realtime_scraper.py  # Real-time data scraper (RSS/Atom)
│   ├── topic_scraper.py     # Topic-based content scraper
│   └── combined_scraper.py  # Combined mode: Google search + Newspaper3k article extraction
│
├── utils/
│   ├── nlp_processing.py    # NLP functions (e.g., summarization, lemmatization)
│   ├── save_data.py         # Functions to save data as CSV, JSON, or XML
│   └── db.py                # Database utilities (optional)
│
├── selenium_manager.py      # Manages Selenium and undetected‑chromedriver sessions
└── README.md                # This file
```

---

## Notes

- **Handling CAPTCHAs:**  
  If the Combined Scraper encounters a CAPTCHA, it will automatically retry up to 3 times. Running without headless mode (`headless=False`) might help simulate human behavior more closely, reducing the chance of CAPTCHA triggers.

- **Browser Version Compatibility:**  
  The `SeleniumManager` automatically detects your installed Chrome version and starts a compatible `undetected-chromedriver` session. If you encounter issues, verify that your Chrome version and driver version match.

---

## Contributing

Contributions are welcome! If you find bugs or have suggestions for improvements, please open an issue or submit a pull request on GitHub.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
```

---