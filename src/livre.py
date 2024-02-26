import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

class Livre:
    def __init__(self, url):
        self.url = url

    def extract_info(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            # Extraction des informations souhaitées
            upc = soup.find('th', string='UPC').find_next('td').text.strip() if soup.find('th', string='UPC') else None
            title = soup.find('h1').text.strip()
            price_including_tax = soup.find('th', string='Price (incl. tax)').find_next('td').text.strip()
            price_excluding_tax = soup.find('th', string='Price (excl. tax)').find_next('td').text.strip()
            number_available = soup.find('th', string='Availability').find_next('td').text.strip()
            product_description = soup.find('meta', attrs={'name': 'description'})['content'].strip() if soup.find('meta', attrs={'name': 'description'}) else None
            review_rating = soup.find('p', class_='star-rating')['class'][1] if soup.find('p', class_='star-rating') else None
            image_url = urljoin(self.url, soup.find('div', class_='item active').img['src'].replace('../../', '')) if soup.find('div', class_='item active') and soup.find('div', class_='item active').img else None

            return {
                'product_page_url': self.url,
                'upc': upc,
                'title': title,
                'price_including_tax': price_including_tax,
                'price_excluding_tax': price_excluding_tax,
                'number_available': number_available,
                'product_description': product_description,
                'review_rating': review_rating,
                'image_url': image_url
            }
