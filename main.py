# main.py
import argparse
import logging
from scrapers.google_scraper import GoogleScraper
from scrapers.dynamic_scraper import DynamicScraper
from scrapers.realtime_scraper import RealtimeScraper
from scrapers.topic_scraper import TopicScraper
from utils.nlp_processing import process_text, summarize_text

# Global liste, realtime modundan toplanan verileri tutar.
realtime_results = []

def run_google_scraper(query):
    gs = GoogleScraper()
    results = gs.fetch_data(query)
    print("Google Scraper Sonuçları:")
    for r in results:
        print(r)
    return results

def run_dynamic_scraper(url):
    ds = DynamicScraper()
    content = ds.fetch_data(url)
    print("Dynamic Scraper İçeriği (ilk 500 karakter):")
    print(content[:500])
    return content

def realtime_job(data):
    global realtime_results
    print("Gerçek Zamanlı İşlem Çalıştı:")
    for item in data:
        title = item.get("title", "")
        description = item.get("description", "")
        processed_title = process_text(title)
        summary = summarize_text(description)
        print(f"\nBaşlık: {title}")
        print(f"İşlenmiş: {processed_title}")
        print(f"Özet: {summary}")
        realtime_results.append({
            "title": title,
            "description": description,
            "processed_title": processed_title,
            "summary": summary
        })
    print("Veriler toplandı.")

def run_realtime_scraper(url, interval):
    rs = RealtimeScraper(interval=interval)
    rs.start_realtime(url, realtime_job)
    print("Gerçek zamanlı scraper başlatıldı. (Ctrl+C ile durdurabilirsiniz.)")
    try:
        while True:
            pass
    except KeyboardInterrupt:
        rs.stop_realtime()
        print("Gerçek zamanlı scraper durduruldu.")

def run_topic_scraper(query):
    ts = TopicScraper()
    results = ts.fetch_data(query)
    print("Topic Scraper Sonuçları:")
    for idx, result in enumerate(results, start=1):
        print(f"({idx}) URL: {result['url']}\n{'-'*60}")
        print(result["content"][:1000])
        print("\n" + "="*80 + "\n")
    return results

def run_combined_scraper(query):
    logging.info("Combined mode için sorgu: '%s' alınıyor...", query)
    from scrapers.combined_scraper import CombinedScraper
    cs = CombinedScraper()  # varsayılan olarak ilk 3 sonucu alır.
    results = cs.fetch_data(query)
    logging.info("Combined mode tamamlandı.")
    return results

def save_data(data, save_format, output):
    from utils.save_data import save_as_csv, save_as_json, save_as_xml
    # Eğer data liste içinde string ise, sözlük yapısına çevir.
    if isinstance(data, list) and data and not isinstance(data[0], dict):
        data = [{"result": d} for d in data]
    if save_format == "json":
        save_as_json(data, output)
    elif save_format == "csv":
        save_as_csv(data, output)
    elif save_format == "xml":
        save_as_xml(data, output)

def main():
    parser = argparse.ArgumentParser(description="Zengin Kütüphane Scraper Projesi")
    parser.add_argument("--mode", choices=["google", "dynamic", "realtime", "db", "topic", "combined"], required=True,
                        help="Çalıştırılacak mod: google, dynamic, realtime, db, topic, combined")
    parser.add_argument("--query", type=str, help="Arama sorgusu (google, topic ve combined modları için)")
    parser.add_argument("--url", type=str, help="URL (dynamic veya realtime modu için)")
    parser.add_argument("--interval", type=int, default=300, help="Gerçek zamanlı modda yenileme aralığı (saniye)")
    parser.add_argument("--save_format", choices=["json", "csv", "xml"], help="Veri kaydetme formatı (json, csv, xml)")
    parser.add_argument("--output", type=str, help="Çıktı dosya adı")
    parser.add_argument("--loglevel", type=str, default="INFO", help="Log seviyesi (DEBUG, INFO, WARNING, ERROR, CRITICAL)")
    args = parser.parse_args()

    # Loglama yapılandırması
    numeric_level = getattr(logging, args.loglevel.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError("Geçersiz log seviyesi: %s" % args.loglevel)
    logging.basicConfig(level=numeric_level, format="%(asctime)s - %(levelname)s - %(message)s")

    scraped_data = None

    if args.mode == "google":
        if not args.query:
            print("Google modu için --query parametresi gereklidir.")
            return
        scraped_data = run_google_scraper(args.query)
    elif args.mode == "dynamic":
        if not args.url:
            print("Dynamic modu için --url parametresi gereklidir.")
            return
        scraped_data = run_dynamic_scraper(args.url)
    elif args.mode == "realtime":
        if not args.url:
            print("Realtime modu için --url parametresi gereklidir.")
            return
        run_realtime_scraper(args.url, args.interval)
        scraped_data = realtime_results
    elif args.mode == "topic":
        if not args.query:
            print("Topic modu için --query parametresi gereklidir.")
            return
        scraped_data = run_topic_scraper(args.query)
    elif args.mode == "combined":
        if not args.query:
            print("Combined modu için --query parametresi gereklidir.")
            return
        scraped_data = run_combined_scraper(args.query)
    elif args.mode == "db":
        print("DB modu seçildi. Ancak DB kaydı yerine dosya kaydı tercih ediliyor.")
        scraped_data = []  # İsteğe bağlı

    if scraped_data and args.save_format and args.output:
        save_data(scraped_data, args.save_format, args.output)

if __name__ == "__main__":
    main()
