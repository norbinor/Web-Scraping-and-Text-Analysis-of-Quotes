import requests
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
import string

nltk.download('punkt')
nltk.download('stopwords')

class QuotesScraper:
    def __init__(self, url):
        self.url = url

    def scrape_quotes(self):
        """Scrapes quotes and authors from the webpage."""
        page = requests.get(self.url)
        soup = BeautifulSoup(page.content, 'html.parser')
        quotes_elements = soup.find_all('div', class_='quote')
        quotes = []
        for quote_element in quotes_elements:
            text = quote_element.find('span', class_='text').text
            author = quote_element.find('small', class_='author').text
            quotes.append((text, author))
        return quotes

    def clean_and_tokenize(self, quote):
        """Cleans and tokenizes quote text."""
        # Remove punctuation
        quote = quote.translate(str.maketrans('', '', string.punctuation))
        # Tokenize
        tokens = word_tokenize(quote)
        # Remove stopwords
        tokens = [word for word in tokens if word.lower() not in stopwords.words('english')]
        return tokens

    def frequency_analysis(self, quotes):
        """Performs a simple frequency analysis on the words in the quotes."""
        all_words = []
        for quote, _ in quotes:
            tokens = self.clean_and_tokenize(quote)
            all_words.extend(tokens)
        return Counter(all_words).most_common()

if __name__ == "__main__":
    url = 'https://quotes.toscrape.com/'  # Example website for demonstration purposes
    scraper = QuotesScraper(url)
    quotes = scraper.scrape_quotes()
    word_frequencies = scraper.frequency_analysis(quotes)
    print("Most common words in quotes:")
    for word, freq in word_frequencies[:10]:  # Display top 10 most common words
        print(f"{word}: {freq}")
