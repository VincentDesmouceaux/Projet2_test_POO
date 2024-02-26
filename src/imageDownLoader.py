import os
import requests

class ImageDownloader:
    def __init__(self, destination_folder):
        self.destination_folder = destination_folder
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)

    def download_image(self, image_url, category, title):
        try:
            response = requests.get(image_url)
            if response.status_code == 200:
                image_data = response.content
                safe_title = title.replace('/', '-').replace('\\', '-')  # Pour éviter les problèmes de chemin
                image_name = f"{safe_title}.jpg"
                destination_path = os.path.join(self.destination_folder, category, image_name)
                if not os.path.exists(os.path.join(self.destination_folder, category)):
                    os.makedirs(os.path.join(self.destination_folder, category))
                with open(destination_path, 'wb') as image_file:
                    image_file.write(image_data)
                print(f"Image downloaded: {image_name}")
                return destination_path
        except Exception as e:
            print(f"Error downloading image: {image_url}. {str(e)}")
        return None
