import os
import requests
import base64
from bs4 import BeautifulSoup

def imagedown(url, folder):
    if not os.path.isdir(folder):
        os.mkdir(folder)
    
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    for i, img_tag in enumerate(soup.find_all('img'), 1):
        try:
            image_src = img_tag['src']
            if image_src.startswith('data:image'):  # Check if it's a base64-encoded image
                # Extract base64-encoded image data
                image_data = image_src.split(';base64,')[1]
                # Decode base64-encoded image data
                image_binary = base64.b64decode(image_data)
                # Write the image data to a file
                with open(os.path.join(folder, f"{folder}_{i}.webp"), 'wb') as f:
                    f.write(image_binary)
                print(f"Downloaded base64-encoded image {i}")
            else:
                # Download image from URL
                image_url = img_tag['src']
                image_name = f"{folder}_{i}.jpg"
                with open(os.path.join(folder, image_name), 'wb') as f:
                    f.write(requests.get(image_url).content)
                print(f"Downloaded image {i}: {image_url}")
        except KeyError:
            print(f"Skipping image {i}: No 'src' attribute found")

# URLs of webpages containing images
urls = [
    'https://example.com',
]

# Download images from each URL
for index, url in enumerate(urls, 1):
    folder_name = f"gobolt_images_{index}"
    imagedown(url, folder_name)
