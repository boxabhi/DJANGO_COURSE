import requests
from bs4 import BeautifulSoup
from home.models import News
import os
import uuid
from .tasks import download_image




def scrape_imdb_news():
    url = "https://www.imdb.com/news/movie/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers = headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    news_items = soup.find_all('div', class_='ipc-list-card--border-line')
    for item in news_items:
        title = item.find('a', class_="ipc-link ipc-link--base sc-bec740f7-3 egwFBY")
        description = item.find('div', class_= "ipc-html-content-inner-div")
        image = item.find('img', class_="ipc-image")

        external_link = title['href']
        title = title.text.strip() if title else "No title"
        description = description.text.strip() if title else "No description"
        image = image['src']
        image_path = None

        if image:
            image_name = f"image_{uuid.uuid4()}.jpg"
            image_path = download_image.delay(image, 'downloads/', image_name)

        news = {
            "title" : title,
            "description" : description,
            "image" : image,
            "external_link" : external_link}
        
        News.objects.create(**news)

