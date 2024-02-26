from categorie import Categorie
from livre import Livre
import csv
import os

class Scraper:
    def __init__(self, base_url, data_folder):
        self.base_url = base_url
        self.data_folder = data_folder

    def scrape(self):
        # Assurez-vous que le dossier de données existe
        if not os.path.exists(self.data_folder):
            os.makedirs(self.data_folder)

        # Extraction des informations pour toutes les catégories depuis la page d'accueil
        all_category_links = Categorie(self.base_url).extract_links()

        for category_link in all_category_links:
            print(f"Processing category: {category_link}")

            # Créer un dossier pour chaque catégorie
            category_name = category_link.split('/')[-2]
            category_folder = os.path.join(self.data_folder, category_name)
            if not os.path.exists(category_folder):
                os.makedirs(category_folder)

            all_product_links, next_page_link = Categorie(category_link).extract_product_links(category_link)
            while next_page_link:
                additional_links, next_page_link = Categorie(next_page_link).extract_product_links(next_page_link)
                all_product_links.extend(additional_links)

            if not all_product_links:
                print("No product links found for this category.")
                continue

            all_product_info = []
            for product_link in all_product_links:
                print(f"Processing product link: {product_link}")
                product_info = Livre(product_link).extract_info()
                if not product_info:
                    print(f"Error processing product link: {product_link}")
                    continue
                all_product_info.append(product_info)

            if not all_product_info:
                print(f"No product info found for this category: {category_link}")
                continue

            # Sauvegarde des informations dans un fichier CSV
            csv_file = f'{category_name}_books.csv'
            csv_path = os.path.join(category_folder, csv_file)
            with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = all_product_info[0].keys()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for product_info in all_product_info:
                    writer.writerow(product_info)
                print(f"{category_name} books saved to {csv_path}")
