import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup

class Categorie:
    def __init__(self, url):
        self.url = url

    def extract_category_links(self):
        links = []
        response = requests.get(self.url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            category_div = soup.find('div', class_='side_categories')
            if category_div:
                links = [urljoin(self.url, a['href']) for a in category_div.find_all('a')]
        return links

    def extract_product_links(self, category_url):
        links = []
        response = requests.get(category_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            product_divs = soup.find_all('h3')
            links = [urljoin(category_url, div.a['href']) for div in product_divs]
            next_page = soup.find('li', class_='next')
            next_page_link = urljoin(category_url, next_page.a['href']) if next_page and next_page.a else None
            return links, next_page_link
        return links, None
