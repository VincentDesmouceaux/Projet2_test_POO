from src.scraper import Scraper

def main():
    base_url = "https://books.toscrape.com/index.html"
    data_folder = "data"  # Spécifiez le chemin où vous souhaitez sauvegarder les fichiers CSV
    scraper = Scraper(base_url, data_folder)
    scraper.scrape()

if __name__ == "__main__":
    main()
