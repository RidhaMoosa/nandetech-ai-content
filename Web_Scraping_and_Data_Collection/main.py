# main.py

from scripts.scraper import WebScraper

if __name__ == "__main__":
    
    scraper = WebScraper(base_url="https://quotes.toscrape.com")
    scraper.run()
