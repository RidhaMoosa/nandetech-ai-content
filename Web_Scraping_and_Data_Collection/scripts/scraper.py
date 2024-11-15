import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

class WebScraper:
    def __init__(self, base_url, headers=None):
        self.base_url = base_url
        self.headers = headers if headers else {'User-Agent': 'Mozilla/5.0'}
        self.data = [] 

    def fetch_page(self, endpoint=""):
        """Fetch HTML content from the given URL."""
        url = f"{self.base_url}/{endpoint}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.text

    def parse(self, html):
        """Parse HTML content with BeautifulSoup and extract the desired data."""
        soup = BeautifulSoup(html, 'html.parser')
        quotes = soup.findAll('span', attrs={'class': 'text'})
        authors = soup.findAll('small', attrs={'class': 'author'})

        for quote, author in zip(quotes, authors):
            self.data.append({
                "QUOTES": quote.text,
                "AUTHORS": author.text
            })

    def save_to_csv(self, filename="data/output.csv"):
        """Save the extracted data to a CSV file."""
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        df = pd.DataFrame(self.data)
        df.to_csv(filename, index=False)
        print(f"Data saved to {filename}")

    def run(self, endpoint=""):
        """Run the scraper."""
        html = self.fetch_page(endpoint)
        self.parse(html)
        self.save_to_csv()
