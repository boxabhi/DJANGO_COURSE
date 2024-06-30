from celery import shared_task
import time
import os
import requests

@shared_task
def add(x, y):
    time.sleep(15)
    return x + y

@shared_task
def download_image(image_url , save_directory, image_name):
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)
    image_path = os.path.join(save_directory, image_name)
    response = requests.get(image_url, stream=True)
    if response.status_code == 200:
        with open(image_path, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
    
    return image_url
from .models import News

@shared_task
def create_news():
    News.objects.create(
        title = "title",
        description = "description",
        image ="https://chatgpt.com/c/d6c16fe5-b3c4-4392-b5e0-b2d52c7c5bb0",
        external_link = "https://chatgpt.com/c/d6c16fe5-b3c4-4392-b5e0-b2d52c7c5bb0"
    )